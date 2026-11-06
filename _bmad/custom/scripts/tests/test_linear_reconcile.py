"""Reconcile drift plan: refactored breakdowns and Linear-side edits (no live MCP)."""

from __future__ import annotations

import contextlib
import copy
import io
import json
import tempfile
import unittest
from pathlib import Path
from typing import Any

from _bmad.custom.scripts import linear_reconcile as lr

BINDING = "0b6f3f9e-2b7c-4d1e-9a51-3c2d7e8f9a10"
PROJECT = "project-1"

BASE = """\
# Recon - Epic Breakdown

## Epic List

### Epic 1: Import data
Users can import reconnaissance data.

### Epic 2: Report findings
Users can report what they found.

## Epic 1: Import data

Users can import reconnaissance data.

### Story 1.1: Upload CSV

As an analyst, I want to upload a CSV.

**Given** a file **When** uploaded **Then** rows are stored

### Story 1.2: Validate rows

As an analyst, I want invalid rows rejected.

**Given** a bad row **When** imported **Then** it is reported

## Epic 2: Report findings

Users can report what they found.

### Story 2.1: Show summary

As an analyst, I want a summary page.

```
### Story 9.9: Not a story (inside a fence)
```
"""


def key_for(local: lr.Local) -> str:
    if local.kind == "epic":
        return f"epic:{local.id}"
    epic, story = local.id.split(".")
    return f"story:{epic}:{story}"


def block(key: str, local: lr.Local | None, extra: str = "") -> str:
    source = f"BMAD-SOURCE: {local.path}#{local.id} {local.digest}\n" if local else ""
    return (
        f"Human notes stay here.\n\n---\nBMAD-managed - change it in BMAD, not in Linear.\n"
        f"Acceptance summary.{extra}\n{source}BMAD-ID: {BINDING}:{key}"
    )


