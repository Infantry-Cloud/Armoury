"""Edit guard (#6): the real contract-guard extension, driven through a Node harness.

Runs the validator's `guard` command for real. Skips when Node cannot run TypeScript.
"""

from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TESTS = Path(__file__).resolve().parent
SCRIPTS = TESTS.parent
REPO = SCRIPTS.parents[2]
EXTENSION = REPO / ".pi/extensions/contract-guard.ts"
HARNESS = TESTS / "guard_harness.ts"


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


anchor = load("guard_anchor_helpers", TESTS / "test_jj_approval_anchor.py")
SPEC_PATH, TEST_PATH = anchor.SPEC_PATH, anchor.TEST_PATH


def node_runs_typescript() -> bool:
    node = shutil.which("node")
    if node is None:
        return False
    probe = subprocess.run(
        [node, "--input-type=module-typescript", "-e", "const x: number = 1"],
        capture_output=True,
        check=False,
    )
    return probe.returncode == 0


@unittest.skipUnless(node_runs_typescript(), "node with TypeScript support not found")
class EditGuardTests(unittest.TestCase):
    def setUp(self) -> None:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name).resolve()
        scripts = self.root / "_bmad/custom/scripts"
        scripts.mkdir(parents=True)
        shutil.copy2(SCRIPTS / "validate_story_contract.py", scripts)
        self.write(TEST_PATH, anchor.SCAFFOLD)
        self.approved = anchor.approve(anchor.fixtures.BUILD_SPEC)
        self.write(SPEC_PATH, self.approved)

    def write(self, relative: str, text: str) -> None:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def run_steps(self, *steps: dict) -> list:
        payload = {"extension": str(EXTENSION), "cwd": str(self.root), "steps": steps}
        result = subprocess.run(
            ["node", str(HARNESS)],
            input=json.dumps(payload),
            capture_output=True,
            text=True,
            check=True,
        )
        return json.loads(result.stdout)

    @staticmethod
    def edit(path: str, old: str, new: str) -> dict:
        return {
            "tool": "edit",
            "input": {"path": path, "edits": [{"oldText": old, "newText": new}]},
        }

    def assert_blocked(self, result: dict, fragment: str) -> None:
        self.assertTrue(result["blocked"], result)
        self.assertIn(fragment, result["reason"])

    def test_editing_the_approved_contract_is_blocked(self) -> None:
        [result] = self.run_steps(
            self.edit(
                SPEC_PATH, "Users can save a valid profile.", "Users can replace it."
            )
        )
        self.assert_blocked(result, "approved 'Acceptance Contract' section")

    def test_editing_approval_fields_is_blocked(self) -> None:
        [result] = self.run_steps(
            self.edit(SPEC_PATH, "- Approved by: Product Owner", "- Approved by: Agent")
        )
        self.assert_blocked(result, "approved 'Contract Approval' section")

    def test_rewriting_the_spec_with_write_is_blocked(self) -> None:
        changed = self.approved.replace("Users can save", "Users can delete")
        [result] = self.run_steps(
            {"tool": "write", "input": {"path": SPEC_PATH, "content": changed}}
        )
        self.assert_blocked(result, "Acceptance Contract")

    def test_delivery_evidence_and_notes_stay_writable(self) -> None:
        [result] = self.run_steps(
            self.edit(
                SPEC_PATH,
                "## Implementation Notes\n",
                "## Implementation Notes\n\n- VAL-1 PASS\n",
            )
        )
        self.assertFalse(result["blocked"], result)

    def test_unverifiable_edit_to_protected_spec_fails_closed(self) -> None:
        [result] = self.run_steps(self.edit(SPEC_PATH, "text that is not there", "x"))
        self.assert_blocked(result, "could not be verified")

    def test_activating_locked_scaffold_is_allowed(self) -> None:
        skip = "@pytest.mark.skip(reason='red phase: VAL-1')\n"
        [result] = self.run_steps(self.edit(TEST_PATH, skip, ""))
        self.assertFalse(result["blocked"], result)

    def test_weakening_locked_test_is_blocked(self) -> None:
        [result] = self.run_steps(
            self.edit(TEST_PATH, "save_profile({'name': 'Ada'}) == 'saved'", "True")
        )
        self.assert_blocked(result, "beyond removing skip markers")

    def test_user_unlock_allows_and_lock_restores(self) -> None:
        change = self.edit(
            SPEC_PATH, "Users can save a valid profile.", "Users can replace it."
        )
        before, _, during, _, after = self.run_steps(
            change,
            {"command": "contract-unlock", "args": SPEC_PATH},
            change,
            {"command": "contract-lock"},
            change,
        )
        self.assertTrue(before["blocked"])
        self.assertFalse(during["blocked"], during)
        self.assertTrue(after["blocked"])

    def test_draft_contracts_and_ordinary_files_are_untouched(self) -> None:
        self.write(SPEC_PATH, anchor.fixtures.BUILD_SPEC)
        results = self.run_steps(
            self.edit(
                SPEC_PATH, "Users can save a valid profile.", "Users can replace it."
            ),
            {"tool": "write", "input": {"path": "src/app.py", "content": "print(1)\n"}},
        )
        self.assertEqual([False, False], [r["blocked"] for r in results], results)

    def test_recording_approval_from_draft_is_allowed(self) -> None:
        self.write(SPEC_PATH, anchor.fixtures.BUILD_SPEC)
        [result] = self.run_steps(
            {"tool": "write", "input": {"path": SPEC_PATH, "content": self.approved}}
        )
        self.assertFalse(result["blocked"], result)


if __name__ == "__main__":
    unittest.main()
