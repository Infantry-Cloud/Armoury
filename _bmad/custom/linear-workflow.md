# Linear: the whole BMAD workflow

This is an operational workflow, not just a recommendation to use a tracker. When
authorised, call the connected Linear MCP tools and persist their returned IDs.
One named body of work (Recon, Serial, etc.) gets one Linear **Project**. Planning
steps are issues in that project; development epics are parent issues, stories/bugs/
spikes are their sub-issues, and implementation tasks are story sub-issues. Linear
has no separate Epic object. Each epic also gets one **project milestone** in the
same Project, and the epic issue and all its descendants belong to that milestone.
Do not create a paid Initiative or one project per epic.

The agent also writes **activity notes**: an issue comment for each status change it
makes, and a project status update when an epic closes or reopens. They give the team
visibility and context. They are reports, never approval (see Activity notes).

Local planning artifacts and approved Acceptance Contracts remain authoritative.
Publishing, a Linear status, or a task checkbox never authorises implementation or
changes an approved contract. These instructions are agent-executed soft integration,
not webhooks, an unattended sync daemon, or a protected approval gate.

## Installed-version boundary

The verified released baseline is BMAD **v6.12.2**: `bmad-help`,
`_bmad/_config/bmad-help.csv`, `bmad-create-epics-and-stories`, `epics.md`,
`bmad-sprint-planning`, `sprint-status.yaml`, and Build specs. Resolve actual output
paths through `_bmad/scripts/resolve_config.py`; never assume `_bmad-output`.

Upstream `main` also has `bmad`, `bmad-ticket`, an `active_initiative`, and
`tickets.toml`. If installed, use its help and native store operations instead of
inventing a second ticket tree. Never migrate the project's artifacts or replace
its contract lifecycle as a side effect of setting up Linear. This repository's
existing Build/Code Review contract overrides target v6: they require a separately
approved migration before using the newer plan/ticket-tree implementation lifecycle.
Halt implementation if that migration is missing; native publishing is not proof of
contract-lifecycle compatibility.

## State, identity and permission

- Keep a committed, secret-free manifest at `_bmad/linear/projects/<slug>.json`.
  Keep the selected manifest's relative path in `_bmad/linear/active.json`, e.g.
  `{"manifest": "projects/recon.json"}`. Resolve it strictly inside `_bmad/linear/`.
  These are outside the mirrored `_bmad/custom/` directory. Never put credentials
  or OAuth tokens in them. Multiple named projects have separate manifests.
- A manifest contains `schema_version: 1`, a once-generated `binding_id` (UUID),
  `name`, confirmed `team_id`/`team_key`, `project` (confirmed `id` and `url`, or
  null before creation), the actual status-ID map, `publication_approved`, and
  `items`. Each item has a stable `key`, `kind`, `title`, `skill`/action if applicable,
  `source` (current project-relative artifact `path` and source `id`), `parent_key`
  or null, `after` keys, agreed `done_when`, publication state (`pending`,
  `published`, or `uncertain`), confirmed remote `id`/`identifier`/`url`, and evidence
  when known. An epic item also has `milestone`: its publication state and confirmed
  `id`/`name`. Any item can have `notes`: one entry per activity note, with `marker`,
  `kind` (`comment` or `project-update`), publication state and confirmed remote `id`.
  Reconcile adds `synced` (the baseline at the last proven sync), `source_history`
  (earlier source IDs), and `lifecycle` (`active`, or `cancelled`/`superseded` with
  `superseded_by`, only after the user approves). Only the reconcile helper's
  `baseline` command writes `synced`. These fields are additive; an older manifest
  gets them through Reconcile. Existing manifests may use other shapes: `source.id`
  as `epic-1`/`story-1.1`, titles with their `Epic 1:` prefix, remote IDs under
  `remote`, story keys such as `story:1:1.1`, or epic milestones in a top-level
  `milestones` map (with `milestone_key` and their own recorded marker). The helper
  reads all of them and writes back in the shape the manifest already uses. Never
  migrate a manifest's shape as a side effect of reconciling.
  Save atomically (temporary sibling file + replace), after each confirmed write.
