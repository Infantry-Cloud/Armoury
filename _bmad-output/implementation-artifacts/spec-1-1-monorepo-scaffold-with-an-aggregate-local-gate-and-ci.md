---
title: 'Story 1.1: Monorepo scaffold with an aggregate local gate and CI'
type: 'chore'
created: '2026-11-06'
status: 'draft'
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

The repository has planning artifacts but no code. Every later story and Agent Readiness (INF-12) need a real codebase, a pinned toolchain and one feedback loop. Scaffold the agreed monorepo with one aggregate local gate (`mise run check`, plus `mise run check:fast`), the same gate in tiered CI, OpenAPI code generation with a drift check, digest-pinned images, and a dev-cluster loop (`mise run dev`: Skaffold on the in-cluster BuildKit) with a Playwright smoke test.

### Scope

- In scope: the layout from architecture.md (Cargo workspace `control-plane`/`agent`/`agent-proto`, `proto/agent/v1/agent.proto`, `api/openapi.yaml`, `web/`, `charts/armoury` with `control-plane` and `agent` subcharts); `mise.toml`, `mise.local.toml.example` and `mise-tasks/` (`check`, `check:fast` and their steps, `gen:api`, `dev`, `e2e`, `ci:deploy`, `ci:teardown`, `image:build`); the test-database Pod manifest; two multi-stage Dockerfiles; `skaffold.yaml` with `dev` and `ci` profiles; `.github/workflows/ci.yml` and `build.yml`; `AGENTS.md`; `README.md`; workspace lints for R2/R3 (deny `unwrap`/`expect` outside tests, forbid `unsafe`); one real test or lint target per unit.
- Out of scope: product behaviour of any kind; Postgres/SeaweedFS in the chart, migrations, riverqueue and the install test (Story 1.2); auth/RBAC and the `x-armoury-role` spec test (1.3/1.4); themes, shell, palette (1.5+); agent gRPC listener (Epic 3); `release.yml`, signing, `bundles.yml`, `action/` (Epics 10/11). Agent Readiness phase 3 items: gate steps `lob`, `workflows`, `secrets`, `contracts`; `cargo deny`; `npm audit signatures`; the JUnit adapter and contract step; `codeql.yml`; gitleaks; Renovate; `SECURITY.md`; `CODEOWNERS`; readiness rules. The dev cluster, BuildKit, dev registry, ARC scale set and their RBAC (Daniel).

### Boundaries & Constraints

**Always:** pin every tool, crate, npm package, container image (by digest) and GitHub Action (by commit SHA); commit `Cargo.lock`, `web/package-lock.json` and `mise.lock`. Follow ARCH25 Locality of Behaviour (no `utils/`/`helpers/`/`common/`, no `unwrap`/`expect` outside tests and startup, no `unsafe`, `main.rs` wiring only). Generated code is never hand-edited. Local and CI run the same mise tasks. Every command that touches the cluster names its kube context from `ARMOURY_KUBE_CONTEXT` (D3). Kube credentials, BuildKit client certificates and registry credentials stay outside the repository.

