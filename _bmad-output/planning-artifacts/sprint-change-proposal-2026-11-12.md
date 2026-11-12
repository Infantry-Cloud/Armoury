---
status: approved
approved: 2026-11-12 — Daniel approved the whole proposal ("Yes, apply it")
applied: 2026-11-12 — sections 4.1-4.5 written into epics.md, architecture.md, docs/agent-readiness.md, epic-1-context.md and the STORY-1.1 spec (outside the frozen block; status draft)
date: 2026-11-12
scope: moderate — the dev loop, CI and three architecture decisions change their tooling; no product behaviour changes; the STORY-1.1 contract was never approved, so it stays at Revision 1 and Build re-plans it
workflow: bmad-correct-course (incremental; every proposal approved one at a time by Daniel)
trigger: Daniel, 2026-11-12 — Okteto replaces Skaffold; every CI step becomes a mise task; `act` leaves the project; Renovate becomes a mise task
---

# Sprint Change Proposal — Okteto dev loop and mise-only CI

## 1. Issue summary

**Problem.** The plan uses Skaffold on our own in-cluster BuildKit and dev registry for the dev
loop, and GitHub workflow steps for parts of CI. Daniel wants the shortest developer feedback
cycle and a CI pipeline that runs the same way on the workstation and on GitHub.

**Type.** Deliberate tooling decision, made before any code exists.

**Decisions (Daniel, 2026-11-12):**

- The Okteto Platform replaces Skaffold. Okteto builds the images (Okteto BuildKit, Okteto
  Registry), deploys the chart and runs the dev container (`okteto up`).
- Okteto is installed and operated outside this repository. The repository assumes a working
  Okteto context with every right it needs. It records no Okteto setup decision.
- Every check, scan, build and dependency update is a mise task. GitHub Actions only installs mise
  and calls `mise run ci:<tier>`. `mise run ci` runs the same pipeline locally.
- ARC runners stay, in a separate runner cluster, with an identity for the dev cluster (external).
- `act` leaves the project. Renovate becomes `mise run renovate` (dry run by default).
- PR integration tests run in Okteto preview environments.
- The `api` drift step and CodeQL run in `ci:cluster` on ARC.
- DevSpace is reconsidered after Epic 1 (tooling log in `docs/agent-readiness.md`).

**Evidence.** Okteto 3.25.0 source: `up`, `deploy`, `build`, `test`, `destroy` and `preview` take
`--context`; `okteto build` exports `OKTETO_BUILD_<NAME>_IMAGE` with a digest; `okteto build`
cannot write local output, `okteto test` can (`artifacts`); previews deploy from a pushed branch.
The dev-loop speed comparison with DevSpace was not measured.

## 2. Impact analysis

- **Epics:** Epic 1 (Stories 1.1, 1.2) changes. Stories 2.12, 3.2 and 10.1 change environment text
  only. No epic is added, removed or reordered.
- **PRD:** no conflict. CodeQL appears in the PRD only as a product non-goal.
- **Architecture:** decision "Images, chart build and the dev loop", init commands, build tooling,
  testing, CI/CD and the directory tree.
- **UX:** not affected.
- **Agent Readiness:** D4–D9, the gate tiers, the CI design, the threat model, L14, R28, M5,
  OI-2, OI-3 and the tooling log.
- **STORY-1.1:** contract never approved; status back to `draft`; Build re-plans the frozen block;
  TEA ATDD Edit then updates VAL-7 and VAL-15 (not locked).
- **Already done:** `mise.toml` and `mise.lock` (change `lnktusrn`, deviation recorded below);
  Steward Decision SD-5 (Renovate trust exclusion).

## 3. Recommended approach

**Direct adjustment.** Edit the text below. Every product AC keeps its oracle. Rollback does not
apply (no code). MVP review is not needed.

- Effort: low to medium (text, a Build re-plan, an ATDD Edit).
- Risk: medium. The dev loop now depends on an external Okteto installation.
- Timeline: no change to the epic order.

## 4. Detailed change proposals

### 4.1 epics.md — requirements inventory (Proposal 1, approved)

