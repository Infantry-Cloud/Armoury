"""One-off, idempotent jj wiring for BMAD customisation trees (shared base, overlays, installs).

Usage: python3 jj_wiring.py <custom-dir> [<project-context.md>]
Each edit is anchored on exact existing text; a missing anchor fails loudly before any write.
"""

from __future__ import annotations

import sys
from pathlib import Path

import tomllib

# Literal persistent facts defer manuals until the relevant operation, instead of
# file: entries which load the entire manual on every activation.
PROCEDURE_FACTS = {
    "jj-vcs.md": (
        "Before any version-control command, stage write or closure recommendation, "
        "read {project-root}/_bmad/custom/jj-vcs.md completely; defer until work needs it."
    ),
    "story-contract.md": (
        "Before contract planning, approval, independent test design/review or revision, "
        "read {project-root}/_bmad/custom/story-contract.md completely. For approved "
        "implementation and its checks only, read "
        "{project-root}/_bmad/custom/instructions/implementation.md first and follow "
        "its freshness check, stop conditions and full-manual fallback. Defer until "
        "a contract is in scope."
    ),
    "linear-workflow.md": (
        "Before Linear kickoff, activation, publication, status changes or reconciliation, "
        "read {project-root}/_bmad/custom/linear-workflow.md completely; defer until "
        "the project and target are known."
    ),
    "agent-readiness-workflow.md": (
        "Before running or redesigning Agent Readiness, read "
        "{project-root}/_bmad/custom/agent-readiness-workflow.md completely; "
        "a general health scan alone does not require the full recipe."
    ),
}
LEGACY_JJ_FACT = '  "file:{project-root}/_bmad/custom/jj-vcs.md",\n'
JJ_FACT = '  "' + PROCEDURE_FACTS["jj-vcs.md"] + '",\n'
FACT_ANCHORS = (
    '  "file:{project-root}/project-context.md",\n',
    '  "file:{project-root}/_bmad/custom/story-contract.md",\n',
)
FACT_ONLY = (
    "bmad-testarch-automate.toml",
    "bmad-testarch-test-review.toml",
    "bmad-testarch-test-design.toml",
    "bmad-testarch-ci.toml",
    "bmad-testarch-framework.toml",
    "bmad-qa-generate-e2e-tests.toml",
    "bmad-sprint-planning.toml",
    "bmad-retrospective.toml",
    # Planning workflows and personas write artifacts too: one described change per stage.
    "bmad-product-brief.toml",
    "bmad-prfaq.toml",
    "bmad-prd.toml",
    "bmad-ux.toml",
    "bmad-architecture.toml",
    "bmad-spec.toml",
    "bmad-brainstorming.toml",
    "bmad-deep-recon.toml",
    "bmad-create-epics-and-stories.toml",
    "bmad-project-context.toml",
    "bmad-ticket.toml",
    "bmad-agent-analyst.toml",
    "bmad-agent-pm.toml",
    "bmad-agent-architect.toml",
    "bmad-tea.toml",
)

