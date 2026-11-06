# BMad Story Acceptance Contract Standard

<!-- markdownlint-disable MD013 -->

Every tracked BMad story has one authoritative work contract. Do not create a competing sidecar
specification. Since BMad 6.11, `bmad-build` is the only implementation workflow, so the contract
lives in the story's **Build spec**:

- interactive Build: `{implementation_artifacts}/spec-<story_key>.md` (for example
  `spec-1-2-user-auth.md`), or `{spec_folder}/stories/<story_id>-<slug>.md` for spec-folder stories;
- Build Auto (unattended): the spec file it writes or receives.

The spec's `Acceptance Contract` section is normative. `Contract Approval` and `Delivery Evidence`
are governance and evidence records.

## Required spec shape

Put `## Acceptance Contract` **inside** Build's frozen block (`<frozen-after-approval>` in Build,
`<intent-contract>` in Build Auto), so Build's human-owned lock and the validator digest protect the
same text. The contract replaces the template's frozen `## Intent`, `## Boundaries & Constraints` and
`## I/O & Edge-Case Matrix` sections:

| Build template section | Contract location |
| --- | --- |
| `## Intent` (Problem / Approach) | `### Intent` |
| `## Boundaries & Constraints` (Always / Never) | `### Scope` (in/out) plus optional `### Boundaries & Constraints` |
| `## I/O & Edge-Case Matrix` | optional `### I/O & Edge-Case Matrix`; rows cite the `AC-*` they exercise |
| `## Open Questions` (intent gaps) | `### Open Questions`; exactly `- None.` once every gap is answered, never deleted |
| Acceptance Criteria in `## Tasks & Acceptance` | `### Acceptance Criteria`; Tasks list execution steps citing `AC-*`/`VAL-*`, never restated criteria |

After the frozen block keep Build's sections (`## Code Map`, `## Tasks & Acceptance`,
`## Implementation Notes`, `## Spec Change Log`, `## Review Triage Log`, `## Verification`, …) and add
`## Contract Approval` and `## Delivery Evidence`. List
`{project-root}/_bmad/custom/instructions/implementation.md` and `{project-root}/project-context.md`
in the spec's frontmatter `context:` so the implementation subagent loads the generated developer
instructions and their full-manual fallback. Planning and approval still use this full standard. Contract IDs are `STORY-<epic>.<story>` for tracked stories and
`SPEC-<slug>` for untracked micro-contracts.

Use these headings and field names exactly so agents and the validator can consume the contract:

```markdown
## Acceptance Contract

- Contract ID: STORY-1.2
- Revision: 1
- Risk: medium

### Intent

State the externally observable product or engineering outcome and why it matters.

### Scope

- In scope: ...
- Out of scope: ...

### Sources

- [Source: path/to/prd.md#Requirement]
- [Source: path/to/architecture.md#Decision]

### Assumptions and Dependencies

- Assumption or dependency, or `None.`

### Acceptance Criteria

- AC-1 [P0]: Given ..., when ..., then ...
- AC-2 [P1]: Given ..., when ..., then ...

### Validation Design

| VAL ID | Covers | Method | Level | Planned check or procedure | Expected evidence | Owner | Manual reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| VAL-1 | AC-1 | mechanical | API | `tests/api/test_profile.py::test_val_1_save` (preferred) or the exact command | Observable pass condition and retained output | Dev | - |
| VAL-2 | AC-2 | manual | demonstration | Exact steps the reviewer performs | Screenshot, log, or observation record | Test Architect | Automation would not credibly assess this behavior |

### Open Questions

- None.

### Change Control

After approval, any change to intent, scope, sources, assumptions, acceptance criteria, validation
oracles, risk, or required evidence creates a new revision and requires product and validation
reapproval. A validation-mechanism-only refinement with an unchanged oracle requires Test Architect
approval and rerunning affected checks. Never weaken the contract to match an implementation.

## Contract Approval

- Status: draft
- Approved by: pending
- Validation approved by: pending
- Approved at: pending
- Contract digest: pending
- Validation artifacts: pending

### Locked Tests

| Path | Lock digest |
| --- | --- |

## Delivery Evidence

### Validation Results

| VAL ID | Result | Evidence | Build or run |
| --- | --- | --- | --- |

### Exceptions

| VAL ID | Reason | Owner | Expires |
| --- | --- | --- | --- |

### Review Record

- Reviewed by: pending
- Review session: pending
- Reviewed at: pending
```

