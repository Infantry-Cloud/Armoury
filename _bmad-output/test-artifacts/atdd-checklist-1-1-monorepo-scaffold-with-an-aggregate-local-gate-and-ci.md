---
stepsCompleted:
  - step-01-preflight-and-context
  - step-02-generation-mode
  - step-03-test-strategy
  - step-04-generate-tests
  - step-04c-aggregate
  - step-05-validate-and-complete
  - edit/step-01-assess
  - edit/step-02-apply-edit
lastStep: edit/step-02-apply-edit
lastSaved: '2026-11-13'
storyId: '1.1'
storyKey: 1-1-monorepo-scaffold-with-an-aggregate-local-gate-and-ci
storyFile: _bmad-output/implementation-artifacts/spec-1-1-monorepo-scaffold-with-an-aggregate-local-gate-and-ci.md
atddChecklistPath: _bmad-output/test-artifacts/atdd-checklist-1-1-monorepo-scaffold-with-an-aggregate-local-gate-and-ci.md
contract: STORY-1.1
contractRevision: 1
contractStatus: draft (ready for product approval)
detectedStack: fullstack (target; no manifests exist yet)
generationMode: AI generation (no app exists to record)
executionMode: sequential (one writer; two independent reviewer subagents)
generatedTestFiles:
  - agent-proto/tests/val_2_roundtrip.rs
  - control-plane/tests/val_3_age.rs
  - web/src/routes/val-4.test.ts
  - mise-tasks/check/pins.test.mjs
  - mise-tasks/gen/api.cluster.test.mjs
  - web/e2e/smoke.spec.ts
  - mise-tasks/cluster-context.test.mjs
  - mise-tasks/ci/ci.test.mjs
inputDocuments:
  - _bmad-output/implementation-artifacts/spec-1-1-monorepo-scaffold-with-an-aggregate-local-gate-and-ci.md
  - _bmad-output/planning-artifacts/epics.md (Story 1.1, lines 337-387)
  - _bmad-output/planning-artifacts/sprint-change-proposal-2026-11-12.md
  - docs/agent-readiness.md
  - project-context.md
  - _bmad/custom/story-contract.md
  - _bmad/custom/jj-vcs.md
  - _bmad/custom/linear-workflow.md
  - _bmad/custom/scripts/validate_story_contract.py
  - _bmad/linear/projects/armoury.json
acceptanceCriteria:
  - { id: AC-1, idSource: supplied, text: 'Fresh clone + mise.local.toml: mise install and mise run check build the Cargo workspace, the SvelteKit app; umbrella chart and api/openapi.yaml exist' }
  - { id: AC-2, idSource: supplied, text: 'Every tool, crate, npm dependency, image (incl. Okteto manifests) and action pinned exactly; lockfiles committed; mise.local.toml ignored, example committed' }
  - { id: AC-3, idSource: supplied, text: 'mise run check runs fast then cluster steps (api, test-db run-unique Pod, test-tasks-cluster, codeql) and exits 0; check:fast needs no context' }
  - { id: AC-4, idSource: supplied, text: 'Each of nine injected defects makes mise run check exit non-zero and name the step' }
  - { id: AC-5, idSource: supplied, text: 'Each crate, the web app and the chart has a real passing test or lint target' }
  - { id: AC-6, idSource: supplied, text: 'gen:api through okteto test artifacts, repeatable; api step compares without VCS and names an edited file' }
  - { id: AC-7, idSource: supplied, text: 'Digest-pinned multi-stage images built by okteto build, cargo-chef, debug dev stage; agent image has no scanners' }
  - { id: AC-8, idSource: supplied, text: 'mise run dev runs okteto up: builds on Okteto, deploys by digest, dev container, localhost:8080, cached deps' }
  - { id: AC-9, idSource: supplied, text: 'Playwright smoke passes against an Okteto deployment; mise run e2e fails when none is reachable' }
  - { id: AC-10, idSource: supplied, text: 'ci.yml: one mise run ci:<tier> per job, ARC jobs only for push and same-repo PRs, ci-gate always runs, least privilege' }
  - { id: AC-11, idSource: supplied, text: 'build.yml: ci:build on ARC; ci:publish main only copies digests to GHCR with crane' }
  - { id: AC-12, idSource: supplied, text: 'AGENTS.md states ARCH25, layout, PROC3, explicit context; README documents the commands and Okteto prerequisites' }
  - { id: AC-13, idSource: supplied, text: 'ci:e2e uses a fresh armoury-ci-* namespace or the pr-<n> preview; cleanup on failure; preview-cleanup.yml for same-repo PRs' }
  - { id: AC-14, idSource: supplied, text: 'Okteto/kubectl tasks guard and pass explicit contexts and namespaces; no task removes what it does not own' }
  - { id: AC-15, idSource: supplied, text: 'mise run ci runs ci:fast, ci:cluster, ci:e2e in order, stops at the first failure and names it' }
  - { id: AC-16, idSource: supplied, text: 'codeql step: local databases, pinned code-scanning packs, no upload, any result fails, reasoned dismissals' }
  - { id: AC-17, idSource: supplied, text: 'mise run renovate dry run without token lists every dependency kind; renovate.yml keeps exact pins' }