- Use keys such as `planning:prd`, `planning:architecture`, `epic:<source-id>`,
  `story:<epic-id>:<story-id>`, and `task:<story-key>:<stable-task-id>`. Multiple
  research/architecture/spec steps need distinct user-agreed IDs. Assign a task ID
  once when its approved plan first appears. Never derive identity from mutable
  titles, array positions, run dates, or absolute workstation paths; never reuse an ID.
  A key is opaque once assigned: when an epic or story is renumbered, moved to
  another epic, or retitled it keeps its key, and only `source` changes. For example,
  `story:1:2` stays `story:1:2` after it becomes Story 2.4. A new key that would
  collide gets a suffix (`story:1:2~2`). Never re-key an item to tidy its name.
- A project description carries `BMAD-PROJECT-ID: <binding_id>`; an issue description
  carries `BMAD-ID: <binding_id>:<key>`; an epic milestone description carries
  `BMAD-ID: <binding_id>:<epic key>:milestone`. Record the same marker and IDs locally.
  Fetch saved IDs before updating, checking team/project/marker. With no saved ID,
  search/list all relevant pages and verify exact markers before creating. For an
  explicitly adopted existing project, confirm its identity and add the marker.
  A title-only match, conflicting mapping, or multiple marker matches requires
  user resolution, not a new duplicate or a guessed update.
- BMAD owns an issue's description only inside its **managed block** at the end.
  Text above the block belongs to the team. The block is:

  ```text
  ---
  BMAD-managed - change this in BMAD, not in Linear.
  <publishable summary, acceptance references, source link, dependencies>
  BMAD-SOURCE: <project-relative path>#<source id> <digest>
  BMAD-ID: <binding_id>:<key>
  ```

  Copy the `BMAD-SOURCE` line exactly from the reconcile helper's `source_line`.
  Planning and task issues omit that line. When you update a description, replace
  only the block and keep the text above it.
- Project/team and publication approval are obtained once at Kickoff. This allows
  publishing subsequently approved planning steps, stories and execution tasks
  without asking again per issue. It does not approve new scope, assign people,
  expose secrets/private artifact bodies, change team settings, or bypass host
  tool-permission prompts. Keep remote descriptions to publishable summaries,
  acceptance references and source links; obtain separate approval for sensitive data.
- Use one publishing session per manifest. Concurrent writers need a real lock/
  transactional reconciler before unattended use; markers alone are not uniqueness
  constraints. Never claim exactly-once delivery or mechanical approval enforcement.

## Kickoff — project first, agreed planning tickets next

1. Confirm the project's name and select/create its stable manifest. Do not infer
   that the current folder's name is the product name or switch another active project.
   If BMAD is absent, stop and offer the installed version's setup; no fake install.
2. Read installed BMAD help/catalog, existing artifacts, and configured paths.
   Propose the smallest ordered plan appropriate to this project, with skill/action,
   dependencies and observable completion criteria. Examples are product brief,
   PRD, UX, architecture, technical spec, epics/stories, implementation readiness,
   sprint planning, and this repo's AR (Agent Readiness). They are candidates, NOT
   mandatory boilerplate. Include installed TEA steps where the agreed risks require
   them. Distinguish already accepted output from drafts; file existence is not completion.
3. Ask the user to approve/edit this plan and authorise publishing to the confirmed
   Linear workspace/team. Discover the current MCP tool names and schemas; do not
   assume names from examples. In Pi use MCP tool discovery when tools are deferred.
   Also check for milestone, comment and project status-update tools (for example
   `save_milestone`, `save_comment`, `save_status_update`). Report any that are absent.
   If no tools/authentication are available, leave the plan pending, report the blocker
   and point to `linear-setup.md`. Do not claim anything was created.
