"""Approval-anchor and provenance checks against real temporary jj repositories.

jj-dependent tests skip when jj is unavailable (set BMAD_JJ_BIN to point at it).
"""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
VALIDATOR = SCRIPTS / "validate_story_contract.py"
JJ = os.environ.get("BMAD_JJ_BIN", "jj")


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


validator = load("validate_story_contract_anchor", VALIDATOR)
fixtures = load(
    "story_contract_fixtures",
    Path(__file__).with_name("test_validate_story_contract.py"),
)
SPEC_PATH = "_bmad-output/implementation-artifacts/spec-1-2-profile.md"
TEST_PATH = "tests/api/profile.py"  # VAL-1's planned check in the fixture spec
SCAFFOLD = (
    "import pytest\n\n\n@pytest.mark.skip(reason='red phase: VAL-1')\n"
    "def test_save():\n    assert save_profile({'name': 'Ada'}) == 'saved'\n"
)
ACTIVE = SCAFFOLD.replace("@pytest.mark.skip(reason='red phase: VAL-1')\n", "")
WEAKENED = ACTIVE.replace("save_profile({'name': 'Ada'}) == 'saved'", "True")
IMPLEMENTATION_SESSION = "impl-3f1c9a2e"
REVIEW_SESSION = "review-8b7d6e5f"


def jj_available() -> bool:
    try:
        result = subprocess.run([JJ, "--version"], capture_output=True, check=False)
    except OSError:
        return False
    return result.returncode == 0


def digest(text: str) -> str:
    return validator.contract_digest(
        validator.ContractDocument.from_text(Path("spec.md"), text)
    )


def locks(test_text: str = SCAFFOLD) -> str:
    return (
        "### Locked Tests\n\n| Path | Lock digest |\n| --- | --- |\n"
        f"| {TEST_PATH} | {validator.lock_digest(test_text)} |\n\n"
    )


def approve(text: str, approver: str = "Product Owner", *, lock: str = "") -> str:
    lock = lock or locks()
    return (
        text.replace("- Status: draft", "- Status: approved")
        .replace("- Approved by: pending", f"- Approved by: {approver}")
        .replace(
            "- Validation approved by: pending",
            "- Validation approved by: Test Architect",
        )
        .replace("- Approved at: pending", "- Approved at: 2026-07-29T12:00:00Z")
        .replace("- Contract digest: pending", f"- Contract digest: {digest(text)}")
        .replace(
            "- Validation artifacts: pending",
            "- Validation artifacts: _bmad-output/test-artifacts/atdd-checklist-1-2.md",
        )
        .replace("\n## Delivery Evidence", "\n" + lock + "## Delivery Evidence", 1)
    )


def deliver(
    approved: str,
    *,
    evidence: str = "_bmad-output/test-artifacts/val-1-output.txt",
    review_session: str = REVIEW_SESSION,
    review_record: bool = True,
) -> str:
    """The spec as Code Review leaves it: results, review record, session notes."""
    start = approved.index("### Validation Results")
    end = approved.index("### Exceptions")
    results = (
        "### Validation Results\n\n| VAL ID | Result | Evidence | Build or run |\n"
        "| --- | --- | --- | --- |\n"
        f"| VAL-1 | PASS | {evidence} | commit:abc123 |\n"
        "| VAL-2 | PASS | review/profile-observation.md | ci:456 |\n\n"
    )
    record = (
        "### Review Record\n\n- Reviewed by: Daniel (human reviewer)\n"
        f"- Review session: {review_session}\n- Reviewed at: 2026-07-30T09:00:00Z\n\n"
        if review_record
        else ""
    )
    text = approved[:start] + results + approved[end:]
    return text.replace(
        "\n## Implementation Notes\n",
        "\n" + record + "## Implementation Notes\n\n"
        f"- Implementation session: {IMPLEMENTATION_SESSION}\n",
        1,
    )


def trailers(text: str, revision: str = "1", approver: str = "Product Owner") -> str:
    return (
        "chore(story-1.2): approve acceptance contract\n\n"
        "Contract-ID: STORY-1.2\n"
        f"Contract-Revision: {revision}\n"
        f"Contract-Spec: {SPEC_PATH}\n"
        f"Contract-Digest: {digest(text)}\n"
        f"Approved-by: {approver}\n"
        "Validation-approved-by: Test Architect\n"
    )


