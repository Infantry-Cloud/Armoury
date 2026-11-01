# Linear integration and contract/ATDD rollout

Armoury is now fully synced with `bmad-customisations/sync.sh` (all shared customisations,
including the Guardrail Steward agent and the contract edit guard).

## Installed

- `.agents/skills/bmad-linear/SKILL.md`: explicit Kickoff, Reconcile and Run an agreed step.
- `.mcp.json` and `.pi/mcp.json`: secret-free official Linear HTTP MCP connection.
- `_bmad/custom/linear-workflow.md`, `linear-setup.md`, `linear-mcp.json`: shared references.
- LP menus on analyst, PM, architect and dev; AR menus load one shared AR workflow.
- `_bmad/custom/story-contract.md`: acceptance, approval, validation and evidence rules.
- `_bmad/custom/scripts/validate_story_contract.py` and its runnable regression tests.
- Contract-aware Build, Build Auto, ATDD, TEA test-design/automation/test-review/trace,
  QA generation, Code Review, Correct Course and Sprint Planning overrides.
- Dev/TEA contract guidance and the contract-validator integration instructions in AR.
- `_bmad/custom/jj-vcs.md` and its wiring (Build, Build Auto, ATDD, Code Review, TEA/QA,
  Correct Course, Sprint Planning, Walkthrough, dev agent, project context): agents use jj,
  never git, and may only run `jj new`/`jj describe`. Armoury is a colocated jj workspace
  (jj over a Git backend), so agents follow `jj-vcs.md` directly.
- Contract approval as its own sealed jj change (`story-contract.md`, "Approval change (jj)"):
  approved/delivered validation compares the contract with that recorded version, with the
  digest field as a fallback where no jj history is available; CI should pass `--require-jj`.

No installed BMAD skill bodies, personal configuration or readiness extension were
replaced. No files were deleted, existing stories rewritten, approvals fabricated,
or remote Linear projects/issues created. Legacy overrides are retained, but direct
implementation through dev-story is halted in favour of `bmad-build`. The installed
quick-dev compatibility shim may request a legacy-file migration: do not approve an
automatic replacement/deletion as part of this rollout; invoke `bmad-build` directly.

## Use from Armoury

Grant project trust in Pi if needed, then `/reload`. Inspect `/mcp` and, if Linear
requires sign-in, use `/mcp login linear`. Authentication remains outside the repo.
If a replacement MCP adapter owns `/mcp`, configure it to use the root `.mcp.json`
according to its own documentation; native Pi uses `.pi/mcp.json`.

Invoke `bmad-linear` or choose LP to confirm the workspace/team, named project,
smallest agreed plan and publishing permission. Use Reconcile to backfill approved
work or recover an interrupted publish. Existing IDs must be reused, not recreated.

The installed contract workflows include their shared Linear activation/completion
instructions. AR also has its shared tracking instructions. These execute only when
the relevant workflow runs; installation itself performs no remote publishing.
Unrelated planning-workflow callbacks remain deferred: use the explicit Linear
skill to reconcile those steps. These are agent instructions, not a sync daemon.

## Tracked-story workflow

1. Run `bmad-build` to plan the contract. At the planning checkpoint, approve and stop.
2. Run `bmad-testarch-atdd` with the Build spec path. Review the validation design,
   create red-phase scaffolds and obtain explicit product plus Test Architect approval.
3. Resume `bmad-build` with the spec path. Approved-phase validation must pass before coding.
4. Run TEA Test Review when risk/test sensitivity requires it, then `bmad-code-review`.
   Code Review records independently verified delivery evidence and runs delivered validation.
5. Use Correct Course for changed approved requirements; do not rewrite the contract to fit code.

No real story was planned, approved, implemented or accepted by this deployment.
Use the proportional micro-contract rules in `story-contract.md` for untracked work.

## Checks and enforcement boundary

Run the deployed validator regression suite from Armoury:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s _bmad/custom/scripts/tests -p 'test_validate_story_contract.py'
```

Run the validator's draft/approved/delivered commands from `story-contract.md` at
those lifecycle points. Its tests prove local structural and drift checks, not the
correctness of real requirements, real test results, remote publishing or a complete
agent-run lifecycle. Independent review remains necessary.

Syncing files does not create required CI checks, branch protection or a validated
agent environment. AR must wire the validator into the target project's aggregate
local command and protected CI/repository gates, then prove that invalid contracts
actually block. Workflow TOML instructions alone are not hard enforcement.

Re-sync with `bmad-customisations/sync.sh --dry-run armoury` first, then with `--backup-dir`.
It mirrors `_bmad/custom/` with deletions; personal `*.user.toml` files are kept.
