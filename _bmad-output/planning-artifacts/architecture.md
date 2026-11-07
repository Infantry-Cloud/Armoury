---
stepsCompleted: [1, 2, 3, 4, 5, 6, 7, 8]
lastStep: 8
status: 'complete'
completedAt: '2026-06-14'
revisedAt: '2026-11-01'  # backend Go → Rust (control plane + agent)
amendedAt: '2026-11-07'  # Correct Course: sprint-change-proposal-2026-11-07-readiness.md (readiness blockers B1–B8) and sprint-change-proposal-2026-11-07.md (UX spines ux-Armoury-2026-11-06; FR32/FR33); earlier: sprint-change-proposal-2026-11-05.md (readiness fixes, FR31/NFR12)
inputDocuments:
  - _bmad-output/planning-artifacts/prds/prd-Armoury-2026-06-11/prd.md
  - _bmad-output/planning-artifacts/prds/prd-Armoury-2026-06-11/addendum.md
  - _bmad-output/planning-artifacts/briefs/brief-Armoury-2026-06-11/brief.md
  - _bmad-output/planning-artifacts/ux-designs/ux-Armoury-2026-11-06/DESIGN.md
  - _bmad-output/planning-artifacts/ux-designs/ux-Armoury-2026-11-06/EXPERIENCE.md
  - _bmad-output/planning-artifacts/research/market-software-supply-chain-security-research-2026-06-11.md
workflowType: 'architecture'
project_name: 'Armoury'
user_name: 'Daniel'
date: '2026-06-13'
---

# Architecture Decision Document

_This document builds collaboratively through step-by-step discovery. Sections are appended as we work through each architectural decision together._

## Project Context Analysis

_Historical analysis from before the decisions below. Where it names GUAC as a component, the later decision applies: GUAC is deferred and the AGE graph in PostgreSQL is used (Core Architectural Decisions)._

### Requirements Overview

**Functional Requirements (33 across 6 groups):**

- **Fleet Inventory (FR1–FR5, FR29, FR31, FR32):** Two ingestion sources — registry/package-feed enumeration (FR1, FR29) and a live Kubernetes cluster agent (FR3) — joined into one inventory with shipped-vs-running reconciliation (FR4), honest coverage gaps (FR5) and the signature status of registry artifacts, verified against trusted signers (FR32). _Architecturally: pull-based connectors + central Syft SBOM generation (FR2). An optional CI scan (FR31) submits an artifact by digest or upload; the server still does all scanning (NFR12)._
- **Consistent Scanning & Lifecycle Freshness (FR6–FR10):** Single fleet-wide Grype config (FR6); feed-driven re-evaluation of _stored_ SBOMs without rebuilds (FR7); evaluation provenance recorded (FR8); continuous auto-onboarding within 1h (FR9); air-gapped signed feed bundles (FR10). _Architecturally: the core asynchronous job/scheduler + feed-versioning subsystem, decoupled from builds._
- **Enrichment & Prioritization (FR11–FR15, FR33):** Multi-source post-NVD enrichment (KEV, EPSS, CNA, OSV) with per-datum source attribution (FR11–FR12); end-of-life data for packages, attributed the same way (FR33); deterministic, explainable ordering in severity groups (FR13); triage decisions as first-class versioned data (FR14); VEX ingest + emit (FR15).
- **Blast-Radius & Posture (FR16–FR20, FR30):** Fleet posture landing view (FR16); sub-minute blast-radius query over the graph (FR17); artifact detail (FR18); exportable answers, stored as evidence (FR19); Prometheus metrics, pull-only (FR20); a data-quality score distinct from risk (FR30).
- **Compliance Evidence (FR21–FR25):** CRA pack as first instance of an extensible pack architecture over the evidence graph (FR21–FR22); evidence collected continuously, generated on demand (FR23); PDF + machine-readable companions (FR24); Sigstore/operator-key signed (FR25).
- **License Compliance (FR26–FR28):** Grant across its full surface (SBOM/image/filesystem) (FR26); fleet allow/deny policy surfaced as findings (FR27); embedded in evidence packs (FR28).

**Non-Functional Requirements (architecture-driving):**

