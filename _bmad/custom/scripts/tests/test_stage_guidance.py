"""Implementation pilot: exact canonical extraction with exception/full-manual fallback."""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import tomllib

from _bmad.custom.scripts.render_stage_guidance import (
    OUTPUT,
    REQUIRED,
    SECTION,
    render_implementation,
)
from _bmad.custom.scripts.validate_story_contract import ContractDocument

ROOT = Path(__file__).resolve().parents[4]
CUSTOM = ROOT / "_bmad/custom"
SCRIPT = CUSTOM / "scripts/render_stage_guidance.py"
MANUAL = CUSTOM / "story-contract.md"


class StageGuidanceTests(unittest.TestCase):
    def test_generated_file_is_current_and_much_shorter(self) -> None:
        expected = render_implementation(MANUAL)
        self.assertEqual(expected, (CUSTOM / OUTPUT).read_text())
        self.assertLess(len(expected.split()), 1000)
        self.assertLess(len(expected.split()), len(MANUAL.read_text().split()) / 3)

    def test_all_developer_rules_are_extracted_not_summarised(self) -> None:
        document = ContractDocument.load(MANUAL)
        section = document.section(SECTION)
        self.assertIsNotNone(section)
        assert section is not None
        original = "\n".join(document.lines[section.start : section.end]).rstrip()
        extracted = original.replace("](#", "](../story-contract.md#")
        self.assertTrue(render_implementation(MANUAL).endswith(extracted + "\n"))
        for rule in REQUIRED:
            self.assertIn(rule, extracted)

    def test_stops_and_exception_links_reach_real_full_sections(self) -> None:
        card = render_implementation(MANUAL)
        full = ContractDocument.load(MANUAL)
        anchors = {
            re.sub(r"[^\w\s-]", "", section.title.casefold()).replace(" ", "-")
            for section in full.sections
        }
        links = re.findall(r"\]\(\.\./story-contract\.md#([^\)]+)\)", card)
        self.assertGreaterEqual(len(links), 8)
        for anchor in links:
            self.assertIn(anchor, anchors, anchor)
        for condition in (
            "HALT on failure",
            "Never repair approval fields",
            "Locked test is wrong",
            "Required evidence or manual validation is unavailable",
            "instructions conflict or the situation is not covered",
            "read the **full**",
            "An omission is never permission",
            "ask the user or Vera",
            "never bash as a bypass",
        ):
            self.assertIn(condition, card)

    def run_check(self, custom: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--check", "--custom-dir", str(custom)],
            cwd=custom,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_stale_or_missing_card_fails_closed_without_writes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            custom = Path(directory)
            shutil.copy2(MANUAL, custom / MANUAL.name)
            missing = self.run_check(custom)
            self.assertEqual(1, missing.returncode)
            self.assertIn("Read the full", missing.stderr)
            self.assertFalse((custom / OUTPUT).exists())
            (custom / OUTPUT).parent.mkdir()
            (custom / OUTPUT).write_text(render_implementation(custom / MANUAL.name))
            self.assertEqual(0, self.run_check(custom).returncode)
            # Even a manual change outside the selected section invalidates its fingerprint.
            with (custom / MANUAL.name).open("a") as output:
                output.write("\nNew exception requires review.\n")
            before = (custom / OUTPUT).read_bytes()
            stale = self.run_check(custom)
            self.assertEqual(1, stale.returncode)
            self.assertIn("Read the full", stale.stderr)
            self.assertEqual(before, (custom / OUTPUT).read_bytes())

    def test_generator_refuses_a_missing_mandatory_stop(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / MANUAL.name
            path.write_text(
                MANUAL.read_text().replace("HALT on failure", "Continue on failure", 1)
            )
            with self.assertRaisesRegex(ValueError, "missing: HALT on failure"):
                render_implementation(path)

    def test_build_context_uses_card_without_shortening_other_stages(self) -> None:
        paths = [
            CUSTOM / "bmad-build.toml",
            CUSTOM / "bmad-build-auto.toml",
            *sorted((ROOT / "projects").glob("*/_bmad/custom/bmad-build.toml")),
        ]
        for path in paths:
            workflow = tomllib.loads(path.read_text())["workflow"]
            facts = " ".join(workflow["persistent_facts"])
            instructions = " ".join(workflow["activation_steps_append"])
            with self.subTest(workflow=str(path.relative_to(ROOT))):
                self.assertIn("independent test design/review or revision", facts)
                self.assertIn("story-contract.md completely", facts)
                self.assertIn("instructions/implementation.md", facts)
                self.assertIn("full-manual fallback", facts)
                self.assertIn("instructions/implementation.md", instructions)
                self.assertIn("validate --phase approved", instructions)
                self.assertIn("HALT", instructions)
                self.assertIn("bmad-code-review", workflow["on_complete"])


if __name__ == "__main__":
    unittest.main()
