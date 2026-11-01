"""Guard the locked-test, evidence and review-record wiring (instructions only)."""

from __future__ import annotations

import unittest
from pathlib import Path

import tomllib

ROOT = Path(__file__).resolve().parents[4]
EXPECTED = {
    "bmad-testarch-atdd": (
        "LOCKED TESTS",
        "validate_story_contract.py lock",
        "Contract CI Wiring",
        "CI NAMING CHECK",
        "contract and full test identity",
        "in one edit",
    ),
    "bmad-build": ("Implementation session", "skip markers", "edit guard refuses"),
    "bmad-build-auto": (
        "Implementation session",
        "locked test change requires",
        "edit guard refuses",
    ),
    "bmad-code-review": (
        "### Review Record",
        "cannot review its own work",
        "--junit <report>",
        "done/review story still requires delivered validation",
        "exact Contract ID",
    ),
    "bmad-correct-course": ("LOCKED TESTS", "re-locked", "/contract-unlock"),
    "bmad-testarch-test-review": (
        "LOCKED TESTS AND EVIDENCE",
        "existing project files",
    ),
    "bmad-testarch-trace": ("--junit",),
    "bmad-testarch-ci": (
        "validate_story_contract.py ci",
        "PROVE IT",
        "testcase contract property",
    ),
    "bmad-testarch-framework": (
        "`val`",
        "Contract CI Wiring",
        "testcase `contract` property",
        "`test-file`/`test-id`",
    ),
}


def steps(path: Path) -> str:
    workflow = tomllib.loads(path.read_text())["workflow"]
    return " ".join(workflow.get("activation_steps_append", []))


class ProvenanceGuidanceTests(unittest.TestCase):
    def test_shared_workflows_carry_the_provenance_steps(self) -> None:
        for name, phrases in EXPECTED.items():
            text = steps(ROOT / f"_bmad/custom/{name}.toml")
            for phrase in phrases:
                with self.subTest(workflow=name, phrase=phrase):
                    self.assertIn(phrase, text)

    def test_overlays_that_replace_a_workflow_keep_its_steps(self) -> None:
        for overlay in sorted((ROOT / "projects").glob("*/_bmad/custom")):
            for name, phrases in EXPECTED.items():
                path = overlay / f"{name}.toml"
                if path.exists():
                    with self.subTest(overlay=str(path.relative_to(ROOT))):
                        for phrase in phrases:
                            self.assertIn(phrase, steps(path))

    def test_ar_records_contract_and_test_identity_per_suite(self) -> None:
        paths = [ROOT / "_bmad/custom/agent-readiness-workflow.md"]
        paths += sorted(
            (ROOT / "projects").glob("*/_bmad/custom/agent-readiness-workflow.md")
        )
        for path in paths:
            text = " ".join(path.read_text().split())
            with self.subTest(path=str(path.relative_to(ROOT))):
                self.assertIn("testcase `contract` identity", text)
                self.assertIn("full `test-file`/`test-id` export", text)

    def test_contract_standard_documents_the_new_sections(self) -> None:
        text = (ROOT / "_bmad/custom/story-contract.md").read_text()
        for phrase in (
            "### Locked Tests",
            "### Review Record",
            "## Locked ATDD tests",
            "## Delivery provenance",
            "skip markers ignored",
            "validate_story_contract.py lock",
            "## CI results",
            "## Edit guard (Pi)",
            "/contract-unlock",
            "validate_story_contract.py ci",
            "named `val`",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