class ValidatorRun(unittest.TestCase):
    root: Path
    spec: Path
    env: dict[str, str]

    def write(self, relative: str, text: str) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def validate(self, phase: str = "approved", *extra: str) -> dict:
        result = subprocess.run(
            [sys.executable, str(VALIDATOR), "validate", "--phase", phase, "--json"]
            + list(extra)
            + [str(self.spec)],
            capture_output=True,
            text=True,
            env=self.env,
            check=False,
        )
        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 0 if payload["valid"] else 1)
        return payload

    def assert_error(self, payload: dict, fragment: str) -> None:
        self.assertFalse(payload["valid"])
        self.assertTrue(
            any(fragment in error for error in payload["errors"]), payload["errors"]
        )


@unittest.skipUnless(jj_available(), "jj is not available (set BMAD_JJ_BIN)")
class JjApprovalAnchorTests(ValidatorRun):
    def setUp(self) -> None:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        config = self.root.parent / f"{self.root.name}-jj.toml"
        config.write_text('[user]\nname = "Tester"\nemail = "tester@example.invalid"\n')
        self.addCleanup(config.unlink)
        self.env = {**os.environ, "JJ_CONFIG": str(config), "BMAD_JJ_BIN": JJ}
        self.jj("git", "init", "--quiet", ".")
        self.spec = self.root / SPEC_PATH
        self.draft = fixtures.BUILD_SPEC
        self.approved = approve(self.draft)
        self.write(SPEC_PATH, self.draft)
        self.jj("describe", "--quiet", "-m", "docs(story-1.2): plan contract")
        self.jj("new", "--quiet")
        self.write(TEST_PATH, SCAFFOLD)
        self.jj("describe", "--quiet", "-m", "test(story-1.2): add acceptance tests")
        self.jj("new", "--quiet")

    def jj(self, *args: str) -> None:
        subprocess.run([JJ, *args], cwd=self.root, env=self.env, check=True)

    def record_approval(self, text: str, message: str, *, seal: bool = True) -> None:
        self.spec.write_text(text)
        self.jj("describe", "--quiet", "-m", message)
        if seal:
            self.jj("new", "--quiet")

    def approve_and_seal(self) -> None:
        self.record_approval(self.approved, trailers(self.draft))

    # Approval anchor
    def test_sealed_approval_change_passes(self) -> None:
        self.approve_and_seal()
        self.assertEqual([], self.validate()["errors"])

    def test_recomputed_digest_is_rejected(self) -> None:
        self.approve_and_seal()
        changed = self.approved.replace(
            "Users can save a valid profile.", "Users can replace a valid profile."
        )
        old = f"- Contract digest: {digest(self.draft)}"
        self.spec.write_text(
            changed.replace(old, f"- Contract digest: {digest(changed)}")
        )
        payload = self.validate()
        self.assert_error(payload, "differs from the version approved in jj change")
        self.assertFalse(any("digest does not match" in e for e in payload["errors"]))

    def test_file_only_approval_is_rejected_in_a_jj_workspace(self) -> None:
        self.spec.write_text(self.approved)
        self.assert_error(self.validate(), "no jj approval change")

    def test_unsealed_approval_is_rejected(self) -> None:
        self.record_approval(self.approved, trailers(self.draft), seal=False)
        self.assert_error(self.validate(), "run `jj new` to seal it")

    def test_approval_change_must_touch_only_the_spec(self) -> None:
        self.write("src.py", "print('implementation')\n")
        self.approve_and_seal()
        self.assert_error(self.validate(), "must change only")

    def test_second_approval_for_same_revision_is_ambiguous(self) -> None:
        self.approve_and_seal()
        self.record_approval(self.approved + "\n", trailers(self.draft))
        self.assert_error(self.validate(), "approval is ambiguous")

    def test_swapped_approver_is_rejected(self) -> None:
        self.approve_and_seal()
        self.spec.write_text(
            self.approved.replace(
                "- Approved by: Product Owner", "- Approved by: Agent"
            )
        )
        self.assert_error(self.validate(), "differs from the value approved")

    def test_trailer_must_match_recorded_content(self) -> None:
        wrong = trailers(self.draft).replace(digest(self.draft), "sha256:" + "0" * 64)
        self.record_approval(self.approved, wrong)
        self.assert_error(self.validate(), "Contract-Digest trailer does not match")

    def test_new_revision_needs_its_own_approval(self) -> None:
        self.approve_and_seal()
        revised = self.draft.replace("- Revision: 1", "- Revision: 2")
        self.spec.write_text(approve(revised))
        self.assert_error(self.validate(), "revision 2")
        self.jj("describe", "--quiet", "-m", trailers(revised, revision="2"))
        self.jj("new", "--quiet")
        self.assertEqual([], self.validate()["errors"])

    # Locked ATDD tests (#4)
    def test_activating_the_scaffold_keeps_the_lock(self) -> None:
        self.approve_and_seal()
        self.write(TEST_PATH, ACTIVE)
        self.assertEqual([], self.validate()["errors"])

    def test_weakened_test_needs_reapproval(self) -> None:
        self.approve_and_seal()
        self.write(TEST_PATH, WEAKENED)
        self.assert_error(self.validate(), "locked test changed since approval")

    def test_relocking_after_approval_is_rejected(self) -> None:
        self.approve_and_seal()
        self.write(TEST_PATH, WEAKENED)
        self.spec.write_text(
            self.approved.replace(
                validator.lock_digest(SCAFFOLD), validator.lock_digest(WEAKENED)
            )
        )
        payload = self.validate()
        self.assert_error(payload, "Locked Tests differ from those recorded")
        self.assertFalse(any("locked test changed" in e for e in payload["errors"]))

    def test_fabricated_lock_at_approval_is_rejected(self) -> None:
        fabricated = approve(self.draft, lock=locks(WEAKENED))
        self.record_approval(fabricated, trailers(self.draft))
        self.write(TEST_PATH, WEAKENED)
        self.assert_error(self.validate(), "does not match the test as approved")

    def test_tracked_contract_must_lock_planned_tests(self) -> None:
        unlocked = approve(self.draft, lock="### Locked Tests\n\n- None.\n\n")
        self.record_approval(unlocked, trailers(self.draft))
        self.assert_error(self.validate(), "planned test file is not locked")

    # Delivery provenance (#3, #7)
    def deliver_story(self, **options: object) -> dict:
        self.approve_and_seal()
        self.write(TEST_PATH, ACTIVE)
        self.write("_bmad-output/test-artifacts/val-1-output.txt", "1 passed\n")
        self.write("review/profile-observation.md", "Observed error; data unchanged.\n")
        self.spec.write_text(deliver(self.approved, **options))  # type: ignore[arg-type]
        return self.validate("delivered")

    def test_complete_delivery_passes(self) -> None:
        self.assertEqual([], self.deliver_story()["errors"])

    def test_skipped_planned_test_fails_delivery(self) -> None:
        payload = self.deliver_story()
        self.assertTrue(payload["valid"], payload["errors"])
        self.write(TEST_PATH, SCAFFOLD)
        self.assert_error(self.validate("delivered"), "is skipped")

    def test_missing_planned_test_fails_delivery(self) -> None:
        self.deliver_story()
        self.write(TEST_PATH, ACTIVE.replace("test_save", "test_store"))
        self.assert_error(self.validate("delivered"), "not found in")

    def test_fabricated_evidence_path_fails_delivery(self) -> None:
        payload = self.deliver_story(evidence="ci-logs/run-9999.txt")
        self.assert_error(payload, "references a missing file: ci-logs/run-9999.txt")

    def test_self_review_fails_delivery(self) -> None:
        payload = self.deliver_story(review_session=IMPLEMENTATION_SESSION)
        self.assert_error(payload, "reviewed by the session that wrote it")

    def test_missing_review_record_fails_delivery(self) -> None:
        payload = self.deliver_story(review_record=False)
        self.assert_error(payload, "needs a '### Review Record'")


