#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""Validate BMad story acceptance contracts using only the Python standard library."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from xml.parsers import expat

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
FENCE_RE = re.compile(r"^\s{0,3}(`{3,}|~{3,})")
AC_RE = re.compile(r"^-\s+(AC-\d+)\s+\[(P[0-3])\]\s*:\s*(.+)$", re.IGNORECASE)
VAL_ID_RE = re.compile(r"^VAL-\d+$", re.IGNORECASE)
PLACEHOLDER_MARKUP_RE = re.compile(r"\{\{.*?\}\}|\[add(?:\s+[^\]]*)?\]", re.IGNORECASE)
SOURCE_RE = re.compile(r"\[Source:\s*([^\]\n#]+)#([^\]\n]+)\]", re.IGNORECASE)
SOURCE_PLACEHOLDER_RE = re.compile(
    r"(?:^|[._/#-])(?:tbd|todo)(?:$|[._/#-])", re.IGNORECASE
)
DIGEST_RE = re.compile(r"^sha256:([0-9a-f]{64})$", re.IGNORECASE)
TRAILER_RE = re.compile(r"^([A-Za-z][A-Za-z-]*):[ \t]*(.*?)\s*$")
# A mechanical planned check written as `path/to/file.ext::test name` (commands don't match).
PLANNED_TEST_RE = re.compile(r"^(?P<path>[^\s:`]+\.[A-Za-z0-9]+)::(?P<name>\S.*)$")
LOCK_HEADERS = ("Path", "Lock digest")
# Lock digests ignore skip markers so activating red-phase scaffolds is not a test change.
SKIP_LINE_RE = re.compile(
    r"^\s*(?:@(?:pytest\.mark\.(?:skip|skipif|xfail)|unittest\.(?:skip\w*|expectedFailure)"
    r"|Disabled|Ignore)\b.*"
    r"|(?:test|it)\.(?:skip|fixme)\((?!.*(?:=>|function)).*\)\s*;?"
    r"|t\.Skip(?:f|Now)?\(.*\)\s*;?"
    r'|#\[ignore(?:\s*=\s*"[^"]*")?\])\s*$'
)
INLINE_SKIP_RE = re.compile(
    r"\b(test|it|describe|context|suite)(\.describe)?\.(?:skip|fixme|only)\("
)
X_PREFIX_RE = re.compile(r"\bx(it|test|describe)\(")
# Heuristic skip detection for delivery; CI results (not yet implemented) are the real proof.
SKIP_MARK_RE = re.compile(
    r"\b(?:test|it|describe|context|suite)(?:\.describe)?\.(?:skip|fixme|todo)\b"
    r"|\bx(?:it|test|describe)\(|@pytest\.mark\.(?:skip|skipif|xfail)\b"
    r"|\bunittest\.(?:skip\w*|expectedFailure)\b|@(?:Disabled|Ignore)\b"
    r"|\bt\.Skip(?:f|Now)?\(|#\[ignore\b"
)
FILE_SKIP_RE = re.compile(
    r"\b(?:test\.)?describe\.(?:skip|fixme)\(|\bxdescribe\(|^\s*pytestmark\b.*\bskip",
    re.MULTILINE,
)
EVIDENCE_TOKEN_RE = re.compile(r"[^\s,;()\[\]`'\"]+")
# Testcase-level JUnit properties that tag a test with its VAL ID (pytest record_property,
# hand-written converters). Values may list several IDs.
VAL_PROPERTY_NAMES = {"val", "val-id", "val_id", "validation", "validation-id"}
CONTRACT_PROPERTY_NAMES = {"contract", "contract-id", "contract_id"}
TEST_FILE_PROPERTY_NAMES = {"test-file", "test_file"}
TEST_ID_PROPERTY_NAMES = {"test-id", "test_id"}
FILE_NAME_RE = re.compile(r"[\w.-]+\.[A-Za-z][A-Za-z0-9]{1,7}")
SESSION_RE = re.compile(r"^-\s+Implementation session:\s*(\S+)", re.IGNORECASE)
# Trailers that make a jj change the approval record for one contract revision.
APPROVAL_TRAILERS = (
    "Contract-ID",
    "Contract-Revision",
    "Contract-Spec",
    "Contract-Digest",
    "Approved-by",
    "Validation-approved-by",
)

REQUIRED_CONTRACT_SUBSECTIONS = (
    "Intent",
    "Scope",
    "Sources",
    "Assumptions and Dependencies",
    "Acceptance Criteria",
    "Validation Design",
    "Open Questions",
    "Change Control",
)

ALLOWED_METHODS = {"mechanical", "manual"}
ALLOWED_LEVELS = {
    "unit",
    "component",
    "api",
    "boundary-contract",
    "integration",
    "e2e",
    "inspection",
    "analysis",
    "demonstration",
}
ALLOWED_RESULTS = {"PASS", "FAIL", "WAIVED"}


@dataclass(frozen=True)
class Section:
    title: str
    level: int
    start: int
    content_start: int
    end: int


@dataclass(frozen=True)
class ValidationRow:
    validation_id: str
    covers: tuple[str, ...]
    method: str
    level: str
    planned_check: str
    expected_evidence: str
    owner: str
    manual_reason: str


@dataclass
class ContractDocument:
    path: Path
    text: str
    lines: list[str]
    sections: list[Section]

    @classmethod
    def load(cls, path: Path) -> ContractDocument:
        return cls.from_text(path, path.read_text(encoding="utf-8"))

    @classmethod
    def from_text(cls, path: Path, text: str) -> ContractDocument:
        lines = text.splitlines()
        return cls(path=path, text=text, lines=lines, sections=parse_sections(lines))

    def section(self, title: str, *, parent: str | None = None) -> Section | None:
        candidates = [
            section
            for section in self.sections
            if section.title.casefold() == title.casefold()
        ]
        if parent is None:
            return candidates[0] if candidates else None
        parent_section = self.section(parent)
        if parent_section is None:
            return None
        return next(
            (
                section
                for section in candidates
                if parent_section.start < section.start < parent_section.end
            ),
            None,
        )

    def body(self, section: Section) -> list[str]:
        return self.lines[section.content_start : section.end]

    def direct_body(self, section: Section) -> list[str]:
        """Return content before the section's first nested heading."""
        end = section.end
        for candidate in self.sections:
            if (
                section.start < candidate.start < section.end
                and candidate.level > section.level
            ):
                end = candidate.start
                break
        return visible_lines(self.lines[section.content_start : end])

    def contract_text(self) -> str:
        section = self.section("Acceptance Contract")
        if section is None:
            raise ValueError("missing '## Acceptance Contract' section")
        return "\n".join(self.lines[section.start : section.end]).rstrip() + "\n"


def visible_indexed_lines(lines: Iterable[str]) -> Iterator[tuple[int, str]]:
    """Yield Markdown outside fenced code blocks and HTML comments."""
    fence: tuple[str, int] | None = None
    in_comment = False
    for index, original in enumerate(lines):
        line = original
        visible = ""
        while line:
            if in_comment:
                end = line.find("-->")
                if end < 0:
                    line = ""
                    break
                line = line[end + 3 :]
                in_comment = False
                continue
            start = line.find("<!--")
            if start < 0:
                visible += line
                break
            visible += line[:start]
            line = line[start + 4 :]
            in_comment = True

        fence_match = FENCE_RE.match(visible)
        if fence is not None:
            closing = re.fullmatch(
                rf"\s{{0,3}}{re.escape(fence[0])}{{{fence[1]},}}\s*", visible
            )
            if closing:
                fence = None
            continue
        if fence_match:
            marker = fence_match.group(1)
            fence = (marker[0], len(marker))
            continue
        yield index, visible


def visible_lines(lines: Iterable[str]) -> list[str]:
    return [line for _, line in visible_indexed_lines(lines)]


def parse_sections(lines: list[str]) -> list[Section]:
    headings: list[tuple[str, int, int]] = []
    for index, line in visible_indexed_lines(lines):
        match = HEADING_RE.match(line)
        if match:
            headings.append((match.group(2).strip(), len(match.group(1)), index))

    sections: list[Section] = []
    for position, (title, level, start) in enumerate(headings):
        end = len(lines)
        for _, next_level, next_start in headings[position + 1 :]:
            if next_level <= level:
                end = next_start
                break
        sections.append(Section(title, level, start, start + 1, end))
    return sections