- **ARCH1:** "`skaffold.yaml` (ARCH34)" → "`okteto.yaml` (ARCH34)".
- **ARCH23 (NEW):** "CI/CD on GitHub Actions. Every check, scan and build is a mise task, so
  `mise run ci` runs the whole pipeline on the workstation and in CI. Workflows only install mise
  (`jdx/mise-action`, pinned by commit) and call `mise run ci:<tier>`; no analysis, scan or build
  logic lives in workflow YAML. Fork pull requests run only `ci:fast` on GitHub-hosted runners. The
  full gate, end-to-end tests and image builds run on ARC self-hosted runners in a separate runner
  cluster, which reach the dev cluster through Okteto — `ci.yml` (`ci:fast`, `ci:cluster`,
  `ci:e2e`), `build.yml` (`ci:build` on each push; `ci:publish` copies both images by digest to
  GHCR on `main` only), a scheduled Renovate workflow (`mise run renovate`) and `release.yml`
  (…unchanged…)."
- **ARCH27:** the AGE Pod runs in the developer's Okteto namespace and `mise run check` reaches it
  by port-forward from the workstation and from ARC; the agent integration test runs in a temporary
  Okteto namespace in CI; `mise run e2e` runs against the Okteto deployment.
- **ARCH34:** the Skaffold block is replaced by: `okteto.yaml` on the Okteto Platform is the
  development loop (PROC3) — `build` (both images, Okteto BuildKit and Registry, deploys reference
  them by digest through `OKTETO_BUILD_<NAME>_IMAGE`), `deploy` (Helm), `dev` (control-plane dev
  container). `mise run dev` runs `okteto up` with an explicit Okteto context: file sync,
  `cargo watch` on a persistent cargo cache, UI and API on `localhost:8080`. `mise run ci:e2e`
  deploys a preview (PR) or a fresh namespace (local). `ci:build` and `ci:publish` (`main` only,
  pinned `crane`, digest preserved) produce the GHCR images. No local container runtime or cluster.
  `ponytail:` slow Rust rebuilds — debug profile, `cargo-chef` layer, persistent cargo cache;
  upgrade path a remote build cache.
- **PROC3:** "**Skaffold runs during every development step**" → "**The Okteto dev loop runs
  during every development step** (amended 2026-11-12)"; "(Skaffold `dev` on the dev cluster)" →
  "(`okteto up` on the dev cluster)".

### 4.2 epics.md — story text (Proposal 2, approved)

- **Story 1.1:** `gen:api` runs its pinned generator image in the dev cluster (no local Java, no
  local container runtime); images use `cargo-chef`, the dev container builds with the debug profile
  on a persistent cargo cache; the dev-loop block uses `okteto up` (build, deploy by digest, dev
  container, `localhost:8080`); the e2e block names "an Okteto deployment from `mise run dev` or
  `mise run ci:e2e`"; the `ci.yml` block says each job only installs mise and runs one
  `mise run ci:<tier>` task, and `mise run ci` runs the same tiers locally; the `build.yml` block
  uses `ci:build` and `ci:publish` with `crane`; AGENTS.md documents the Okteto prerequisites.
- **Story 1.2:** "the Skaffold `ci` profile" → "`mise run ci:e2e` from Story 1.1", deploying with
  Okteto into a preview (CI) or a fresh namespace (workstation).
- **Story 2.12:** "a fresh … namespace in the dev cluster" → "a fresh … Okteto namespace";
  "with Skaffold" → "with `okteto deploy`".
- **Story 3.2:** "a temporary namespace of the dev cluster on an ARC runner" → "a temporary Okteto
  namespace of the dev cluster, run from an ARC runner".
- **Story 10.1:** "reuses the `build.yml` pipeline" → "reuses the `ci:build` and `ci:publish`
  tasks"; the release check runs "in a temporary Okteto namespace, run from an ARC runner".
- Note for Epic 10 planning: images built by `okteto build` may not carry SLSA provenance; Story
  10.1 must confirm how provenance is produced.

### 4.3 architecture.md (Proposal 3, approved)

- Decision "Images, chart build and the dev loop" (line 113): Okteto replaces Skaffold as above;
  `ci:build`/`ci:publish` replace the `build.yml` description; DevSpace revisit noted.
- Init commands (lines 149–154): `mise.toml` pins rust, node, helm, kubectl, okteto, crane, codeql,
  gitleaks, renovate; `okteto.yaml` replaces `skaffold.yaml`; workflows call `mise run ci:<tier>`;
  the generator runs in the dev cluster.
- Build tooling (line 161), Testing/Dev (line 163) and CI/CD (line 201) follow 4.1.
- Directory tree (lines 399–406): `okteto.yaml` replaces `skaffold.yaml`; `mise-tasks/` lists
  `check, ci, dev, e2e, gen/api, renovate`; workflows call mise tasks; `renovate.yml` added.