class WithoutJjTests(ValidatorRun):
    """Outside jj, provenance checks still run; only the approval anchor falls back."""

    def setUp(self) -> None:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        (self.root / "_bmad").mkdir()
        self.env = dict(os.environ)
        self.spec = self.root / SPEC_PATH
        self.write(TEST_PATH, SCAFFOLD)
        self.write(SPEC_PATH, approve(fixtures.BUILD_SPEC))

    def test_require_jj_fails_outside_a_workspace(self) -> None:
        self.assertEqual([], self.validate()["errors"])
        self.assert_error(self.validate("approved", "--require-jj"), "not inside a jj")

    def test_locks_still_checked_without_jj(self) -> None:
        self.write(TEST_PATH, WEAKENED)
        self.assert_error(self.validate(), "locked test changed since approval")

    def test_lock_command_prints_the_table(self) -> None:
        result = subprocess.run(
            [sys.executable, str(VALIDATOR), "lock", str(self.spec)],
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn(
            f"| {TEST_PATH} | {validator.lock_digest(SCAFFOLD)} |", result.stdout
        )

    def test_no_project_root_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            spec = Path(directory) / "spec.md"
            spec.write_text(approve(fixtures.BUILD_SPEC))
            self.spec = spec
            self.assert_error(self.validate(), "cannot find the project root")


if __name__ == "__main__":
    unittest.main()
