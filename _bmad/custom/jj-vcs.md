# Version control: Jujutsu (jj)

Adapted from Seeker's jj configuration for reuse across BMAD projects. This guide
selects jj for target projects; it does not initialise, convert or rewrite a repo.
Before VCS work, verify jj is available in the agreed environment and the target
workspace is already a jj workspace. If either is missing, stop and ask for setup;
unattended work reports `blocked`. Never silently initialise jj or fall back to Git.
A colocated Git backend is supported, but the agent-facing interface remains jj.

## Hard rules

- Never run `git` commands, including read-only status, diff or log commands. Translate
  upstream Git/HEAD/index/branch instructions using the table below.
- The only mutating jj commands an agent may run are `jj new`, `jj describe`, and
  for any bookmark except `main`: `jj bookmark create`, `jj bookmark set` and
  `jj git push --bookmark <name>` (it also creates and tracks a new remote bookmark).
  Move a bookmark forward only: its current target must be an ancestor of the new
  target, and `conflicts() & ::<target>` must be empty. Never pass `--allow-backwards`,
  never delete, rename, forget or force-push a bookmark, and never push `--all`.
- `main` stays with the user: never create, set, move or push it.
- Fetches, history edits, squash, split, rebase, abandon, restore, edit, undo,
  operation restore and repository setup stay with the user. Never hide
  prohibited operations inside a script, alias or wrapper.
- `jj describe` only ever targets `@`. Never `jj describe -r` another revision: that
  rewrites history, including sealed contract approval changes.
- Read-only inspection through `jj st`, `jj log`, `jj diff`, `jj show`, `jj file list`,
  `jj bookmark list` and `jj op log` is allowed. Most jj commands snapshot the working
  copy into `@`: nominally read-only does not mean zero metadata changes.
- There is no staging index. Interpret a staged/uncommitted diff request as the
  current change `@`; never stage files.
- A shipped BMAD evidence helper that internally reads Git may be used only after
  checking that it is read-only and permitted. It is not permission for direct Git
  calls or hidden writes. In a conventional single-parent colocated workspace Git's
  HEAD follows the working-copy parent, not the current working-copy contents.
  Supplement helper output with jj evidence covering `@`; never treat it as the full diff.

These are workflow instructions, not an operating-system permission boundary.

## One change per stage

The agent performs the permitted `jj new` / `jj describe` commands, rather than
handing them to the user. Planning, ATDD, implementation, and review/closure are
separate stages. Read-only work needs no new change. Resume an existing stage in
its existing change only after verifying its identity and scope; a spec status
alone is not proof. Resuming Build implementation after ATDD is a new stage, not
resuming the earlier planning change.

Do not mutate VCS merely because a persona greeted the user or a workflow activated.
Once the actual target/stage is known and its applicable approval gate has passed,
prepare the stage immediately before its first file write:

1. Classify `@`:

   ```sh
   jj log -r @ --no-graph -T 'if(empty, "empty", "changed") ++ " " ++ if(description, "described", "undescribed") ++ "\n"'
   ```

   | Current change | Action for a genuinely new stage |
   | --- | --- |
   | `empty undescribed` | Reuse `@`; do not create an unnecessary child. |
   | `changed described` or `empty described` | Run `jj new` to start a fresh change. |
   | `changed undescribed` | Stop and ask; do not label or absorb unknown work. Unattended mode blocks with `undescribed changes in jj working copy`. |

2. Give the stage a provisional Conventional Commits subject with `jj describe -m`.
   For tracked stories retain the exact `(story-<epic>.<story>)` marker in each stage:
   `docs(story-1.3): plan profile editing`, `test(story-1.3): add acceptance tests`,
   `feat(story-1.3): implement profile editing`, or
   `fix(story-1.3): address review findings`. Use the actual stable story identity;
   if a project cannot use this marker, agree and record its equivalent before work.
