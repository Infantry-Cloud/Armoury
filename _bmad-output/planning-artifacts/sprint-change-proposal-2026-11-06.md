---
status: approved
approved: 2026-11-06 — Daniel approved the whole proposal ("Yes, apply it")
applied: 2026-11-06 — sections 4.1-4.10 written into epics.md, architecture.md, epic-1-context.md and the STORY-1.1 spec status; architecture.md "Mirrors the project CLAUDE.md" also corrected to AGENTS.md
date: 2026-11-06
scope: moderate — process rule, two architecture decisions and six stories change their environment; no product behaviour changes; no approved story contract exists, so no contract revision is needed
workflow: bmad-correct-course (batch)
trigger: docs/agent-readiness.md decisions D1, D3-D8 (AR phase 2, 2026-11-06)
---

# Sprint Change Proposal — cluster-based dev loop and CI

## 1. Issue summary

**Problem.** The planning artifacts put the development loop and the CI test clusters on kind,
and kind on a local Podman machine. The workstation has a 2 GiB Podman machine. Daniel decided
during Agent Readiness (2026-11-06) that images build in his dev cluster, not on the workstation,
and that no heavy test service (AGE database, image builds, throwaway clusters) runs locally.

**Type.** Technical limitation and a deliberate environment decision, found before implementation.

**Evidence.**

- Workstation observation: Podman machine `applehv`, 2 GiB, 4 CPUs; no Rust, no kind.
- Daniel, 2026-11-06: "We're not going to build the images locally via Podman. We're going to do
  that on a cluster. I can provide a Kubernetes cluster." and "the age test database is going to
  kill my machine. I'd preferably not have any of those tests running here."
- AR decisions recorded in `docs/agent-readiness.md`:
  - D1: pin Helm 4; "Helm 3" in architecture.md is stale (host has Helm 4.3.1).
  - D3: Daniel owns the dev cluster; every cluster command names its kube context explicitly.
  - D4: images build on rootless, mTLS `buildkitd` in the cluster through a pinned `buildx`.
  - D5: dev images go to Harbor or Artifact Keeper (open item OI-2); official images stay on GHCR.
  - D6: the AGE test database is a digest-pinned Pod in the dev cluster.
  - D7: `openapi-generator` runs as a BuildKit stage (`--output type=local`).
  - D8: CI uses GitHub-hosted runners (fast tier) and ARC self-hosted runners in the cluster.
- Correct Course answers (2026-11-06): change every kind, Podman and Helm 3 reference; throwaway
  test clusters become temporary namespaces in the dev cluster on ARC runners; the Story 2.12
  timed install runs in a fresh namespace of the dev cluster.

## 2. Impact analysis

**Epic impact.** Epics 1, 2, 3 and 10 keep their goals and order. Only the environment of their
checks changes. No epic is added, removed or resequenced.

| Story | Impact |
| --- | --- |
| 1.1 | Dev loop, CI and build ACs change environment. STORY-1.1 spec (draft r1) returns to Build re-plan. |
| 1.2 | Install, durability and same-origin checks run in a fresh dev-cluster namespace. |
| 2.12 | Timed install runs in a fresh dev-cluster namespace. |
| 3.2 | Agent integration test runs in a temporary dev-cluster namespace on ARC. |
| 10.1 | Release self-scan runs in a temporary dev-cluster namespace on ARC. |
| 10.4 | Air-gap run uses a temporary namespace with default-deny egress. |

**Artifact conflicts.**

- PRD: none. NFR1 (one `helm install` for customers) and NFR4 are unchanged.
- UX: none.
- Architecture: "Images, chart build and the dev loop", "Versions" (Helm), scaffold comments,
  "Testing/Dev", "CI/CD", directory tree (also the stale `CLAUDE.md` entry; OQ-3 says no
  `CLAUDE.md`), process-rules line.
- Epics: ARCH23, ARCH27, ARCH34, PROC3, Stories 1.1, 1.2, 2.12, 3.2, 10.1, 10.4.
- `epic-1-context.md`: compiled from the above; update the same facts.

**Technical impact.**