BUILD_STEP = (
    "JJ STAGES (team policy; follow jj-vcs.md). Never run git. Once routing resolves and before Step 2 "
    "writes the spec, prepare the planning stage change (for tracked stories `docs(story-<epic>.<story>): ...`) "
    "unless genuinely resuming it. At Step 3, only after approved-phase contract validation passes and before "
    "capturing baseline_commit or changing tests/code, start the separate implementation stage change, then record "
    "baseline_commit as the full commit id of `@-`; keep an existing baseline only when genuinely resuming that "
    "implementation stage. Build every diff with `jj diff --git --from <baseline_commit> --to @`. Unknown "
    "`changed undescribed` work, a missing jj workspace or an ambiguous stage identity halts and asks the user."
)
BUILD_AUTO_STEP = (
    "JJ STAGES (team policy; follow jj-vcs.md). Never run git. Run `jj st` first: failure HALTs `blocked` with "
    "`version-control metadata not writable`; no jj workspace HALTs `blocked` with `jj workspace unavailable`; "
    "`changed undescribed` HALTs `blocked` with `undescribed changes in jj working copy`. Prepare the planning stage "
    "change before writing the spec. Only after approved-phase contract validation passes, start the separate "
    "implementation stage change, record baseline_commit as the full commit id of `@-`, and build every diff with "
    "`jj diff --git --from <baseline_commit> --to @`. Resume an existing stage only after verifying its identity."
)
# Superseded wording, replaced in place so re-running the wiring upgrades older trees.
ATDD_STEP_V1 = (
    "JJ STAGE (team policy; follow jj-vcs.md). Never run git. Red-phase scaffolds, the atdd-checklist and any "
    "explicitly approved contract/approval edits get their own `test(story-<epic>.<story>): add acceptance tests` "
    "change, prepared immediately before the first write. When the run finishes, finalise that description as one "
    "`-m` holding the subject, a blank line and 2-6 `- ` bullets naming the test files and checklist."
)
ATDD_STEP = (
    "JJ STAGE (team policy; follow jj-vcs.md). Never run git. Red-phase scaffolds, the atdd-checklist and any "
    "draft-contract edits the user explicitly approves get their own `test(story-<epic>.<story>): add acceptance "
    "tests` change, prepared immediately before the first write. Finalise it before approval: one `-m` holding the "
    "subject, a blank line and 2-6 `- ` bullets naming the test files and checklist. The approval is never part of "
    "this change; it is the separate JJ APPROVAL change."
)
APPROVAL_STEP = (
    "JJ APPROVAL (team policy; follow story-contract.md 'Approval change (jj)'). Only after explicit product "
    "approval and a passing Test Architect review in this session: run `jj new`, edit only the spec's Contract "
    "Approval fields (Status approved, approvers, UTC Approved at, digest from the validator `digest` command, "
    "Validation artifacts), describe that change with exactly the trailers story-contract.md lists, run `jj new` to "
    "seal it, then run approved-phase validation, which verifies the sealed change. Never create an approval change "
    "without explicit approval, never put tests or other files in it, and never describe, rewrite or replace an "
    "existing approval change."
)
BUILD_APPROVAL_STEP = (
    "JJ APPROVAL (untracked micro-contracts; follow story-contract.md 'Approval change (jj)'). After the user's "
    "explicit CHECKPOINT 1 approval, record the approval fields as their own sealed approval change with the listed "
    "trailers (only the spec changed, then `jj new`), and pass approved-phase validation before the implementation "
    "stage starts. Tracked stories are approved in ATDD, never here."
)
BUILD_AUTO_APPROVAL_STEP = (
    "JJ APPROVAL (team policy). Unattended runs never create or edit an approval change. A missing, ambiguous or "
    "mismatched jj approval change reported by approved-phase validation HALTs `blocked` with `contract approval "
    "required` (or `contract drift` when the contract differs from the sealed approved version)."
)
REVIEW_APPROVAL_STEP = (
    "JJ APPROVAL CHECK (team policy). Approved- and delivered-phase validation verify the contract against its "
    "sealed jj approval change. A failure is a blocking Correct Course finding: never fix it by editing approval "
    "fields, digests or trailers, or by creating a new approval change during review."
)
CORRECT_COURSE_STEP = (
    "JJ REVISION (team policy; follow jj-vcs.md and story-contract.md). Never run git. Any edit inside the "
    "Acceptance Contract, even editorial, changes its digest, so it needs a new Revision. Make the revision its own "
    "`docs(story-<epic>.<story>): revise acceptance contract r<N>` change. Never describe, rewrite or replace an "
    "earlier approval change; the new revision is approved only by a new sealed approval change with "
    "`Contract-Revision: <N>`, recorded after product and Test Architect reapproval."
)
TRACE_STEP = (
    "JJ (team policy; follow jj-vcs.md). Never run git; trace is read-only. Delivered-phase validation verifies the "
    "sealed jj approval change; in a jj project run it with `--require-jj`. A missing, ambiguous or mismatched "
    "approval change is FAIL, never a waiver candidate."
)
AR_ANCHOR = "project-context.md describes.\n"
AR_SENTENCE = (
    "In jj projects, run the CI validation with `--require-jj` so a missing, ambiguous or mismatched approval\n"
    "change fails the gate (see story-contract.md 'Approval change (jj)').\n"
)
REVIEW_STEP = (
    "JJ REVIEW (team policy; follow jj-vcs.md). Never run git. For a tracked story, review the full verified story "
    "range from jj-vcs.md (planning, ATDD, implementation and review fixes), not only the implementation diff from "
    "baseline_commit; record that range without rewriting the spec's baseline. Before the first fix, review artifact, "
    "Delivery Evidence or status write, prepare the review/closure stage change. Rerun checks after the last patch "
    "and review any review-time fixes."
)
DEV_PRINCIPLE = (
    "jj, never git — follow _bmad/custom/jj-vcs.md: each stage gets its own change via `jj new` and "
    "`jj describe`; bookmarks, history edits and pushes stay with the user."
)
BUILD_COMPLETE = (
    " Finally, if this run wrote files, finalise the current stage's jj description with the full Conventional "
    "Commits message as one `-m` argument; do not end with a fenced commit message, run no other mutating VCS "
    "command, and never recommend a bookmark (only bmad-code-review may, after closure)."
)
REVIEW_COMPLETE = (
    " If, and only if, every jj-vcs.md closure item passes after delivered-phase validation, finalise the review "
    "change description and show the bookmark recommendation exactly as jj-vcs.md describes, for the user to run "
    "manually; otherwise state that the story is not closed and recommend no bookmark. Never run bookmark or push commands."
)
CONTEXT_SECTION_V1 = """## Version control (jj)

Projects using these customisations use Jujutsu (jj), never git, for agent version-control work.
Follow `_bmad/custom/jj-vcs.md`: agents may run only `jj new` and `jj describe` to give each stage
(planning, ATDD, implementation, review) its own described change; bookmarks, pushes and history
edits stay with the user. If the workspace is not a jj workspace, stop and ask rather than falling
back to git or initialising jj.

"""
CONTEXT_SECTION = """## Version control (jj)

Projects using these customisations use Jujutsu (jj), never git, for agent version-control work.
Follow `_bmad/custom/jj-vcs.md`: agents may run only `jj new` and `jj describe` to give each stage
(planning, ATDD, implementation, review) its own described change; bookmarks, pushes and history
edits stay with the user. If the workspace is not a jj workspace, stop and ask rather than falling
back to git or initialising jj. A story contract's approval is its own sealed jj change, and the
validator checks the contract against that recorded version (story-contract.md, "Approval change (jj)").

"""
WALKTHROUGH = (
    "# Team override for bmad-walkthrough: inspect changes with jj, never git.\n"
    "[workflow]\npersistent_facts = [\n"
    '  "file:{project-root}/project-context.md",\n' + JJ_FACT + "]\n"
)