### 4.4 docs/agent-readiness.md (Proposal 4, approved)

- D4 and D5 superseded: Okteto builds and stores the images (external). D6: the AGE Pod runs in the
  Okteto namespace. D7: the generator runs as an `okteto test` container with `artifacts`. D8:
  hosted runners run `ci:fast`; ARC runners in a separate cluster run `ci:cluster`, `ci:e2e`,
  `ci:build`. D9: Dagger and `act` are not used. New D14: every CI step is a mise task.
- Gate: `api` and `codeql` move to the cluster tier; `renovate` is a task, not a gate step.
- CI design: `fast`, `cluster` (`check` + `codeql`), `e2e`, `ci-gate`, `build`, `renovate`;
  `codeql.yml` removed.
- PR integration tests: in CI a PR runs `okteto preview deploy pr-<n>` then `okteto test`; PR close
  destroys the preview. Locally `ci:e2e` runs `okteto deploy` from the working tree into a fresh
  namespace, then the same `okteto test`. This replaces `ci:deploy`, `ci:teardown` and OQ-5.
- Threat model: one row "Okteto token or context — stored outside the repository, never committed"
  replaces the BuildKit certificate and registry credential rows.
- L14, R28, M5: `mise run dev` (`okteto up`). OI-2, OI-3 closed (external). Tooling log: BuildKit
  and `act` rows removed; DevSpace row (added in change `lyzzrtpp`) and SD-5 kept.

### 4.5 STORY-1.1 spec and epic-1-context.md (Proposal 5, approved)

- Spec (outside the frozen block): status `ready-for-dev` → `draft`; Spec Change Log entry; Code
  Map uses `okteto.yaml` and the tasks `ci`, `ci/fast`, `ci/cluster`, `ci/e2e`, `ci/build`,
  `ci/publish`, `renovate`; `mise.toml` marked done in `lnktusrn`.
- Build re-plan proposes these frozen-block edits for Daniel's approval at CHECKPOINT 1: one
  assumption line ("A working Okteto context, provided outside this repository, can build images,
  deploy the full chart, run previews and tests"); remove OQ-5; close OQ-6; AC-6/VAL-7 (`okteto
  test` generator, `api` in the cluster tier); AC-8/VAL-9 (`okteto up`); AC-9/VAL-10 (Okteto
  deployment or preview); AC-10/AC-11/VAL-11/VAL-12 (workflows call `mise run ci:<tier>`,
  `ci:build`, `ci:publish`, CodeQL in `ci:cluster`, Renovate dry run); AC-13/VAL-14 (preview in CI,
  `okteto deploy` locally, same `okteto test`); AC-14/VAL-15 (explicit `okteto --context` and
  `kubectl --context`); a new AC that `mise run ci` runs every tier locally in CI order.
- TEA ATDD Edit: update `mise-tasks/gen/api.test.mjs` (VAL-7) and
  `mise-tasks/cluster-context.test.mjs` (VAL-15); the other five scaffolds do not change.
- epic-1-context.md: dev workflow, gate and CI, images and dev loop, and the Story 1.2 dependency
  follow 4.1.

### 4.6 Recorded deviation

`mise.toml` and `mise.lock` were changed before STORY-1.1 approval (change `lnktusrn`, Daniel's
request): okteto, crane, gitleaks, helm, kubectl, actionlint, node and renovate added; skaffold
removed. Story 1.1 T1 still owns the Rust, nextest and web pins.

## 5. Implementation handoff

**Scope: moderate.**

| Who | Does | Done when |
| --- | --- | --- |
| Correct Course (this run) | Apply 4.1–4.5 after approval; run Linear Reconcile | Text applied; reconcile `plan --check` reported |
| `bmad-build` (re-plan) | Re-plan STORY-1.1; frozen edits only with Daniel's approval | CHECKPOINT 1 passes; draft validation VALID |
| Murat (`bmad-testarch-atdd`, Edit) | Update VAL-7 and VAL-15; CI naming check; approval | Approved-phase validation passes |
| Daniel | Provide a working Okteto context for the workstation and ARC (outside this repository) | `okteto` commands work with the named context |

**Success criteria.**

- `rg -n -i "skaffold|buildkit|buildx|\bact\b"` finds no current-plan text in `epics.md`,
  `architecture.md` or `epic-1-context.md` (history and change logs excepted).
- Every product AC keeps its oracle; only environment and CI text change.
- The STORY-1.1 spec is `draft` and passes draft validation.
