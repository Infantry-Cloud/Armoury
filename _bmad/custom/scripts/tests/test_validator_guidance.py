"""Recovery references are additive: original validator errors and verdicts stay intact."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from _bmad.custom.scripts import validate_story_contract as validator
from _bmad.custom.scripts.tests import test_jj_approval_anchor as examples

ROOT = Path(__file__).resolve().parents[4]
MANUAL = ROOT / "_bmad/custom/story-contract.md"
SCRIPT = MANUAL.parent / "scripts/validate_story_contract.py"


class DiagnosticReferenceTests(unittest.TestCase):
    def test_known_errors_point_at_the_relevant_full_sections(self) -> None:
        cases = {
            "locked test changed since approval: tests/example.py": "locked-atdd-tests",
            "Locked Tests differ from those recorded in approval change abc": "locked-atdd-tests",
            "Acceptance Contract changed after approval; digest does not match": "approval-change-jj",
            "no jj approval change for STORY-1.2 revision 1": "approval-change-jj",
            "VAL-1 was skipped in CI ('test_save')": "ci-results",
            "CI ran 'test_save' but nothing ties the result to VAL-1": "ci-results",
            "Review session matches an implementation session": "delivery-provenance",
            "VAL-1 evidence references a missing file: results.txt": "delivery-provenance",
            "VAL-2 is WAIVED without a complete exception": "delivery-provenance",
            "it changes the approved 'Acceptance Contract' section": "edit-guard-pi",
            "Open Questions must be resolved before approval": "contract-rules",
            "missing required section: Acceptance Contract": "required-spec-shape",
        }
        for message, section in cases.items():
            with self.subTest(error=message):
                self.assertIn(
                    f"{validator.CONTRACT_MANUAL}#{section}",
                    validator.documentation_references(message),
                )

    def test_every_link_targets_an_existing_manual_heading(self) -> None:
        document = validator.ContractDocument.load(MANUAL)
        anchors = {
            re.sub(r"[^\w\s-]", "", section.title.casefold()).replace(" ", "-")
            for section in document.sections
        }
        for _, sections in validator.ERROR_SECTIONS:
            for section in sections:
                self.assertIn(section, anchors)

    def test_unknown_errors_require_the_full_manual(self) -> None:
        message = "An unfamiliar condition has occurred"
        payload: dict[str, object] = {"errors": [message], "valid": False}
        validator.attach_guidance(payload, [message])
        self.assertEqual([message], payload["errors"])
        self.assertFalse(payload["valid"])
        self.assertEqual(
            [{"error": message, "references": [validator.CONTRACT_MANUAL]}],
            payload["guidance"],
        )
        self.assertIn("read the full", str(payload["recovery"]))
        self.assertIn("ask the user or Vera", str(payload["recovery"]))
        self.assertIn("Do not bypass", str(payload["recovery"]))


class DiagnosticCliTests(unittest.TestCase):
    def setUp(self) -> None:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        (self.root / "_bmad").mkdir()
        self.spec = self.write(
            examples.SPEC_PATH, examples.approve(examples.fixtures.BUILD_SPEC)
        )
        self.write(examples.TEST_PATH, examples.SCAFFOLD)

    def write(self, relative: str, content: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
        return path

    def run_cli(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *arguments],
            cwd=self.root,
            capture_output=True,
            text=True,
            check=False,
        )

    def break_locked_test(self) -> None:
        self.write(examples.TEST_PATH, examples.WEAKENED)

    def test_json_preserves_failure_and_adds_references(self) -> None:
        self.break_locked_test()
        original_errors, _ = validator.run_validation(self.spec, "approved")
        result = self.run_cli(
            "validate", "--phase", "approved", "--json", str(self.spec)
        )
        data = json.loads(result.stdout)
        self.assertEqual(1, result.returncode)
        self.assertFalse(data["valid"])
        self.assertEqual(original_errors, data["errors"])
        self.assertEqual(data["errors"], [item["error"] for item in data["guidance"]])
        self.assertIn("#locked-atdd-tests", str(data["guidance"]))

    def test_plain_text_failure_names_the_section_and_stop_rule(self) -> None:
        self.break_locked_test()
        result = self.run_cli("validate", "--phase", "approved", str(self.spec))
        self.assertEqual(1, result.returncode)
        self.assertIn("locked test changed since approval", result.stdout)
        self.assertIn(
            f"Read: {validator.CONTRACT_MANUAL}#locked-atdd-tests", result.stdout
        )
        self.assertIn("Do not bypass the failed check", result.stdout)

    def test_valid_json_output_has_no_spurious_recovery(self) -> None:
        result = self.run_cli(
            "validate", "--phase", "approved", "--json", str(self.spec)
        )
        self.assertEqual(0, result.returncode, result.stderr)
        data = json.loads(result.stdout)
        self.assertTrue(data["valid"])
        self.assertEqual([], data["errors"])
        self.assertNotIn("guidance", data)

    def test_ci_reports_keep_the_same_failure_and_recovery(self) -> None:
        self.break_locked_test()
        result = self.run_cli("ci", "--json")
        data = json.loads(result.stdout)
        self.assertEqual(1, result.returncode)
        contract = data["contracts"][0]
        self.assertEqual("approved", contract["phase"])
        self.assertIn("#locked-atdd-tests", str(contract["guidance"]))
        self.assertIn("Do not bypass", contract["recovery"])
        text = self.run_cli("ci")
        self.assertEqual(1, text.returncode)
        self.assertIn("Read:", text.stdout)

    def test_guard_refusal_is_unchanged_but_has_recovery_references(self) -> None:
        proposed = self.write(
            "proposed.md",
            self.spec.read_text().replace(
                "Users can save a valid profile.", "Users can replace it."
            ),
        )
        result = self.run_cli("guard", "--proposed", str(proposed), str(self.spec))
        data = json.loads(result.stdout)
        self.assertEqual(
            0, result.returncode
        )  # guard reports a verdict, not a validation exit code
        self.assertFalse(data["allowed"])
        self.assertIn("#edit-guard-pi", str(data["guidance"]))

    def test_unreadable_input_preserves_io_exit_code_and_full_reference(self) -> None:
        result = self.run_cli(
            "validate", "--phase", "approved", str(self.root / "missing.md")
        )
        self.assertEqual(2, result.returncode)
        self.assertIn(f"Read: {validator.CONTRACT_MANUAL}", result.stderr)
        self.assertIn("Do not bypass", result.stderr)


if __name__ == "__main__":
    unittest.main()