4. Query actual team statuses and use their IDs. Map Backlog/Todo, In Progress,
   In Review and Done to existing statuses. If In Review is absent, use In Progress
   plus a review label; never invent/create a team status through unsupported tools.
   Warn that Linear parent/sub-issue and Git auto-close rules can change board status
   outside this workflow. Do not alter team automations without explicit permission;
   a remote Done still cannot satisfy local delivery gates.
5. Create or reuse the Linear Project, persist its returned ID/URL immediately, then
   upsert **every agreed planning step** as an issue with that explicit project ID,
   its stable marker, skill/action, Done when, dependencies and source references.
   Use existing labels, or create missing `bmad:planning`, `bmad:epic`, `bmad:story`,
   `bmad:task`, `bmad:bug`, `bmad:spike` labels after confirming the schema supports it.
   No invented owners, deadlines, estimates or scope. Backfill Done only from accepted
   completion evidence. Persist each returned issue immediately; do not wait for a batch.
6. Apply supported blocked-by relations after both issues exist, resolving stable
   keys to remote IDs. If nesting/relations are not exposed, keep all tickets in the
   Project, link their parent/prerequisites in descriptions, and report the limitation.
7. Show the Project URL, planning-ticket URLs, pending/failed items and the next
   agreed BMAD step. This is the end of kickoff, NOT project delivery.

## Activation — follow the selected step, don't mutate too early

This is a standing instruction for the main workflow **once its intent and target
are known**, not an action before that workflow has loaded its project/story.

Read the active manifest (ask if absent/ambiguous). For a new project with no binding,
offer/run Kickoff before substantial work; never silently attach it to another project.
Before the first Linear write of a run, run the reconcile helper's local drift gate
(`plan --check` without `--remote`; see Reconcile). Exit 3 means the breakdown
changed since the last sync. Run Reconcile first, or at least resolve its identity
steps, so writes never land on a stale key, parent or milestone.
For authorised work, resolve the matching planning/story/task item and upsert missing
approved work. Move the targeted issue to In Progress only when actual work starts.
Help, status-only, validation-only, greeting or an unrelated project do not start work.
If a step was not agreed, ask to amend the plan before creating it. Publish a newly
approved amendment before executing it. Never skip a local gate because Linear is green.

## Run an agreed step

For a requested sequence or a selected step, resolve its manifest key, run Activation,
then invoke its installed skill/action in a fresh context and check its result with
the user. AR loads this repo's shared readiness recipe instead of inventing an upstream
readiness skill. Follow Planning completion with actual evidence afterward. Keep this
wrapper for selected module/custom steps without their own completion hook; don't
invent unsupported TOML hooks. Stop on a local blocker, record the real result, and
never execute the next step merely because a ticket exists. Reconcile is the recovery
path when a direct invocation lacked a callback or was interrupted.

## Planning completion — close the specific agreed obligation

The calling override supplies the skill (or AR) and actual target artifact. Match
that to the manifest item; if several match, resolve the target rather than closing all.
After the workflow has finalised its output, verify that item's agreed Done when and
the user's required acceptance/review. Record evidence (artifact, revision/commit if
available, actual checks) and update its issue to Done only if the obligation is met.
A draft, failed validation, interrupted run, merely existing file, or validation-only
operation is not automatically completion. Edits invalidating accepted output reopen
the affected issue with an evidence summary; don't close it again until reaccepted.
Post concise evidence as an activity note on the planning issue, without secrets.
A reopened planning issue also gets a note. A missing binding remains visibly pending.

AR completes only when docs/agent-readiness.md is actually ready at its agreed score,
with proven applicable correction loops and agent-visible failure/repair evidence,
and has validated its agreed boundary and controls. A design document, installed tools
or a high score alone is not Done.

## Publish development — every approved epic, story and task

