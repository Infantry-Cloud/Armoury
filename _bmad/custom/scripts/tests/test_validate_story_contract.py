from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).parents[1] / "validate_story_contract.py"
SPEC = importlib.util.spec_from_file_location("validate_story_contract", MODULE_PATH)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validator
SPEC.loader.exec_module(validator)


DRAFT = """# Story 1.2: Contract example

Status: ready-for-dev

## Acceptance Contract

- Contract ID: STORY-1.2
- Revision: 1
- Risk: medium

### Intent

Users can save a valid profile.

### Scope

- In scope: profile save
- Out of scope: avatar upload

### Sources

- [Source: docs/prd.md#FR-1]

### Assumptions and Dependencies

- Existing authenticated user fixture.

### Acceptance Criteria

- AC-1 [P0]: Given a valid profile, when it is saved, then the persisted profile is observable.
- AC-2 [P1]: Given invalid input, when save is attempted, then no data is changed and an error is shown.

### Validation Design

| VAL ID | Covers | Method | Level | Planned check or procedure | Expected evidence | Owner | Manual reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| VAL-1 | AC-1 | mechanical | API | tests/api/profile.py::test_save | Passing assertion and response log | Dev | - |
| VAL-2 | AC-2 | manual | demonstration | Submit invalid input and inspect behavior | Observation record showing error and unchanged data | Test Architect | UI semantics require human assessment |

### Open Questions

- None.

### Change Control

Semantic changes require a revision and reapproval.

## Contract Approval

- Status: draft
- Approved by: pending
- Validation approved by: pending
- Approved at: pending
- Contract digest: pending
- Validation artifacts: pending

## Delivery Evidence

### Validation Results

| VAL ID | Result | Evidence | Build or run |
| --- | --- | --- | --- |

### Exceptions

| VAL ID | Reason | Owner | Expires |
| --- | --- | --- | --- |
"""


BUILD_SPEC = """---
title: 'Story 1.2: Contract example'
type: 'feature'
created: '2026-07-29'
status: 'ready-for-dev'
route: 'dispatch'
review_loop_iteration: 0
context:
  - '{project-root}/_bmad/custom/story-contract.md'
---

<frozen-after-approval reason="human-owned intent">

""" + DRAFT.split("## Acceptance Contract", 1)[1].split("### Open Questions", 1)[0].join(
    ("## Acceptance Contract", "")
).replace(
    "### Acceptance Criteria",
    "### Boundaries & Constraints\n\n**Always:** keep profile writes atomic.\n\n"
    "**Never:** change avatar storage.\n\n### Acceptance Criteria",
).replace(
    "### Validation Design",
    "### I/O & Edge-Case Matrix\n\n"
    "| Scenario | Input / State | Expected Output / Behavior | Error Handling |\n"
    "| --- | --- | --- | --- |\n"
    "| HAPPY_PATH | valid profile | saved (AC-1) | N/A |\n\n"
    "### Validation Design",
) + """### Open Questions

- None.

### Change Control

Semantic changes require a revision and reapproval.

</frozen-after-approval>

## Code Map

- `src/profile.py` -- save handler

## Tasks & Acceptance

**Execution:**
- [ ] `src/profile.py` -- implement save -- AC-1, AC-2 via VAL-1, VAL-2

""" + "## Contract Approval" + DRAFT.split("## Contract Approval", 1)[1] + """
## Implementation Notes

## Spec Change Log

## Review Triage Log

## Verification

**Commands:**
- `pytest tests/api/profile.py` -- expected: pass
"""


