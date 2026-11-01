"""Universal context stays small; operating manuals are required at their point of use.

These test loading declarations, not whether an LLM obeys the instructions.
"""

from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

import tomllib

from _bmad.custom.scripts.jj_wiring import (
    LEGACY_JJ_FACT,
    PROCEDURE_FACTS,
    WALKTHROUGH,
    add_fact,
    wire,
)

ROOT = Path(__file__).resolve().parents[4]
PROJECT_CONTEXT = "file:{project-root}/project-context.md"


def configurations() -> list[Path]:
    return [
        *sorted((ROOT / "_bmad/custom").glob("bmad-*.toml")),
        *sorted((ROOT / "projects").glob("*/_bmad/custom/bmad-*.toml")),
        ROOT / ".agents/skills/bmad-agent-steward/customize.toml",
    ]


class InstructionLoadingTests(unittest.TestCase):
    def test_universal_context_is_short_and_keeps_the_invariants(self) -> None:
        for path in (
            ROOT / "project-context.md",
            *ROOT.glob("projects/*/project-context.md"),
        ):
            text = path.read_text()
            with self.subTest(context=str(path.relative_to(ROOT))):
                # Selected project facts travel to the root context when an overlay is synced.
                budget = 1000 if "## Project-specific decisions" in text else 800
                self.assertLessEqual(len(text.split()), budget)
                for phrase in (
                    "Never invent product or Test Architect",
                    "Use jj, never git",
                    "Never bypass a check",
                    "CI provider",
                    "change -> check -> diagnostic -> correction -> recheck",
                    "readiness.md",
                    "stop if it is missing",
                ):
                    self.assertIn(phrase.casefold(), " ".join(text.split()).casefold())

    def test_facts_load_universal_context_not_full_operating_manuals(self) -> None:
        for path in configurations():
            data = tomllib.loads(path.read_text())
            block = data.get("agent", data.get("workflow", {}))
            facts = block.get("persistent_facts")
            if facts is None:  # deprecated dev-story halts immediately
                continue
            with self.subTest(config=str(path.relative_to(ROOT))):
                self.assertEqual(1, facts.count(PROJECT_CONTEXT))
                for name, instruction in PROCEDURE_FACTS.items():
                    self.assertNotIn(
                        f"file:{{project-root}}/_bmad/custom/{name}", facts
                    )
                    if any(name in fact for fact in facts):
                        self.assertEqual(1, facts.count(instruction))
                        self.assertIn("Before", instruction)
                        self.assertIn("read", instruction)
                        self.assertIn("completely", instruction)

    def test_full_references_exist_and_keep_the_operating_guidance(self) -> None:
        for name in PROCEDURE_FACTS:
            self.assertTrue((ROOT / "_bmad/custom" / name).is_file(), name)
        for context in (
            ROOT / "project-context.md",
            *ROOT.glob("projects/*/project-context.md"),
        ):
            reference = context.parent / "_bmad/custom/project-guidance.md"
            text = reference.read_text()
            with self.subTest(reference=str(reference.relative_to(ROOT))):
                for heading in (
                    "## Story contracts",
                    "## Linear project workflow",
                    "## Version control (jj)",
                    "## Guardrail Steward",
                    "## Agent readiness",
                ):
                    self.assertIn(heading, text)
                self.assertIn("Feedback Loop Register", text)
                self.assertIn("Agent capabilities are clone-ready", text)
                self.assertIn("_bmad/custom/project-guidance.md", context.read_text())

    def test_strata_environment_remains_always_loaded(self) -> None:
        path = ROOT / "projects/strata/project-context.md"
        if not path.exists():
            self.skipTest("no Strata overlay in this installation")
        text = " ".join(path.read_text().split())
        for decision in (
            "native host + mise, by explicit user decision",
            "Do not create or require devcontainers",
            "owner-accepted risk",
            "Do not repurpose/weaken the existing rootless Podman machine",
            "AD-30/AD-31 or release gates",
        ):
            self.assertIn(decision, text)

    def test_jj_wiring_does_not_reintroduce_eager_loading(self) -> None:
        original = "[agent]\npersistent_facts = [\n" + LEGACY_JJ_FACT + "]\n"
        upgraded = add_fact(original)
        self.assertNotIn(LEGACY_JJ_FACT, upgraded)
        facts = tomllib.loads(upgraded)["agent"]["persistent_facts"]
        self.assertEqual([PROCEDURE_FACTS["jj-vcs.md"]], facts)
        self.assertEqual(upgraded, add_fact(upgraded))
        walkthrough = tomllib.loads(WALKTHROUGH)["workflow"]["persistent_facts"]
        self.assertIn(PROJECT_CONTEXT, walkthrough)
        self.assertIn(PROCEDURE_FACTS["jj-vcs.md"], walkthrough)

    def test_wiring_is_idempotent_for_the_split_context(self) -> None:
        for base in (ROOT, *sorted((ROOT / "projects").glob("*"))):
            if not (base / "_bmad/custom").is_dir():
                continue
            with (
                self.subTest(project=str(base.relative_to(ROOT))),
                tempfile.TemporaryDirectory() as directory,
            ):
                destination = Path(directory)
                custom = destination / "_bmad/custom"
                shutil.copytree(
                    base / "_bmad/custom",
                    custom,
                    ignore=shutil.ignore_patterns("__pycache__", ".ruff_cache"),
                )
                context = destination / "project-context.md"
                shutil.copy2(base / "project-context.md", context)
                self.assertEqual([], wire(custom, context))


if __name__ == "__main__":
    unittest.main()