---

# ATDD Checklist - Epic 1, Story 1.1: Monorepo scaffold with an aggregate local gate and CI

**Contract:** STORY-1.1, Revision 1, Risk medium, Status **draft**. B6 is resolved (SD-6). The contract waits for product approval.
**Story file:** `_bmad-output/implementation-artifacts/spec-1-1-monorepo-scaffold-with-an-aggregate-local-gate-and-ci.md`
**ATDD change:** `wsqtxwxm`, `test(story-1.1): add acceptance tests` (this Edit run, 2026-11-13). Earlier runs: `qnkkvwmm` (2026-11-06) and `mmlpxlwq` (2026-11-11).

The story contract is the requirements oracle. This checklist supports it and does not compete with it.
This run is an ATDD **Edit** after Correct Course 2026-11-12 (Okteto, mise-only CI) and the Build re-plan `knkuuyxl`. It replaces the 2026-11-11 checklist.

## Preflight

| Item | Result |
| --- | --- |
| `validate --phase draft` before the edits | VALID |
| `validate --phase draft` after the approved edits | VALID |
| Build status | `ready-for-dev` (CHECKPOINT 1, 2026-11-12) |
| Mode | Edit. The spec's Code Map listed the required ATDD edits. |
| Stack | Target `fullstack` (Rust + SvelteKit + mise task tests). No manifest exists yet. |
| Test framework configured | **No, by design.** This story creates nextest, Vitest, Playwright and the node:test task suites. This is a recorded deviation, not a halt. |
| Linear | `_bmad/linear/projects/armoury.json` has no agreed ATDD obligation for story 1.1 (INF-23 is the story). No Linear write was made. |
| Workflow deviations | One scaffold per mechanical VAL-*, named with its VAL ID; AC IDs are in the file header. Planned test names are fixed in the contract. Manual VAL-* rows are checked as procedures. |

## Independent review and decisions (2026-11-13)

A fresh-context reviewer challenged the draft contract. Daniel decided the open points and approved all recommended edits in this session. The contract records them under "Decisions (user, 2026-11-13, TEA ATDD Edit)" and in the Spec Change Log.

| ID | Finding | Resolution |
| --- | --- | --- |
| B1 | No explicit-namespace or data-loss oracle | AC-14 and VAL-15: explicit namespaces, `ARMOURY_NAMESPACE` guard, only own namespaces and the AGE Pod are removed |
| B2 | `preview-cleanup.yml` had no fork guard; D13 control missing | AC-13 same-repository `if:` and permissions; Assumption on outside-collaborator approval; VAL-11 inspects instead of a live fork run (Daniel) |
| B3 | A skipped `ci-gate` passes a ruleset | AC-10: `ci-gate` always runs; VAL-11 checks the red run's `ci-gate` is `failure` |
| B4 | Okteto 3.25.0 runs `git` inside a Git repository (`pkg/repository.LocalGit`, confirmed with `strings`) | Boundaries and VAL-7 header: run `okteto test` from a temporary directory outside the repository |
| B5 | CodeQL terms need an OSI licence; no `LICENSE` exists (confirmed in the CodeQL 2.27.4 `LICENSE.md`) | Assumption: an OSI licence (OI-1) is committed before T13 (Daniel) |
| B6 | Contract CI Wiring has no `test-tasks-cluster` report, and its task-test command also picks up `*.cluster.test.mjs` | Resolved by Vera, SD-6 (change `oyqnzyns`): one report per step and a hosted `contracts` job. AC-10/VAL-11 edited in change `rppznkzx` (Daniel approved) to allow the report steps; `ci-gate` needs every other job. |
| SF-1..16 | AC-1 chart clause; AC-3 globs and Pod cleanup; cleanup on failure; VAL-15 inputs; main-only `ci:publish` (Daniel: main only, Okteto credentials); YAML wording; VAL-5/6/8/9/12/17/18 oracles; AC-16 suite; AC-17 dry run | Applied to the contract and the scaffolds |