class StoryContractValidatorTests(unittest.TestCase):
    def document(self, content: str = DRAFT):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "story.md"
        path.write_text(content, encoding="utf-8")
        return validator.ContractDocument.load(path)

    def approved(self, content: str = DRAFT) -> str:
        draft = self.document(content)
        digest = validator.contract_digest(draft)
        return (
            content.replace("- Status: draft", "- Status: approved")
            .replace("- Approved by: pending", "- Approved by: Product Owner")
            .replace(
                "- Validation approved by: pending",
                "- Validation approved by: Test Architect",
            )
            .replace("- Approved at: pending", "- Approved at: 2026-07-29T12:00:00Z")
            .replace("- Contract digest: pending", f"- Contract digest: {digest}")
            .replace(
                "- Validation artifacts: pending",
                "- Validation artifacts: tests/atdd/story-1.2.md",
            )
        )

    def test_build_spec_with_frozen_block_and_extra_subsections(self):
        self.assertEqual([], validator.validate(self.document(BUILD_SPEC), "draft"))
        approved = self.approved(BUILD_SPEC)
        self.assertEqual([], validator.validate(self.document(approved), "approved"))

    def test_build_spec_frozen_edit_invalidates_digest(self):
        approved = self.approved(BUILD_SPEC).replace(
            "keep profile writes atomic", "keep profile writes eventually consistent"
        )
        errors = validator.validate(self.document(approved), "approved")
        self.assertIn(
            "Acceptance Contract changed after approval; digest does not match", errors
        )

    def test_build_spec_non_normative_edit_keeps_digest(self):
        approved = self.approved(BUILD_SPEC).replace(
            "## Implementation Notes\n", "## Implementation Notes\n\n- VAL-1 PASS (candidate)\n"
        )
        self.assertEqual([], validator.validate(self.document(approved), "approved"))

    def test_valid_draft(self):
        self.assertEqual([], validator.validate(self.document(), "draft"))

    def test_rejects_unmapped_acceptance_criterion(self):
        content = DRAFT.replace("| VAL-2 | AC-2 |", "| VAL-2 | AC-1 |")
        errors = validator.validate(self.document(content), "draft")
        self.assertIn("AC-2 has no validation obligation", errors)

    def test_rejects_empty_normative_content(self):
        content = DRAFT.replace("Users can save a valid profile.", "TBD")
        errors = validator.validate(self.document(content), "draft")
        self.assertIn(
            "Acceptance Contract subsection is empty or contains only placeholders: Intent",
            errors,
        )

    def test_rejects_missing_draft_approval_field(self):
        content = DRAFT.replace("- Validation artifacts: pending\n", "")
        errors = validator.validate(self.document(content), "draft")
        self.assertIn(
            "Contract Approval field is missing: validation artifacts", errors
        )

    def test_contract_metadata_does_not_use_nested_scope_fields(self):
        content = DRAFT.replace("- Risk: medium", "- Risk: impossible", 1).replace(
            "- Out of scope: avatar upload",
            "- Out of scope: avatar upload\n- Risk: medium",
        )
        errors = validator.validate(self.document(content), "draft")
        self.assertIn("Risk must be low, medium, high, or critical", errors)

    def test_commented_metadata_cannot_satisfy_contract(self):
        content = DRAFT.replace(
            "- Contract ID: STORY-1.2", "<!--\n- Contract ID: STORY-1.2\n-->"
        )
        errors = validator.validate(self.document(content), "draft")
        self.assertIn(
            "Acceptance Contract metadata is missing or pending: contract id", errors
        )

    def test_rejects_manual_validation_without_reason(self):
        content = DRAFT.replace(
            "| Test Architect | UI semantics require human assessment |",
            "| Test Architect | - |",
        )
        errors = validator.validate(self.document(content), "draft")
        self.assertIn("VAL-2 manual validation requires a reason", errors)

    def test_legitimate_placeholder_like_verbs_are_allowed(self):
        content = DRAFT.replace(
            "Given a valid profile, when it is saved, then the persisted profile is observable.",
            "Given pending users, when they add a <button> profile, then unknown fields are described safely.",
        )
        self.assertEqual([], validator.validate(self.document(content), "draft"))

    def test_fenced_markdown_is_not_parsed_as_structure_or_acceptance(self):
        content = DRAFT.replace(
            "Semantic changes require a revision and reapproval.",
            "Semantic changes require a revision and reapproval.\n\n"
            "```markdown\n## Contract Approval\n- AC-99 [P0]: fake example\n```",
        )
        approved = self.approved(content)
        self.assertEqual([], validator.validate(self.document(approved), "approved"))

    def test_rejects_duplicate_acceptance_section(self):
        content = DRAFT.replace(
            "### Validation Design",
            "### Acceptance Criteria\n\n- AC-3 [P2]: Duplicate section.\n\n### Validation Design",
        )
        errors = validator.validate(self.document(content), "draft")
        self.assertIn(
            "duplicate Acceptance Contract subsection: Acceptance Criteria", errors
        )

    def test_rejects_malformed_acceptance_line(self):
        content = DRAFT.replace("- AC-2 [P1]:", "- AC-2:")
        errors = validator.validate(self.document(content), "draft")
        self.assertTrue(
            any(error.startswith("malformed acceptance criterion:") for error in errors)
        )

    def test_rejects_malformed_validation_row(self):
        content = DRAFT.replace(
            "| VAL-1 | AC-1 | mechanical | API |", "| VAL-1 | AC-1 | API |"
        )
        errors = validator.validate(self.document(content), "draft")
        self.assertIn("Validation Design row 1 is malformed", errors)

    def test_rejects_malformed_covers_value(self):
        content = DRAFT.replace(
            "| VAL-1 | AC-1 | mechanical |", "| VAL-1 | AC-1, AC-X | mechanical |"
        )
        errors = validator.validate(self.document(content), "draft")
        self.assertIn("VAL-1 has malformed Covers value: AC-1, AC-X", errors)

    def test_rejects_unsupported_validation_level(self):
        content = DRAFT.replace(
            "| VAL-1 | AC-1 | mechanical | API |",
            "| VAL-1 | AC-1 | mechanical | magic |",
        )
        errors = validator.validate(self.document(content), "draft")
        self.assertIn("VAL-1 has unsupported validation level: magic", errors)

    def test_rejects_wrong_evidence_heading_level(self):
        content = DRAFT.replace("### Validation Results", "#### Validation Results")
        errors = validator.validate(self.document(content), "draft")
        self.assertIn(
            "Delivery Evidence subsection must be a level-3 heading: Validation Results",
            errors,
        )

    def test_allows_escaped_pipe_in_validation_command(self):
        content = DRAFT.replace(
            "tests/api/profile.py::test_save", r"printf result \| grep result"
        )
        self.assertEqual([], validator.validate(self.document(content), "draft"))

    def test_even_backslashes_do_not_escape_table_delimiter(self):
        self.assertEqual(
            ["left \\", "right"], validator.split_table_row(r"| left \\| right |")
        )

    def test_rejects_malformed_source_reference(self):
        content = DRAFT.replace("[Source: docs/prd.md#FR-1]", "[Source: docs/prd.md]")
        errors = validator.validate(self.document(content), "draft")
        self.assertIn(
            "Sources must contain at least one complete '[Source: path#section]' reference",
            errors,
        )

    def test_rejects_placeholder_source_components(self):
        for source in ("[Source: TBD#TODO]", "[Source: TBD.md#TODO-1]"):
            with self.subTest(source=source):
                content = DRAFT.replace("[Source: docs/prd.md#FR-1]", source)
                errors = validator.validate(self.document(content), "draft")
                self.assertIn("Sources contain a placeholder path or section", errors)

    def test_valid_approved_contract(self):
        self.assertEqual(
            [], validator.validate(self.document(self.approved()), "approved")
        )

    def test_approved_contract_requires_atdd_artifact(self):
        content = self.approved().replace(
            "- Validation artifacts: tests/atdd/story-1.2.md",
            "- Validation artifacts: None",
        )
        errors = validator.validate(self.document(content), "approved")
        self.assertIn(
            "Validation artifacts must link the pre-implementation validation output",
            errors,
        )

    def test_approved_contract_rejects_dash_identity(self):
        content = self.approved().replace(
            "- Approved by: Product Owner", "- Approved by: -"
        )
        errors = validator.validate(self.document(content), "approved")
        self.assertIn("Contract Approval field is pending: approved by", errors)

    def test_rejects_duplicate_contract_and_approval_bullet_fields(self):
        for original, duplicate in [
            ("- Contract ID: STORY-1.2", "- Contract ID: STORY-9.9\n- Contract ID: STORY-1.2"),
            ("- Status: approved", "- Status: superseded\n- Status: approved"),
            ("- Approved by: Product Owner", "- Approved by: pending\n- Approved by: Product Owner"),
        ]:
            with self.subTest(field=original):
                content = self.approved().replace(original, duplicate)
                errors = validator.validate(self.document(content), "approved")
                self.assertTrue(any(error.startswith("duplicate ") for error in errors))

    def test_rejects_normative_drift_after_approval(self):
        content = self.approved().replace(
            "Users can save a valid profile.", "Users can replace a valid profile."
        )
        errors = validator.validate(self.document(content), "approved")
        self.assertIn(
            "Acceptance Contract changed after approval; digest does not match", errors
        )

    def test_rejects_impossible_approval_timestamp(self):
        content = self.approved().replace(
            "2026-07-29T12:00:00Z", "2026-99-99T99:99:99Z"
        )
        errors = validator.validate(self.document(content), "approved")
        self.assertIn(
            "Approved at must be a valid UTC timestamp YYYY-MM-DDTHH:MM:SSZ", errors
        )

    def test_delivery_requires_each_validation_result(self):
        content = self.approved().replace(
            "| --- | --- | --- | --- |\n\n### Exceptions",
            "| --- | --- | --- | --- |\n| VAL-1 | PASS | tests/api/profile.py output | commit:abc123 |\n\n### Exceptions",
        )
        errors = validator.validate(self.document(content), "delivered")
        self.assertIn("VAL-2 has no delivery evidence", errors)

    def test_valid_delivered_contract(self):
        content = self.approved().replace(
            "| --- | --- | --- | --- |\n\n### Exceptions",
            "| --- | --- | --- | --- |\n"
            "| VAL-1 | PASS | tests/api/profile.py output | commit:abc123 |\n"
            "| VAL-2 | PASS | review/profile-observation.md | ci:456 |\n\n### Exceptions",
        )
        self.assertEqual([], validator.validate(self.document(content), "delivered"))

    def test_waiver_requires_exception(self):
        content = self.approved().replace(
            "| --- | --- | --- | --- |\n\n### Exceptions",
            "| --- | --- | --- | --- |\n"
            "| VAL-1 | PASS | tests/api/profile.py output | commit:abc123 |\n"
            "| VAL-2 | WAIVED | waiver record | ci:456 |\n\n### Exceptions",
        )
        errors = validator.validate(self.document(content), "delivered")
        self.assertIn("VAL-2 is WAIVED without a complete exception", errors)

    def test_rejects_expired_waiver(self):
        content = (
            self.approved()
            .replace(
                "| --- | --- | --- | --- |\n\n### Exceptions",
                "| --- | --- | --- | --- |\n"
                "| VAL-1 | PASS | tests/api/profile.py output | commit:abc123 |\n"
                "| VAL-2 | WAIVED | waiver record | ci:456 |\n\n### Exceptions",
            )
            .replace(
                "### Exceptions\n\n| VAL ID | Reason | Owner | Expires |\n| --- | --- | --- | --- |\n",
                "### Exceptions\n\n| VAL ID | Reason | Owner | Expires |\n| --- | --- | --- | --- |\n"
                "| VAL-2 | Accepted for release | QA Lead | 2000-01-01 |\n",
            )
        )
        errors = validator.validate(self.document(content), "delivered")
        self.assertIn("VAL-2 exception expired on 2000-01-01", errors)

    def test_accepts_time_bounded_waiver(self):
        content = (
            self.approved()
            .replace(
                "| --- | --- | --- | --- |\n\n### Exceptions",
                "| --- | --- | --- | --- |\n"
                "| VAL-1 | PASS | tests/api/profile.py output | commit:abc123 |\n"
                "| VAL-2 | WAIVED | waiver record | ci:456 |\n\n### Exceptions",
            )
            .replace(
                "### Exceptions\n\n| VAL ID | Reason | Owner | Expires |\n| --- | --- | --- | --- |\n",
                "### Exceptions\n\n| VAL ID | Reason | Owner | Expires |\n| --- | --- | --- | --- |\n"
                "| VAL-2 | Accepted for release | QA Lead | 2999-01-01 |\n",
            )
        )
        self.assertEqual([], validator.validate(self.document(content), "delivered"))


