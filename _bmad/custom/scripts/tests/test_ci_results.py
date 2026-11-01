"""CI-written results (#2): delivered validation trusts JUnit XML, not the spec's PASS.

Runs real pytest to produce the JUnit report; skips when pytest is unavailable.
"""

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
VALIDATOR = SCRIPTS / "validate_story_contract.py"


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


anchor = load(
    "ci_anchor_helpers", Path(__file__).with_name("test_jj_approval_anchor.py")
)
validator = anchor.validator
SPEC_PATH = anchor.SPEC_PATH
TEST_PATH = "tests/api/test_profile.py"
TEST_NAME = "test_val_1_save"
PASSING = f"def {TEST_NAME}():\n    assert 1 + 1 == 2\n"
FAILING = f"def {TEST_NAME}():\n    assert 1 + 1 == 3\n"
SKIPPED = f"import pytest\n\n\n@pytest.mark.skip(reason='red')\n{PASSING}"


def pytest_available() -> bool:
    return importlib.util.find_spec("pytest") is not None


def spec_text(planned: str, test_text: str) -> str:
    draft = anchor.fixtures.BUILD_SPEC.replace(
        "tests/api/profile.py::test_save", planned
    )
    lock = (
        "### Locked Tests\n\n| Path | Lock digest |\n| --- | --- |\n"
        f"| {TEST_PATH} | {validator.lock_digest(test_text)} |\n\n"
    )
    return anchor.deliver(anchor.approve(draft, lock=lock))


