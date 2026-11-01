#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""Guardrail health scan: is the enforcement machinery hindering development?

Read-only and advisory. It reads story specs and the readiness record, and reports
friction signals (contract churn, waivers, checks CI can never verify, review loops,
stalled stories, failing gates) for the Guardrail Steward to discuss with the user.
It never changes anything and always exits 0 unless it cannot run.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import validate_story_contract as contract

CHURN_REVISION = (
    3  # a contract revised this many times suggests unclear intent or a rigid oracle
)
REVIEW_LOOPS = 3  # review bounced back this many times
WAIVER_RATIO = 0.25  # share of VAL-* waived before the validation design looks unfit
MANUAL_RATIO = 0.5
STALL_DAYS = 14
EXPIRY_WARNING_DAYS = 14
LOOP_RE = re.compile(r"^review_loop_iteration:\s*(\d+)\s*$", re.MULTILINE)
STATUS_RE = re.compile(r"status\W{0,6}(designing|building|ready)\b", re.IGNORECASE)


def signal(
    kind: str, severity: str, story: str | None, message: str, suggestion: str
) -> dict[str, object]:
    return {
        "id": kind,
        "severity": severity,
        "story": story,
        "message": message,
        "suggestion": suggestion,
    }


def readiness_signals(root: Path) -> list[dict[str, object]]:
    path = root / "docs/agent-readiness.md"
    if not path.is_file():
        return [
            signal(
                "readiness-missing",
                "concern",
                None,
                "docs/agent-readiness.md is missing, so no mechanism has proven it helps",
                "Run AR to design and prove the feedback loops before relying on them.",
            )
        ]
    text = path.read_text(encoding="utf-8")
    found: list[dict[str, object]] = []
    status = STATUS_RE.search(text)
    if status and status[1].casefold() != "ready":
        found.append(
            signal(
                "readiness-not-ready",
                "note",
                None,
                f"readiness status is '{status[1]}'",
                "Finish or re-prove AR; stories run against unproven mechanisms.",
            )
        )
    if "Contract CI Wiring" not in text:
        found.append(
            signal(
                "ci-wiring-missing",
                "note",
                None,
                "no Contract CI Wiring recorded; mechanical checks cannot be CI-verified",
                "Agree the per-suite JUnit/VAL convention in AR (bmad-testarch-ci).",
            )
        )
    return found


