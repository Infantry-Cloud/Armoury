---
stepsCompleted:
  - step-01-preflight-and-context
  - step-02-generation-mode
  - step-03-test-strategy
  - step-04-generate-tests
  - step-04c-aggregate
  - step-05-validate-and-complete
lastStep: step-05-validate-and-complete
lastSaved: '2026-11-11'
storyId: '1.1'
storyKey: 1-1-monorepo-scaffold-with-an-aggregate-local-gate-and-ci
storyFile: _bmad-output/implementation-artifacts/spec-1-1-monorepo-scaffold-with-an-aggregate-local-gate-and-ci.md
atddChecklistPath: _bmad-output/test-artifacts/atdd-checklist-1-1-monorepo-scaffold-with-an-aggregate-local-gate-and-ci.md
contract: STORY-1.1
contractRevision: 1
contractStatus: draft (blocked by OQ-6)
detectedStack: fullstack (target; no manifests exist yet)
generationMode: AI generation (no app exists to record)
executionMode: sequential (seven small scaffolds in one shared checkout; one independent reviewer subagent)
generatedTestFiles:
  - agent-proto/tests/val_2_roundtrip.rs
  - control-plane/tests/val_3_age.rs
  - mise-tasks/check/pins.test.mjs
  - mise-tasks/gen/api.test.mjs
  - mise-tasks/cluster-context.test.mjs
  - web/src/routes/val-4.test.ts
  - web/e2e/smoke.spec.ts
inputDocuments:
  - _bmad-output/implementation-artifacts/spec-1-1-monorepo-scaffold-with-an-aggregate-local-gate-and-ci.md
  - _bmad-output/planning-artifacts/epics.md (Story 1.1, lines 337-386)
  - docs/agent-readiness.md
  - project-context.md
  - _bmad/custom/story-contract.md
  - _bmad/custom/jj-vcs.md
  - _bmad/custom/scripts/validate_story_contract.py
  - _bmad/linear/projects/armoury.json
  - .agents/skills/bmad-testarch-atdd/resources/knowledge/test-quality.md
  - .agents/skills/bmad-testarch-atdd/resources/knowledge/test-levels-framework.md
acceptanceCriteria:
  - { id: AC-1, idSource: supplied, text: 'Fresh clone + mise.local.toml: mise install and mise run check build the Cargo workspace and the SvelteKit app' }
  - { id: AC-2, idSource: supplied, text: 'Every tool, crate, npm dependency, image and action pinned exactly; lockfiles committed; mise.local.toml ignored, example committed' }
  - { id: AC-3, idSource: supplied, text: 'mise run check runs the named steps incl. test-db on the AGE Pod and exits 0; check:fast skips test-db and needs no kube context' }
  - { id: AC-4, idSource: supplied, text: 'Each of nine injected defects makes mise run check exit non-zero and name the step' }
  - { id: AC-5, idSource: supplied, text: 'Each crate, the web app and the chart has a real passing test or lint target' }
  - { id: AC-6, idSource: supplied, text: 'gen:api as a BuildKit stage, repeatable; api step compares without VCS and names an edited file' }
  - { id: AC-7, idSource: supplied, text: 'Digest-pinned multi-stage images, cargo-chef, debug dev profile; agent image has no scanners' }
  - { id: AC-8, idSource: supplied, text: 'mise run dev builds in-cluster, deploys repo:tag@digest, forwards localhost:8080, redeploys with cached deps' }
  - { id: AC-9, idSource: supplied, text: 'mise run e2e smoke passes against a deployment; fails when none is reachable' }
  - { id: AC-10, idSource: supplied, text: 'ci.yml tiers, ci-gate, least privilege (ARC wording superseded by OQ-6)' }
  - { id: AC-11, idSource: supplied, text: 'build.yml builds and packages; pushes to GHCR by digest only on main (ARC wording superseded by OQ-6)' }
  - { id: AC-12, idSource: supplied, text: 'AGENTS.md states ARCH25, layout, PROC3, explicit context; README documents the commands' }
  - { id: AC-13, idSource: supplied, text: 'ci:deploy uses a fresh armoury-ci-* namespace and prints it; ci:teardown deletes it' }
  - { id: AC-14, idSource: supplied, text: 'Cluster tasks fail without ARMOURY_KUBE_CONTEXT and pass it explicitly to every call' }
