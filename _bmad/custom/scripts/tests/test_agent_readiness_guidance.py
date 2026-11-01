"""Guard the shared AR instructions; these checks do not measure real agent performance."""

from __future__ import annotations

import unittest
from pathlib import Path

import tomllib

ROOT = Path(__file__).resolve().parents[4]


@unittest.skipUnless((ROOT / "sync.sh").is_file(), "shared-repo test: needs sync.sh")
class AgentReadinessGuidanceTests(unittest.TestCase):
    def workflow(self) -> str:
        return (ROOT / "_bmad/custom/agent-readiness-workflow.md").read_text()

    def test_correction_loop_is_the_deliverable_not_a_tool_inventory(self) -> None:
        text = self.workflow()
        self.assertIn(
            "## Purpose — improve agentic programming through mechanical feedback", text
        )
        self.assertIn(
            "change -> triggered deterministic check -> agent-visible diagnostic -> correction -> fresh recheck",
            text,
        )
        self.assertIn("not a tooling checklist or a high rubric score", text)
        self.assertIn("which agreed risk or programming failure does it address", text)
        self.assertIn("Feedback Loop Register", text)
        self.assertIn("do not install\nsomething for every pillar", text)
        artifact = " ".join(
            text.split("PHASE 2 — ARTIFACT", 1)[1].split("PHASE 3", 1)[0].split()
        )
        self.assertIn("risk/principle-led feedback-loop strategy", artifact)
        self.assertIn("Feedback Loop Register the primary delivery plan", artifact)
        self.assertIn("not-needed + reason", artifact)
        self.assertNotIn("pillar-by-pillar strategy", artifact)

    def test_rehearsal_requires_fault_diagnostic_repair_and_fresh_result(self) -> None:
        text = self.workflow()
        rehearsal = text.split("PROVE THE LOOP FROM THE AGENT'S POINT OF VIEW", 1)[1]
        rehearsal = rehearsal.split(
            "Configure the selected CI feedback integration", 1
        )[0]
        for requirement in (
            "passing baseline",
            "known fault",
            "normal edit/check trigger",
            "diagnostic in the channel the coding agent uses",
            "elapsed time",
            "without weakening the oracle or disabling a gate",
            "rerun the same check freshly",
            "confirm it passes",
            "A direct CLI test alone does not prove an automatic hook",
            "never production resources, secrets or an altered approved contract",
            "applicable critical gaps still prevent ready",
        ):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, rehearsal)

    def test_score_is_secondary_without_waiving_threshold_or_protected_gates(
        self,
    ) -> None:
        text = self.workflow()
        scoring = text.split("Then ASSESS COVERAGE", 1)[1]
        for requirement in (
            "coverage\ndiagnostic, not the objective",
            "Never add irrelevant tooling",
            "Do not declare ready below the agreed threshold",
            "do not silently lower the threshold or waive a required control",
            "failure/repair evidence",
            "These instructions are soft policy",
            "protected gates",
            "proven failure/repair loops",
        ):
            with self.subTest(requirement=requirement):
                self.assertIn(requirement, scoring)
        self.assertIn("validate_story_contract.py", text)
        self.assertIn("_bmad/custom/linear-workflow.md", text)
        linear = " ".join(
            (ROOT / "_bmad/custom/linear-workflow.md").read_text().split()
        )
        self.assertIn("proven applicable correction loops", linear)
        self.assertIn("agent-visible failure/repair evidence", linear)
        self.assertIn("high score alone is not Done", linear)

    def test_all_ar_entry_points_share_the_same_purpose_and_recipe(self) -> None:
        prompts: list[str] = []
        for name in ("bmad-agent-architect", "bmad-agent-dev", "bmad-tea"):
            config = tomllib.loads((ROOT / f"_bmad/custom/{name}.toml").read_text())
            entries = [item for item in config["agent"]["menu"] if item["code"] == "AR"]
            self.assertEqual(len(entries), 1)
            entry = entries[0]
            self.assertIn("mechanical feedback loops", entry["description"])
            self.assertIn("agent-readiness-workflow.md", entry["prompt"])
            self.assertIn(
                "not checklist completion or score maximisation", entry["prompt"]
            )
            self.assertIn("If the file is missing", entry["prompt"])
            prompts.append(entry["prompt"])
        self.assertEqual(len(set(prompts)), 1)

    def test_shared_and_strata_context_preserve_purpose_and_environment_choices(
        self,
    ) -> None:
        paragraphs: list[str] = []
        for relative in ("project-context.md", "projects/strata/project-context.md"):
            context_path = ROOT / relative
            always_loaded = context_path.read_text()
            self.assertIn("_bmad/custom/project-guidance.md", always_loaded)
            reference = context_path.parent / "_bmad/custom/project-guidance.md"
            text = reference.read_text()
            readiness = text.split(
                "## Agent readiness (the environment makes the agent effective)", 1
            )[1]
            purpose = readiness.split("AR is downstream of product planning", 1)[0]
            self.assertIn("Feedback Loop Register", purpose)
            self.assertIn("failure -> diagnosis -> repair -> fresh pass", purpose)
            self.assertIn("never sufficient for ready", purpose)
            self.assertIn(
                "full aggregate/CI backstop and independent manual assurance", purpose
            )
            self.assertIn("explicit product and Test Architect", " ".join(text.split()))
            paragraphs.append(purpose)
        self.assertEqual(paragraphs[0], paragraphs[1])
        strata = (ROOT / "projects/strata/project-context.md").read_text()
        self.assertIn("native host + mise, by explicit user decision", strata)
        self.assertIn("Do not create\nor require devcontainers", strata)

    def test_readiness_entry_gates_require_loop_proof_without_per_story_rehearsals(
        self,
    ) -> None:
        for name in (
            "bmad-agent-dev",
            "bmad-build",
            "bmad-build-auto",
            "bmad-code-review",
        ):
            with self.subTest(gate=name):
                config = tomllib.loads((ROOT / f"_bmad/custom/{name}.toml").read_text())
                section = config.get("agent", config.get("workflow"))
                assert isinstance(section, dict)
                instructions = " ".join(
                    section.get("activation_steps_prepend", [])
                    + section.get("activation_steps_append", [])
                )
                for requirement in (
                    "or lacks documented representative failure/repair evidence",
                    "or has an unproven applicable critical loop",
                    "Reuse current recorded evidence",
                    "not for every story",
                    "agreed environment boundary and applicable critical controls",
                    "agreed score threshold",
                ):
                    self.assertIn(requirement, instructions)

    def test_review_asks_for_actual_feedback_not_score_only_assurance(self) -> None:
        for name in ("bmad-tea", "bmad-code-review"):
            config = tomllib.loads((ROOT / f"_bmad/custom/{name}.toml").read_text())
            section = config.get("agent", config.get("workflow"))
            assert isinstance(section, dict)
            instructions = " ".join(section["activation_steps_append"])
            self.assertIn("Feedback Loop Register", instructions)
            self.assertIn("measured latency", instructions)
            self.assertIn("diagnostic", instructions)
            self.assertIn("fresh", instructions)
        review = tomllib.loads(
            (ROOT / "_bmad/custom/bmad-code-review.toml").read_text()
        )["workflow"]
        self.assertIn("delivered-phase validation", review["on_complete"])
        self.assertIn("protected gates", " ".join(review["activation_steps_append"]))


if __name__ == "__main__":
    unittest.main()