Write each mechanical planned check as `path/to/file.ext::test name` whenever the test is known. That
form is what the validator can lock and check for existence at delivery; an exact command cannot be
verified that way. Build adds `- Implementation session: <id>` lines under `## Implementation Notes`.

## Contract rules

1. **One source of truth.** The Build spec's contract is the story contract. TEA outputs, tests and
   reports support it and link back by `AC-*`, `VAL-*`, contract revision and digest.
2. **Stable identities.** Acceptance criteria use unique `AC-<number>` IDs. Validation obligations
   use unique `VAL-<number>` IDs. Never renumber an approved revision; supersede it.
3. **Observable acceptance.** Criteria describe behavior, invariants or inspectable artifacts, not
   internal implementation. Use concrete positive, negative, boundary and failure examples when the
   risk warrants them.
4. **Validation before implementation.** Every AC maps to at least one validation obligation before
   approval. Every validation maps back to one or more ACs.
5. **Cheapest trustworthy level.** Prefer fast, narrow checks. Valid levels include unit, component,
   API, boundary-contract, integration, E2E, inspection, analysis and demonstration. Do not create an
   E2E test for every AC.
6. **Honest manual assurance.** Manual checks are valid when automation is disproportionate or
   untrustworthy, but require an exact procedure, expected evidence, owner and reason.
7. **No unresolved approval.** Material open questions, placeholders, unknown dependencies or missing
   oracles block approval.
8. **Independent validation.** Product/user approval owns intent and scope. The Test Architect owns
   validation design and residual manual assurance. The developer owns implementation and test assets
   but cannot unilaterally change normative behavior. Code Review is the sole writer of final Delivery
   Evidence in the story; other test workflows return reports/evidence candidates for it to verify.
9. **Exact baseline.** Approval records the SHA-256 digest emitted by the validator for the complete
   `Acceptance Contract` section. Normative edits invalidate approval. Evidence outside that section
   does not alter the digest.
10. **Evidence, not assertion.** Completion requires a `PASS` or explicit `WAIVED` result for every
    `VAL-*`, tied to a commit, build or CI run. A waiver requires reason, owner and expiry.
11. **Risk proportionality.** Every story follows the contract lifecycle, but the quantity and level
    of validation scale with risk. Chores and documentation may use inspection or analysis rather than
    fabricated executable tests.
12. **No silent bypass.** Tracked stories never take Build's oneshot route. Untracked, non-trivial
    behavioral work uses Build's dispatch route with a proportional micro-contract in the same shape.
    Only genuinely untracked, zero-blast-radius trivial work may take the stock oneshot route, keeping
    its concise intent/review trace and one runnable check; it must switch to the dispatch route if
    scope or risk stops being trivial. Unattended Build Auto cannot obtain approval, so it halts
    `blocked` instead of implementing an unapproved contract.
13. **TEA is required.** The independent Test Architect role is the BMad TEA module (`bmad-tea`,
    `bmad-testarch-*`). Without it, tracked-story contracts cannot be approved or reviewed, and work
    stays blocked rather than silently downgrading the lifecycle.

## Lifecycle

1. **Plan — `bmad-build` (planning, CHECKPOINT 1).** Build writes the draft contract and initial
   validation design into the frozen block and runs draft validation. For a tracked story, Build's
   checkpoint approval is a product review of the draft that sets Build status `ready-for-dev`; it is
   *not* contract approval. Choose **Approve and stop**.
2. **Validate — TEA Test Design (optional, system/epic) and TEA ATDD (`bmad-testarch-atdd`).** ATDD
   consumes the Build spec while its contract is draft, challenges risks and oracles, generates or
   identifies red-phase checks and links them in `Validation artifacts`. Because Build has frozen the
   block, edits to it need the user's explicit approval in that session.
3. **Approve.** The product owner/user and the Test Architect approve the exact revision; record
   both, the UTC time, the validator digest and the artifacts, then set Status `approved` (normally
   at the end of ATDD). In a jj workspace this is its own sealed approval change; see
   **Approval change (jj)**.
