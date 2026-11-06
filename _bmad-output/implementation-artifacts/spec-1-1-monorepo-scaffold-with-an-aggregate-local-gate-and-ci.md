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
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Acceptance Contract

- Contract ID: STORY-1.1
- Revision: 1
- Risk: medium

### Intent

The repository has planning artifacts but no code. Every later story and Agent Readiness (INF-12) need a real codebase, pinned toolchain and one feedback loop. Scaffold the agreed monorepo with one aggregate local gate (`mise run check`), the same gate in CI, OpenAPI code generation with a drift check, digest-pinned images, and a Skaffold `kind` dev loop with a Playwright smoke test.

### Scope

- In scope: the layout from architecture.md (Cargo workspace `control-plane`/`agent`/`agent-proto`, `proto/agent/v1/agent.proto`, `api/openapi.yaml`, `web/`, `charts/armoury` with `control-plane` and `agent` subcharts), `mise.toml` + `mise-tasks/` (`check`, `gen:api`, `e2e`, image build), two multi-stage Dockerfiles, `skaffold.yaml` with a `kind` profile, `.github/workflows/ci.yml` and `build.yml`, `AGENTS.md`, `README.md`, one trivial test or lint target per unit.
- Out of scope: product behaviour of any kind; Postgres/SeaweedFS in the chart, migrations, riverqueue (Story 1.2); auth/RBAC and the `x-armoury-role` spec test (1.3/1.4); themes, shell, palette (1.5+); agent gRPC listener (Epic 3); `release.yml`, signing, `bundles.yml`, `action/` (Epics 10/11); JUnit contract wiring and `validate_story_contract.py ci` in CI, and `docs/agent-readiness.md` (Agent Readiness, INF-12).

### Boundaries & Constraints

**Always:** pin every tool, crate, npm package, container image (by digest) and GitHub Action (by commit SHA); commit `Cargo.lock`, `web/package-lock.json` and `mise.lock`. Follow ARCH25 Locality of Behaviour (no `utils/`/`helpers/`/`common/`, no `unwrap`/`expect` outside tests and startup, no `unsafe`, `main.rs` wiring only). Generated code is never hand-edited. Local and CI run the same mise tasks.

**Never:** a `CLAUDE.md` file (the project does not use Claude Code); floating `latest` tags or `-F latest` crate features (pin a concrete `k8s-openapi` `v1_xx` feature); a local Java install; scanner tools in either image; git commands; pushes from any branch except `main`.

**Decisions (agent-owned, recorded):** web uses npm (architecture init commands); web lint is ESLint + Prettier through the official `sv add eslint prettier` add-ons; the control plane listens on 8080 and Skaffold forwards it to `localhost:8080` (UI and API share one origin); images are `ghcr.io/<repository owner>/armoury-control-plane` and `ghcr.io/<repository owner>/armoury-agent`; Rust and Node are pinned in `mise.toml`.

**Decisions (user, 2026-11-06):**

- OQ-1 → The local container runtime is a local Podman machine. kind runs with `KIND_EXPERIMENTAL_PROVIDER=podman` (set in `mise.toml` `[env]`), and the mise tasks call the `docker`-compatible CLI so they also work with Docker on GitHub-hosted runners.
- OQ-2 → The user creates the GitHub repository and pushes the story before Code Review, so VAL-11 and VAL-12 use real workflow runs.
- OQ-3 → Only `AGENTS.md` is written. The project does not use Claude Code, so there is no `CLAUDE.md`.
- OQ-4 → "No floating version" (AC-2) also applies to manifests: `Cargo.toml` requirements use `=x.y.z`, `web/package.json` uses exact versions (no `^`, `~`, `*`, ranges or `latest`), and mise tools use exact versions. Committed lockfiles are still required.

### Sources