After epics/stories are finalised, or a later approved change adds work, reconcile all
approved entries into the **same** Linear Project: epics first, then their stories,
bugs and spikes. In the released layout, use stable epic/story IDs from epics.md and
sprint status; in the ticket-tree layout, use scoped IDs from tickets.toml and pulled
files. Publish the whole approved breakdown, not just the story starting next.
Every issue gets the explicit project ID (including standalone bugs), type, parent
where supported, source references, acceptance summary, dependency links and marker.
Work under an epic also gets that epic's milestone (see Epic milestones below).

When Build has an approved execution plan, publish **each execution task** as its own
issue under the story, with stable task identity and AC/VAL references. Do this before
implementation: register at Build CHECKPOINT 1 after plan approval, and on resumed
plans before coding. Product plan approval may precede TEA contract approval: those
tasks stay Backlog until the existing approved-contract gate passes. Publishing never
edits the frozen contract; keep tracking metadata in the manifest, not its normative block.
Unattended Build cannot invent approvals. A blocked run remains blocked/pending.

If `bmad-ticket` is installed, configure its native Linear store using its own
`read_store.py`/setup references and persist only project-specific settings in
`_bmad/custom/ticketing-store-config.toml`. Use its native write/query verbs and record
the same remote IDs/URLs in the manifest and native `tracker_id`/`remote` fields so
neither publisher creates a second issue. A native issue without our marker must be
confirmed and adopted, not duplicated. Publication is at inception, not only on start.
Its starter omits project on standalone tickets: the shared rule above overrides that.
The epic milestone and activity-note rules also apply to its tickets.
Its local initiative is not a second Linear Project. Do not copy/replace whole native
verbs or introduce this config when the skill is not installed.

Every status change in this section gets an activity note (see Activity notes).
Build finishing is **In Review**, never delivered. Checked tasks also remain In Review
until independent Code Review accepts their evidence. Code Review alone may publish
Done for contracted work, after delivered-phase contract validation and the project's
required gates/independent review pass. Any unresolved finding keeps/reopens affected
work to In Progress. For a spike/manual task, use its explicitly agreed independent
acceptance instead of fabricating a code-review obligation. Epic completion follows
the two stages below; Build never closes an epic. No workflow automatically closes
the Linear Project. Remote board edits cannot modify contracts or local Build/sprint status.

Correct Course revises local intent and obtains reapproval first. Then run Reconcile:
it carries renumbered, moved, split, merged and retitled work onto the existing
issues. Reopen invalidated completion, retain old evidence/history, and flag removed
work for explicit cancellation approval. Never delete tickets.
Post a comment on each reopened or changed issue that names the change record.
Retrospective action items become tickets only when agreed, not speculative work.

### Epic milestones

1. For each approved epic, upsert its milestone before the epic issue. Find it by its
   marker in the Project's milestones; never match on name alone.
2. Name it as the epic, for example `Epic 1: Import reconnaissance data`. Put the
   marker, a short goal and the source reference in its description.
3. Do not set a target date unless the user agreed one. Keep the epic order.
4. Set the milestone on the epic issue and on every story, bug, spike and task under
   it. Planning issues and standalone bugs have no milestone.
5. When an approved change moves work to another epic, move its milestone too.
6. Never delete or rename-reuse a milestone. A cancelled epic keeps its milestone
   until the user decides. Linear computes milestone progress from its issues, so
   the workflow never marks a milestone complete.

If the tools do not support milestones, publish the epic issues, record each
milestone as `pending`, and report the limitation. Do not use labels as a substitute.

## Activity notes — comments and project updates

Activity notes make each completed step visible in Linear, with its context. Use
the smallest suitable kind:

| Event | Kind and target |
| Planning step Done or reopened | Comment on the planning issue |
| Task, story, bug or spike moves to In Progress for rework, In Review or Done | Comment on that issue |
| Epic moves to In Review (last story accepted) | Comment on the epic issue |
| Epic Done (retrospective accepted) | Comment on the epic issue, then a project status update |
| Accepted epic reopened | Comment on the epic issue, then a project status update |
| Approved Correct Course change | Comment on each changed or reopened issue |