A second fresh-context review of the edited contract and scaffolds found three more blockers. Daniel approved the fixes C1-C9 in this session:

| ID | Finding | Resolution |
| --- | --- | --- |
| C1 | Okteto 3.25.0 has no `--context` on `namespace`, `context show`, `kubeconfig` and `registrytoken` (confirmed with `--help`) | AC-14: those commands run with `OKTETO_CONTEXT="$ARMOURY_OKTETO_CONTEXT"`; VAL-15 accepts that form only for them |
| C2 | `okteto --context X deploy` bypassed the namespace and destroy checks | VAL-15: every `okteto` call starts with its subcommand |
| C3 | `test-db` could delete anything in the developer namespace | AC-14/VAL-15: only `kubectl delete pod <name>` of a Pod the run named earlier; no `--all`, selector, `-f`, `okteto down --volumes` or `okteto destroy` there |
| C4 | `okteto namespace create` defaults to `--use=true` | AC-14/VAL-15: `--use=false` |
| C5 | VAL-15 allowed `git`/`jj` | Failing `git` and `jj` shims |
| C6 | Okteto runs `git` itself inside the checkout | Never list: git commands issued by a task or an agent; AC-6 stays strict for `gen:api`/`api` |
| C7 | GitHub renamed the setting | "all external contributors", saved from the Actions settings |
| C8 | Cleanup-on-failure checks could pass without the failing call | VAL-15 asserts `cargo` and `okteto test` ran; the port-forward shim prints its ready line |
| C9 | AC-3 Pod cleanup on interrupt had no check | The `cargo` shim sends SIGINT to `test-db`; the Pod is still deleted |

`ci:publish` is not a release. It copies each `main` build's images by digest from the Okteto Registry to GHCR. Releases, signing and chart publication stay in Epic 10.

## Red-phase scaffolds

| File | Test (planned check name) | VAL / AC | Inactive state | Activated by |
| --- | --- | --- | --- | --- |
| `agent-proto/tests/val_2_roundtrip.rs` | `val_2_generated_message_roundtrip` | VAL-2 / AC-1, AC-5 | `#[ignore = "…"]` line; no crate yet | T2 removes the `#[ignore]` line |
| `control-plane/tests/val_3_age.rs` | `val_3_age_extension_is_available` | VAL-3 / AC-3, AC-5 | `#[ignore = "…"]` line; no crate yet | T3 removes the `#[ignore]` line |
| `web/src/routes/val-4.test.ts` | `VAL-4 root layout disables SSR and uses the static adapter` | VAL-4 / AC-1, AC-5 | `test.skip` | T5 removes `.skip` |
| `mise-tasks/check/pins.test.mjs` | `VAL-5 pins check rejects floating references` | VAL-5 / AC-2 | `test.skip` | T7 removes `.skip` |
| `mise-tasks/gen/api.cluster.test.mjs` (moved) | `VAL-7 gen:api is repeatable and the api step names an edited generated file` | VAL-7 / AC-6 | `test.skip` | T4 removes `.skip` |
| `web/e2e/smoke.spec.ts` | `loads the web app @VAL-10` | VAL-10 / AC-9 | `test.skip` | T9 removes `.skip` |
| `mise-tasks/cluster-context.test.mjs` (rewritten) | `VAL-15 cluster tasks require and pass an explicit Okteto and kube context` | VAL-15 / AC-14 | `test.skip` | T12 removes `.skip` |
| `mise-tasks/ci/ci.test.mjs` (new) | `VAL-16 mise run ci runs the CI tiers in order and stops at the first failure` | VAL-16 / AC-15 | `test.skip` | T10 removes `.skip` |