4. **Implement — `bmad-build` (resume with the spec path).** Before Build captures its baseline,
   approved-phase validation must pass. The implementation subagent follows the developer rules
   below. Build's own review runs, then Build marks the spec `done` and moves sprint status to
   `review`: implementation is ready for independent review, not yet delivered.
5. **Test Review — `bmad-testarch-test-review` (risk-based).** For medium/high/critical-risk or
   test-sensitive contracts, independently audit tests and return a report; it does not edit the
   contract or the final evidence ledger.
6. **Code Review — `bmad-code-review`.** It independently reruns checks, performs residual manual
   assurance, writes the final Delivery Evidence, runs delivered validation, and only then allows the
   sprint `done` transition. Otherwise the spec returns to `in-progress` and Build resumes there.
7. **Trace — `bmad-testarch-trace` (risk/release gate).** For high-risk stories, epics and releases,
   map `AC -> VAL -> test/check -> result` and issue PASS, CONCERNS, FAIL or explicit time-bounded
   WAIVED.

**Untracked micro-contracts** skip steps 2–3 and 5: the user's explicit approval at Build's
CHECKPOINT 1 is their approval (Approved by = that user; Validation approved by = `Build plan review
approved by <user>`; Validation artifacts = the spec path; digest and UTC time recorded, as its own
sealed approval change in a jj workspace). They still finish through Code Review, which writes their
Delivery Evidence.

**Semantic changes** after approval go through `bmad-correct-course`: increment Revision, reset
Contract Approval to draft, clear the digest, mark invalidated evidence, and set the Build spec status
to `draft` so Build re-plans (preserving Implementation Notes, Spec Change Log and Review Triage Log)
before TEA reapproval. Any edit inside the Acceptance Contract, even editorial, changes its digest,
so it needs a new Revision and a new approval change; never edit or replace an earlier approval change.

## Approval change (jj)

In a jj workspace the approval is its own sealed jj change, and the validator compares the contract
with the version stored in that change instead of trusting the digest field alone. After explicit
product approval and a passing Test Architect review:

1. Run `jj new`, then edit only the spec's `## Contract Approval` fields (Status `approved`, approvers,
   UTC `Approved at`, the validator's `digest` output, Validation artifacts) and its `### Locked Tests`
   table (the validator's `lock` output). Change no other file.
2. Describe that change with these trailers, one per line, values matching the spec exactly.
   `Contract-Spec` is the spec path relative to the workspace root.

   ```text
   chore(story-1.2): approve acceptance contract r1

   Contract-ID: STORY-1.2
   Contract-Revision: 1
   Contract-Spec: _bmad-output/implementation-artifacts/spec-1-2-user-auth.md
   Contract-Digest: sha256:<validator digest output>
   Approved-by: <product approver, as in the spec>
   Validation-approved-by: <Test Architect approver, as in the spec>
   ```

3. Run `jj new` to seal it. The approval change must be an ancestor of the working-copy parent (`::@-`).

Approved- and delivered-phase validation then require exactly one sealed approval change for the
contract ID, spec path and current Revision. It must change only the spec, its `Contract-Digest` must
match the contract text it records, it must record Status `approved` with the same approvers as the
trailers, and the current contract must be identical to that approved version. Editing the contract
and recomputing the digest therefore fails, as does approving inside the still-open working copy. A
new Revision needs its own approval change. The `### Locked Tests` table must equal the one in the
approval change, and each lock digest must match that test file as it existed at the approval change,
so locks can neither be fabricated at approval nor refreshed afterwards.

Outside a jj workspace the validator falls back to the digest field alone. CI in a jj project passes
`--require-jj`, so that fallback can never satisfy the gate there.

This pins *what* was approved, not *who* approved it: an agent can run `jj describe`, so the trailers
are a record, not authentication. Prove the approver with signed approval changes or a protected,
human-reviewed merge.

## Locked ATDD tests

Approval also locks the acceptance tests ATDD produced, so they cannot be quietly weakened later.

- When recording approval, run the validator's `lock` command and paste its table under
  `### Locked Tests`. It locks every file named by a mechanical `path::test` planned check; add
  other approved test files with `--file <path>`.
- A lock digest is the SHA-256 of the file with **skip markers ignored**, so removing the red-phase
  `skip`/`fixme` markers to activate a scaffold is allowed. Any other edit (an assertion, test data,
  a deleted test) fails approved- and delivered-phase validation.
- Changing a locked test therefore needs Correct Course: a new Revision, Test Architect reapproval
  (plus product reapproval when the oracle or behaviour changes), and a new approval change with
  re-locked tests.
- Tracked stories (`STORY-*`) must lock every planned `path::test` file. Untracked micro-contracts
  (`SPEC-*`) may use `- None.` when they have no ATDD tests.

Limits: skip-marker handling is a pattern list for common frameworks (pytest, unittest, Playwright,
Jest/Vitest/Mocha, Go, JUnit, Rust `#[ignore]` on its own line), so an unusual marker may need
reapproval to remove. Fixtures and
helpers outside the locked files are not covered; add them with `--file` if they define the oracle.
Outside a jj workspace the lock table itself could be rewritten together with the tests.

## Delivery provenance

Delivered-phase validation also checks the project tree, not just the spec text:

1. **Planned tests exist and run.** Every mechanical `path::test` planned check must name an
   existing file that contains the test, with no skip marker on it, its decorators, or the file.
2. **Evidence exists.** Every `PASS` result must name at least one existing project file (test
   output, log, report or observation record). Every file-like path in the cell must exist. URLs
   are not accepted as evidence on their own. A mechanical check that passed in the CI results
   (see **CI results**) needs no separate file: the CI run is its evidence.
3. **Independent review.** Build records `- Implementation session: <id>` under
   `## Implementation Notes` for each agent session that implements (one generated ID per session).
   Code Review generates its own ID and records `### Review Record` with `Reviewed by`, `Review
   session` and a UTC `Reviewed at` no earlier than `Approved at`. The review session must not
   match any implementation session.

Limits: these prove files exist and catch same-session self-review; they do not prove a test passed
or who a reviewer was. Skip detection is a heuristic, so real test results (see **CI results**)
remain the proof of execution, and an independent reviewer remains the proof of review.

## CI results

For mechanical checks, a `PASS` typed into Delivery Evidence proves nothing. The project's CI runs
the tests, writes a JUnit XML report, and delivered-phase validation reads that report instead. The CI
provider (Dagger, GitHub Actions, GitLab CI or other) is a per-project decision recorded in Agent
Readiness; the contract step is the same for every provider:

```bash
# In the CI job that ran the tests (results written outside the workspace, e.g. $RUNNER_TEMP
# or the provider's equivalent). The same command previews it locally.
# The test commands are the project's choice; the last step is the same for every stack.
pytest --junitxml="$RUNNER_TEMP/api.xml"
npx playwright test --reporter=junit   # PLAYWRIGHT_JUNIT_OUTPUT_FILE="$RUNNER_TEMP/e2e.xml"
uv run _bmad/custom/scripts/validate_story_contract.py ci --require-jj \
  --junit "$RUNNER_TEMP/api.xml" --junit "$RUNNER_TEMP/e2e.xml"
```

`ci` finds every spec with an Acceptance Contract outside `_bmad/` and chooses the strongest
phase its current state requires:

| Spec state | CI validation |
| --- | --- |
| Draft or superseded, with no completion claim or delivery evidence | Skipped |
| Approved, still in planning/implementation, with no delivery evidence | Approved |
| Status `done`, `review`, `in-review`, `completed` or `delivered`; any completed review field; or any delivery result row | Delivered, even when review or approval fields are missing |
| Missing/invalid approval on an otherwise uncompleted spec | Approved, which reports the invalid approval rather than skipping it |

Deleting a reviewer name, the whole Review Record or result rows cannot downgrade a completed
spec. A delivered check without `--junit` fails. Build may set its spec to `done` before independent
review; CI then stays incomplete until Code Review records actual delivery evidence and its review
record, and reruns the gate. Do not lower status or erase evidence to turn it green.
`validate --phase delivered --junit ...` checks a single spec.

Agent Readiness records how each project does this (the **Contract CI Wiring** table in
`docs/agent-readiness.md`); `bmad-testarch-framework` and `bmad-testarch-ci` build it.

- **Give every acceptance test its check ID.** A mechanical planned check is `path::test name`.
  The VAL ID (any common form: `VAL-1`, `VAL_1`, `val_1`) is carried by **any** of:
  - the test name: `tests/api/test_profile.py::test_val_1_save`;
  - a tag the reporter appends to the name: Playwright `test('saves profile', { tag: '@VAL-1' }, ...)`
    (keep `omitTags` off);
  - a testcase property named `val` (also `val_id`, `validation`), which may list several IDs:
    pytest `record_property("val", "VAL-1")`, or a converter's `<property name="val" value="VAL-1"/>`.
    Suite-level properties do not count.

  A command-only planned check cannot be verified from results; plan it as a test, or record an
  authorised waiver. Checks that are not tests (security scans, contract verification) can emit
  JUnit through a small converter that writes one testcase per check with the `val` property.
- **Bind each result to its contract and full test identity.** VAL IDs repeat between stories;
  a generic name plus `VAL-1` is not enough. Every matching testcase must satisfy all four:

  | Field | Required match |
  | --- | --- |
  | Contract | Testcase property `contract` (aliases `contract-id`, `contract_id`) names the exact Contract ID; suite-level properties do not count |
  | Full test | Project-relative file path plus planned test name/class, or a testcase `test-id` property equal to `path::Class::test` / `path::test` |
  | VAL | Its name, appended tag or `val` property carries the required VAL ID |
  | Result | Every matching testcase passes; any failure, error or skip fails delivery |

  For example:

  ```xml
  <testcase name="test_val_1_save" file="tests/api/test_profile.py">
    <properties><property name="contract" value="STORY-1.2"/></properties>
  </testcase>
  ```

  If the reporter omits `file`, emit `test-file` (alias `test_file`) with the full project-relative
  path, or `test-id` (alias `test_id`) with the full planned node identity. An absolute reporter
  path may prepend its CI workspace, but a basename alone cannot identify a test. Conflicting
  identity fields fail matching. Class-qualified plans must match the reported classname unless
  an explicit full `test-id` is supplied. Parameterised IDs may extend the planned node with `[case]`.

  Configure identity export per framework during AR; use an adapter when the reporter cannot
  emit these properties. With pytest, collection-time `item.user_properties` also tags skipped
  tests; a fixture called only during execution cannot tag a test that never starts.
  Explicitly shared tests may list several contract IDs, separated by whitespace, commas or
  semicolons; there is no unscoped fallback. Old VAL-only reports no longer count.

  A correctly scoped test that ran but carries no VAL ID is reported as untagged. Missing or
  mismatched contract/full test identity is reported as missing, not borrowed from another story.
  Every mechanical, non-waived VAL needs a matching result, and all matches must pass. A mismatch
  with the recorded result is reported for Code Review to reconcile.
- **Results must come from the run.** The report must be outside the project tree, so a committed
  or stale file cannot stand in for a real run. Pass several reports with repeated `--junit`.
  Reports with a DOCTYPE or entities are refused.
- **Reporters.** pytest `--junitxml`; Playwright `--reporter=junit` with
  `PLAYWRIGHT_JUNIT_OUTPUT_FILE`; Jest `jest-junit` with `JEST_JUNIT_OUTPUT_DIR`; Vitest
  `--reporter=junit --outputFile`; Go `gotestsum --junitfile`. For exact file matching, turn on
  file attributes where offered (pytest `-o junit_family=xunit1`, jest-junit `addFileAttribute`).
- `--json` output includes `ci_results`, the per-VAL outcome, for Code Review's Delivery Evidence.

Limits: delivery evidence must come from the CI run, which the agent does not control; a local run of
the same command is a preview only. Nothing here blocks a merge by itself; that is a per-project choice.
Matching requires the contract, VAL ID and full test identity; the reporter/adapter must assign
those identities correctly. Locally, without `--junit`, the evidence-file checks above still apply.

## Edit guard (Pi)

`.pi/extensions/contract-guard.ts` (shipped by sync.sh, separate from the project's own
readiness extension) intercepts the agent's `write` and `edit` tool calls and
asks the validator's `guard` command whether the change is allowed. It refuses:

- changes to the `## Acceptance Contract` or `## Contract Approval` sections (including
  `### Locked Tests`) of a spec whose Status is `approved` or `superseded`;
- changes to a locked ATDD test other than removing skip markers;
- any edit to those files it cannot reproduce exactly (it fails closed).

Recording approval on a draft spec is allowed; record every approval field and the Locked Tests
table in a **single** edit, because after Status becomes `approved` the section is protected.
Delivery Evidence, the Review Record, notes, tasks and ordinary files stay writable.

Only the user can lift the guard: `/contract-unlock <spec path>` allows changes to that spec and its
locked tests for the session (Correct Course), and `/contract-lock` re-locks. The agent cannot run
slash commands.

Limits: it sees only the `write` and `edit` tools; `bash` (for example `sed -i`), other tools and
humans are not intercepted. It catches mistakes early; validation and protected CI remain the gate.

## Developer rules (implementation subagent)

### Mandatory preflight

These rules cover approved implementation only, including its tests and checks, not planning or
approval. Use the generated `_bmad/custom/instructions/implementation.md` first; it extracts this
section, not an independently maintained summary. Check it before relying on it:

```bash
python3 _bmad/custom/scripts/render_stage_guidance.py --check
```

If missing or stale, read this full manual before continuing. Read the actual spec and the project's
readiness decisions. Before capturing a baseline, syncing status, or changing tests or code, run:

```bash
python3 _bmad/custom/scripts/validate_story_contract.py validate --phase approved <spec_file>
```

HALT on failure. A `ready-for-dev` label is not approval. Never repair approval fields, locks or the
digest to make this pass. Unattended Build reports `blocked`; it never invents an approval or waiver.

### Implementation obligations

- Implement only an approved revision; work must trace to an `AC-*` and a task. Never edit the
  frozen block, `Contract Approval` or `Delivery Evidence`. If ambiguity or a semantic change is
  needed, stop and report it for Correct Course rather than continuing.
- Use the Validation Design as the test-first plan. For each Dev-owned mechanical `VAL-*`, activate
  or create the planned check, show RED where the behavior does not yet exist, implement to GREEN,
  and keep the exact command and output. Name or tag acceptance-level tests with their `VAL-*` and
  `AC-*` IDs. Leave Test Architect-owned manual checks for review.
- Record evidence candidates for every Dev-owned `VAL-*` under `## Implementation Notes`: PASS or FAIL,
  path/output, and commit/build/CI identity. Never invent independent results or self-approve
  waivers. Run the project's aggregate local gate, as recorded in `docs/agent-readiness.md`.
- Record `- Implementation session: <id>` under `## Implementation Notes` before the first
  implementation write: one generated ID per agent session, reused within it.
- A locked ATDD test may only have its skip markers removed. If one is wrong, stop and report it for
  Correct Course instead of editing it. Save test output you cite as evidence to a project file.
- Keep each acceptance test's VAL ID (in its name, an appended tag, or a `val` property) and the
  project's contract/full-test identity reporting intact, so CI results cannot be borrowed from
  another story. Never edit approved contracts or locked tests through `bash` to get around the edit guard.

### Stop conditions and exception index

Stop before changing approved intent, locked tests or an unmet obligation. On a known failure,
read the linked full section before choosing a correction. Before making any exception, or when
instructions conflict or the situation is not covered here, read the **full**
`_bmad/custom/story-contract.md`. An omission is never permission to proceed. If the full procedure
still leaves doubt, ask the user or Vera (`bmad-agent-steward`, BG); do not guess or bypass a check.

| Trigger | Read in the full manual; route |
| --- | --- |
| Approval missing, invalid, unsealed, or the contract/digest changed | [Approval change (jj)](#approval-change-jj) and [Lifecycle](#lifecycle); Correct Course/reapproval |
| Locked test is wrong, changed, missing or uses an unusual skip marker | [Locked ATDD tests](#locked-atdd-tests); TEA and Correct Course |
| Requirement, scope, risk, oracle, waiver or untracked/trivial routing needs a decision | [Contract rules](#contract-rules) and [Lifecycle](#lifecycle); user/source owner |
| Required evidence or manual validation is unavailable | [Delivery provenance](#delivery-provenance); independent reviewer/TEA, never self-approve |
| CI output is missing, skipped, failing, or names/tags do not match | [CI results](#ci-results); follow project-specific wiring, do not impose a provider |
| Edit guard refuses the change | [Edit guard (Pi)](#edit-guard-pi); user-authorised Correct Course, never bash as a bypass |
| A legitimate request cannot meet a guardrail | [Enforcement boundaries](#enforcement-boundaries); Vera diagnoses with the user |

When implementation finishes, rerun approved validation and the project's aggregate gate. Return
actual AC/VAL evidence candidates and remaining manual obligations; route to TEA Test Review when
risk/test sensitivity requires it, then Code Review. Implementation finished means In Review, not
delivered. Final Delivery Evidence, waivers and the Review Record belong to independent review.

## Enforcement boundaries

BMad TOML activation and completion hooks are durable workflow instructions, not protected state
transitions. They are rendered into the workflow (Build publishes them into its snapshot under
`_bmad/render/`) and execute around the upstream steps; they cannot reorder those steps. The
Build `ready-for-dev` status and sprint `ready-for-dev` label mean the spec exists; only an approved matching contract
authorizes implementation. The validator makes contract structure, digest, traceability, evidence and
waiver expiry deterministic, but a target project's aggregate local check and required CI/repository
control must invoke it to make bypass mechanically blocking. User-level TOML can override scalar
`on_complete`; never represent that hook alone as a hard gate.

When a contract, locked test, the edit guard or the CI step blocks legitimate work, do not work around it:
bring in the Guardrail Steward (`bmad-agent-steward`), who diagnoses the cause with the user and routes or
adjusts it (see project-context.md, "Guardrail Steward").

## Diagnostic guidance

Validator failures retain their original error messages and exit status. Text output adds `Read:`
links to relevant full sections. JSON adds `guidance` entries (`error`, `references`) and a
`recovery` instruction; CI reports include these per failing contract, and guard verdicts include
them for refused edits. Unknown diagnostics point at the full manual, not a guessed correction.

These are navigation hints, not permission to bypass a failure. Read the referenced full sections;
before an exception, or if instructions conflict or the situation is unlisted, read this full
manual and discuss unresolved decisions with the user or Vera. Planning, approval, independent
review and Correct Course still require the full manual; only approved implementation uses the
short generated instructions first.

Generate or check that pilot with `python3 _bmad/custom/scripts/render_stage_guidance.py [--check]`.
The generated file fingerprints the complete source manual, so even an exception added elsewhere
makes `--check` fail until reviewed and regenerated. A stale or missing file requires full-manual
fallback. Generation extracts the complete developer section; do not maintain a second summary.

## Validator commands

```bash
# Draft structure and traceability
uv run _bmad/custom/scripts/validate_story_contract.py validate --phase draft path/to/spec.md

# Compute the exact digest to place under Contract Approval
uv run _bmad/custom/scripts/validate_story_contract.py digest path/to/spec.md

# Development preflight (in a jj workspace this also verifies the sealed approval change)
uv run _bmad/custom/scripts/validate_story_contract.py validate --phase approved path/to/spec.md

# CI in a jj project: also fail when the story is not inside a jj workspace
uv run _bmad/custom/scripts/validate_story_contract.py validate --phase approved --require-jj path/to/spec.md

# Review/completion preflight (also checks locks, planned tests, evidence files, review record)
uv run _bmad/custom/scripts/validate_story_contract.py validate --phase delivered path/to/spec.md

# Print the '### Locked Tests' table at approval (add --file PATH for extra approved test files)
uv run _bmad/custom/scripts/validate_story_contract.py lock path/to/spec.md

# Delivered validation against CI-written JUnit results (repeat --junit per report)
uv run _bmad/custom/scripts/validate_story_contract.py validate --phase delivered --junit "$RUNNER_TEMP/junit.xml" path/to/spec.md

# The CI step (any provider): every approved contract, at the phase it has reached
uv run _bmad/custom/scripts/validate_story_contract.py ci --require-jj --junit "$RUNNER_TEMP/junit.xml"

# Edit-guard verdict as JSON (used by the Pi extension)
uv run _bmad/custom/scripts/validate_story_contract.py guard --proposed /tmp/new-content path/to/file
```

The script is standard-library only; `python3 <script> ...` is equivalent where uv is unavailable.
These commands are deterministic structure and traceability checks. They do not judge whether the
product intent or validation oracle is correct; that remains an approval-blocking human/Test Architect
assurance responsibility.