class Fixture:
    """A project whose manifest and Linear snapshot are in sync with BASE."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.epics = root / "_bmad-output/planning/epics.md"
        self.epics.parent.mkdir(parents=True)
        self.epics.write_text(BASE)
        self.manifest_path = root / "_bmad/linear/projects/recon.json"
        self.manifest_path.parent.mkdir(parents=True)
        (root / "_bmad/linear/active.json").write_text(
            '{"manifest": "projects/recon.json"}'
        )
        self.remote_path = root / "remote.json"
        local, warnings = lr.parse_epics([self.epics], root)
        assert not warnings, warnings
        items, issues, milestones = [], [], []
        for entry in local:
            key = key_for(entry)
            parent = None if entry.kind == "epic" else f"epic:{entry.epic}"
            milestone_id = f"ms-{entry.epic}"
            item: dict[str, Any] = {
                "key": key,
                "kind": entry.kind,
                "title": entry.title,
                "source": {"path": entry.path, "id": entry.id},
                "parent_key": parent,
                "after": [],
                "publication": "published",
                "id": f"id-{key}",
                "identifier": f"REC-{len(items) + 1}",
            }
            description = block(key, entry)
            item["synced"] = {
                "source_id": entry.id,
                "source_title": entry.title,
                "source_digest": entry.digest,
                "title": entry.desired_title,
                "parent_id": f"id-{parent}" if parent else None,
                "milestone_id": milestone_id,
                "block_digest": lr.digest(lr.managed_block(description) or ""),
            }
            if entry.kind == "epic":
                item["milestone"] = {
                    "publication": "published",
                    "id": milestone_id,
                    "name": entry.desired_title,
                }
                item["synced"]["milestone_name"] = entry.desired_title
                milestones.append(
                    {
                        "id": milestone_id,
                        "name": entry.desired_title,
                        "description": f"Goal\nBMAD-ID: {BINDING}:{key}:milestone",
                    }
                )
            items.append(item)
            issues.append(
                {
                    "id": item["id"],
                    "identifier": item["identifier"],
                    "title": entry.desired_title,
                    "description": description,
                    "parent_id": item["synced"]["parent_id"],
                    "milestone_id": milestone_id,
                    "project_id": PROJECT,
                    "status": "backlog",
                }
            )
        self.manifest: dict[str, Any] = {
            "schema_version": 1,
            "binding_id": BINDING,
            "name": "Recon",
            "project": {"id": PROJECT, "url": "https://linear.app/x/project/recon"},
            "publication_approved": True,
            "items": items,
        }
        self.remote: dict[str, Any] = {
            "project": {"id": PROJECT},
            "issues": issues,
            "milestones": milestones,
        }
        self.save()

    def save(self) -> None:
        self.manifest_path.write_text(json.dumps(self.manifest))
        self.remote_path.write_text(json.dumps(self.remote))

    def issue(self, key: str) -> dict[str, Any]:
        return next(i for i in self.remote["issues"] if i["id"] == f"id-{key}")

    def item(self, key: str) -> dict[str, Any]:
        return next(i for i in self.manifest["items"] if i["key"] == key)

    def run(
        self, *extra: str, remote: bool = True, command: str = "plan"
    ) -> tuple[int, dict[str, Any]]:
        self.save()
        argv = [command, "--root", str(self.root), "--epics", str(self.epics)]
        if remote:
            argv += ["--remote", str(self.remote_path)]
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = lr.main([*argv, *extra])
        return code, json.loads(out.getvalue())


def actions(plan: dict[str, Any], key: str | None = None) -> set[str]:
    return {s["action"] for s in plan["steps"] if key is None or s["key"] == key}


class ReconcilePlanTests(unittest.TestCase):
    def setUp(self) -> None:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.fx = Fixture(Path(directory.name))

    def edit(self, old: str, new: str) -> None:
        text = self.fx.epics.read_text()
        self.assertIn(old, text)
        self.fx.epics.write_text(text.replace(old, new))

    def test_in_sync_project_has_no_drift_and_check_passes(self) -> None:
        code, plan = self.fx.run("--check")
        self.assertEqual(code, 0, plan["steps"])
        self.assertFalse(plan["drift"])
        self.assertNotIn("9.9", json.dumps(plan["matched"]))

    def test_inserted_story_keeps_existing_identities_and_avoids_key_reuse(
        self,
    ) -> None:
        self.edit("### Story 1.2: Validate rows", "### Story 1.3: Validate rows")
        self.edit(
            "## Epic 2: Report findings\n\nUsers", "## Epic 2: Report findings\n\nUsers"
        )
        self.edit(
            "### Story 1.3: Validate rows",
            "### Story 1.2: Deduplicate uploads\n\nAs an analyst, I want duplicate files ignored.\n\n"
            "### Story 1.3: Validate rows",
        )
        code, plan = self.fx.run("--check")
        self.assertEqual(code, lr.EXIT_DRIFT)
        self.assertIn("remap-source", actions(plan, "story:1:2"))
        self.assertIn("update-title", actions(plan, "story:1:2"))
        new = plan["new"]
        self.assertEqual([n["proposed_key"] for n in new], ["story:1:2~2"])
        self.assertEqual(new[0]["parent_key"], "epic:1")
        self.assertIn("create", actions(plan, "story:1:2~2"))
        self.assertFalse(plan["needs_user"])

    def test_story_moved_to_another_epic_moves_parent_and_milestone(self) -> None:
        moved = (
            "### Story 1.2: Validate rows\n\nAs an analyst, I want invalid rows rejected.\n\n"
            "**Given** a bad row **When** imported **Then** it is reported\n\n"
        )
        self.edit(moved, "")
        self.edit(
            "### Story 2.1: Show summary",
            moved.replace("1.2", "2.2") + "### Story 2.1: Show summary",
        )
        _, plan = self.fx.run()
        found = actions(plan, "story:1:2")
        self.assertTrue(
            {
                "remap-source",
                "move",
                "update-parent",
                "update-milestone",
                "update-title",
            }
            <= found,
            found,
        )
        move = next(s for s in plan["steps"] if s["action"] == "update-milestone")
        self.assertEqual(move["desired"], "ms-2")
        self.assertEqual(plan["new"], [])

    def test_renumbered_epics_rename_milestones_without_new_identities(self) -> None:
        text = self.fx.epics.read_text()
        text = (
            text.replace("Epic 1:", "Epic X:")
            .replace("Epic 2:", "Epic 1:")
            .replace("Epic X:", "Epic 2:")
            .replace("Story 1.", "Story X.")
            .replace("Story 2.", "Story 1.")
            .replace("Story X.", "Story 2.")
        )
        self.fx.epics.write_text(text)
        _, plan = self.fx.run()
        self.assertEqual(plan["new"], [])
        self.assertIn("update-milestone-name", actions(plan, "epic:1"))
        self.assertIn("remap-source", actions(plan, "story:2:1"))
        self.assertNotIn("move", actions(plan))
        self.assertFalse(plan["needs_user"])

    def test_retitled_story_matches_by_body(self) -> None:
        self.edit("Story 1.1: Upload CSV", "Story 1.1: Upload spreadsheet")
        _, plan = self.fx.run()
        self.assertTrue({"retitle", "update-title"} <= actions(plan, "story:1:1"))
        self.assertEqual(plan["new"], [])

    def test_ambiguous_replacement_needs_user_and_creates_nothing(self) -> None:
        self.edit(
            "### Story 1.2: Validate rows\n\nAs an analyst, I want invalid rows rejected.",
            "### Story 1.2: Validate imported rows\n\nAs an analyst, I want a row report.",
        )
        self.edit("**Given** a bad row **When** imported **Then** it is reported", "")
        _, plan = self.fx.run()
        self.assertTrue(plan["needs_user"])
        self.assertIn("confirm-identity", actions(plan))
        self.assertIn("missing-locally", actions(plan, "story:1:2"))
        self.assertNotIn("create", actions(plan))

    def test_user_confirmed_mapping_is_honoured(self) -> None:
        self.edit(
            "### Story 1.2: Validate rows\n\nAs an analyst, I want invalid rows rejected.",
            "### Story 1.2: Row report\n\nAs an analyst, I want a row report.",
        )
        self.fx.item("story:1:2")["source"]["confirmed"] = True
        _, plan = self.fx.run()
        self.assertNotIn("confirm-identity", actions(plan))
        self.assertTrue(
            {"retitle", "content-changed", "refresh-block"}
            <= actions(plan, "story:1:2")
        )

    def test_removed_story_is_flagged_never_cancelled_automatically(self) -> None:
        self.edit(
            "### Story 2.1: Show summary\n\nAs an analyst, I want a summary page.\n", ""
        )
        _, plan = self.fx.run()
        self.assertEqual(actions(plan, "story:2:1"), {"missing-locally"})
        self.assertNotIn("cancel", actions(plan))

    def test_cancelled_item_is_cancelled_remotely_once_approved(self) -> None:
        self.edit(
            "### Story 2.1: Show summary\n\nAs an analyst, I want a summary page.\n", ""
        )
        self.fx.item("story:2:1")["lifecycle"] = "cancelled"
        _, plan = self.fx.run()
        self.assertEqual(actions(plan, "story:2:1"), {"cancel"})
        self.fx.issue("story:2:1")["status"] = "canceled"
        _, plan = self.fx.run("--check")
        self.assertEqual(actions(plan, "story:2:1"), set())

    def test_remote_edits_restore_or_conflict_three_way(self) -> None:
        self.fx.issue("story:1:1")["title"] = "Upload a CSV (edited in Linear)"
        _, plan = self.fx.run()
        self.assertIn("restore-title", actions(plan, "story:1:1"))
        self.assertFalse(plan["needs_user"])
        self.edit("Story 1.1: Upload CSV", "Story 1.1: Upload spreadsheet")
        _, plan = self.fx.run()
        self.assertIn("conflict-title", actions(plan, "story:1:1"))
        self.assertTrue(plan["needs_user"])

    def test_managed_block_edits_and_stale_source(self) -> None:
        issue = self.fx.issue("story:1:2")
        local = lr.parse_epics([self.fx.epics], self.fx.root)[0]
        story = next(e for e in local if e.id == "1.2")
        issue["description"] = block("story:1:2", story, extra=" Plus a Linear edit.")
        _, plan = self.fx.run()
        self.assertIn("restore-block", actions(plan, "story:1:2"))
        self.edit("invalid rows rejected", "invalid rows rejected with a reason")
        _, plan = self.fx.run()
        self.assertIn("conflict-block", actions(plan, "story:1:2"))
        issue["description"] = issue["description"].replace(" Plus a Linear edit.", "")
        _, plan = self.fx.run()
        self.assertTrue(
            {"content-changed", "refresh-block"} <= actions(plan, "story:1:2")
        )

    def test_markdown_round_trip_is_not_an_edit(self) -> None:
        issue = self.fx.issue("story:1:1")
        issue["description"] = issue["description"].replace(
            "BMAD-managed", "* BMAD\\-managed"
        )
        issue["description"] = issue["description"].replace(
            "BMAD\\-managed", "BMAD-managed"
        )
        _, plan = self.fx.run("--check")
        self.assertFalse(plan["drift"], plan["steps"])

    def test_markdown_escaped_source_line_is_current(self) -> None:
        # Linear stores `_bmad-output` as `\_bmad-output`; that is not a stale source.
        issue = self.fx.issue("story:1:1")
        self.assertIn("BMAD-SOURCE: _bmad-output/", issue["description"])
        issue["description"] = issue["description"].replace(
            "BMAD-SOURCE: _bmad-output/", "BMAD-SOURCE: \\_bmad-output/"
        )
        self.fx.item("story:1:1").pop("synced")
        _, plan = self.fx.run()
        self.assertEqual(actions(plan, "story:1:1"), {"no-baseline"}, plan["steps"])
        _, result = self.fx.run("--write", command="baseline")
        self.assertIn("story:1:1", result["recorded"])
        self.fx.manifest = json.loads(self.fx.manifest_path.read_text())
        _, plan = self.fx.run()
        self.assertEqual(actions(plan, "story:1:1"), set(), plan["steps"])

    def test_remote_identity_problems_need_user(self) -> None:
        self.fx.remote["issues"].remove(self.fx.issue("story:2:1"))
        duplicate = copy.deepcopy(self.fx.issue("story:1:1"))
        duplicate["id"], duplicate["identifier"] = "dup", "REC-99"
        self.fx.remote["issues"].append(duplicate)
        self.fx.remote["issues"].append(
            {
                "id": "u1",
                "identifier": "REC-50",
                "title": "Ad hoc",
                "description": "no marker",
                "project_id": PROJECT,
            }
        )
        self.fx.remote["issues"].append(
            {
                "id": "u2",
                "identifier": "REC-51",
                "title": "Stray",
                "description": f"BMAD-ID: {BINDING}:story:7:7",
                "project_id": PROJECT,
            }
        )
        _, plan = self.fx.run()
        self.assertIn("remote-missing", actions(plan, "story:2:1"))
        self.assertIn("duplicate-remote", actions(plan, "story:1:1"))
        self.assertIn("unmanaged", actions(plan, "REC-50"))
        self.assertIn("remote-unknown", actions(plan, "story:7:7"))
        self.assertTrue(plan["needs_user"])

    def test_unpublished_item_adopts_marker_instead_of_creating(self) -> None:
        item = self.fx.item("story:2:1")
        item.pop("id")
        _, plan = self.fx.run()
        adopt = [s for s in plan["steps"] if s["action"] == "adopt"]
        self.assertEqual(adopt[0]["remote_id"], "id-story:2:1")
        self.assertNotIn("create", actions(plan))

    def test_remote_status_is_never_imported(self) -> None:
        status = self.fx.root / "sprint-status.yaml"
        status.write_text(
            "development_status:\n  epic-1: in-progress\n  1-1-upload-csv: review\n"
            "  1-2-validate-rows: backlog # comment\n  2-1-show-summary: backlog\n"
        )
        self.fx.issue("story:1:2")["status"] = "done"
        _, plan = self.fx.run("--sprint-status", str(status))
        self.assertIn("status-ahead", actions(plan, "story:1:2"))
        self.assertIn("status-behind", actions(plan, "story:1:1"))
        ahead = next(s for s in plan["steps"] if s["action"] == "status-ahead")
        self.assertTrue(ahead["needs_user"])

    def test_dangling_dependency_is_reported(self) -> None:
        self.fx.item("story:1:2")["after"] = ["story:1:1", "story:9:9"]
        _, plan = self.fx.run()
        self.assertIn("dangling-dependency", actions(plan, "story:1:2"))

    def test_duplicate_story_heading_blocks(self) -> None:
        self.edit(
            "### Story 2.1: Show summary",
            "### Story 1.1: Again\n\n### Story 2.1: Show summary",
        )
        code, plan = self.fx.run("--check")
        self.assertEqual(code, lr.EXIT_DRIFT)
        self.assertFalse(plan["ok"])
        self.assertEqual(plan["warnings"][0]["code"], "duplicate-story")

    def test_local_only_check_detects_breakdown_edits(self) -> None:
        code, _ = self.fx.run("--check", remote=False)
        self.assertEqual(code, 0)
        self.edit("I want a summary page.", "I want a summary page with charts.")
        code, plan = self.fx.run("--check", remote=False)
        self.assertEqual(code, lr.EXIT_DRIFT)
        self.assertEqual(actions(plan), {"content-changed"})

    def test_baseline_records_only_proven_in_sync_items(self) -> None:
        moved = (
            "### Story 1.2: Validate rows\n\nAs an analyst, I want invalid rows rejected.\n\n"
            "**Given** a bad row **When** imported **Then** it is reported\n\n"
        )
        self.edit(moved, "")
        self.edit(
            "### Story 2.1: Show summary",
            moved.replace("1.2", "2.2") + "### Story 2.1: Show summary",
        )
        self.fx.issue("story:2:1")["title"] = "Edited in Linear"
        before = self.fx.manifest_path.read_text()
        code, result = self.fx.run(command="baseline")
        self.assertEqual(code, 0)
        self.assertEqual(
            self.fx.manifest_path.read_text(), before, "dry run must not write"
        )
        self.assertIn("story:1:2", result["skipped"])
        # Agent applies the move in Linear, then re-snapshots.
        issue = self.fx.issue("story:1:2")
        local = {e.id: e for e in lr.parse_epics([self.fx.epics], self.fx.root)[0]}
        issue.update(
            title="Story 2.2: Validate rows",
            parent_id="id-epic:2",
            milestone_id="ms-2",
            description=block("story:1:2", local["2.2"]),
        )
        code, result = self.fx.run("--write", command="baseline")
        self.assertIn("story:1:2", result["recorded"])
        self.assertIn("story:2:1", result["skipped"])
        saved = json.loads(self.fx.manifest_path.read_text())
        item = next(i for i in saved["items"] if i["key"] == "story:1:2")
        self.assertEqual(item["source"]["id"], "2.2")
        self.assertEqual(item["parent_key"], "epic:2")
        self.assertEqual(item["source_history"][0]["id"], "1.2")
        self.fx.manifest = saved
        _, plan = self.fx.run()
        self.assertEqual(actions(plan, "story:1:2"), set())

    def add_item(
        self, key: str, kind: str, parent: str | None, milestone: str | None
    ) -> None:
        description = block(key, None)
        self.fx.manifest["items"].append(
            {
                "key": key,
                "kind": kind,
                "title": f"{kind} {key}",
                "parent_key": parent,
                "id": f"id-{key}",
                "publication": "published",
                "synced": {
                    "title": f"{kind} {key}",
                    "parent_id": f"id-{parent}" if parent else None,
                    "milestone_id": milestone,
                    "block_digest": lr.digest(lr.managed_block(description) or ""),
                },
            }
        )
        self.fx.remote["issues"].append(
            {
                "id": f"id-{key}",
                "identifier": key,
                "title": f"{kind} {key}",
                "description": description,
                "parent_id": f"id-{parent}" if parent else None,
                "milestone_id": milestone,
                "project_id": PROJECT,
                "status": "backlog",
            }
        )

    def test_tasks_follow_their_story_to_the_new_epic_milestone(self) -> None:
        self.add_item("task:story:1:2:t1", "task", "story:1:2", "ms-1")
        self.add_item("planning:prd", "planning", None, None)
        code, _ = self.fx.run("--check")
        self.assertEqual(code, 0)
        moved = (
            "### Story 1.2: Validate rows\n\nAs an analyst, I want invalid rows rejected.\n\n"
            "**Given** a bad row **When** imported **Then** it is reported\n\n"
        )
        self.edit(moved, "")
        self.edit(
            "### Story 2.1: Show summary",
            moved.replace("1.2", "2.2") + "### Story 2.1: Show summary",
        )
        _, plan = self.fx.run()
        self.assertEqual(actions(plan, "task:story:1:2:t1"), {"update-milestone"})
        self.assertEqual(actions(plan, "planning:prd"), set())

    def test_rewritten_block_awaits_baseline_and_accept_covers_unparsed_items(
        self,
    ) -> None:
        self.edit("I want a summary page.", "I want a summary page with charts.")
        local = {e.id: e for e in lr.parse_epics([self.fx.epics], self.fx.root)[0]}
        self.fx.issue("story:2:1")["description"] = block("story:2:1", local["2.1"])
        self.add_item("planning:prd", "planning", None, None)
        prd = next(i for i in self.fx.remote["issues"] if i["id"] == "id-planning:prd")
        prd["description"] = prd["description"].replace(
            "Acceptance summary.", "Accepted r2."
        )
        _, plan = self.fx.run()
        self.assertEqual(
            actions(plan, "story:2:1"), {"content-changed", "baseline-pending"}
        )
        self.assertEqual(actions(plan, "planning:prd"), {"restore-block"})
        _, result = self.fx.run("--write", command="baseline")
        self.assertIn("story:2:1", result["recorded"])
        self.assertIn("planning:prd", result["skipped"])
        self.fx.manifest = json.loads(self.fx.manifest_path.read_text())
        _, result = self.fx.run(
            "--write", "--accept", "planning:prd", command="baseline"
        )
        self.assertIn("planning:prd", result["recorded"])
        self.fx.manifest = json.loads(self.fx.manifest_path.read_text())
        code, plan = self.fx.run("--check")
        self.assertEqual(code, 0, plan["steps"])

    def test_legacy_manifest_upgrades_without_guessing(self) -> None:
        for item in self.fx.manifest["items"]:
            item.pop("synced")
        for issue in self.fx.remote["issues"]:
            marker = issue["description"].rsplit("\n", 1)[1]
            issue["description"] = f"Old summary\n{marker}"
        _, plan = self.fx.run()
        self.assertEqual(plan["new"], [])
        self.assertFalse(plan["needs_user"])
        self.assertEqual(actions(plan, "story:1:1"), {"no-baseline", "refresh-block"})
        for issue in self.fx.remote["issues"]:
            key = issue["id"].removeprefix("id-")
            local = next(m for m in plan["matched"] if m["key"] == key)
            entry = lr.Local(
                "story" if key.startswith("story") else "epic",
                local["id"],
                local["id"].split(".")[0],
                local["title"],
                local["path"],
                local["line"],
                local["digest"],
                False,
            )
            issue["description"] = block(key, entry)
        _, result = self.fx.run("--write", command="baseline")
        self.assertEqual(len(result["recorded"]), 5)
        self.fx.manifest = json.loads(self.fx.manifest_path.read_text())
        code, plan = self.fx.run("--check")
        self.assertEqual(code, 0, plan["steps"])

    def armoury_shape(self) -> None:
        """Rewrite the fixture in the shape real pre-helper manifests use."""
        milestones = {}
        for item in self.fx.manifest["items"]:
            item.pop("synced")
            kind, source = item["kind"], item["source"]
            label = "Epic" if kind == "epic" else "Story"
            item["title"] = f"{label} {source['id']}: {item['title']}"
            source["id"] = f"{kind}-{source['id']}"
            item["remote"] = {
                "id": item.pop("id"),
                "identifier": item.pop("identifier"),
            }
            epic = item["key"] if kind == "epic" else item["parent_key"]
            item["milestone_key"] = epic
            if kind == "epic":
                record = item.pop("milestone")
                number = epic.split(":")[1]
                milestones[epic] = {
                    "id": record["id"],
                    "marker": f"BMAD-ID: {BINDING}:milestone:{number}",
                }
        self.fx.manifest["milestones"] = milestones
        for milestone in self.fx.remote["milestones"]:
            number = milestone["id"].removeprefix("ms-")
            milestone["description"] = f"Goal\nBMAD-ID: {BINDING}:milestone:{number}"

    def test_pre_helper_manifest_shape_matches_without_identity_questions(
        self,
    ) -> None:
        self.armoury_shape()
        _, plan = self.fx.run("--check", remote=False)
        self.assertEqual(plan["new"], [])
        self.assertEqual(actions(plan), {"no-baseline"})
        _, plan = self.fx.run()
        self.assertFalse(
            plan["needs_user"], [s for s in plan["steps"] if s["needs_user"]]
        )
        self.assertNotIn("create-milestone", actions(plan))
        self.assertNotIn("adopt", actions(plan))
        # A moved story keeps its key and is written back in the existing shape.
        moved = (
            "### Story 1.2: Validate rows\n\nAs an analyst, I want invalid rows rejected.\n\n"
            "**Given** a bad row **When** imported **Then** it is reported\n\n"
        )
        self.edit(moved, "")
        self.edit(
            "### Story 2.1: Show summary",
            moved.replace("1.2", "2.2") + "### Story 2.1: Show summary",
        )
        _, plan = self.fx.run()
        self.assertEqual(plan["new"], [])
        self.assertIn("move", actions(plan, "story:1:2"))
        local = {e.id: e for e in lr.parse_epics([self.fx.epics], self.fx.root)[0]}
        for issue in self.fx.remote["issues"]:
            key = issue["id"].removeprefix("id-")
            match = next(m for m in plan["matched"] if m["key"] == key)
            issue["description"] = block(key, local[match["id"]])
            issue["title"] = match["desired_title"]
        self.fx.issue("story:1:2").update(parent_id="id-epic:2", milestone_id="ms-2")
        _, result = self.fx.run("--write", command="baseline")
        self.assertEqual(len(result["recorded"]), 5, result)
        saved = json.loads(self.fx.manifest_path.read_text())
        item = next(i for i in saved["items"] if i["key"] == "story:1:2")
        self.assertEqual(item["source"]["id"], "story-2.2")
        self.assertEqual(item["title"], "Story 2.2: Validate rows")
        self.assertEqual(item["milestone_key"], "epic:2")
        self.assertIn("remote", item)
        self.assertNotIn("id", item)
        self.assertNotIn("milestone", saved["items"][0])
        self.assertEqual(saved["milestones"]["epic:1"]["name"], "Epic 1: Import data")
        self.fx.manifest = saved
        code, plan = self.fx.run("--check")
        self.assertEqual(code, 0, plan["steps"])

    def test_active_manifest_must_stay_inside_linear_directory(self) -> None:
        (self.fx.root / "_bmad/linear/active.json").write_text(
            '{"manifest": "../../outside.json"}'
        )
        code, result = self.fx.run()
        self.assertEqual(code, 1)
        self.assertIn("outside", result["error"])


if __name__ == "__main__":
    unittest.main()