Changes in this Edit:

- **VAL-5:** Okteto manifest fixtures (`okteto.yaml` with a `${OKTETO_BUILD_CONTROL_PLANE_DEV_IMAGE}` dev image, `mise-tasks/gen/okteto.yml` with the generator test image). There are two new Okteto defects and three new npm defects (`*`, `>=`, `latest`). The clean tree has a `FROM build AS dev` stage. Workflows use `jdx/mise-action`. There are now 21 defect cases, and each `pins` run has a 60 s timeout.
- **VAL-7:** moved to the cluster tier. It uses `okteto test` instead of `buildx`. It adds `docker`, `podman` and `buildx` shims that fail if called, and a deleted-file drift case.
- **VAL-15:** rewritten for `okteto`/`kubectl` and the eight AC-14 tasks (nine cases: `ci:e2e` runs locally and for a pull request). It checks explicit namespaces, the `ARMOURY_NAMESPACE` guard, cleanup on failure, run-unique Pods, the main-only publish guard and the data-loss rule.
- **VAL-16:** new. The four cases are: no failure, then each tier failing.
- **VAL-3, VAL-10:** comments only (Okteto namespace Pod; `ci:e2e` instead of `ci:deploy`).

### Red-phase verification (actual runs, 2026-11-13)

- `node --test mise-tasks/` gives `tests 4, skipped 4, fail 0`.
- With `.skip` removed (a temporary copy, then deleted), each node:test file gives `fail 1` for the expected reason:
  - VAL-5: `status: null` for every case, because `mise-tasks/check/pins` does not exist.
  - VAL-7 and VAL-15: `ENOENT` for `api/openapi.yaml` (T4 creates it).
  - VAL-16: `ENOENT` for `mise-tasks/ci/_default`.
- **Proof after the second review (C1-C9):** the correct fake set passes VAL-15. Each of these 19 defects fails it:
  - flags before the subcommand (a hidden `deploy` without `-n`, and a hidden `destroy --volumes`);
  - `delete pods --all`, `delete deployment`, deleting a Pod the task did not create, `delete -f`;
  - `okteto down --volumes` in the developer namespace;
  - `namespace create` without `--use=false` or without `OKTETO_CONTEXT`, and `deploy` with only `OKTETO_CONTEXT`;
  - no cleanup on an `okteto test` failure; no Pod cleanup; dying on SIGINT without cleanup;
  - a TCP probe so `cargo` never runs; a fixed Pod name; a `git` call;
  - `registrytoken` without a context; no main guard; `build` without a namespace.
  - A task that ignores SIGINT but still exits and deletes its Pod passes. This is correct, because the oracle only needs the cleanup.
- **First proof (before the second review):** I ran VAL-15 and VAL-16 against fake tasks in a temporary tree.
  - A correct set passes both tests.
  - Each of these defects fails VAL-15: no `--context`; the kube context passed to `okteto`; no namespace; no `ARMOURY_NAMESPACE` guard; no context guard; `helm upgrade`; no cleanup on `okteto test` failure; `okteto destroy -n $ARMOURY_NAMESPACE`; `okteto namespace delete $ARMOURY_NAMESPACE`; the wrong preview; a nested `mise run`; a fixed Pod name; no Pod cleanup; no main-only guard; a `kubectl delete` in the developer namespace; a `docker` call.
  - Each of these defects fails VAL-16: it continues after a failure; it does not name the tier; the wrong order; an extra `ci:build`.
- **Locks:** for all eight files, removing the skip marker keeps the `lock_digest`. `is_skipped` detects the marker before removal and not after.
- `node --test --test-reporter=junit` gives flat `<testcase>` names equal to the planned names.
- No `val-*` temporary directory was left, and no probe file is in the jj change.
- The Rust, web and Playwright scaffolds cannot run yet: no toolchain, crate or `package.json` exists.