def add_fact(text: str) -> str:
    if JJ_FACT in text:
        return text
    if LEGACY_JJ_FACT in text:
        return text.replace(LEGACY_JJ_FACT, JJ_FACT, 1)
    for anchor in FACT_ANCHORS:
        if text.count(anchor) == 1:
            return text.replace(anchor, anchor + JJ_FACT, 1)
    raise ValueError("no unique persistent_facts anchor")


def append_step(text: str, key: str, step: str) -> str:
    if step in text:
        return text
    marker = f"{key} = [\n"
    if text.count(marker) != 1:
        raise ValueError(f"no unique {key} array")
    start = text.index(marker)
    end = text.index("\n]\n", start)
    return text[:end] + "\n  " + _quote(step) + "," + text[end:]


def append_on_complete(text: str, sentence: str) -> str:
    if sentence.strip() in text:
        return text
    lines = text.splitlines(keepends=True)
    matches = [i for i, line in enumerate(lines) if line.startswith('on_complete = "')]
    if len(matches) != 1 or not lines[matches[0]].rstrip("\n").endswith('"'):
        raise ValueError("no single-line on_complete")
    i = matches[0]
    lines[i] = lines[i].rstrip("\n")[:-1] + sentence.replace('"', '\\"') + '"\n'
    return "".join(lines)