---

# ATDD Checklist - Epic 1, Story 1.1: Monorepo scaffold with an aggregate local gate and CI

**Contract:** STORY-1.1, Revision 1, Risk medium, Status **draft**. Approval is **blocked by OQ-6**.
**Story file:** `_bmad-output/implementation-artifacts/spec-1-1-monorepo-scaffold-with-an-aggregate-local-gate-and-ci.md`
**ATDD change:** `mmlpxlwq` — `test(story-1.1): add acceptance tests` (this run). The first ATDD run was `qnkkvwmm` (2026-11-06).

The story contract is the requirements oracle. This checklist supports it and does not compete with it.
This run is a full Create after the dev-cluster re-plan (`znmusovo`). It replaces the 2026-11-06 checklist.

## Preflight

| Item | Result |
| --- | --- |
| `validate --phase draft` before ATDD | VALID |
| `validate --phase draft` after the approved edits | VALID |
| `validate --phase approved` | INVALID, as expected: OQ-6 is open and no approval change exists |
| Build status | `ready-for-dev` (CHECKPOINT 1, 2026-11-10) |
| Stack | Target `fullstack` (Rust + SvelteKit). No manifest exists yet. |
| Test framework configured | **No, by design.** This story creates nextest, Vitest, Playwright and the node:test task suite. This is a recorded deviation, not a halt. |
| Linear | `_bmad/linear/projects/armoury.json` has no agreed ATDD obligation for story 1.1. No Linear write was made. |
| Playwright-utils | Not applicable: `@seontechnologies/playwright-utils` is in no `package.json`. One smoke test does not justify it. |
| Knowledge fragments | Selected by the step-01 rule. `test-quality.md` (deterministic, isolated, skip reasons, assertions that can fail) and `test-levels-framework.md` were applied. The data, fixture, network, selector and burn-in fragments do not apply to these scaffolds. |
| Workflow deviations | Scaffolds follow the team rule (one scaffold per mechanical VAL-*, named with its VAL ID; AC IDs in the file header). The upstream rule "one `AC-n` per leaf title" does not apply: planned test names are fixed in the contract. Manual VAL-* rows are checked as procedures. |

## Draft-contract edits (approved by Daniel in this session, 2026-11-11)

| Edit | Change | Reason |
| --- | --- | --- |
| E5 | VAL-5 adds "a `latest` crate feature" and "a missing `mise.local.toml.example`" | AC-2 and the Never list had no check for these |
| E6 | VAL-1 removes the `ARMOURY_KUBE_CONTEXT` line from the copy's `mise.local.toml` and runs `KUBECONFIG=/nonexistent mise run check:fast`; it also reads the AC-1 facts (resolver 3, edition 2024, binaries, Tailwind 4, `@xyflow/svelte`, adapter-static, `components.json`) | mise reloads `mise.local.toml`, so "unset" was not possible; AC-1 facts had no check |
| E7 | VAL-5 adds "a workflow `container:` or `services:` image without `@sha256:`" | AC-2 covers images in workflows |
| E8 | VAL-8 checks that the dev build target uses the debug profile | AC-7 clause had no check |
| E9 | VAL-9 runs `pgrep` for local runtimes before and after, and checks the `SKAFFOLD_DEFAULT_REPO` prefix | "No local runtime" was not observable |
| E10 | VAL-10 negative run is `ARMOURY_E2E_BASE_URL=http://127.0.0.1:9 mise run e2e` | "No deployment reachable" was not exact |
| E12 | VAL-14 checks that each `ci:deploy` output shows its namespace and in-cluster base URL | AC-13 clause had no check |
| OQ-6 | Open Question added: ARC is dropped; CI becomes `mise run ci` on the workstation and on a self-hosted GitHub Actions runner | Decision by Daniel; it needs Correct Course across epics.md, architecture D8 and docs/agent-readiness.md |