### Interfaces the scaffolds impose (Dev must follow them)

- **`mise-tasks/check/pins <root>`:** exits 0 when the tree is clean, or 1 and prints the offending path.
  - It finds files by kind: `Dockerfile` and `*.Dockerfile`, every `Cargo.toml`, Kubernetes manifests, Okteto manifests (`okteto.yml`/`okteto.yaml` in any directory) and workflows.
  - In an Okteto manifest, it accepts `@sha256:` or `${OKTETO_BUILD_<NAME>_IMAGE}`. It accepts `FROM <earlier stage>`, mise inline-table pins and Helm-templated `image:` lines.
  - On this repository it skips `_bmad/`, `.agents/`, `node_modules/`, `target/`, `.jj/` and `.git/`.
  - It names `.gitignore` when `mise.local.toml` is not ignored.
- **`mise-tasks/gen/api [ROOT]` and `mise-tasks/check/api [ROOT]`:**
  - They run `okteto test` from a temporary directory outside the repository that holds only the spec and the generator manifest.
  - `check/api` names each differing, missing or extra file.
  - The test copies only `api/openapi.yaml`.
- **Okteto calls:**
  - The subcommand comes first.
  - `build`/`deploy`/`destroy`/`down`/`endpoints`/`preview`/`test`/`up` pass `--context`.
  - `namespace`/`context show`/`kubeconfig`/`registrytoken` run with `OKTETO_CONTEXT="$ARMOURY_OKTETO_CONTEXT"`.
  - `namespace create` passes `--use=false`.
- **The AC-14 tasks** are `gen/api`, `check/api`, `check/test-db`, `dev`, `ci/e2e`, `ci/build`, `ci/publish` and `ci/preview-destroy`.
  - They are plain executables. They find the repository from their own path or `MISE_PROJECT_ROOT`.
  - They call `okteto`, `kubectl`, `helm`, `cargo`, `crane`, `npm` and `npx` directly, never `mise`, `git`, `jj`, `docker`, `podman`, `buildx`, `skaffold` or `kind`.
  - Each task has one guard line per variable it needs (`ARMOURY_OKTETO_CONTEXT`, `ARMOURY_KUBE_CONTEXT`, `ARMOURY_NAMESPACE`), before any `okteto` or `kubectl` call.
  - Every `okteto` `build`/`deploy`/`destroy`/`down`/`endpoints`/`test`/`up` call and every `kubectl` call passes `-n`.
  - Each task bounds its own waits (60 s against the shims).
- **CI inputs** come from the standard GitHub variables: `GITHUB_EVENT_NAME`, `GITHUB_EVENT_PATH` (the pull request number), `GITHUB_REF`, `GITHUB_REPOSITORY` and `GITHUB_REPOSITORY_OWNER`.
- **`ci/publish`:**
  - It reads `ARMOURY_CONTROL_PLANE_IMAGE` and `ARMOURY_AGENT_IMAGE` (`repository@sha256:…`), which come from the `build` job outputs.
  - It exits non-zero before any `crane` call unless `GITHUB_REF=refs/heads/main`.
  - It makes an `okteto` call with `--context` for the registry credentials.
- **`check/test-db`:**
  - It uses a run-unique Pod name that appears in its port-forward and in `kubectl delete pod <name>`.
  - It treats the `Forwarding from` line as ready (no TCP probe), then runs `cargo`.
  - It deletes the Pod on exit, on failure and on SIGINT. Trap `INT` and `TERM` too: Linux `/bin/sh` (dash) does not run an `EXIT` trap on a signal.
- **`ci/e2e`:** it deletes its `armoury-ci-*` namespace also when `okteto test` fails.
- **`ci/_default`:** it calls exactly `mise run ci:fast`, `mise run ci:cluster` and `mise run ci:e2e` in order, and prints the failing tier.
- **VAL-2** needs `armoury.agent.v1.Heartbeat { string agent_id = 1; }` as `agent_proto::v1`. **VAL-10** needs the page title and the visible text to contain "Armoury".

## AC → VAL → artifact map