def upgrade(old: str, new: str):
    """Replace superseded wording once; a no-op when the new wording is already present."""

    def step(text: str) -> str:
        if new in text or old not in text:
            return text
        return text.replace(old, new, 1)

    return step


def _quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def wire(custom: Path, context: Path | None) -> list[Path]:
    edits: dict[Path, str] = {}

    def edit(name: str, *steps) -> None:
        path = custom / name
        if not path.is_file():
            return
        text = path.read_text()
        for step in steps:
            text = step(text)
        tomllib.loads(text)
        edits[path] = text

    for name in FACT_ONLY:
        edit(name, add_fact)
    edit(
        "bmad-build.toml",
        add_fact,
        lambda t: append_step(t, "activation_steps_append", BUILD_STEP),
        lambda t: append_step(t, "activation_steps_append", BUILD_APPROVAL_STEP),
        lambda t: append_on_complete(t, BUILD_COMPLETE),
    )
    edit(
        "bmad-build-auto.toml",
        add_fact,
        lambda t: append_step(t, "activation_steps_append", BUILD_AUTO_STEP),
        lambda t: append_step(t, "activation_steps_append", BUILD_AUTO_APPROVAL_STEP),
        lambda t: append_on_complete(t, BUILD_COMPLETE),
    )
    edit(
        "bmad-testarch-atdd.toml",
        add_fact,
        upgrade(_quote(ATDD_STEP_V1), _quote(ATDD_STEP)),
        lambda t: append_step(t, "activation_steps_append", ATDD_STEP),
        lambda t: append_step(t, "activation_steps_append", APPROVAL_STEP),
    )
    edit(
        "bmad-code-review.toml",
        add_fact,
        lambda t: t.replace(
            "with the implementation baseline and git changes",
            "with the implementation baseline and the story's jj changes",
        ),
        lambda t: append_step(t, "activation_steps_append", REVIEW_STEP),
        lambda t: append_step(t, "activation_steps_append", REVIEW_APPROVAL_STEP),
        lambda t: append_on_complete(t, REVIEW_COMPLETE),
    )
    edit(
        "bmad-correct-course.toml",
        add_fact,
        lambda t: append_step(t, "activation_steps_append", CORRECT_COURSE_STEP),
    )
    edit(
        "bmad-testarch-trace.toml",
        add_fact,
        lambda t: append_step(t, "activation_steps_append", TRACE_STEP),
    )
    edit(
        "bmad-agent-dev.toml",
        add_fact,
        lambda t: append_step(t, "principles", DEV_PRINCIPLE),
    )

    walkthrough = custom / "bmad-walkthrough.toml"
    if walkthrough.exists() and "jj-vcs.md" not in walkthrough.read_text():
        raise ValueError(f"{walkthrough} exists without jj wiring; merge manually")
    # Base trees/installs only (they carry story-contract.md); overlays inherit it from the base.
    if (custom / "story-contract.md").exists() and not walkthrough.exists():
        edits[walkthrough] = WALKTHROUGH

    readiness = custom / "agent-readiness-workflow.md"
    if readiness.is_file():
        text = readiness.read_text()
        if AR_SENTENCE not in text:
            if text.count(AR_ANCHOR) != 1:
                raise ValueError(f"{readiness}: no unique validator-wiring anchor")
            edits[readiness] = text.replace(AR_ANCHOR, AR_ANCHOR + AR_SENTENCE, 1)

    if context is not None and context.is_file():
        text = upgrade(CONTEXT_SECTION_V1, CONTEXT_SECTION)(context.read_text())
        edits[context] = text
        if "## Version control (jj)" not in text:
            anchor = "## Methodology & structure"
            if text.count(anchor) != 1:
                raise ValueError(f"{context}: no unique methodology heading")
            text = text.replace(anchor, CONTEXT_SECTION + anchor, 1)
            edits[context] = text

    changed = [
        path
        for path, text in edits.items()
        if not path.exists() or path.read_text() != text
    ]
    for path in changed:
        path.write_text(edits[path])
    return changed


if __name__ == "__main__":
    custom_dir = Path(sys.argv[1])
    context_file = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    for path in wire(custom_dir, context_file):
        print(f"wired {path}")
