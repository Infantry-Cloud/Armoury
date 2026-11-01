---
stepsCompleted: [1, 2, 3, 4, 5, 6, 7, 8]
lastStep: 8
status: 'complete'
completedAt: '2026-06-14'
revisedAt: '2026-11-01'  # backend Go → Rust (control plane + agent)
inputDocuments:
  - _bmad-output/planning-artifacts/prds/prd-Armoury-2026-06-11/prd.md
  - _bmad-output/planning-artifacts/prds/prd-Armoury-2026-06-11/addendum.md
  - _bmad-output/planning-artifacts/briefs/brief-Armoury-2026-06-11/brief.md
  - _bmad-output/planning-artifacts/ux-designs/ux-Armoury-2026-06-12/DESIGN.md
  - _bmad-output/planning-artifacts/ux-designs/ux-Armoury-2026-06-12/EXPERIENCE.md
  - _bmad-output/planning-artifacts/research/market-software-supply-chain-security-research-2026-06-11.md
workflowType: 'architecture'
project_name: 'Armoury'
user_name: 'Daniel'
date: '2026-06-13'
---

# Architecture Decision Document

_This document builds collaboratively through step-by-step discovery. Sections are appended as we work through each architectural decision together._

## Project Context Analysis

### Requirements Overview

**Functional Requirements (30 across 6 groups):**

- **Fleet Inventory (FR1–FR5, FR29):** Two ingestion sources — registry/package-feed enumeration (FR1, FR29) and a live Kubernetes cluster agent (FR3) — joined into one inventory with shipped-vs-running reconciliation (FR4) and honest coverage gaps (FR5). _Architecturally: pull-based connectors + central Syft SBOM generation (FR2), no CI integration in v1._
- **Consistent Scanning & Lifecycle Freshness (FR6–FR10):** Single fleet-wide Grype config (FR6); feed-driven re-evaluation of _stored_ SBOMs without rebuilds (FR7); evaluation provenance recorded (FR8); continuous auto-onboarding within 1h (FR9); air-gapped signed feed bundles (FR10). _Architecturally: the core asynchronous job/scheduler + feed-versioning subsystem, decoupled from builds._
- **Enrichment & Prioritization (FR11–FR15):** Multi-source post-NVD enrichment (KEV, EPSS, CNA, OSV) with per-datum source attribution (FR11–FR12); deterministic, explainable ranking (FR13); triage decisions as first-class versioned data (FR14); VEX ingest + emit (FR15).
- **Blast-Radius & Posture (FR16–FR20, FR30):** Fleet posture landing view (FR16); sub-minute blast-radius query over the graph (FR17); artifact detail (FR18); exportable answers (FR19); Prometheus metrics, pull-only (FR20); a data-quality score distinct from risk (FR30).
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
- **Observability** — Prometheus pull-only; _no_ in-product notifications anywhere.
- **Determinism & explainability** — ranking (FR13) and data-quality (FR30) must be reproducible and inspectable.

### Architectural Risk Register (pre-decision)

Non-obvious risks surfaced during context analysis, carried forward into the decision steps. (R6 — a single-instance batch/query workload-isolation mandate — was considered and cut: NFR10 is a deliberate v1 simplification, not a constraint to architect around.)