| AC | VAL | Method | Artifact or procedure | Owner |
| --- | --- | --- | --- | --- |
| AC-1 | VAL-1, VAL-2, VAL-4 | manual + mechanical | fresh-copy record (now with the chart and `api/openapi.yaml`); `agent-proto/tests/val_2_roundtrip.rs`; `web/src/routes/val-4.test.ts` | Dev |
| AC-2 | VAL-5 | mechanical | `mise-tasks/check/pins.test.mjs` | Dev |
| AC-3 | VAL-1, VAL-3 (+ VAL-15 for the `test-db` Pod) | manual + mechanical | fresh-copy record; `control-plane/tests/val_3_age.rs` | Dev |
| AC-4 | VAL-6 | manual | nine-defect record with the step map | Dev |
| AC-5 | VAL-1, VAL-2, VAL-3, VAL-4 | manual + mechanical | as above | Dev |
| AC-6 | VAL-7 | mechanical (cluster tier) | `mise-tasks/gen/api.cluster.test.mjs` | Dev |
| AC-7 | VAL-8 | manual | image file-list difference record | Test Architect |
| AC-8 | VAL-9 | manual | dev-loop record (restart, `pgrep -x`) | Test Architect |
| AC-9 | VAL-10 | mechanical | `web/e2e/smoke.spec.ts` + saved negative run | Dev |
| AC-10 | VAL-11 | manual | CI run record, `ci-gate` conclusion, approval-setting record | Test Architect |
| AC-11 | VAL-12 | manual | `build.yml` runs and digest comparison | Test Architect |
| AC-12 | VAL-13 | manual | documentation walk-through | Test Architect |
| AC-13 | VAL-11, VAL-14 | manual | CI preview record; three-run namespace record | Dev / Test Architect |
| AC-14 | VAL-15 | mechanical | `mise-tasks/cluster-context.test.mjs` | Dev |
| AC-15 | VAL-16 | mechanical | `mise-tasks/ci/ci.test.mjs` | Dev |
| AC-16 | VAL-17 | manual | CodeQL injection record | Dev |
| AC-17 | VAL-18 | manual | Renovate dry run without a token, plus a workflow run | Test Architect |

Evidence location for all records: `_bmad-output/implementation-artifacts/evidence/1-1/`.
Every manual row has an exact procedure, an observable oracle, evidence, an owner and a reason.

## CI naming check (passes, 2026-11-13)

| VAL | Planned test | Suite and step | Report | Job |
| --- | --- | --- | --- | --- |
| VAL-2 | `val_2_generated_message_roundtrip` | nextest, `test-rust` | `rust.xml` | `cluster` |
| VAL-3 | `val_3_age_extension_is_available` | nextest, `test-db` | `rust-db.xml` | `cluster` |
| VAL-4 | `VAL-4 root layout …` | Vitest, `web` | `web-unit.xml` | `cluster` |
| VAL-5, VAL-15, VAL-16 | `VAL-5 …`, `VAL-15 …`, `VAL-16 …` | node:test, `test-tasks` | `tasks.xml` | `cluster` |
| VAL-7 | `VAL-7 …` | node:test, `test-tasks-cluster` | `tasks-cluster.xml` | `cluster` |
| VAL-10 | `loads the web app @VAL-10` | Playwright through `okteto test`, `ci:e2e` | `e2e.xml` | `e2e` |

- Every report goes to the hosted `contracts` job, which runs `ci:contracts` with all six reports (SD-6).
- I ran the globs on this repository. The fast glob runs VAL-5, VAL-15 and VAL-16. The cluster glob runs only VAL-7, with its planned name.
- Contract and full test identity come from the JUnit adapter `mise-tasks/ci/junit-contract`. It is designed but not built: AR phase 3 builds it before Code Review of Story 1.1 (SD-2). If it is missing, delivered-phase validation fails, so this is not an approval blocker.
- **Recorded for AR phase 3:** the `okteto test` artifacts land inside the workspace, so `ci:e2e` must move `e2e.xml` out before upload.

## Residual risks for Dev (no contract change)