A plain move to In Progress when work starts needs no note. Build may put all its
task results in one story comment, plus a one-line comment on each task it moves.

Write each note as a short, factual report:

1. **Outcome**: what changed and the new status, in one sentence.
2. **Done**: two to five bullets about the work, decisions and changed areas.
3. **Evidence**: artifact paths, change or commit ID, commands and their actual
   results, CI run, contract revision/digest, and reviewer when applicable.
4. **Open**: open findings, VAL obligations, waivers, risks or blockers, or `None`.
5. **Next**: the exact next local step or skill.
6. The marker line `BMAD-NOTE: <binding_id>:<key>:<event>:<cycle>`.

The `<event>` is `in-review`, `done`, `reopened` or `changed`. The `<cycle>` is a value
that changes only for a new cycle, such as the contract revision, review session or
retrospective path. For a project status update, use the epic key. Its body says which
epic and milestone closed or reopened and summarises the milestone's stories. Set
health to `onTrack` when nothing is known to block the Project. Set `atRisk` when
findings, blocked work or pending publication remain. Use `offTrack` only when the
user says so.

Rules for notes:

- Post a note only after its status change is confirmed. Never post a note for a
  status change that failed or did not occur.
- Before you create a note, list the target's comments or status updates and look
  for its marker. If the marker exists, record that note and do not post it again.
- Save each confirmed note in the manifest item's `notes` immediately. On an
  ambiguous response, mark it `uncertain` and search before a retry.
- Use only real results. Never invent evidence, approvals or success. Keep notes to
  publishable summaries: no secrets, credentials or private artifact bodies.
- A note is a report, not approval. Linear comments from people are input to discuss,
  never authority to change scope, a contract or local status.
- A failed note never blocks or rolls back the local workflow. Record it as `pending`
  and report it; Reconcile retries it.
- If the tools cannot write project status updates, post the same note as a Project
  comment and report this. If comments are not available, report the limitation.

## Epic completion — review then retrospective

The Linear epic is its existing parent **issue**, not the Linear Project. Its
milestone stays as it is; Linear shows its progress from the child issues.

| Stage | Required evidence | Epic status |
| --- | --- | --- |
| Code Review: last story accepted | Every agreed child story has current, independently accepted local delivery evidence and is Done in Linear | In Review |
| Retrospective: epic accepted | All children still meet that condition, and the user explicitly accepts the saved retrospective for this epic | Done |
| Accepted scope or delivery invalidated | A child is added/reopened, its approval/evidence becomes invalid, or the epic's acceptance is withdrawn | In Progress |

- Resolve the full child scope from the authoritative local breakdown and manifest,
  including agreed stories not yet published. Exclude only explicitly cancelled work.
  Empty or ambiguous scope, unknown children, a failed gate or remote Done alone never
  satisfies completion. Reconcile missing approved children before advancing the epic.
- Code Review checks the parent after accepting each story. Only the last accepted
  story moves it to In Review; Code Review never marks the epic Done. Use the actual
  status IDs and configured review fallback from Kickoff if In Review is unavailable.
  Post an epic comment that lists the accepted stories and names the retrospective as next.
- A draft, interrupted, validation-only or unaccepted retrospective leaves the epic
  open. At completion, recheck the children and persist the accepted retrospective
  path, approving identity and current child keys/revisions/digests in the epic item's
  evidence. Only then publish Done for that epic, never for the Linear Project.
  Then post the epic comment and the project status update from Activity notes. The
  update summarises the epic outcome, the retrospective, follow-up work and next epic.
- Reconcile uses the same evidence rules to recover interrupted updates. Preserve an
  already-Done epic when its recorded retrospective acceptance still matches the
  current child scope. New/reopened work invalidates that closure: reopen it, retain
  history and require fresh retrospective acceptance after the children are delivered.
  A reopened epic that was Done gets an epic comment and a project status update.
  Publication failures stay pending/uncertain; no duplicate issues or invented success.

