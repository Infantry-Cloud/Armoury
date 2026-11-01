"""Local deployment/wiring checks; these do not pretend to test live Linear MCP writes."""

from __future__ import annotations

import contextlib
import io
import json
import subprocess
import tempfile
import unittest
from collections.abc import Mapping
from pathlib import Path

import tomllib

from _bmad.custom.scripts.install_linear import deploy, read_config
from _bmad.custom.scripts.jj_wiring import PROCEDURE_FACTS

ROOT = Path(__file__).resolve().parents[4]


@unittest.skipUnless((ROOT / "sync.sh").is_file(), "shared-repo test: needs sync.sh")
class LinearIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.destination = self.root / "project"
        (self.destination / "_bmad").mkdir(parents=True)

    def write_config(self, relative: str, value: Mapping[str, object]) -> Path:
        path = self.destination / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value))
        return path

    def snapshot(self) -> dict[str, bytes]:
        return {
            str(path.relative_to(self.destination)): path.read_bytes()
            for path in self.destination.rglob("*")
            if path.is_file()
        }

    def install(
        self,
        *,
        dry_run: bool = False,
        backup_dir: Path | None = None,
        overlay: Path | None = None,
    ) -> list[Path]:
        with contextlib.redirect_stdout(io.StringIO()):
            return deploy(
                ROOT,
                self.destination,
                dry_run=dry_run,
                backup_dir=backup_dir,
                overlay=overlay,
            )

    def test_new_deployment_and_idempotent_resync(self) -> None:
        self.assertEqual(len(self.install()), 3)
        for relative in (".mcp.json", ".pi/mcp.json"):
            self.assertEqual(
                read_config(self.destination / relative),
                read_config(ROOT / "_bmad/custom/linear-mcp.json"),
            )
        self.assertTrue(
            (self.destination / ".agents/skills/bmad-linear/SKILL.md").is_file()
        )
        before = self.snapshot()
        self.assertEqual(self.install(), [])
        self.assertEqual(self.snapshot(), before)

    def test_existing_servers_runtime_settings_and_auth_are_preserved(self) -> None:
        config = {
            "mcpServers": {"other": {"url": "https://example.com/mcp"}},
            "autoEnableCodemode": False,
            "auth": {"token": "fixture-only"},
        }
        self.write_config(".mcp.json", config)
        path = self.write_config(".pi/mcp.json", config)
        path.chmod(0o600)
        self.install()
        for relative in (".mcp.json", ".pi/mcp.json"):
            merged = read_config(self.destination / relative)
            self.assertEqual(merged["auth"], config["auth"])
            self.assertFalse(merged["autoEnableCodemode"])
            servers = merged["mcpServers"]
            assert isinstance(servers, dict)
            self.assertEqual(servers["other"], {"url": "https://example.com/mcp"})
        self.assertEqual(path.stat().st_mode & 0o777, 0o600)

    def test_existing_linear_choices_are_not_replaced(self) -> None:
        config = {
            "mcpServers": {"linear": {"command": "approved-adapter", "enabled": False}}
        }
        paths = [
            self.write_config(relative, config)
            for relative in (".mcp.json", ".pi/mcp.json")
        ]
        before = [path.read_bytes() for path in paths]
        self.install()
        self.assertEqual([path.read_bytes() for path in paths], before)

    def test_dry_run_creates_no_files_or_backup(self) -> None:
        before = self.snapshot()
        backup = self.root / "backup"
        self.assertEqual(len(self.install(dry_run=True, backup_dir=backup)), 3)
        self.assertEqual(self.snapshot(), before)
        self.assertFalse(backup.exists())

    def test_invalid_config_is_rejected_before_any_write(self) -> None:
        self.write_config(".pi/mcp.json", {"mcpServers": []})
        before = self.snapshot()
        with self.assertRaises(TypeError):
            self.install()
        self.assertEqual(self.snapshot(), before)

    def test_backup_keeps_original_bytes_and_prior_overlay_snapshot(self) -> None:
        path = self.write_config(".mcp.json", {"mcpServers": {}})
        path.chmod(0o600)
        before = path.read_bytes()
        backup = self.root / "backup"
        self.install(backup_dir=backup)
        self.assertEqual((backup / ".mcp.json").read_bytes(), before)
        self.assertEqual((backup / ".mcp.json").stat().st_mode & 0o777, 0o600)
        path.write_text('{"mcpServers": {}}')
        self.install(backup_dir=backup)
        self.assertEqual((backup / ".mcp.json").read_bytes(), before)

    def test_overlay_config_and_skill_win_even_in_dry_run(self) -> None:
        overlay = self.root / "overlay"
        overlay.mkdir()
        (overlay / ".mcp.json").write_text(
            '{"mcpServers": {"overlay": {"url": "https://example.com/mcp"}}}'
        )
        skill = overlay / ".agents/skills/bmad-linear/SKILL.md"
        skill.parent.mkdir(parents=True)
        skill.write_text("project-specific skill")
        before = self.snapshot()
        self.install(overlay=overlay, dry_run=True)
        self.assertEqual(self.snapshot(), before)
        self.install(overlay=overlay)
        servers = read_config(self.destination / ".mcp.json")["mcpServers"]
        assert isinstance(servers, dict)
        self.assertIn("overlay", servers)
        self.assertEqual(
            (self.destination / ".agents/skills/bmad-linear/SKILL.md").read_text(),
            skill.read_text(),
        )

    def test_symlink_cannot_deploy_outside_destination(self) -> None:
        external = self.root / "external"
        external.mkdir()
        (self.destination / ".agents").symlink_to(external, target_is_directory=True)
        with self.assertRaises(ValueError):
            self.install()
        self.assertFalse((self.destination / ".mcp.json").exists())
        self.assertEqual(list(external.iterdir()), [])

    def test_sync_preserves_binding_and_personal_overrides(self) -> None:
        state = self.destination / "_bmad/linear/projects/recon.json"
        state.parent.mkdir(parents=True)
        state.write_text('{"project": {"id": "confirmed-id"}}')
        personal = self.destination / "_bmad/custom/config.user.toml"
        personal.parent.mkdir(parents=True)
        personal.write_text('[core]\nuser_name = "Fixture"\n')
        native = self.destination / "_bmad/custom/ticketing-store-config.toml"
        native.write_text('[tickets]\nstore = "linear"\nteam = "FIXTURE"\n')
        before = self.snapshot()
        preview = subprocess.run(
            ["bash", str(ROOT / "sync.sh"), "--dry-run", str(self.destination)],
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("would install .pi/mcp.json", preview.stdout)
        self.assertEqual(self.snapshot(), before)
        subprocess.run(
            ["bash", str(ROOT / "sync.sh"), str(self.destination)],
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertEqual(
            state.read_bytes(), before[str(state.relative_to(self.destination))]
        )
        self.assertEqual(
            personal.read_bytes(), before[str(personal.relative_to(self.destination))]
        )
        self.assertEqual(
            native.read_bytes(), before[str(native.relative_to(self.destination))]
        )
        self.assertTrue(
            (self.destination / ".agents/skills/bmad-linear/SKILL.md").exists()
        )

    def test_sync_invalid_mcp_fails_before_replacing_customisations(self) -> None:
        original = self.destination / "project-context.md"
        original.write_text("must survive")
        self.write_config(".pi/mcp.json", {"mcpServers": []})
        before = self.snapshot()
        result = subprocess.run(
            ["bash", str(ROOT / "sync.sh"), str(self.destination)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.snapshot(), before)

    def test_sync_backs_up_mcp_and_skill_and_repeat_is_unchanged(self) -> None:
        self.write_config(".mcp.json", {"mcpServers": {}})
        self.write_config(".pi/mcp.json", {"mcpServers": {}})
        skill = self.destination / ".agents/skills/bmad-linear/SKILL.md"
        skill.parent.mkdir(parents=True)
        skill.write_text("older shared skill")
        before = self.snapshot()
        backup = self.root / "backup"
        subprocess.run(
            [
                "bash",
                str(ROOT / "sync.sh"),
                "--backup-dir",
                str(backup),
                str(self.destination),
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        for relative in (
            ".mcp.json",
            ".pi/mcp.json",
            ".agents/skills/bmad-linear/SKILL.md",
        ):
            self.assertEqual((backup / relative).read_bytes(), before[relative])
        installed = self.snapshot()
        repeat_backup = self.root / "repeat-backup"
        subprocess.run(
            [
                "bash",
                str(ROOT / "sync.sh"),
                "--backup-dir",
                str(repeat_backup),
                str(self.destination),
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertEqual(self.snapshot(), installed)
        self.assertEqual(list(repeat_backup.rglob("*")), [])

    def test_malformed_config_error_does_not_print_credentials(self) -> None:
        path = self.destination / ".mcp.json"
        path.write_text('{"secret": "fixture-not-for-logs"')
        result = subprocess.run(
            [
                "python3",
                str(ROOT / "_bmad/custom/scripts/install_linear.py"),
                "--source",
                str(ROOT),
                "--destination",
                str(self.destination),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn("fixture-not-for-logs", result.stdout + result.stderr)
        self.assertFalse((self.destination / ".pi/mcp.json").exists())

    def test_full_sync_merges_overlay_without_losing_existing_mcp_choices(self) -> None:
        source = self.root / "source"
        for relative in (
            "sync.sh",
            "project-context.md",
            "_bmad/custom/linear-mcp.json",
            "_bmad/custom/scripts/install_linear.py",
            ".agents/skills/bmad-linear/SKILL.md",
            ".pi/extensions/readiness-enforce.ts",
            ".pi/extensions/contract-guard.ts",
        ):
            path = source / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes((ROOT / relative).read_bytes())
        existing = {
            "mcpServers": {
                "existing": {"url": "https://existing.example/mcp"},
                "linear": {"command": "approved-adapter"},
            },
            "autoEnableCodemode": True,
        }
        incoming = {
            "mcpServers": {
                "overlay": {"url": "https://overlay.example/mcp"},
                "linear": {"url": "https://mcp.linear.app/mcp"},
            },
            "autoEnableCodemode": False,
        }
        for relative in (".mcp.json", ".pi/mcp.json"):
            self.write_config(relative, existing)
            overlay_file = source / "projects/project" / relative
            overlay_file.parent.mkdir(parents=True, exist_ok=True)
            overlay_file.write_text(json.dumps(incoming))
        before = self.snapshot()
        subprocess.run(
            ["bash", str(source / "sync.sh"), "--dry-run", str(self.destination)],
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertEqual(self.snapshot(), before)
        subprocess.run(
            ["bash", str(source / "sync.sh"), str(self.destination)],
            capture_output=True,
            text=True,
            check=True,
        )
        for relative in (".mcp.json", ".pi/mcp.json"):
            merged = read_config(self.destination / relative)
            self.assertIs(merged["autoEnableCodemode"], True)
            servers = merged["mcpServers"]
            assert isinstance(servers, dict)
            self.assertEqual(servers["linear"], {"command": "approved-adapter"})
            self.assertIn("existing", servers)
            self.assertIn("overlay", servers)

    def test_epic_completion_is_review_then_accepted_retrospective(self) -> None:
        trees = [
            ROOT / "_bmad/custom",
            *sorted((ROOT / "projects").glob("*/_bmad/custom")),
        ]
        for tree in trees:
            path = tree / "bmad-code-review.toml"
            if not path.exists():
                continue
            with self.subTest(review=str(path.relative_to(ROOT))):
                completion = tomllib.loads(path.read_text())["workflow"]["on_complete"]
                self.assertIn("Linear Epic completion (Code Review stage)", completion)
                self.assertIn("after the last accepted story", completion)
                self.assertIn("set its epic In Review, never Done", completion)
                self.assertIn("do not close the Linear Project", completion)
                self.assertLess(
                    completion.index("Linear Epic completion"),
                    completion.index("RV <spec_file>"),
                )
            retrospective = tree / "bmad-retrospective.toml"
            if retrospective.exists():
                completion = tomllib.loads(retrospective.read_text())["workflow"][
                    "on_complete"
                ]
                self.assertIn(
                    "Linear Epic completion (Retrospective stage)", completion
                )
                self.assertIn(
                    "explicit acceptance of the saved retrospective", completion
                )
                self.assertIn(
                    "current delivery of every agreed child story", completion
                )
                self.assertIn("move only that epic to Done", completion)
                self.assertIn(
                    "unaccepted retrospectives leave the epic open", completion
                )
                self.assertIn("never close the Linear Project", completion)

    def test_epic_completion_guards_scope_evidence_and_reconciliation(self) -> None:
        text = (ROOT / "_bmad/custom/linear-workflow.md").read_text()
        section = " ".join(
            text.split("## Epic completion — review then retrospective", 1)[1]
            .split("## Reconcile, failures and reporting", 1)[0]
            .split()
        )
        for phrase in (
            "Every agreed child story has current, independently accepted local delivery evidence",
            "user explicitly accepts the saved retrospective",
            "including agreed stories not yet published",
            "Exclude only explicitly cancelled work",
            "Empty or ambiguous scope, unknown children, a failed gate or remote Done alone never",
            "configured review fallback",
            "current child keys/revisions/digests",
            "Preserve an already-Done epic",
            "New/reopened work invalidates that closure",
            "require fresh retrospective acceptance",
            "Publication failures stay pending/uncertain",
            "never for the Linear Project",
        ):
            with self.subTest(rule=phrase):
                self.assertIn(phrase, section)

    def test_epic_milestones_and_activity_notes_are_specified(self) -> None:
        text = " ".join((ROOT / "_bmad/custom/linear-workflow.md").read_text().split())
        milestones = text.split("### Epic milestones", 1)[1].split(
            "## Activity notes", 1
        )[0]
        for phrase in (
            "upsert its milestone before the epic issue",
            "never match on name alone",
            "Do not set a target date unless the user agreed one",
            "every story, bug, spike and task under it",
            "Planning issues and standalone bugs have no milestone",
            "Never delete or rename-reuse a milestone",
            "record each milestone as `pending`",
        ):
            with self.subTest(milestone_rule=phrase):
                self.assertIn(phrase, milestones)
        self.assertIn("`BMAD-ID: <binding_id>:<epic key>:milestone`", text)
        notes = text.split("## Activity notes", 1)[1].split(
            "## Epic completion", 1
        )[0]
        for phrase in (
            "Comment on the epic issue, then a project status update",
            "`BMAD-NOTE: <binding_id>:<key>:<event>:<cycle>`",
            "Post a note only after its status change is confirmed",
            "look for its marker",
            "Never invent evidence, approvals or success",
            "A note is a report, not approval",
            "A failed note never blocks or rolls back the local workflow",
            "Use `offTrack` only when the user says so",
        ):
            with self.subTest(note_rule=phrase):
                self.assertIn(phrase, notes)
        reconcile = text.split("## Reconcile, failures and reporting", 1)[1]
        self.assertIn("upserts missing epic milestones", reconcile)
        self.assertIn("retries `pending`/`uncertain` notes", reconcile)

    def test_completion_hooks_post_activity_notes(self) -> None:
        trees = [
            ROOT / "_bmad/custom",
            *sorted((ROOT / "projects").glob("*/_bmad/custom")),
        ]
        hooks = {
            "bmad-build.toml": "Activity notes",
            "bmad-build-auto.toml": "Activity notes",
            "bmad-code-review.toml": "Activity notes",
            "bmad-retrospective.toml": "project status update",
            "bmad-correct-course.toml": "Activity notes",
            "bmad-create-epics-and-stories.toml": "milestone",
        }
        for tree in trees:
            for name, phrase in hooks.items():
                path = tree / name
                if not path.exists():
                    continue
                with self.subTest(hook=str(path.relative_to(ROOT))):
                    completion = tomllib.loads(path.read_text())["workflow"][
                        "on_complete"
                    ]
                    self.assertIn(phrase, completion)

    def test_planning_delivery_and_agent_surfaces_are_wired(self) -> None:
        workflows = (
            "prd",
            "product-brief",
            "architecture",
            "ux",
            "spec",
            "prfaq",
            "brainstorming",
            "deep-recon",
            "project-context",
            "create-epics-and-stories",
            "sprint-planning",
            "build",
            "build-auto",
            "code-review",
            "correct-course",
            "retrospective",
            "testarch-atdd",
            "testarch-test-design",
            "testarch-automate",
            "testarch-test-review",
            "testarch-trace",
            "qa-generate-e2e-tests",
            "ticket",
        )
        for name in workflows:
            with self.subTest(workflow=name):
                config = tomllib.loads(
                    (ROOT / f"_bmad/custom/bmad-{name}.toml").read_text()
                )["workflow"]
                self.assertIn(
                    PROCEDURE_FACTS["linear-workflow.md"],
                    config["persistent_facts"],
                )
                self.assertIn("Linear", " ".join(config["activation_steps_append"]))
                self.assertIn("Linear", config["on_complete"])
        context_workflow = tomllib.loads(
            (ROOT / "_bmad/custom/bmad-project-context.toml").read_text()
        )["workflow"]
        self.assertIn(
            "main-flow completion instruction",
            " ".join(context_workflow["activation_steps_append"]),
        )
        for name in ("analyst", "pm", "architect", "dev"):
            config = tomllib.loads(
                (ROOT / f"_bmad/custom/bmad-agent-{name}.toml").read_text()
            )["agent"]
            self.assertEqual(sum(item["code"] == "LP" for item in config["menu"]), 1)
        for relative in ("project-context.md", "projects/strata/project-context.md"):
            self.assertIn("## Linear project workflow", (ROOT / relative).read_text())
        self.assertIn(
            "Linear Planning completion for AR",
            (ROOT / "_bmad/custom/agent-readiness-workflow.md").read_text(),
        )


if __name__ == "__main__":
    unittest.main()