- **R4.** The `api` drift check uses no VCS, and neither does Okteto (run it outside the repository). VAL-7 enforces this. If Okteto still runs `git` outside a repository, route it to Correct Course.
- **R5.** `mise-tasks/check` holds the gate and its steps: `check/_default` is the gate, and `check/pins` is the checker. `mise-tasks/ci/_default` is `mise run ci`. A non-executable `*.test.mjs` file is not a task.
- **R6.** Exact pins: add `save-exact=true` to `web/.npmrc`. Use `cargo … --locked` and `npm ci` in the gate.
- **R8.** VAL-3 must be in the nextest database group (`test-db`, not `test-rust`).
- **R9.** Vitest `include` must leave out `web/e2e/*.spec.ts`.
- **R10.** VAL-7 makes seven `okteto test` runs. Record the `test-tasks-cluster` time against the budget. Concurrent runs share `ARMOURY_NAMESPACE`, so give each `okteto test` run a unique name if Okteto collides.
- **R11.** Node 26.13.1 is pinned (`Dirent.parentPath` needs 22 or newer).
- **R12.** `agent-proto` needs `protoc` (or `protox`) on the workstation and in the builder images. It is not in the T1 pin list.
- **R13.** Chart image values: use no floating default. Make the digest required at render time or set it from the Okteto build output.
- **R14.** `okteto namespace create` and `okteto up` may change the current Okteto or kube context. The tasks are not affected, but `AGENTS.md` should say so.
- **R15.** The repository is public. The ARC runner group must allow public repositories, or the ARC jobs never start (Daniel, outside the repository).
- **Source deviation (accepted at CHECKPOINT 1):** epics.md says CI runs `mise run e2e`. The contract runs the same spec through `okteto test` inside `ci:e2e`.

## Implementation checklist (per task)

- [ ] T1: pin the toolchain exactly (also `protoc`), add `mise.local.toml.example` and the `.gitignore` entry. VAL-5 activates in T7.
- [ ] T2: workspace, lints, `proto/agent/v1/agent.proto`. Remove `#[ignore]` from VAL-2; show red, then green.
- [ ] T3: `control-plane`, `agent`, `check/test-db` and the AGE Pod manifest. Remove `#[ignore]` from VAL-3; red, then green in `test-db`.
- [ ] T4: `api/openapi.yaml`, `gen/api` with its Okteto manifest, `check/api`. Remove `.skip` from VAL-7; red, then green.
- [ ] T5: web app. Remove `.skip` from VAL-4; red, then green.
- [ ] T6: chart and `helm lint`.
- [ ] T7: `check/_default`, `check/fast`, the other steps and `check/pins`. Remove `.skip` from VAL-5; red, then green. Run the VAL-6 demonstration.
- [ ] T8: Dockerfiles (VAL-8 is for the reviewer).
- [ ] T9: `okteto.yaml`, `dev`, `e2e`, `ci/e2e`, `ci/preview-destroy`, `playwright.config.ts`. Remove `.skip` from VAL-10; save the negative run.
- [ ] T10: `ci/_default`, `ci/fast`, `ci/cluster`, `ci/build`, `ci/publish` and the workflows. Remove `.skip` from VAL-16; red, then green.
- [ ] T11: `AGENTS.md`, `README.md`.
- [ ] T12: context and namespace guards. Remove `.skip` from VAL-15; red, then green.
- [ ] T13: commit the OSI `LICENSE` first (Assumption), then `check/codeql` and its configuration.
- [ ] T14: `renovate` task, `renovate.json`, `renovate.yml`.

After approval, the only allowed edit to a locked scaffold is removing its skip marker.

## Running the tests

```sh
node --test 'mise-tasks/**/*.test.mjs'               # all task tests; the gate splits fast and cluster
cargo nextest run -p agent-proto                     # VAL-2
mise run check                                       # VAL-3 (test-db), VAL-7 (test-tasks-cluster)
npm --prefix web run test -- --run src/routes/val-4.test.ts  # VAL-4
mise run e2e                                         # VAL-10 against mise run dev
```

## Status and next step

The contract stays **draft**. No approval change was made, and no test is locked.

1. Daniel gives explicit product approval. The Test Architect review passes (two independent reviews; every blocker fixed and proven by mutation runs).
2. The separate JJ APPROVAL change records the digest and the `### Locked Tests` table (eight files).
3. Approved-phase validation passes. Then resume `bmad-build` with the spec path.