if __name__ == "__main__":
    unittest.main()


RUST_ACTIVE = (
    "#[test]\n"
    "fn val_2_generated_message_roundtrip() {\n"
    "    assert_eq!(roundtrip(1), 1);\n"
    "}\n"
)


class RustIgnoreTests(unittest.TestCase):
    """Rust `#[ignore]` is a skip marker: removing it keeps the lock, keeping it is a skip."""

    def ignored(self, marker: str) -> str:
        return RUST_ACTIVE.replace("#[test]\n", f"#[test]\n{marker}\n")

    def test_removing_ignore_keeps_the_lock(self) -> None:
        for marker in ("#[ignore]", '#[ignore = "red phase: VAL-2"]', "    #[ignore]"):
            with self.subTest(marker=marker):
                self.assertEqual(
                    validator.lock_digest(RUST_ACTIVE),
                    validator.lock_digest(self.ignored(marker)),
                )

    def test_weakening_a_rust_test_changes_the_lock(self) -> None:
        weakened = RUST_ACTIVE.replace("roundtrip(1), 1", "1, 1")
        self.assertNotEqual(
            validator.lock_digest(RUST_ACTIVE), validator.lock_digest(weakened)
        )

    def test_ignored_rust_test_is_detected_as_skipped(self) -> None:
        for marker in ("#[ignore]", '#[ignore = "red phase"]'):
            with self.subTest(marker=marker):
                lines = self.ignored(marker).splitlines()
                index = next(i for i, line in enumerate(lines) if "val_2_" in line)
                self.assertTrue(validator.is_skipped(lines, index))

    def test_active_rust_test_is_not_skipped(self) -> None:
        lines = RUST_ACTIVE.splitlines()
        self.assertFalse(validator.is_skipped(lines, 1))
        ignored_name = RUST_ACTIVE.replace("fn val_2_", "fn ignore_val_2_").splitlines()
        self.assertFalse(validator.is_skipped(ignored_name, 1))
