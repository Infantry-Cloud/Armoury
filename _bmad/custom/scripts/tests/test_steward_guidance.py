"""Guardrail Steward wiring: agent skill, roster entry, hooks and sync deployment."""

from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

import tomllib

ROOT = Path(__file__).resolve().parents[4]
SKILL = ROOT / ".agents/skills/bmad-agent-steward"


def block(path: Path) -> dict:
    data = tomllib.loads(path.read_text())
    return data.get("agent", data.get("workflow", {}))


class StewardGuidanceTests(unittest.TestCase):
    def test_agent_skill_is_complete(self) -> None:
        text = (SKILL / "SKILL.md").read_text()
        self.assertIn("name: bmad-agent-steward", text)
        for phrase in (
            "Collaborate, don't decree",
            "Steward Decisions",
            "steward_scan.py",
            "Post-review analysis (RV)",
            "Why the guardrails exist",
            "Blind spots",
            "Friction alone never justifies removing",
        ):
            self.assertIn(phrase, text)
        agent = block(SKILL / "customize.toml")
        self.assertEqual(
            {"AR", "HC", "RV", "BG", "FA", "SK"}, {m["code"] for m in agent["menu"]}
        )
        self.assertTrue(all("prompt" in m for m in agent["menu"]))
        self.assertIn(
            "file:{project-root}/docs/agent-readiness.md", agent["persistent_facts"]
        )

    def test_agent_is_on_the_roster(self) -> None:
        config = tomllib.loads((ROOT / "_bmad/custom/config.toml").read_text())
        entry = config["agents"]["bmad-agent-steward"]
        self.assertEqual(("Vera", "Guardrail Steward"), (entry["name"], entry["title"]))

    def test_workflows_hand_off_to_the_steward(self) -> None:
        expected = {
            "bmad-build": "activation_steps_append",
            "bmad-build-auto": "activation_steps_append",
            "bmad-code-review": "on_complete",
            "bmad-retrospective": "on_complete",
            "bmad-agent-dev": "principles",
        }
        trees = [
            ROOT / "_bmad/custom",
            *sorted((ROOT / "projects").glob("*/_bmad/custom")),
        ]
        for tree in trees:
            for name, key in expected.items():
                path = tree / f"{name}.toml"
                if path.exists():
                    with self.subTest(path=str(path.relative_to(ROOT))):
                        value = block(path)[key]
                        text = value if isinstance(value, str) else " ".join(value)
                        self.assertIn("bmad-agent-steward", text)
            review = tree / "bmad-code-review.toml"
            if review.exists():
                self.assertIn("RV <spec_file>", block(review)["on_complete"])
        for context in (
            ROOT / "project-context.md",
            *ROOT.glob("projects/*/project-context.md"),
        ):
            self.assertIn("## Guardrail Steward", context.read_text())

    def test_no_branch_protection_or_hosted_ci_assumed(self) -> None:
        paths = [
            *(ROOT / "_bmad/custom").glob("bmad-*.toml"),
            ROOT / "_bmad/custom/story-contract.md",
            SKILL / "SKILL.md",
        ]
        for path in paths:
            with self.subTest(path=path.name):
                self.assertNotIn("branch protection", path.read_text().casefold())

    @unittest.skipUnless(
        (ROOT / "sync.sh").is_file(), "shared-repo test: needs sync.sh"
    )
    def test_sync_deploys_the_skill_without_touching_installed_skills(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            dest = Path(directory)
            (dest / "_bmad").mkdir()
            installed = dest / ".agents/skills/bmad-agent-dev/SKILL.md"
            installed.parent.mkdir(parents=True)
            installed.write_text("installed")
            run = ["bash", str(ROOT / "sync.sh")]
            subprocess.run(
                [*run, "--dry-run", str(dest)], capture_output=True, check=True
            )
            self.assertFalse((dest / ".agents/skills/bmad-agent-steward").exists())
            subprocess.run([*run, str(dest)], capture_output=True, check=True)
            deployed = dest / ".agents/skills/bmad-agent-steward"
            self.assertEqual(
                (SKILL / "SKILL.md").read_bytes(), (deployed / "SKILL.md").read_bytes()
            )
            self.assertEqual("installed", installed.read_text())
            self.assertTrue((dest / ".agents/skills/bmad-linear/SKILL.md").exists())
            guard = dest / ".pi/extensions/contract-guard.ts"
            self.assertEqual(
                (ROOT / ".pi/extensions/contract-guard.ts").read_bytes(),
                guard.read_bytes(),
            )


if __name__ == "__main__":
    unittest.main()