## Reconcile, failures and reporting

Reconcile keeps Linear aligned with BMAD after anything changes: new work, a
renumbered or reordered breakdown, a story moved to another epic, a split, merge,
retitle or removal, and edits people make in Linear. Local artifacts are
authoritative, so Reconcile changes Linear and the manifest's tracking fields to match
them. It never imports Linear text/status as approved local intent.

Run it after create-epics-and-stories, Correct Course, sprint planning and any hand
edit of the breakdown. Also run it when the Activation drift gate fails, when a
completion hook was interrupted, and when the user asks.

Reconcile reads the selected manifest and authoritative local artifacts, adopts
verified native IDs, and queries Linear before each upsert. It backfills agreed
planning steps and ALL approved development entries/tasks, including artifacts
created before kickoff. It also upserts missing epic milestones, sets each issue's
milestone, and retries `pending`/`uncertain` notes. It posts notes for status changes
it makes itself. It does not write notes for past events unless the user asks for a
backfill.

### The reconcile helper

```bash
uv run {project-root}/_bmad/custom/scripts/linear_reconcile.py plan \
  --root {project-root} --epics <resolved epics file(s) or sharded epics dir> \
  [--sprint-status <resolved sprint-status.yaml>] [--remote <snapshot.json>] [--check]
```

The helper is read-only. It prints a JSON plan with `steps` (`phase`, `key`,
`action`, `needs_user`), `new` entries (proposed keys and lookalike `candidates`),
`matched` entries (desired title and parent) and `warnings`. With `--check` it exits
3 when anything needs reconciling. Without `--remote` it compares the breakdown with
the manifest only, which is the cheap Activation gate. It reads the released layout
(epics.md, sprint-status.yaml). In the ticket-tree layout native IDs are stable:
apply the same field, block and three-way rules by hand.

It matches entries to keys in this order, so identity survives refactoring:

1. Same title and body, wherever the entry now lives (renumbered or moved).
2. Same source ID, and the title, the body or a recorded user confirmation agrees.
3. Same title only.
4. Same body only (retitled).

Anything left over is never guessed. The helper reports a lookalike as
`confirm-identity`, and a manifest item with no local entry as `missing-locally`.

### Remote snapshot

Build it from MCP list/get calls before each full plan and again after applying.
Include all pages, canceled and archived issues of the Project, and every issue found
by a marker search. Fetch an issue when a list call truncates its description. Write
it to a temporary file outside the repository; it may hold private text. Never commit it.

```json
{"project": {"id": "..."},
 "issues": [{"id": "...", "identifier": "...", "url": "...", "title": "...",
             "description": "...", "parent_id": null, "milestone_id": null,
             "project_id": "...", "status": "backlog", "archived": false}],
 "milestones": [{"id": "...", "name": "...", "description": "..."}]}
```

`status` is one of `backlog`, `todo`, `in-progress`, `in-review`, `done` or `canceled`,
mapped through the manifest's status map. The configured review label counts as
`in-review`.

### What Reconcile owns