| #   | Risk                                                                                                                      | Detection / mitigation hook                                                                                           |
| --- | ----------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| R1  | GUAC query latency degrades non-linearly at upper scale anchor → blast-radius slips past "seconds" (NFR2)                | Query-latency SLO from day one, surfaced via NFR8 path. Favors GUAC-as-rebuildable-projection — _but the rebuild-from-ledger path is itself a load-bearing, must-be-tested component, not an assumed fallback._ |
| R2  | Re-eval throughput bottleneck is feed-delta computation, invisible until a large feed lands; runs overlap next update → backpressure/staleness | Treat feed-delta as a discrete measurable stage; surface backpressure honestly, never hide                           |
| R3  | Agent drops events during control-plane restart (expected under single-instance NFR10) → running-inventory silently desyncs (violates NFR8) | Decide buffer-replay vs. stateless re-derive. If stateless: **jittered reconnect + bounded reconciliation rate** so ≤10 clusters don't storm the just-recovered control plane |
| R4  | Agent transport works connected but breaks under air-gapped mTLS/egress/proxy reality — on exactly the regulated buyers who matter | Design transport against locked-down networks from the start                                                         |
| R5  | Evidence-ledger durability is a _stronger_ requirement than the rest of the DB (NFR10/NFR11), with no cloud backup fallback air-gapped | Separate immutable hash-chained ledger from mutable operational state; air-gap-safe backup story                     |
| R7  | Running digests unmatched to any connected source → invisible _under_-count of "what's running" (worse than over-counting) | Surface as a first-class coverage row ("N running digests not matched to any connected source")                      |
| R8  | Corrupt/partial feed bundle (air-gap, FR10) drives a false-green re-eval → a signed CRA pack seals the false-green       | Atomically validate + sign bundles before they can drive re-eval; partial/failed import **fails closed as stale**, never applies silently |
| R9  | Shared storage contention: a ledger-append failure under disk pressure also freezes operational scan jobs (SPOF, distinct from R5 loss) | Separate quota/reservation for ledger vs. operational state; expose disk-headroom as a health metric (FR20/NFR8)     |
| R10 | Evidence immutability (NFR11) + signing (FR25) **amplify** upstream data errors (enrichment drift, bad feed) into sealed, uncorrectable records | Versioned, superseding corrections; record enrichment/feed **source versions** on findings and pack covers so a later correction is explainable, not locked |
| R11 | Rust backend runs Grype as a subprocess per SBOM (spawn + DB open each time) → re-eval throughput may miss NFR5's 1-hour bound at the scale anchor | Bounded parallel worker pool; measure per-SBOM cost in the R1/R2 load test. Fallback only if the CLI fails the bar: a long-lived Go matcher sidecar (the one Go component allowed back in) |

## Starter Template Evaluation

### Primary Technology Domain