- [Source: _bmad-output/planning-artifacts/epics.md#Story 1.1: Monorepo scaffold with an aggregate local gate and CI]
- [Source: _bmad-output/planning-artifacts/epics.md#ARCH1, ARCH12, ARCH23, ARCH25, ARCH27, ARCH34, PROC1, PROC3]
- [Source: _bmad-output/planning-artifacts/architecture.md#Complete Project Directory Structure]
- [Source: _bmad-output/planning-artifacts/sprint-change-proposal-2026-11-05.md#Topic 1]

### Assumptions and Dependencies

- mise 2026.11.0 is installed on the workstation; `mise install` provides every other tool.
- Registries (crates.io, npmjs, Docker Hub, GHCR) are reachable during development and CI.
- The user runs `podman machine init` and `podman machine start` and makes the local machine the default Podman connection; `README.md` documents these steps. kind on Podman is experimental in kind.
- The user creates the GitHub repository and pushes before Code Review; the agent never pushes.

### Acceptance Criteria

- AC-1 [P0]: Given a fresh clone with mise installed, when the developer runs `mise install` and then `mise run check`, then a Cargo workspace (resolver 3, edition 2024) builds `control-plane` (binary `armoury`), `agent` (binary `armoury-agent`) and `agent-proto` (tonic/prost codegen from `proto/agent/v1/agent.proto`), and `web/` builds as a SvelteKit app with Tailwind v4, shadcn-svelte initialised, `@xyflow/svelte` installed, `adapter-static` and SSR disabled in the root layout.
- AC-2 [P0]: Given the repository, when its manifests are inspected, then every tool in `mise.toml`, every crate and npm dependency, every container image (by `@sha256` digest) and every GitHub Action (by 40-character commit SHA) is pinned, lockfiles are committed, and no `latest` tag or floating version exists.
- AC-3 [P0]: Given a clean scaffold, when `mise run check` runs, then it executes rustfmt check, `clippy -D warnings`, `cargo nextest` (including a `#[sqlx::test]` against `apache/age:release_PG18_1.8.0` pinned by digest), ESLint/Prettier, `svelte-check`, Vitest, `helm lint` of the chart and the generated-code drift check, and exits 0.
- AC-4 [P0]: Given exactly one injected defect (unformatted Rust, a clippy warning, a failing Rust test, a failing `#[sqlx::test]`, a web lint error, a `svelte-check` type error, a failing Vitest test, an invalid chart template, or edited generated code), when `mise run check` runs, then it exits non-zero and its output names the failing step.
- AC-5 [P1]: Given the scaffold, when the gate runs, then each Rust crate, the web app and the chart has at least one real passing test or lint target.
- AC-6 [P0]: Given `api/openapi.yaml`, when `mise run gen:api` runs, then it generates the Rust server types with `openapi-generator` (rust-axum, pinned container image, no local Java) and the TS client types with `openapi-typescript` for use with `openapi-fetch`, and a second run produces no diff.
- AC-7 [P0]: Given the repository, when the images are built, then multi-stage Dockerfiles produce a control-plane image with the `armoury` binary and the SPA build, and an agent image with only `armoury-agent` and no scanner tools; all base images are pinned by digest; the dev build uses a debug profile and a cached dependency layer (`cargo-chef`), with a `ponytail:` comment naming slow Rust rebuilds as the ceiling and a remote build cache as the upgrade path.
- AC-8 [P0]: Given a workstation with mise and a running local Podman machine, when `skaffold dev -p kind` runs, then it builds both images, deploys the chart to a local kind cluster with images as `repo:tag@digest`, serves the UI and API on `localhost:8080`, and redeploys after a code change without rebuilding the dependency layer.
- AC-9 [P1]: Given the Skaffold deployment, when `mise run e2e` runs, then a Playwright smoke test loads the web app from it and passes; when no deployment is reachable, the task fails.
- AC-10 [P0]: Given a push or pull request, when `.github/workflows/ci.yml` runs, then it installs mise with `jdx/mise-action` pinned by commit, runs `mise run check` and `mise run e2e` against a kind deployment, and fails on the same conditions as local.
- AC-11 [P1]: Given a push, when `.github/workflows/build.yml` runs, then it builds both images and packages the chart; only on `main` does it push them to GHCR, referenced by digest.
- AC-12 [P1]: Given the repository root, when an agent or developer opens it, then `AGENTS.md` states the ARCH25 Locality of Behaviour rules, the layout and PROC3 (keep `skaffold dev -p kind` running during every development step), and `README.md` documents the init, check, e2e and dev-loop commands.

### Validation Design

| VAL ID | Covers | Method | Level | Planned check or procedure | Expected evidence | Owner | Manual reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| VAL-1 | AC-1, AC-3, AC-5 | mechanical | integration | `mise install && mise run check` in a fresh temporary copy of the tracked files (`jj file list` copied outside the repository) | Exit 0; every step listed in the log; log saved under `_bmad-output/implementation-artifacts/evidence/1-1/` | Dev | - |
| VAL-2 | AC-1, AC-5 | mechanical | unit | `agent-proto/tests/val_2_roundtrip.rs::val_2_generated_message_roundtrip` | A prost type generated from `agent.proto` (`armoury.agent.v1.Heartbeat`, exposed as `agent_proto::v1`) encodes and decodes to an equal value | Dev | - |
| VAL-3 | AC-3, AC-5 | mechanical | integration | `control-plane/tests/val_3_age.rs::val_3_age_extension_is_available` | `#[sqlx::test]` passes against the digest-pinned AGE image and reads `age` extension version `1.8.0` | Dev | - |
| VAL-4 | AC-1, AC-5 | mechanical | unit | `web/src/routes/val-4.test.ts::VAL-4 root layout disables SSR and uses the static adapter` | Vitest passes: root layout exports `ssr = false` and the static adapter is configured | Dev | - |
| VAL-5 | AC-2 | mechanical | analysis | `mise-tasks/check/pins.test.mjs::VAL-5 pins check rejects floating references` | node:test, run as a step of `mise run check`: the `mise-tasks/check/pins` checker exits 0 on this repository and on a clean fixture, and exits 1 naming the offending file for each fixture defect: a `latest` tool, a non-exact mise tool version, a `FROM` without `@sha256:`, an action ref that is not a 40-hex SHA, a Cargo requirement without `=`, a `^` or `~` npm range, and a missing `Cargo.lock`, `web/package-lock.json` or `mise.lock` | Dev | - |
| VAL-6 | AC-4 | manual | demonstration | In a temporary copy of the tracked files outside the repository, inject each of the nine AC-4 defects in turn, run `mise run check`, record the exit code and failing step, then restore the file before the next defect | Nine non-zero runs, each naming the right step, in a saved observation record | Dev | One-off mutation of source per category; a permanent mutation harness is disproportionate for a scaffold |
| VAL-7 | AC-6 | mechanical | integration | `mise run gen:api` twice, then `jj diff --stat` | Generated files exist in `control-plane/src/httpapi/` and `web/src/lib/api/`; second run gives an empty diff; no `java` on `PATH` is needed | Dev | - |
| VAL-8 | AC-7 | manual | inspection | Build both images; read both Dockerfiles; list each image filesystem (`docker image inspect`, `docker create` + `docker export \| tar -t`) | Agent image holds only `armoury-agent` and base files, no syft/grype/grant/cosign; control-plane image holds `armoury` and the SPA; every `FROM` has `@sha256:`; `cargo-chef` stage and `ponytail:` comment present | Test Architect | Image content is a one-time structural fact; release SBOMs (Epic 10) give the lasting check |
| VAL-9 | AC-8 | manual | demonstration | Run `skaffold dev -p kind`; check pod image refs with `kubectl get pods -o jsonpath='{..image}'`; open `localhost:8080`; edit one source string; observe redeploy and a cached `cargo-chef` layer in the build log | Image refs contain `@sha256:`; page loads; redeploy log shows cached dependency layer; observation record saved | Test Architect | A watch loop on a workstation is not credibly automated |
| VAL-10 | AC-9 | mechanical | e2e | `web/e2e/smoke.spec.ts::loads the web app @VAL-10` | Passes against the Skaffold deployment; with the deployment stopped, `mise run e2e` exits non-zero (output saved) | Dev | - |
| VAL-11 | AC-10 | manual | demonstration | Push the story to the GitHub repository; record one green `ci.yml` run, then push one injected defect and record the red run | Two run URLs with commit IDs in a saved record; red run fails at the same step as local | Test Architect | The workflow runs only on GitHub-hosted infrastructure |
| VAL-12 | AC-11 | manual | demonstration | Record a `build.yml` run on a non-`main` push (builds, packages, no push) and on `main` (pushes images by digest to GHCR) | Run URLs and the pushed `@sha256` digests in a saved record; `ci.yml` and `build.yml` declare top-level `permissions: contents: read`, only the `main` push job gets `packages: write`, and neither uses `pull_request_target` | Test Architect | Registry push needs the real repository and token |
| VAL-13 | AC-12 | manual | inspection | Read `AGENTS.md` and `README.md`; check that no `CLAUDE.md` exists; follow the README commands on a fresh checkout | All ARCH25 rules, the layout and PROC3 are stated; every README command works as written | Test Architect | Documentation quality needs human judgement |

### Open Questions

- None.

### Change Control

After approval, any change to intent, scope, sources, assumptions, acceptance criteria, validation oracles, risk, or required evidence creates a new revision and requires product and validation reapproval. A validation-mechanism-only refinement with an unchanged oracle requires Test Architect approval and rerunning affected checks. Never weaken the contract to match an implementation.

</frozen-after-approval>

## Code Map

The repository has no code yet. Everything below is new, except where noted.

- `mise.toml`, `mise.lock` -- EXISTING (pins `jj`, `skaffold` 2.25.0). Add exact pins for rust, node, helm, kind (plus `KIND_EXPERIMENTAL_PROVIDER=podman` in `[env]`), kubectl, cargo-nextest, cargo-chef (if used outside Docker), actionlint. Keep existing pins.
- `.gitignore` -- EXISTING. Add `target/`, `web/node_modules/`, `web/.svelte-kit/`, `web/build/`, Playwright output.
- `_bmad-output/planning-artifacts/architecture.md:379-456` -- the target tree. `:117` versions ("pin at init" list), `:126-153` init commands (`npx sv create web --template minimal --types ts --add tailwindcss`, shadcn-svelte init — pin its version, do not use `@latest`), `:113`/`:151` Skaffold and Dockerfile rules, `:282-360` LoB rules for `AGENTS.md`, `:140` `k8s-openapi -F latest` (do NOT copy; pin a `v1_xx` feature that matches the pinned kind node image).
- `_bmad-output/planning-artifacts/epics.md:310-359` -- the story source.
- `_bmad-output/implementation-artifacts/epic-1-context.md` -- condensed Epic 1 decisions; read "Technical Decisions".
- `Cargo.toml` (workspace) / `control-plane/` / `agent/` / `agent-proto/` (`build.rs` with `tonic-build`) / `proto/agent/v1/agent.proto` -- minimal crates; `control-plane` depends on axum, tokio, sqlx 0.9 (postgres, runtime-tokio, tls-rustls, uuid, migrate); `agent` on kube (runtime, rustls), k8s-openapi, tokio. Do not add riverqueue (Story 1.2).
- `control-plane/src/httpapi/` -- generated rust-axum output target plus router mount; serve the SPA and `/api/v1/*` from one origin on port 8080. `api/openapi.yaml` needs one trivial operation (e.g. `GET /api/v1/healthz`) so generation produces real code.
- `web/` -- SvelteKit + Tailwind v4 + shadcn-svelte + `@xyflow/svelte` 1.6.x; `src/routes/+layout.ts` sets `ssr = false`; `src/lib/api/` generated types; `e2e/` Playwright.
- `charts/armoury/` -- umbrella chart with `charts/control-plane` and `charts/agent` subcharts (from `helm create`, stripped). No database subcharts yet.
- `mise-tasks/` -- file tasks: `check` (aggregate, fail fast with step names), `check/pins`, `gen/api`, `e2e`, `image/build`. `openapi-generator` runs from its digest-pinned image through `docker run`.
- `control-plane/Dockerfile`, `agent/Dockerfile` -- multi-stage, `cargo-chef`, distroless non-root runtime for the agent.
- `skaffold.yaml` -- artifacts for both images, Helm deployer with `setValueTemplates` (`repo:tag@digest`), `kind` profile, `portForward` 8080.
- `.github/workflows/ci.yml`, `build.yml` -- `jdx/mise-action` pinned by SHA; AGE image as a service container or started by the check task.
- `AGENTS.md`, `README.md` -- see AC-12. No `CLAUDE.md`.

## Tasks & Acceptance

**Execution:**
- [ ] `mise.toml`, `.gitignore` -- pin the toolchain and ignore build output -- AC-2 via VAL-5
- [ ] `Cargo.toml`, `proto/agent/v1/agent.proto`, `agent-proto/` -- workspace and proto codegen with the roundtrip test -- AC-1, AC-5 via VAL-1, VAL-2
- [ ] `control-plane/`, `agent/` -- minimal binaries, one-origin HTTP server on 8080, AGE `#[sqlx::test]` -- AC-1, AC-3 via VAL-1, VAL-3
- [ ] `api/openapi.yaml`, `mise-tasks/gen/api`, generated output -- generation and drift check -- AC-6 via VAL-7
- [ ] `web/` -- SvelteKit app, lint, `svelte-check`, Vitest test -- AC-1, AC-5 via VAL-4
- [ ] `charts/armoury/` -- umbrella chart and subcharts, `helm lint` -- AC-3, AC-5 via VAL-1
- [ ] `mise-tasks/check`, `mise-tasks/check/pins` -- aggregate gate with named steps; then run the defect demonstration -- AC-2, AC-3, AC-4 via VAL-1, VAL-5, VAL-6
- [ ] `control-plane/Dockerfile`, `agent/Dockerfile` -- digest-pinned multi-stage images with `cargo-chef` and the `ponytail:` comment -- AC-7 via VAL-8
- [ ] `skaffold.yaml`, `mise-tasks/e2e`, `web/e2e/smoke.spec.ts` -- kind dev loop and smoke test -- AC-8, AC-9 via VAL-9, VAL-10
- [ ] `.github/workflows/ci.yml`, `.github/workflows/build.yml` -- CI mirror and image build -- AC-10, AC-11 via VAL-11, VAL-12
- [ ] `AGENTS.md`, `README.md` -- rules, layout, PROC3, commands and Podman machine setup -- AC-12 via VAL-13

## Contract Approval

- Status: draft
- Approved by: pending
- Validation approved by: pending
- Approved at: pending
- Contract digest: pending
- Validation artifacts: `_bmad-output/test-artifacts/atdd-checklist-1-1-monorepo-scaffold-with-an-aggregate-local-gate-and-ci.md`; `agent-proto/tests/val_2_roundtrip.rs`; `control-plane/tests/val_3_age.rs`; `web/src/routes/val-4.test.ts`; `mise-tasks/check/pins.test.mjs`; `web/e2e/smoke.spec.ts`

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

## Review Triage Log

## Verification

**Commands:**
- `mise install && mise run check` -- expected: exit 0 with every step named
- `mise run gen:api && jj diff --stat` -- expected: no changes
- `skaffold dev -p kind` then `mise run e2e` -- expected: smoke test passes
- `uv run _bmad/custom/scripts/validate_story_contract.py validate --phase draft <this spec>` -- expected: valid