## Red-phase scaffolds

| File | Test (planned check name) | VAL / AC | Inactive state | Activated by |
| --- | --- | --- | --- | --- |
| `agent-proto/tests/val_2_roundtrip.rs` | `val_2_generated_message_roundtrip` | VAL-2 / AC-1, AC-5 | `#[ignore = "…"]` line, and no crate exists yet | T2 removes the `#[ignore]` line |
| `control-plane/tests/val_3_age.rs` | `val_3_age_extension_is_available` | VAL-3 / AC-3, AC-5 | `#[ignore = "…"]` line, and no crate exists yet | T3 removes the `#[ignore]` line |
| `web/src/routes/val-4.test.ts` | `VAL-4 root layout disables SSR and uses the static adapter` | VAL-4 / AC-1, AC-5 | `test.skip` | T5 removes `.skip` |
| `mise-tasks/check/pins.test.mjs` | `VAL-5 pins check rejects floating references` | VAL-5 / AC-2 | `test.skip` | T7 removes `.skip` |
| `mise-tasks/gen/api.test.mjs` (new) | `VAL-7 gen:api is repeatable and the api step names an edited generated file` | VAL-7 / AC-6 | `test.skip` | T4 removes `.skip` |
| `web/e2e/smoke.spec.ts` | `loads the web app @VAL-10` | VAL-10 / AC-9 | `test.skip` | T9 removes `.skip` |
| `mise-tasks/cluster-context.test.mjs` (new) | `VAL-15 cluster tasks require and pass an explicit kube context` | VAL-15 / AC-14 | `test.skip` | T12 removes `.skip` |

Changes to the scaffolds from the first run: the Rust files now have `#[ignore]` (the validator handles it since SD-1); VAL-5 is one flat test with 18 defect cases at varied paths; VAL-10 also checks that the client app rendered and threw no page error; comments were updated for the dev cluster.

### Red-phase verification (actual runs, 2026-11-11)

- `node --test mise-tasks/` → `tests 3, skipped 3, fail 0`.
- Each node:test file with `.skip` removed (temporary copy, then deleted) → `fail 1`, for the expected reason:
  - VAL-5: every defect gives `status: null` because `mise-tasks/check/pins` does not exist.
  - VAL-7: `ENOENT` for `api/openapi.yaml` (T4 creates it).
  - VAL-15: `ENOENT` for every cluster task.
- VAL-15 with fake tasks in a temporary directory: a correct set passes. These defects each fail it: skaffold with `--context`, teardown deleting `ARMOURY_NAMESPACE`, and a nested `mise exec`.
- No `val-*` directories were left in `$TMPDIR`. No probe file is in the jj change.
- Rust and web scaffolds cannot run yet: no toolchain, crate or `package.json` exists.
- Locks: for all seven files, removing the skip marker keeps the `lock_digest`, and `is_skipped` detects the marker.
- `node --test --test-reporter=junit mise-tasks/` gives three flat `<testcase>` elements whose names equal the planned names.

### Interfaces the scaffolds impose (Dev must follow them)

