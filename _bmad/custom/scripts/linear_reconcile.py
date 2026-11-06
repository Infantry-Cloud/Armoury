#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""Deterministic drift plan for a BMAD project's Linear binding.

The agent does the Linear MCP writes; this script only computes what must change.
It compares three states:

* local   - the authoritative BMAD breakdown (epics.md, optional sprint-status.yaml),
* manifest - `_bmad/linear/projects/<slug>.json`: stable keys, remote IDs and the
  `synced` baseline recorded at the last confirmed sync,
* remote  - an optional JSON snapshot of the Linear Project the agent assembled
  from MCP list/get calls (see `linear-workflow.md`, Reconcile).

`plan` is read-only and prints a JSON plan. `plan --check` exits 3 when anything
needs reconciling. `baseline --write` records the synced baseline for items that a
fresh remote snapshot proves are in sync; it never touches anything else.

Identity rules: manifest keys are opaque and never re-derived from numbering.
Renumbered, moved or retitled entries are matched to their existing key; anything
ambiguous is reported for user confirmation instead of guessed.
"""

from __future__ import annotations

import argparse
import copy
import difflib
import hashlib
import json
import os
import re
import sys
import tempfile
import unicodedata
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Same heading grammar as BMAD v6.12.2 bmad-sprint-planning/scripts/sprint_plan.py.
EPIC_RE = re.compile(r"^#{1,3}\s*Epic\s+(\d+)\s*:?\s*(.*?)\s*#*\s*$", re.IGNORECASE)
STORY_RE = re.compile(
    r"^#{2,4}\s*Story\s+(\d+)\.(\d+[a-z]?)\s*:?\s*(.*?)\s*#*\s*$", re.IGNORECASE
)
HEADING_RE = re.compile(r"^(#{1,6})\s")
FENCE_RE = re.compile(r"^\s{0,3}(?:```|~~~)")
SPRINT_STORY_RE = re.compile(r"^(\d+)-(\d+[a-z]?)-")
SPRINT_EPIC_RE = re.compile(r"^epic-(\d+)$")
MARKER_RE = re.compile(r"BMAD-ID:\s*([0-9A-Za-z-]+):(\S+)")
SOURCE_LINE_RE = re.compile(r"BMAD-SOURCE:\s*(\S+)\s+(sha256:[0-9a-f]+)")
# Linear stores markdown-escaped text (`_bmad-output` comes back as `\_bmad-output`).
MARKDOWN_ESCAPE_RE = re.compile(r"\\([\\`*_{}\[\]()#+\-.!|~<>])")
BLOCK_START = "BMAD-managed"

LOCAL_RANK = {
    "backlog": 0,
    "ready-for-dev": 0,
    "in-progress": 1,
    "review": 2,
    "done": 3,
}
REMOTE_RANK = {"backlog": 0, "todo": 0, "in-progress": 1, "in-review": 2, "done": 3}
PARSED_KINDS = ("epic", "story")
SIMILAR = 0.6
EXIT_DRIFT = 3


class ReconcileError(Exception):
    pass


# --------------------------------------------------------------------------- text


def _clean(text: str) -> str:
    """Normalise markdown so formatting-only round trips do not look like edits."""
    lines = []
    for line in unicodedata.normalize("NFKC", text).splitlines():
        line = re.sub(r"^\s*(?:[-+*]|\d+[.)])\s+", "", line)
        line = re.sub(r"[\\*_`>#~|]", " ", line)
        lines.append(line)
    return " ".join(" ".join(lines).split())


def digest(text: str) -> str:
    return "sha256:" + hashlib.sha256(_clean(text).encode("utf-8")).hexdigest()[:16]


def norm_title(title: str) -> str:
    folded = unicodedata.normalize("NFKC", title).lower()
    return " ".join(re.sub(r"[^\w\s]", " ", folded).split())


def similarity(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, norm_title(a), norm_title(b)).ratio()


# -------------------------------------------------------------------------- local


@dataclass
class Local:
    kind: str
    id: str  # "2" for an epic, "2.3" for a story
    epic: str
    title: str
    path: str
    line: int
    digest: str
    empty: bool
    status: str | None = None

    @property
    def source_line(self) -> str:
        return f"BMAD-SOURCE: {self.path}#{self.id} {self.digest}"

    @property
    def desired_title(self) -> str:
        label = "Epic" if self.kind == "epic" else "Story"
        return f"{label} {self.id}: {self.title}"

    def view(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "path": self.path,
            "line": self.line,
            "digest": self.digest,
            "status": self.status,
        }


@dataclass
class Warning_:
    code: str
    message: str
    blocking: bool = False

    def view(self) -> dict[str, Any]:
        return {"code": self.code, "message": self.message, "blocking": self.blocking}


def _relative(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def epic_files(paths: list[Path]) -> list[Path]:
    files: list[Path] = []
    for path in paths:
        if path.is_dir():
            files.extend(sorted(p for p in path.rglob("*.md") if p.is_file()))
        elif path.is_file():
            files.append(path)
        else:
            raise ReconcileError(f"epic source not found: {path}")
    return files


def parse_epics(paths: list[Path], root: Path) -> tuple[list[Local], list[Warning_]]:
    sections: list[dict[str, Any]] = []
    warnings: list[Warning_] = []
    for path in epic_files(paths):
        relative = _relative(path, root)
        current: dict[str, Any] | None = None
        in_fence = False
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if FENCE_RE.match(line):
                in_fence = not in_fence
            elif not in_fence:
                heading = HEADING_RE.match(line)
                epic, story = EPIC_RE.match(line), STORY_RE.match(line)
                if epic or story:
                    current = {
                        "kind": "epic" if epic else "story",
                        "match": epic or story,
                        "level": len(heading.group(1)) if heading else 1,
                        "path": relative,
                        "line": number,
                        "body": [],
                    }
                    sections.append(current)
                    continue
                if heading and current and len(heading.group(1)) <= current["level"]:
                    current = None
            if current is not None:
                current["body"].append(line)

    epics: dict[str, list[dict[str, Any]]] = {}
    stories: list[Local] = []
    seen: dict[str, Local] = {}
    for section in sections:
        body = "\n".join(section["body"]).strip()
        if section["kind"] == "epic":
            epics.setdefault(section["match"].group(1), []).append(
                {**section, "text": body}
            )
            continue
        epic_id, story_no, title = section["match"].groups()
        story_id = f"{epic_id}.{story_no}"
        entry = Local(
            "story",
            story_id,
            epic_id,
            title.strip(),
            section["path"],
            section["line"],
            digest(body),
            not body,
        )
        if story_id in seen:
            warnings.append(
                Warning_(
                    "duplicate-story",
                    f"Story {story_id} appears at {seen[story_id].path}:{seen[story_id].line}"
                    f" and {entry.path}:{entry.line}; fix the breakdown before reconciling",
                    blocking=True,
                )
            )
            continue
        seen[story_id] = entry
        stories.append(entry)

    result: list[Local] = []
    for epic_id in sorted(epics, key=int):
        found = epics[epic_id]
        # The Epic List entry and the `## Epic N` section share a number: the last
        # heading names it; the last non-empty body is its goal.
        last = found[-1]
        goal = next((f["text"] for f in reversed(found) if f["text"]), "")
        result.append(
            Local(
                "epic",
                epic_id,
                epic_id,
                last["match"].group(2).strip(),
                last["path"],
                last["line"],
                digest(goal),
                not goal,
            )
        )
        result.extend(s for s in stories if s.epic == epic_id)
    for story in stories:
        if story.epic not in epics:
            warnings.append(
                Warning_(
                    "story-without-epic",
                    f"Story {story.id} at {story.path}:{story.line} has no Epic {story.epic} heading",
                    blocking=True,
                )
            )
    return result, warnings


def parse_sprint_status(path: Path) -> dict[str, str]:
    """Read development_status without a YAML dependency (flat key: value map)."""
    statuses: dict[str, str] = {}
    inside = False
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        if not raw[:1].isspace():
            inside = line.strip() == "development_status:"
            continue
        if inside and ":" in line:
            key, value = line.split(":", 1)
            statuses[key.strip().strip("'\"")] = value.strip().strip("'\"")
    return statuses


def apply_statuses(
    entries: list[Local], statuses: dict[str, str], warnings: list[Warning_]
) -> None:
    by_story: dict[str, list[str]] = {}
    for key in statuses:
        match = SPRINT_STORY_RE.match(key)
        if match:
            by_story.setdefault(f"{match.group(1)}.{match.group(2)}", []).append(key)
    known = {e.id for e in entries if e.kind == "story"}
    for story_id, keys in sorted(by_story.items()):
        if story_id not in known:
            warnings.append(
                Warning_(
                    "sprint-orphan",
                    f"sprint-status has {', '.join(keys)} but epics.md has no Story {story_id};"
                    " run sprint planning to reconcile local tracking",
                )
            )
        elif len(keys) > 1:
            warnings.append(
                Warning_(
                    "sprint-duplicate",
                    f"sprint-status has several keys for Story {story_id}: {keys}",
                )
            )
    for entry in entries:
        if entry.kind == "epic":
            entry.status = statuses.get(f"epic-{entry.id}")
        elif by_story.get(entry.id):
            entry.status = statuses[by_story[entry.id][0]]


# ----------------------------------------------------------------------- manifest


def read_json(path: Path, what: str) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ReconcileError(f"cannot read {what} {path}: {error}") from error


def resolve_manifest(root: Path, manifest: Path | None) -> Path:
    if manifest is not None:
        return manifest
    linear = (root / "_bmad/linear").resolve()
    active = linear / "active.json"
    if not active.is_file():
        raise ReconcileError(
            "no --manifest given and _bmad/linear/active.json is missing"
        )
    pointer = read_json(active, "active manifest pointer")
    if not isinstance(pointer, dict) or not isinstance(pointer.get("manifest"), str):
        raise ReconcileError('active.json must be {"manifest": "projects/<slug>.json"}')
    target = (linear / pointer["manifest"]).resolve()
    if linear not in target.parents:
        raise ReconcileError("active.json points outside _bmad/linear/")
    return target


def load_manifest(path: Path) -> dict[str, Any]:
    data = read_json(path, "manifest")
    if not isinstance(data, dict):
        raise ReconcileError("manifest must be a JSON object")
    if data.get("schema_version") != 1 or not data.get("binding_id"):
        raise ReconcileError("manifest needs schema_version 1 and a binding_id")
    keys = [item.get("key") for item in data.get("items", [])]
    if len(keys) != len(set(keys)) or None in keys:
        raise ReconcileError("manifest items need unique, non-empty keys")
    return data


def save_manifest(path: Path, data: dict[str, Any]) -> None:
    handle, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as stream:
            json.dump(data, stream, indent=2, ensure_ascii=False)
            stream.write("\n")
        os.replace(temporary, path)
    except BaseException:
        Path(temporary).unlink(missing_ok=True)
        raise


def lifecycle(item: dict[str, Any]) -> str:
    return item.get("lifecycle") or "active"


# Manifests written before this helper existed use other, equally valid shapes:
# `source.id` as `epic-1`/`story-1.1`, titles with their `Epic 1:` prefix, remote IDs
# under `remote`, and epic milestones in a top-level `milestones` map. Read them all
# and write back in the shape each item already uses; never migrate a manifest.
SOURCE_PREFIX_RE = re.compile(r"^(?:epic|story)-", re.IGNORECASE)
TITLE_PREFIX_RE = re.compile(
    r"^\s*(?:Epic\s+\d+|Story\s+\d+\.\d+[a-z]?)\s*:\s*", re.IGNORECASE
)


def source_id(item: dict[str, Any]) -> str | None:
    raw = (item.get("source") or {}).get("id")
    if raw and item.get("kind") in PARSED_KINDS:
        return SOURCE_PREFIX_RE.sub("", str(raw))
    return raw


def bare_title(title: str | None) -> str | None:
    return TITLE_PREFIX_RE.sub("", title) if title else title


def remote_id(item: dict[str, Any]) -> str | None:
    return (item.get("remote") or {}).get("id") or item.get("id")


def milestone_ref(item: dict[str, Any], manifest: dict[str, Any]) -> dict[str, Any]:
    """The epic's milestone record, wherever this manifest keeps it (live reference)."""
    if isinstance(item.get("milestone"), dict):
        return item["milestone"]
    shared = manifest.get("milestones") or {}
    found = shared.get(item.get("milestone_key") or item["key"])
    return found if isinstance(found, dict) else {}