def story_signals(
    spec: Path, root: Path, today: date
) -> tuple[list[dict[str, object]], str]:
    text = spec.read_text(encoding="utf-8")
    document = contract.ContractDocument.from_text(spec, text)
    story = spec.relative_to(root).as_posix()
    status = contract.approval_status(document)
    found: list[dict[str, object]] = []

    section = document.section("Acceptance Contract")
    metadata = contract.parse_bullets(document.direct_body(section)) if section else {}
    revision = metadata.get("revision", "")
    if revision.isdigit() and int(revision) >= CHURN_REVISION:
        found.append(
            signal(
                "revision-churn",
                "concern",
                story,
                f"contract is on Revision {revision}",
                "Check whether intent was unclear at planning or the oracle is too "
                "rigid; discuss with PM/TEA before another revision.",
            )
        )

    loops = LOOP_RE.search(text.split("\n---", 2)[0] if text.startswith("---") else "")
    if loops and int(loops[1]) >= REVIEW_LOOPS:
        found.append(
            signal(
                "review-loops",
                "concern",
                story,
                f"review loop iteration {loops[1]}",
                "Repeated review rounds: look for a guardrail or test the developer "
                "cannot satisfy rather than another patch round.",
            )
        )

    validations = contract.extract_validations(document, [])
    results = contract.extract_results(document, [])
    total = len(validations)
    unverifiable = [
        row.validation_id
        for row in validations.values()
        if row.method == "mechanical"
        and not contract.PLANNED_TEST_RE.match(
            row.planned_check.strip().strip("`").strip()
        )
    ]
    if unverifiable:
        found.append(
            signal(
                "ci-unverifiable",
                "concern",
                story,
                f"{', '.join(unverifiable)} cannot be verified by CI (not a path::test)",
                "Plan it as a VAL-tagged test, or create a small converter skill that "
                "emits JUnit for it, instead of waiving it at delivery.",
            )
        )
    manual = sum(row.method == "manual" for row in validations.values())
    if total >= 3 and manual / total > MANUAL_RATIO:
        found.append(
            signal(
                "manual-heavy",
                "note",
                story,
                f"{manual} of {total} checks are manual",
                "Ask TEA whether some could be cheap automated checks.",
            )
        )
    waived = sorted(val for val, result in results.items() if result == "WAIVED")
    if total and len(waived) / total >= WAIVER_RATIO:
        found.append(
            signal(
                "waiver-heavy",
                "concern",
                story,
                f"{len(waived)} of {total} checks waived ({', '.join(waived)})",
                "The validation design may not fit how this work can be tested; "
                "revisit it with TEA rather than waiving by default.",
            )
        )
    exceptions = document.section("Exceptions", parent="Delivery Evidence")
    if exceptions is not None:
        rows = contract.parse_table(
            document.body(exceptions), ("VAL ID", "Reason", "Owner", "Expires"), [], ""
        )
        for row in rows:
            try:
                expires = date.fromisoformat(row["expires"])
            except ValueError:
                continue
            val = row["val id"].upper()
            if expires < today:
                found.append(
                    signal(
                        "waiver-expired",
                        "concern",
                        story,
                        f"{val} waiver expired on {expires}",
                        "Resolve or re-approve the waiver; delivered validation fails.",
                    )
                )
            elif expires <= today + timedelta(days=EXPIRY_WARNING_DAYS):
                found.append(
                    signal(
                        "waiver-expiring",
                        "note",
                        story,
                        f"{val} waiver expires on {expires}",
                        "Plan the follow-up before it lapses.",
                    )
                )

    if status == "approved":
        review = document.section("Review Record", parent="Delivery Evidence")
        reviewed = review is not None and not contract.contains_placeholder(
            contract.parse_bullets(document.direct_body(review)).get("reviewed by", "")
        )
        approval = document.section("Contract Approval")
        approved_at = (
            contract.parse_bullets(document.direct_body(approval)).get(
                "approved at", ""
            )
            if approval
            else ""
        )
        try:
            approved_day = datetime.strptime(approved_at, "%Y-%m-%dT%H:%M:%SZ").date()
        except ValueError:
            approved_day = None
        if not reviewed and approved_day:
            age = (today - approved_day).days
            if age > STALL_DAYS:
                found.append(
                    signal(
                        "stalled",
                        "note",
                        story,
                        f"approved {age} days ago and not yet reviewed",
                        "Ask whether a guardrail, test or environment issue is "
                        "blocking the developer.",
                    )
                )
        errors, _ = contract.run_validation(spec, "approved")
        if errors:
            shown = "; ".join(errors[:3]) + (" …" if len(errors) > 3 else "")
            found.append(
                signal(
                    "gate-failing",
                    "concern",
                    story,
                    f"approved contract fails its gate: {shown}",
                    "Fix the cause, or route a genuine requirement/test problem "
                    "through Correct Course; never weaken the check to pass.",
                )
            )
    return found, status


def scan(
    root: Path, *, story: Path | None = None, today: date | None = None
) -> dict[str, object]:
    today = today or datetime.now(timezone.utc).date()
    found = readiness_signals(root)
    specs = [story.resolve()] if story else contract.discover_specs(root)
    checked = 0
    for spec in specs:
        story_found, status = story_signals(spec, root, today)
        if status in {"approved", "draft"} or story_found:
            checked += 1
        found.extend(story_found)
    # The same friction in several stories points at the mechanism, not the story.
    if story is None:
        counts = Counter(item["id"] for item in found if item["story"])
        for kind, count in sorted(counts.items()):
            if count >= 2:
                found.append(
                    signal(
                        f"recurring:{kind}",
                        "concern",
                        None,
                        f"'{kind}' appears in {count} stories",
                        "A recurring pattern suggests the mechanism or convention "
                        "needs adjusting; review it with the Guardrail Steward.",
                    )
                )
    concerns = sum(item["severity"] == "concern" for item in found)
    return {
        "root": str(root),
        "contracts": checked,
        "concerns": concerns,
        "notes": len(found) - concerns,
        "signals": found,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, help="project root (default: from cwd)")
    parser.add_argument(
        "--story", type=Path, help="scan one spec (plus project checks)"
    )
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--today", type=date.fromisoformat, help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    root = args.root or contract.find_project_root(Path.cwd() / "_")
    if root is None or not root.is_dir():
        print("ERROR: cannot find the project root (no .jj or _bmad)", file=sys.stderr)
        return 2
    report = scan(root.resolve(), story=args.story, today=args.today)
    if args.as_json:
        print(json.dumps(report, indent=2))
        return 0
    print(
        f"Guardrail health scan: {report['concerns']} concern(s), {report['notes']} "
        f"note(s) across {report['contracts']} contract(s)"
    )
    for item in report["signals"]:  # type: ignore[union-attr]
        where = f" {item['story']}" if item["story"] else ""
        print(f"{item['severity'].upper()} [{item['id']}]{where}: {item['message']}")
        print(f"  -> {item['suggestion']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
