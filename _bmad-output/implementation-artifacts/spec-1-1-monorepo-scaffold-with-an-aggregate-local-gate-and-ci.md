---
title: 'Story 1.1: Monorepo scaffold with an aggregate local gate and CI'
type: 'chore'
created: '2026-11-06'
status: 'ready-for-dev'
route: 'dispatch'
review_loop_iteration: 0
story_key: '1-1-monorepo-scaffold-with-an-aggregate-local-gate-and-ci'
context:
  - '{project-root}/_bmad/custom/instructions/implementation.md'
  - '{project-root}/project-context.md'
  - '{project-root}/_bmad-output/implementation-artifacts/epic-1-context.md'
  - '{project-root}/docs/agent-readiness.md'
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Acceptance Contract

- Contract ID: STORY-1.1
- Revision: 1
- Risk: medium

### Intent

The repository has planning artifacts but no code. Every later story and Agent Readiness (INF-12) need a real codebase, a pinned toolchain and one feedback loop. Scaffold the agreed monorepo with one aggregate local gate (`mise run check`, plus `mise run check:fast`), OpenAPI code generation with a drift check, digest-pinned images, an Okteto dev loop (`mise run dev`) with a Playwright smoke test, CodeQL in the gate, Renovate as a task, and CI in which every step is a mise task, so `mise run ci` runs on the workstation the same tiers that GitHub Actions runs.

### Scope

- In scope: the layout from architecture.md (Cargo workspace `control-plane`/`agent`/`agent-proto`, `proto/agent/v1/agent.proto`, `api/openapi.yaml`, `web/`, `charts/armoury` with `control-plane` and `agent` subcharts); `mise.toml`, `mise.local.toml.example` and `mise-tasks/` (`check`, `check:fast` and their steps including `codeql`, `gen:api`, `dev`, `e2e`, `ci`, `ci:fast`, `ci:cluster`, `ci:e2e`, `ci:build`, `ci:publish`, `ci:preview-destroy`, `renovate`); the CodeQL configuration; the Renovate configuration; the AGE test-database Pod manifest; two multi-stage Dockerfiles; `okteto.yaml`; `.github/workflows/ci.yml`, `build.yml`, `preview-cleanup.yml` and `renovate.yml`; `AGENTS.md`; `README.md`; workspace lints for R2/R3 (deny `unwrap`/`expect` outside tests, forbid `unsafe`); one real test or lint target per unit.
- Out of scope: product behaviour of any kind; Postgres/SeaweedFS in the chart, migrations, riverqueue and the install test (Story 1.2); auth/RBAC and the `x-armoury-role` spec test (1.3/1.4); themes, shell, palette (1.5+); agent gRPC listener (Epic 3); `release.yml`, signing, provenance, chart publication, `bundles.yml`, `action/` (Epics 10/11). Agent Readiness phase 3 items: gate steps `lob`, `workflows`, `secrets` and `contracts`; `cargo deny`; `npm audit signatures`; the JUnit adapter and contract step; gitleaks; `SECURITY.md`; `CODEOWNERS`; readiness rules. The Okteto installation, its contexts, identities and repository access, the dev cluster, the ARC scale set and their RBAC (Daniel, outside this repository).

### Boundaries & Constraints

**Always:** pin every tool, crate, npm package, container image (by digest) and GitHub Action (by commit SHA); commit `Cargo.lock`, `web/package-lock.json` and `mise.lock`. Follow ARCH25 Locality of Behaviour (no `utils/`/`helpers/`/`common/`, no `unwrap`/`expect` outside tests and startup, no `unsafe`, `main.rs` wiring only). Generated code is never hand-edited. The workstation and CI run the same mise tasks; each workflow job only installs mise and runs one `mise run ci:<tier>` task (D14). Every `okteto` call names its Okteto context and every `kubectl` call names its kube context (D3). Okteto tokens, kube credentials and registry credentials stay outside the repository.