- **NFR1 (30-min time-to-value, visibly populating)** + **NFR5 (1-hour feed re-evaluation)** + **NFR2 (sub-minute blast-radius)** — three hard performance gates that constrain the job pipeline and query layer.
- **NFR3 (scale anchor):** hundreds of repos, thousands of images, ≤10 clusters — sizing target for storage, graph, and scheduler.
- **NFR4 (self-hosted Helm, fully air-gapped, no phone-home)** — constrains every external dependency and the signing/feed-update design.
- **NFR6 (declarative OIDC + bootstrap admin; 3 roles: admin / analyst / read-only auditor).**
- **NFR7 (Armoury's own releases SLSA/Sigstore-attested).**
- **NFR8 (honest degradation — failures always visible in posture + metrics).**
- **NFR9 (read-only, watch/list-only cluster agents; never cluster-admin).**
- **NFR10 (single-instance control plane v1; durable evidence survives loss).**
- **NFR11 (append-only, tamper-evident evidence store).**
- **NFR12 (server-side evaluation — Syft, Grype, Grant and policy run only on the control plane; clients only identify artifacts or supply bytes).**

### Scale & Complexity

- Primary domain: **self-hosted full-stack** (SvelteKit/shadcn-svelte SPA + control-plane backend + per-cluster read-only K8s agents, Helm-delivered).
- Complexity level: **High / enterprise** — distributed, graph-backed, compliance-grade, dual-mode (connected + air-gapped).
- Estimated major architectural components: **~10** — UI; API/query layer; graph store (GUAC); SBOM/scan orchestrator + scheduler; feed-ingestion & re-evaluation engine; enrichment aggregator; evidence store (append-only); pack generator + signer; cluster agent; metrics endpoint.

### Technical Constraints & Dependencies

- **Named OSS substrate (non-negotiable):** Syft, Grype, GUAC, Grant, Sigstore/cosign. Architecture orchestrates these as components, does not reinvent them. Multi-scanner neutrality is **rejected, not deferred** — go hard on Syft+Grype only.
- **Kubernetes-native delivery:** Helm chart; control plane runs in the customer's existing cluster.
- **Air-gapped parity:** every feed/update/signing path must have an offline equivalent; no capability may silently require internet.
- **GUAC's role is an open architectural decision:** system-of-record vs. rebuildable projection over our own evidence store. Treating GUAC as a derived, rebuildable index (our store as source-of-truth) contains its incubating-maturity risk and keeps NFR1/NFR2 off GUAC's pre-1.0 guarantees. GUAC's multi-service footprint (NATS, collectors, GraphQL) pressures NFR1 (install) as much as NFR2 (query) — it may even belong off the install path (crack A7).
- **Re-evaluation is a feed-delta join, not a rescan:** NFR5 (1-hour fleet-wide) is a batch-throughput problem — diff the feed to changed CVEs/affected-ranges, match only affected stored packages. A naive full rescan breaks both NFR5 and the UJ-2 "already re-evaluated overnight" promise.
- **K8s API as running-truth has resolution gaps (crack A3):** running digests may come from registries Armoury isn't connected to, mutable tags, mirror/proxy digests, or third-party sidecars — so "what's running" can be under-counted, not just incomplete (see R7).
- **Single primary registry assumed in first session** (extensible after).

### Cross-Cutting Concerns Identified

- **Air-gapped operation is an architectural axis (likely an instance-mode), not a feature** — it reshapes signing, feed ingress, _and_ enrichment ingress (KEV/EPSS/OSV/CNA must ride the offline bundle too, beyond FR10/FR25).
- **Evidence integrity & provenance** — append-only storage, tamper-evidence, pack signing, source attribution on every datum.
- **Agent state-recovery model (open):** buffer-and-replay vs. stateless re-derive from the K8s API on reconnect — with reconnect-storm implications (see R3 coupling note).
- **Honest degradation** — coverage gaps, stale feeds, disconnected agents, unmatched running digests must surface as first-class data through API → UI → metrics.
- **RBAC** — admin/analyst/read-only-auditor enforced across every surface and the pack generator.
- **Observability** — Prometheus pull-only; _no_ in-product notifications anywhere. (The Issues nav badge shows the Needs-attention count — what needs a decision — and is not a new-findings notification; badges for new findings stay banned.)
- **Determinism & explainability** — issue ordering (FR13: severity groups, actively exploited first within each) and data-quality (FR30) must be reproducible and inspectable.

### Architectural Risk Register (pre-decision)

Non-obvious risks surfaced during context analysis, carried forward into the decision steps. (R6 — a single-instance batch/query workload-isolation mandate — was considered and cut: NFR10 is a deliberate v1 simplification, not a constraint to architect around.)

| #   | Risk                                                                                                                      | Detection / mitigation hook                                                                                           |
| --- | ----------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| R1  | GUAC query latency degrades non-linearly at upper scale anchor → blast-radius slips past "seconds" (NFR2)                | Query-latency SLO from day one, surfaced via NFR8 path. Favors GUAC-as-rebuildable-projection — _but the rebuild-from-ledger path is itself a load-bearing, must-be-tested component, not an assumed fallback._ _(Superseded: GUAC is deferred; the AGE graph is rebuilt from the relational tables, Story 6.1.)_ |
| R2  | Re-eval throughput bottleneck is feed-delta computation, invisible until a large feed lands; runs overlap next update → backpressure/staleness | Treat feed-delta as a discrete measurable stage; surface backpressure honestly, never hide                           |
| R3  | Agent drops events during control-plane restart (expected under single-instance NFR10) → running-inventory silently desyncs (violates NFR8) | Decide buffer-replay vs. stateless re-derive. If stateless: **jittered reconnect + bounded reconciliation rate** so ≤10 clusters don't storm the just-recovered control plane |
| R4  | Agent transport works connected but breaks under air-gapped mTLS/egress/proxy reality — on exactly the regulated buyers who matter | Design transport against locked-down networks from the start                                                         |
| R5  | Evidence-ledger durability is a _stronger_ requirement than the rest of the DB (NFR10/NFR11), with no cloud backup fallback air-gapped | Separate immutable hash-chained ledger from mutable operational state; air-gap-safe backup story                     |
| R7  | Running digests unmatched to any connected source → invisible _under_-count of "what's running" (worse than over-counting) | Surface as a first-class coverage row ("N running digests not matched to any connected source")                      |
| R8  | Corrupt/partial feed bundle (air-gap, FR10) drives a false-green re-eval → a signed CRA pack seals the false-green       | Atomically validate + sign bundles before they can drive re-eval; partial/failed import **fails closed as stale**, never applies silently |
| R9  | Shared storage contention: a ledger-append failure under disk pressure also freezes operational scan jobs (SPOF, distinct from R5 loss) | Report ledger/history size and database volume headroom on the health endpoint and in metrics, with a warning threshold (Postgres has no tablespace quotas; amended 2026-11-05) |
| R10 | Evidence immutability (NFR11) + signing (FR25) **amplify** upstream data errors (enrichment drift, bad feed) into sealed, uncorrectable records | Versioned, superseding corrections; record enrichment/feed **source versions** on findings and pack covers so a later correction is explainable, not locked |
| R11 | Rust backend runs Grype as a subprocess per SBOM (spawn + DB open each time) → re-eval throughput may miss NFR5's 1-hour bound at the scale anchor | Bounded parallel worker pool; measure per-SBOM cost in the R1/R2 load test. Fallback only if the CLI fails the bar: a long-lived Go matcher sidecar (the one Go component allowed back in) |

## Starter Template Evaluation

### Primary Technology Domain

**Multi-component self-hosted system** — there is no single monolithic starter. Four deliverables in **one monorepo** (Daniel's call), all versioned/released together to support SLSA-attested unified releases (NFR7):

1. Web SPA (Svelte) · 2. Rust control plane · 3. Rust cluster agent · 4. Helm chart

Guiding principle (from project memory): **API-first** — the UI, future MCP server, and Prometheus metrics are all consumers of one API spine. The SPA is just the first client.

### Starter Options Considered

- **Frontend — SvelteKit (static/SPA) vs. plain Svelte + Vite.** Chose **SvelteKit with `adapter-static` + SSR disabled**: it's shadcn-svelte's first-class path, uses Vite under the hood, and produces a pure client-rendered SPA (static assets, no Node runtime to operate self-hosted/air-gapped) while giving us file-based routing for the seven sidebar surfaces (Home, Software, Issues, Exposure, Reports, Settings, Help). Plain Svelte+Vite is the fallback if we want to avoid SvelteKit entirely.
- **Graph library — Svelte Flow (`@xyflow/svelte`, stable v1.6.0)** for the Exposure map (hairline four-tier graph with circular nodes; Blast radius and Graph explorer merged into Exposure, which keeps moving the map to any node). Stable 1.x release on the same shared core (`@xyflow/system`) as React Flow; further de-risked by the mandatory Graph/Table equivalent (accessibility requirement) so it is never a single point of failure.
- **Backend — Rust, no framework starter.** _Changed from Go on 2026-11-01 (Daniel: more confident with Rust for AI-driven development; the compiler catches more agent mistakes)._ `axum` on `tokio` — a thin router, not a heavyweight framework — producing a lean static (musl) binary for air-gapped Helm delivery. API-first via an OpenAPI contract with generated server types + typed TS client for the SPA. Consequence: the Go OSS substrate is no longer callable in-process — see **Substrate Integration**.
- **Cluster agent — `kube-rs` (`kube` + `kube-runtime` watchers/reflectors), no CRDs.** NFR9 makes the agent a read-only watch/list reporter, not a CRD-owning operator, so no operator framework is needed.
- **Monorepo tooling — Cargo workspace + a task runner.** Root `Cargo.toml` workspace spanning `control-plane`, `agent`, and a shared `agent-proto` crate (agent↔CP protocol types), the SPA under `web/`, charts under `charts/`, driven by **mise** — `mise.toml` pins every tool, and tasks are mise file tasks in `mise-tasks/` (`mise run check`, `mise run e2e`, `mise run gen:api`). Rejected Nx/Turborepo — JS-centric, poor Rust fit. _Taskfile replaced by mise on 2026-11-05 (Daniel)._
- **Images, chart build and the dev loop (2026-11-05, Daniel).** Multi-stage Dockerfiles for `control-plane` and `agent` (base images pinned by digest). A GitHub Actions pipeline (`build.yml`) builds the official images and packages the chart on each push, and pushes them to GHCR by digest on `main`. **Skaffold** is the development loop: `mise run dev` runs Skaffold, which builds both images on the in-cluster BuildKit (rootless, mTLS, pinned `buildx`), pushes them to the dev registry, deploys the chart to the developer's namespace in the dev cluster with the Helm deployer (`setValueTemplates`, images as `repo:tag@digest`) and redeploys on each change (PROC3). No local container runtime or cluster is used (amended 2026-11-06). Customers still install the published chart with one `helm install`. `ponytail:` Rust image rebuilds are slow; the dev profile uses a debug build and a cached dependency layer (for example `cargo-chef`). Upgrade path: a remote build cache.

### Selected Stack & Scaffold

**Versions (current as of 2026-06 — pin at init, not hardcoded forever):** Rust stable (2024 edition) · Svelte 5 / SvelteKit 2 / Vite / Tailwind v4 · shadcn-svelte (latest, runes-native) · `@xyflow/svelte` v1.6.x · `kube-rs` · `tonic` · `sqlx` · Helm 4 · pinned Syft/Grype/Grant/cosign CLIs.

**Initialization commands (these become the first implementation story):**

```bash
# --- repo root: Cargo workspace ---
# root Cargo.toml: [workspace] members = ["control-plane", "agent", "agent-proto"], resolver = "3"

# --- web SPA: SvelteKit (static SPA) + Tailwind + shadcn-svelte ---
npx sv create web --template minimal --types ts --add tailwindcss
cd web
npx shadcn-svelte@latest init          # new-york style, wires Tailwind v4 + components.json
npm i @xyflow/svelte                    # Svelte Flow (stable) for the Exposure map (Graph view; the Table view is the equivalent)
# set adapter-static + `export const ssr = false` in the root +layout for SPA mode
cd ..

# --- Rust control plane ---
cargo new control-plane --bin --name armoury
(cd control-plane && cargo add axum tokio -F tokio/full && cargo add sqlx@0.9 -F postgres,runtime-tokio,tls-rustls,uuid,migrate)
# riverqueue =0.5.0 (requires sqlx 0.9 + jiff) is added in Story 1.2 with its enqueue/run test

# --- Rust cluster agent (kube-rs, read-only watcher) ---
cargo new agent --bin --name armoury-agent
(cd agent && cargo add kube -F runtime,rustls-tls && cargo add k8s-openapi -F latest && cargo add tokio -F full)

# --- shared agent protocol (tonic/prost codegen from proto/agent/v1 in build.rs) ---
cargo new agent-proto --lib

# --- Helm chart ---
helm create charts/armoury           # then strip to control-plane + agent subcharts

# --- toolchain, tasks, images and dev loop (amended 2026-11-05) ---
# mise.toml pins rust, node, helm, buildx, kubectl, skaffold and the other tools; tasks live in mise-tasks/
# control-plane/Dockerfile (armoury + SPA build), agent/Dockerfile (armoury-agent only)
# skaffold.yaml: artifacts control-plane + agent, Helm deployer, profiles `dev` and `ci`, portForward UI + API
# .github/workflows/ci.yml (mise run check), build.yml (images + chart → ghcr.io by digest on main)
# web: npm i openapi-fetch @tanstack/svelte-query && npm i -D openapi-typescript @playwright/test
# mise run gen:api: openapi-generator (pinned container image, no local Java) + openapi-typescript
```

**Architectural decisions provided by this scaffold:**

- **Language & Runtime:** Rust stable (static binaries); Syft/Grype/Grant/cosign run as pinned CLI subprocesses shipped in the control-plane image; Svelte 5 + TypeScript SPA.
- **Styling:** Tailwind v4 + shadcn-svelte (owned components, copied in); design tokens map onto shadcn CSS variables per DESIGN.md "shadcn mapping" (ux-Armoury-2026-11-06): two themes over the same semantic roles — Light (default, unsuffixed tokens) and Dark (`-dark` tokens) — plus `--paper`, `--dq`, `--dq-muted` and `--dq-wash`; `print-*` tokens feed the Typst templates only. Fonts: IBM Plex Sans and IBM Plex Mono, self-hosted (SIL OFL 1.1).
- **Build tooling:** Vite (via SvelteKit) for the SPA; Cargo for binaries; mise tasks (`mise-tasks/`) orchestrate the monorepo; Skaffold builds and deploys for development; GitHub Actions builds the official images and chart.
- **Code organization:** `web/` · `control-plane/` · `agent/` · `charts/` · shared crates via the Cargo workspace; OpenAPI spec as the API source of truth.
- **Testing/Dev:** Vitest + Playwright (SPA); `cargo nextest` + `#[sqlx::test]` (per-test Postgres DB) for the control plane; `#[sqlx::test]` runs against `apache/age:release_PG18_1.8.0` (pinned by digest) as a Pod in the dev cluster, used by `mise run check` locally (port-forward) and on ARC runners; agent unit-tested against a mocked `kube` client and integration-tested in a temporary dev-cluster namespace in CI; Playwright e2e (`mise run e2e`) runs against the Skaffold deployment. Development loop: `mise run dev` runs and redeploys continuously while code is written (PROC3).

**Note:** Repo + scaffold initialization (above) should be the first implementation story.

**Downstream doc fix (done 2026-11-01):** DESIGN.md / EXPERIENCE.md now name Svelte (SvelteKit + shadcn-svelte); visual identity and tokens unaffected. **Superseded 2026-11-06:** the UX spines are now `ux-Armoury-2026-11-06` (Greenhouse: light default + one dark theme, IBM Plex, labelled sidebar, three-column master-detail); still SvelteKit + shadcn-svelte + Tailwind.

## Core Architectural Decisions

### Decision Priority Analysis

**Critical (block implementation):**

- **Governing principle — all scanning on the server (NFR12, 2026-11-05, Daniel).** Syft, Grype, Grant, license policy, the CI policy and every other check run only in the control plane with the single fleet tool versions and configuration. A CI runner, a cluster agent or any other client only identifies an artifact or supplies its bytes. The server never uses an SBOM, finding, license result or verdict that a client computed. This principle overrides any conflicting statement in this document.
- **Datastore:** **PostgreSQL 18** + **Apache AGE 1.8** (image `apache/age:release_PG18_1.8.0`, pinned by digest — the bundled chart database and the test database) — relational + openCypher graph in one engine. Blast-radius (CVE→package→artifact→workload+time) runs as AGE Cypher traversals.
- **Blob/ledger storage:** **SeaweedFS** (bundled, S3-compatible; external S3 optional) for SBOM blobs and temporal-ledger compaction.
- **Job/queue + re-eval engine:** **River** via its Rust client **`riverqueue`** ([docs](https://riverqueue.com/docs?lang=rust); Postgres-backed, transactional enqueue — a job is inserted in the same transaction as the data it concerns; built on `sqlx` + `tokio`, matching our stack; optional self-hosted River UI). The Rust client is young (first release 2026-10) but shares River's mature database schema and job protocol with the Go original. Pinned `=0.5.0` (2026-11-02): it requires `sqlx` 0.9 and `jiff`, and ships its own migrator (`riverqueue-migrate`); River migrations run before the `sqlx` migrations. Story 1.2 proves that a job enqueued in a transaction is run by a worker; if that fails, switch to the fallback there, before any story depends on the queue. Fallback if it bites: `graphile_worker`; re-evaluation is a **feed-delta join** (changed CVEs/ranges → affected stored packages), never a fleet rescan (NFR5).
- **Evidence ledger and history:** append-only, **hash-chained** rows in Postgres (NFR11); corrections are superseding entries (FR14). Evidence-bearing tables keep every past version in **history tables** (see Data Architecture → Evidence history), so any past state is one indexed query (FR23).
- **Agent transport:** **agent-initiated outbound, HTTPS/gRPC + mTLS** (gRPC streaming, HTTPS long-poll fallback where proxies block it) — no inbound to prod clusters (R4). _(Amended 2026-11-05.)_ The agent uses its own control-plane port, separate from the UI/API port; that one port serves gRPC and the long-poll fallback. The control plane ends mTLS itself (`rustls`), so it sees the client certificate; nothing in between ends TLS. The chart exposes the port as a `LoadBalancer` or `NodePort` Service, or through an ingress with TLS passthrough. An ingress that ends TLS is not supported for the agent port, and the chart documentation says so.
- **Agent recovery:** **stateless re-derive** — relist from K8s API on reconnect, control plane reconciles; jitter + bounded rate on reconnect (R3).
- **Auth:** OIDC code flow + declarative config + bootstrap admin (NFR6); **httpOnly secure cookie session** for the SPA (avoids tokens-in-JS / XSS). _(Amended 2026-11-05.)_ Sessions live in a PostgreSQL `sessions` table: the cookie holds a random session ID and the table stores only its hash. Sessions survive a restart; sign-out deletes the row. Idle timeout and maximum lifetime are Helm values (PROC2; defaults 8 h idle, 24 h maximum). User preferences (theme `light` | `dark`, default `light` when none is stored; single-key keyboard shortcuts on or off, default on — WCAG 2.1.4) live in `user_preferences`, keyed by a stable user ID (OIDC issuer + `sub`; a fixed ID for the bootstrap admin), via `GET`/`PUT /api/v1/me/preferences`; every role can change its own preferences. Sessions and preferences are operational data, marked "not evidence" for the history coverage test.
- **API spine:** OpenAPI-first; server types generated from `api/openapi.yaml` (`openapi-generator` `rust-axum` target) + **`openapi-typescript` + `openapi-fetch`** (typed TS client, used with svelte-query). `openapi-generator` runs from its pinned container image, so no local Java is needed; `mise run gen:api` regenerates, and `mise run check` fails if generated code differs from committed code. Fallback if the Rust generator fights us: code-first `utoipa`, with CI failing on any diff between the emitted and committed spec — the committed spec stays the contract either way.

**Important (shape architecture):**

- **RBAC:** admin / analyst / read-only auditor enforced in API middleware; read-only auditor mutations _absent_, not disabled (per EXPERIENCE spec).
- **Secrets at rest:** registry/feed credentials envelope-encrypted; key material from a k8s Secret / Helm value. _(Amended 2026-11-05.)_ AES-256-GCM with `aws-lc-rs` (already used by `rustls`). Each credential has its own random data key; the master key encrypts the data keys. Each record stores a key ID for rotation: add a new master key, re-encrypt the data keys with a job, then remove the old key. The record ID is AAD (associated data), so an encrypted value cannot move to another record. With no master key in the chart, the control plane generates one on first start and stores it in a Secret (same pattern as the signing key).
- **Signing (FR25/NFR7) — amended 2026-11-05.** Runtime signing (packs, ledger checkpoints) uses `cosign` with setting `signing.mode` (PROC2); operator-built feed bundles (Story 4.5) are always signed with the operator key:
  - `key` (**default**): the operator key from a Secret. If none is supplied, the control plane generates one on first start and stores it in a named Secret in its own namespace (its RBAC covers only that Secret); Settings shows the public key. Each public key in use is appended to the ledger, so old signatures stay verifiable after rotation.
  - `keyless` (opt-in): a projected service-account token (audience `sigstore`) to public Fulcio — which accepts only EKS, GKE and AKS issuers — or to a configured private Fulcio, with Rekor. If the issuer is not accepted, startup fails with a clear message.
  - Air-gapped mode always uses `key`. The mode and signer identity are recorded on each signature. Verification never requires internet.
  - Reason: public Fulcio does not trust self-managed clusters, and keyless signatures publish the cluster issuer URL to the public Rekor log.
  - `ponytail:` a key in a Kubernetes Secret is only as safe as the cluster. Upgrade path: a cosign KMS key reference (cloud KMS or Vault).
  - Build-time keyless signing of Armoury's own releases in CI (NFR7) is unchanged.
  - Armoury-published feed bundles (Story 10.2; used only by air-gapped instances; each published bundle is complete — it carries the full CVE List v5 snapshot, not a delta — so it imports into any instance; its SLSA provenance is signed with the same KMS bundle key via `cosign attest --key`, so the import verifies signature and provenance offline with one shipped public key and no Sigstore trust root) are the exception: they are signed with a long-lived **bundle signing key** held in a cloud KMS that cosign supports (the private key never leaves the KMS; the workflow authenticates with GitHub OIDC, so no long-lived secret is stored). The chart ships the public key in the Story 4.6 trusted-key list, so users configure nothing. Rotation: the chart ships the old and new public keys together for 12 months. Reason: offline import verifies against public keys, and keyless verification would need a Sigstore trust root in every air-gapped instance.
- **Frontend server-state:** **`@tanstack/svelte-query`** for server-state caching (the Home summary and Needs-attention count from the posture API, Exposure answers from the blast-radius API, the Issues, Software and Reports lists); Svelte 5 runes for local state.
- **Delivery:** Helm **umbrella chart + subcharts** (control-plane, agent), bundling Postgres-AGE + SeaweedFS by default, **external DB/S3 opt-in**; `adapter-static` SPA served by the control plane.
- **Air-gap:** instance-mode flag reshaping feed ingress, enrichment ingress, and signing paths (architectural axis, not a feature).
- **CI client (FR31, decided 2026-11-05):** the `armoury` binary is also published as a standalone CLI for Linux and macOS (x86-64, arm64) as GitHub Release files, each with a checksum, a cosign signature and SLSA provenance. It contains no scanners (NFR12). The GitHub Action lives in `action/` in this repository and uses the same version tags; it downloads the CLI and verifies the checksum and signature before it runs `armoury scan`. A separate Marketplace repository can come later.
- **CI/CD:** GitHub Actions, all jobs installing mise (`jdx/mise-action`, pinned by commit) and running the same mise tasks as local. Fork pull requests run only the fast tier on GitHub-hosted runners; the full gate, e2e and image builds run on ARC self-hosted runners in the dev cluster (amended 2026-11-06). `ci.yml` runs `mise run check`; `build.yml` builds the images and packages the chart on each push and pushes them to GHCR by digest on `main`; `release.yml` reuses those digests and adds release tags, **SLSA provenance + keyless cosign signatures** and SBOM attestations for images, charts and the CLI (NFR7). A scheduled `bundles.yml` builds, signs and attests the Armoury-published feed bundles (Story 10.2).
- **Observability:** Prometheus `/metrics`, pull-only (FR20); no in-product notifications. _(Amended 2026-11-05.)_ Armoury does not define "new": the counter `armoury_findings_created_total{severity, kev}` increases when a finding appears or becomes KEV-listed, and the gauge `armoury_findings_open{severity, kev, triage_status}` gives open counts. Alerts compute "new" in Prometheus (for example `increase(...[1h]) > 0`). Labels stay bounded; never per artifact or per CVE. These metrics count findings (one per place); the UI counts issues (finding groups), so a metric total can be higher than the number on screen.
- **Vendor VEX matching (FR15, amended 2026-11-05):** exact identifiers only, in this order: image digest; purl with version; purl without version. No fuzzy name or CPE matching. A statement with no fleet match is stored and shown as "no fleet match". Each applied match records the rule that matched.
- **Stored exports (FR19, decided 2026-11-07, Correct Course D3).** Export (a CSV of the current view; JSON as an option, PROC2) from Exposure, Issues and Software, and "Audit report for this answer" (the Story 6.5 PDF answer report), are stored as evidence. The file goes to the object store through `blob`, content-addressed. An `exports` row records who, when, the view (`exposure` | `issues` | `software`), the query or filters, the format, the row count, the caveats and the file digest; the same transaction appends a ledger entry with that digest. Stored exports are insert-only (no update or delete endpoint, no UPDATE or DELETE grant) and follow the evidence-pack retention (ARCH30: default and minimum 24 months, archive path, never deleted by hand). `GET /api/v1/exports` lists them newest first for Reports → Exports. Auditors can export (a read action); their exports are stored and attributed like anyone else's. Owner: a new `exports` capability (recommended — O1). Not decided: whether stored export files are also cosign-signed (O2).
- **Artifact signature verification (FR32, added 2026-11-07, Correct Course D10).** Runs only in the control plane (NFR12). After discovery, and again when the trust policy changes, `inventory` runs the pinned cosign CLI through `tools` (`cosign verify` with a configured public key, or with a keyless identity — certificate OIDC issuer and subject) against signatures read from the same connected registry with that connection's read-only credentials (per-invocation env, never argv). Trust is admin-configured (Settings → Policy and Helm values; PROC2 default: none, so nothing is verified and the UI says so) and each trust-policy version is appended to the ledger. Each result (state, signer, trust-policy version, cosign version, check time) is appended to the ledger and returned by `GET /api/v1/artifacts/{id}`. Air-gapped: key-based verification makes no network call; keyless verification uses an offline Sigstore trusted root and the signature's own bundle, with no call to public Fulcio, Rekor or the Sigstore TUF repository. Registry reads are admin-configured endpoints owned by `inventory`. Open before Story 4.10 (an amendment approved by the user): the result states and their names, per-registry or fleet-wide trust, the signature formats read (cosign signatures, OCI referrers and attestations), how the trusted root is delivered and refreshed (offline bundle, admin-supplied file, or an online refresh in connected mode as a built-in public endpoint owned by `signing`), and whether artifacts from package feeds are in scope (O6–O10).
- **End-of-life data (FR33, added 2026-11-07, Correct Course D10).** One more enrichment source, owned by `enrichment`: an attributed end-of-life dataset, fetched on the enrichment schedule in connected mode (a built-in public endpoint with an offline-bundle equivalent, off in air-gapped mode), validated, stored as a versioned snapshot (source, version or date, retrieved_at) and appended to the ledger (ARCH21). A new snapshot is re-joined to the packages of stored SBOMs through the package index without re-matching SBOMs, like the KEV/EPSS re-join. Each package gets an end-of-life date and a status (past end of life, supported or unknown; never "supported" by default), with source and retrieval time, served per package by `GET /api/v1/artifacts/{id}`; the source's age is in `provenance.sources`. Air-gapped: the dataset is one more component of the signed offline bundle (Story 4.5 format, Story 4.6 import). Open before Story 4.9 (an amendment approved by the user): the source (neither the PRD nor this document names one) and its licence, its coverage (package ecosystems; runtimes and OS releases), the exact matching rule and the staleness threshold (O11–O15). End-of-life status creates no finding and does not count toward Needs attention (O13, answered 2026-11-07: in v1, signature and end-of-life results are shown only).

**Deferred (post-v1, with rationale):**

- HA / multi-instance control plane — NFR10 defers it; durable evidence survives CP loss.
- **GUAC-as-a-service** — revisit only if graph needs outgrow AGE; avoided now for install/footprint/flux reasons.
- MCP query server; build provenance and attestation captured at build — explicit roadmap. (CI scan submission moved into v1 as FR31 on 2026-11-05; scanning stays on the server.)

### Data Architecture

PostgreSQL 18 (with AGE 1.8; bundled image `apache/age:release_PG18_1.8.0`, pinned by digest) is the single source of truth — relational tables for inventory/findings/triage, an AGE graph for traversal queries, and an append-only hash-chained ledger for evidence. SeaweedFS holds SBOM blobs and compacted historical snapshots (enabling the Retroactive Exposure Replay north-star). Logical separation by schema; R9 (storage contention) and R1 (Cypher latency at scale anchor) carry forward as validated SLOs.

#### Evidence history (amended 2026-11-05)

- Each evidence-bearing table has a **current table** (live rows only) and a **history table** (every closed version, with `valid_from` and `valid_to`); only the trigger writes history, and each version closes at the exact moment the next version starts, so versions cannot overlap by design (PostgreSQL `WITHOUT OVERLAPS` is not used: on month-partitioned tables it checks only inside one partition). A test changes rows many times across a month boundary and checks with a query that no versions overlap.
- A **database trigger** copies the old version to the history table on each update or delete, so application code cannot skip it.
- History tables are **insert-only**: the application role has no UPDATE or DELETE grant. They are partitioned by month on `valid_to` (the close time), so a closed version always goes into the current month and the retention mechanism below applies to them. The ledger is partitioned by entry time.
- **Version only on content change.** A row that is checked but not changed writes no history version. A re-evaluation writes one run entry ("fleet evaluated against Grype DB vX") instead of re-versioning unaffected findings.
- Each change appends a ledger entry with the digest of the new version; the hash chain and signed checkpoints therefore cover the history. Events that are themselves the fact (for example a triage decision) keep their full content in the ledger entry. Large content (SBOMs, scan output) lives in the object store, content-addressed, never overwritten inside retention.
- A **coverage test** lists every table in every application schema; each must have a history table or an explicit "not evidence" marker.
- Ledger entries and history rows never contain credentials or secrets; a test checks this for every connection type.
- Disk: the health endpoint and metrics report ledger and history size and database volume headroom (bundled database: the size of its PersistentVolumeClaim, read with get access to that one PVC only, minus `pg_database_size`; `ponytail:` this ignores WAL and file-system overhead — upgrade path: a small sidecar in the database pod that reports real free space), with a warning threshold (default 80 % used). For external Postgres there is no default budget: with none set, only size is reported, with "headroom unknown" and no warning.
- Past-time questions (FR23, Story 9.1) read the history tables, and verified archive segments for archived windows. The AGE graph shows current state only; a time-travel graph stays on the roadmap.

#### Retention — signed checkpoints, then archive (ARCH30, decided 2026-11-04)

1. Ledger and history tables are partitioned by month from their first migration: the ledger by entry time, history tables by `valid_to`. "Wholly older than retention" means that every row in the partition is older than the retention limit by that column.
2. At a configurable interval (default daily), a checkpoint entry records the chain head hash, entry count and covered time range, signed in the configured signing mode. Signed checkpoints also detect a full-chain recompute by a database superuser.
3. When a whole monthly partition is older than the retention period (default and minimum 24 months) and covered by a signed checkpoint, the maintenance CronJob (login `armoury_owner`; see Data boundary) exports it to the object store as a compressed archive segment (digest referenced by a ledger entry), verifies the segment against the checkpoint, and only then drops the partition. The application role keeps no DELETE grant.
4. Chain verification starts from the oldest hot checkpoint; archive segments verify independently against their checkpoint.
5. Point-in-time queries and packs for archived windows read verified archive segments.
6. Archive segments are kept forever by default; an admin can enable a purge after a further configurable period, recorded as a ledger entry, never silent (PROC2, NFR11).
7. All ledger appends (control plane and maintenance CronJob) go through one append function that serializes them with a PostgreSQL advisory lock, so the hash chain stays in order.
8. **Optional Rekor anchoring (ARCH37, decided 2026-11-05).** `rekor.anchoring.mode`: `disabled` (default), `external` or `bundled` (`rekor-tiles`, POSIX backend, own volume, log key in a Secret created once; no witness required, an optional witness policy is a value). Chart comments recommend `external`, because only a log outside the administrator's control can show a full rebuild. After each signed checkpoint, `signing` submits only the checkpoint digest, its signature and the public key as a `hashedrekord` entry (through `tools`, cosign CLI) and appends the inclusion proof to the ledger; a failure leaves the anchor pending and never blocks the ledger. The public key links the entries of one installation. Air-gapped mode refuses the public Rekor. **Known limit:** Rekor v2 returns no signed timestamp, so a full rebuild that is anchored again is found only by comparing with an earlier receipt (evidence packs carry the latest one) or by monitoring the log for two checkpoints of one key that cover the same time range. Upgrade path: an RFC 3161 timestamp authority.

### Authentication & Security

OIDC (`openidconnect` crate) declaratively configured; bootstrap admin for first sign-in / IdP outage. Cookie-session SPA auth. RBAC middleware for the three roles. Connection credentials encrypted at rest. All release artifacts cosign-signed and SLSA-attested.

### API & Communication Patterns

One OpenAPI-described REST spine; UI, future MCP, and metrics are consumers. Agent↔CP over a separate mTLS gRPC/HTTPS channel (agent-initiated, outbound, streaming deltas with stateless re-derive). Standardized typed error envelope; provenance/coverage metadata accompanies every answer-bearing response (honest-degradation contract, NFR8).

**Long operations — polling, no SSE in v1 (amended 2026-11-05).** Work that can take longer than one request (blast-radius queries, pack generation, CI scans) uses one pattern:

- `POST /api/v1/<operations>` creates the operation and returns it at once with `id`, `status` (`running` / `completed` / `failed`), `progress` (done and total counts), partial results so far, `provenance`, and a cursor for result pages.
- `GET /api/v1/<operations>/{id}` returns the same shape. If the first response is already `completed`, the client sends no second request.
- The SPA polls with svelte-query `refetchInterval`: about 1 s for long operations, about 10 s for the Home summary (posture API, including the Needs-attention count behind the Issues badge) while backlog exists, and only while work is queued or running.
- `ponytail:` partial blast-radius results are held in control-plane memory for about 10 minutes (single instance, NFR10); a restart loses them and the user runs the query again. Upgrade path: store them in PostgreSQL if more than one control plane runs. SSE stays a later option if polling delay is measured as too slow.
- An Exposure query still running after 2 s renders its partial results with a scope line (EXPERIENCE → Long-running operations); the ~1 s poll above serves it.

**Issues and review (amended 2026-11-07, Correct Course D1, D6–D8).** A finding stays one match on one artifact (a "place"). The Issues surface lists **finding groups** (UI label "issue"): a read model over findings, keyed by vulnerability ID and package purl@version, or by licence, finding kind (`license_violation` | `license_warning`) and package purl@version. Per group the list response gives `group` (`licence` | `critical` | `high` | `medium` | `low` | `negligible` | `unrated`; `negligible` is Grype's Negligible and `unrated` is Grype's Unknown or no severity, UI "Not rated yet"; both sort after `low` and, like `licence`, the UI hides them at 0), `kev`, the place count, the issue-wide `triage_status` (the status of the latest `all_places` decision on the group; `untriaged` when there is none), `mixed` with the number of places whose own `artifact` decision differs from the issue-wide status (the UI shows "Mixed · N of M" when it is above 0; M is the place count; when N equals M it shows "Mixed" with no count and the accessible name "All M places have their own status"), and `needs_attention`; the page carries counts per group and per triage status (a group matches a status filter when any place has that status; counts are groups, not places), the Needs-attention count, and the total for the pager. The list also takes `needs_attention=true`, which returns only groups with `needs_attention`, in the same order; the Issues "Needs attention" filter and Home's "Review all N" use it. Ordering is server-side and deterministic (`ranking`, FR13). **Needs attention:** a vulnerability group with any place `untriaged` AND (`kev` OR severity critical); a `license_violation` group with any place `untriaged`; `license_warning` groups never (D8). It is computed only on the server, so the Issues badge, Home and the Issues summary show the same number. **Decisions** carry scope `all_places` (default: this vulnerability or licence in this package version on every artifact, including artifacts found later) or `artifact`; a per-artifact decision overrides `all_places`, and a later `all_places` decision leaves per-artifact decisions in place (Story 5.8). A place's effective status is its own `artifact` decision if present, else the issue-wide status; status filters, Needs attention and VEX (one statement per product) use effective statuses. `justification` is required for `not_affected`, `mitigated` and `accepted` and optional for `fix_planned` (D7). `mixed` is derived, never stored. **Issue sentence (decided 2026-11-07):** the issue detail shows the first sentence of the advisory description in the vulnerability record (the record's description field), unchanged, with its source and retrieval time (FR12). Armoury never rewrites or generates it; when the record has no description, no sentence is shown.

### Frontend Architecture

SvelteKit static SPA · shadcn-svelte · Tailwind v4 · Svelte Flow (Exposure map) · TanStack Svelte Query (server state) · command palette (shadcn `Command` + `Dialog`). Every graph view has a table equivalent (accessibility + graph-lib de-risk). UI source of truth: `ux-designs/ux-Armoury-2026-11-06/` DESIGN.md (tokens, components) and EXPERIENCE.md (behaviour).

- **Shell:** black labelled sidebar (shadcn `Sidebar`: Home · Software · Issues · Exposure · Reports, then Settings · Help; the ⌘K search field; the user menu) and three-column master-detail on every surface (sidebar · grouped list column · tabbed detail column); Exposure has a full-width header over the list and the map. Below 1280px the sidebar becomes an icon rail; below 1024px list and detail stack with a Back link, at the same URL. One density only.
- **Themes:** Light (default) and Dark, two value maps over the same semantic roles, applied as shadcn CSS variables (plus `--paper` and the `--dq*` roles) by a root class; switching is instant and persisted in `user_preferences`. No other themes. The printed report never follows the theme.
- **Fonts:** IBM Plex Sans (variable, plus Bold Italic for the wordmark) and IBM Plex Mono, self-hosted in the SPA bundle (no network at view time, NFR4); the same files feed Typst.
- **Review:** the review panel lives in the Issues detail column (Review tab); no slide-over drawer. The ⌘K dialog is the only modal. Status changes happen only in the panel.
- **Exposure traversal (D4):** click or `Enter` on any node moves the map to it (ego view) using the `graph` neighbours API; the trail, question, answer, Export, "Audit report for this answer" and the URL (`&from=` the previous step) follow the centre; Back, `Backspace` or the browser Back returns a step; ⌘K starts a new trail.
- **Keyboard:** single-key shortcuts (`J`, `K`, `/`, `x`, `?`, `g` + letter, `Backspace` on the map) work only outside text fields and can be turned off per user; `⌘K` and `⌘↵` always work.
- **Counts are server-derived:** Needs attention, group and status counts, and "Mixed · N of M" come from the API, never from summing a page in the SPA.
- **Accessibility:** WCAG 2.2 AA in both themes; reflow at 400% zoom through the responsive rule above; all strings externalised (British English); UI labels mapped from API enums in one place.

### Infrastructure & Deployment

Single Helm umbrella chart; bundled Postgres-AGE + SeaweedFS by default, external opt-in. Air-gap instance mode. SLSA-attested, cosign-signed releases. Single-instance control plane (NFR10); read-only Rust agents via kube-rs.

### Substrate Integration (Rust ↔ Go OSS tools)

Syft, Grype, Grant and cosign are Go with no Rust bindings, so the control plane runs them as **pinned CLI subprocesses** bundled in its image (each tool enters the image, checksum-verified, in the story that first uses it: Syft 2.3, Grype 2.4, cosign 4.5, Grant 7.1), through one `tools` module (timeouts, JSON decoding, stderr capture, version capture). Tool versions are recorded on every finding and evidence entry, which strengthens FR8 provenance.

- **Syft:** `syft <image-ref> -o syft-json` (CycloneDX/SPDX derived for packs). Registry credentials go in via per-invocation env, never argv. **Package archives** (npm tarball, wheel/sdist, `.crate`, Go module zip): the connector downloads the archive, checks its checksum against the feed, unpacks it into a temporary folder (rejecting path traversal and links outside the folder) and runs `syft dir:<path>`; JAR files use `syft file:<path>`. Known limit: an archive without a lock file gives the package itself, not exact dependency versions — shown as a caveat on package artifacts.
- **Registry access:** the `oci-client` crate (0.18.0). Repository discovery modes (PROC2): **catalog** (default for generic registries), **provider API** for ECR, Artifact Registry and Docker Hub (same read-only credentials), and **repository list** (names or a prefix). "Test connection" states when the catalog endpoint is missing.
- **Grype:** `grype sbom:<file> -o json` with `GRYPE_DB_AUTO_UPDATE=false`; `feeds` owns the DB directory and keeps each activated DB in its own directory (`<feeds-dir>/grype/<db-version>/`, at least current and previous); a downloaded DB is validated against the checksum in the Grype DB listing and its schema version; offline bundles apply via `grype db import` (R8: validate first, fail closed). **Feed delta (amended 2026-11-05):** `reeval` runs `grype db diff -o json <previous-db> <current-db>` (Grype pinned, ≥ v0.121.1); the changed packages select the stored SBOMs that contain them through the package index, and `scan` re-matches that subset. Armoury never reads the Grype SQLite schema itself. Fallback, chosen by the Story 4.8 measurement: a full re-check of every stored SBOM.
- **Grant:** `grant check` against stored SBOMs, JSON output; the wider Grant surface (images, filesystems) stays reachable (FR26).
- **cosign:** `cosign sign-blob --bundle` in the configured signing mode (`key` by default; see Signing). Verification may use the `sigstore` crate (verification-focused, pre-1.0) or the cosign CLI. `cosign verify` also checks customer artifact signatures against admin-configured trust (FR32, Story 4.10), with registry credentials in per-invocation env.
- **Typst** (PDF renderer, 0.15.1): a pinned static binary run through `tools`, with no network access, for the Exposure answer report (Story 6.5; shown in the UI as "Audit report for this answer" and stored with the exports) and evidence packs (audit reports, Story 9.3). Templates live in the module that owns the report; the bundled IBM Plex Sans and IBM Plex Mono fonts (the files the SPA self-hosts) are passed to Typst, and templates use DESIGN.md's `print-*` palette, never the app theme.

**Upside:** results are byte-for-byte what users get running the same tools themselves (the "embrace the OSS stack" position), a tool crash can't take down the control plane, and tool upgrades don't need a recompile. **Cost:** per-SBOM process spawn plus Grype DB open — see R11.

### Decision Impact Analysis

**Implementation sequence** (indicative; the epic order in `epics.md` is authoritative): (1) repo + scaffold (step-3 commands) → (2) Postgres-AGE schema + evidence ledger → (3) registry connector + Syft SBOM generation + SeaweedFS → (4) Grype scan + River pipeline → (5) feed ingestion + delta re-eval engine → (6) enrichment + ranking → (7) blast-radius/posture API + SPA → (8) agent (transport + re-derive) → (9) triage/VEX → (10) evidence packs + signing → (11) license (Grant) → (12) Prometheus + air-gap bundle path → (13) optional CI scan submission (FR31; after the scan, enrichment, triage, blast-radius, license and release slices — Epics 2, 4, 5, 6, 7 and 10).

**Cross-component dependencies:** AGE graph schema underpins blast-radius queries and moving the Exposure map (which absorbed the former Graph explorer); the OpenAPI spine gates UI + future MCP; the hash-chained ledger underlies both triage history and signed packs; the air-gap axis touches feeds, enrichment, and signing simultaneously.

## Implementation Patterns & Consistency Rules

**Primary organizing principle: Locality of Behaviour** — everything that changes together lives together. Organize by capability/domain, never by technical layer. Shallow abstractions (max 3 layers), explicit dependencies, rule-of-three before extraction. (Mirrors the project `AGENTS.md`; there is no `CLAUDE.md`.)

### Critical Conflict Points Identified

Nine areas where agents could diverge: DB naming, API naming, JSON casing, error/answer envelopes, Rust layout, Svelte file naming, IDs/timestamps, the locked domain vocabulary (code, API, exports) versus the plain UI labels, and honest-degradation metadata.

### Naming Patterns

**Database (Postgres + AGE):**

- Tables: `snake_case`, **plural** (`artifacts`, `findings`, `triage_decisions`). AGE graph labels: `PascalCase` singular vertices (`Artifact`, `Package`, `Cve`, `Workload`), `UPPER_SNAKE` edges (`DEPENDS_ON`, `AFFECTS`, `RUNS_IN`).
- Columns: `snake_case`; PKs `id`; FKs `<entity>_id`; timestamps `created_at`/`updated_at`; indexes `idx_<table>_<cols>`.

**API:**

- REST, versioned: `/api/v1/<plural-noun>`; path params `{id}`; query params `snake_case`. Resource nesting max one level.
- Headers: `X-Armoury-*` for custom.
- Roles: every operation in `openapi.yaml` declares `x-armoury-role: admin | analyst | auditor` (the minimum role). The RBAC middleware reads it; a spec test fails on an operation without it, and a route test calls each route with each role (403 below the role, no 403 at or above it). A route that a setting can open to a lower role also declares `x-armoury-role-setting` (for example `rbac.auditorCanGeneratePacks` on pack generation). A CI token is not a role: routes that CI may call also declare `x-armoury-ci-token: true`. CI tokens use `Authorization: Bearer <token>` (a session cookie never counts as a CI token); the middleware accepts a CI token only on marked routes and returns 403 on every other route.

**Rust code:** standard Rust naming (`snake_case` items, `PascalCase` types); `rustfmt` + `clippy -D warnings`. **Module-by-capability** under `src/` — each capability module holds its HTTP handlers, domain logic, SQL, and tests _together_ (LoB), never split into `models/`/`services/`/`repositories/`. One crate per binary plus the shared `agent-proto`; **no crate-per-capability split**. **Traits only at the third occurrence or when a real second implementation exists** — never speculative, never single-impl, no `dyn` for a single implementor. No `Manager`/`Factory`/`Provider`/`Handler`/`Adapter` layers. Errors: one `thiserror` enum per capability, propagated with `?`; `anyhow` only in `main`. No `unwrap`/`expect` outside tests and startup wiring; no `unsafe`.

**Svelte/TS:** component files `kebab-case.svelte`, components used `PascalCase`; routes lowercase (SvelteKit `+page.svelte`); stores/composables `use-x.ts` / `camelCase`; types `PascalCase` (generated client is source of truth — never hand-edit).

### Format Patterns

**Long operations:** blast-radius queries, pack generation and CI scans return the long-operation shape (`id`, `status`, `progress`, partial results, `provenance`, cursor) — see API & Communication Patterns.

**JSON wire casing:** `snake_case` on the wire (aligns with Postgres columns, friendly to the future MCP server and `curl`/scripting auditors). The TS client maps via codegen, so the SPA still reads idiomatic types.

**Success responses:** return the resource directly (no `{data:...}` wrapper). **Lists** use `{ "items": [...], "page": {...} }` with cursor pagination (no offset at NFR3 scale). `page` carries `total` (and group counts for grouped lists), so the SPA shows "1–25 of 312 · page 1 of 13" with previous and next only; 25 per page; no jump-to-page, no infinite scroll.

**Error envelope (uniform):**

```json
{ "error": { "code": "snake_case_code", "message": "human readable", "details": {} } }
```

HTTP status carries semantics (400/401/403/404/409/422/500); `code` is the stable machine key.

**Honest-degradation metadata (Armoury-specific, mandatory).** Every answer-bearing response (posture, blast-radius, artifact, packs) carries a `provenance` block — `sources[]` (name, version, retrieved_at), `coverage` (in_scope / scanned / unmatched counts), `freshness` (per-feed age) — and, when partial, a `caveats[]` array. This is the API-side contract behind NFR8 / the honest-provenance UX. No answer ships without it. A blast-radius query for a vulnerability ID that the vulnerability data used for matching (the active Grype DB) has no record for — even when the CVE List or another enrichment feed already lists it — returns the Story 6.2 error (a `code` distinct from "not a valid identifier") with the active feed versions and their age in `details`; the SPA shows it as the unknown-vulnerability state ("Armoury has no data for <ID> yet"), never as a zero. Only a known vulnerability — one with a record in the active Grype DB — gets the coverage-scoped zero. "Check again" on that state re-runs the query against the latest data; it is not a rescan.

**IDs & time:** external IDs **UUIDv7** (time-sortable — suits the append-only ledger and agent-side generation); timestamps **RFC 3339 UTC** strings, always. Durations in seconds (integer).

**Domain vocabulary is locked in code, API and exports, not free text.** The domain terms (`Artifact`, `Fleet`, `Finding`, `Posture`, `Evidence`, `Evidence pack`, `Control plane`, `Cluster agent`) and the triage status set (`not_affected` / `mitigated` / `accepted` / `fix_planned`, plus derived `untriaged`) are **typed enums** in Rust (`serde` `snake_case`), the OpenAPI schema, and TS — never stringly-typed, never synonymized. VEX and machine-readable exports keep these technical terms. **UI copy uses the plain labels** of EXPERIENCE.md's glossary (ux-Armoury-2026-11-06) — Home, Software, Issues, Exposure, Reports, Audit report; Not reviewed yet / Not impacted / Fix planned / Mitigated / Risk accepted; Actively exploited (KEV); Deployed / Not deployed; Packages (SBOM) — with the technical term small beside the label. Labels map from the enums in one place in the externalised strings; enums are never renamed to match a label. `mixed` is a derived display state, never stored.

### Structure Patterns (Locality of Behaviour)

**Primary rule:** everything that changes together lives together. Organize by **capability/domain, not technical layer.**

**Rust (control-plane & agent):**

```
control-plane/
  src/main.rs             # entrypoint — wiring only
  src/
    inventory/            # registry connect, SBOM gen, reconciliation + its storage + tests
    scan/                 # grype orchestration + pipeline + tests
    reeval/               # feed-delta engine + tests
    enrichment/           # KEV/EPSS/OSV/CNA aggregation + tests
    evidence/             # append-only ledger + hash-chain + tests
    packs/                # CRA pack generation + signing + tests
    blastradius/          # AGE queries + provenance assembly + tests
    ...
```

- **Max 3 layers:** Entrypoint (HTTP handler / `cmd`) → Coordinator (capability orchestrator) → Implementation. A 4th layer is the signal to stop.
- **Explicit dependencies** — DB handle, object-store client, config passed in via constructors; **no globals, no singletons, no magic** (no `static`/`OnceLock`/`lazy_static` state). `main.rs` is the only place wiring happens.
- **No `utils/`/`helpers/`/`common/`.** A shared thing earns a _named_ home by capability (rule of three before extraction).
- Files **100–400 lines**, split at 500+; each file opens with a one-line docstring stating its purpose.

**Svelte SPA:** locality via SvelteKit routes — surface-specific components, loaders, and stores live _with their route_ (`routes/issues/`, `routes/exposure/`); only genuinely shared primitives sit in `lib/components/ui` (shadcn-svelte), and the Armoury brand-layer components every surface uses (shell, list row, severity and exploited markers, status chip, coverage-gap row, freshness strip, inline error, code block, data-quality value and meter) earn the named home `lib/design/`. No global `components/` dumping ground; co-locate `*.test.ts`.

**Tests:** co-located everywhere (Rust in-file `#[cfg(test)] mod tests`, cross-module in `tests/`; Svelte `*.test.ts`); Playwright e2e in `web/e2e/`. Run frequently; never deleted to pass.

### Process Patterns

- **Config:** env / Helm values only (NFR6); twelve-factor; secrets via k8s Secret refs.
- **Composition over inheritance** — register implementations in collections (e.g. connector / pack-definition registries), don't extend base types.
- **SPA state/errors:** TanStack Query owns server-state; skeletons mirror layout; render the typed error envelope's `message`; never a bare spinner. A failed save or start (review, export, generate audit report, Check again, settings) shows an inline error in the panel where it happened, with Try again; nothing advances and entered values stay; no toasts.
- **Logging:** structured `tracing` JSON (`tracing-subscriber`), levels `debug/info/warn/error`; never log credentials or full SBOM payloads.
- **Migrations:** versioned forward-only SQL (`sqlx migrate`); AGE graph schema versioned alongside.

### Enforcement — All agents MUST

- Treat the **OpenAPI spec as the contract**; regenerate clients, never hand-edit generated code.
- Attach **provenance metadata** to every answer-bearing endpoint.
- Use the **locked enums** in code, API and exports, and EXPERIENCE.md's plain labels in UI copy; no invented status or entity synonyms in either.
- Keep evidence writes **append-only** (superseding entries, never mutate/delete).
- Honor the **outbound boundary**: a new outbound call is either an admin-configured endpoint owned by one module, or a built-in public endpoint in `feeds`, `enrichment` or `signing` that has an offline-bundle equivalent and is off in air-gapped mode.
- Follow **Locality of Behaviour**: by-capability layout, max 3 layers, no speculative abstraction, no `utils/`/`helpers/`.

### Anti-patterns

Wrapping every response in `{data}`; offset pagination on fleet tables; free-string triage statuses; answers without coverage/provenance; mutable evidence rows; hand-edited generated client code; secrets in logs; by-layer folders (`models/`/`services/`/`repositories/`); `utils/`/`helpers/`/`common/`; single-implementation interfaces; `Manager`/`Factory`/`Provider` layers; enum values shown as UI labels or UI labels used as enum values; counts summed in the SPA from a page of rows.

## Project Structure & Boundaries

### Complete Project Directory Structure

```
armoury/
├── Cargo.toml                    # workspace: control-plane, agent, agent-proto
├── mise.toml                     # pinned tool versions (Rust, Node, Helm, buildx, Skaffold, …)
├── mise-tasks/                   # mise file tasks: check, e2e, gen/api, image, … (`mise run <task>`)
├── skaffold.yaml                 # dev loop: build both images, Helm deploy to the dev cluster (PROC3)
├── AGENTS.md                     # LoB rules, layout, PROC3 (no CLAUDE.md)
├── README.md
├── .github/workflows/
│   ├── ci.yml                    # mise run check (Rust fmt/clippy/nextest, web, API drift)
│   ├── build.yml                 # build images + package chart; push to ghcr.io by digest on main
│   ├── release.yml               # reuse built digests; SLSA provenance, cosign-sign images/charts and the CLI (NFR7)
│   └── bundles.yml               # scheduled (daily): build, KMS-sign and attest Armoury-published feed bundles (Story 10.2)
├── action/                       # GitHub Action for `armoury scan` (FR31), released with the CLI version tags
│
├── api/
│   └── openapi.yaml              # THE REST contract — source of truth (UI + future MCP)
├── proto/
│   └── agent/v1/agent.proto      # agent↔control-plane gRPC contract (FR3/FR4)
├── agent-proto/                  # tonic/prost codegen from proto/ (build.rs), shared by CP + agent
│
├── control-plane/
│   ├── Cargo.toml
│   ├── Dockerfile                # armoury + SPA build; pinned syft/grype/grant/cosign/typst added per story
│   ├── src/main.rs               # wiring ONLY — the one place deps are constructed
│   ├── migrations/               # versioned forward-only SQL + AGE graph schema
│   └── src/                      # module-by-capability; each owns handler+logic+queries+tests
│   │   ├── httpapi/              # generated server stubs + router mount (entrypoint glue only)
│   │   ├── inventory/            # FR1–FR5, FR29, FR32  registry/feed connect, Syft SBOM, reconcile, coverage, signature checks
│   │   ├── ciscan/               # FR31           CI scan submission, CI tokens, CI policy verdict
│   │   ├── feeds/                # FR7, FR10      feed ingestion + signed offline bundles (R8)
│   │   ├── scan/                 # FR6, FR9       uniform Grype matching of stored SBOMs
│   │   ├── reeval/               # FR7, FR8       feed-change re-evaluation (NFR5)
│   │   ├── enrichment/           # FR11, FR12, FR33  KEV/EPSS/OSV/CNA + end-of-life aggregation + attribution
│   │   ├── ranking/              # FR13           deterministic grouping + order: Licences, Critical…Low, Negligible, unrated; KEV first in a group, then raw EPSS, then a stable tie-break
│   │   ├── triage/               # FR14, FR15     decisions + VEX ingest/emit
│   │   ├── license/              # FR26–FR28      Grant evaluation + policy (parallel to scan)
│   │   ├── posture/              # FR16, FR30     fleet posture (Home summary, Needs attention, finding groups) + data-quality score
│   │   ├── blastradius/          # FR17, FR19     AGE Cypher traversal + provenance assembly
│   │   ├── exports/              # FR19           stored exports: file → blob, record + ledger entry, Reports → Exports list (recommended, O1)
│   │   ├── graph/                # FR17, FR18     neighbour queries for moving the Exposure map (ego view, roll-ups)
│   │   ├── evidence/             # FR23, NFR11    append-only hash-chained ledger
│   │   ├── packs/                # FR21–FR24      CRA pack generation (extensible)
│   │   ├── signing/              # FR25, NFR7     cosign operator key (default) / keyless (opt-in); created in Story 4.5
│   │   ├── metrics/              # FR20           Prometheus exposition
│   │   ├── auth/                 # NFR6           OIDC, bootstrap admin, sessions, RBAC
│   │   ├── agentgw/              # FR3, FR4       agent gRPC gateway (mTLS, reconcile re-derive)
│   │   ├── tools/                # pinned Syft/Grype/Grant/cosign/Typst CLI runner (callers → earned)
│   │   ├── postgres/             # sqlx pool + migration runner + AGE bootstrap (constructed in main)
│   │   └── blob/                 # S3 client — SeaweedFS default, any S3 (constructed in main)
│
├── agent/
│   ├── Cargo.toml
│   ├── Dockerfile                # armoury-agent only (no scanner tools), distroless, non-root
│   ├── src/main.rs
│   └── src/
│       ├── watch/                # FR3   kube-runtime watchers/reflectors (watch/list only, NFR9)
│       └── report/               # FR4   outbound mTLS tonic gRPC client + stateless re-derive (R3)
│
├── web/
│   ├── package.json
│   ├── svelte.config.js          # adapter-static, SSR off
│   ├── components.json           # shadcn-svelte
│   ├── e2e/                      # Playwright
│   └── src/
│       ├── lib/
│       │   ├── api/              # generated TS client (never hand-edited)
│       │   ├── components/ui/    # shadcn-svelte primitives (genuinely shared only)
│       │   ├── command/          # ⌘K palette
│       │   ├── design/           # Armoury brand-layer components shared by every surface (DESIGN.md Components)
│       │   └── theme/            # Light (default) / Dark token maps → shadcn CSS variables (+ --paper, --dq*); self-hosted IBM Plex Sans + Mono
│       └── routes/               # locality: each surface owns its components/loaders/tests
│           ├── +page.svelte      # Home (/) + software/ issues/ exposure/ reports/ settings/[panel]/ help/ (Help content open, EXPERIENCE Open item 24)
│
└── charts/
    └── armoury/                  # umbrella chart
        ├── Chart.yaml            # deps: postgres-age, seaweedfs (bundled; external opt-in)
        ├── values.yaml           # air-gap flag, OIDC, retention, connections
        └── templates/            # control-plane + agent (agent is install-per-cluster)
```

### Architectural Boundaries

- **API boundary:** `api/openapi.yaml` is the only contract between SPA/MCP and the control plane. Handlers live _in their capability module_; `httpapi` module holds only generated stubs + router assembly. Generated code is never hand-edited.
- **Agent boundary:** `proto/agent/v1` is the only contract between agent and control plane. Agent reaches the control plane _outbound_ (mTLS); never the reverse. The agent crate depends on nothing in the `control-plane` crate.
- **Capability boundary:** modules communicate through plain `pub` functions and types; traits only at rule-of-three; wired in `main.rs`. No cross-capability reach into another's storage — each owns its own queries.
- **Data boundary:** one Postgres (separate schemas by capability, for example inventory, evidence and graph); the ledger and history tables are append-only at the DB layer (no UPDATE/DELETE grants for the application role, NFR11). Two database logins: `armoury_owner` owns every schema and table and is used only by the migration Job (`armoury migrate`, a Helm post-install and pre-upgrade hook that also creates monthly partitions 3 months ahead; the control plane reports not ready until the schema version is at least its expected version; the documented install does not use `--wait` or `--atomic`) and the maintenance CronJob (daily: keeps partitions 3 months ahead, warns on the health endpoint and in metrics when less than 1 month remains; later archive and drop, ARCH30); `armoury_app` owns nothing and is the only login of the control-plane pod, with INSERT but no UPDATE or DELETE on ledger and history tables. The passwords are in two Secrets, and the control-plane pod cannot read the owner Secret. The bundled database gets both logins from the chart; an external database must supply both, the owner login must be able to create schemas, and a database administrator installs the AGE extension once. Only the maintenance CronJob (as `armoury_owner`) exports and drops archived partitions (Retention). Reason: a table owner always has full rights in PostgreSQL, so the application must not own the tables. SBOM blobs only via the `blob` module.
- **Scanning boundary (NFR12):** Syft, Grype, Grant, policy evaluation and signature verification (cosign, FR32) run only in the control plane through `tools`. The agent reports running digests only; the CI scan path submits a digest or the artifact bytes only.
- **Outbound and air-gap boundary (amended 2026-11-05):** two endpoint classes.
  - **Admin-configured endpoints** — registries, package feeds, the OIDC issuer, a private Fulcio, a configured Rekor (ARCH37) and proxies. The module that owns the connection (`inventory`, `auth`, `signing`) calls only its configured URL. A default public URL that the admin accepts when saving a connection (for example the public npm registry) is stored in the connection record and counts as admin-configured.
  - **Built-in public endpoints** — Grype DB, KEV, EPSS, OSV, CVE List, the end-of-life data source (FR33), public Fulcio and Rekor. Only the `feeds`, `enrichment` and `signing` modules call them. Air-gapped mode turns this class off completely.
  - The Story 10.3 check enforces both classes.

### Requirements → Structure Mapping

| FR group                            | Primary modules                             |
| ----------------------------------- | ------------------------------------------- |
| Fleet Inventory (FR1–5,29,32)       | `inventory`, `agentgw`, `agent/watch`       |
| Scanning & Freshness (FR6–10)       | `scan`, `reeval`, `feeds`                   |
| Enrichment & Prioritization (FR11–15,33) | `enrichment`, `ranking`, `triage`      |
| Blast-Radius & Posture (FR16–20,30) | `posture`, `blastradius`, `graph`, `exports`, `metrics` |
| Compliance Evidence (FR21–25)       | `evidence`, `packs`, `signing`              |
| License (FR26–28)                   | `license`                                   |
| CI scan (FR31)                      | `ciscan` (with `inventory`, `scan`, `license`) |

**Cross-cutting:** `auth` (NFR6, all surfaces), `evidence` (NFR11, written by triage/scan/feeds), provenance metadata (assembled by `posture`/`blastradius`/`packs`, NFR8).

### Data Flow

**Two evaluators per SBOM.** A `Finding` is either a vulnerability match or a license violation:

```
inventory (SBOM via blob)
   ├─► scan / Grype     ─► vulnerability findings ─► enrichment ─► ranking ─┐
   └─► license / Grant  ─► license findings (vs policy FR27) ───────────────┤
                                                                            ▼
                                                  findings ─► posture / blastradius / artifact
```

- **Grype** matches the package@versions in the stored SBOM against its vuln DB (version-range matching, no image pull). **Grant** evaluates licenses on the same SBOM. License findings skip enrichment (no KEV/EPSS) and have no severity; `ranking` places them in the Licences group, listed first and hidden at 0 (violations and warnings; only untriaged violations need attention). They are triagable with the same decision model (FR14) and embedded in the same surfaces (FR28).
- **Feed update → re-evaluation:** `feeds` ingests the new DB; `reeval` uses the **feed delta to select the bounded subset** of stored SBOMs whose packages are touched by changed CVEs, then **re-matches just that subset by reusing `scan`'s Grype matcher** (delta picks the work set; Grype still matches — faithful and uniform, FR6). No rebuilds, no rescans of images, no whole-fleet rerun (NFR5). Updated findings are re-ranked. On a license-policy change, license findings are recomputed from stored license data without re-running Grant (Story 7.3); Grant runs again only for a new SBOM.
- **Evidence:** every scan, feed version, triage decision, stored export and signature check appends to the `evidence` hash-chained ledger (NFR11).
- **CI scan (FR31):** a pipeline runs `armoury scan` (a subcommand of the `armoury` binary, with no scanner inside). Digest mode (default): the CLI sends the image digest and declared build details; the server pulls the image by digest from the connected registry. Upload mode: the CLI uploads the built image or package archive (never source); the server computes the digest itself. Either way the artifact enters the same inventory → Syft → Grype/Grant pipeline at a higher queue priority, the server applies the versioned fleet CI policy, and the CLI polls (long-operation pattern) and prints the verdict and artifact URL (the piece of software in Software; how CI-only software is grouped there is open, EXPERIENCE Open item 28). Exit codes `0` pass, `1` policy failure, `2` no verdict. An artifact is identified by image digest, or package coordinates plus archive checksum; a known artifact gets a new source record, not a duplicate. A scoped CI token (not a user) authenticates the step.
- **Signing — two distinct roles.** Runtime: `packs` reads the ledger → `signing`/cosign seals the generated pack (FR25; configured signing mode, `key` by default) → SeaweedFS. `signing` is created by Story 4.5 (bundles) and extended by Story 9.4 (packs, checkpoints). Build-time (CI, not runtime): cosign-sign + SLSA-attest Armoury's own images/charts/bundles (NFR7). Verifying customer-artifact signatures is a separate, read-only role (FR32, in v1 since 2026-11-07): `inventory` runs `cosign verify` through `tools` against admin-configured trust; it never signs anything.
- **Exit:** all read surfaces leave via `httpapi` carrying provenance metadata (NFR8); signals leave via `metrics` (Prometheus pull, FR20). The ledger's own integrity is the hash-chain, independent of Sigstore.

## Architecture Validation Results

### Coherence Validation ✅

**Decision compatibility:** Internally consistent — Rust control plane orchestrating the Go OSS tools (Syft/Grype/Grant/cosign) as pinned CLI subprocesses; one Postgres (AGE for graph, relational for state, hash-chained ledger for evidence); SeaweedFS (default) or any S3 for blobs; River (`riverqueue`) for jobs; Svelte SPA over an OpenAPI spine. No version conflicts (AGE supports PG 11–18; all else current). Single-datastore choice directly serves NFR1/NFR4.

**Pattern consistency:** LoB by-capability layout aligns with the FR-group decomposition; OpenAPI-as-contract and the provenance-metadata mandate are enforceable and consistent with NFR8. Locked enums carry the technical terms that the UX glossary (ux-Armoury-2026-11-06) keeps for exports, VEX and docs; UI labels map from them in one place.

**Structure alignment:** Capability modules map 1:1 to FR groups; boundaries (API, agent-proto, the two-class outbound boundary, append-only ledger grants) are concrete and respected by the tree.

### Requirements Coverage Validation

**Functional (33/33 mapped):** Every FR group has owning modules (see Requirements→Structure table). ✅

**Non-functional:** NFR4/6/7/8/9/10/11 fully addressed architecturally. ✅ **NFR2 (sub-minute blast-radius) and NFR5 (1-hour re-eval) are _designed_ but _unvalidated_** — they rest on AGE Cypher latency (R1) and reeval delta-subset throughput (R2), which need a load test at the scale anchor. ⚠️

### Gap Analysis

**Critical gaps (block implementation):** None. Scaffold + inventory + scan + evidence can begin immediately.

**Important gaps (nail before the dependent slice):**

1. **FR30 data-quality scoring model is undefined.** _(Still open — closed by the Story 8.1 amendment.)_ The PRD/UX deliberately left the scoring algorithm (SBOM depth, scan coverage, feed freshness, enrichment coverage, CVE record quality → score+grade) as an architecture/UX decision. Placed in `posture` but the inputs→score function and grade banding need definition before the DQ API fields and the surfaces in ux-Armoury-2026-11-06 (Software detail value and quality meter, audit report detail, printed cover page; not on Home, not in list rows). The UX grade bands are a placeholder until then (EXPERIENCE Open item 11).
2. **Agent enrollment & identity bootstrap.** Transport (mTLS, outbound) is decided, but how the one-line `helm install` agent obtains its mTLS identity + control-plane address/enrollment token isn't specified — and it's on the UJ-1 30-minute critical path.
3. **Performance validation plan** for R1/R2/R11 (NFR2/NFR5) — including measured per-SBOM Grype subprocess cost — an explicit load test at the scale anchor.

**Minor gaps (specify during the relevant slice):**

- FR13 exact ordering (severity groups Critical/High/Medium/Low/Negligible/unrated with a Licences group first; KEV first within each group, then raw EPSS — never shown as a rating — then a stable tie-breaker). _Open — Story 5.1 amendment fixes the tie-breaker._
- ~~FR15 VEX format coverage~~ — **closed 2026-11-04:** OpenVEX and CycloneDX VEX, user picks per export; CSAF deferred until a customer needs it (ARCH29). The **VEX status mapping** (locked statuses → each format's states and justifications, including `accepted` and `fix_planned`; decisions per place give one statement per product, so a "Mixed" issue states each product's own effective status (its per-artifact decision if present, else the All places decision); a `fix_planned` decision without a justification uses the planned fix, for example "Update log4j-core to 2.17.2", as its action statement) stays open — Story 5.6 amendment, approved by the user before implementation.
- ~~FR23 retention enforcement + SBOM compaction~~ — **closed 2026-11-04/05:** see Data Architecture → Evidence history and Retention.
- Air-gapped _enrichment_ bundle format (R8 covers feeds; enrichment sources need the same offline path). _Open — Story 4.5 amendment._ The end-of-life dataset (FR33) rides the same bundle (Story 4.9 extends the manifest); whether the Sigstore trusted root for keyless signature verification (FR32) does too is open (O8).
- FR32 signature verification details (trust configuration, result states, formats, trusted-root delivery, artifact types). _Open — Story 4.10 amendment._
- FR33 end-of-life source, licence, coverage, matching rule and staleness threshold. _Open — Story 4.9 amendment._
- Stored exports: owning module and whether files are signed. _Open — Story 6.5 planning (O1, O2)._

**Process rules** (project workflow, recorded in `epics.md`, not architecture): PROC1 (Agent Readiness after the scaffold), PROC2 (offer options with smart defaults), PROC3 (`mise run dev` runs continuously during every development step).

### Architecture Completeness Checklist

**Requirements Analysis** — [x] context · [x] scale/complexity · [x] constraints · [x] cross-cutting concerns
**Architectural Decisions** — [x] critical decisions w/ versions · [x] stack specified · [x] integration patterns · [x] performance addressed (validation pending)
**Implementation Patterns** — [x] naming · [x] structure · [x] communication · [x] process
**Project Structure** — [x] directory tree · [x] boundaries · [~] integration points mapped (agent enrollment open) · [x] requirements→structure

### Architecture Readiness Assessment

**Overall Status:** **READY WITH MINOR GAPS** — no critical blockers; implementation can start, with FR30 scoring, agent enrollment, and R1/R2 perf validation to be closed before their dependent slices.

**Confidence:** Medium-high.

**Key strengths:** Single-datastore simplicity serving the air-gap/install gates; honest-degradation baked into the API contract; clean FR→capability mapping under LoB; risk register carried from analysis into concrete mitigations.

**Areas for future enhancement:** HA control plane (NFR10 deferral); GUAC-as-service if graph needs outgrow AGE; build provenance capture; MCP query server; **non-Kubernetes runtime agents** (Docker Swarm, HashiCorp Nomad, AWS ECS, Vercel, etc.) — same report-only contract (`proto/agent/v1`), different runtime watcher, so the control plane stays runtime-agnostic.

### Implementation Handoff

**AI agent guidelines:** Follow the documented decisions exactly; use the implementation patterns (LoB, locked enums, provenance metadata) consistently; respect capability + air-gap boundaries; treat OpenAPI/proto as contracts. Refer here for all architectural questions.

**First implementation priority:** the step-3 scaffold commands (repo init), then Postgres-AGE schema + append-only evidence ledger, then the inventory→scan→findings slice.