**Multi-component self-hosted system** — there is no single monolithic starter. Four deliverables in **one monorepo** (Daniel's call), all versioned/released together to support SLSA-attested unified releases (NFR7):

1. Web SPA (Svelte) · 2. Rust control plane · 3. Rust cluster agent · 4. Helm chart

Guiding principle (from project memory): **API-first** — the UI, future MCP server, and Prometheus metrics are all consumers of one API spine. The SPA is just the first client.

### Starter Options Considered

- **Frontend — SvelteKit (static/SPA) vs. plain Svelte + Vite.** Chose **SvelteKit with `adapter-static` + SSR disabled**: it's shadcn-svelte's first-class path, uses Vite under the hood, and produces a pure client-rendered SPA (static assets, no Node runtime to operate self-hosted/air-gapped) while giving us file-based routing for the 7 surfaces. Plain Svelte+Vite is the fallback if we want to avoid SvelteKit entirely.
- **Graph library — Svelte Flow (`@xyflow/svelte`, stable v1.6.0).** Stable 1.x release on the same shared core (`@xyflow/system`) as React Flow; further de-risked by the mandatory Graph/Table equivalent (accessibility requirement) so it is never a single point of failure.
- **Backend — Rust, no framework starter.** _Changed from Go on 2026-11-01 (Daniel: more confident with Rust for AI-driven development; the compiler catches more agent mistakes)._ `axum` on `tokio` — a thin router, not a heavyweight framework — producing a lean static (musl) binary for air-gapped Helm delivery. API-first via an OpenAPI contract with generated server types + typed TS client for the SPA. Consequence: the Go OSS substrate is no longer callable in-process — see **Substrate Integration**.
- **Cluster agent — `kube-rs` (`kube` + `kube-runtime` watchers/reflectors), no CRDs.** NFR9 makes the agent a read-only watch/list reporter, not a CRD-owning operator, so no operator framework is needed.
- **Monorepo tooling — Cargo workspace + a task runner.** Root `Cargo.toml` workspace spanning `control-plane`, `agent`, and a shared `agent-proto` crate (agent↔CP protocol types), the SPA under `web/`, charts under `charts/`, driven by a `Taskfile`. Rejected Nx/Turborepo — JS-centric, poor Rust fit.

### Selected Stack & Scaffold

**Versions (current as of 2026-06 — pin at init, not hardcoded forever):** Rust stable (2024 edition) · Svelte 5 / SvelteKit 2 / Vite / Tailwind v4 · shadcn-svelte (latest, runes-native) · `@xyflow/svelte` v1.6.x · `kube-rs` · `tonic` · `sqlx` · Helm 3 · pinned Syft/Grype/Grant/cosign CLIs.

**Initialization commands (these become the first implementation story):**

```bash
# --- repo root: Cargo workspace ---
# root Cargo.toml: [workspace] members = ["control-plane", "agent", "agent-proto"], resolver = "3"

# --- web SPA: SvelteKit (static SPA) + Tailwind + shadcn-svelte ---
npx sv create web --template minimal --types ts --add tailwindcss
cd web
npx shadcn-svelte@latest init          # new-york style, wires Tailwind v4 + components.json
npm i @xyflow/svelte                    # Svelte Flow (stable) for blast-radius + graph explorer
# set adapter-static + `export const ssr = false` in the root +layout for SPA mode
cd ..

# --- Rust control plane ---
cargo new control-plane --bin --name armoury
(cd control-plane && cargo add axum tokio -F tokio/full && cargo add sqlx -F postgres,runtime-tokio,tls-rustls,uuid,migrate)

# --- Rust cluster agent (kube-rs, read-only watcher) ---
cargo new agent --bin --name armoury-agent
(cd agent && cargo add kube -F runtime,rustls-tls && cargo add k8s-openapi -F latest && cargo add tokio -F full)

# --- shared agent protocol (tonic/prost codegen from proto/agent/v1 in build.rs) ---
cargo new agent-proto --lib

# --- Helm chart ---
helm create charts/armoury           # then strip to control-plane + agent subcharts
```

**Architectural decisions provided by this scaffold:**

- **Language & Runtime:** Rust stable (static binaries); Syft/Grype/Grant/cosign run as pinned CLI subprocesses shipped in the control-plane image; Svelte 5 + TypeScript SPA.
- **Styling:** Tailwind v4 + shadcn-svelte (owned components, copied in); design tokens map straight onto the DESIGN.md theme system (Forge/High-Signal/Gunmetal).
- **Build tooling:** Vite (via SvelteKit) for the SPA; Cargo for binaries; Taskfile/Make orchestrates the monorepo.
- **Code organization:** `web/` · `control-plane/` · `agent/` · `charts/` · shared crates via the Cargo workspace; OpenAPI spec as the API source of truth.
- **Testing/Dev:** Vitest + Playwright (SPA); `cargo nextest` + `#[sqlx::test]` (per-test Postgres DB) for the control plane; agent unit-tested against a mocked `kube` client and integration-tested against a kind cluster in CI; hot reload via Vite dev server proxied to the Rust API (`bacon`/`watchexec` on the Rust side).

**Note:** Repo + scaffold initialization (above) should be the first implementation story.

**Downstream doc fix (done 2026-11-01):** DESIGN.md / EXPERIENCE.md now name Svelte (SvelteKit + shadcn-svelte); visual identity and tokens unaffected.

## Core Architectural Decisions

### Decision Priority Analysis

**Critical (block implementation):**

- **Datastore:** PostgreSQL + **Apache AGE** — relational + openCypher graph in one engine. Blast-radius (CVE→package→artifact→workload+time) runs as AGE Cypher traversals.
- **Blob/ledger storage:** **SeaweedFS** (bundled, S3-compatible; external S3 optional) for SBOM blobs and temporal-ledger compaction.
- **Job/queue + re-eval engine:** **River** via its Rust client **`riverqueue`** ([docs](https://riverqueue.com/docs?lang=rust); Postgres-backed, transactional enqueue — a job is inserted in the same transaction as the data it concerns; built on `sqlx` + `tokio`, matching our stack; optional self-hosted River UI). The Rust client is young (first release 2026-10, v0.4) but shares River's mature database schema and job protocol with the Go original; pin the version. Fallback if it bites: `graphile_worker`; re-evaluation is a **feed-delta join** (changed CVEs/ranges → affected stored packages), never a fleet rescan (NFR5).
- **Evidence ledger:** append-only, **hash-chained** rows in Postgres (NFR11); SBOM snapshots compacted to SeaweedFS; corrections are superseding entries (FR14).
- **Agent transport:** **agent-initiated outbound, HTTPS/gRPC + mTLS** (gRPC streaming, HTTPS long-poll fallback where proxies block it) — no inbound to prod clusters (R4).
- **Agent recovery:** **stateless re-derive** — relist from K8s API on reconnect, control plane reconciles; jitter + bounded rate on reconnect (R3).
- **Auth:** OIDC code flow + declarative config + bootstrap admin (NFR6); **httpOnly secure cookie session** for the SPA (avoids tokens-in-JS / XSS).
- **API spine:** OpenAPI-first; server types generated from `api/openapi.yaml` (`openapi-generator` `rust-axum` target) + **`openapi-typescript`/orval** (typed TS client). Fallback if the Rust generator fights us: code-first `utoipa`, with CI failing on any diff between the emitted and committed spec — the committed spec stays the contract either way.

**Important (shape architecture):**

- **RBAC:** admin / analyst / read-only auditor enforced in API middleware; read-only auditor mutations _absent_, not disabled (per EXPERIENCE spec).
- **Secrets at rest:** registry/feed credentials envelope-encrypted; key material from a k8s Secret / Helm value.
- **Signing (FR25/NFR7):** `cosign` — Sigstore **keyless + Rekor when connected**, **operator-managed keys when air-gapped**; verification never requires internet.
- **Frontend server-state:** **`@tanstack/svelte-query`** for posture/blast-radius caching; Svelte 5 runes for local state.
- **Delivery:** Helm **umbrella chart + subcharts** (control-plane, agent), bundling Postgres-AGE + SeaweedFS by default, **external DB/S3 opt-in**; `adapter-static` SPA served by the control plane.
- **Air-gap:** instance-mode flag reshaping feed ingress, enrichment ingress, and signing paths (architectural axis, not a feature).
- **CI/CD:** GitHub Actions; **SLSA provenance + cosign-signed** images, charts, and feed bundles (NFR7).
- **Observability:** Prometheus `/metrics`, pull-only (FR20); no in-product notifications.

**Deferred (post-v1, with rationale):**

- HA / multi-instance control plane — NFR10 defers it; durable evidence survives CP loss.
- **GUAC-as-a-service** — revisit only if graph needs outgrow AGE; avoided now for install/footprint/flux reasons.
- MCP query server & build-time CI SBOM ingestion — explicit roadmap.

### Data Architecture

PostgreSQL (with AGE extension; bundle the `apache/age` Postgres image or build our own) is the single source of truth — relational tables for inventory/findings/triage, an AGE graph for traversal queries, and an append-only hash-chained ledger for evidence. SeaweedFS holds SBOM blobs and compacted historical snapshots (enabling the Retroactive Exposure Replay north-star). Logical separation by schema; R9 (storage contention) and R1 (Cypher latency at scale anchor) carry forward as validated SLOs.

### Authentication & Security

OIDC (`openidconnect` crate) declaratively configured; bootstrap admin for first sign-in / IdP outage. Cookie-session SPA auth. RBAC middleware for the three roles. Connection credentials encrypted at rest. All release artifacts cosign-signed and SLSA-attested.

### API & Communication Patterns

One OpenAPI-described REST spine; UI, future MCP, and metrics are consumers. Agent↔CP over a separate mTLS gRPC/HTTPS channel (agent-initiated, outbound, streaming deltas with stateless re-derive). Standardized typed error envelope; provenance/coverage metadata accompanies every answer-bearing response (honest-degradation contract, NFR8).

### Frontend Architecture

SvelteKit static SPA · shadcn-svelte · Tailwind v4 · Svelte Flow (graph) · TanStack Svelte Query (server state) · command palette (shadcn `Command`). Every graph view has a table equivalent (accessibility + graph-lib de-risk).

### Infrastructure & Deployment

Single Helm umbrella chart; bundled Postgres-AGE + SeaweedFS by default, external opt-in. Air-gap instance mode. SLSA-attested, cosign-signed releases. Single-instance control plane (NFR10); read-only Rust agents via kube-rs.

### Substrate Integration (Rust ↔ Go OSS tools)

Syft, Grype, Grant and cosign are Go with no Rust bindings, so the control plane runs them as **pinned CLI subprocesses** bundled in its image, through one `tools` module (timeouts, JSON decoding, stderr capture, version capture). Tool versions are recorded on every finding and evidence entry, which strengthens FR8 provenance.

- **Syft:** `syft <image-ref> -o syft-json` (CycloneDX/SPDX derived for packs). Registry credentials go in via per-invocation env, never argv.
- **Grype:** `grype sbom:<file> -o json` with `GRYPE_DB_AUTO_UPDATE=false`; `feeds` owns the DB directory, and offline bundles apply via `grype db import` (R8: validate first, fail closed).
- **Grant:** `grant check` against stored SBOMs, JSON output; the wider Grant surface (images, filesystems) stays reachable (FR26).
- **cosign:** `cosign sign-blob --bundle` (keyless when connected, operator key when air-gapped). Verification may use the `sigstore` crate (verification-focused, pre-1.0) or the cosign CLI.

**Upside:** results are byte-for-byte what users get running the same tools themselves (the "embrace the OSS stack" position), a tool crash can't take down the control plane, and tool upgrades don't need a recompile. **Cost:** per-SBOM process spawn plus Grype DB open — see R11.

### Decision Impact Analysis

**Implementation sequence:** (1) repo + scaffold (step-3 commands) → (2) Postgres-AGE schema + evidence ledger → (3) registry connector + Syft SBOM generation + SeaweedFS → (4) Grype scan + River pipeline → (5) feed ingestion + delta re-eval engine → (6) enrichment + ranking → (7) blast-radius/posture API + SPA → (8) agent (transport + re-derive) → (9) triage/VEX → (10) evidence packs + signing → (11) license (Grant) → (12) Prometheus + air-gap bundle path.

**Cross-component dependencies:** AGE graph schema underpins blast-radius _and_ graph explorer; the OpenAPI spine gates UI + future MCP; the hash-chained ledger underlies both triage history and signed packs; the air-gap axis touches feeds, enrichment, and signing simultaneously.

## Implementation Patterns & Consistency Rules

**Primary organizing principle: Locality of Behaviour** — everything that changes together lives together. Organize by capability/domain, never by technical layer. Shallow abstractions (max 3 layers), explicit dependencies, rule-of-three before extraction. (Mirrors the project CLAUDE.md to be generated.)

### Critical Conflict Points Identified

Nine areas where agents could diverge: DB naming, API naming, JSON casing, error/answer envelopes, Rust layout, Svelte file naming, IDs/timestamps, the locked domain vocabulary, and honest-degradation metadata.

### Naming Patterns

**Database (Postgres + AGE):**

- Tables: `snake_case`, **plural** (`artifacts`, `findings`, `triage_decisions`). AGE graph labels: `PascalCase` singular vertices (`Artifact`, `Package`, `Cve`, `Workload`), `UPPER_SNAKE` edges (`DEPENDS_ON`, `AFFECTS`, `RUNS_IN`).
- Columns: `snake_case`; PKs `id`; FKs `<entity>_id`; timestamps `created_at`/`updated_at`; indexes `idx_<table>_<cols>`.

**API:**

- REST, versioned: `/api/v1/<plural-noun>`; path params `{id}`; query params `snake_case`. Resource nesting max one level.
- Headers: `X-Armoury-*` for custom.

**Rust code:** standard Rust naming (`snake_case` items, `PascalCase` types); `rustfmt` + `clippy -D warnings`. **Module-by-capability** under `src/` — each capability module holds its HTTP handlers, domain logic, SQL, and tests _together_ (LoB), never split into `models/`/`services/`/`repositories/`. One crate per binary plus the shared `agent-proto`; **no crate-per-capability split**. **Traits only at the third occurrence or when a real second implementation exists** — never speculative, never single-impl, no `dyn` for a single implementor. No `Manager`/`Factory`/`Provider`/`Handler`/`Adapter` layers. Errors: one `thiserror` enum per capability, propagated with `?`; `anyhow` only in `main`. No `unwrap`/`expect` outside tests and startup wiring; no `unsafe`.

**Svelte/TS:** component files `kebab-case.svelte`, components used `PascalCase`; routes lowercase (SvelteKit `+page.svelte`); stores/composables `use-x.ts` / `camelCase`; types `PascalCase` (generated client is source of truth — never hand-edit).

### Format Patterns

**JSON wire casing:** `snake_case` on the wire (aligns with Postgres columns, friendly to the future MCP server and `curl`/scripting auditors). The TS client maps via codegen, so the SPA still reads idiomatic types.

**Success responses:** return the resource directly (no `{data:...}` wrapper). **Lists** use `{ "items": [...], "page": {...} }` with cursor pagination (no offset at NFR3 scale).

**Error envelope (uniform):**

```json
{ "error": { "code": "snake_case_code", "message": "human readable", "details": {} } }
```

HTTP status carries semantics (400/401/403/404/409/422/500); `code` is the stable machine key.

**Honest-degradation metadata (Armoury-specific, mandatory).** Every answer-bearing response (posture, blast-radius, artifact, packs) carries a `provenance` block — `sources[]` (name, version, retrieved_at), `coverage` (in_scope / scanned / unmatched counts), `freshness` (per-feed age) — and, when partial, a `caveats[]` array. This is the API-side contract behind NFR8 / the honest-provenance UX. No answer ships without it.

**IDs & time:** external IDs **UUIDv7** (time-sortable — suits the append-only ledger and agent-side generation); timestamps **RFC 3339 UTC** strings, always. Durations in seconds (integer).

**Domain vocabulary is locked, not free text.** The glossary (`Artifact`, `Fleet`, `Finding`, `Posture`, `Evidence`, `Evidence pack`, `Control plane`, `Cluster agent`) and the triage status set (`not_affected` / `mitigated` / `accepted` / `fix_planned`, plus derived `untriaged`) are **typed enums** in Rust (`serde` `snake_case`), the OpenAPI schema, and TS — never stringly-typed, never synonymized.

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

**Svelte SPA:** locality via SvelteKit routes — surface-specific components, loaders, and stores live _with their route_ (`routes/posture/`, `routes/blast-radius/`); only genuinely shared primitives sit in `lib/components/ui` (shadcn-svelte). No global `components/` dumping ground; co-locate `*.test.ts`.

**Tests:** co-located everywhere (Rust in-file `#[cfg(test)] mod tests`, cross-module in `tests/`; Svelte `*.test.ts`); Playwright e2e in `web/e2e/`. Run frequently; never deleted to pass.

### Process Patterns

- **Config:** env / Helm values only (NFR6); twelve-factor; secrets via k8s Secret refs.
- **Composition over inheritance** — register implementations in collections (e.g. connector / pack-definition registries), don't extend base types.
- **SPA state/errors:** TanStack Query owns server-state; skeletons mirror layout; render the typed error envelope's `message`; never a bare spinner.
- **Logging:** structured `tracing` JSON (`tracing-subscriber`), levels `debug/info/warn/error`; never log credentials or full SBOM payloads.
- **Migrations:** versioned forward-only SQL (`sqlx migrate`); AGE graph schema versioned alongside.

### Enforcement — All agents MUST

- Treat the **OpenAPI spec as the contract**; regenerate clients, never hand-edit generated code.
- Attach **provenance metadata** to every answer-bearing endpoint.
- Use the **locked enums/glossary**; no invented status or entity synonyms.
- Keep evidence writes **append-only** (superseding entries, never mutate/delete).
- Honor the **air-gap axis**: no new outbound network calls without an offline-bundle equivalent.
- Follow **Locality of Behaviour**: by-capability layout, max 3 layers, no speculative abstraction, no `utils/`/`helpers/`.

### Anti-patterns

Wrapping every response in `{data}`; offset pagination on fleet tables; free-string triage statuses; answers without coverage/provenance; mutable evidence rows; hand-edited generated client code; secrets in logs; by-layer folders (`models/`/`services/`/`repositories/`); `utils/`/`helpers/`/`common/`; single-implementation interfaces; `Manager`/`Factory`/`Provider` layers.

## Project Structure & Boundaries

### Complete Project Directory Structure

```
armoury/
├── Cargo.toml                    # workspace: control-plane, agent, agent-proto
├── Taskfile.yaml                 # build/test/lint/run orchestration (Rust + web + charts)
├── CLAUDE.md                     # LoB rules (generated from Daniel's template)
├── README.md
├── .github/workflows/
│   ├── ci.yml                    # test + lint (Rust fmt/clippy/nextest, web)
│   └── release.yml               # build, SLSA provenance, cosign-sign images/charts/bundles (NFR7)
│
├── api/
│   └── openapi.yaml              # THE REST contract — source of truth (UI + future MCP)
├── proto/
│   └── agent/v1/agent.proto      # agent↔control-plane gRPC contract (FR3/FR4)
├── agent-proto/                  # tonic/prost codegen from proto/ (build.rs), shared by CP + agent
│
├── control-plane/
│   ├── Cargo.toml
│   ├── Dockerfile                # bundles pinned syft/grype/grant/cosign binaries
│   ├── src/main.rs               # wiring ONLY — the one place deps are constructed
│   ├── migrations/               # versioned forward-only SQL + AGE graph schema
│   └── src/                      # module-by-capability; each owns handler+logic+queries+tests
│   │   ├── httpapi/              # generated server stubs + router mount (entrypoint glue only)
│   │   ├── inventory/            # FR1–FR5, FR29  registry/feed connect, Syft SBOM, reconcile, coverage
│   │   ├── feeds/                # FR7, FR10      feed ingestion + signed offline bundles (R8)
│   │   ├── scan/                 # FR6, FR9       uniform Grype matching of stored SBOMs
│   │   ├── reeval/               # FR7, FR8       feed-change re-evaluation (NFR5)
│   │   ├── enrichment/           # FR11, FR12     KEV/EPSS/OSV/CNA aggregation + attribution
│   │   ├── ranking/              # FR13           deterministic KEV-first/EPSS ranking
│   │   ├── triage/               # FR14, FR15     decisions + VEX ingest/emit
│   │   ├── license/              # FR26–FR28      Grant evaluation + policy (parallel to scan)
│   │   ├── posture/              # FR16, FR30     fleet posture + data-quality score
│   │   ├── blastradius/          # FR17, FR19     AGE Cypher traversal + provenance assembly
│   │   ├── graph/                # FR17, FR18     graph-explorer queries
│   │   ├── evidence/             # FR23, NFR11    append-only hash-chained ledger
│   │   ├── packs/                # FR21–FR24      CRA pack generation (extensible)
│   │   ├── signing/              # FR25, NFR7     cosign keyless / operator-key
│   │   ├── metrics/              # FR20           Prometheus exposition
│   │   ├── auth/                 # NFR6           OIDC, bootstrap admin, sessions, RBAC
│   │   ├── agentgw/              # FR3, FR4       agent gRPC gateway (mTLS, reconcile re-derive)
│   │   ├── tools/                # pinned Syft/Grype/Grant/cosign CLI runner (4 callers → earned)
│   │   ├── postgres/             # sqlx pool + migration runner + AGE bootstrap (constructed in main)
│   │   └── blob/                 # S3 client — SeaweedFS default, any S3 (constructed in main)
│
├── agent/
│   ├── Cargo.toml
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
│       │   └── theme/            # Forge / High-Signal / Gunmetal token maps
│       └── routes/               # locality: each surface owns its components/loaders/tests
│           ├── posture/          # + blast-radius/ graph/ artifacts/ findings/ evidence/ settings/
│
└── charts/
    └── armoury/                  # umbrella chart
        ├── Chart.yaml            # deps: postgres-age, seaweedfs (bundled; external opt-in)
        ├── values.yaml           # air-gap flag, OIDC, retention, connections
        └── templates/            # control-plane + agent (agent is install-per-cluster)
```

### Architectural Boundaries

- **API boundary:** `api/openapi.yaml` is the only contract between SPA/MCP and the control plane. Handlers live _in their capability module_; `httpapi` module holds only generated stubs + router assembly. Generated code is never hand-edited.
- **Agent boundary:** `proto/agent/v1` is the only contract between agent and control plane. Agent reaches the control plane _outbound_ (mTLS); never the reverse. Agent depends on nothing in `control-plane/internal`.
- **Capability boundary:** modules communicate through plain `pub` functions and types; traits only at rule-of-three; wired in `main.rs`. No cross-capability reach into another's storage — each owns its own queries.
- **Data boundary:** one Postgres (schemas separate inventory / evidence / graph); evidence schema is append-only at the DB layer (no UPDATE/DELETE grants on ledger tables, NFR11). SBOM blobs only via the `blob` module.
- **Air-gap boundary:** all outbound network access funnels through `feeds`, `enrichment`, and `signing` — the three packages an air-gap audit must cover; nothing else makes external calls.

### Requirements → Structure Mapping

| FR group                            | Primary packages                            |
| ----------------------------------- | ------------------------------------------- |
| Fleet Inventory (FR1–5,29)          | `inventory`, `agentgw`, `agent/watch`       |
| Scanning & Freshness (FR6–10)       | `scan`, `reeval`, `feeds`                   |
| Enrichment & Prioritization (FR11–15) | `enrichment`, `ranking`, `triage`         |
| Blast-Radius & Posture (FR16–20,30) | `posture`, `blastradius`, `graph`, `metrics` |
| Compliance Evidence (FR21–25)       | `evidence`, `packs`, `signing`              |
| License (FR26–28)                   | `license`                                   |

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

- **Grype** matches the package@versions in the stored SBOM against its vuln DB (version-range matching, no image pull). **Grant** evaluates licenses on the same SBOM. License findings skip enrichment/ranking (no KEV/EPSS) but are triagable with the same decision model (FR14) and embedded in the same surfaces (FR28).
- **Feed update → re-evaluation:** `feeds` ingests the new DB; `reeval` uses the **feed delta to select the bounded subset** of stored SBOMs whose packages are touched by changed CVEs, then **re-matches just that subset by reusing `scan`'s Grype matcher** (delta picks the work set; Grype still matches — faithful and uniform, FR6). No rebuilds, no rescans of images, no whole-fleet rerun (NFR5). Updated findings are re-ranked. Grant re-evaluates on license-policy change.
- **Evidence:** every scan, feed version, and triage decision appends to the `evidence` hash-chained ledger (NFR11).
- **Signing — two distinct roles.** Runtime: `packs` reads the ledger → `signing`/cosign seals the generated pack (FR25; Sigstore keyless + Rekor when connected, operator keys when air-gapped) → SeaweedFS. Build-time (CI, not runtime): cosign-sign + SLSA-attest Armoury's own images/charts/bundles (NFR7). Verifying inbound customer-artifact signatures is roadmap, not v1.
- **Exit:** all read surfaces leave via `httpapi` carrying provenance metadata (NFR8); signals leave via `metrics` (Prometheus pull, FR20). The ledger's own integrity is the hash-chain, independent of Sigstore.

## Architecture Validation Results

### Coherence Validation ✅

**Decision compatibility:** Internally consistent — Rust control plane orchestrating the Go OSS tools (Syft/Grype/Grant/cosign) as pinned CLI subprocesses; one Postgres (AGE for graph, relational for state, hash-chained ledger for evidence); SeaweedFS (default) or any S3 for blobs; River (`riverqueue`) for jobs; Svelte SPA over an OpenAPI spine. No version conflicts (AGE supports PG 11–18; all else current). Single-datastore choice directly serves NFR1/NFR4.

**Pattern consistency:** LoB by-capability layout aligns with the FR-group decomposition; OpenAPI-as-contract and the provenance-metadata mandate are enforceable and consistent with NFR8. Locked enums match the UX spec's locked glossary.

**Structure alignment:** Capability packages map 1:1 to FR groups; boundaries (API, agent-proto, air-gap funnel, append-only ledger grants) are concrete and respected by the tree.

### Requirements Coverage Validation

**Functional (30/30 mapped):** Every FR group has owning packages (see Requirements→Structure table). ✅

**Non-functional:** NFR4/6/7/8/9/10/11 fully addressed architecturally. ✅ **NFR2 (sub-minute blast-radius) and NFR5 (1-hour re-eval) are _designed_ but _unvalidated_** — they rest on AGE Cypher latency (R1) and reeval delta-subset throughput (R2), which need a load test at the scale anchor. ⚠️

### Gap Analysis

**Critical gaps (block implementation):** None. Scaffold + inventory + scan + evidence can begin immediately.

**Important gaps (nail before the dependent slice):**

1. **FR30 data-quality scoring model is undefined.** The PRD/UX deliberately left the scoring algorithm (SBOM depth, scan coverage, feed freshness, enrichment coverage, CVE record quality → score+grade) as an architecture/UX decision. Placed in `posture` but the inputs→score function and grade banding need definition before the posture/pack DQ surfaces.
2. **Agent enrollment & identity bootstrap.** Transport (mTLS, outbound) is decided, but how the one-line `helm install` agent obtains its mTLS identity + control-plane address/enrollment token isn't specified — and it's on the UJ-1 30-minute critical path.
3. **Performance validation plan** for R1/R2/R11 (NFR2/NFR5) — including measured per-SBOM Grype subprocess cost — an explicit load test at the scale anchor.

**Minor gaps (specify during the relevant slice):**

- FR13 exact ranking formula (deterministic KEV-first/EPSS-weighted — algorithm vs. principle).
- FR15 VEX format coverage (OpenVEX / CycloneDX VEX / CSAF).
- FR23 retention enforcement + SBOM compaction-to-SeaweedFS mechanism (24-month floor).
- Air-gapped _enrichment_ bundle format (R8 covers feeds; enrichment sources need the same offline path).

### Architecture Completeness Checklist

**Requirements Analysis** — [x] context · [x] scale/complexity · [x] constraints · [x] cross-cutting concerns
**Architectural Decisions** — [x] critical decisions w/ versions · [x] stack specified · [x] integration patterns · [x] performance addressed (validation pending)
**Implementation Patterns** — [x] naming · [x] structure · [x] communication · [x] process
**Project Structure** — [x] directory tree · [x] boundaries · [~] integration points mapped (agent enrollment open) · [x] requirements→structure

### Architecture Readiness Assessment

**Overall Status:** **READY WITH MINOR GAPS** — no critical blockers; implementation can start, with FR30 scoring, agent enrollment, and R1/R2 perf validation to be closed before their dependent slices.

**Confidence:** Medium-high.

**Key strengths:** Single-datastore simplicity serving the air-gap/install gates; honest-degradation baked into the API contract; clean FR→capability mapping under LoB; risk register carried from analysis into concrete mitigations.

**Areas for future enhancement:** HA control plane (NFR10 deferral); GUAC-as-service if graph needs outgrow AGE; build-time SBOM ingestion + inbound-artifact signature verification; MCP query server; **non-Kubernetes runtime agents** (Docker Swarm, HashiCorp Nomad, AWS ECS, Vercel, etc.) — same report-only contract (`proto/agent/v1`), different runtime watcher, so the control plane stays runtime-agnostic.

### Implementation Handoff

**AI agent guidelines:** Follow the documented decisions exactly; use the implementation patterns (LoB, locked enums, provenance metadata) consistently; respect capability + air-gap boundaries; treat OpenAPI/proto as contracts. Refer here for all architectural questions.

**First implementation priority:** the step-3 scaffold commands (repo init), then Postgres-AGE schema + append-only evidence ledger, then the inventory→scan→findings slice.