def parse_bullets(lines: Iterable[str]) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in lines:
        match = re.match(r"^-\s+([^:]+):\s*(.*?)\s*$", line)
        if match:
            values[match.group(1).strip().casefold()] = match.group(2).strip()
    return values


def split_table_row(line: str) -> list[str] | None:
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        return None
    cells: list[str] = []
    current: list[str] = []
    inner = stripped[1:-1]
    index = 0
    while index < len(inner):
        char = inner[index]
        if char == "\\":
            run_end = index
            while run_end < len(inner) and inner[run_end] == "\\":
                run_end += 1
            slash_count = run_end - index
            if run_end < len(inner) and inner[run_end] == "|":
                current.extend("\\" * (slash_count // 2))
                if slash_count % 2:
                    current.append("|")
                else:
                    cells.append("".join(current).strip())
                    current = []
                index = run_end + 1
                continue
            current.extend("\\" * slash_count)
            index = run_end
            continue
        if char == "|":
            cells.append("".join(current).strip())
            current = []
        else:
            current.append(char)
        index += 1
    cells.append("".join(current).strip())
    return cells


def parse_table(
    lines: Iterable[str],
    expected_headers: tuple[str, ...],
    errors: list[str],
    table_name: str,
) -> list[dict[str, str]]:
    groups: list[list[str]] = []
    current: list[str] = []
    for line in visible_lines(lines):
        if line.strip().startswith("|"):
            current.append(line)
        elif current:
            groups.append(current)
            current = []
    if current:
        groups.append(current)
    if not groups:
        errors.append(f"{table_name} table is missing")
        return []
    if len(groups) > 1:
        errors.append(f"{table_name} must contain exactly one Markdown table")
    table_lines = groups[0]
    if len(table_lines) < 2:
        errors.append(f"{table_name} table has no divider row")
        return []

    header_cells = split_table_row(table_lines[0])
    if header_cells is None:
        errors.append(f"{table_name} header is malformed")
        return []
    headers = tuple(cell.casefold() for cell in header_cells)
    expected = tuple(header.casefold() for header in expected_headers)
    if headers != expected:
        errors.append(f"{table_name} table has non-standard headers")
        return []

    divider = split_table_row(table_lines[1])
    if (
        divider is None
        or len(divider) != len(headers)
        or any(not re.fullmatch(r":?-{3,}:?", cell) for cell in divider)
    ):
        errors.append(f"{table_name} table has an invalid divider row")
        return []

    rows: list[dict[str, str]] = []
    for row_number, line in enumerate(table_lines[2:], start=1):
        row = split_table_row(line)
        if row is None or len(row) != len(headers):
            errors.append(f"{table_name} row {row_number} is malformed")
            continue
        if all(not cell for cell in row):
            errors.append(f"{table_name} row {row_number} is empty")
            continue
        rows.append(dict(zip(headers, row, strict=True)))
    return rows


def contract_digest(document: ContractDocument) -> str:
    payload = document.contract_text().encode("utf-8")
    return f"sha256:{hashlib.sha256(payload).hexdigest()}"


def contains_placeholder(value: str) -> bool:
    stripped = value.strip()
    token = stripped.strip("`[] .:-").casefold()
    angle_placeholder = bool(re.fullmatch(r"<[A-Za-z][A-Za-z0-9 _.-]*>", stripped))
    return (
        not token
        or token in {"pending", "tbd", "todo", "unknown"}
        or angle_placeholder
        or bool(PLACEHOLDER_MARKUP_RE.search(stripped))
    )


def extract_acceptance_criteria(
    document: ContractDocument, errors: list[str]
) -> dict[str, str]:
    section = document.section("Acceptance Criteria", parent="Acceptance Contract")
    if section is None:
        return {}
    criteria: dict[str, str] = {}
    for line in visible_lines(document.body(section)):
        stripped = line.strip()
        match = AC_RE.match(stripped)
        if not match:
            if re.match(r"^-\s+AC(?:-|\b)", stripped, re.IGNORECASE):
                errors.append(f"malformed acceptance criterion: {stripped}")
            continue
        criterion_id = match.group(1).upper()
        if criterion_id in criteria:
            errors.append(f"duplicate acceptance criterion: {criterion_id}")
        elif contains_placeholder(match.group(3)):
            errors.append(
                f"{criterion_id} contains a placeholder or has no observable criterion"
            )
        else:
            criteria[criterion_id] = match.group(2).upper()
    if not criteria:
        errors.append("no acceptance criteria found; expected '- AC-1 [P0]: ...'")
    return criteria


def extract_validations(
    document: ContractDocument, errors: list[str]
) -> dict[str, ValidationRow]:
    section = document.section("Validation Design", parent="Acceptance Contract")
    if section is None:
        return {}
    headers = (
        "VAL ID",
        "Covers",
        "Method",
        "Level",
        "Planned check or procedure",
        "Expected evidence",
        "Owner",
        "Manual reason",
    )
    raw_rows = parse_table(document.body(section), headers, errors, "Validation Design")
    if not raw_rows:
        errors.append("Validation Design table has no obligations")
        return {}

    validations: dict[str, ValidationRow] = {}
    for raw in raw_rows:
        validation_id = raw["val id"].upper()
        covers_text = raw["covers"]
        if not re.fullmatch(r"AC-\d+(?:\s*,\s*AC-\d+)*", covers_text, re.IGNORECASE):
            errors.append(
                f"{validation_id or '<empty>'} has malformed Covers value: {covers_text or '<empty>'}"
            )
            covers: tuple[str, ...] = ()
        else:
            covers = tuple(
                dict.fromkeys(
                    item.upper()
                    for item in re.findall(r"AC-\d+", covers_text, re.IGNORECASE)
                )
            )
        method = raw["method"].casefold()
        row = ValidationRow(
            validation_id=validation_id,
            covers=covers,
            method=method,
            level=raw["level"],
            planned_check=raw["planned check or procedure"],
            expected_evidence=raw["expected evidence"],
            owner=raw["owner"],
            manual_reason=raw["manual reason"],
        )
        if not VAL_ID_RE.fullmatch(validation_id):
            errors.append(f"invalid validation ID: {validation_id or '<empty>'}")
            continue
        if validation_id in validations:
            errors.append(f"duplicate validation obligation: {validation_id}")
            continue
        if not covers:
            errors.append(f"{validation_id} does not cover an AC-* ID")
        if method not in ALLOWED_METHODS:
            errors.append(f"{validation_id} method must be mechanical or manual")
        if row.level.casefold() not in ALLOWED_LEVELS:
            errors.append(
                f"{validation_id} has unsupported validation level: {row.level or '<empty>'}"
            )
        for field_name, value in (
            ("level", row.level),
            ("planned check or procedure", row.planned_check),
            ("expected evidence", row.expected_evidence),
            ("owner", row.owner),
        ):
            if contains_placeholder(value):
                errors.append(
                    f"{validation_id} has a missing or placeholder {field_name}"
                )
        if method == "manual" and (
            contains_placeholder(row.manual_reason) or row.manual_reason == "-"
        ):
            errors.append(f"{validation_id} manual validation requires a reason")
        validations[validation_id] = row
    return validations


def check_required_content(document: ContractDocument, errors: list[str]) -> None:
    def material(title: str) -> list[str]:
        section = document.section(title, parent="Acceptance Contract")
        if section is None:
            return []
        return [line.strip() for line in document.direct_body(section) if line.strip()]

    for title in ("Intent", "Assumptions and Dependencies", "Change Control"):
        lines = material(title)
        if not lines or all(contains_placeholder(line) for line in lines):
            errors.append(
                f"Acceptance Contract subsection is empty or contains only placeholders: {title}"
            )

    scope_section = document.section("Scope", parent="Acceptance Contract")
    scope = parse_bullets(document.direct_body(scope_section)) if scope_section else {}
    for field in ("in scope", "out of scope"):
        if field not in scope or contains_placeholder(scope.get(field, "")):
            errors.append(f"Scope field is missing or pending: {field}")

    sources = material("Sources")
    source_matches = [match for line in sources for match in SOURCE_RE.finditer(line)]
    if not source_matches:
        errors.append(
            "Sources must contain at least one complete '[Source: path#section]' reference"
        )
    elif any(
        contains_placeholder(component) or SOURCE_PLACEHOLDER_RE.search(component)
        for match in source_matches
        for component in match.groups()
    ):
        errors.append("Sources contain a placeholder path or section")


def check_open_questions(
    document: ContractDocument, errors: list[str], *, approved: bool
) -> None:
    section = document.section("Open Questions", parent="Acceptance Contract")
    if section is None or not approved:
        return
    material = [line.strip() for line in document.body(section) if line.strip()]
    accepted = {"- none.", "none."}
    if not material or any(line.casefold() not in accepted for line in material):
        errors.append(
            "approved contract has unresolved Open Questions; use exactly '- None.' when clear"
        )


def check_approval(
    document: ContractDocument, errors: list[str], *, require_approved: bool
) -> None:
    section = document.section("Contract Approval")
    if section is None:
        return
    approval = parse_bullets(document.direct_body(section))
    required = (
        "status",
        "approved by",
        "validation approved by",
        "approved at",
        "contract digest",
        "validation artifacts",
    )
    for field in required:
        if field not in approval:
            errors.append(f"Contract Approval field is missing: {field}")
        elif require_approved and contains_placeholder(approval[field]):
            errors.append(f"Contract Approval field is pending: {field}")

    status = approval.get("status", "").casefold()
    if status not in {"draft", "approved", "superseded"}:
        errors.append("Contract Approval status must be draft, approved, or superseded")
    if require_approved and status != "approved":
        errors.append("Contract Approval status must be 'approved'")

    approved_at = approval.get("approved at", "")
    if approved_at and not contains_placeholder(approved_at):
        try:
            datetime.strptime(approved_at, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            errors.append(
                "Approved at must be a valid UTC timestamp YYYY-MM-DDTHH:MM:SSZ"
            )
    artifacts = approval.get("validation artifacts", "")
    if require_approved and artifacts.casefold() in {
        "none",
        "none.",
        "n/a",
        "not applicable",
    }:
        errors.append(
            "Validation artifacts must link the pre-implementation validation output"
        )
    recorded_digest = approval.get("contract digest", "")
    if recorded_digest and not contains_placeholder(recorded_digest):
        if not DIGEST_RE.fullmatch(recorded_digest):
            errors.append(
                "Contract digest must use sha256:<64 lowercase hex characters>"
            )
        elif recorded_digest.casefold() != contract_digest(document).casefold():
            errors.append(
                "Acceptance Contract changed after approval; digest does not match"
            )


def extract_results(document: ContractDocument, errors: list[str]) -> dict[str, str]:
    section = document.section("Validation Results", parent="Delivery Evidence")
    if section is None:
        return {}
    headers = ("VAL ID", "Result", "Evidence", "Build or run")
    raw_rows = parse_table(
        document.body(section), headers, errors, "Validation Results"
    )
    if not raw_rows:
        errors.append("Validation Results table has no evidence rows")
        return {}
    results: dict[str, str] = {}
    for row in raw_rows:
        validation_id = row["val id"].upper()
        result = row["result"].upper()
        if validation_id in results:
            errors.append(f"duplicate delivery evidence row: {validation_id}")
            continue
        if result not in ALLOWED_RESULTS:
            errors.append(f"{validation_id} result must be PASS, FAIL, or WAIVED")
        if contains_placeholder(row["evidence"]):
            errors.append(f"{validation_id} delivery evidence is missing")
        if contains_placeholder(row["build or run"]):
            errors.append(f"{validation_id} build or run identity is missing")
        results[validation_id] = result
    return results


def extract_exceptions(document: ContractDocument, errors: list[str]) -> set[str]:
    section = document.section("Exceptions", parent="Delivery Evidence")
    if section is None:
        return set()
    headers = ("VAL ID", "Reason", "Owner", "Expires")
    rows = parse_table(document.body(section), headers, errors, "Exceptions")
    exception_ids: set[str] = set()
    today = datetime.now(timezone.utc).date()
    for row in rows:
        validation_id = row["val id"].upper()
        if not VAL_ID_RE.fullmatch(validation_id):
            errors.append(
                f"invalid exception validation ID: {validation_id or '<empty>'}"
            )
            continue
        if validation_id in exception_ids:
            errors.append(f"duplicate exception row: {validation_id}")
            continue
        for field in ("reason", "owner", "expires"):
            if contains_placeholder(row[field]):
                errors.append(f"{validation_id} exception {field} is missing")
        expires = row["expires"]
        if not contains_placeholder(expires):
            try:
                expiry_date = date.fromisoformat(expires)
                if expiry_date < today:
                    errors.append(f"{validation_id} exception expired on {expires}")
            except ValueError:
                errors.append(f"{validation_id} exception expiry must use YYYY-MM-DD")
        exception_ids.add(validation_id)
    return exception_ids


def validate(document: ContractDocument, phase: str) -> list[str]:
    errors: list[str] = []

    def unique_section(title: str, *, level: int) -> Section | None:
        matches = [
            section
            for section in document.sections
            if section.title.casefold() == title.casefold()
        ]
        if not matches:
            errors.append(f"missing required section: {title}")
            return None
        if len(matches) > 1:
            errors.append(f"duplicate section: {title}")
        section = matches[0]
        if section.level != level:
            errors.append(f"{title} must be a level-{level} heading")
        return section

    contract = unique_section("Acceptance Contract", level=2)
    approval = unique_section("Contract Approval", level=2)
    evidence = unique_section("Delivery Evidence", level=2)
    if contract is None:
        return sorted(set(errors))

    for title in REQUIRED_CONTRACT_SUBSECTIONS:
        matches = [
            section
            for section in document.sections
            if section.title.casefold() == title.casefold()
            and contract.start < section.start < contract.end
        ]
        if not matches:
            errors.append(f"missing Acceptance Contract subsection: {title}")
        elif len(matches) > 1:
            errors.append(f"duplicate Acceptance Contract subsection: {title}")
        elif matches[0].level != 3:
            errors.append(
                f"Acceptance Contract subsection must be a level-3 heading: {title}"
            )

    if evidence is not None:
        for title in ("Validation Results", "Exceptions"):
            matches = [
                section
                for section in document.sections
                if section.title.casefold() == title.casefold()
                and evidence.start < section.start < evidence.end
            ]
            if not matches:
                errors.append(f"missing Delivery Evidence subsection: {title}")
            elif len(matches) > 1:
                errors.append(f"duplicate Delivery Evidence subsection: {title}")
            elif matches[0].level != 3:
                errors.append(
                    f"Delivery Evidence subsection must be a level-3 heading: {title}"
                )

    for heading in (contract, approval):
        if heading is None:
            continue
        seen_keys: set[str] = set()
        for line in document.direct_body(heading):
            entry = re.match(r"^-\s+([^:]+):\s*(.*?)\s*$", line)
            if entry is None:
                continue
            key = entry[1].strip().casefold()
            if key in seen_keys:
                errors.append(f"duplicate {heading.title} field: {key}")
            seen_keys.add(key)

    metadata = parse_bullets(document.direct_body(contract))
    for field in ("contract id", "revision", "risk"):
        if field not in metadata or contains_placeholder(metadata.get(field, "")):
            errors.append(
                f"Acceptance Contract metadata is missing or pending: {field}"
            )
    if metadata.get("risk", "").casefold() not in {"low", "medium", "high", "critical"}:
        errors.append("Risk must be low, medium, high, or critical")
    revision = metadata.get("revision", "")
    if revision and (not revision.isdigit() or revision == "0"):
        errors.append("Revision must be a positive integer")

    check_required_content(document, errors)
    criteria = extract_acceptance_criteria(document, errors)
    validations = extract_validations(document, errors)
    for validation in validations.values():
        for criterion_id in validation.covers:
            if criterion_id not in criteria:
                errors.append(
                    f"{validation.validation_id} references missing criterion {criterion_id}"
                )
    covered = {
        criterion_id
        for validation in validations.values()
        for criterion_id in validation.covers
    }
    for criterion_id in criteria:
        if criterion_id not in covered:
            errors.append(f"{criterion_id} has no validation obligation")

    approved = phase in {"approved", "delivered"}
    check_open_questions(document, errors, approved=approved)
    if approval is not None:
        check_approval(document, errors, require_approved=approved)

    if phase == "delivered" and evidence is not None:
        results = extract_results(document, errors)
        exceptions = extract_exceptions(document, errors)
        for validation_id in validations:
            if validation_id not in results:
                errors.append(f"{validation_id} has no delivery evidence")
            elif results[validation_id] == "FAIL":
                errors.append(f"{validation_id} delivery result is FAIL")
            elif results[validation_id] == "WAIVED" and validation_id not in exceptions:
                errors.append(f"{validation_id} is WAIVED without a complete exception")
        for validation_id in results:
            if validation_id not in validations:
                errors.append(
                    f"delivery evidence references unknown validation {validation_id}"
                )
        for validation_id in exceptions:
            if validation_id not in validations:
                errors.append(
                    f"exception references unknown validation {validation_id}"
                )
            elif results.get(validation_id) != "WAIVED":
                errors.append(f"{validation_id} has an exception but is not WAIVED")
    return sorted(set(errors))


class JjError(RuntimeError):
    """jj could not be run or rejected a read-only query."""


def find_jj_root(start: Path) -> Path | None:
    for candidate in (start, *start.parents):
        if (candidate / ".jj").is_dir():
            return candidate
    return None


def run_jj(root: Path, *args: str) -> str:
    # --ignore-working-copy keeps verification read-only: it never snapshots or locks @.
    command = [
        os.environ.get("BMAD_JJ_BIN", "jj"),
        "--ignore-working-copy",
        "--color=never",
        "--no-pager",
        *args,
    ]
    try:
        result = subprocess.run(
            command, cwd=root, capture_output=True, text=True, check=False
        )
    except OSError as error:
        raise JjError(f"cannot run jj: {error}") from error
    if result.returncode != 0:
        raise JjError(result.stderr.strip() or f"jj exited with {result.returncode}")
    return result.stdout


def parse_trailers(description: str) -> dict[str, list[str]]:
    trailers: dict[str, list[str]] = {}
    for line in description.splitlines():
        match = TRAILER_RE.match(line)
        if match:
            trailers.setdefault(match[1].casefold(), []).append(match[2])
    return trailers


def check_jj_approval(document: ContractDocument, *, require: bool) -> list[str]:
    """Verify the contract against the version sealed in its jj approval change.

    The approved text is read from history, so editing the contract and recomputing the
    digest in the working file cannot pass. This pins *what* was approved; it does not
    authenticate *who* approved it (that needs signed approval changes or host review).
    """
    errors: list[str] = []
    story = document.path.resolve()
    root = find_jj_root(story.parent)
    if root is None:
        if require:
            errors.append(
                "--require-jj: the story is not inside a jj workspace, so its approval "
                "change cannot be verified"
            )
        return errors
    contract = document.section("Acceptance Contract")
    approval = document.section("Contract Approval")
    if contract is None or approval is None:
        return errors  # structural validation already reports the missing section
    relative = story.relative_to(root.resolve()).as_posix()
    if '"' in relative or "\\" in relative:
        return [f"story path cannot be quoted in a jj fileset: {relative}"]
    metadata = parse_bullets(document.direct_body(contract))
    contract_id = metadata.get("contract id", "")
    revision = metadata.get("revision", "")

    try:
        history = run_jj(
            root,
            "log",
            "--no-graph",
            "-r",
            '::@- & description(substring-i:"Contract-ID:")',
            "-T",
            'commit_id ++ "\\x1e" ++ description ++ "\\x1f"',
        )
    except JjError as error:
        return [f"cannot read jj history to verify the approval change: {error}"]

    candidates: list[tuple[str, dict[str, list[str]]]] = []
    for record in history.split("\x1f"):
        if "\x1e" not in record:
            continue
        commit, description = record.split("\x1e", 1)
        trailers = parse_trailers(description)
        ids = [value.casefold() for value in trailers.get("contract-id", [])]
        if ids == [contract_id.casefold()] and trailers.get("contract-spec") == [
            relative
        ]:
            candidates.append((commit.strip(), trailers))

    if revision.isdigit():
        later = [
            commit[:12]
            for commit, trailers in candidates
            if any(
                value.isdigit() and int(value) > int(revision)
                for value in trailers.get("contract-revision", [])
            )
        ]
        if later:
            errors.append(
                f"jj history approves a later revision than Revision {revision} "
                f"({', '.join(later)}); a contract revision must not go backwards"
            )
    matching = [
        (commit, trailers)
        for commit, trailers in candidates
        if trailers.get("contract-revision") == [revision]
    ]
    if not matching:
        errors.append(
            f"no jj approval change for {contract_id or '<missing id>'} revision "
            f"{revision or '<missing>'} in ::@-; record approval as its own change "
            "with the trailers in story-contract.md, then run `jj new` to seal it"
        )
        return errors
    if len(matching) > 1:
        shorts = ", ".join(commit[:12] for commit, _ in matching)
        errors.append(
            f"multiple jj approval changes for {contract_id} revision {revision} "
            f"({shorts}); approval is ambiguous"
        )
        return errors

    commit, trailers = matching[0]
    short = commit[:12]
    for name in APPROVAL_TRAILERS:
        values = trailers.get(name.casefold(), [])
        if len(values) != 1 or contains_placeholder(values[0]):
            errors.append(
                f"approval change {short} needs exactly one completed {name} trailer"
            )
    if errors:
        return errors

    try:
        touched = set(run_jj(root, "diff", "-r", commit, "--name-only").splitlines())
        approved_text = run_jj(
            root, "file", "show", "-r", commit, f'root-file:"{relative}"'
        )
    except JjError as error:
        return [f"cannot read approval change {short}: {error}"]
    if touched != {relative}:
        errors.append(
            f"approval change {short} must change only {relative}; it changes: "
            + (", ".join(sorted(touched)) or "nothing")
        )

    approved = ContractDocument.from_text(document.path, approved_text)
    try:
        approved_digest = contract_digest(approved)
    except ValueError as error:
        return [*errors, f"approval change {short}: {error}"]
    if approved_digest.casefold() != trailers["contract-digest"][0].casefold():
        errors.append(
            f"approval change {short}: its Contract-Digest trailer does not match "
            "the contract text it records"
        )
    approved_section = approved.section("Contract Approval")
    approved_fields = (
        parse_bullets(approved.direct_body(approved_section))
        if approved_section
        else {}
    )
    if approved_fields.get("status", "").casefold() != "approved":
        errors.append(f"approval change {short} does not record Status: approved")
    current_fields = parse_bullets(document.direct_body(approval))
    for field, trailer in (
        ("approved by", "approved-by"),
        ("validation approved by", "validation-approved-by"),
    ):
        expected = trailers[trailer][0]
        if approved_fields.get(field) != expected:
            errors.append(
                f"approval change {short}: '{field}' in the spec differs from its "
                "trailer"
            )
        elif current_fields.get(field) != expected:
            errors.append(
                f"'{field}' differs from the value approved in jj change {short}"
            )
    errors.extend(check_approved_locks(root, commit, approved, document))
    if contract_digest(document).casefold() != approved_digest.casefold():
        errors.append(
            f"Acceptance Contract differs from the version approved in jj change "
            f"{short}; recomputing the digest does not re-approve it, use Correct "
            "Course and a new approval change"
        )
    return errors


def find_project_root(story: Path) -> Path | None:
    """The jj workspace root, else the nearest ancestor holding a BMad install."""
    start = story.resolve().parent
    jj_root = find_jj_root(start)
    if jj_root is not None:
        return jj_root
    for candidate in (start, *start.parents):
        if (candidate / "_bmad").is_dir():
            return candidate
    return None


def lock_digest(text: str) -> str:
    """SHA-256 of a test file with skip markers neutralised (activation is not a change)."""
    lines = [
        line.rstrip()
        for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
        if not SKIP_LINE_RE.match(line)
    ]
    normalised = "\n".join(
        X_PREFIX_RE.sub(r"\1(", INLINE_SKIP_RE.sub(r"\1\2(", line)) for line in lines
    ).strip()
    return f"sha256:{hashlib.sha256(normalised.encode('utf-8')).hexdigest()}"


def resolve_in_root(root: Path, relative: str) -> Path | None:
    """Resolve a project-relative path, refusing anything outside the project root."""
    candidate = (root / relative).resolve()
    return candidate if candidate.is_relative_to(root.resolve()) else None


def planned_tests(document: ContractDocument) -> list[tuple[str, str, str]]:
    """(VAL ID, path, test name) for mechanical checks written as `path::name`."""
    planned = []
    for row in extract_validations(document, []).values():
        match = PLANNED_TEST_RE.match(row.planned_check.strip().strip("`").strip())
        if row.method == "mechanical" and match:
            name = match["name"].split("::")[-1].strip()
            planned.append((row.validation_id, match["path"], name))
    return planned


def read_locks(document: ContractDocument, errors: list[str]) -> dict[str, str] | None:
    """Locked test path -> lock digest, or None when the table is absent."""
    section = document.section("Locked Tests", parent="Contract Approval")
    if section is None:
        return None
    body = document.body(section)
    if not any(line.strip().startswith("|") for line in visible_lines(body)):
        text = " ".join(line.strip() for line in visible_lines(body) if line.strip())
        if text.casefold().strip("- .") == "none":
            return {}
    locks: dict[str, str] = {}
    for row in parse_table(body, LOCK_HEADERS, errors, "Locked Tests"):
        path, digest = row["path"].strip("`"), row["lock digest"].strip("`")
        if contains_placeholder(path) or '"' in path or "\\" in path:
            errors.append(f"Locked Tests has an invalid path: {path or '<empty>'}")
        elif not DIGEST_RE.fullmatch(digest):
            errors.append(f"Locked Tests digest for {path} must be sha256:<64 hex>")
        elif path in locks:
            errors.append(f"Locked Tests lists {path} twice")
        else:
            locks[path] = digest.casefold()
    return locks


def check_locks(document: ContractDocument, root: Path | None) -> list[str]:
    """Approved ATDD tests must still match their lock digests (#4)."""
    errors: list[str] = []
    locks = read_locks(document, errors)
    contract = document.section("Acceptance Contract")
    metadata = parse_bullets(document.direct_body(contract)) if contract else {}
    tracked = metadata.get("contract id", "").upper().startswith("STORY-")
    planned = planned_tests(document)
    if locks is None:
        if tracked and planned:
            errors.append(
                "Contract Approval needs a '### Locked Tests' table locking the planned "
                "ATDD test files; generate it with the validator `lock` command"
            )
        return errors
    if tracked:
        for validation_id, path, _ in planned:
            if path not in locks:
                errors.append(
                    f"{validation_id} planned test file is not locked: {path}"
                )
    if not locks:
        return errors
    if root is None:
        return [
            *errors,
            "cannot find the project root (no .jj or _bmad ancestor) to check locked tests",
        ]
    for path, digest in locks.items():
        file = resolve_in_root(root, path)
        if file is None or not file.is_file():
            errors.append(f"locked test file is missing: {path}")
        elif lock_digest(file.read_text(encoding="utf-8")) != digest:
            errors.append(
                f"locked test changed since approval: {path}; only skip markers may be "
                "removed, any other change needs a new Revision and approval (Correct Course)"
            )
    return errors


def check_approved_locks(
    root: Path, commit: str, approved: ContractDocument, document: ContractDocument
) -> list[str]:
    """Locks must come from the approval change and match the tests as approved."""
    short = commit[:12]
    approved_locks = read_locks(approved, []) or {}
    errors: list[str] = []
    if (read_locks(document, []) or {}) != approved_locks:
        errors.append(
            f"Locked Tests differ from those recorded in approval change {short}"
        )
    for path, digest in approved_locks.items():
        try:
            text = run_jj(root, "file", "show", "-r", commit, f'root-file:"{path}"')
        except JjError:
            errors.append(f"approval change {short}: locked test {path} did not exist")
            continue
        if lock_digest(text) != digest:
            errors.append(
                f"approval change {short}: lock digest for {path} does not match the "
                "test as approved"
            )
    return errors


def val_tag_re(validation_id: str) -> re.Pattern[str]:
    """Matches VAL-1 / VAL_1 / val1 / test_val_1_save, but not VAL-12 or interval1."""
    number = validation_id.split("-", 1)[1].lstrip("0") or "0"
    return re.compile(rf"(?<![A-Za-z0-9])VAL[-_ ]?0*{number}(?![0-9])", re.IGNORECASE)


def path_suffix_matches(location: str, planned: str) -> bool:
    """True when one path is a component-wise suffix of the other (reporters vary)."""
    a = [
        part for part in location.replace("\\", "/").split("/") if part not in ("", ".")
    ]
    b = [
        part for part in planned.replace("\\", "/").split("/") if part not in ("", ".")
    ]
    shorter, longer = sorted((a, b), key=len)
    return bool(shorter) and longer[-len(shorter) :] == shorter


class UnsafeXml(ValueError):
    """The report declares a DTD or entity (refused: entity expansion attacks)."""


def read_junit(path: Path, errors: list[str]) -> list[dict[str, str]]:
    """Testcases from a JUnit XML report: name, status and any reported file.

    Streams with expat and refuses DTDs and entities, as defusedxml would, so the
    validator stays standard-library only.
    """
    try:
        data = path.read_bytes()
    except OSError as error:
        errors.append(f"cannot read CI results {path}: {error}")
        return []
    cases: list[dict[str, str]] = []
    suite_files: list[str] = []
    current: dict[str, str] | None = None

    def refuse(*_: object) -> int:
        raise UnsafeXml

    def record_property(attrs: dict[str, str]) -> None:
        # Only testcase-level properties tag a test; suite-level ones would tag them all.
        name = attrs.get("name", "").strip().casefold()
        if current is None:
            return
        for names, field in (
            (VAL_PROPERTY_NAMES, "vals"),
            (CONTRACT_PROPERTY_NAMES, "contracts"),
            (TEST_FILE_PROPERTY_NAMES, "test_files"),
            (TEST_ID_PROPERTY_NAMES, "test_ids"),
        ):
            if name in names:
                current[field] = (
                    current[field] + "\n" + attrs.get("value", "")
                ).strip()
                break

    def start(tag: str, attrs: dict[str, str]) -> None:
        nonlocal current
        if tag == "testsuite":
            suite_files.append(attrs.get("file", ""))
        elif tag == "testcase":
            inherited = next((file for file in reversed(suite_files) if file), "")
            current = {
                "name": attrs.get("name", ""),
                "file": attrs.get("file") or inherited,
                "status": "passed",
                "vals": "",
                "contracts": "",
                "test_files": "",
                "test_ids": "",
                "classname": attrs.get("classname", ""),
            }
        elif tag == "property":
            record_property(attrs)
        elif current is not None and tag in {"failure", "error"}:
            current["status"] = "failed"
        elif current is not None and tag == "skipped" and current["status"] != "failed":
            current["status"] = "skipped"

    def end(tag: str) -> None:
        nonlocal current
        if tag == "testsuite" and suite_files:
            suite_files.pop()
        elif tag == "testcase" and current is not None:
            cases.append(current)
            current = None

    parser = expat.ParserCreate()
    parser.StartDoctypeDeclHandler = refuse
    parser.EntityDeclHandler = refuse
    parser.ExternalEntityRefHandler = refuse
    parser.StartElementHandler = start
    parser.EndElementHandler = end
    try:
        parser.Parse(data, True)
    except UnsafeXml:
        errors.append(f"CI results {path} must not contain a DOCTYPE or entities")
        return []
    except expat.ExpatError as error:
        errors.append(f"CI results {path} are not valid JUnit XML: {error}")
        return []
    if not cases:
        errors.append(f"CI results {path} contain no testcases")
    return cases


def full_test_path_matches(location: str, planned: str) -> bool:
    """A reporter may prepend its CI workspace, but may not omit planned directories."""
    actual = tuple(
        p for p in location.replace("\\", "/").split("/") if p not in {"", "."}
    )
    expected = tuple(
        p for p in planned.replace("\\", "/").split("/") if p not in {"", "."}
    )
    return (
        bool(expected)
        and ".." not in actual
        and ".." not in expected
        and len(actual) >= len(expected)
        and actual[-len(expected) :] == expected
    )


def testcase_identity_matches(case: dict[str, str], path: str, node: str) -> bool:
    """Match a full planned test, never just a basename and generic leaf name.

    Native reporters can supply file+name (and classname for class-qualified plans).
    Otherwise an adapter supplies testcase test-file or test-id properties. If another
    identity field is present it must agree; short reporter basenames alone prove nothing.
    """
    ids = set(case.get("test_ids", "").splitlines()) - {""}
    files = set(case.get("test_files", "").splitlines()) - {""}
    if len(ids) > 1 or len(files) > 1:
        return False
    reported_file = case.get("file", "")
    if reported_file and not path_suffix_matches(reported_file, path):
        return False
    if files and not full_test_path_matches(next(iter(files)), path):
        return False
    if ids:
        test_path, separator, test_node = next(iter(ids)).partition("::")
        return (
            bool(separator)
            and full_test_path_matches(test_path, path)
            and (
                test_node == node
                or (test_node.startswith(node + "[") and test_node.endswith("]"))
            )
        )
    if not files and not full_test_path_matches(reported_file, path):
        return False
    parts = node.split("::")
    if len(parts) > 1:
        classname = ".".join(parts[:-1])
        reported_class = case.get("classname", "")
        if reported_class != classname and not reported_class.endswith("." + classname):
            return False
    # A reporter-appended VAL tag is metadata, not part of the test title. Other
    # prefixes/groups remain identity: a partial title must not match another test.
    actual = re.sub(
        r"(?<!\S)@VAL[-_]?\d+(?![\w])", "", case["name"], flags=re.IGNORECASE
    ).strip()
    expected = re.sub(
        r"(?<!\S)@VAL[-_]?\d+(?![\w])", "", parts[-1], flags=re.IGNORECASE
    ).strip()
    return actual == expected or (
        actual.startswith(expected + "[") and actual.endswith("]")
    )


def check_ci_results(
    document: ContractDocument, junit: list[Path], root: Path | None
) -> tuple[list[str], dict[str, str]]:
    """Delivered: every mechanical VAL-* must have passed in the CI-written results (#2).

    The spec's PASS is not trusted. Results must identify the exact contract and full
    planned test, plus its VAL ID (name/tag/property). A generic leaf name and VAL ID
    cannot be borrowed from another story or file.
    """
    errors: list[str] = []
    cases: list[dict[str, str]] = []
    for path in junit:
        resolved = path.resolve()
        if root is not None and resolved.is_relative_to(root.resolve()):
            errors.append(
                f"CI results {path} are inside the project tree, where a committed or "
                "stale file could stand in for a real run; write them outside the "
                "workspace (for example $RUNNER_TEMP)"
            )
            continue
        cases.extend(read_junit(resolved, errors))

    contract = document.section("Acceptance Contract")
    metadata = parse_bullets(document.direct_body(contract)) if contract else {}
    contract_id = metadata.get("contract id", "")
    if contains_placeholder(contract_id):
        return [*errors, "CI results cannot be attributed without a Contract ID"], {}
    scoped = [
        case
        for case in cases
        if contract_id.casefold()
        in {
            item.casefold()
            for item in re.split(r"[\s,;]+", case.get("contracts", ""))
            if item
        }
    ]
    recorded = extract_results(document, [])
    outcomes: dict[str, str] = {}
    for row in extract_validations(document, []).values():
        val = row.validation_id
        if row.method != "mechanical" or recorded.get(val) == "WAIVED":
            continue
        match = PLANNED_TEST_RE.match(row.planned_check.strip().strip("`").strip())
        if match is None:
            errors.append(
                f"{val} planned check is not a `path::test`, so CI results cannot "
                "verify it; plan it as path::test name or record an authorised waiver"
            )
            continue
        node = match["name"].strip()
        name = node.split("::")[-1]
        tag = val_tag_re(val)
        named = [
            case
            for case in scoped
            if testcase_identity_matches(case, match["path"], node)
        ]
        hits = [
            case
            for case in named
            if tag.search(case["name"]) or tag.search(case.get("vals", ""))
        ]
        statuses = {case["status"] for case in hits}
        if not hits and named:
            errors.append(
                f"{val} CI ran '{name}' but nothing ties the result to {val}: put "
                f"{val} in the test name or tag, or record a testcase property "
                f'named "val" with value {val}'
            )
            status = "untagged"
        elif not hits:
            errors.append(
                f"{val} has no CI result for '{name}' bound to contract {contract_id} "
                f"and test {match['path']}::{node}; CI did not run it or the report "
                "is missing/mismatching contract or full test identity"
            )
            status = "missing"
        elif "failed" in statuses:
            errors.append(f"{val} failed in CI ('{name}')")
            status = "failed"
        elif "skipped" in statuses:
            errors.append(f"{val} was skipped in CI ('{name}')")
            status = "skipped"
        else:
            status = "passed"
            if recorded.get(val) == "FAIL":
                errors.append(
                    f"{val} is recorded FAIL in Delivery Evidence but passed in CI; "
                    "Code Review must reconcile the record"
                )
        outcomes[val] = status
    return errors, outcomes


def check_assets(
    document: ContractDocument, root: Path | None, ci_passed: set[str] | None = None
) -> list[str]:
    """Delivered: planned tests exist and are not skipped; evidence files exist (#3).

    VALs that passed in CI results need no separate evidence file (CI is the proof).
    """
    if root is None:
        return [
            "cannot find the project root (no .jj or _bmad ancestor) to check evidence"
        ]
    errors: list[str] = []
    for validation_id, path, name in planned_tests(document):
        file = resolve_in_root(root, path)
        if file is None or not file.is_file():
            errors.append(f"{validation_id} planned test file is missing: {path}")
            continue
        text = file.read_text(encoding="utf-8")
        lines = text.splitlines()
        hits = [index for index, line in enumerate(lines) if name in line]
        if not hits:
            errors.append(f"{validation_id} planned test '{name}' not found in {path}")
        elif FILE_SKIP_RE.search(text) or any(
            is_skipped(lines, index) for index in hits
        ):
            errors.append(f"{validation_id} planned test '{name}' is skipped in {path}")

    section = document.section("Validation Results", parent="Delivery Evidence")
    if section is None:
        return errors
    rows = parse_table(
        document.body(section), ("VAL ID", "Result", "Evidence", "Build or run"), [], ""
    )
    for row in rows:
        if row["result"].upper() != "PASS" or row["val id"].upper() in (
            ci_passed or ()
        ):
            continue
        existing = 0
        for token in EVIDENCE_TOKEN_RE.findall(row["evidence"]):
            token = token.split("::")[0].rstrip(".:")
            if "://" in token or not ("/" in token or FILE_NAME_RE.fullmatch(token)):
                continue
            file = resolve_in_root(root, token)
            if file is not None and file.is_file():
                existing += 1
            else:
                errors.append(
                    f"{row['val id'].upper()} evidence references a missing file: {token}"
                )
        if not existing:
            errors.append(
                f"{row['val id'].upper()} PASS evidence must name at least one existing "
                "project file (output, log, report or observation record)"
            )
    return errors


def is_skipped(lines: list[str], index: int) -> bool:
    """Skip marker on the declaration, its decorators, or the first body lines."""
    window = [lines[index], *lines[index + 1 : index + 4]]
    above = index - 1
    while above >= 0 and lines[above].strip().startswith(("@", "#[")):
        window.append(lines[above])
        above -= 1
    return any(SKIP_MARK_RE.search(line) for line in window)


def check_review_record(document: ContractDocument) -> list[str]:
    """Delivered: an independent review session is recorded (#7)."""
    errors: list[str] = []
    section = document.section("Review Record", parent="Delivery Evidence")
    if section is None:
        return ["Delivery Evidence needs a '### Review Record' written by Code Review"]
    record = parse_bullets(document.direct_body(section))
    for field in ("reviewed by", "review session", "reviewed at"):
        if contains_placeholder(record.get(field, "")):
            errors.append(f"Review Record field is missing or pending: {field}")
    reviewed_at = record.get("reviewed at", "")
    approval = document.section("Contract Approval")
    approved_at = (
        parse_bullets(document.direct_body(approval)).get("approved at", "")
        if approval
        else ""
    )
    try:
        if datetime.strptime(reviewed_at, "%Y-%m-%dT%H:%M:%SZ") < datetime.strptime(
            approved_at, "%Y-%m-%dT%H:%M:%SZ"
        ):
            errors.append("Reviewed at is earlier than the contract's Approved at")
    except ValueError:
        if not contains_placeholder(reviewed_at):
            errors.append(
                "Reviewed at must be a valid UTC timestamp YYYY-MM-DDTHH:MM:SSZ"
            )

    notes = document.section("Implementation Notes")
    sessions = {
        match[1].casefold()
        for line in (visible_lines(document.body(notes)) if notes else [])
        if (match := SESSION_RE.match(line.strip()))
    }
    if not sessions:
        errors.append(
            "no '- Implementation session:' recorded under '## Implementation Notes'; "
            "review independence cannot be checked"
        )
    review_session = record.get("review session", "").split()[:1]
    if review_session:
        if len(review_session[0]) < 8:
            errors.append(
                "Review session must be a generated ID (at least 8 characters)"
            )
        if review_session[0].casefold() in sessions:
            errors.append(
                "Review session matches an implementation session: the work was "
                "reviewed by the session that wrote it"
            )
    return errors


def discover_specs(root: Path) -> list[Path]:
    """Story specs under root that carry an Acceptance Contract (outside fences)."""
    specs: list[Path] = []
    for directory, subdirs, files in os.walk(root):
        subdirs[:] = sorted(
            name for name in subdirs if name not in PRUNED_DIRS | {"_bmad"}
        )
        for name in sorted(files):
            path = Path(directory) / name
            if not name.endswith(".md"):
                continue
            try:
                if path.stat().st_size > 2_000_000:
                    continue
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeError):
                continue
            if "## Acceptance Contract" not in text:
                continue
            if ContractDocument.from_text(path, text).section("Acceptance Contract"):
                specs.append(path)
    return specs


def lifecycle_status(document: ContractDocument) -> str:
    """Read the top-level spec status, not a status hidden in an example or contract."""
    lines = document.lines
    if lines and lines[0].strip() == "---":
        closing = next(
            (i for i in range(1, len(lines)) if lines[i].strip() == "---"), None
        )
        if closing is None:
            return "ambiguous"
        prefix = lines[1:closing]
    else:
        contract = document.section("Acceptance Contract")
        prefix = visible_lines(lines[: contract.start] if contract else lines)
    statuses = []
    for line in prefix:
        match = re.match(r"^status\s*:\s*([^#\n]+)", line, re.IGNORECASE)
        if match:
            statuses.append(match[1].strip().strip("'\"").casefold().replace("_", "-"))
    if len(statuses) > 1:
        return "ambiguous"
    return statuses[0] if statuses else ""


def ci_phase(document: ContractDocument) -> str | None:
    """Completion claims cannot weaken CI by losing a reviewer name or whole record.

    Evidence-bearing or done/review specs require delivered validation, even if approval
    or review fields were deleted. Untouched drafts/history may still be skipped.
    """
    status = lifecycle_status(document)
    if status in {"done", "review", "in-review", "completed", "delivered", "ambiguous"}:
        return "delivered"
    review = document.section("Review Record", parent="Delivery Evidence")
    fields = parse_bullets(document.direct_body(review)) if review else {}
    if any(
        not contains_placeholder(fields.get(field, ""))
        for field in ("reviewed by", "review session", "reviewed at")
    ) or extract_results(document, []):
        return "delivered"
    if approval_status(document) in {"draft", "superseded"}:
        return None
    return "approved"  # missing/invalid approval is checked, never silently skipped


def run_ci(
    root: Path, junit: list[Path], *, require_jj: bool = False
) -> list[dict[str, object]]:
    """Validate every approved contract in the project at the phase CI must enforce."""
    reports: list[dict[str, object]] = []
    for spec in discover_specs(root):
        document = ContractDocument.load(spec)
        phase = ci_phase(document)
        relative = spec.relative_to(root).as_posix()
        if phase is None:
            reports.append({"story": relative, "phase": "skipped", "valid": True})
            continue
        errors, outcomes = run_validation(
            spec, phase, require_jj=require_jj, junit=junit
        )
        if phase == "delivered" and not junit:
            missing = (
                "delivered contract needs CI-written results: pass --junit with "
                "this run's JUnit reports"
            )
            errors = sorted({*errors, missing})
        report: dict[str, object] = {
            "story": relative,
            "phase": phase,
            "valid": not errors,
            "errors": errors,
        }
        if junit and phase == "delivered":
            report["ci_results"] = outcomes
        attach_guidance(report, errors)
        reports.append(report)
    return reports


PROTECTED_STATUSES = {"approved", "superseded"}
PRUNED_DIRS = {
    ".git", ".jj", "node_modules", ".venv", "venv", "dist", "build", "target",
    "__pycache__", ".next", ".ruff_cache", ".pytest_cache",
}  # fmt: skip


def approval_status(document: ContractDocument) -> str:
    section = document.section("Contract Approval")
    if section is None:
        return ""
    return parse_bullets(document.direct_body(section)).get("status", "").casefold()


def section_text(document: ContractDocument, title: str) -> str | None:
    section = document.section(title)
    if section is None:
        return None
    return "\n".join(document.lines[section.start : section.end]).rstrip()


def lock_owners(root: Path, relative: str) -> list[tuple[Path, str]]:
    """Approved specs under root that lock `relative`, with the locked digest."""
    owners: list[tuple[Path, str]] = []
    for directory, subdirs, files in os.walk(root):
        subdirs[:] = [name for name in subdirs if name not in PRUNED_DIRS]
        for name in files:
            if not name.endswith(".md"):
                continue
            path = Path(directory) / name
            try:
                if path.stat().st_size > 2_000_000:
                    continue
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeError):
                continue
            if "### Locked Tests" not in text or "## Contract Approval" not in text:
                continue
            document = ContractDocument.from_text(path, text)
            if approval_status(document) not in PROTECTED_STATUSES:
                continue
            digest = (read_locks(document, []) or {}).get(relative)
            if digest:
                owners.append((path.resolve(), digest))
    return owners


def guard_edit(target: Path, proposed: str | None) -> dict[str, object]:
    """Decide whether an agent may write `proposed` to `target` (#6).

    Protected: the Acceptance Contract and Contract Approval (incl. Locked Tests) of an
    approved spec, and every test file such a spec locks, except removing skip markers.
    `proposed` is None when the caller could not compute the result exactly; a protected
    target then fails closed. Delivery Evidence, notes and code stay writable.
    """
    target = target.resolve()
    reasons: list[str] = []
    specs: list[str] = []
    current = None
    if target.is_file() and target.suffix == ".md":
        try:
            current = target.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            current = None
    if current is not None and "## Acceptance Contract" in current:
        document = ContractDocument.from_text(target, current)
        if approval_status(document) in PROTECTED_STATUSES:
            specs.append(str(target))
            if proposed is None:
                reasons.append("edit could not be verified exactly")
            else:
                after = ContractDocument.from_text(target, proposed)
                for title in ("Acceptance Contract", "Contract Approval"):
                    if section_text(after, title) != section_text(document, title):
                        reasons.append(f"it changes the approved '{title}' section")
    root = find_project_root(target)
    if root is not None and target.is_relative_to(root.resolve()):
        relative = target.relative_to(root.resolve()).as_posix()
        for spec, digest in lock_owners(root, relative):
            if proposed is None:
                reasons.append(
                    f"edit to locked test could not be verified ({spec.name})"
                )
            elif lock_digest(proposed).casefold() != digest:
                reasons.append(
                    f"it changes a test locked by {spec.name} beyond removing skip markers"
                )
            specs.append(str(spec))
    return {
        "protected": bool(specs),
        "allowed": not reasons,
        "reason": "; ".join(dict.fromkeys(reasons)),
        "specs": list(dict.fromkeys(specs)),
    }


def run_validation(
    story: Path,
    phase: str,
    *,
    require_jj: bool = False,
    junit: list[Path] | None = None,
) -> tuple[list[str], dict[str, str]]:
    """Structural validation plus provenance checks; returns (errors, CI outcomes)."""
    document = ContractDocument.load(story)
    errors = set(validate(document, phase))
    outcomes: dict[str, str] = {}
    if phase in {"approved", "delivered"}:
        root = find_project_root(story)
        # Inside a jj workspace the approved version is pinned in history; no opt-out.
        errors |= set(check_jj_approval(document, require=require_jj))
        errors |= set(check_locks(document, root))
        if phase == "delivered":
            if junit:
                ci_errors, outcomes = check_ci_results(document, junit, root)
                errors |= set(ci_errors)
            passed = {val for val, status in outcomes.items() if status == "passed"}
            errors |= set(check_assets(document, root, passed))
            errors |= set(check_review_record(document))
    return sorted(errors), outcomes


def lock_table(story: Path, extra: list[str]) -> str:
    """Markdown '### Locked Tests' rows for the planned test files plus any extras."""
    document = ContractDocument.load(story)
    root = find_project_root(story)
    if root is None:
        raise ValueError("cannot find the project root (no .jj or _bmad ancestor)")
    paths = list(
        dict.fromkeys([path for _, path, _ in planned_tests(document)] + extra)
    )
    if not paths:
        raise ValueError("no planned `path::test` checks or --file paths to lock")
    rows = ["| Path | Lock digest |", "| --- | --- |"]
    for path in paths:
        file = resolve_in_root(root, path)
        if file is None or not file.is_file():
            raise ValueError(f"cannot lock missing file: {path}")
        rows.append(f"| {path} | {lock_digest(file.read_text(encoding='utf-8'))} |")
    return "\n".join(rows)


CONTRACT_MANUAL = "_bmad/custom/story-contract.md"
RECOVERY_GUIDANCE = (
    "Read the referenced full sections before choosing a correction. Before any exception, "
    "or if the situation is unlisted or instructions conflict, read the full "
    f"{CONTRACT_MANUAL} and ask the user or Vera if still unclear. "
    "Do not bypass the failed check."
)
# Presentation hints only: validation decisions and existing error strings stay unchanged.
ERROR_SECTIONS = (
    (
        (
            "locked test",
            "locked tests",
            "lock digest",
            "planned test file is not locked",
        ),
        ("locked-atdd-tests",),
    ),
    (
        (
            "review record",
            "review session",
            "reviewed at",
            "implementation session",
            "reviewed by",
        ),
        ("delivery-provenance",),
    ),
    (
        (
            "junit",
            "ci result",
            "ci ran",
            "ci did not",
            "ci-written",
            "failed in ci",
            "skipped in ci",
            "planned check is not a `path::test`",
            "must carry its",
            "nothing ties the result",
        ),
        ("ci-results",),
    ),
    (
        ("jj", "approval change", "digest", "changed after approval", "contract drift"),
        ("approval-change-jj", "lifecycle"),
    ),
    (
        (
            "evidence",
            "planned test",
            "delivery result",
            "waiver",
            "exception expired",
            "exception expiry",
            "is waived",
            "is not waived",
            "has an exception",
        ),
        ("delivery-provenance", "contract-rules"),
    ),
    (("guard", "could not be verified", "it changes the approved"), ("edit-guard-pi",)),
    (
        (
            "open questions",
            "has no validation obligation",
            "references missing criterion",
            "does not cover an ac",
        ),
        ("contract-rules", "lifecycle"),
    ),
    (
        (
            "missing required section",
            "missing '## acceptance contract'",
            "contract approval",
            "acceptance contract",
            "validation design",
            "criterion",
            "validation id",
            "sources",
            "risk must",
            "revision must",
            "duplicate",
            "malformed",
            "placeholder",
        ),
        ("required-spec-shape",),
    ),
)


def documentation_references(error: str) -> list[str]:
    """Best-effort section pointers; an unknown diagnostic points at the full manual."""
    lower = error.casefold()
    for terms, sections in ERROR_SECTIONS:
        if any(term in lower for term in terms):
            return [f"{CONTRACT_MANUAL}#{section}" for section in sections]
    return [CONTRACT_MANUAL]


def attach_guidance(payload: dict[str, object], errors: Iterable[str]) -> None:
    """Add recovery context without replacing or rewording the original diagnostics."""
    guidance = [
        {"error": error, "references": documentation_references(error)}
        for error in errors
    ]
    if guidance:
        payload["guidance"] = guidance
        payload["recovery"] = RECOVERY_GUIDANCE


def print_diagnostic(error: str) -> None:
    print(f"- {error}")
    print("  Read: " + ", ".join(documentation_references(error)))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    digest_parser = subparsers.add_parser(
        "digest", help="print the normative contract SHA-256 digest"
    )
    digest_parser.add_argument("story", type=Path)

    validate_parser = subparsers.add_parser(
        "validate", help="validate a story contract"
    )
    validate_parser.add_argument(
        "--phase", choices=("draft", "approved", "delivered"), required=True
    )
    validate_parser.add_argument("--json", action="store_true", dest="as_json")
    validate_parser.add_argument(
        "--require-jj",
        action="store_true",
        help="fail approved/delivered validation outside a jj workspace (use in CI)",
    )
    validate_parser.add_argument(
        "--junit",
        action="append",
        default=[],
        type=Path,
        help="CI-written JUnit XML results (delivered phase; repeatable)",
    )
    validate_parser.add_argument("story", type=Path)

    lock_parser = subparsers.add_parser(
        "lock", help="print the '### Locked Tests' table for the approved ATDD tests"
    )
    lock_parser.add_argument(
        "--file", action="append", default=[], help="extra project-relative test file"
    )
    lock_parser.add_argument("story", type=Path)

    ci_parser = subparsers.add_parser(
        "ci",
        help="validate every approved contract in the project (one CI step, any stack)",
    )
    ci_parser.add_argument(
        "--junit",
        action="append",
        default=[],
        type=Path,
        help="CI-written JUnit XML results from this run (repeat per report)",
    )
    ci_parser.add_argument("--require-jj", action="store_true")
    ci_parser.add_argument("--json", action="store_true", dest="as_json")
    ci_parser.add_argument(
        "--root", type=Path, default=None, help="project root (default: from cwd)"
    )

    guard_parser = subparsers.add_parser(
        "guard", help="JSON verdict on whether an agent may write a file (edit guard)"
    )
    guard_parser.add_argument(
        "--proposed",
        type=Path,
        help="file holding the content the write would produce (omit if unknown)",
    )
    guard_parser.add_argument("path", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "ci":
        root = args.root or find_project_root(Path.cwd() / "_")
        if root is None or not root.is_dir():
            print(
                "ERROR: cannot find the project root (no .jj or _bmad)", file=sys.stderr
            )
            print(f"Read: {CONTRACT_MANUAL}", file=sys.stderr)
            print(RECOVERY_GUIDANCE, file=sys.stderr)
            return 2
        reports = run_ci(root.resolve(), args.junit, require_jj=args.require_jj)
        failed = [report for report in reports if not report["valid"]]
        if args.as_json:
            print(json.dumps({"valid": not failed, "contracts": reports}, indent=2))
        else:
            for report in reports:
                state = "VALID" if report["valid"] else "INVALID"
                print(f"{state} {report['story']} ({report['phase']})")
                for error in report.get("errors", []):  # type: ignore[union-attr]
                    print_diagnostic(error)
            checked = sum(report["phase"] != "skipped" for report in reports)
            print(f"{checked} contract(s) checked, {len(failed)} invalid")
            if failed:
                print(RECOVERY_GUIDANCE)
        return 1 if failed else 0
    if args.command == "guard":
        try:
            proposed = (
                args.proposed.read_text(encoding="utf-8") if args.proposed else None
            )
        except (OSError, UnicodeError) as error:
            print(f"ERROR: cannot read proposed content: {error}", file=sys.stderr)
            print(f"Read: {CONTRACT_MANUAL}#edit-guard-pi", file=sys.stderr)
            print(RECOVERY_GUIDANCE, file=sys.stderr)
            return 2
        verdict = guard_edit(args.path, proposed)
        if not verdict["allowed"]:
            attach_guidance(verdict, [str(verdict["reason"])])
        print(json.dumps(verdict))
        return 0
    try:
        document = ContractDocument.load(args.story)
    except (OSError, UnicodeError) as error:
        print(f"ERROR: cannot read {args.story}: {error}", file=sys.stderr)
        print(f"Read: {CONTRACT_MANUAL}", file=sys.stderr)
        print(RECOVERY_GUIDANCE, file=sys.stderr)
        return 2

    if args.command in {"digest", "lock"}:
        try:
            print(
                contract_digest(document)
                if args.command == "digest"
                else lock_table(args.story, args.file)
            )
        except (ValueError, OSError, UnicodeError) as error:
            print(f"ERROR: {error}", file=sys.stderr)
            print(
                "Read: " + ", ".join(documentation_references(str(error))),
                file=sys.stderr,
            )
            print(RECOVERY_GUIDANCE, file=sys.stderr)
            return 1
        return 0

    errors, outcomes = run_validation(
        args.story, args.phase, require_jj=args.require_jj, junit=args.junit
    )
    payload: dict[str, object] = {
        "story": str(args.story),
        "phase": args.phase,
        "valid": not errors,
        "errors": errors,
    }
    attach_guidance(payload, errors)
    if args.junit:
        payload["ci_results"] = outcomes
    if args.as_json:
        print(json.dumps(payload, indent=2))
    elif errors:
        print(f"INVALID {args.story} ({args.phase})")
        for error in errors:
            print_diagnostic(error)
        print(RECOVERY_GUIDANCE)
    else:
        print(f"VALID {args.story} ({args.phase})")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