- `mise-tasks/check/pins <root>`: exit 0 when clean; exit 1 and print the offending path. It finds files by kind: `Dockerfile` and `*.Dockerfile`, every `Cargo.toml`, Kubernetes manifests, workflows. Name `.gitignore` when `mise.local.toml` is not ignored. On this repository, skip `_bmad/`, `.agents/` (it holds a template workflow), `node_modules/`, `target/`, `.jj/` and `.git/`. Accept mise inline-table pins (`codeql`) and Helm-templated `image:` lines.
- `mise-tasks/gen/api [ROOT]` and `mise-tasks/check/api [ROOT]`: see the header of `api.test.mjs`. Set `BUILDX_GIT_INFO=false`, or the `git` shim records a call (correct red). The test copies only `api/openapi.yaml`.
- Cluster tasks (`check/test-db`, `dev`, `ci/deploy`, `ci/teardown`): plain executables that call `kubectl --context`, `helm --kube-context`, `skaffold --kube-context` and `cargo` directly, never `mise`, `docker` or `buildx`. `ci/teardown` takes the namespace as `$1` or `ARMOURY_CI_NAMESPACE`.
- VAL-2 needs `armoury.agent.v1.Heartbeat { string agent_id = 1; }` as `agent_proto::v1`. VAL-10 needs the page title and visible text to contain "Armoury".

## AC → VAL → artifact map

| AC | VAL | Method | Artifact or procedure | Owner |
| --- | --- | --- | --- | --- |
| AC-1 | VAL-1, VAL-2, VAL-4 | manual + mechanical | fresh-copy record (E6); `agent-proto/tests/val_2_roundtrip.rs`; `web/src/routes/val-4.test.ts` | Dev |
| AC-2 | VAL-5 | mechanical | `mise-tasks/check/pins.test.mjs` | Dev |
| AC-3 | VAL-1, VAL-3 | manual + mechanical | fresh-copy record; `control-plane/tests/val_3_age.rs` | Dev |
| AC-4 | VAL-6 | manual | nine-defect observation record | Dev (Code Review repeats at least one) |
| AC-5 | VAL-1, VAL-2, VAL-3, VAL-4 | manual + mechanical | as above | Dev |
| AC-6 | VAL-7 | mechanical | `mise-tasks/gen/api.test.mjs` | Dev |
| AC-7 | VAL-8 | manual | image listing record (E8) | Test Architect |
| AC-8 | VAL-9 | manual | dev-loop observation record (E9) | Test Architect |
| AC-9 | VAL-10 | mechanical | `web/e2e/smoke.spec.ts` + saved negative run (E10) | Dev |
| AC-10 | VAL-11 | manual | **blocked by OQ-6** | Test Architect |
| AC-11 | VAL-12 | manual | **blocked by OQ-6** | Test Architect |
| AC-12 | VAL-13 | manual | documentation walk-through | Test Architect |
| AC-13 | VAL-14 | manual | two-namespace observation record (E12) | Dev |
| AC-14 | VAL-15 | mechanical | `mise-tasks/cluster-context.test.mjs` | Dev |

Evidence location for all records: `_bmad-output/implementation-artifacts/evidence/1-1/`.
Manual rows VAL-1, 6, 8, 9, 13 and 14 each have an exact procedure, an observable oracle, evidence, an owner and a reason. VAL-11 and VAL-12 must be rewritten by Correct Course.

## Test Architect review

An independent reviewer (fresh-context subagent) challenged the design. All three of its blockers were resolved in this session: B1 by E6, B2 by the VAL-15 rewrite, and B3 by E5, E7, E8 and E12. Its should-fix items were applied to the scaffolds or the contract (E9, E10). The VAL-11 fallback item became OQ-6.

### Approval blockers

- **OQ-6 (open).** ARC is dropped. CI becomes one task, `mise run ci`, that runs the whole pipeline on the workstation and on a self-hosted GitHub Actions runner. Run `bmad-correct-course`. It must update `epics.md` Story 1.1, architecture D8, `docs/agent-readiness.md` (D8, CI design, threat model, Contract CI Wiring "Runs in"), Boundaries, Assumptions, OQ-5, AC-10, AC-11, VAL-11 and VAL-12. It must also decide whether `ci` belongs in the AC-14 cluster task list. If it does, VAL-15 needs a Test Architect re-check before approval, because the test is not locked yet.
- **CI NAMING CHECK.** The names follow the Contract CI Wiring convention (`val_<n>_…`, `VAL-<n> …`, `@VAL-10`). The JUnit adapter and the contract step are AR phase 3 work (SD-2). The suites they run in change with OQ-6, so check them again after Correct Course.