**Never:** a `CLAUDE.md` file; floating `latest` tags or `-F latest` crate features (pin a concrete `k8s-openapi` `v1_xx` feature no newer than the dev cluster's Kubernetes version); a local Java install; a local container runtime, local cluster or local database (D6, D8); check, scan or build logic in workflow YAML; scanner tools in either image; git commands; image pushes to GHCR from any branch except `main`; `pull_request_target`; fork pull-request code on ARC runners.

**Decisions (agent-owned, recorded):**

- Web uses npm (architecture init commands); web lint is ESLint + Prettier through the official `sv add eslint prettier` add-ons; the control plane listens on 8080 and serves the UI and API from one origin; images are `ghcr.io/<repository owner>/armoury-control-plane` and `ghcr.io/<repository owner>/armoury-agent`; Rust and Node are pinned in `mise.toml`.
- Site values live in the untracked `mise.local.toml`: `ARMOURY_OKTETO_CONTEXT` (passed to every `okteto --context`), `ARMOURY_KUBE_CONTEXT` (the kube context that `okteto kubeconfig` writes for the Okteto namespace, passed to every `kubectl --context`) and `ARMOURY_NAMESPACE` (the developer's Okteto namespace). There are two context variables because Okteto and kubectl name the same cluster differently. On ARC runners the runner environment provides the same three variables.
- Gate steps and tiers follow `docs/agent-readiness.md` "Aggregate gate", plus two task-test steps. Fast tier: `pins`, `rust`, `test-rust`, `web`, `chart`, `test-tasks` (node:test over `mise-tasks/**/*.test.mjs` except `*.cluster.test.mjs`). Cluster tier: `api`, `test-db`, `test-tasks-cluster` (node:test over `mise-tasks/**/*.cluster.test.mjs`, the task tests that need Okteto) and `codeql`.
- The `codeql` step is in the cluster tier because it is slow; it needs no cluster and no context variable. Query packs are pinned by exact version, databases and results are written outside the workspace, and nothing is uploaded to GitHub. A dismissal is a `query-filters` entry in `.github/codeql/codeql-config.yml` with a reason comment.
- `renovate.json` at the repository root configures Renovate to keep every update exactly pinned (exact versions, `=` Cargo requirements, image digests, action SHAs). `mise run renovate` is a dry run unless `RENOVATE_DRY_RUN=false`; only `renovate.yml` sets that, with the token from a repository secret.
- `gen:api` runs the generator as an `okteto test` container from a manifest with no `deploy` section, so it never deploys the app; the container's `artifacts` return the generated files (D7).
- `test-db` starts a run-unique AGE Pod in `ARMOURY_NAMESPACE`, reaches it through `kubectl port-forward` and deletes it on exit, so parallel runs never share a database (D6).
- `ci:fast` runs `check:fast`; `ci:cluster` runs `check`; `ci:e2e` deploys and runs the smoke test (AC-13); `mise run ci` runs `ci:fast`, `ci:cluster` and `ci:e2e`. `ci:build` and `ci:publish` belong to `build.yml`, not to `mise run ci`.
- Inside `ci:e2e`, `okteto test` runs the same Playwright spec and configuration as `mise run e2e`, in a digest-pinned Playwright image, against the in-cluster service URL.
- The only YAML logic is `ci-gate`'s `if:` on the results of the jobs it needs; it is job-status logic, not a check.
- `build.yml` has two jobs: `build` (every push, `ci:build`) and `publish` (`main` only, needs `build`, `packages: write`, `ci:publish`); `build` passes the image digests to `publish` as job outputs. The packaged chart is not uploaded; chart publication is Epic 10.
- Pull-request previews are named `pr-<n>` (`docs/agent-readiness.md`); other fresh namespaces are `armoury-ci-<unique suffix>`.

**Decisions (user, 2026-11-06):**

- OQ-1 (superseded by Correct Course 2026-11-06 and 2026-11-12) → Development and CI use Daniel's dev cluster through the Okteto Platform (Okteto BuildKit and Registry, preview environments), the AGE test database as a digest-pinned Pod in an Okteto namespace, ARC runners in a separate runner cluster for the cluster tiers and image builds, and Helm 4. Site values live in the untracked `mise.local.toml`.
- OQ-2 → The user creates the GitHub repository and pushes the story before Code Review, so VAL-11 and VAL-12 use real workflow runs.
- OQ-3 → Only `AGENTS.md` is written. The project does not use Claude Code, so there is no `CLAUDE.md`.
- OQ-4 → "No floating version" (AC-2) also applies to manifests: `Cargo.toml` requirements use `=x.y.z`, `web/package.json` uses exact versions (no `^`, `~`, `*`, ranges or `latest`), and mise tools use exact versions. Committed lockfiles are still required.

**Decisions (user, 2026-11-12):**

- OQ-6 → Closed by Correct Course 2026-11-12: ARC runners stay, in a separate runner cluster that reaches the dev cluster through an Okteto identity provided outside this repository. Every CI step is a mise task, and `mise run ci` runs the CI tiers on the workstation. OQ-5 (repository RBAC for `armoury-ci-*` namespaces) is withdrawn: Okteto creates and deletes namespaces under its own identity.
- OQ-7 → The CodeQL gate step and the Renovate task, its configuration and `renovate.yml` belong to Story 1.1, not to AR phase 3.

### Sources

- [Source: _bmad-output/planning-artifacts/epics.md#Story 1.1: Monorepo scaffold with an aggregate local gate and CI]
- [Source: _bmad-output/planning-artifacts/epics.md#ARCH1, ARCH12, ARCH23, ARCH25, ARCH27, ARCH34, PROC1, PROC3]
- [Source: _bmad-output/planning-artifacts/epics.md#Story 1.2 (uses `mise run ci:e2e`)]
- [Source: _bmad-output/planning-artifacts/architecture.md#Images, chart build and the dev loop; #CI/CD; #Complete Project Directory Structure]
- [Source: _bmad-output/planning-artifacts/sprint-change-proposal-2026-11-06.md]
- [Source: _bmad-output/planning-artifacts/sprint-change-proposal-2026-11-07-aliases.md#5 step 7]
- [Source: _bmad-output/planning-artifacts/sprint-change-proposal-2026-11-12.md]
- [Source: docs/agent-readiness.md#Decisions (D3-D14), #Aggregate gate, #CI design]

### Assumptions and Dependencies

- mise is installed on the workstation; `mise install` provides every other tool.
- crates.io, npmjs, Docker Hub, GHCR and the Okteto Registry are reachable during development and CI.
- Before T3, T4 and T9: a working Okteto context, provided outside this repository, can build images, deploy the full chart, run previews and tests, and create and delete namespaces; `okteto kubeconfig` gives a kube context for the developer's Okteto namespace.
- Before VAL-11 and VAL-12 (AR phase 3), Daniel provides the GitHub repository, an ARC scale set limited to this repository with its runner label and the three site variables plus an Okteto identity in its environment, Okteto access to the repository for previews, GHCR package permissions, and a Renovate token (GitHub App or fine-grained token) as a repository secret, because pull requests opened with `GITHUB_TOKEN` do not start CI.
- The repository `Infantry-Cloud/Armoury` is public (Daniel, 2026-11-12; `gh repo view` reports `PUBLIC`), so the CodeQL CLI open-source terms apply and fork pull requests can occur (AC-10 already keeps them off ARC runners).
- The user pushes; the agent never pushes.

### Acceptance Criteria

- AC-1 [P0]: Given a fresh clone with mise installed and `mise.local.toml` filled from `mise.local.toml.example`, when the developer runs `mise install` and then `mise run check`, then a Cargo workspace (resolver 3, edition 2024) builds `control-plane` (binary `armoury`), `agent` (binary `armoury-agent`) and `agent-proto` (tonic/prost codegen from `proto/agent/v1/agent.proto`), and `web/` builds as a SvelteKit app with Tailwind v4, shadcn-svelte initialised, `@xyflow/svelte` installed, `adapter-static` and SSR disabled in the root layout.
- AC-2 [P0]: Given the repository, when its manifests are inspected, then every tool in `mise.toml`, every crate and npm dependency, every container image reference in Dockerfiles, Kubernetes manifests, Okteto manifests and workflows (by `@sha256` digest, or an Okteto build output that carries its digest) and every GitHub Action (by 40-character commit SHA) is pinned exactly; `Cargo.lock`, `web/package-lock.json` and `mise.lock` are committed; no `latest` tag or floating version exists; `mise.local.toml` is ignored and `mise.local.toml.example` is committed.
- AC-3 [P0]: Given a clean scaffold and a working Okteto context, when `mise run check` runs, then it runs the fast-tier steps `pins`, `rust` (rustfmt check, `clippy -D warnings`), `test-rust` (nextest without database tests), `web` (ESLint, Prettier, `svelte-check`, Vitest), `chart` (Helm 4 `helm lint`) and `test-tasks` (node:test over `mise-tasks/`), then the cluster-tier steps `api` (drift check), `test-db` (nextest `#[sqlx::test]` tests against `apache/age:release_PG18_1.8.0`, pinned by digest, as a Pod in the Okteto namespace) `test-tasks-cluster` and `codeql`, and exits 0; `mise run check:fast` runs only the fast tier and needs no Okteto or kube context.
- AC-4 [P0]: Given exactly one injected defect (unformatted Rust, a clippy warning, a failing Rust test, a failing `#[sqlx::test]`, a web lint error, a `svelte-check` type error, a failing Vitest test, an invalid chart template, or edited generated code), when `mise run check` runs, then it exits non-zero and its output names the failing step.
- AC-5 [P1]: Given the scaffold, when the gate runs, then each Rust crate, the web app and the chart has at least one real passing test or lint target.
- AC-6 [P0]: Given `api/openapi.yaml`, when `mise run gen:api` runs, then it generates the Rust server types with `openapi-generator` (rust-axum) from its digest-pinned image as an `okteto test` container whose `artifacts` return the files (no local Java, no local container runtime) and the TS types with `openapi-typescript` for `openapi-fetch`, and a second run produces identical output; the cluster-tier `api` step generates into a temporary directory and compares it with the committed output without any VCS command, and fails naming the file when generated code was edited.
- AC-7 [P0]: Given the repository, when the images are built with `okteto build`, then multi-stage Dockerfiles produce a control-plane image with the `armoury` binary and the SPA build, and an agent image with only `armoury-agent` and no scanner tools; all base images are pinned by digest; the images use a cached dependency layer (`cargo-chef`); a dev stage provides the control-plane dev container (debug profile, `cargo watch`); a `ponytail:` comment names slow Rust rebuilds as the ceiling and a remote build cache as the upgrade path.
- AC-8 [P0]: Given mise and a `mise.local.toml` with `ARMOURY_OKTETO_CONTEXT`, `ARMOURY_KUBE_CONTEXT` and `ARMOURY_NAMESPACE`, when `mise run dev` runs, then it runs `okteto up` with that context and namespace: Okteto builds both images on its BuildKit into the Okteto Registry, deploys the chart into `ARMOURY_NAMESPACE` with the images referenced by digest, and replaces the control-plane Deployment with a dev container that syncs the source, rebuilds with `cargo watch` on a persistent cargo cache and forwards the UI and API to `localhost:8080`; a source change rebuilds without rebuilding the dependencies; no image build, database or cluster runs on the workstation.
- AC-9 [P1]: Given an Okteto deployment from `mise run dev` or `mise run ci:e2e`, when the Playwright smoke test runs against its URL (`mise run e2e` on the workstation: default `http://localhost:8080`, overridden by `ARMOURY_E2E_BASE_URL`; `okteto test` inside `ci:e2e`: the in-cluster service URL), then it loads the web app and passes; when no deployment is reachable, `mise run e2e` fails.
- AC-10 [P0]: Given a push or pull request, when `.github/workflows/ci.yml` runs, then each job only installs mise with `jdx/mise-action` pinned by commit and runs one `mise run ci:<tier>` task; job `fast` (`ci:fast`) runs on GitHub-hosted runners for every event; jobs `cluster` (`ci:cluster`) and `e2e` (`ci:e2e`) run on ARC runners only for pushes and same-repository pull requests; job `ci-gate` fails unless `fast`, `cluster` and `e2e` all succeeded (skipped counts as failure); an injected defect fails at the same step as in `mise run ci`; the workflow declares top-level `permissions: contents: read` and has no `pull_request_target`.
- AC-11 [P1]: Given a push, when `.github/workflows/build.yml` runs, then an ARC runner runs `mise run ci:build`, which builds both images with `okteto build` and packages the chart with Helm 4; only on `main`, a separate job runs `mise run ci:publish`, which copies both images by digest to GHCR with the pinned `crane`, so each GHCR digest equals the built digest; only that job has `packages: write`, and the workflow declares top-level `permissions: contents: read`.
- AC-12 [P1]: Given the repository root, when an agent or developer opens it, then `AGENTS.md` (no `CLAUDE.md`) states the ARCH25 Locality of Behaviour rules, the layout, PROC3 (keep `mise run dev` running during every development step) and the explicit-context rule, and `README.md` documents the init, check, check:fast, ci, ci:e2e, e2e and dev commands and the Okteto and dev-cluster prerequisites.
- AC-13 [P1]: Given a working Okteto context, when `mise run ci:e2e` runs on the workstation or for a CI push, then it deploys the working tree with `okteto deploy` into a fresh namespace named `armoury-ci-<unique suffix>`, prints the namespace and the base URL, runs the smoke test with `okteto test`, and deletes the namespace afterwards, also on failure or interrupt; two runs never share a namespace. For a same-repository pull request it deploys the preview `pr-<n>` from the pull-request branch with `okteto preview deploy` and runs the same `okteto test`; when the pull request closes, `.github/workflows/preview-cleanup.yml` runs `mise run ci:preview-destroy` on an ARC runner, which destroys that preview.
- AC-14 [P0]: Given a task that calls `okteto` or `kubectl` (`gen:api`, the `api` and `test-db` steps, `dev`, `ci:e2e`, `ci:build`, `ci:publish`, `ci:preview-destroy`), when a context variable it needs (`ARMOURY_OKTETO_CONTEXT` or `ARMOURY_KUBE_CONTEXT`) is unset, then it exits non-zero with a message naming the variable before any `okteto` or `kubectl` call; when it is set, every `okteto` call passes `--context "$ARMOURY_OKTETO_CONTEXT"` and every `kubectl` call passes `--context "$ARMOURY_KUBE_CONTEXT"`; no task calls `helm` against a cluster or relies on the current Okteto or kubeconfig context.
- AC-15 [P0]: Given a working Okteto context, when `mise run ci` runs, then it runs `ci:fast`, `ci:cluster` and `ci:e2e` in that order (the tasks the `ci.yml` jobs run), stops at the first failing tier, exits non-zero and names that tier.
- AC-16 [P1]: Given the working tree, when the cluster-tier `codeql` step runs, then the pinned CodeQL CLI creates databases for Rust, JavaScript/TypeScript and GitHub Actions locally and analyzes them with version-pinned query packs, uploading nothing; the step fails and names the file and rule of each result, and a result is dismissed only by a committed CodeQL configuration entry that states its reason.
- AC-17 [P1]: Given the committed Renovate configuration, when `mise run renovate` runs without `RENOVATE_DRY_RUN=false`, then Renovate runs as a dry run, creates no branch or pull request, and its log lists the dependencies it found for mise tools, Cargo requirements, npm packages, container image digests (Dockerfiles, Kubernetes and Okteto manifests, workflows) and GitHub Action SHAs; `.github/workflows/renovate.yml` runs `mise run renovate` with `RENOVATE_DRY_RUN=false` weekly and on manual dispatch on a GitHub-hosted runner, declares top-level `permissions: contents: read`, and its pull requests keep every update exactly pinned.

### Validation Design

| VAL ID | Covers | Method | Level | Planned check or procedure | Expected evidence | Owner | Manual reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| VAL-1 | AC-1, AC-3, AC-5 | manual | demonstration | Copy the tracked files (`jj file list`) to a temporary directory outside the repository, add the local `mise.local.toml`, run `mise install && mise run check`; then remove the `ARMOURY_OKTETO_CONTEXT` and `ARMOURY_KUBE_CONTEXT` lines from the copy's `mise.local.toml` and run `KUBECONFIG=/nonexistent mise run check:fast`; read `cargo metadata --no-deps --format-version 1`, `web/package.json` and `web/components.json` | `check` exits 0 and names every AC-3 step in tier order; `check:fast` exits 0 and runs no cluster-tier step; the workspace uses resolver 3 and edition 2024 with binaries `armoury` and `armoury-agent`; `web/package.json` has Tailwind 4.x, `@xyflow/svelte` and `@sveltejs/adapter-static`; `web/components.json` exists; log saved under `_bmad-output/implementation-artifacts/evidence/1-1/` | Dev | A fresh-copy run of the whole gate is an environment demonstration (SD-3); the CI `cluster` job repeats the gate on every push (VAL-11) |
| VAL-2 | AC-1, AC-5 | mechanical | unit | `agent-proto/tests/val_2_roundtrip.rs::val_2_generated_message_roundtrip` | A prost type generated from `agent.proto` (`armoury.agent.v1.Heartbeat`, exposed as `agent_proto::v1`) encodes and decodes to an equal value | Dev | - |
| VAL-3 | AC-3, AC-5 | mechanical | integration | `control-plane/tests/val_3_age.rs::val_3_age_extension_is_available` | `#[sqlx::test]` passes in the `test-db` step against the digest-pinned AGE Pod and reads `age` extension version `1.8.0` | Dev | - |
| VAL-4 | AC-1, AC-5 | mechanical | unit | `web/src/routes/val-4.test.ts::VAL-4 root layout disables SSR and uses the static adapter` | Vitest passes: root layout exports `ssr = false` and the static adapter is configured | Dev | - |
| VAL-5 | AC-2 | mechanical | analysis | `mise-tasks/check/pins.test.mjs::VAL-5 pins check rejects floating references` | The `mise-tasks/check/pins` checker exits 0 on this repository and on a clean fixture, and exits 1 naming the offending file for each fixture defect: a `latest` tool, a non-exact mise tool version, a `FROM` without `@sha256:`, a Kubernetes manifest `image:` without `@sha256:`, an Okteto manifest `image:` that is neither `@sha256:`-pinned nor an Okteto build output, a workflow `container:` or `services:` image without `@sha256:`, an action ref that is not a 40-hex SHA, a Cargo requirement without `=`, a `latest` crate feature, a `^` or `~` npm range, a missing `Cargo.lock`, `web/package-lock.json`, `mise.lock` or `mise.local.toml.example`, and a `mise.local.toml` that is not ignored | Dev | - |
| VAL-6 | AC-4 | manual | demonstration | In a temporary copy of the tracked files outside the repository, inject each of the nine AC-4 defects in turn, run `mise run check`, record the exit code and failing step, then restore the file before the next defect | Nine non-zero runs, each naming the right step, in a saved observation record | Dev | One-off mutation of source per category; a permanent mutation harness is disproportionate for a scaffold |
| VAL-7 | AC-6 | mechanical | integration | `mise-tasks/gen/api.cluster.test.mjs::VAL-7 gen:api is repeatable and the api step names an edited generated file` | Runs in the `test-tasks-cluster` step: two `gen:api` runs into temporary copies give identical trees with Rust and TS files; the `api` step exits 0 on this repository and exits 1 naming the file when one generated file is edited; `java`, `git` and `jj` shims placed first on `PATH` are never called | Dev | - |
| VAL-8 | AC-7 | manual | inspection | Read both Dockerfiles; build both images and the dev stage with `okteto build`; list each image's filesystem with `crane export <image@digest> - \| tar -t` | Agent image holds only `armoury-agent` and base files, no syft/grype/grant/cosign; control-plane image holds `armoury` and the SPA; every `FROM` has `@sha256:`; `cargo-chef` stage and `ponytail:` comment present; the dev stage uses the debug profile and has `cargo watch` | Test Architect | Image content is a one-time structural fact; release SBOMs (Epic 10) give the lasting check |
| VAL-9 | AC-8 | manual | demonstration | Run `mise run dev`; run `kubectl --context "$ARMOURY_KUBE_CONTEXT" -n "$ARMOURY_NAMESPACE" get pods -o jsonpath='{..image}'`; open `localhost:8080` and `localhost:8080/api/v1/healthz`; edit one source string and watch the `cargo watch` rebuild in the dev container; run `pgrep -fl 'docker\|podman\|containerd\|colima\|kind\|postgres\|buildkitd'` before and after | Image refs start with the Okteto Registry host and contain `@sha256:`; page and API respond from one origin; the rebuild compiles only workspace crates; `pgrep` finds no such process; observation record saved | Test Architect | A watch loop against a shared cluster is not credibly automated |
| VAL-10 | AC-9 | mechanical | e2e | `web/e2e/smoke.spec.ts::loads the web app @VAL-10` | Passes against the `mise run dev` deployment and in the `okteto test` run of `ci:e2e`; with `ARMOURY_E2E_BASE_URL=http://127.0.0.1:9`, `mise run e2e` exits non-zero (output saved) | Dev | - |
| VAL-11 | AC-10, AC-13 | manual | demonstration | Push the story; record one green `ci.yml` run with all four jobs; push one injected defect, record the red run and the failing step of the same defect in `mise run ci`; open a fork pull request (or, without a fork account, record a run where the ARC jobs are skipped) and record `ci-gate`; open and close a same-repository pull request and record its preview `pr-<n>` in `okteto preview list` before and after `preview-cleanup.yml` runs; read the workflows | Run URLs with commit IDs in a saved record; the red run fails at the same step as locally; `ci-gate` fails when an ARC job is skipped; each job only installs mise and runs one `mise run ci:<tier>` task; top-level `permissions: contents: read`; ARC jobs gated to pushes and same-repository pull requests; no `pull_request_target`; the preview exists while the pull request is open and is gone after it closes | Test Architect | The workflows run only on GitHub and ARC infrastructure |
| VAL-12 | AC-11 | manual | demonstration | Record a `build.yml` run on a non-`main` push (build only, no publish job) and on `main` (publish); compare `crane digest` of each GHCR image with the digest that `ci:build` printed; read the workflow | Run URLs and digests in a saved record; each GHCR digest equals its built digest; builds ran on an ARC runner through `okteto build`; only the `publish` job has `packages: write` | Test Architect | Registry push needs the real repository and token |
| VAL-13 | AC-12 | manual | inspection | Read `AGENTS.md` and `README.md`; check that no `CLAUDE.md` exists; follow the README commands on a fresh checkout | All ARCH25 rules, the layout, PROC3, the explicit-context rule and the Okteto prerequisites are stated; every README command works as written | Test Architect | Documentation quality needs human judgement |
| VAL-14 | AC-13 | manual | demonstration | Run `mise run ci:e2e` twice and record both outputs; run it a third time and interrupt it with Ctrl-C after the deploy; list the namespaces of the Okteto context with `okteto namespace list` | Two different `armoury-ci-` namespace names; each output shows its namespace and base URL and a passing smoke test; none of the three namespaces exists afterwards; observation record saved | Dev | Needs the real Okteto Platform; the CI `e2e` job repeats it on every run (VAL-11) |
| VAL-15 | AC-14 | mechanical | integration | `mise-tasks/cluster-context.test.mjs::VAL-15 cluster tasks require and pass an explicit Okteto and kube context` | With `PATH` shims for `okteto`, `kubectl` and `helm` that record their arguments: with a needed context variable unset, each AC-14 task exits non-zero, names the variable and records no call; with both set to probe values, every recorded `okteto` call carries `--context` with the Okteto probe, every `kubectl` call carries `--context` with the kube probe, and every recorded `helm` call is a local command (`package`, `lint` or `dependency`) | Dev | - |
| VAL-16 | AC-15 | mechanical | unit | `mise-tasks/ci/ci.test.mjs::VAL-16 mise run ci runs the CI tiers in order and stops at the first failure` | With a `mise` shim first on `PATH` that records each call and fails a chosen tier: when no tier fails, the calls are `run ci:fast`, `run ci:cluster`, `run ci:e2e` in that order and the task exits 0; when `ci:cluster` fails, `ci:e2e` is never called, the task exits non-zero and its output names `ci:cluster` | Dev | - |
| VAL-17 | AC-16 | manual | demonstration | Read `mise-tasks/check/codeql` and `.github/codeql/codeql-config.yml`; in a temporary copy of the tracked files, add one JavaScript finding (`eval` of `location.hash` in a web route) and run `mise run check`; then add a `query-filters` exclusion with a reason for that rule and run it again | The first run fails at `codeql` and names the file and rule; the second run passes; every exclusion has a reason; query packs are pinned by version; no upload command or GitHub API call is in the step; observation record saved | Dev | One-off injection of a finding; a permanent fixture would run CodeQL twice on every gate run |
| VAL-18 | AC-17 | manual | demonstration | Run `mise run renovate` and save the log; read `renovate.json` and `renovate.yml`; dispatch `renovate.yml` once and record the run and one pull request it opens (or its log when no update exists) | The dry-run log lists dependencies of each named kind and creates nothing; the configuration pins exact versions, digests and SHAs; the workflow has top-level `permissions: contents: read`, a hosted runner and the token from a secret; the pull request keeps exact pins and starts CI; record saved | Test Architect | Renovate needs the real repository, its token and live registries |

### Open Questions

- None.

### Change Control

After approval, any change to intent, scope, sources, assumptions, acceptance criteria, validation oracles, risk, or required evidence creates a new revision and requires product and validation reapproval. A validation-mechanism-only refinement with an unchanged oracle requires Test Architect approval and rerunning affected checks. Never weaken the contract to match an implementation.

</frozen-after-approval>

## Code Map

Nothing exists yet except the files marked EXISTING.

- `mise.toml`, `mise.lock` -- EXISTING. Change `lnktusrn` pinned okteto 3.25.0, crane, helm 4.3.1, kubectl, node, codeql, gitleaks, actionlint, jj and `npm:renovate` (SD-5). T1 adds exact pins for rust and cargo-nextest. No skaffold, buildx, docker, kind or local database.
- `mise.local.toml.example` -- NEW: `ARMOURY_OKTETO_CONTEXT`, `ARMOURY_KUBE_CONTEXT` (the name `okteto kubeconfig` prints, for example `okteto_example_com/<namespace>`), `ARMOURY_NAMESPACE`. mise loads `mise.local.toml` itself.
- `.gitignore` -- EXISTING. Add `mise.local.toml`, `target/`, `web/node_modules/`, `web/.svelte-kit/`, `web/build/`, Playwright output. `.stignore` -- NEW: keep `target/` and `node_modules/` out of the `okteto up` file sync.
- `_bmad-output/planning-artifacts/architecture.md` -- `:113` dev loop (Okteto) and images, `:121-154` init commands (`:128` shadcn-svelte: pin a version, never `@latest`), `:163` AGE Pod and e2e, `:201` CI/CD, `:342-390` LoB rules for `AGENTS.md`, `:394-475` target tree (include `web/src/lib/{api,components/ui,command,design,theme}`).
- `_bmad-output/planning-artifacts/epics.md:337-387` -- the story source. `:403` -- Story 1.2 uses `mise run ci:e2e`.
- `docs/agent-readiness.md` -- decisions D3-D14, "Aggregate gate", "CI design", "Contract CI Wiring". AR phase 3 adds `lob`, `workflows`, `secrets`, `contracts` without restructuring `check`; its JUnit adapter must also read the `test-tasks-cluster` report. Follow-up for Vera: the phase 3 build list (items 3 and 5) still names `check/codeql` and Renovate, which OQ-7 moved to this story.
- `Cargo.toml` (workspace, `[workspace.lints]`: `unwrap_used`/`expect_used` deny, `unsafe_code` forbid; `clippy.toml` allows them in tests), `proto/agent/v1/agent.proto`, `agent-proto/` (`build.rs` with `tonic-build`), `control-plane/` (axum, tokio, sqlx 0.9 with postgres, runtime-tokio, tls-rustls, uuid, migrate), `agent/` (kube with runtime and rustls, k8s-openapi, tokio). No riverqueue.
- `control-plane/src/httpapi/` -- generated rust-axum output plus the router mount; serve the SPA and `/api/v1/*` on 8080. `api/openapi.yaml` holds one trivial operation (`GET /api/v1/healthz`).
- `web/` -- SvelteKit + Tailwind v4 + shadcn-svelte + `@xyflow/svelte` 1.6.x; `src/routes/+layout.ts` sets `ssr = false`; `src/lib/api/` generated types; `playwright.config.ts` reads `ARMOURY_E2E_BASE_URL`, no `webServer`, JUnit reporter when `PLAYWRIGHT_JUNIT_OUTPUT_FILE` is set.
- `charts/armoury/` -- umbrella chart with `charts/control-plane` and `charts/agent` (from `helm create`, stripped); images rendered as `repo@digest` (or `repo:tag@digest`) from values.
- `mise-tasks/` -- file tasks: `check/_default` (runs steps in tier order, fails fast, prints the failing step name), `check/fast`, one file per step (`pins`, `rust`, `test-rust`, `web`, `chart`, `test-tasks`, `api`, `test-db`, `test-tasks-cluster`); the AGE Pod manifest next to `check/test-db`; `gen/api` plus its own Okteto manifest (generator test container, no `deploy`); `dev` (`okteto up`); `e2e`; `ci/_default`, `ci/fast`, `ci/cluster`, `ci/e2e`, `ci/build`, `ci/publish`, `ci/preview-destroy`; `check/codeql`; `renovate`. Each task that calls `okteto` or `kubectl` starts with a one-line guard per context variable; no shared helper directory. Test files are not executable, so mise does not list them as tasks.
- `control-plane/Dockerfile`, `agent/Dockerfile` -- multi-stage, `cargo-chef`, distroless non-root runtime for the agent; a `dev` target (Rust base by digest, pinned `cargo-watch`, debug profile) for the control-plane dev container.
- `okteto.yaml` -- `build` (control-plane, agent, control-plane dev target), `deploy` (`helm upgrade --install` with the built digests; check which `OKTETO_BUILD_<NAME>_*` variable carries the digest in Okteto 3.25.0), `dev` (control-plane: sync, `cargo watch`, persistent volume for the cargo registry and `target/`, forward 8080), `test` (`e2e`: pinned Playwright image, in-cluster base URL, `artifacts` return the JUnit report).
- `.github/codeql/codeql-config.yml` -- NEW: languages, pinned query packs, `query-filters` dismissals with reasons. The mise `codeql` asset is the CLI without queries, so the step downloads the pinned packs. `renovate.json` -- NEW: managers for mise, Cargo, npm, Dockerfile, Kubernetes and Okteto manifests (regex manager if needed), GitHub Actions; exact pins and digests.
- `.github/workflows/ci.yml`, `build.yml`, `preview-cleanup.yml`, `renovate.yml` -- each job installs mise and runs one `mise run ci:<tier>` task (D14); ARC jobs `if:` push or same-repository pull request; actions pinned by SHA.
- Existing ATDD scaffolds (not yet locked): `agent-proto/tests/val_2_roundtrip.rs`, `control-plane/tests/val_3_age.rs`, `web/src/routes/val-4.test.ts`, `mise-tasks/check/pins.test.mjs`, `mise-tasks/gen/api.test.mjs`, `mise-tasks/cluster-context.test.mjs`, `web/e2e/smoke.spec.ts`. TEA ATDD Edit must: move VAL-7 to `mise-tasks/gen/api.cluster.test.mjs` and replace its `buildx` assumptions with `okteto test`; rewrite VAL-15 for `okteto`/`kubectl` and the AC-14 task list; add VAL-16 `mise-tasks/ci/ci.test.mjs`; add the VAL-5 Okteto-manifest fixture; fix the `ci:deploy` comment in `smoke.spec.ts`; refresh the checklist and the Validation artifacts list.

## Tasks & Acceptance

**Execution:**
- [ ] T1 `mise.toml`, `mise.local.toml.example`, `.gitignore`, `.stignore` -- pin the toolchain, document site values, ignore build output -- AC-2 via VAL-5
- [ ] T2 `Cargo.toml`, `proto/agent/v1/agent.proto`, `agent-proto/` -- workspace, lints and proto codegen -- AC-1, AC-5 via VAL-1, VAL-2
- [ ] T3 `control-plane/`, `agent/`, `mise-tasks/check/test-db` and the AGE Pod manifest -- minimal binaries, one-origin server on 8080, database step -- AC-1, AC-3 via VAL-1, VAL-3
- [ ] T4 `api/openapi.yaml`, `mise-tasks/gen/api` and its Okteto manifest, `mise-tasks/check/api`, generated output -- generation and drift check -- AC-6 via VAL-7
- [ ] T5 `web/` -- SvelteKit app, lint, `svelte-check`, Vitest -- AC-1, AC-5 via VAL-4
- [ ] T6 `charts/armoury/` -- umbrella chart and subcharts -- AC-3, AC-5 via VAL-1
- [ ] T7 `mise-tasks/check/` -- aggregate gate in two tiers, `check:fast`, remaining steps and the pins checker; then the defect demonstration -- AC-2, AC-3, AC-4 via VAL-1, VAL-5, VAL-6
- [ ] T8 `control-plane/Dockerfile`, `agent/Dockerfile` -- digest-pinned multi-stage images and the dev target -- AC-7 via VAL-8
- [ ] T9 `okteto.yaml`, `mise-tasks/{dev,e2e,ci/e2e,ci/preview-destroy}`, `web/playwright.config.ts` -- Okteto dev loop, e2e deployments and smoke test -- AC-8, AC-9, AC-13 via VAL-9, VAL-10, VAL-14
- [ ] T10 `mise-tasks/ci/{_default,fast,cluster,build,publish}`, `.github/workflows/{ci,build,preview-cleanup}.yml` -- CI tiers, `mise run ci`, image build and publish -- AC-10, AC-11, AC-13, AC-15 via VAL-11, VAL-12, VAL-16
- [ ] T11 `AGENTS.md`, `README.md` -- rules, layout, PROC3, commands, Okteto prerequisites -- AC-12 via VAL-13
- [ ] T12 every task that calls `okteto` or `kubectl` -- explicit-context guard, activated by its test -- AC-14 via VAL-15
- [ ] T13 `mise-tasks/check/codeql`, `.github/codeql/codeql-config.yml` -- CodeQL cluster-tier step with reasoned dismissals -- AC-3, AC-16 via VAL-1, VAL-17
- [ ] T14 `mise-tasks/renovate`, `renovate.json`, `.github/workflows/renovate.yml` -- Renovate dry-run task and scheduled workflow -- AC-17 via VAL-18

## Contract Approval

- Status: draft
- Approved by: pending
- Validation approved by: pending
- Approved at: pending
- Contract digest: pending
- Validation artifacts: `_bmad-output/test-artifacts/atdd-checklist-1-1-monorepo-scaffold-with-an-aggregate-local-gate-and-ci.md`; `agent-proto/tests/val_2_roundtrip.rs`; `control-plane/tests/val_3_age.rs`; `web/src/routes/val-4.test.ts`; `mise-tasks/check/pins.test.mjs`; `mise-tasks/gen/api.test.mjs`; `web/e2e/smoke.spec.ts`; `mise-tasks/cluster-context.test.mjs`

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

## Implementation Notes

## Spec Change Log

- 2026-11-06 — Correct Course `_bmad-output/planning-artifacts/sprint-change-proposal-2026-11-06.md` (approved by Daniel): the dev loop and CI move from kind on local Podman to the dev cluster (in-cluster BuildKit, dev registry, AGE as a cluster Pod, ARC runners), Helm 4, and `mise run dev` replaces `skaffold dev -p kind`. The epics.md source for Story 1.1 changed (dev loop, ci.yml, build.yml, AGENTS.md ACs). Status set to `draft` so Build re-plans and repeats CHECKPOINT 1. Frozen-block edits still need Daniel's approval in that re-plan. Affected: OQ-1, Assumptions, AC-8, AC-10, AC-11, AC-12, VAL-9, VAL-11, Code Map. The contract was never approved, so it stays at Revision 1.
- 2026-11-10 — Build re-plan (planning change `znmusovo`), awaiting Daniel's CHECKPOINT 1 approval. Rewrote Intent, Scope, Boundaries, OQ-1, Sources, Assumptions, AC-2/3/6/8/9/10/11/12 and VAL-1/5/7/8/9/10/11/12 from `epics.md:337-386` and D3-D9. Added AC-13 (Skaffold `ci` profile, for Story 1.2) and AC-14 (explicit kube context) with VAL-14 and VAL-15. VAL-1 is a manual demonstration and VAL-7 a node:test (SD-3). Fast-tier steps follow `docs/agent-readiness.md`. Covers ACR step 7 in `sprint-change-proposal-2026-11-07-aliases.md`. AC and VAL IDs kept where the meaning holds; still Revision 1 (never approved). Daniel decided OQ-5 (option A) and kept the full spec (about 7,200 tokens).
- 2026-11-10 — CHECKPOINT 1: Daniel approved the plan (product review, "Approve and stop"). Build status `ready-for-dev`. Contract Approval stays `draft`; next step is TEA ATDD.
- 2026-11-11 — TEA ATDD (change `mmlpxlwq`), edits approved by Daniel in session: E5 VAL-5 adds a `latest` crate feature and a missing `mise.local.toml.example`; E6 VAL-1 runs `check:fast` without the context line and reads the AC-1 facts; E7 VAL-5 adds workflow `container:`/`services:` images; E8 VAL-8 checks the debug profile; E9 VAL-9 adds `pgrep` and the registry prefix; E10 VAL-10 names the unreachable URL; E12 VAL-14 checks the printed namespace and URL. Added OQ-6 (ARC dropped; `mise run ci`), which blocks approval until Correct Course. Still Revision 1 (never approved).
- 2026-11-12 — Correct Course `_bmad-output/planning-artifacts/sprint-change-proposal-2026-11-12.md` (approved by Daniel): Okteto replaces Skaffold, every CI step becomes a mise task (`mise run ci`, `ci:<tier>`), `act` leaves, Renovate becomes `mise run renovate`, PR integration tests run in Okteto previews, `api` and CodeQL move to the cluster tier. Okteto is external; the contract only assumes a working Okteto context. Status set to `draft` so Build re-plans and repeats CHECKPOINT 1. Build must propose these frozen-block edits for Daniel's approval: the Okteto assumption line; remove OQ-5; close OQ-6; AC-6/VAL-7; AC-8/VAL-9; AC-9/VAL-10; AC-10/AC-11/VAL-11/VAL-12; AC-13/VAL-14; AC-14/VAL-15; a new AC that `mise run ci` runs every tier locally in CI order. Then TEA ATDD Edit updates `mise-tasks/gen/api.test.mjs` (VAL-7) and `mise-tasks/cluster-context.test.mjs` (VAL-15). Still Revision 1 (never approved).
- 2026-11-12 — Build re-plan (planning change `knkuuyxl`) for Correct Course `sprint-change-proposal-2026-11-12.md`, awaiting Daniel's CHECKPOINT 1 approval. Proposed frozen-block edits: Intent, Scope, Boundaries (Okteto, D14, two context variables, two task-test steps, `test-db` Pod per run, `build.yml` jobs, preview names), OQ-1 text, OQ-5 withdrawn, OQ-6 closed, Sources, Assumptions (Okteto context line), AC-2/3/6/7/8/9/10/11/12/13/14 and VAL-1/5/7/8/9/10/11/12/13/14/15. Added AC-15 (`mise run ci`) with VAL-16. VAL-7 moves to `mise-tasks/gen/api.cluster.test.mjs` (needs Okteto). OQ-7 (CodeQL and Renovate scope) answered by Daniel: both move from AR phase 3 into this story, adding the `codeql` step to AC-3, AC-16/VAL-17 (CodeQL), AC-17/VAL-18 (Renovate), T13 and T14, and a Renovate-token assumption. Daniel kept the full spec (about 11,000 tokens). Tasks T9/T10 retitled. Still Revision 1 (never approved).
- 2026-11-12 — CHECKPOINT 1: Daniel approved the re-plan (product review, "Approve and continue"). Build status `ready-for-dev`. Contract Approval stays `draft`; the next step is TEA ATDD Edit and contract approval.
- 2026-11-12 — Daniel reported that the repository is public (`gh repo view` confirms `PUBLIC`). The Assumptions line about the CodeQL licence and OI-5 now records the public repository. Still Revision 1 (never approved). Follow-up for Vera: close OI-5 and update the private-repository notes in `docs/agent-readiness.md`.

## Review Triage Log

## Verification

**Commands:**
- `mise install && mise run check` -- expected: exit 0 with every step named, in tier order
- `mise run check:fast` -- expected: exit 0 without any cluster-tier step and without context variables
- `mise run gen:api` twice, then `mise run check` step `api` -- expected: no drift
- `mise run dev`, then `mise run e2e` -- expected: smoke test passes
- `mise run ci` -- expected: `ci:fast`, `ci:cluster` (including `codeql`), `ci:e2e` pass in that order
- `mise run renovate` -- expected: dry-run log lists dependencies of each kind and creates nothing
- `uv run _bmad/custom/scripts/validate_story_contract.py validate --phase draft <this spec>` -- expected: valid
- `rg -n -i "skaffold|buildx|buildkitd|ci:deploy|ci:teardown|ARMOURY_BUILDX|SKAFFOLD_|kind cluster|podman|helm 3"` over the `## Acceptance Contract` and `## Code Map` sections -- expected: only the VAL-9 `pgrep` pattern and Code Map lines that name removed tools or the TEA edits