def stored_source(item: dict[str, Any], local: Local) -> dict[str, Any]:
    previous = item.get("source") or {}
    raw = str(previous.get("id") or "")
    prefix = SOURCE_PREFIX_RE.match(raw)
    identifier = f"{prefix.group(0)}{local.id}" if prefix else local.id
    return {**previous, "path": local.path, "id": identifier}


# ----------------------------------------------------------------------- matching


@dataclass
class Match:
    key: str
    local: Local
    how: str


def _anchor(item: dict[str, Any]) -> tuple[str | None, str | None, str | None]:
    synced = item.get("synced") or {}
    title = synced.get("source_title") or bare_title(item.get("title"))
    return source_id(item), title, synced.get("source_digest")


def match_kind(
    locals_: list[Local], items: list[dict[str, Any]]
) -> tuple[list[Match], list[Local], list[dict[str, Any]]]:
    """Pair local entries with manifest items; never guess when a pairing is ambiguous."""
    remaining_local = list(locals_)
    remaining_items = [i for i in items if lifecycle(i) == "active"]
    matches: list[Match] = []

    def take(local: Local, item: dict[str, Any], how: str) -> None:
        matches.append(Match(item["key"], local, how))
        remaining_local.remove(local)
        remaining_items.remove(item)

    def unique_pass(local_value, item_value, how: str) -> None:
        for local in list(remaining_local):
            value = local_value(local)
            if value is None:
                continue
            on_items = [i for i in remaining_items if item_value(i) == value]
            on_local = [lo for lo in remaining_local if local_value(lo) == value]
            if len(on_items) == 1 and len(on_local) == 1:
                take(local, on_items[0], how)

    def title_of(item):
        title = _anchor(item)[1]
        return norm_title(title) if title else None

    def digest_of(item):
        return _anchor(item)[2]

    # 1. Same heading title and same body, wherever it now lives.
    unique_pass(
        lambda lo: None if lo.empty else (norm_title(lo.title), lo.digest),
        lambda i: (title_of(i), digest_of(i)),
        "exact",
    )
    # 2. Same source ID, and either the title, the body or a user confirmation agrees.
    for local in list(remaining_local):
        same = [i for i in remaining_items if _anchor(i)[0] == local.id]
        if len(same) != 1:
            continue
        item = same[0]
        confirmed = (item.get("source") or {}).get("confirmed") is True
        if (
            title_of(item) == norm_title(local.title)
            or (not local.empty and digest_of(item) == local.digest)
            or confirmed
        ):
            take(local, item, "confirmed" if confirmed else "source-id")
    # 3. Same title only (renumbered or moved, body edited).
    unique_pass(lambda lo: norm_title(lo.title), title_of, "title")
    # 4. Same body only (retitled, maybe renumbered).
    unique_pass(lambda lo: None if lo.empty else lo.digest, digest_of, "digest")
    return matches, remaining_local, remaining_items


