"""Guardrail health scan: friction signals from real spec fixtures (read-only)."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
SCAN = SCRIPTS / "steward_scan.py"


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


anchor = load(
    "steward_anchor_helpers", Path(__file__).with_name("test_jj_approval_anchor.py")
)
SPEC_PATH, TEST_PATH = anchor.SPEC_PATH, anchor.TEST_PATH
TODAY = date(2026, 8, 30)  # fixture approval is 2026-07-29: 32 days earlier
READINESS = "# Agent readiness\n\nStatus: ready\n\n## Contract CI Wiring\n"


class StewardScanTests(unittest.TestCase):
    def setUp(self) -> None:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        (self.root / "_bmad").mkdir()
        self.write("docs/agent-readiness.md", READINESS)
        self.write(TEST_PATH, anchor.SCAFFOLD)
        self.approved = anchor.approve(anchor.fixtures.BUILD_SPEC)

    def write(self, relative: str, text: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return path

    def scan(self, *extra: str) -> dict:
        result = subprocess.run(
            [sys.executable, str(SCAN), "--json", "--today", TODAY.isoformat(), *extra],
            cwd=self.root,
            capture_output=True,
            text=True,
            check=True,
        )
        return json.loads(result.stdout)

    def ids(self, report: dict) -> set[str]:
        return {item["id"] for item in report["signals"]}

    def test_healthy_delivered_story_is_quiet(self) -> None:
        self.write(SPEC_PATH, anchor.deliver(self.approved))
        report = self.scan()
        self.assertEqual([], report["signals"])

    def test_missing_readiness_record_is_a_concern(self) -> None:
        (self.root / "docs/agent-readiness.md").unlink()
        self.assertIn("readiness-missing", self.ids(self.scan()))

    def test_unready_and_unwired_readiness_are_notes(self) -> None:
        self.write("docs/agent-readiness.md", "Status: building\n")
        self.assertTrue(
            {"readiness-not-ready", "ci-wiring-missing"} <= self.ids(self.scan())
        )

    def test_revision_churn_and_review_loops(self) -> None:
        text = self.approved.replace("- Revision: 1", "- Revision: 3").replace(
            "review_loop_iteration: 0", "review_loop_iteration: 4"
        )
        self.write(SPEC_PATH, anchor.deliver(text))
        self.assertTrue({"revision-churn", "review-loops"} <= self.ids(self.scan()))

    def test_command_only_mechanical_check_is_flagged(self) -> None:
        text = self.approved.replace(
            "tests/api/profile.py::test_save", "`pytest tests/api`"
        )
        self.write(SPEC_PATH, anchor.deliver(text))
        report = self.scan()
        item = next(i for i in report["signals"] if i["id"] == "ci-unverifiable")
        self.assertIn("VAL-1", item["message"])

    def test_waivers_heavy_expired_and_expiring(self) -> None:
        start = self.approved.index("### Validation Results")
        end = self.approved.index("## Implementation Notes")
        evidence = (
            "### Validation Results\n\n| VAL ID | Result | Evidence | Build or run |\n"
            "| --- | --- | --- | --- |\n"
            "| VAL-1 | WAIVED | waiver | ci:1 |\n| VAL-2 | WAIVED | waiver | ci:2 |\n\n"
            "### Exceptions\n\n| VAL ID | Reason | Owner | Expires |\n"
            "| --- | --- | --- | --- |\n"
            "| VAL-1 | infra down | QA | 2026-08-01 |\n"
            "| VAL-2 | flaky env | QA | 2026-09-05 |\n\n"
        )
        self.write(SPEC_PATH, self.approved[:start] + evidence + self.approved[end:])
        ids = self.ids(self.scan())
        self.assertTrue({"waiver-heavy", "waiver-expired", "waiver-expiring"} <= ids)

    def test_stalled_and_failing_gate_on_approved_story(self) -> None:
        self.write(SPEC_PATH, self.approved)
        self.write(TEST_PATH, anchor.WEAKENED)  # locked test changed after approval
        report = self.scan()
        ids = self.ids(report)
        self.assertTrue({"stalled", "gate-failing"} <= ids, report)
        gate = next(i for i in report["signals"] if i["id"] == "gate-failing")
        self.assertIn("locked test changed", gate["message"])

    def test_recurring_friction_points_at_the_mechanism(self) -> None:
        churned = anchor.deliver(
            self.approved.replace("- Revision: 1", "- Revision: 4")
        )
        self.write(SPEC_PATH, churned)
        self.write(SPEC_PATH.replace("1-2", "1-3"), churned)
        self.assertIn("recurring:revision-churn", self.ids(self.scan()))

    def test_story_option_limits_story_signals(self) -> None:
        churned = anchor.deliver(
            self.approved.replace("- Revision: 1", "- Revision: 4")
        )
        self.write(SPEC_PATH, churned)
        other = self.write(SPEC_PATH.replace("1-2", "1-3"), churned)
        report = self.scan("--story", str(other))
        stories = {item["story"] for item in report["signals"]}
        self.assertEqual({other.relative_to(self.root).as_posix()}, stories)

    def test_scan_never_writes(self) -> None:
        self.write(SPEC_PATH, self.approved)
        before = {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.scan()
        after = {p: p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)

    def test_text_output_lists_concerns(self) -> None:
        (self.root / "docs/agent-readiness.md").unlink()
        result = subprocess.run(
            [sys.executable, str(SCAN)],
            cwd=self.root,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, result.returncode)
        self.assertIn("CONCERN [readiness-missing]", result.stdout)


if __name__ == "__main__":
    unittest.main()