class CiResultsTests(unittest.TestCase):
    def setUp(self) -> None:
        project = tempfile.TemporaryDirectory()
        outside = tempfile.TemporaryDirectory()
        self.addCleanup(project.cleanup)
        self.addCleanup(outside.cleanup)
        self.root = Path(project.name)
        self.outside = Path(outside.name)
        (self.root / "_bmad").mkdir()
        self.spec = self.root / SPEC_PATH
        self.write("review/profile-observation.md", "Observed error; data unchanged.\n")

    def write(self, relative: str, text: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    def story(self, test_text: str, planned: str = f"{TEST_PATH}::{TEST_NAME}") -> None:
        self.write(TEST_PATH, test_text)
        self.write(SPEC_PATH, spec_text(planned, test_text))

    def run_pytest(self) -> Path:
        report = self.outside / "junit.xml"
        # Reporter metadata is attached at collection so it also survives skipped tests.
        self.write(
            "conftest.py",
            (
                "from pathlib import Path\n\n"
                "def pytest_collection_modifyitems(items):\n"
                "    for item in items:\n"
                "        item.user_properties.append(('contract', 'STORY-1.2'))\n"
                "        path = item.path.resolve().relative_to(Path.cwd().resolve()).as_posix()\n"
                "        item.user_properties.append(('test-file', path))\n"
            ),
        )
        subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
             f"--junitxml={report}", TEST_PATH],
            cwd=self.root, capture_output=True, check=False,
        )  # fmt: skip
        self.assertTrue(report.is_file())
        return report

    def validate(self, *junit: Path) -> dict:
        command = [sys.executable, str(VALIDATOR), "validate", "--phase", "delivered"]
        for path in junit:
            command += ["--junit", str(path)]
        result = subprocess.run(
            [*command, "--json", str(self.spec)],
            capture_output=True,
            text=True,
            check=False,
        )
        return json.loads(result.stdout)

    def assert_error(self, payload: dict, fragment: str) -> None:
        self.assertFalse(payload["valid"])
        self.assertTrue(
            any(fragment in error for error in payload["errors"]), payload["errors"]
        )

    def junit(self, body: str, *, bind: bool = True) -> Path:
        if bind:
            planned = validator.planned_tests(
                validator.ContractDocument.load(self.spec)
            )
            path = planned[0][1] if planned else TEST_PATH
            properties = (
                '<property name="contract" value="STORY-1.2"/>'
                f'<property name="test-file" value="{path}"/>'
            )
            body = re.sub(r"<testcase([^<>]*?)/>", r"<testcase\1></testcase>", body)

            def attach(match: re.Match[str]) -> str:
                content = match[2]
                if "</properties>" in content:
                    content = content.replace(
                        "</properties>", properties + "</properties>", 1
                    )
                else:
                    content += "<properties>" + properties + "</properties>"
                return "<testcase" + match[1] + ">" + content + "</testcase>"

            body = re.sub(
                r"<testcase([^<>]*)>(.*?)</testcase>", attach, body, flags=re.DOTALL
            )
        report = self.outside / "handmade.xml"
        report.write_text(f'<?xml version="1.0"?>\n<testsuites>{body}</testsuites>\n')
        return report

    @unittest.skipUnless(pytest_available(), "pytest is not installed")
    def test_passing_ci_run_is_the_evidence(self) -> None:
        self.story(PASSING)  # note: no val-1-output.txt evidence file is written
        payload = self.validate(self.run_pytest())
        self.assertEqual([], payload["errors"])
        self.assertEqual({"VAL-1": "passed"}, payload["ci_results"])

    @unittest.skipUnless(pytest_available(), "pytest is not installed")
    def test_spec_pass_is_ignored_when_ci_fails(self) -> None:
        self.story(FAILING)
        payload = self.validate(self.run_pytest())
        self.assert_error(payload, "VAL-1 failed in CI")
        self.assertEqual({"VAL-1": "failed"}, payload["ci_results"])

    @unittest.skipUnless(pytest_available(), "pytest is not installed")
    def test_skipped_in_ci_fails(self) -> None:
        self.story(SKIPPED)
        self.assert_error(self.validate(self.run_pytest()), "VAL-1 was skipped in CI")

    def test_results_inside_the_project_are_refused(self) -> None:
        self.story(PASSING)
        inside = self.write(
            "reports/junit.xml",
            f'<testsuite><testcase name="{TEST_NAME}"/></testsuite>',
        )
        self.assert_error(self.validate(inside), "inside the project tree")

    def test_test_absent_from_results_fails(self) -> None:
        self.story(PASSING)
        report = self.junit(
            '<testsuite><testcase name="test_val_2_other"/></testsuite>'
        )
        self.assert_error(self.validate(report), "VAL-1 has no CI result")

    def test_similar_name_does_not_count(self) -> None:
        self.story(PASSING)
        report = self.junit(
            f'<testsuite><testcase name="{TEST_NAME}_all"/></testsuite>'
        )
        self.assert_error(self.validate(report), "VAL-1 has no CI result")

    def test_untagged_result_is_not_attributed(self) -> None:
        self.story(PASSING.replace(TEST_NAME, "test_save"), f"{TEST_PATH}::test_save")
        report = self.junit('<testsuite><testcase name="test_save"/></testsuite>')
        self.assert_error(self.validate(report), "nothing ties the result to VAL-1")

    def test_val_property_tags_an_untagged_name(self) -> None:
        self.story(PASSING.replace(TEST_NAME, "test_save"), f"{TEST_PATH}::test_save")
        report = self.junit(
            '<testsuite><testcase name="test_save"><properties>'
            '<property name="val" value="VAL-3, VAL-1"/></properties>'
            "</testcase></testsuite>"
        )
        payload = self.validate(report)
        self.assertEqual({"VAL-1": "passed"}, payload["ci_results"], payload["errors"])

    def test_wrong_property_or_suite_property_does_not_tag(self) -> None:
        self.story(PASSING.replace(TEST_NAME, "test_save"), f"{TEST_PATH}::test_save")
        case = '<testcase name="test_save"><properties>{}</properties></testcase>'
        for body in (
            case.format('<property name="val" value="VAL-12"/>'),
            case.format('<property name="owner" value="VAL-1"/>'),
            "<properties>" + '<property name="val" value="VAL-1"/>' + "</properties>"
            '<testcase name="test_save"/>',
        ):
            with self.subTest(body=body):
                report = self.junit(f"<testsuite>{body}</testsuite>")
                self.assert_error(self.validate(report), "nothing ties the result")

    def test_playwright_tag_appended_to_name(self) -> None:
        planned = "tests/e2e/profile.spec.ts::Profile › saves profile"
        self.story(PASSING, planned)
        report = self.junit(
            '<testsuite file="profile.spec.ts">'
            '<testcase name="Profile › saves profile @VAL-1"/></testsuite>'
        )
        payload = self.validate(report)
        self.assertEqual({"VAL-1": "passed"}, payload["ci_results"], payload["errors"])

    def test_command_planned_check_cannot_be_ci_verified(self) -> None:
        self.story(PASSING, "`pytest tests/api`")
        report = self.junit(f'<testsuite><testcase name="{TEST_NAME}"/></testsuite>')
        self.assert_error(self.validate(report), "is not a `path::test`")

    def test_playwright_style_report_with_relative_file(self) -> None:
        planned = "tests/e2e/profile.spec.ts::Profile › VAL-1 saves profile"
        self.story(PASSING, planned)
        good = self.junit(
            '<testsuite name="profile.spec.ts" file="profile.spec.ts">'
            '<testcase name="Profile › VAL-1 saves profile"/></testsuite>'
        )
        payload = self.validate(good)
        self.assertEqual({"VAL-1": "passed"}, payload["ci_results"], payload["errors"])
        wrong = self.junit(
            '<testsuite file="billing.spec.ts">'
            '<testcase name="VAL-1 saves profile"/></testsuite>'
        )
        self.assert_error(self.validate(wrong), "VAL-1 has no CI result")

    def test_doctype_is_refused(self) -> None:
        self.story(PASSING)
        report = self.outside / "evil.xml"
        report.write_text(
            '<?xml version="1.0"?><!DOCTYPE x [<!ENTITY a "aaaa">]>'
            f'<testsuite><testcase name="{TEST_NAME}"/></testsuite>'
        )
        self.assert_error(self.validate(report), "must not contain a DOCTYPE")

    def test_without_junit_the_evidence_file_is_still_required(self) -> None:
        self.story(PASSING)
        self.assert_error(self.validate(), "references a missing file")

    @unittest.skipUnless(pytest_available(), "pytest is not installed")
    def test_pytest_record_property_tags_the_test(self) -> None:
        test_text = (
            "def test_save(record_property):\n"
            '    record_property("val", "VAL-1")\n'
            "    assert 1 + 1 == 2\n"
        )
        self.story(test_text, f"{TEST_PATH}::test_save")
        payload = self.validate(self.run_pytest())
        self.assertEqual({"VAL-1": "passed"}, payload["ci_results"], payload["errors"])

    def run_ci(self, *junit: Path) -> tuple[int, dict]:
        command = [sys.executable, str(VALIDATOR), "ci", "--json"]
        command += [f"--junit={path}" for path in junit]
        result = subprocess.run(
            command, cwd=self.root, capture_output=True, text=True, check=False
        )
        return result.returncode, json.loads(result.stdout)

    @unittest.skipUnless(pytest_available(), "pytest is not installed")
    def test_ci_command_validates_every_contract(self) -> None:
        self.story(PASSING)
        draft = self.root / "_bmad-output/implementation-artifacts/spec-9-9-draft.md"
        draft.write_text(anchor.fixtures.BUILD_SPEC)
        self.write(
            "_bmad/custom/story-contract.md", "```\n## Acceptance Contract\n```\n"
        )
        code, payload = self.run_ci(self.run_pytest())
        self.assertEqual(0, code, payload)
        phases = {item["story"]: item["phase"] for item in payload["contracts"]}
        self.assertEqual("delivered", phases[SPEC_PATH])
        self.assertEqual("skipped", phases[str(draft.relative_to(self.root))])
        self.assertEqual(2, len(phases))  # _bmad/ templates are never treated as specs

    @unittest.skipUnless(pytest_available(), "pytest is not installed")
    def test_ci_command_fails_on_failing_test(self) -> None:
        self.story(FAILING)
        code, payload = self.run_ci(self.run_pytest())
        self.assertEqual(1, code)
        self.assertIn("VAL-1 failed in CI ('test_val_1_save')", str(payload))

    def test_ci_command_requires_junit_for_delivered_contracts(self) -> None:
        self.story(PASSING)
        self.write("_bmad-output/test-artifacts/val-1-output.txt", "typed PASS\n")
        code, payload = self.run_ci()
        self.assertEqual(1, code)
        self.assertIn("needs CI-written results", str(payload))

    def test_ci_command_checks_approved_but_unreviewed_contracts(self) -> None:
        self.write(TEST_PATH, PASSING)
        lock = (
            "### Locked Tests\n\n| Path | Lock digest |\n| --- | --- |\n"
            f"| {TEST_PATH} | {validator.lock_digest(PASSING)} |\n\n"
        )
        draft = anchor.fixtures.BUILD_SPEC.replace(
            "tests/api/profile.py::test_save", f"{TEST_PATH}::{TEST_NAME}"
        )
        self.write(SPEC_PATH, anchor.approve(draft, lock=lock))
        code, payload = self.run_ci()
        self.assertEqual(0, code, payload)
        self.assertEqual("approved", payload["contracts"][0]["phase"])
        self.write(TEST_PATH, FAILING)  # a weakened/changed locked test
        code, payload = self.run_ci()
        self.assertEqual(1, code)
        self.assertIn("locked test changed since approval", str(payload))

    def test_report_without_contract_identity_is_not_borrowed(self) -> None:
        self.story(PASSING)
        report = self.junit(
            f'<testsuite><testcase file="{TEST_PATH}" name="{TEST_NAME}"/></testsuite>',
            bind=False,
        )
        payload = self.validate(report)
        self.assert_error(payload, "missing/mismatching contract or full test identity")
        self.assertEqual({"VAL-1": "missing"}, payload["ci_results"])

    def test_contract_identity_is_exact_and_testcase_scoped(self) -> None:
        self.story(PASSING)
        for contract in ("STORY-9.9", "STORY-1.20", ""):
            with self.subTest(contract=contract):
                report = self.junit(
                    f'<testsuite><testcase file="{TEST_PATH}" name="{TEST_NAME}">'
                    f'<properties><property name="contract" value="{contract}"/>'
                    "</properties></testcase></testsuite>",
                    bind=False,
                )
                self.assert_error(self.validate(report), "bound to contract STORY-1.2")
        report = self.junit(
            '<testsuite><properties><property name="contract" value="STORY-1.2"/>'
            f'</properties><testcase file="{TEST_PATH}" name="{TEST_NAME}"/></testsuite>',
            bind=False,
        )
        self.assert_error(self.validate(report), "bound to contract STORY-1.2")

    def test_full_reporter_path_supplies_test_identity(self) -> None:
        self.story(PASSING)
        report = self.junit(
            f'<testsuite><testcase file="/ci/build/project/{TEST_PATH}" name="{TEST_NAME}">'
            '<properties><property name="contract" value="STORY-1.2"/></properties>'
            "</testcase></testsuite>",
            bind=False,
        )
        self.assertEqual([], self.validate(report)["errors"])

    def test_basename_or_other_directory_does_not_supply_identity(self) -> None:
        self.story(PASSING)
        for path in (
            "test_profile.py",
            "tests/billing/test_profile.py",
            "../" + TEST_PATH,
        ):
            with self.subTest(path=path):
                report = self.junit(
                    f'<testsuite><testcase file="{path}" name="{TEST_NAME}">'
                    '<properties><property name="contract" value="STORY-1.2"/></properties>'
                    "</testcase></testsuite>",
                    bind=False,
                )
                self.assert_error(self.validate(report), "full test identity")

    def test_partial_title_cannot_match_another_test(self) -> None:
        self.story(PASSING)
        report = self.junit(
            f'<testsuite><testcase name="unrelated {TEST_NAME}"/></testsuite>'
        )
        self.assert_error(self.validate(report), "full test identity")

    def test_explicitly_shared_parameterised_test_is_supported(self) -> None:
        self.story(PASSING)
        report = self.junit(
            f'<testsuite><testcase file="{TEST_PATH}" name="{TEST_NAME}[valid]">'
            '<properties><property name="contract" value="STORY-9.9, STORY-1.2"/></properties>'
            "</testcase></testsuite>",
            bind=False,
        )
        self.assertEqual([], self.validate(report)["errors"])

    def test_explicit_test_id_supports_reporters_without_file_attributes(self) -> None:
        self.story(PASSING)
        report = self.junit(
            '<testsuite><testcase name="generated case @VAL-1"><properties>'
            '<property name="contract" value="STORY-1.2"/>'
            f'<property name="test-id" value="{TEST_PATH}::{TEST_NAME}"/>'
            "</properties></testcase></testsuite>",
            bind=False,
        )
        self.assertEqual([], self.validate(report)["errors"])

    def test_conflicting_explicit_identity_is_refused(self) -> None:
        self.story(PASSING)
        for properties in (
            '<property name="test-id" value="tests/billing/test_profile.py::test_val_1_save"/>',
            (
                f'<property name="test-id" value="{TEST_PATH}::{TEST_NAME}"/>'
                '<property name="test-id" value="tests/billing/test_profile.py::test_val_1_save"/>'
            ),
            '<property name="test-file" value="tests/billing/test_profile.py"/>',
        ):
            with self.subTest(properties=properties):
                report = self.junit(
                    f'<testsuite><testcase file="{TEST_PATH}" name="{TEST_NAME}"><properties>'
                    '<property name="contract" value="STORY-1.2"/>'
                    + properties
                    + "</properties></testcase></testsuite>",
                    bind=False,
                )
                self.assert_error(self.validate(report), "full test identity")

    def test_class_qualified_plan_does_not_match_a_different_class(self) -> None:
        self.story(PASSING, f"{TEST_PATH}::TestProfile::{TEST_NAME}")
        for classname, expected in (
            ("module.TestOther", "missing"),
            ("module.TestProfile", "passed"),
        ):
            with self.subTest(classname=classname):
                report = self.junit(
                    f'<testsuite><testcase file="{TEST_PATH}" classname="{classname}" name="{TEST_NAME}">'
                    '<properties><property name="contract" value="STORY-1.2"/></properties>'
                    "</testcase></testsuite>",
                    bind=False,
                )
                self.assertEqual(
                    {"VAL-1": expected}, self.validate(report)["ci_results"]
                )

    def test_ci_cannot_reuse_one_storys_result_for_another(self) -> None:
        self.story(PASSING)
        draft = anchor.fixtures.BUILD_SPEC.replace(
            "tests/api/profile.py::test_save", f"{TEST_PATH}::{TEST_NAME}"
        ).replace("- Contract ID: STORY-1.2", "- Contract ID: STORY-2.1")
        lock = (
            "### Locked Tests\n\n| Path | Lock digest |\n| --- | --- |\n"
            f"| {TEST_PATH} | {validator.lock_digest(PASSING)} |\n\n"
        )
        second = SPEC_PATH.replace("spec-1-2-profile", "spec-2-1-profile")
        self.write(second, anchor.deliver(anchor.approve(draft, lock=lock)))
        report = self.junit(f'<testsuite><testcase name="{TEST_NAME}"/></testsuite>')
        code, payload = self.run_ci(report)
        self.assertEqual(1, code)
        reports = {item["story"]: item for item in payload["contracts"]}
        self.assertTrue(reports[SPEC_PATH]["valid"], reports[SPEC_PATH])
        self.assertEqual({"VAL-1": "missing"}, reports[second]["ci_results"])

    def remove_review_record(self) -> None:
        text = self.spec.read_text()
        document = validator.ContractDocument.from_text(self.spec, text)
        section = document.section("Review Record", parent="Delivery Evidence")
        assert section is not None
        self.spec.write_text(
            "\n".join(document.lines[: section.start] + document.lines[section.end :])
            + "\n"
        )

    def test_done_without_review_record_still_requires_delivery(self) -> None:
        self.story(PASSING)
        self.spec.write_text(
            self.spec.read_text().replace("status: 'ready-for-dev'", "status: 'done'")
        )
        self.remove_review_record()
        code, payload = self.run_ci()
        self.assertEqual(1, code)
        report = payload["contracts"][0]
        self.assertEqual("delivered", report["phase"])
        self.assertIn("needs a '### Review Record'", str(report["errors"]))
        self.assertIn("needs CI-written results", str(report["errors"]))

    def test_done_without_any_delivery_evidence_still_fails_closed(self) -> None:
        self.write(TEST_PATH, PASSING)
        draft = anchor.fixtures.BUILD_SPEC.replace(
            "tests/api/profile.py::test_save", f"{TEST_PATH}::{TEST_NAME}"
        ).replace("status: 'ready-for-dev'", "status: 'done'")
        lock = (
            "### Locked Tests\n\n| Path | Lock digest |\n| --- | --- |\n"
            f"| {TEST_PATH} | {validator.lock_digest(PASSING)} |\n\n"
        )
        self.write(SPEC_PATH, anchor.approve(draft, lock=lock))
        code, payload = self.run_ci()
        self.assertEqual(1, code)
        self.assertEqual("delivered", payload["contracts"][0]["phase"])

    def test_changing_the_reviewer_to_pending_does_not_downgrade(self) -> None:
        self.story(PASSING)
        self.spec.write_text(
            self.spec.read_text().replace(
                "- Reviewed by: Daniel (human reviewer)", "- Reviewed by: pending"
            )
        )
        code, payload = self.run_ci()
        self.assertEqual(1, code)
        self.assertEqual("delivered", payload["contracts"][0]["phase"])

    def test_results_without_a_review_record_still_require_delivery(self) -> None:
        self.story(PASSING)
        self.remove_review_record()  # status is still ready-for-dev, results remain
        code, payload = self.run_ci()
        self.assertEqual(1, code)
        self.assertEqual("delivered", payload["contracts"][0]["phase"])

    def test_completed_claim_cannot_hide_behind_draft_approval(self) -> None:
        for status in ("done", "review", "in-review"):
            with self.subTest(status=status):
                text = anchor.fixtures.BUILD_SPEC.replace(
                    "status: 'ready-for-dev'", f"status: '{status}'"
                )
                self.write(SPEC_PATH, text)
                code, payload = self.run_ci()
                self.assertEqual(1, code)
                self.assertEqual("delivered", payload["contracts"][0]["phase"])
                self.assertIn(
                    "Contract Approval status must be 'approved'", str(payload)
                )


class TagMatchingTests(unittest.TestCase):
    def test_val_tag_forms(self) -> None:
        tag = validator.val_tag_re("VAL-1")
        for text in ("VAL-1 saves", "test_val_1_save", "val1", "VAL_01 x"):
            self.assertTrue(tag.search(text), text)
        for text in ("VAL-12", "interval1", "test_val_10"):
            self.assertFalse(tag.search(text), text)


if __name__ == "__main__":
    unittest.main()
