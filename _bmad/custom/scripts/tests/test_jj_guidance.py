"""Guard the jj wiring; these checks do not run jj or prove agent behaviour."""

from __future__ import annotations

import unittest
from pathlib import Path

import tomllib

from _bmad.custom.scripts.jj_wiring import PROCEDURE_FACTS

ROOT = Path(__file__).resolve().parents[4]
CUSTOM = ROOT / "_bmad/custom"
JJ_FACT = PROCEDURE_FACTS["jj-vcs.md"]
WIRED = (
    "bmad-agent-dev",
    "bmad-build",
    "bmad-build-auto",
    "bmad-code-review",
    "bmad-testarch-atdd",
    "bmad-testarch-automate",
    "bmad-testarch-test-review",
    "bmad-qa-generate-e2e-tests",
    "bmad-correct-course",
    "bmad-sprint-planning",
    "bmad-retrospective",
    "bmad-walkthrough",
    "bmad-testarch-test-design",
    "bmad-testarch-trace",
    "bmad-testarch-ci",
    "bmad-testarch-framework",
    "bmad-prd",
    "bmad-architecture",
    "bmad-create-epics-and-stories",
    "bmad-tea",
    "bmad-agent-architect",
)


def section(path: Path) -> dict:
    data = tomllib.loads(path.read_text())
    block = data.get("agent", data.get("workflow"))
    if not isinstance(block, dict):
        raise TypeError(f"{path.name}: no [agent] or [workflow] table")
    return block


class JjGuidanceTests(unittest.TestCase):
    def test_guide_keeps_hard_rules_and_contract_order(self) -> None:
        text = " ".join((CUSTOM / "jj-vcs.md").read_text().split())
        for phrase in (
            "Never run `git` commands",
            "The only mutating jj commands an agent may run are `jj new` and `jj describe`",
            "Never silently initialise jj or fall back to Git",
            "Build planning -> ATDD and explicit approvals -> Build implementation -> independent review",
            "do not use it alone to scope a story review",
            "Never execute it, and do not suggest a push",
            "Do not assume Seeker's `feature/epic-*` convention",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_every_vcs_touching_workflow_loads_the_guide_before_work(self) -> None:
        for name in WIRED:
            path = CUSTOM / f"{name}.toml"
            if not path.exists():
                continue  # installs may not carry every shared override
            with self.subTest(workflow=name):
                self.assertIn(JJ_FACT, section(path)["persistent_facts"])

    def test_stage_instructions_and_bookmark_ownership(self) -> None:
        def steps(name: str) -> str:
            block = section(CUSTOM / f"{name}.toml")
            return " ".join(block.get("activation_steps_append", [])) + block.get(
                "on_complete", ""
            )

        self.assertIn("approved-phase contract validation passes", steps("bmad-build"))
        self.assertIn("never recommend a bookmark", steps("bmad-build"))
        self.assertIn("jj workspace unavailable", steps("bmad-build-auto"))
        self.assertIn("add acceptance tests", steps("bmad-testarch-atdd"))
        review = steps("bmad-code-review")
        self.assertIn("full verified story range", review)
        self.assertIn("Never run bookmark or push commands", review)
        self.assertNotIn("git changes", review)

    def test_approval_is_its_own_sealed_change_everywhere_it_is_recorded(self) -> None:
        def steps(name: str) -> str:
            return " ".join(
                section(CUSTOM / f"{name}.toml").get("activation_steps_append", [])
            )

        atdd = steps("bmad-testarch-atdd")
        self.assertIn("JJ APPROVAL", atdd)
        self.assertIn("run `jj new` to seal it", atdd)
        self.assertIn("approval is never part of this change", atdd)
        self.assertNotIn("explicitly approved contract/approval edits", atdd)
        self.assertIn("micro-contracts", steps("bmad-build"))
        self.assertIn(
            "never create or edit an approval change", steps("bmad-build-auto")
        )
        self.assertIn("never fix it by editing approval", steps("bmad-code-review"))
        self.assertIn("new sealed approval change", steps("bmad-correct-course"))
        self.assertIn("--require-jj", steps("bmad-testarch-trace"))
        contract = " ".join((CUSTOM / "story-contract.md").read_text().split())
        for phrase in (
            "## Approval change (jj)",
            "Contract-Revision: 1",
            "Validation-approved-by:",
            "--require-jj",
            "not *who* approved it",
        ):
            self.assertIn(phrase, contract)
        guide = (CUSTOM / "jj-vcs.md").read_text()
        self.assertIn("`jj describe` only ever targets `@`", guide)
        self.assertIn(
            "--require-jj", (CUSTOM / "agent-readiness-workflow.md").read_text()
        )

    def test_project_context_and_overlays_stay_wired(self) -> None:
        contexts = [ROOT / "project-context.md"]
        overlays = sorted((ROOT / "projects").glob("*/_bmad/custom"))
        contexts += [path.parents[1] / "project-context.md" for path in overlays]
        for context in contexts:
            if context.exists():
                with self.subTest(context=str(context.relative_to(ROOT))):
                    self.assertIn("## Version control (jj)", context.read_text())
        for overlay in overlays:
            for name in WIRED:
                path = overlay / f"{name}.toml"
                if path.exists():
                    with self.subTest(overlay=str(path.relative_to(ROOT))):
                        self.assertIn(JJ_FACT, section(path)["persistent_facts"])


if __name__ == "__main__":
    unittest.main()