Reconcile owns these managed fields: the title (`Epic N: <title>`,
`Story N.M: <title>`, and the epic's milestone named the same), Project, parent,
milestone, `bmad:*` labels, relations it created, the managed description block, and
status under the evidence rules. Everything else belongs to the team. That includes
assignee, priority, estimate, cycle, other labels, comments and description text above
the block. Never overwrite those fields.

For each managed field the helper compares three values: BMAD's desired value,
Linear's current value, and the `synced` baseline.

| Linear | BMAD | Result |
| --- | --- | --- |
| equals desired | any | in sync |
| equals baseline | changed | `update-*`: write the BMAD value |
| changed | equals baseline | `restore-*`: write the BMAD value back, then comment why |
| changed | changed | `conflict-*`: ask the user |

An item without a baseline gets `update-*` and `no-baseline`. List these items for the
user once before the first write.

### Procedure

1. **Preflight.** Use one publishing session and the active manifest. Resolve paths
   through the BMAD config, then run the local plan. A blocking warning (duplicate
   story ID, story without an epic) stops Reconcile. Fix the breakdown through its
   owning workflow first.
2. **Snapshot.** Build the remote snapshot and run the full plan.
3. **Resolve identity and conflicts with the user before any write.** Show every
   `needs_user` step in one table, then record each decision atomically in the manifest:
   - `confirm-identity`/`missing-locally`, renumbered or rewritten: set `source.id`
     to the local ID and `source.confirmed: true`.
   - Split: the user picks which part keeps the existing key; the other parts are new.
   - Merge: the survivor keeps its key; the absorbed item gets `lifecycle: superseded`
     and `superseded_by`.
   - Removed: set `lifecycle: cancelled` only after explicit cancellation approval.
   - Genuinely new: approve creation under the proposed key.
   - `remote-missing`, `identity-conflict`, `duplicate-remote`, `remote-unknown`,
     `duplicate-milestone`, `milestone-missing`: adopt, relink or recreate as the user
     decides. Never create a duplicate to get past one.
   - `conflict-*`: show both values. The user keeps BMAD's value, or changes BMAD
     through its owning workflow (Correct Course for approved scope), then reruns.
   - `status-ahead`, `remote-canceled`: discuss them. Correct them only with approval.
   - `dangling-dependency`: fix `after` from the approved breakdown.

   Rerun the plan until only steps the user explicitly parked still need the user.
4. **Apply in plan phase order**: identity, milestones, epics, stories, other
   (tasks, bugs, spikes, planning), relations, statuses, notes. Before each write,
   fetch by saved ID and verify the marker. Persist returned IDs immediately.
   - `adopt`/`adopt-milestone`: record the existing ID; never create.
   - `create`/`create-milestone`: create it with its marker under the proposed key.
   - `update-*`, `restore-*`, `retitle`, `refresh-block`, `restore-marker`,
     `set-project`: write the desired value or block.
   - `move`: set the new parent and the new epic milestone on the story and on every
     task under it (the plan lists them).
   - `update-milestone-name`: rename the same milestone for a renumbered epic. This
     is not rename-reuse.
   - `cancel`: set Canceled and keep the issue and its history.
   - Relations: add missing blocked-by links. Remove only the links this workflow
     created that the breakdown no longer has.
   - `status-behind`: advance only through the owning workflow's evidence rules
     (Code Review for Done, and so on), with its activity note.
5. **Verify and baseline.** Re-snapshot and rerun the plan. Then run the same command
   with `baseline --write`. Add `--accept <key>` only for a planning or task item whose
   block this session has just rewritten. Baseline records `synced`, `source` and
   `source_history` only for items the snapshot proves are in sync. Finish with
   `plan --check`; exit 0 means aligned. Otherwise report what remains.

Post a `changed` activity note when Reconcile moves an issue to another epic, cancels
or supersedes it, restores a Linear edit, or applies a conflict decision. Name the
reason and the change record if there is one. Plain renumbering and block refreshes
are silent, so an inserted story does not flood the board with comments.

### Failures

On a timeout/ambiguous create response, mark the item `uncertain`, keep the SAME
marker, and search/reconcile before retrying. Do not blindly retry creates. On auth,
rate-limit, transport or schema failure, preserve confirmed IDs and local artifacts,
record unsent work as pending/uncertain, report the actual failure and resume from it.
Do not claim success, drop pending items, duplicate successful writes, or roll back an
approved local artifact because publishing failed. A local hard gate still halts as usual.

### Reporting

Every integration action reports the Project URL and the URLs of issues and
milestones it created, updated, moved, restored, cancelled or left unchanged. It
also reports posted notes, pending/uncertain items and notes, blockers, decisions the
user parked, the final `plan --check` result, and the exact next local step. If a
workflow's completion hook did not run (halt/interruption), use Reconcile. There is no
automatic background sync.