**Never:** a `CLAUDE.md` file; floating `latest` tags or `-F latest` crate features (pin a concrete `k8s-openapi` `v1_xx` feature no newer than the dev cluster's Kubernetes version); a local Java install; a local container runtime, local cluster or local database (D6, D8); scanner tools in either image; git commands; image pushes to GHCR from any branch except `main`; `pull_request_target`; fork pull-request code on ARC runners.

**Decisions (agent-owned, recorded):** web uses npm (architecture init commands); web lint is ESLint + Prettier through the official `sv add eslint prettier` add-ons; the control plane listens on 8080 and serves the UI and API from one origin; images are `ghcr.io/<repository owner>/armoury-control-plane` and `ghcr.io/<repository owner>/armoury-agent`; Rust and Node are pinned in `mise.toml`. Gate step names and tiers follow `docs/agent-readiness.md` "Aggregate gate"; this story adds the fast-tier step `test-tasks` (node:test over `mise-tasks/`). Skaffold builds through a custom builder that calls `mise run image:build` (`buildx` with the builder named by `ARMOURY_BUILDX_BUILDER`). The workstation and ARC runners use the in-cluster builder; the hosted `fast` job uses a local `docker-container` buildx builder for `gen:api` only. The AGE test Pod manifest is in the repository and the `test-db` step applies it to `ARMOURY_NAMESPACE`. `ci.yml` jobs follow the AR CI design (`fast`, `cluster`, `e2e`, `ci-gate`); AR phase 3 adds its steps later. `build.yml` keeps the packaged chart as a workflow artifact; chart publication is Epic 10.

**Decisions (user, 2026-11-06):**

- OQ-1 (superseded by Correct Course 2026-11-06, D3-D8) → Development and CI use Daniel's dev cluster: rootless mTLS `buildkitd` in the cluster through a pinned `buildx`, a dev registry set through `SKAFFOLD_DEFAULT_REPO`, the AGE test database as a digest-pinned Pod, ARC runners for the cluster tier, Helm 4. Site values live in the untracked `mise.local.toml`.
- OQ-2 → The user creates the GitHub repository and pushes the story before Code Review, so VAL-11 and VAL-12 use real workflow runs.
- OQ-3 → Only `AGENTS.md` is written. The project does not use Claude Code, so there is no `CLAUDE.md`.
- OQ-4 → "No floating version" (AC-2) also applies to manifests: `Cargo.toml` requirements use `=x.y.z`, `web/package.json` uses exact versions (no `^`, `~`, `*`, ranges or `latest`), and mise tools use exact versions. Committed lockfiles are still required.

**Decisions (user, 2026-11-10):**

- OQ-5 → Each `ci` profile run gets a fresh namespace named `armoury-ci-<unique suffix>`. The ARC ServiceAccount may create and delete only namespaces with the `armoury-ci-` prefix, limited by an admission policy. Vera updates the threat model in `docs/agent-readiness.md`; Daniel sets the RBAC.

### Sources

- [Source: _bmad-output/planning-artifacts/epics.md#Story 1.1: Monorepo scaffold with an aggregate local gate and CI]
- [Source: _bmad-output/planning-artifacts/epics.md#ARCH1, ARCH12, ARCH23, ARCH25, ARCH27, ARCH34, PROC1, PROC3]
- [Source: _bmad-output/planning-artifacts/epics.md#Story 1.2 (uses the Skaffold `ci` profile)]
- [Source: _bmad-output/planning-artifacts/architecture.md#Complete Project Directory Structure]
- [Source: _bmad-output/planning-artifacts/sprint-change-proposal-2026-11-06.md]
- [Source: _bmad-output/planning-artifacts/sprint-change-proposal-2026-11-07-aliases.md#5 step 7]
- [Source: docs/agent-readiness.md#Decisions, #Aggregate gate, #CI design]

### Assumptions and Dependencies

- mise is installed on the workstation; `mise install` provides every other tool.
- crates.io, npmjs, Docker Hub, GHCR and the dev registry are reachable during development and CI.
- Before T3, T4 and T9 (OI-2, OI-3), Daniel provides: a kube context and namespace in the dev cluster, the BuildKit endpoint with client certificate files outside the repository, and the dev registry with its credentials in the host configuration.
- Before VAL-11 and VAL-12 (AR phase 3), Daniel provides the GitHub repository, an ARC scale set limited to this repository with its runner label, its Kubernetes permissions (including create and delete of `armoury-ci-*` namespaces, OQ-5), and GHCR package permissions.
- The user pushes; the agent never pushes.

### Acceptance Criteria

- AC-1 [P0]: Given a fresh clone with mise installed and `mise.local.toml` filled from `mise.local.toml.example`, when the developer runs `mise install` and then `mise run check`, then a Cargo workspace (resolver 3, edition 2024) builds `control-plane` (binary `armoury`), `agent` (binary `armoury-agent`) and `agent-proto` (tonic/prost codegen from `proto/agent/v1/agent.proto`), and `web/` builds as a SvelteKit app with Tailwind v4, shadcn-svelte initialised, `@xyflow/svelte` installed, `adapter-static` and SSR disabled in the root layout.
- AC-2 [P0]: Given the repository, when its manifests are inspected, then every tool in `mise.toml`, every crate and npm dependency, every container image reference in Dockerfiles, Kubernetes manifests and workflows (by `@sha256` digest) and every GitHub Action (by 40-character commit SHA) is pinned exactly; `Cargo.lock`, `web/package-lock.json` and `mise.lock` are committed; no `latest` tag or floating version exists; `mise.local.toml` is ignored and `mise.local.toml.example` is committed.
- AC-3 [P0]: Given a clean scaffold and a reachable dev cluster, when `mise run check` runs, then it runs the named steps `pins`, `rust` (rustfmt check, `clippy -D warnings`), `test-rust` (nextest without database tests), `web` (ESLint, Prettier, `svelte-check`, Vitest), `chart` (Helm 4 `helm lint`), `api` (drift check), `test-tasks` (node:test over `mise-tasks/`) and `test-db` (nextest `#[sqlx::test]` tests against `apache/age:release_PG18_1.8.0`, pinned by digest, as a Pod in the dev cluster), and exits 0; `mise run check:fast` runs every step except `test-db` and needs no kube context.
- AC-4 [P0]: Given exactly one injected defect (unformatted Rust, a clippy warning, a failing Rust test, a failing `#[sqlx::test]`, a web lint error, a `svelte-check` type error, a failing Vitest test, an invalid chart template, or edited generated code), when `mise run check` runs, then it exits non-zero and its output names the failing step.
- AC-5 [P1]: Given the scaffold, when the gate runs, then each Rust crate, the web app and the chart has at least one real passing test or lint target.
- AC-6 [P0]: Given `api/openapi.yaml`, when `mise run gen:api` runs, then it generates the Rust server types with `openapi-generator` (rust-axum) as a digest-pinned BuildKit stage (`--output type=local`; no local Java, no local container) and the TS types with `openapi-typescript` for `openapi-fetch`, and a second run produces identical output; the `api` step generates into a temporary directory and compares it with the committed output without any VCS command, and fails naming the file when generated code was edited.
- AC-7 [P0]: Given the repository, when the images are built, then multi-stage Dockerfiles produce a control-plane image with the `armoury` binary and the SPA build, and an agent image with only `armoury-agent` and no scanner tools; all base images are pinned by digest; the dev build uses a debug profile and a cached dependency layer (`cargo-chef`), with a `ponytail:` comment naming slow Rust rebuilds as the ceiling and a remote build cache as the upgrade path.
- AC-8 [P0]: Given mise and a `mise.local.toml` with `ARMOURY_KUBE_CONTEXT`, `ARMOURY_NAMESPACE`, `SKAFFOLD_DEFAULT_REPO` and `ARMOURY_BUILDX_BUILDER`, when `mise run dev` runs, then Skaffold builds both images on the in-cluster BuildKit, pushes them to the dev registry, deploys the chart to `ARMOURY_NAMESPACE` with images as `repo:tag@digest`, port-forwards the UI and API to `localhost:8080`, and redeploys after a code change without rebuilding the dependency layer; no image build, database or cluster runs on the workstation.
- AC-9 [P1]: Given a deployment from `mise run dev` or `mise run ci:deploy`, when `mise run e2e` runs against its URL (default `http://localhost:8080`, overridden by `ARMOURY_E2E_BASE_URL`), then a Playwright smoke test loads the web app and passes; when no deployment is reachable, the task fails.
- AC-10 [P0]: Given a push or pull request, when `.github/workflows/ci.yml` runs, then it installs mise with `jdx/mise-action` pinned by commit; job `fast` runs `mise run check:fast` on GitHub-hosted runners for every event; jobs `cluster` (`mise run check`) and `e2e` (`ci:deploy`, `e2e`, then `ci:teardown` even on failure) run on ARC runners only for pushes and same-repository pull requests; job `ci-gate` fails unless `fast`, `cluster` and `e2e` all succeeded (skipped counts as failure); an injected defect fails at the same step as locally; the workflow declares top-level `permissions: contents: read` and has no `pull_request_target`.
- AC-11 [P1]: Given a push, when `.github/workflows/build.yml` runs, then on an ARC runner it builds both images on the in-cluster BuildKit and packages the chart with Helm 4; only on `main` does it push the images to GHCR by digest; only that push job has `packages: write`, and the workflow declares top-level `permissions: contents: read`.
- AC-12 [P1]: Given the repository root, when an agent or developer opens it, then `AGENTS.md` (no `CLAUDE.md`) states the ARCH25 Locality of Behaviour rules, the layout, PROC3 (keep `mise run dev` running during every development step) and the explicit-context rule, and `README.md` documents the init, check, check:fast, e2e, dev and ci:deploy commands and the dev-cluster prerequisites.
- AC-13 [P1]: Given `ARMOURY_KUBE_CONTEXT`, when `mise run ci:deploy` runs, then the Skaffold `ci` profile builds both images and deploys the chart into a fresh, uniquely named `armoury-ci-*` namespace of the dev cluster and prints the namespace and the in-cluster base URL; `mise run ci:teardown` deletes that namespace; two runs never share a namespace.
- AC-14 [P0]: Given a task that touches the cluster (the `test-db` step, `dev`, `ci:deploy`, `ci:teardown`), when `ARMOURY_KUBE_CONTEXT` is unset, then it exits non-zero with a message naming the variable before any `kubectl`, `helm` or `skaffold` call; when it is set, every such call passes it explicitly (`--context` or `--kube-context`), and no task relies on the kubeconfig current context.

### Validation Design

| VAL ID | Covers | Method | Level | Planned check or procedure | Expected evidence | Owner | Manual reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| VAL-1 | AC-1, AC-3, AC-5 | manual | demonstration | Copy the tracked files (`jj file list`) to a temporary directory outside the repository, add the local `mise.local.toml`, run `mise install && mise run check`; then remove the `ARMOURY_KUBE_CONTEXT` line from the copy's `mise.local.toml` and run `KUBECONFIG=/nonexistent mise run check:fast`; read `cargo metadata --no-deps --format-version 1`, `web/package.json` and `web/components.json` | `check` exits 0 and names every AC-3 step; `check:fast` exits 0 without `test-db`; the workspace uses resolver 3 and edition 2024 with binaries `armoury` and `armoury-agent`; `web/package.json` has Tailwind 4.x, `@xyflow/svelte` and `@sveltejs/adapter-static`; `web/components.json` exists; log saved under `_bmad-output/implementation-artifacts/evidence/1-1/` | Dev | A fresh-copy run of the whole gate is an environment demonstration (SD-3); the CI `cluster` job repeats the gate on every push (VAL-11) |
| VAL-2 | AC-1, AC-5 | mechanical | unit | `agent-proto/tests/val_2_roundtrip.rs::val_2_generated_message_roundtrip` | A prost type generated from `agent.proto` (`armoury.agent.v1.Heartbeat`, exposed as `agent_proto::v1`) encodes and decodes to an equal value | Dev | - |
| VAL-3 | AC-3, AC-5 | mechanical | integration | `control-plane/tests/val_3_age.rs::val_3_age_extension_is_available` | `#[sqlx::test]` passes in the `test-db` step against the digest-pinned AGE Pod and reads `age` extension version `1.8.0` | Dev | - |
| VAL-4 | AC-1, AC-5 | mechanical | unit | `web/src/routes/val-4.test.ts::VAL-4 root layout disables SSR and uses the static adapter` | Vitest passes: root layout exports `ssr = false` and the static adapter is configured | Dev | - |
| VAL-5 | AC-2 | mechanical | analysis | `mise-tasks/check/pins.test.mjs::VAL-5 pins check rejects floating references` | The `mise-tasks/check/pins` checker exits 0 on this repository and on a clean fixture, and exits 1 naming the offending file for each fixture defect: a `latest` tool, a non-exact mise tool version, a `FROM` without `@sha256:`, a Kubernetes manifest `image:` without `@sha256:`, a workflow `container:` or `services:` image without `@sha256:`, an action ref that is not a 40-hex SHA, a Cargo requirement without `=`, a `latest` crate feature, a `^` or `~` npm range, a missing `Cargo.lock`, `web/package-lock.json`, `mise.lock` or `mise.local.toml.example`, and a `mise.local.toml` that is not ignored | Dev | - |
| VAL-6 | AC-4 | manual | demonstration | In a temporary copy of the tracked files outside the repository, inject each of the nine AC-4 defects in turn, run `mise run check`, record the exit code and failing step, then restore the file before the next defect | Nine non-zero runs, each naming the right step, in a saved observation record | Dev | One-off mutation of source per category; a permanent mutation harness is disproportionate for a scaffold |
| VAL-7 | AC-6 | mechanical | integration | `mise-tasks/gen/api.test.mjs::VAL-7 gen:api is repeatable and the api step names an edited generated file` | Two `gen:api` runs into temporary copies give identical trees; the `api` step exits 0 on this repository and exits 1 naming the file when one generated file is edited; a `java` shim placed first on `PATH` is never called; no VCS command runs | Dev | - |
| VAL-8 | AC-7 | manual | inspection | Read both Dockerfiles; build each image with `buildx build --output type=tar` and list its filesystem with `tar -t` | Agent image holds only `armoury-agent` and base files, no syft/grype/grant/cosign; control-plane image holds `armoury` and the SPA; every `FROM` has `@sha256:`; the dev build target uses the debug profile; `cargo-chef` stage and `ponytail:` comment present | Test Architect | Image content is a one-time structural fact; release SBOMs (Epic 10) give the lasting check |
| VAL-9 | AC-8 | manual | demonstration | Run `mise run dev`; run `kubectl --context "$ARMOURY_KUBE_CONTEXT" -n "$ARMOURY_NAMESPACE" get pods -o jsonpath='{..image}'`; open `localhost:8080` and `localhost:8080/api/v1/healthz`; edit one source string; observe the redeploy; run `pgrep -fl 'docker\|podman\|containerd\|colima\|kind\|postgres'` before and after | Image refs start with `SKAFFOLD_DEFAULT_REPO` and contain `@sha256:`; `pgrep` finds no such process; page and API respond from one origin; redeploy log shows a cached `cargo-chef` layer on the in-cluster builder; observation record saved | Test Architect | A watch loop against a shared cluster is not credibly automated |
| VAL-10 | AC-9 | mechanical | e2e | `web/e2e/smoke.spec.ts::loads the web app @VAL-10` | Passes against the `mise run dev` deployment and in the CI `e2e` job; with `ARMOURY_E2E_BASE_URL=http://127.0.0.1:9`, `mise run e2e` exits non-zero (output saved) | Dev | - |
| VAL-11 | AC-10 | manual | demonstration | Push the story; record one green `ci.yml` run with all four jobs; push one injected defect and record the red run; open a fork pull request (or, without a fork account, record a run where the ARC jobs are skipped) and record `ci-gate`; read the workflow | Run URLs with commit IDs in a saved record; red run fails at the same step as locally; `ci-gate` fails when an ARC job is skipped; top-level `permissions: contents: read`; ARC jobs gated to pushes and same-repository pull requests; no `pull_request_target` | Test Architect | The workflow runs only on GitHub and ARC infrastructure |
| VAL-12 | AC-11 | manual | demonstration | Record a `build.yml` run on a non-`main` push (builds, packages, no push) and on `main` (pushes images by digest to GHCR); read the workflow | Run URLs and the pushed `@sha256` digests in a saved record; builds ran on an ARC runner through the in-cluster builder; only the `main` push job has `packages: write` | Test Architect | Registry push needs the real repository and token |
| VAL-13 | AC-12 | manual | inspection | Read `AGENTS.md` and `README.md`; check that no `CLAUDE.md` exists; follow the README commands on a fresh checkout | All ARCH25 rules, the layout, PROC3 and the explicit-context rule are stated; every README command works as written | Test Architect | Documentation quality needs human judgement |
| VAL-14 | AC-13 | manual | demonstration | Run `mise run ci:deploy` twice and record both namespaces; port-forward one and run `ARMOURY_E2E_BASE_URL=<forwarded URL> mise run e2e`; run `mise run ci:teardown` for each; list namespaces with `kubectl --context "$ARMOURY_KUBE_CONTEXT" get ns` | Two different namespace names; each `ci:deploy` output shows its namespace and in-cluster base URL; e2e passes; both namespaces are gone; observation record saved | Dev | Needs the real dev cluster; the CI `e2e` job repeats it on every run (VAL-11) |
| VAL-15 | AC-14 | mechanical | integration | `mise-tasks/cluster-context.test.mjs::VAL-15 cluster tasks require and pass an explicit kube context` | With `PATH` shims for `kubectl`, `helm` and `skaffold` that record their arguments: with `ARMOURY_KUBE_CONTEXT` unset each cluster task exits non-zero, names the variable and records no call; with it set to a probe value, every recorded call carries that context | Dev | - |

### Open Questions

- OQ-6 (blocks approval; route to Correct Course): ARC runners are dropped (Daniel, 2026-11-11). CI becomes one mise task, `mise run ci`, that runs the whole pipeline on the workstation and on a self-hosted GitHub Actions runner that is not ARC. Correct Course must update `epics.md` Story 1.1, architecture D8, the `docs/agent-readiness.md` CI design and threat model, Boundaries, Assumptions, OQ-5, AC-10, AC-11, VAL-11, VAL-12 and the AC-14/VAL-15 cluster task list.

### Change Control

After approval, any change to intent, scope, sources, assumptions, acceptance criteria, validation oracles, risk, or required evidence creates a new revision and requires product and validation reapproval. A validation-mechanism-only refinement with an unchanged oracle requires Test Architect approval and rerunning affected checks. Never weaken the contract to match an implementation.

</frozen-after-approval>

## Code Map

Nothing exists yet except the files marked EXISTING.

- `mise.toml`, `mise.lock` -- EXISTING. Change `lnktusrn` (2026-11-12) pinned codeql, jj, okteto, crane, gitleaks, helm, kubectl, actionlint, node and `npm:renovate` (SD-5) and removed skaffold. T1 adds exact pins for rust and cargo-nextest. No local cluster or container runtime tools.
- `mise.local.toml.example` -- NEW: the kube and Okteto context and the developer namespace. Okteto itself is installed and configured outside this repository. mise loads `mise.local.toml` itself.
- `.gitignore` -- EXISTING. Add `mise.local.toml`, `target/`, `web/node_modules/`, `web/.svelte-kit/`, `web/build/`, Playwright output.
- `_bmad-output/planning-artifacts/architecture.md` -- `:113` dev loop and Skaffold, `:117` versions to pin (shadcn-svelte: pin a version, never `@latest`), `:121-155` init commands, `:163` AGE Pod and e2e, `:201` CI tiers, `:297` and `:342-390` LoB rules for `AGENTS.md`, `:394-475` target tree (include `web/src/lib/{api,components/ui,command,design,theme}`).
- `_bmad-output/planning-artifacts/epics.md:337-386` -- the story source. `:404` -- Story 1.2 uses the `ci` profile.
- `docs/agent-readiness.md` -- `:121-145` gate steps and tiers, `:247-260` CI design, `:80-95` decisions D3-D9. Gate steps that phase 3 adds later must slot in without restructuring `check`.
- `Cargo.toml` (workspace, `[workspace.lints]`: `unwrap_used`/`expect_used` deny, `unsafe_code` forbid; `clippy.toml` allows them in tests), `proto/agent/v1/agent.proto`, `agent-proto/` (`build.rs` with `tonic-build`), `control-plane/` (axum, tokio, sqlx 0.9 with postgres, runtime-tokio, tls-rustls, uuid, migrate), `agent/` (kube with runtime and rustls, k8s-openapi, tokio). No riverqueue.
- `control-plane/src/httpapi/` -- generated rust-axum output plus the router mount; serve the SPA and `/api/v1/*` on 8080. `api/openapi.yaml` holds one trivial operation (`GET /api/v1/healthz`).
- `web/` -- SvelteKit + Tailwind v4 + shadcn-svelte + `@xyflow/svelte` 1.6.x; `src/routes/+layout.ts` sets `ssr = false`; `src/lib/api/` generated types; `playwright.config.ts` reads `ARMOURY_E2E_BASE_URL`, no `webServer`.
- `charts/armoury/` -- umbrella chart with `charts/control-plane` and `charts/agent` (from `helm create`, stripped); images rendered as `repo:tag@digest`.
- `mise-tasks/` -- file tasks: `check/_default` (aggregate: runs steps in order, fails fast, prints the failing step name), `check/fast`, one file per step (`pins`, `rust`, `test-rust`, `web`, `chart`, `test-tasks`; cluster tier `api`, `test-db`, `codeql`), `gen/api`, `dev` (`okteto up`), `e2e`, `ci` (all tiers in CI order), `ci/fast`, `ci/cluster`, `ci/e2e` (Okteto preview in CI, `okteto deploy` locally, then `okteto test`), `ci/build` (`okteto build`, chart package), `ci/publish` (`crane` copy to GHCR, `main` only), `renovate` (dry run unless `RENOVATE_DRY_RUN=false`). The AGE Pod + Service manifest sits next to `check/test-db`. `test-db` reaches it by port-forward locally and by Service DNS on ARC (D6). Each cluster task starts with a one-line guard for `ARMOURY_KUBE_CONTEXT`; no shared helper directory.
- `control-plane/Dockerfile`, `agent/Dockerfile` -- multi-stage, `cargo-chef`, distroless non-root runtime for the agent; a `dev` stage or pinned image for the Okteto dev container; the openapi-generator runs through `okteto test` with `artifacts` (D7).
- `okteto.yaml` -- `build` (control-plane, agent; images by digest through `OKTETO_BUILD_<NAME>_IMAGE`), `deploy` (Helm), `dev` (control-plane dev container: sync, `cargo watch`, persistent cargo cache, forward 8080), `test` (e2e and the generator). Replaces `skaffold.yaml`.
- `.github/workflows/ci.yml`, `build.yml`, `renovate.yml` -- each job installs mise and runs one `mise run ci:<tier>` task (D14); ARC jobs `if:` push or same-repository pull request; no check, scan or build logic in YAML.
- Existing ATDD scaffolds (not yet locked): `agent-proto/tests/val_2_roundtrip.rs`, `control-plane/tests/val_3_age.rs`, `web/src/routes/val-4.test.ts`, `mise-tasks/check/pins.test.mjs`, `web/e2e/smoke.spec.ts`. TEA ATDD Edit must add `mise-tasks/gen/api.test.mjs` (VAL-7), `mise-tasks/cluster-context.test.mjs` (VAL-15), the new VAL-5 fixtures, and refresh the checklist (R1/R3 are obsolete; R4/R5 still apply).

## Tasks & Acceptance

**Execution:**
- [ ] T1 `mise.toml`, `mise.local.toml.example`, `.gitignore` -- pin the toolchain, document site values, ignore build output -- AC-2 via VAL-5
- [ ] T2 `Cargo.toml`, `proto/agent/v1/agent.proto`, `agent-proto/` -- workspace, lints and proto codegen -- AC-1, AC-5 via VAL-1, VAL-2
- [ ] T3 `control-plane/`, `agent/`, `mise-tasks/check/test-db` and the AGE Pod manifest -- minimal binaries, one-origin server on 8080, database step -- AC-1, AC-3 via VAL-1, VAL-3
- [ ] T4 `api/openapi.yaml`, `mise-tasks/gen/api`, `mise-tasks/check/api`, generated output -- generation and drift check -- AC-6 via VAL-7
- [ ] T5 `web/` -- SvelteKit app, lint, `svelte-check`, Vitest -- AC-1, AC-5 via VAL-4
- [ ] T6 `charts/armoury/` -- umbrella chart and subcharts -- AC-3, AC-5 via VAL-1
- [ ] T7 `mise-tasks/check/` -- aggregate gate, `check:fast`, remaining steps and the pins checker; then the defect demonstration -- AC-2, AC-3, AC-4 via VAL-1, VAL-5, VAL-6
- [ ] T8 `control-plane/Dockerfile`, `agent/Dockerfile` -- digest-pinned multi-stage images -- AC-7 via VAL-8
- [ ] T9 `skaffold.yaml`, `mise-tasks/{image/build,dev,e2e,ci/deploy,ci/teardown}`, `web/playwright.config.ts` -- dev and ci profiles, smoke test -- AC-8, AC-9, AC-13 via VAL-9, VAL-10, VAL-14
- [ ] T10 `.github/workflows/ci.yml`, `.github/workflows/build.yml` -- tiered CI and image build -- AC-10, AC-11 via VAL-11, VAL-12
- [ ] T11 `AGENTS.md`, `README.md` -- rules, layout, PROC3, commands, prerequisites -- AC-12 via VAL-13
- [ ] T12 every cluster task -- explicit-context guard, activated by its test -- AC-14 via VAL-15

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

## Review Triage Log

## Verification

**Commands:**
- `mise install && mise run check` -- expected: exit 0 with every step named
- `mise run check:fast` -- expected: exit 0 without `test-db`
- `mise run gen:api` twice, then `mise run check` step `api` -- expected: no drift
- `mise run dev`, then `mise run e2e` -- expected: smoke test passes
- `uv run _bmad/custom/scripts/validate_story_contract.py validate --phase draft <this spec>` -- expected: valid
- the same stale-term search as the 2026-11-06 proposal (kind cluster, `-p kind`, Podman, Helm 3) over the `## Acceptance Contract` and `## Code Map` sections -- expected: no match
