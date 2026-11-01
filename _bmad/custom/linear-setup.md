# Using the shared Linear integration

## Install into a BMAD project

These are customisations, not a BMAD installer. The checked release is v6.12.2.
Sync into a real installation (preview first):

```sh
./sync.sh --dry-run /path/to/recon
./sync.sh --backup-dir /path/to/backup /path/to/recon
```

Sync installs the portable `.agents/skills/bmad-linear/` skill and merges the
secret-free `_bmad/custom/linear-mcp.json` server into root `.mcp.json` and Pi's
native `.pi/mcp.json`. Existing servers, tokens, runtime options and existing
`linear` entries are preserved. Conflicting existing configurations need manual
resolution; the integration never silently replaces them. MCP overlays add missing
servers/options, while existing choices win conflicts. Backups retain restrictive
source-file permissions. Native `_bmad/custom/ticketing-store-config.toml` settings
survive shared mirroring. No user-global config changes.

In Pi, grant project trust, `/reload`, then `/mcp login linear` (or sign in through
`/mcp`). OAuth credentials are stored by Pi outside the repository. A replacement
MCP adapter may ignore Pi's native file: point it at the root `.mcp.json` according
to that adapter's documentation. Other clients use their supported project MCP path.

## Start Recon or Serial

```text
/skill:bmad-linear Start Recon. Agree the BMAD steps with me, create its
Linear project, and publish those steps and subsequent approved development work.
```

Alternatively choose **LP** on the analyst, PM, architect or dev agent. The
integration proposes steps from the installed catalog, not a compulsory checklist.
Confirm the Linear team, project and plan once. Example result:

```text
Recon (Linear Project)
  Create PRD                         [planning]
  Create architecture spine          [planning]
  Establish agent readiness          [planning]
  Define epics and stories            [planning]
  Milestone: Epic 1: Import reconnaissance data
    Epic: Import reconnaissance data
      Story: Validate an import
        Task: Reject malformed input
        Task: Add AC/VAL checks
```

Each epic is a parent issue and also a project milestone with the same name. The
epic and all its stories, bugs, spikes and tasks belong to that milestone, so the
Project shows progress per epic. Milestones get no target date unless you agree one.

The agent also writes activity notes. Each status change that it makes gets a
comment on that issue: what was done, the actual evidence, open items and the next
step. When an epic closes after its accepted retrospective, or reopens, the agent
also posts a project status update. Notes are reports, not approvals. A failed note
stays pending and Reconcile retries it.

Stories are published when their breakdown is approved. Execution tasks are
published when Build's plan is approved, before implementation; they are not invented
at kickoff. The contract/TEA gates still apply. Build does not mark work delivered.

IDs and the agreed plan live in `_bmad/linear/`, which `sync.sh` does not mirror/delete.
Commit the secret-free manifests so teammates reuse the same binding. To backfill
existing output or recover a partial publish:

```text
/skill:bmad-linear Reconcile Recon, including planning steps, all stories and tasks.
```

No real Linear project is created by syncing files alone. The agent performs MCP
calls after authentication and your kickoff approval. This checkout has no live
Linear test workspace configured; local tests prove deployment/wiring, not remote writes.

## Supported surfaces and limitations

- Agent `persistent_facts` and `menu` entries; workflow `persistent_facts`,
  `activation_steps_append`, and `on_complete`. Existing contract summaries are
  retained. The shared AR recipe calls the same integration explicitly.
- The custom kickoff skill exists because released `bmad-help` has no workflow
  customization hook. Do not invent `bmad-help.toml`/`bmad.toml` setup interceptors.
- Native `bmad-ticket` publishing support is additive for installations that have it;
  it is on upstream `main`, not the verified v6.12.2 release. Existing v6 Build/Code
  Review contract overrides need a separately approved migration before implementation
  on that newer lifecycle. No automatic migration or upgrade.
- Use `/skill:bmad-linear Run the next agreed step` for module/custom planning steps
  without their own workflow callback; the wrapper checks actual output before closing.
  Released `bmad-project-context` declares but does not execute `on_complete`; its
  override registers the completion instruction through the consumed activation
  surface instead, with the wrapper available as a fallback.
- Agent-executed callbacks, not a webhook/daemon or a mechanical uniqueness/approval
  gate. Interrupted runs need Reconcile; concurrent publishing needs a real lock.
- Team auto-close/Git rules and human edits can change Linear status independently.
  Only local contract validation and protected project gates establish delivery.
- Milestones, comments and project status updates need a Linear MCP server with
  those tools (Linear added them on 5 February 2026). If they are absent, the
  workflow keeps them pending and reports the limitation.

Primary sources checked:

- https://github.com/bmad-code-org/BMAD-METHOD/releases/tag/v6.12.2
- https://github.com/bmad-code-org/BMAD-METHOD/blob/v6.12.2/src/core-skills/bmad-help/SKILL.md
- https://github.com/bmad-code-org/BMAD-METHOD/blob/v6.12.2/src/bmm-skills/plan/bmad-create-epics-and-stories/customize.toml
- https://github.com/bmad-code-org/BMAD-METHOD/blob/main/skills/bmad-ticket/SKILL.md
- https://github.com/bmad-code-org/BMAD-METHOD/blob/main/skills/bmad-ticket/config/linear-ticketing.toml
- https://linear.app/docs/mcp
- https://linear.app/docs/parent-and-sub-issues
- https://linear.app/changelog/2026-02-05-linear-mcp-for-product-management

Local regression check:

```sh
python3 -m unittest discover -s _bmad/custom/scripts/tests -p 'test_linear_integration.py'
```