3. When the stage finishes, replace the provisional description with its final
   Conventional Commits message. Pass subject, blank line and body as one `-m`
   argument. Separate `-m` arguments starting with `- ` can be parsed as flags.

Keep stage/change identities and evidence in existing mutable notes, checklists or
review artifacts, never the frozen Acceptance Contract. A change ID is stable as
the change evolves; its commit ID is not. Evidence must name the actual observed
commit/build/run, and later edits require fresh verification.

### No commit-message hand-off

The agent records the message itself with `jj describe`. Keep the upstream subject,
body and Spec-footer conventions, but override any instruction to finish with a
fenced commit-message draft or ask the user to copy/commit it. Instead finish with
one line naming the described change and subject. Build Auto may retain its spec's
`### Commit message` subsection as a record. On a halt after writing files, describe
only the work actually done and keep the blocker; never turn a description into
approval or delivery. Do not mutate an unrelated change merely to finalise a report.

## Contract / ATDD stages

Planning artifacts (brief, PRD, UX, architecture, epics/stories, specs) follow the same
rule: one described change per planning step, e.g. `docs(prd): draft product requirements`.

Keep the shared contract lifecycle, not Seeker's old blanket ATDD-before-Build gate:

**Build planning -> ATDD and explicit approvals -> Build implementation -> independent review.**

Both planning and ATDD happen before implementation. ATDD's red-phase scaffolds and
checklist get their own change. Preserve their tests, AC/VAL links and evidence;
never delete, skip or weaken required tests to make delivery pass. A required
skipped scaffold is not completion evidence. Planned skips are valid before coding;
required delivery checks must run or have an independently approved contract waiver.

The approval is its own change, separate from the ATDD change: after explicit approval,
`jj new`, edit only the spec's Contract Approval fields and `### Locked Tests` table (from
the validator's `lock` command), describe it with the trailers
in story-contract.md ("Approval change (jj)"), then `jj new` to seal it. Approved- and
delivered-phase validation compare the contract with that sealed version, so a later
contract edit with a recomputed digest fails. A new contract revision gets a new approval
change; never describe, rewrite or replace an existing one.

Build must pass approved-phase contract validation before creating the implementation
stage, capturing `baseline_commit`, changing tests or implementing code. After starting
that stage, record `baseline_commit` as the full commit ID of its single parent `@-`.
Keep an existing baseline when genuinely resuming that implementation stage. If the
parent or stage identity is ambiguous, stop; never guess or rewrite the baseline.

## Git -> jj translations

| BMAD asks for | Use |
| --- | --- |
| Clean working tree | Classify `@`; unknown `changed undescribed` work blocks. |
| Writable VCS metadata | `jj st`; failure blocks with `version-control metadata not writable`. |
| Current branch | `jj log -r '::@' -n 10`; inspect the nearest ancestor bookmark, not an assumed branch name. |
| Current working change / parent | `@` / `@-`; check for a single parent before treating it as one baseline. |
| `baseline_commit` | After the approved implementation stage starts: `jj log -r @- --no-graph -T commit_id`. |
| Diff since the stored baseline | `jj diff --git --from <baseline_commit> --to @`. New non-ignored files are included. |
| Staged/uncommitted/current-change diff | `jj diff --git`. |
| Branch diff | Resolve the agreed base; `jj diff --git --from 'fork_point(<base> \| @)' --to @`. Do not assume a bookmark named main exists. |
| Revision range | `jj diff --git --from <from> --to <to>`. |
| One revision | `jj show --git <rev>`. |
| Selected files | `jj diff --git <path> ...`. |
| Summary / numstat | `jj diff --stat` for summary; use the Git-format patch for details, not a fabricated numstat equivalent. |
| History | `jj log -r '<base>..<head>'`; use `--no-graph -T 'description ++ "\n"'` when only messages are needed. |
| Ancestor check | `jj log -r '<ancestor> & ::<descendant>' --no-graph -T commit_id`. Empty output means no match. |
| Commit preparation | Start/reuse the correct stage and describe it; never run another mutating VCS operation. |