- No local container runtime is required. Podman can stay installed but the project does not use it.
- New dependencies on the dev cluster (owned by Daniel, open item OI-3 in AR):
  - BuildKit endpoint and mTLS client files; dev registry (OI-2).
  - An AGE Pod reachable by port-forward locally and by Service DNS from ARC runners.
  - ARC runner scale set with a ServiceAccount that can create and delete temporary namespaces.
  - Story 3.2 needs cluster-scoped read-only RBAC (the agent's own ClusterRole) in the dev cluster.
  - Stories 1.2 (air-gap test) and 10.4 need a CNI that enforces NetworkPolicy egress rules.
- Risk: temporary namespaces share the dev cluster with the developer's own loop. Tests must name
  their namespace uniquely per run and assert only on objects in that namespace.

## 3. Recommended approach

**Direct Adjustment.** Edit the text below; keep every product AC and its oracle. Rollback is not
applicable (no code exists). MVP review is not needed (no scope change).

- Effort: low (text only, plus a Build re-plan of STORY-1.1).
- Risk: low to medium; the new cluster dependencies are tracked as AR open items OI-2 and OI-3.
- Timeline: no change to epic order.

## 4. Detailed change proposals

### 4.1 epics.md — requirements inventory

**ARCH23**

OLD:
> CI/CD on GitHub Actions, installing mise (`jdx/mise-action`, pinned by commit) and running the same mise tasks as local — `ci.yml` (`mise run check`: …), `build.yml` (…) …

NEW (insert after "running the same mise tasks as local"):
> ; untrusted code (fork pull requests) runs only the fast tier on GitHub-hosted runners, and the full gate, end-to-end tests and image builds run on ARC self-hosted runners in the dev cluster

Rationale: D8 and D13.

**ARCH27**

OLD:
> Tests co-located — `cargo nextest` + `#[sqlx::test]` against `apache/age:release_PG18_1.8.0` (in `mise run check` and as a CI service container); agent tested against a mocked kube client plus a kind cluster in CI; Vitest + Playwright (`web/e2e/`, `mise run e2e` against the Skaffold deployment) for the SPA.

NEW:
> Tests co-located — `cargo nextest` + `#[sqlx::test]` against `apache/age:release_PG18_1.8.0`, pinned by digest, which runs as a Pod in the dev cluster (`mise run check` reaches it by port-forward locally and by Service DNS on ARC runners; no local database); agent tested against a mocked kube client plus an integration test in a temporary dev-cluster namespace in CI; Vitest + Playwright (`web/e2e/`, `mise run e2e` against the Skaffold deployment) for the SPA.

Rationale: D6, D8.

**ARCH34**

OLD:
> … `skaffold.yaml` (pinned Skaffold) with the Helm deployer (`setValueTemplates`, `repo:tag@digest`) and a `kind` profile with port-forwarding is the development loop (PROC3). Customers install the published chart with one `helm install`. …

NEW:
> … `skaffold.yaml` (pinned Skaffold) with the Helm deployer (`setValueTemplates`, `repo:tag@digest`) is the development loop (PROC3): `mise run dev` builds both images on the in-cluster BuildKit (rootless, mTLS, through a pinned `buildx`), pushes them to the dev registry (`SKAFFOLD_DEFAULT_REPO`), deploys to the developer's namespace in the dev cluster with an explicit kube context, and port-forwards the UI and API to `localhost:8080`. A `ci` profile deploys to a temporary namespace from ARC runners. No local container runtime or local cluster is used. Customers install the published chart with one `helm install` (Helm 4). …

Rationale: D3-D5, D8. The `ponytail:` text stays.

**PROC3**

OLD:
> Every development step starts with `skaffold dev -p kind` running and deploying continuously. …

NEW:
> Every development step starts with `mise run dev` (Skaffold `dev` on the dev cluster) running and deploying continuously. …

The rest of PROC3 stays. Rationale: D3, D4.

### 4.2 epics.md — Story 1.1

AC "Given a developer workstation with mise installed":

OLD:
> **When** `skaffold dev -p kind` runs
> **Then** it builds both images, deploys the chart to a local kind cluster with the images as `repo:tag@digest`, port-forwards the UI and API, and redeploys after a code change (ARCH34, PROC3).

NEW:
> **Given** a developer workstation with mise and access to the dev cluster (kube context, in-cluster BuildKit, dev registry)
> **When** `mise run dev` runs
> **Then** Skaffold builds both images on the in-cluster BuildKit, pushes them to the dev registry, deploys the chart to the developer's namespace with the images as `repo:tag@digest`, port-forwards the UI and API to `localhost:8080`, and redeploys after a code change (ARCH34, PROC3)
> **And** no image build, database or cluster runs on the workstation.

AC "Given a push or pull request":

OLD:
> **Then** it installs mise with `jdx/mise-action` (pinned by commit), runs the same `mise run check` gate as local and fails on the same conditions.

NEW:
> **Then** it installs mise with `jdx/mise-action` (pinned by commit), runs the fast tier on GitHub-hosted runners for every event, and runs the full `mise run check` gate and `mise run e2e` on ARC runners in the dev cluster for pushes and same-repository pull requests; a fork pull request never reaches an ARC runner, and a required gate job fails unless every tier passed (ARCH23).

AC "Given a push" (build.yml):

OLD:
> **Then** it builds both images and packages the chart; on `main` it pushes them to GHCR (`ghcr.io`) by digest (ARCH23, ARCH34).

NEW:
> **Then** it builds both images on the in-cluster BuildKit from an ARC runner and packages the chart; on `main` it pushes them to GHCR (`ghcr.io`) by digest (ARCH23, ARCH34).

AC "Given the repository root":

OLD:
> **Then** a `CLAUDE.md`/`AGENTS.md` states … and PROC3 (keep `skaffold dev -p kind` running during every development step), and `README.md` documents the init, check, e2e and dev-loop commands.

NEW:
> **Then** `AGENTS.md` (no `CLAUDE.md`) states … and PROC3 (keep `mise run dev` running during every development step), and `README.md` documents the init, check, e2e and dev-loop commands and the dev-cluster prerequisites.

### 4.3 epics.md — Story 1.2

OLD:
> **Given** the Skaffold `kind` profile from Story 1.1
> **When** `skaffold run -p kind` deploys the chart
> **Then** the install, durability and same-origin checks in this story run against that deployment, so they exercise the built images, not placeholders (ARCH34).

NEW:
> **Given** the Skaffold `ci` profile from Story 1.1
> **When** it deploys the chart into a fresh, uniquely named namespace of the dev cluster (from an ARC runner in CI, or with `mise run` locally)
> **Then** the install, durability and same-origin checks in this story run against that deployment, so they exercise the built images, not placeholders, and the namespace is deleted afterwards (ARCH34).

Air-gap AC: append to "(verified by a network-policy or egress-capture test)":
> ", in a namespace of the dev cluster whose CNI enforces NetworkPolicy egress rules"

### 4.4 epics.md — Story 2.12

OLD:
> **Given** a kind cluster and a seeded test registry
> **When** the scripted run deploys the chart with the Skaffold `kind` profile (ARCH34), then times …

NEW:
> **Given** a fresh, uniquely named namespace in the dev cluster and a seeded test registry
> **When** the scripted run deploys the chart into that namespace with Skaffold (ARCH34), then times …

Append to the same AC:
> **And** the script deletes the namespace when it finishes, pass or fail.

### 4.5 epics.md — Story 3.2

OLD:
> **Then** unit tests run against a mocked kube client and an integration test runs against a kind cluster in CI (ARCH27).

NEW:
> **Then** unit tests run against a mocked kube client and an integration test runs in a temporary namespace of the dev cluster on an ARC runner in CI, with the agent's own read-only ClusterRole, asserting only on workloads in its namespace (ARCH27).

### 4.6 epics.md — Story 10.1

OLD:
> **When** the release workflow installs the release in a kind cluster, connects that instance to GHCR as a registry and lets it scan the release images

NEW:
> **When** the release workflow installs the release in a temporary namespace of the dev cluster from an ARC runner, connects that instance to GHCR as a registry and lets it scan the release images

Append to that AC:
> **And** the namespace is deleted when the run finishes.

### 4.7 epics.md — Story 10.4

OLD:
> **Given** a kind cluster with all egress blocked except to an internal registry and an internal package feed

NEW:
> **Given** a temporary namespace of the dev cluster with a default-deny egress NetworkPolicy that allows only an internal registry and an internal package feed (the cluster CNI enforces and logs egress policy)

The rest of Story 10.4 stays ("executed in CI on each release" now means an ARC runner).

### 4.8 architecture.md

| Location | OLD | NEW |
| --- | --- | --- |
| "Images, chart build and the dev loop" (line 113) | "`skaffold dev -p kind` builds both images, deploys the chart to a local kind cluster with the Helm deployer …" | "`mise run dev` runs Skaffold: it builds both images on the in-cluster BuildKit (rootless, mTLS, pinned `buildx`), pushes them to the dev registry, deploys the chart to the developer's namespace in the dev cluster with the Helm deployer … No local container runtime or cluster is used (amended 2026-11-06)." |
| Versions (line 117) | "Helm 3" | "Helm 4" |
| Scaffold comments (149, 151) | "pins rust, node, helm, kind, skaffold" / "profile `kind`, portForward UI + API" | "pins rust, node, helm, buildx, kubectl, skaffold" / "profiles `dev` and `ci`, portForward UI + API" |
| Testing/Dev (163) | "… in `mise run check` and as a CI service container; agent … integration-tested against a kind cluster in CI; … `skaffold dev -p kind` runs …" | "… as a digest-pinned Pod in the dev cluster, used by `mise run check` locally (port-forward) and on ARC runners; agent … integration-tested in a temporary dev-cluster namespace in CI; … `mise run dev` runs …" |
| CI/CD (201) | "GitHub Actions, all jobs installing mise …" | Add: "Fork pull requests run only the fast tier on GitHub-hosted runners; the full gate, e2e and image builds run on ARC self-hosted runners in the dev cluster." |
| Tree (384, 386, 387) | "Helm, kind, Skaffold"; "Helm deploy to kind (PROC3)"; "`CLAUDE.md` # LoB rules (generated from Daniel's template)" | "Helm, buildx, Skaffold"; "Helm deploy to the dev cluster (PROC3)"; "`AGENTS.md` # LoB rules, layout, PROC3 (no CLAUDE.md)" |
| Process rules (538) | "PROC3 (`skaffold dev -p kind` runs continuously …)" | "PROC3 (`mise run dev` runs continuously …)" |

### 4.9 epic-1-context.md

- "Dev loop rule": `skaffold dev -p kind` → `mise run dev` (Skaffold on the dev cluster).
- "Gate": `#[sqlx::test]` line adds "as a Pod in the dev cluster"; CI line adds the hosted and ARC tiers.
- "Code rules": "`AGENTS.md`/`CLAUDE.md` states" → "`AGENTS.md` states".
- "Cross-Story Dependencies": "Story 1.2 needs the 1.1 images and kind profile … `skaffold run -p kind`" → "Story 1.2 needs the 1.1 images and the Skaffold `ci` profile; its checks run in a fresh dev-cluster namespace".

### 4.10 STORY-1.1 Build spec

The contract is draft r1 and was never approved, so no new Revision is needed. The change is
semantic (AC-8, AC-10, AC-11 environment; VAL-9, VAL-11; OQ-1; assumptions; Code Map).

- Set frontmatter `status: 'draft'` so Build re-plans and repeats CHECKPOINT 1.
- Add a `## Spec Change Log` entry naming this proposal.
- Do not edit the frozen block here. Build re-plan proposes the frozen edits for Daniel's approval.
- Locked scaffolds are not locked yet (no approval); none needs a change for this proposal.

## 5. Implementation handoff

**Scope: moderate.** Backlog text changes plus a story re-plan.

| Who | Does | Done when |
| --- | --- | --- |
| Correct Course (this run) | Apply sections 4.1-4.9 and the 4.10 status change after approval; run Linear Reconcile | Text applied; reconcile `plan --check` result reported |
| `bmad-build` (re-plan) | Re-plan STORY-1.1 against the new ACs; frozen edits only with Daniel's approval | Build CHECKPOINT 1 passes; draft validation VALID |
| Murat (`bmad-testarch-atdd`, Edit) | VAL-1, VAL-7 (SD-3), VAL-9, VAL-11; fix stale Rust scaffold comments; CI naming check; approval | Approved-phase validation passes |
| Daniel | OI-2 (registry), OI-3 (contexts, CI namespace, BuildKit, AGE Pod, ARC, NetworkPolicy-capable CNI) | Recorded in `docs/agent-readiness.md` |

**Success criteria.**

- `rg -n -i "kind cluster|-p kind|podman|Helm 3"` finds nothing in `epics.md`, `architecture.md`
  or `epic-1-context.md`.
- Every product AC keeps its oracle; only the environment text changes.
- The STORY-1.1 spec is `draft` and passes draft validation.