def candidates(local: Local, items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    found = []
    for item in items:
        source_id, title, _ = _anchor(item)
        score = similarity(local.title, title or "")
        reasons = []
        if source_id == local.id:
            reasons.append("same source ID")
        if score >= SIMILAR:
            reasons.append(f"similar title ({score:.2f})")
        if reasons:
            found.append(
                {
                    "key": item["key"],
                    "lifecycle": lifecycle(item),
                    "source_id": source_id,
                    "title": title,
                    "score": round(score, 2),
                    "why": reasons,
                }
            )
    return sorted(found, key=lambda c: (-len(c["why"]), -c["score"], c["key"]))


def propose_key(local: Local, epic_key: str | None, taken: set[str]) -> str:
    if local.kind == "epic":
        base = f"epic:{local.id}"
    else:
        epic_part = (epic_key or f"epic:{local.epic}").split(":", 1)[1]
        # Follow the manifest's convention: `story:1:2` or `story:1:1.2`.
        full = any(
            k.startswith("story:") and "." in k.rsplit(":", 1)[-1] for k in taken
        )
        story_part = local.id if full else local.id.split(".", 1)[1]
        base = f"story:{epic_part}:{story_part}"
    key, counter = base, 2
    while key in taken:
        key, counter = f"{base}~{counter}", counter + 1
    taken.add(key)
    return key


# ------------------------------------------------------------------------- remote


def source_line(block: str) -> str | None:
    """The block's BMAD-SOURCE line with Linear's markdown escapes removed."""
    found = SOURCE_LINE_RE.search(MARKDOWN_ESCAPE_RE.sub(r"\1", block))
    return found.group(0) if found else None


def managed_block(description: str | None) -> str | None:
    if not description:
        return None
    lines = description.splitlines()
    start = next((n for n, line in enumerate(lines) if BLOCK_START in line), None)
    if start is None:
        return None
    end = next(
        (n for n in range(start, len(lines)) if MARKER_RE.search(lines[n])), None
    )
    return None if end is None else "\n".join(lines[start : end + 1])


def markers(description: str | None, binding: str) -> tuple[list[str], list[str]]:
    ours, foreign = [], []
    for found_binding, key in MARKER_RE.findall(description or ""):
        (ours if found_binding == binding else foreign).append(key)
    return ours, foreign


def three_way(
    desired: Any, remote: Any, synced: dict[str, Any], name: str
) -> str | None:
    if remote == desired:
        return None
    if name not in synced:
        return "update"
    if remote == synced[name]:
        return "update"
    if desired == synced[name]:
        return "restore"
    return "conflict"


# --------------------------------------------------------------------------- plan


@dataclass
class Planner:
    manifest: dict[str, Any]
    local: list[Local]
    warnings: list[Warning_]
    remote: dict[str, Any] | None
    items: dict[str, dict[str, Any]] = field(default_factory=dict)
    reports: dict[str, dict[str, Any]] = field(default_factory=dict)
    steps: list[dict[str, Any]] = field(default_factory=list)
    matched: dict[str, Local] = field(default_factory=dict)
    how: dict[str, str] = field(default_factory=dict)
    desired_parent: dict[str, str | None] = field(default_factory=dict)

    PHASES = (
        "identity",
        "milestones",
        "epics",
        "stories",
        "other",
        "relations",
        "statuses",
        "notes",
    )

    def step(
        self,
        phase: str,
        key: str,
        action: str,
        detail: str = "",
        needs_user: bool = False,
        **extra: Any,
    ) -> None:
        self.steps.append(
            {
                "phase": phase,
                "key": key,
                "action": action,
                "detail": detail,
                "needs_user": needs_user,
                **extra,
            }
        )
        report = self.reports.setdefault(key, {"key": key, "classes": []})
        report["classes"].append(action)

    def run(self) -> dict[str, Any]:
        self.items = {i["key"]: i for i in self.manifest.get("items", [])}
        new_entries = self._match_local()
        if self.remote is not None:
            self._check_remote()
        self._check_dependencies()
        order = {phase: n for n, phase in enumerate(self.PHASES)}
        self.steps.sort(key=lambda s: order[s["phase"]])
        summary: dict[str, int] = {}
        for step in self.steps:
            summary[step["action"]] = summary.get(step["action"], 0) + 1
        blocking = any(w.blocking for w in self.warnings)
        return {
            "ok": not blocking,
            "binding_id": self.manifest["binding_id"],
            "remote_checked": self.remote is not None,
            "drift": bool(self.steps) or blocking,
            "needs_user": any(s["needs_user"] for s in self.steps) or blocking,
            "summary": summary,
            "steps": self.steps,
            "new": new_entries,
            "matched": [
                {
                    "key": key,
                    "how": self.how[key],
                    **local.view(),
                    "desired_title": local.desired_title,
                    "desired_parent_key": self.desired_parent.get(key),
                }
                for key, local in self.matched.items()
            ],
            "warnings": [w.view() for w in self.warnings],
        }

    # local ---------------------------------------------------------------

    def _match_local(self) -> list[dict[str, Any]]:
        taken = set(self.items)
        new_entries: list[dict[str, Any]] = []
        epic_key_by_id: dict[str, str] = {}
        for kind in PARSED_KINDS:
            locals_ = [e for e in self.local if e.kind == kind]
            pool = [i for i in self.items.values() if i.get("kind") == kind]
            matches, unmatched_local, unmatched_items = match_kind(locals_, pool)
            for match in matches:
                self.matched[match.key] = match.local
                self.how[match.key] = match.how
                if kind == "epic":
                    epic_key_by_id[match.local.id] = match.key
            candidate_pool = unmatched_items + [
                i for i in pool if lifecycle(i) != "active"
            ]
            phase = "epics" if kind == "epic" else "stories"
            for local in unmatched_local:
                parent = epic_key_by_id.get(local.epic) if kind == "story" else None
                key = propose_key(local, parent, taken)
                if kind == "epic":
                    epic_key_by_id[local.id] = key
                options = candidates(local, candidate_pool)
                entry = {
                    "proposed_key": key,
                    "kind": kind,
                    "parent_key": parent,
                    **local.view(),
                    "desired_title": local.desired_title,
                    "candidates": options,
                }
                new_entries.append(entry)
                self.desired_parent[key] = parent
                if options:
                    self.step(
                        "identity",
                        key,
                        "confirm-identity",
                        f"{local.desired_title} may be an existing item renumbered, "
                        "split or merged; confirm the mapping or approve it as new",
                        needs_user=True,
                        candidates=options,
                    )
                else:
                    self.step(
                        phase,
                        key,
                        "create",
                        f"publish approved {kind} {local.desired_title}",
                    )
            for item in unmatched_items:
                self.step(
                    "identity",
                    item["key"],
                    "missing-locally",
                    f"{(item.get('source') or {}).get('id')} {item.get('title')!r} is no "
                    "longer in the breakdown: confirm a mapping, merge, split, or "
                    "approve cancellation (never delete)",
                    needs_user=True,
                )
            for match in matches:
                self._compare_local(match, epic_key_by_id, phase)
        return new_entries

    def _compare_local(
        self, match: Match, epic_keys: dict[str, str], phase: str
    ) -> None:
        item, local = self.items[match.key], match.local
        source_id, title, source_digest = _anchor(item)
        if match.how in ("title", "digest", "confirmed") or source_id != local.id:
            self.step(
                "identity",
                match.key,
                "remap-source",
                f"source {source_id} -> {local.id} (matched by {match.how})",
                source_id=local.id,
                source_path=local.path,
            )
        if local.kind == "story":
            parent = epic_keys.get(local.epic)
            self.desired_parent[match.key] = parent
            if parent != item.get("parent_key"):
                self.step(
                    phase,
                    match.key,
                    "move",
                    f"parent {item.get('parent_key')} -> {parent}; move the epic "
                    "milestone too, and on every task under it",
                    parent_key=parent,
                )
        else:
            self.desired_parent[match.key] = None
        if title is not None and norm_title(title) != norm_title(local.title):
            self.step(phase, match.key, "retitle", f"{title!r} -> {local.title!r}")
        if not (item.get("synced") or {}).get("source_digest"):
            self.step(
                phase,
                match.key,
                "no-baseline",
                "no synced baseline yet: verify remote content, then run baseline",
            )
        elif source_digest != local.digest:
            self.step(
                phase,
                match.key,
                "content-changed",
                "local body changed since the last sync: refresh the managed block",
            )

    def _check_dependencies(self) -> None:
        for key, item in self.items.items():
            if lifecycle(item) != "active":
                continue
            for after in item.get("after") or []:
                target = self.items.get(after)
                if target is None or lifecycle(target) != "active":
                    self.step(
                        "relations",
                        key,
                        "dangling-dependency",
                        f"after {after} which is missing or not active",
                        needs_user=True,
                    )

    # remote --------------------------------------------------------------

    def _desired_milestone(self, key: str | None) -> tuple[bool, str | None]:
        """Return (has_epic_ancestor, epic milestone id or None if unpublished)."""
        seen = set()
        while key and key not in seen:
            seen.add(key)
            item = self.items.get(key)
            if item is None:
                return False, None
            if item.get("kind") == "epic":
                return True, milestone_ref(item, self.manifest).get("id")
            if item.get("kind") == "planning":
                return False, None
            key = self.desired_parent.get(key, item.get("parent_key"))
        return False, None

    def _remote_id(self, key: str | None) -> str | None:
        return remote_id(self.items.get(key) or {}) if key else None

    def _check_remote(self) -> None:
        if self.remote is None:
            return
        binding = self.manifest["binding_id"]
        project_id = (self.manifest.get("project") or {}).get("id")
        issues = {i["id"]: i for i in self.remote.get("issues", [])}
        by_marker: dict[str, list[dict[str, Any]]] = {}
        for issue in issues.values():
            ours, foreign = markers(issue.get("description"), binding)
            for key in ours:
                by_marker.setdefault(key, []).append(issue)
            if foreign:
                self.warnings.append(
                    Warning_(
                        "foreign-marker",
                        f"{issue.get('identifier', issue['id'])} carries another binding's marker",
                    )
                )
            if not ours and not foreign:
                self.step(
                    "identity",
                    issue.get("identifier", issue["id"]),
                    "unmanaged",
                    "issue in the Project without a BMAD marker: report only",
                )
        for key, found in by_marker.items():
            if key not in self.items:
                self.step(
                    "identity",
                    key,
                    "remote-unknown",
                    f"{[i.get('identifier', i['id']) for i in found]} carry a marker for "
                    "a key not in the manifest: adopt or ignore, never import as intent",
                    needs_user=True,
                )
        for key, item in self.items.items():
            self._check_item(key, item, issues, by_marker.get(key, []), project_id)
            if item.get("kind") == "epic":
                self._check_milestone(key, item, binding)

    def _check_item(
        self,
        key: str,
        item: dict[str, Any],
        issues: dict[str, Any],
        marked: list[dict[str, Any]],
        project_id: str | None,
    ) -> None:
        phase = {"epic": "epics", "story": "stories"}.get(
            str(item.get("kind")), "other"
        )
        saved_id = remote_id(item)
        if len(marked) > 1:
            self.step(
                "identity",
                key,
                "duplicate-remote",
                f"marker on {[i.get('identifier', i['id']) for i in marked]}",
                needs_user=True,
            )
            return
        if not saved_id:
            if marked:
                self.step(
                    "identity",
                    key,
                    "adopt",
                    f"record existing {marked[0].get('identifier', marked[0]['id'])}",
                    remote_id=marked[0]["id"],
                )
            return
        issue = issues.get(saved_id)
        if issue is None:
            detail = "saved remote ID is not in the Project snapshot"
            if marked:
                detail += (
                    f"; marker found on {marked[0].get('identifier', marked[0]['id'])}"
                )
            self.step(
                "identity",
                key,
                "remote-missing",
                detail + ": deleted, archived or moved? Resolve before writing",
                needs_user=True,
            )
            return
        if marked and marked[0]["id"] != saved_id:
            self.step(
                "identity",
                key,
                "identity-conflict",
                "saved ID and marker point to different issues",
                needs_user=True,
            )
            return
        if not marked:
            self.step(phase, key, "restore-marker", "issue lost its BMAD-ID marker")
        state = issue.get("status")
        active = lifecycle(item) == "active"
        if not active:
            if state != "canceled":
                self.step(
                    "statuses",
                    key,
                    "cancel",
                    f"{lifecycle(item)} locally (already approved); set Canceled, keep history",
                )
            return
        if state == "canceled" or issue.get("archived"):
            self.step(
                "statuses",
                key,
                "remote-canceled",
                "canceled/archived in Linear but active locally",
                needs_user=True,
            )
            return
        if project_id and issue.get("project_id") != project_id:
            self.step(phase, key, "set-project", "issue is outside the bound Project")
        local = self.matched.get(key)
        if local is None and item.get("kind") in PARSED_KINDS:
            return  # identity unresolved (missing-locally): compare fields after the decision
        synced = item.get("synced") or {}
        desired_title = local.desired_title if local else item.get("title")
        fields = [("title", desired_title, issue.get("title"))]
        parent_key = self.desired_parent.get(key, item.get("parent_key"))
        parent_id = self._remote_id(parent_key)
        if parent_key and not parent_id:
            self.step(
                phase, key, "blocked-on-parent", f"{parent_key} is not published yet"
            )
        else:
            fields.append(("parent_id", parent_id, issue.get("parent_id")))
        has_epic, milestone_id = self._desired_milestone(key)
        if has_epic and not milestone_id:
            self.step(
                "milestones",
                key,
                "milestone-pending",
                "epic milestone not published yet",
            )
        elif item.get("kind") not in ("planning",) and (
            has_epic or item.get("kind") != "epic"
        ):
            fields.append(
                (
                    "milestone_id",
                    milestone_id if has_epic else None,
                    issue.get("milestone_id"),
                )
            )
        for name, desired, remote in fields:
            verdict = three_way(desired, remote, synced, name)
            if verdict:
                self.step(
                    phase,
                    key,
                    f"{verdict}-{name.removesuffix('_id')}",
                    f"remote {remote!r}, desired {desired!r}",
                    needs_user=verdict == "conflict",
                    desired=desired,
                )
        self._check_block(phase, key, issue, synced, local)
        self._check_status(key, local, state)

    def _check_block(
        self,
        phase: str,
        key: str,
        issue: dict[str, Any],
        synced: dict[str, Any],
        local: Local | None,
    ) -> None:
        line = local.source_line if local else None
        block = managed_block(issue.get("description"))
        if block is None:
            self.step(
                phase,
                key,
                "refresh-block",
                "managed description block is missing",
                source_line=line,
            )
            return
        current = local is not None and source_line(block) == line
        local_changed = local is not None and not current
        remote_edited = (
            "block_digest" in synced and digest(block) != synced["block_digest"]
        )
        # A current BMAD-SOURCE line that differs from the synced one can only have
        # been written by this workflow: the block awaits its baseline, not a restore.
        rewritten = (
            current
            and local is not None
            and (synced.get("source_id"), synced.get("source_digest"))
            != (local.id, local.digest)
        )
        if remote_edited and rewritten:
            self.step(
                phase,
                key,
                "baseline-pending",
                "block rewritten for the current source: run baseline",
            )
        elif remote_edited and local_changed:
            self.step(
                phase,
                key,
                "conflict-block",
                "both BMAD and Linear changed the managed block",
                needs_user=True,
            )
        elif remote_edited:
            self.step(phase, key, "restore-block", "managed block edited in Linear")
        elif local_changed:
            self.step(
                phase, key, "refresh-block", "managed block is stale", source_line=line
            )

    def _check_status(self, key: str, local: Local | None, state: str | None) -> None:
        if local is None or local.status not in LOCAL_RANK or state not in REMOTE_RANK:
            return
        mine, theirs = LOCAL_RANK[local.status], REMOTE_RANK[state]
        if theirs > mine:
            self.step(
                "statuses",
                key,
                "status-ahead",
                f"Linear {state} is ahead of local {local.status}: never import; "
                "discuss, and only correct with user approval",
                needs_user=True,
            )
        elif mine > theirs:
            self.step(
                "statuses",
                key,
                "status-behind",
                f"local {local.status} is ahead of Linear {state}: advance only after "
                "the workflow's evidence gate passes, with its activity note",
            )

    def _check_milestone(self, key: str, item: dict[str, Any], binding: str) -> None:
        milestone = milestone_ref(item, self.manifest)
        local = self.matched.get(key)
        desired = local.desired_title if local else milestone.get("name")
        accepted = {f"{key}:milestone"}
        accepted.update(k for _, k in MARKER_RE.findall(milestone.get("marker") or ""))
        found = [
            m
            for m in self.remote.get("milestones", [])  # type: ignore[union-attr]
            if accepted & set(markers(m.get("description"), binding)[0])
        ]
        if lifecycle(item) != "active":
            return
        if len(found) > 1:
            self.step(
                "identity",
                key,
                "duplicate-milestone",
                "several milestones carry the marker",
                needs_user=True,
            )
            return
        if not milestone.get("id"):
            if found:
                self.step(
                    "identity",
                    key,
                    "adopt-milestone",
                    f"record {found[0]['id']}",
                    remote_id=found[0]["id"],
                )
            else:
                self.step("milestones", key, "create-milestone", f"create {desired!r}")
            return
        remote = next(
            (
                m
                for m in self.remote.get("milestones", [])  # type: ignore[union-attr]
                if m.get("id") == milestone["id"]
            ),
            None,
        )
        if remote is None:
            self.step(
                "identity",
                key,
                "milestone-missing",
                "saved milestone is gone from the Project",
                needs_user=True,
            )
            return
        synced = {
            k.removeprefix("milestone_"): v
            for k, v in (item.get("synced") or {}).items()
            if k.startswith("milestone_")
        }
        verdict = three_way(desired, remote.get("name"), synced, "name")
        if verdict:
            self.step(
                "milestones",
                key,
                f"{verdict}-milestone-name",
                f"remote {remote.get('name')!r}, desired {desired!r} (same milestone; "
                "renaming for a renumbered epic is not reuse)",
                needs_user=verdict == "conflict",
                desired=desired,
            )


# ----------------------------------------------------------------------- baseline


LOCAL_ONLY = (
    "unmanaged",
    "remap-source",
    "no-baseline",
    "content-changed",
    "retitle",
    "move",
    "baseline-pending",
)


def baseline(
    planner: Planner,
    plan: dict[str, Any],
    manifest: dict[str, Any],
    accept: frozenset[str] | set[str] = frozenset(),
) -> dict[str, Any]:
    """Record synced baselines only for items the snapshot proves are in sync.

    `accept` names items whose managed block this session just rewrote but which
    have no parsed source to prove it (planning steps, tasks).
    """
    if planner.remote is None:
        raise ReconcileError("baseline needs --remote: a fresh snapshot after applying")
    open_keys = {
        s["key"]
        for s in plan["steps"]
        if s["action"] not in LOCAL_ONLY
        and not (s["action"] == "restore-block" and s["key"] in accept)
    }
    issues = {i["id"]: i for i in planner.remote.get("issues", [])}
    milestones = {m["id"]: m for m in planner.remote.get("milestones", [])}
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    recorded, skipped = [], []
    for item in manifest.get("items", []):
        key = item["key"]
        issue = issues.get(remote_id(item) or "")
        block = managed_block(issue.get("description")) if issue else None
        if (
            key in open_keys
            or issue is None
            or block is None
            or lifecycle(item) != "active"
        ):
            skipped.append(key)
            continue
        local = planner.matched.get(key)
        if local is not None and source_line(block) != local.source_line:
            skipped.append(key)
            continue
        previous = copy.deepcopy(item.get("source") or {})
        synced = {
            "title": issue.get("title"),
            "parent_id": issue.get("parent_id"),
            "milestone_id": issue.get("milestone_id"),
            "block_digest": digest(block),
            "at": now,
        }
        if local is not None:
            synced.update(
                source_id=local.id, source_title=local.title, source_digest=local.digest
            )
            item["source"] = stored_source(item, local)
            prefixed = bare_title(item.get("title")) != item.get("title")
            item["title"] = local.desired_title if prefixed else local.title
            item["parent_key"] = planner.desired_parent.get(key, item.get("parent_key"))
            if local.kind == "story" and "milestone_key" in item:
                item["milestone_key"] = item["parent_key"]
            if previous.get("id") and previous.get("id") != item["source"]["id"]:
                item.setdefault("source_history", []).append(
                    {"id": previous["id"], "path": previous.get("path"), "until": now}
                )
        record = milestone_ref(item, manifest) if item.get("kind") == "epic" else {}
        milestone = milestones.get(record.get("id") or "")
        if milestone is not None:
            synced["milestone_name"] = milestone.get("name")
            record["name"] = milestone.get("name")
        item["synced"] = synced
        recorded.append(key)
    return {"recorded": recorded, "skipped": skipped}


# ---------------------------------------------------------------------------- cli


def build_planner(args: argparse.Namespace) -> tuple[Planner, Path, dict[str, Any]]:
    root = args.root.resolve()
    manifest_path = resolve_manifest(root, args.manifest)
    manifest = load_manifest(manifest_path)
    local, warnings = parse_epics(args.epics, root)
    if args.sprint_status is not None:
        apply_statuses(local, parse_sprint_status(args.sprint_status), warnings)
    remote = read_json(args.remote, "remote snapshot") if args.remote else None
    if remote is not None and not isinstance(remote, dict):
        raise ReconcileError("remote snapshot must be a JSON object")
    return Planner(manifest, local, warnings, remote), manifest_path, manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n", 1)[0])
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("plan", "baseline"):
        command = sub.add_parser(name)
        command.add_argument("--root", type=Path, default=Path.cwd())
        command.add_argument("--manifest", type=Path)
        command.add_argument(
            "--epics",
            type=Path,
            nargs="+",
            required=True,
            help="epics.md file(s) or a sharded epics directory",
        )
        command.add_argument("--sprint-status", type=Path)
        command.add_argument(
            "--remote",
            type=Path,
            help="JSON snapshot of the Linear Project (see linear-workflow.md)",
        )
    sub.choices["plan"].add_argument(
        "--check",
        action="store_true",
        help=f"exit {EXIT_DRIFT} when anything needs reconciling",
    )
    sub.choices["baseline"].add_argument("--write", action="store_true")
    sub.choices["baseline"].add_argument(
        "--accept",
        action="append",
        default=[],
        metavar="KEY",
        help="item without a parsed source whose managed block this session just rewrote",
    )
    args = parser.parse_args(argv)
    try:
        planner, manifest_path, manifest = build_planner(args)
        plan = planner.run()
        if args.command == "baseline":
            result = baseline(planner, plan, manifest, set(args.accept))
            if args.write and result["recorded"]:
                save_manifest(manifest_path, manifest)
            print(
                json.dumps(
                    {"ok": True, "written": bool(args.write), **result}, indent=2
                )
            )
            return 0
        print(json.dumps(plan, indent=2, ensure_ascii=False))
        return EXIT_DRIFT if args.check and plan["drift"] else 0
    except (ReconcileError, OSError, ValueError, KeyError) as error:
        print(json.dumps({"ok": False, "error": str(error)}))
        return 1


if __name__ == "__main__":
    sys.exit(main())