## Review the full story, not just the last change

The implementation's `baseline_commit` may already include ATDD. Preserve that field,
but do not use it alone to scope a story review: otherwise the acceptance-test change
can be omitted. Resolve the planning, ATDD, implementation and review-stage change IDs
from their recorded identities and the verified story marker on `::@`.

For a conventional marker, inspect:

```sh
jj log -r 'description(substring:"(story-<epic>.<story>)") & ::@'
```

Call the **verified** set of this story's stages `S` below; `S` is explanatory notation,
not a configured jj alias. Inspect the earliest stage's parent and current top stage,
resolve them to concrete commit IDs, then run:

```sh
jj diff --git --from <full_story_base_commit> --to <reviewed_tip_commit>
```

The range must include ATDD, implementation, and review fixes/status artifacts. A
matching description alone is not authoritative: confirm project/story identity,
ancestry, scope and that no unrelated work is swept into the range. Multiple roots,
ambiguous names, a missing stage or an unrelated intervening change require user
resolution. Record the review range separately; never silently change the spec's
implementation baseline or an approved contract to make a range fit.

Entering review is a new stage before the first fix, review artifact, Delivery
Evidence or status write. Use the same reuse/resume rules. Finalise the review
change description, run checks after the last patch, and review review-time code/test
fixes too. Later edits invalidate affected evidence; do not close from stale results.

## Closing a story and recommending a bookmark

When the user asks, any agent may set and push a non-`main` bookmark under the hard
rules above; that push shares work and is never delivery or closure. ATDD, Build and
Build Auto never recommend a closure bookmark. Only Code Review may do so, after all
of these are freshly true:

1. Review covers the full verified story range, including acceptance tests and review fixes.
2. Required findings are resolved; deferrals/waivers have explicit authority and do not
   bypass the contract. The story/spec and applicable sprint tracking are `done`.
3. Execution tasks are complete and every AC/VAL has independently accepted evidence;
   delivered-phase contract validation passes. Build's own `done` is not delivery.
4. The project's actual agreed aggregate check and required remote checks pass after
   the final patch, using the runner/environment in `docs/agent-readiness.md` and
   project-local test instructions. Do not copy Seeker's npm/cluster commands into
   other projects. Required ATDD tests run and pass, except explicitly authorised,
   recorded contract waivers. Never substitute a partial run or a down test service.
5. `conflicts() & ::@` is empty; verified story stages have final descriptions and
   no unresolved work. Record the current tip's full commit ID with the evidence.
   `@` is the top story stage or an empty undescribed child of it.

On any failure, keep the story open, list blockers and recommend no bookmark. Linear
Done or a completed checklist is not sufficient. Do not close an epic/project just
because its latest story passed.

Only after all checks pass, confirm the project's bookmark naming convention and
resolve the actual top reviewed story change. Do not assume Seeker's `feature/epic-*`
convention. Inspect the existing bookmark and its ancestry. Never recommend a move
backwards/sideways, an ambiguous target or an unreviewed tip. If the name/convention
is unknown, ask rather than inventing it. Precede the bookmark step with the story
closure summary. For a bookmark other than `main`, set it and push it yourself under
the hard rules. For `main`, show the create/set command in a fish code block for the
user to run manually, and never execute it or push it. Keep existing contract and
Linear reports; the bookmark step does not replace them.

## Checks and provenance

This is reusable instruction text, not a daemon or a hard permission gate. Use
`python3 -m unittest discover -s _bmad/custom/scripts/tests -p 'test_jj_guidance.py'`
to check its wiring. The source is Seeker's `_bmad/custom/jj-vcs.md` and jj workflow
overrides; its test runner, fixed bookmark names and old Build-order gate are not imported.
CLI semantics were checked against https://docs.jj-vcs.dev/latest/faq/ and
https://docs.jj-vcs.dev/latest/guides/cli-revision-options/.