### Residual risks for Dev (no contract change)

- **R4.** The `api` drift check must not use jj or git (CI has no jj workspace before setup; VAL-1 copies have no VCS). VAL-7 enforces this.
- **R5.** `mise-tasks/check` holds both the gate and its steps: use `check/_default` for the gate and `check/pins` for the checker. A non-executable `*.test.mjs` file is not a task.
- **R6.** Exact pins: `sv create` and `npm install` write `^` ranges. Add `save-exact=true` to `web/.npmrc`. Use `cargo … --locked` and `npm ci` in the gate.
- **R8.** VAL-3 must be in the nextest database group (run by `test-db`, not `test-rust`). No locked file holds this rule; only CI results catch a mismatch.
- **R9.** Vitest `include` must leave out `web/e2e/*.spec.ts`.
- **R10.** VAL-7 runs six BuildKit runs inside `check:fast`; record the time against the budget in `docs/agent-readiness.md`.
- **R11.** Pin Node 22 or newer (`Dirent.parentPath` in VAL-7).
- Obsolete: R1 and R3 (Podman/kind) and R2 (Rust markers, fixed by SD-1). R7 (JUnit identity) moves to AR phase 3.

## Implementation checklist (per task)

- [ ] T1: pin the toolchain exactly, add `mise.local.toml.example` and the `.gitignore` entry. VAL-5 activates in T7.
- [ ] T2: workspace, lints, `proto/agent/v1/agent.proto`. Remove `#[ignore]` from VAL-2; show red, then green.
- [ ] T3: `control-plane`, `agent`, `check/test-db` and the AGE Pod manifest. Remove `#[ignore]` from VAL-3; red, then green in `test-db`.
- [ ] T4: `api/openapi.yaml`, `gen/api`, `check/api`. Remove `.skip` from VAL-7; red, then green.
- [ ] T5: web app. Remove `.skip` from VAL-4; red, then green.
- [ ] T6: chart and `helm lint`.
- [ ] T7: `check/_default`, `check/fast`, the other steps and `check/pins`. Remove `.skip` from VAL-5; red, then green. Run the VAL-6 demonstration.
- [ ] T8: Dockerfiles (VAL-8 is for the reviewer).
- [ ] T9: Skaffold, `image/build`, `dev`, `e2e`, `ci/deploy`, `ci/teardown`, `playwright.config.ts` (`ARMOURY_E2E_BASE_URL`, no `webServer`). Remove `.skip` from VAL-10; save the negative run.
- [ ] T10: workflows (after OQ-6 Correct Course).
- [ ] T11: `AGENTS.md`, `README.md`.
- [ ] T12: context guards. Remove `.skip` from VAL-15; red, then green.

After approval, the only allowed edit to a locked scaffold is removing its skip marker.

## Running the tests

```sh
node --test mise-tasks/                                    # VAL-5, VAL-7, VAL-15 (test-tasks step)
cargo nextest run -p agent-proto                           # VAL-2
mise run check                                             # VAL-3 runs in the test-db step
npm --prefix web run test -- --run src/routes/val-4.test.ts  # VAL-4
mise run e2e                                               # VAL-10 against mise run dev
```

## Status and next step

The contract stays **draft**. No approval change was made, and no test is locked.
Next: `bmad-correct-course` for OQ-6. Then run ATDD in Validate or Edit mode to re-check VAL-11, VAL-12 and VAL-15. Then Daniel gives explicit product approval, and the separate JJ APPROVAL change records the digest and the `### Locked Tests` table.
