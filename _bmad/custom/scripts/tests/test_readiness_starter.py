"""The readiness starter only blocks configured paths; AR supplies other integration."""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXTENSION = ROOT / ".pi/extensions/readiness-enforce.ts"
HARNESS = Path(__file__).with_name("guard_harness.ts")
STARTER_MARKER = "Project readiness starter: block configured write/edit paths only."


def uses_shared_starter() -> bool:
    """Project-owned AR extensions have their own tests, not this template's contract."""
    return EXTENSION.is_file() and STARTER_MARKER in EXTENSION.read_text()


def node_runs_typescript() -> bool:
    node = shutil.which("node")
    if node is None:
        return False
    result = subprocess.run(
        [node, "--input-type=module-typescript", "-e", "const x: number = 1"],
        capture_output=True,
        check=False,
    )
    return result.returncode == 0


@unittest.skipUnless(node_runs_typescript(), "node with TypeScript support not found")
@unittest.skipUnless(
    uses_shared_starter(), "project uses its own AR extension, not the shared starter"
)
class ReadinessStarterTests(unittest.TestCase):
    def setUp(self) -> None:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name).resolve()

    def run_starter(self, steps: list[dict], rules: dict | None = None) -> dict:
        if rules is not None:
            path = self.root / ".pi/readiness.rules.json"
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps(rules))
        result = subprocess.run(
            ["node", str(HARNESS)],
            input=json.dumps(
                {
                    "extension": str(EXTENSION),
                    "cwd": str(self.root),
                    "steps": steps,
                    "inspect": True,
                }
            ),
            capture_output=True,
            text=True,
            check=True,
        )
        return json.loads(result.stdout)

    def test_without_rules_no_hooks_or_commands_are_registered(self) -> None:
        output = self.run_starter(
            [
                {
                    "tool": "write",
                    "input": {"path": "src/utils/example.ts", "content": ""},
                }
            ]
        )
        self.assertEqual([], output["events"])
        self.assertEqual([], output["commands"])
        self.assertFalse(output["results"][0]["blocked"])

    def test_only_configured_write_and_edit_paths_are_blocked(self) -> None:
        output = self.run_starter(
            [
                {
                    "tool": "write",
                    "input": {"path": "src/utils/example.ts", "content": ""},
                },
                {"tool": "edit", "input": {"path": "helpers/example.ts"}},
                {"tool": "write", "input": {"path": "src/example.ts", "content": ""}},
                {"tool": "read", "input": {"path": "helpers/example.ts"}},
            ],
            {"blockPaths": ["(^|/)(utils|helpers)/"]},
        )
        self.assertEqual(
            [True, True, False, False], [r["blocked"] for r in output["results"]]
        )
        self.assertEqual(["tool_call"], output["events"])
        self.assertEqual([], output["commands"])

    def test_old_lint_and_context_settings_register_no_handlers(self) -> None:
        output = self.run_starter(
            [],
            {
                "lint": {".py": "must-not-run"},
                "context": "must-not-be-injected",
            },
        )
        self.assertEqual([], output["events"])
        self.assertEqual([], output["commands"])

    def test_old_settings_do_not_change_path_blocking(self) -> None:
        output = self.run_starter(
            [
                {"tool": "edit", "input": {"path": "forbidden/example.py"}},
            ],
            {
                "blockPaths": ["^forbidden/"],
                "lint": {".py": "must-not-run"},
                "context": "must-not-be-injected",
            },
        )
        self.assertEqual(["tool_call"], output["events"])
        self.assertTrue(output["results"][0]["blocked"])


if __name__ == "__main__":
    unittest.main()
