---
status: final
stepsCompleted: [1, 2, 3]
inputDocuments:
  - _bmad-output/planning-artifacts/prds/prd-Armoury-2026-06-11/prd.md
  - _bmad-output/planning-artifacts/prds/prd-Armoury-2026-06-11/addendum.md
  - _bmad-output/planning-artifacts/architecture.md
  - _bmad-output/planning-artifacts/ux-designs/ux-Armoury-2026-11-06/DESIGN.md
  - _bmad-output/planning-artifacts/ux-designs/ux-Armoury-2026-11-06/EXPERIENCE.md
amendments:
  - 2026-11-05 Correct Course — _bmad-output/planning-artifacts/sprint-change-proposal-2026-11-05.md (readiness fixes; FR31 and NFR12; Epic 11)
  - 2026-11-06 Correct Course — _bmad-output/planning-artifacts/sprint-change-proposal-2026-11-06.md (cluster-based dev loop and CI)
  - 2026-11-07 Correct Course — _bmad-output/planning-artifacts/sprint-change-proposal-2026-11-07.md (UX spines ux-Armoury-2026-11-06; FR32, FR33; Stories 4.9, 4.10)
  - 2026-11-07 Correct Course — _bmad-output/planning-artifacts/sprint-change-proposal-2026-11-07-readiness.md (readiness blockers B1–B8; no story added, removed or renamed)
  - 2026-11-07 Correct Course — _bmad-output/planning-artifacts/sprint-change-proposal-2026-11-07-aliases.md (readiness blocker 9, vulnerability ID aliases, and the gated concerns; no story added, removed or renamed)
---

# Armoury - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for Armoury, decomposing the requirements from the PRD, UX Design if it exists, and Architecture requirements into implementable stories.

## Requirements Inventory

### Functional Requirements

FR IDs are the PRD's stable IDs (FR29–FR30 were added at finalize, FR31 on 2026-11-05 and FR32–FR33 on 2026-11-07, so they sit out of numeric sequence).

**Fleet Inventory**

- FR1: Registry connection — SecOps supplies container registry credentials; Armoury enumerates repositories and image digests with no CI changes.
- FR29: Package feed connection — SecOps connects package feeds and artifact repositories (language-ecosystem registries, internal mirrors); Armoury enumerates packages and SBOMs them uniformly.
- FR2: Central SBOM generation — Syft SBOMs for every discovered artifact, centrally and uniformly, with no per-repo configuration.
- FR3: Live cluster inventory — a cluster agent watches the Kubernetes API and maintains a live record of running image digests (cluster/namespace/workload), reported to the control plane.
- FR4: Shipped-vs-running reconciliation — registry artifacts and running workloads are linked in one inventory; "is this running anywhere?" is answerable per artifact.
- FR31: Optional CI scan — a pipeline step submits a built artifact (image digest from a connected registry, or an uploaded image or package archive, never source); the server SBOMs, scans and license-checks it with the fleet toolchain, decides pass or fail with the fleet CI policy, links known artifacts instead of duplicating them, and the step always prints the verdict and the artifact URL. Central scanning stays the default.
- FR32: Artifact signature verification — container images and other OCI artifacts in connected registries are checked against signers an admin trusts (public keys or keyless identities); the result, signer and check time are recorded as evidence and shown in artifact detail; verification runs only on the control plane and works air-gapped (key-based with no network, keyless with trust material supplied offline).
- FR5: Coverage visibility — the inventory shows its own gaps: discovered-but-not-SBOM'd images, unreachable registries, disconnected agents.

**Consistent Scanning & Lifecycle Freshness**

- FR6: Uniform scanning — every SBOM is scanned by Grype with one fleet-wide configuration and policy; the same artifact always produces the same result.
- FR7: Feed-driven re-evaluation — when vulnerability feeds update, existing SBOMs are re-evaluated automatically, without rebuilds or manual rescans.
- FR8: Evaluation provenance — every finding records when it was last evaluated and against which feed versions.
- FR9: Continuous onboarding — newly discovered images/packages are SBOM'd and scanned automatically within one hour of discovery.
- FR10: Air-gapped feed updates — vulnerability and enrichment feeds can be imported as a signed offline bundle built on a connected machine; Armoury also publishes signed bundles, so an operator does not need a connected build machine.

**Enrichment & Prioritization**

- FR11: Multi-source enrichment — findings enriched from CISA KEV, EPSS, CNA records and OSV.
- FR12: Source attribution — every enrichment datum is labelled with its source and retrieval time.
- FR33: End-of-life data — for the packages in every stored SBOM, whether each package version has reached its end of life, from an attributed source refreshed like the enrichment feeds, re-joined without rescans and carried in the offline bundle; shown in artifact detail; uncovered packages are "unknown", never "supported".
- FR13: Risk-based prioritization — deterministic, explainable ordering: licence findings as their own group first (hidden when empty), then severity groups Critical, High, Medium, Low, Negligible and unrated (UI "Not rated yet"; both hidden when empty); KEV-listed (actively exploited) first within each group, then by EPSS; EPSS is never presented as a rating; the UI states the order in words.
- FR14: Triage decisions as first-class data — status (not affected / mitigated / accepted / fix planned; untriaged when none), justification (required except for fix planned, whose VEX action statement then comes from the planned fix), author, timestamp and scope (every artifact with the same vulnerability or licence in the same package version by default, or one artifact); decisions propagate to posture views, team consumption and evidence packs.
- FR15: VEX support — triage decisions are expressible as standard VEX; vendor VEX documents are ingested and their not-affected claims applied (with attribution) to fleet findings.

**Blast-Radius Query & Posture View**

- FR16: Fleet posture view — landing state (UI: Home): fleet summary of artifacts, the findings that need attention today, open findings by group (FR13), coverage gaps and feed freshness.
- FR17: Blast-radius query (UI: Exposure) — given a CVE ID, package+version or image digest, answer which artifacts (shipped and running) are affected and where deployed (cluster/namespace/workload), in seconds, with data provenance (sources, coverage, freshness); an unknown CVE ID is answered as unknown with the data's age, never as zero; any node of the answer can be followed to its own connections.
- FR18: Artifact detail (UI: Software detail) — SBOM contents, findings (vulnerability and license) with triage status, evaluation provenance, running locations, signature status (FR32), package end-of-life status (FR33) and the data-quality score (FR30); "check again" re-queues the SBOM and scan.
- FR19: Shareable answers — the current view of a blast-radius answer, the findings list or the artifact list exports as CSV (JSON optional), with the screen's caveats and provenance, and a blast-radius answer also as a PDF report; every export is stored as evidence (file + ledger entry, evidence-pack retention) and listed with the packs; the posture summary is shared as an evidence pack.
- FR20: Prometheus metrics — posture signals exposed as metrics (new critical/KEV findings, coverage gaps, feed freshness, agent health); pull-only, no notifications.
- FR30: Data-quality score — a score grading the trustworthiness of the underlying data (SBOM depth/completeness, scan coverage, feed freshness, enrichment source coverage, CVE record quality), at artifact level in artifact detail and at fleet level in evidence packs (their in-product detail and printed cover page); never in list rows.

**Compliance Evidence**

- FR21: CRA compliance pack — evidence report for a chosen time window: inventory, proof of uniform scanning and feed freshness, findings with handling decisions, license section; states its own coverage and data quality.
- FR22: Compliance packs as a layer — CRA is the first instance of a pack architecture (framework report definitions over the same evidence) so DORA/FedRAMP/PCI are additive.
- FR23: Evidence collected continuously, generated on demand — any period under management is reportable after the fact; configurable retention with a compliance floor (default ≥ 24 months).
- FR24: Auditor-consumable formats — PDF plus machine-readable companions (SBOMs, VEX).
- FR25: Signed evidence packs — tamper-verifiable; connected deployments may use Sigstore keyless, air-gapped deployments sign with operator-managed keys; verification never requires internet. (Runtime default is the operator key; keyless is opt-in — ARCH18.)

**License Compliance**

- FR26: License evaluation — Grant across its full surface (SBOMs, container images, filesystems); defaults to Armoury-generated SBOMs without restricting Grant's capability.
- FR27: License policy — fleet-wide allow/deny policy; violations surface as findings in the same posture/findings/artifact views (UI: a Licences group listed first and hidden when empty, and a Licences type filter), triagable with the FR14 model.
- FR28: License evidence — the license section of evidence packs draws from this data; embedded, never headline.

### NonFunctional Requirements

- NFR1: Time to value — `helm install` to first fleet-wide posture view in < 30 min by one SecOps engineer with no dev-team cooperation; posture live and visibly populating with an explicit coverage indicator; full initial evaluation within 24 h at the scale anchor. Product gate: anything that breaks it doesn't ship in the install path.
- NFR2: Query performance — blast-radius answers in seconds, under a minute worst case, at the scale anchor.
- NFR3: Scale anchor — hundreds of repositories, thousands of container images, up to ten connected clusters.
- NFR4: Deployment — self-hosted Helm chart into existing Kubernetes; fully air-gapped capable; no phone-home, nothing silently requiring internet.
- NFR5: Freshness — after a feed update (online or offline bundle), fleet-wide re-evaluation completes within one hour at the scale anchor.
- NFR6: Access control — OIDC SSO configured declaratively (env / Helm values / config file, never a UI wizard); bootstrap admin for first sign-in and IdP-outage recovery; OIDC optional at install; roles admin / analyst / read-only auditor; scoped CI tokens (not a user role) for CI scans (FR31).
- NFR7: Armoury's own provenance — images, charts and feed bundles signed and SLSA provenance-attested via Sigstore; each release publishes Armoury's own scan result.
- NFR8: Honest degradation — disconnected agents, stale feeds and unscanned artifacts surface in posture and metrics; the posture never needs a caveat the UI doesn't already show.
- NFR9: Agent footprint — cluster agents lightweight and read-only: watch/list only, never cluster-admin.
- NFR10: Availability — single-instance control plane in v1 (no HA); loss of the control plane never loses recorded evidence.
- NFR11: Evidence integrity — the evidence store is append-only and tamper-evident; scans, feed versions and triage decisions cannot be silently edited or deleted. Optionally (off by default), signed ledger checkpoints can be anchored in a Rekor transparency log outside the installation.
- NFR12: Server-side evaluation — Syft, Grype, Grant and every policy check run only on the control plane with the fleet toolchain; CI runners, agents and other clients only identify artifacts or supply their bytes; client-computed SBOMs, findings, license results or verdicts are never used.

### Additional Requirements

From `architecture.md` (revised 2026-11-01, Rust backend; amended 2026-11-05 by the Correct Course). IDs are local to this document.

**Starter / scaffold (→ Epic 1 Story 1)**

- ARCH1: **No off-the-shelf starter; a monorepo scaffold is the first implementation story.** Cargo workspace (`control-plane`, `agent`, `agent-proto`, resolver 3, Rust 2024); `web/` via `npx sv create web --template minimal --types ts --add tailwindcss` + `shadcn-svelte init` + `@xyflow/svelte`, `adapter-static` with SSR off; `cargo new` for control plane (`axum`, `tokio`, `sqlx` postgres/rustls/uuid/migrate) and agent (`kube` runtime+rustls, `k8s-openapi`, `tokio`); `agent-proto` lib with tonic/prost codegen from `proto/agent/v1`; `helm create charts/armoury` stripped to control-plane + agent subcharts; `mise.toml` (pinned tools) and `mise-tasks/` (mise file tasks; Taskfile replaced 2026-11-05); `api/openapi.yaml`; `.github/workflows/ci.yml` and `build.yml`; `control-plane/Dockerfile` and `agent/Dockerfile`; `skaffold.yaml` (ARCH34). Pin versions at init.

**Platform & data**

- ARCH2: PostgreSQL 18 + Apache AGE 1.8 (`apache/age:release_PG18_1.8.0`, pinned by digest, bundled and for tests) is the single source of truth — relational tables, AGE graph for traversals, and separate schemas for inventory / evidence / graph; forward-only `sqlx migrate` migrations with the AGE graph schema versioned alongside.
- ARCH3: SeaweedFS (bundled, S3-compatible; external S3 opt-in) holds SBOM blobs and compacted historical snapshots, accessed only via the `blob` module.
- ARCH4: Jobs via River's Rust client `riverqueue` (pinned `=0.5.0`, requires `sqlx` 0.9 and `jiff`; River migrations via `riverqueue-migrate` run before `sqlx` migrations; fallback `graphile_worker`) with transactional enqueue (job inserted in the same transaction as its data).
- ARCH5: Evidence ledger — append-only, hash-chained rows in Postgres; no UPDATE/DELETE grants on ledger tables for the application role, which owns no table (`armoury_owner` owns them and is used only by the migration Job and the maintenance CronJob; `armoury_app` is the control-plane login); corrections are superseding entries; ledger and history size and database volume headroom exposed on the health endpoint and in metrics with a warning threshold (default 80 % used); for external Postgres with no budget set, size only and "headroom unknown", no warning (risks R5, R9). Past state lives in history tables (ARCH32).
- ARCH6: Re-evaluation is a feed-delta join — `grype db diff -o json <previous-db> <current-db>` (Grype pinned, ≥ v0.121.1) gives the changed packages, which select the bounded subset of stored SBOMs through the package index; that subset is re-matched with `scan`'s Grype matcher. Armoury never reads the Grype SQLite schema. Each activated DB lives in its own directory (current and previous kept). Fallback chosen by measurement (Story 4.8): full re-check of every stored SBOM. The delta stage is measurable and backpressure is surfaced honestly (R2).
- ARCH7: Substrate tools module — Syft/Grype/Grant/cosign (and Typst for PDFs, ARCH35) run as pinned CLI subprocesses bundled in the control-plane image (each added, checksum-verified, by the story that first uses it: Syft 2.3, Grype 2.4, cosign 4.5, Grant 7.1, Typst 6.5) through one `tools` module (timeouts, JSON decoding, stderr capture, version capture). Tool versions are recorded on every finding and evidence entry; credentials go via per-invocation env, never argv; `GRYPE_DB_AUTO_UPDATE=false`; Grype runs with `--by-cve` (ARCH38); bounded parallel worker pool. A long-lived Go matcher sidecar is allowed only if the CLI fails the NFR5 bar (R11).

**Agent**

- ARCH8: Agent transport is agent-initiated outbound mTLS gRPC streaming over `proto/agent/v1` (HTTPS long-poll fallback where proxies block gRPC); no inbound connections to prod clusters (R4). The agent uses its own control-plane port (gRPC and long-poll on one port); the control plane ends mTLS itself with `rustls`; the chart exposes the port as `LoadBalancer`/`NodePort` or ingress TLS passthrough — an ingress that ends TLS is not supported for this port.
- ARCH9: Agent recovery is stateless re-derive — relist from the K8s API on reconnect and let the control plane reconcile, with jittered reconnect and a bounded reconciliation rate (R3).
- ARCH10: **Open gap:** agent enrollment and identity bootstrap — how the one-line agent `helm install` obtains its mTLS identity, control-plane address and enrollment token. On the UJ-1 30-minute critical path; must be defined before the agent slice.
- ARCH11: Running digests unmatched to any connected source are surfaced as a first-class coverage row (R7).

**API & security**

- ARCH12: OpenAPI-first — `api/openapi.yaml` is the contract; server types are generated (`openapi-generator` rust-axum, run from its pinned container image so no local Java is needed; fallback code-first `utoipa` with CI failing on spec diff), plus a generated TS client (`openapi-typescript` + `openapi-fetch`). `mise run gen:api` regenerates; `mise run check` fails if generated code differs from committed code. Generated code is never hand-edited. Every operation declares `x-armoury-role: admin | analyst | auditor` (and `x-armoury-role-setting` where a setting can open it to a lower role); the RBAC middleware reads it. A CI token is not a role: routes that CI may call also declare `x-armoury-ci-token: true`. CI tokens use `Authorization: Bearer <token>` (a session cookie never counts as a CI token); the middleware accepts a CI token only on marked routes and returns 403 on every other route.
- ARCH13: API conventions — `/api/v1/<plural-noun>`, snake_case JSON and query params, resources returned unwrapped, lists as `{items, page}` with cursor pagination (no offset), uniform `{error:{code,message,details}}` envelope, UUIDv7 IDs, RFC 3339 UTC timestamps, durations in integer seconds, `X-Armoury-*` custom headers. Long-running work uses the long-operation pattern (ARCH33).
- ARCH14: Mandatory `provenance` block (`sources[]`, `coverage`, `freshness`, `caveats[]` when partial) on every answer-bearing response (posture, blast radius, artifact, packs).
- ARCH15: Locked domain vocabulary and triage status set (`not_affected` / `mitigated` / `accepted` / `fix_planned`, derived `untriaged`) as typed enums in Rust, OpenAPI and TS. UI labels come from the plain-language glossary (UX-DR33: Not reviewed yet · Not impacted · Fix planned · Mitigated · Risk accepted); enum values and API names do not change.
- ARCH16: Auth — OIDC code flow (`openidconnect` crate), declarative config, bootstrap admin, httpOnly secure cookie session for the SPA; RBAC enforced in API middleware. Sessions live in a PostgreSQL `sessions` table (the cookie holds a random ID; the table stores its hash); idle and maximum lifetime are Helm values (defaults 8 h / 24 h). User preferences (theme Light/Dark, default Light; the single-key shortcut switch from Settings → Personal, default on) live in `user_preferences` (`GET`/`PUT /api/v1/me/preferences`). Both are "not evidence".
- ARCH17: Registry/feed credentials are envelope-encrypted at rest, with key material from a k8s Secret / Helm value: AES-256-GCM via `aws-lc-rs`; one random data key per credential, wrapped by the master key; a key ID per record for rotation (add new master key, re-encrypt data keys, remove old key); the record ID as AAD. With no master key in the chart, the control plane generates one on first start and stores it in a Secret.
- ARCH18: Signing via `cosign` — runtime setting `signing.mode` (PROC2): `key` (default; operator key from a Secret, generated on first start when none is supplied, public key shown in Settings and appended to the ledger) or `keyless` (opt-in; projected service-account token to public Fulcio for EKS/GKE/AKS issuers or a private Fulcio, with Rekor; an unaccepted issuer fails at startup). Air-gapped mode always uses `key`. Mode and signer identity recorded on each signature. Verification never requires internet (`sigstore` crate or cosign CLI). Build-time keyless signing of Armoury's own releases is unchanged. Exceptions: operator-built feed bundles (Story 4.5) are always signed with the operator key; Armoury-published feed bundles (Story 10.2) are signed with the KMS bundle key. `ponytail:` a Secret-held key is only as safe as the cluster; upgrade path a cosign KMS key reference.

**Air gap**

- ARCH19: Air-gap is an instance-mode flag that reshapes feed ingress, enrichment ingress and signing. Outbound calls fall in two classes: **admin-configured endpoints** (registries, package feeds, the OIDC issuer, a private Fulcio, a configured Rekor (ARCH37), proxies — called only by the module that owns the connection, at its configured URL; an accepted default public URL is stored in the connection and counts as admin-configured) and **built-in public endpoints** (Grype DB, KEV, EPSS, OSV, CVE List, the end-of-life data source (FR33), public Fulcio, public Rekor — called only by `feeds`, `enrichment` and `signing`, and turned off completely in air-gapped mode).
- ARCH20: Offline bundles cover both vulnerability feeds **and** enrichment sources (KEV/EPSS/OSV/CNA, and end-of-life data from Story 4.9). Bundles are atomically validated and signature-checked before they can drive re-evaluation; a partial or failed import fails closed as stale (R8). The enrichment bundle format is an open minor gap.
- ARCH21: Record enrichment/feed source versions on findings and pack covers, so later corrections are explainable rather than locked (R10).

**Delivery, CI, observability**

- ARCH22: Helm umbrella chart with control-plane and agent subcharts, images referenced by digest; Postgres-AGE and SeaweedFS bundled by default, external DB/S3 opt-in; values cover the air-gap flag, OIDC, retention and connections. The SPA is served by the control plane.
- ARCH23: CI/CD on GitHub Actions, installing mise (`jdx/mise-action`, pinned by commit) and running the same mise tasks as local; untrusted code (fork pull requests) runs only the fast tier on GitHub-hosted runners, and the full gate, end-to-end tests and image builds run on ARC self-hosted runners in the dev cluster — `ci.yml` (`mise run check`: rustfmt, `clippy -D warnings`, `cargo nextest`, web lint/tests, API drift), `build.yml` (build both images and package the chart on each push; push to GHCR by digest on `main`) and `release.yml` (reuse the built digests; release tags, SLSA provenance, keyless cosign signatures and SBOM attestations for images, charts and the CLI); a scheduled `bundles.yml` builds the Armoury-published feed bundles and signs them and their SLSA provenance with the KMS bundle key (Story 10.2).
- ARCH24: Observability — Prometheus `/metrics`, pull-only; structured `tracing` JSON logs that never contain credentials or full SBOM payloads; no in-product notifications.

**Code & test patterns (apply to every story)**

- ARCH25: Locality of Behaviour — module-by-capability (`inventory`, `ciscan`, `feeds`, `scan`, `reeval`, `enrichment`, `ranking`, `triage`, `license`, `posture`, `blastradius`, `graph`, `exports`, `evidence`, `packs`, `signing`, `metrics`, `auth`, `agentgw`, `tools`, `postgres`, `blob`, `httpapi`); max 3 layers; explicit dependencies wired only in `main.rs`; no globals/singletons; traits only at the third occurrence; one `thiserror` enum per capability; no `unwrap`/`expect` outside tests/startup; no `unsafe`; no `utils/`/`helpers/`/`common/`; files 100–400 lines.
- ARCH26: Frontend — TanStack `svelte-query` for server state, Svelte 5 runes for local state, components co-located with their routes, shadcn-svelte primitives in `lib/components/ui`, and a table equivalent for every graph view.
- ARCH27: Tests co-located — `cargo nextest` + `#[sqlx::test]` against `apache/age:release_PG18_1.8.0`, pinned by digest, which runs as a Pod in the dev cluster (`mise run check` reaches it by port-forward locally and by Service DNS on ARC runners; no local database); agent tested against a mocked kube client plus an integration test in a temporary dev-cluster namespace in CI; Vitest + Playwright (`web/e2e/`, `mise run e2e` against the Skaffold deployment) for the SPA.

**Validation & open decisions**

- ARCH28: Performance validation — a load test at the NFR3 scale anchor for R1 (AGE blast-radius latency, NFR2), R2 (re-eval delta throughput, NFR5) and R11 (per-SBOM Grype subprocess cost), with the query-latency SLO surfaced through the NFR8 path from day one.
- ARCH29: Decisions to close before their dependent slice — FR30 scoring model and grade banding (the UX bands are a placeholder — EXPERIENCE Open item 11); FR13 within-group order (actively exploited first, then raw EPSS, then a stable tie-breaker — EXPERIENCE Open item 1); FR15 VEX formats (decided 2026-11-04: OpenVEX + CycloneDX VEX, CSAF deferred; now recorded in `architecture.md`) and the VEX status mapping (open — Story 5.6 amendment, user-approved before implementation); FR23 retention mechanism (decided 2026-11-04, see ARCH30; now recorded in `architecture.md`).
- ARCH30: **Evidence retention mechanism — signed checkpoints, then archive** (decided by Daniel, 2026-11-04). (1) The ledger table (by entry time) and the history tables (ARCH32, by `valid_to`) are partitioned by month from their first migration. (2) At a configurable interval (default: daily), a checkpoint entry records the chain head hash, entry count and covered time range, and is signed by the `signing` capability in the configured signing mode (ARCH18). Signed checkpoints also detect a full-chain recompute by a database superuser, which the hash chain alone cannot. (3) When a whole monthly partition is older than the retention period (default and minimum 24 months) and is covered by a signed checkpoint, the maintenance CronJob with the `armoury_owner` login exports it to the object store as an archive segment (compressed, with its digest referenced by a ledger entry), verifies the segment against the checkpoint, and only then drops the partition. The application role keeps no DELETE grant. (4) Chain verification starts from the oldest hot checkpoint; archived segments verify independently against their checkpoint. (5) Point-in-time queries and packs for archived windows read verified archive segments, so the window stays reportable. (6) Archive segments are kept forever by default; an admin can enable a purge after a further configurable period, recorded as a ledger entry and never silent (PROC2, NFR11 "never silently deleted"). History-table partitions follow the same archive path.

**Amendments 2026-11-05 (Correct Course; also recorded in `architecture.md`)**

- ARCH31: **All scanning on the server** (NFR12, governing principle). Syft, Grype, Grant, license policy, the CI policy and every other check run only in the control plane with the fleet tool versions and configuration. A CI runner, a cluster agent or any other client only identifies an artifact or supplies its bytes; the server never uses a client-computed SBOM, finding, license result or verdict. Overrides any conflicting statement.
- ARCH32: **Evidence history tables.** Each evidence-bearing table has a current table and an insert-only history table (`valid_from`/`valid_to`), partitioned by month on `valid_to` (the ledger by entry time), filled only by a database trigger on update or delete; each version closes when the next starts, so versions cannot overlap (no `WITHOUT OVERLAPS`, which checks only inside one partition). Rule 1: a version is written only on content change; a re-evaluation writes one run entry instead of re-versioning unaffected rows. Rule 2: a coverage test requires every table in every application schema to have a history table or an explicit "not evidence" marker. Each change appends a ledger entry with the digest of the new version; events that are themselves the fact keep their full content in the entry; large content stays content-addressed in the object store. No credentials or secrets in ledger or history (tested). The AGE graph shows current state only.
- ARCH33: **Long-operation API pattern, polling.** `POST /api/v1/<operations>` returns at once with `id`, `status` (`running`/`completed`/`failed`), `progress`, partial results, `provenance` and a result cursor; `GET /api/v1/<operations>/{id}` returns the same shape. The SPA polls with svelte-query (about 1 s for operations, about 10 s for the Home summary (posture endpoint, including the Needs-attention count) while backlog exists), only while work is queued or running. No SSE in v1. `ponytail:` partial blast-radius results live in memory about 10 minutes (single instance); upgrade path PostgreSQL.
- ARCH34: **Images, chart build and dev loop.** Multi-stage Dockerfiles (control plane with SPA; agent binary only, no scanner tools; base images pinned by digest); `build.yml` builds both images and the chart and pushes to GHCR by digest on `main`; `skaffold.yaml` (pinned Skaffold) with the Helm deployer (`setValueTemplates`, `repo:tag@digest`) is the development loop (PROC3): `mise run dev` builds both images on the in-cluster BuildKit (rootless, mTLS, through a pinned `buildx`), pushes them to the dev registry (`SKAFFOLD_DEFAULT_REPO`), deploys to the developer's namespace in the dev cluster with an explicit kube context, and port-forwards the UI and API to `localhost:8080`. A `ci` profile deploys to a temporary namespace from ARC runners. No local container runtime or local cluster is used (amended 2026-11-06). Customers install the published chart with one `helm install` (Helm 4). `ponytail:` slow Rust rebuilds — debug dev profile and a cached dependency layer; upgrade path a remote build cache.
- ARCH35: **Connectors and renderers.** Registry access with the `oci-client` crate; discovery modes (PROC2): catalog (default), provider API (ECR, Artifact Registry, Docker Hub), repository list. Package archives are downloaded, checksum-checked against the feed, unpacked safely (no path traversal, no links outside the folder) and SBOM'd with `syft dir:<path>` (`syft file:<path>` for JAR files); an archive without a lock file gives the package itself, not exact dependency versions, shown as a caveat. PDFs are rendered by Typst, a pinned static binary run through `tools`, with the bundled IBM Plex Sans and IBM Plex Mono fonts and the DESIGN.md `print-*` palette (Inter is no longer used).
- ARCH36: **CI scan path (FR31).** `armoury scan` is a subcommand of the `armoury` binary with no scanner inside. Digest mode (default): the CLI sends the image digest and build details declared by CI; the server pulls the image by digest from the connected registry. Upload mode: the CLI uploads the built image or package archive (never source); the server computes the digest itself. CI scans run through the same pipeline at a higher queue priority. The server decides the verdict with the versioned fleet CI policy (default: report only); the CLI cannot change it, and vendor VEX claims never change it — only a person's review decision does. Exit codes `0` pass, `1` policy failure, `2` no verdict. Artifact identity is the image digest, or package coordinates plus archive checksum; a known artifact gets a new source record, not a duplicate. A scoped CI token (not a user) authenticates the step. Accepted limit: a pipeline can skip the step; central discovery still scans connected registries.
- ARCH37: **Optional Rekor anchoring of ledger checkpoints** (decided by Daniel, 2026-11-05). Setting `rekor.anchoring.mode`: `disabled` (default), `external` (a Rekor URL and its public key; the public `rekor.sigstore.dev` or a Rekor that another team runs) or `bundled` (the chart deploys `rekor-tiles` with the POSIX backend on its own volume; no witness is required, an optional witness policy is a value). Chart comments recommend `external`. After each signed checkpoint, `signing` submits only the checkpoint digest, its signature and the public key as a `hashedrekord` entry and appends the returned inclusion proof to the ledger. Known limit: Rekor v2 returns no signed timestamp, so detection of a full rebuild that is re-anchored depends on an earlier receipt (for example in an evidence pack) or on a monitor of the log; an RFC 3161 timestamp authority is a later option.

**Amendments 2026-11-07 (Correct Course; also recorded in `architecture.md`)**

- ARCH38: **Issues read model and review scope** (D1, D6–D8). Findings stay per place (one match on one artifact). The API adds **finding groups** (UI "issue"), keyed by vulnerability ID (the key ID: the CVE ID when the vulnerability has one, else the original ID — GHSA, OSV or distro ID) + package purl@version, or licence + finding kind + package purl@version, with `group` (`licence`/`critical`/`high`/`medium`/`low`/`negligible`/`unrated`; `negligible` = Grype Negligible, `unrated` = Grype Unknown or no severity, UI "Not rated yet"), `kev`, place count, issue-wide `triage_status` (the latest `all_places` decision; `untriaged` when there is none), derived `mixed` with the count of places whose own `artifact` decision differs from it, and `needs_attention`; per-group, per-status and Needs-attention counts and a pager total come from the server (the Needs-attention count is always fleet-wide; the type filter and search never change it); the list takes `needs_attention=true` (the Issues "Needs attention" filter and Home's "Review all N"). Needs attention = any place `untriaged` AND (`kev` OR critical) for vulnerabilities; any place `untriaged` for `license_violation`; never for `license_warning`. Decisions carry scope `all_places` (default; covers artifacts found later) or `artifact`; per-artifact decisions override and survive a later `all_places` decision; a place's effective status is its own `artifact` decision if present, else the issue-wide status (used by status filters, Needs attention and VEX); only people's decisions set a status — vendor VEX claims (Story 5.7) are display-only. `justification` is required except for `fix_planned`. Metrics keep counting findings (places). The issue sentence is the first sentence of the advisory description in the vulnerability record, unchanged, with its source (FR12); none when the record has no description. Vulnerability IDs and aliases: Grype runs with `--by-cve`; each finding stores every alias of its vulnerability; KEV matching, the enrichment joins (EPSS, CNA, OSV), Exposure queries, the unknown-vulnerability check and ⌘K search match on any alias, so a CVE query and a GHSA query find the same issue; the UI shows the key ID and lists the other aliases in the technical-details block.
- ARCH39: **Stored exports** (D3, FR19). Export (CSV of the current view; JSON option) from Exposure, Issues and Software, and the Story 6.5 answer report, are stored: the file in the object store (content-addressed, via `blob`), an insert-only `exports` record and a ledger entry with the file digest (who, when, view, query or filters, format, row count, caveats). Evidence-pack retention (ARCH30); no edit or delete. Listed newest first in Reports → Exports. Owner module `exports` (recommended, O1).
- ARCH40: **Artifact signature verification** (FR32). Control plane only: `inventory` runs `cosign verify` through `tools` against signatures read from the connected registry (credentials in per-invocation env), using admin-configured trust (public keys, keyless identities; default none). Results and trust-policy versions go to the ledger and the artifact API. Air-gapped: no network for key-based checks; keyless checks use an offline trusted root. The trust model, result states, formats, trusted-root delivery and artifact types are recorded as an amendment approved before Story 4.10.
- ARCH41: **End-of-life data** (FR33). One more `enrichment` source (a built-in public endpoint with an offline-bundle equivalent), stored as versioned, attributed snapshots, re-joined to stored SBOM packages without re-matching; status past end of life / supported / unknown per package; carried in the offline bundle. The source, licence, coverage, matching rule and staleness threshold are recorded as an amendment approved before Story 4.9.

**Process constraint (project workflow, not architecture)**

- PROC2: **Offer options rather than forcing one approach, with smart defaults** (Daniel, 2026-11-04). Where more than one valid approach is available and supportable — scopes, formats, modes, sources, weights — make it a configurable option instead of picking one for the user. Every option has a smart default, so a default install needs no configuration at all; options are there for users who go looking for them, never a required setup step (protects NFR1). Stories record the default and the alternatives.
- PROC3: **Skaffold runs during every development step** (Daniel, 2026-11-05). Every development step starts with `mise run dev` (Skaffold `dev` on the dev cluster) running and deploying continuously (amended 2026-11-06). The story's changes are checked against that live deployment as well as by `mise run check`. If the loop is not running or the deployment is not healthy, fix that before you write code. Applies to every story after Story 1.1, which creates the loop; `AGENTS.md` states this rule.
- PROC1: The scaffold story is readiness-enabling work. Agent Readiness (Linear INF-12) runs after it and must be ready before product stories start Build (the `bmad-build` / `bmad-code-review` readiness gate).

### UX Design Requirements

From `DESIGN.md` + `EXPERIENCE.md` (ux-Armoury-2026-11-06, both final, updated 2026-11-07; they supersede ux-Armoury-2026-06-12 — Correct Course 2026-11-07). Token names refer to DESIGN.md frontmatter. UX-DR numbers are stable: retired items stay as "Retired" so story references resolve; new items start at UX-DR37. Where a requirement is not yet drawn, the item cites the EXPERIENCE "Open items" number — do not invent it.

**Design tokens & theming**

- UX-DR1: Semantic colour token layer on shadcn-svelte CSS variables (DESIGN.md "shadcn mapping", plus `--paper`, `--dq`, `--dq-muted` and `--dq-wash`), with two themes shipped day 1 — **Light** (default; unsuffixed tokens) and **Dark** (`-dark` tokens) — sharing the same roles, layout and density, using the exact DESIGN.md values. Components reference semantic roles only, never a theme-specific hex. `lime` only for the active nav item and the one primary action per view, plus the agreed exceptions (the selected graph node and "Selected on the map", together with the centre dot of a moved Exposure map; the Issues nav badge count; text selection; the focus ring on the sidebar, on forest selection and in dark; and the all-clear tints `lime-wash` and `lime-ring`); `forest` for selection, the active tab and the active segment, with the text colour switching with the fill (`on-forest`, `sage`, `sage-hi`, `sel-chip`); `dq` and `dq-muted` only for data quality. No red anywhere. `print-*` tokens feed the Typst template only and never follow the app theme. Both themes hold WCAG AA (lowest text pair 4.9:1); there is no separate high-contrast theme (confirm — EXPERIENCE Open item 25).
- UX-DR2: Typography tokens — **IBM Plex Sans** (variable) for everything; IBM Plex Sans Bold Italic only for the 22px wordmark; **IBM Plex Mono** 400 only for IDs, fingerprints, commands and keys. All SIL OFL 1.1, self-hosted (no network at view time; air-gap safe). Nine sizes only — 12 · 13 · 14 · 15 · 17 · 20 · 24 · 30 · 40 — plus the 22px wordmark as the single exception; roles per DESIGN.md (page-title 30/600, headline-number 30/500, group-heading and detail-title 24/600, answer 24/400, inspector-title 20/600, cell-heading 17/600, body and row-title 15, secondary 14, meta, severity-label and mono-id 13, button-label and mono-small 12). Weights 400 / 500 / 600; `tabular-nums` in every data role; sentence case everywhere (uppercase only for button labels, the Graph/Table switch and zoom labels); no eyebrows, kickers or tracked-caps labels.
- UX-DR3: Shape, spacing and elevation tokens — rounded xs 3 / sm (= DEFAULT) 4 / md 6 / lg 10 / pill 999 / full; layout tokens sidebar-width 252, list-width 376 (Issues 500, Reports 420), list-gutter 32, detail cell 30 × 34, row-y 17 (Issues 14, summary rows 12), nav-item-height 54, tab-height 64, button-height 42 (sm 32, wide 54), field-height 42, query-height 44, pager-button 32, table-cell-y 12. **One density only** (no Compact mode or toggle). Depth is flat and tonal (ink → paper → canvas → chip) with 1px `rule` lines, never nested cards; the only shadow is the ⌘K dialog over `scrim`. Disabled controls at 0.45 opacity — the only opacity on elements with text.
- UX-DR4: Theme switch — a Light / Dark segmented control in Settings → Personal and a ⌘K action ("Switch theme…"); no header switcher (the header is gone). Applies instantly with no reload; persisted per user server-side (`user_preferences`, `GET`/`PUT /api/v1/me/preferences`); new users get **Light**. Whether to follow `prefers-color-scheme` is not decided (EXPERIENCE Open item 3) — do not detect OS preference until it is. The printed report never follows the theme.

**App shell & navigation**

- UX-DR5: App shell — black sidebar (`sidebar`, 252px): wordmark; a "Search or jump to… ⌘K" field that opens the palette; seven labelled items **Home · Software · Issues · Exposure · Reports**, a divider, **Settings · Help** (20px icon + label, 54px tall); the user menu at the foot (UX-DR43). The active item mirrors the route (`lime` fill, `ink` text, weight 600); hover `ink-2`. Issues carries the Needs-attention badge (UX-DR38). No top nav and no page header: every surface opens with a page title equal to its sidebar label plus one summary line with key numbers in bold ("Issues" + "3 need attention today. 312 not reviewed yet."). Routes `/`, `/software/<name>`, `/issues`, `/exposure?q=…[&view=table]`, `/reports/<id>`, `/settings/<panel>`. Below 1280px the sidebar becomes an icon rail (UX-DR35).
- UX-DR6: Command palette (`⌘K`/`Ctrl+K`, shadcn `Command`) — every product action invocable; opened from anywhere, from the sidebar search field and from the Exposure query button; a 660px `Dialog` that traps focus, dims the page, never navigates on its own and returns focus on `Esc`; actions include Review, Export, Generate audit report and Switch theme; typing a CVE ID, `package@version` or fingerprint routes to an Exposure answer (a new question on Exposure starts a new trail); any alias of a vulnerability (a CVE ID, a GHSA ID…) finds the same issue and the same answer (ARCH38); results grouped **Issues · Software · Exposure · Actions** with counts, best match first, matched text underlined; `↑`/`↓` move, `↵` open, `esc` close; results announced via polite `aria-live`; no-match copy "No matches. Try a CVE ID, package@version or fingerprint." plus common actions. `?` opens the same dialog on a **Keyboard shortcuts** view that lists every shortcut (no other dialog; UX-DR7). The prior "Recent" group is not drawn (EXPERIENCE Open item 20).
- UX-DR7: Keyboard map — `⌘K`/`Ctrl+K` search or jump; `g` + letter goes to a surface (letters show beside each nav item after pressing `g`; the letters for the renamed surfaces are not yet assigned — EXPERIENCE Open item 13); `J`/`K` next / previous list item; `/` focus the list search; `⌘↵` Save and next in the review panel; `Esc` closes the topmost layer (the palette) or unpins the graph selection; `x` exports the current view; `?` opens the ⌘K palette on its Keyboard shortcuts view (no new modal; Settings → Personal lists the same map); graph: arrows/`Tab` move between nodes, `↵` moves the map to the focused node (UX-DR24), `Backspace` goes back one step, `+`/`−` zoom, Fit; the node's detail opens from the inspector. The prior `t` (triage drawer) and `e` (explore in graph) bindings are retired until new meanings are agreed (Open item 13). Single-key shortcuts (`J`, `K`, `/`, `x`, `?`, `g`+letter, `Backspace` on the map) work only outside text fields and can be turned off in Settings → Personal (WCAG 2.1.4); modified shortcuts stay on. No custom key bindings in v1.

**Components**

- UX-DR8: Retired 2026-11-07 — ux-Armoury-2026-11-06 has no hero numeral, co-stat band or count-up. Home's fleet readings are the summary line, Needs attention, Open issues and the "Across all software" band (UX-DR22).
- UX-DR9: Issue marks — three separate axes, never combined. **Severity** as word + 4-step level marker (Critical 4 bars `clay`, High 3 `amber`, Medium 2 `slate`, Low 1 `forest-ink`; Negligible no bar lit, unlit bars in `slate-dot`; Not rated yet four empty bars with a dashed `text-3` edge; both words in `text-3`), text colour only, no fills, no red. **Actively exploited** (KEV) as quiet clay text with a pulse icon in list rows and palette results, and a `clay-wash` pill in detail panels and the Exposure answer; never dropped when a row truncates; a small grey mono "KEV" tag beside the pill in detail views and technical details only. **Licence** as the neutral `text-2` scale icon + word plus a "Licence" kind tag, never severity-hued; a licence warning (policy treatment "warning") also carries the word "Warning" on line 2, a not-reviewed violation "Needs a decision" (D8). **Review status** as a neutral chip with a drawn icon and its word — Not reviewed yet (open circle), Not impacted (tick), Fix planned (arrow), Mitigated (half-filled circle), Risk accepted (flag) — plus Mixed (UX-DR39). On a selected row every mark switches to `sage-hi` (chips on `sel-chip`). EPSS is never shown as a rating, tag or column; the raw value appears only in the technical-details block.
- UX-DR10: Data quality (FR30) — a small violet reading, never a threat. The value (`dq-value`): score + letter ("91 A−") in `dq`, `dq-muted` for low grades (D and below; the bands are a placeholder until the Story 8.1 model — EXPERIENCE Open item 11); never clay, amber or red, never opacity, never a big numeral in the app; accessible name in full ("Data quality 91 out of 100, grade A−"). The **quality meter** (`quality-meter`): five parts, each out of 100 — Package lists, Coverage, Freshness, Extra sources, Vulnerability records — with only the weakest part emphasised in `dq` and explained in one sentence, with a `forest-ink` link when there is something to do ("See them"); at a low grade the two weakest parts each get a sentence and a grey Check again appears; the technical terms sit on one grey line and in each name's `title` attribute. Placements: Software detail (the Info value and the Data quality cell, UX-DR25), the audit report detail in Reports (a full-width Data quality row with the fleet reading "when it was made", UX-DR27) and the printed cover page (UX-DR46). **Not on Home** (it may join the Home Details tab later — Open item 14) and **never in list rows**. What shows before a score exists is open (Open item 32).
- UX-DR11: Issues list — grouped, not a single ranked table. A **Licences** group at the top (violations and warnings; hidden at 0, while the type filter still shows "Licences 0"), then **Critical · High · Medium · Low · Negligible · Not rated yet** with counts (Negligible and Not rated yet hidden at 0); within each group Actively exploited first, then by raw EPSS (never shown; EXPERIENCE Open item 1); the order stated in words above the list ("Actively exploited sorts first in each group"). One row per issue (UX-DR39) with the review-status chip (or "Mixed · N of M") as the one right column. Filters: the type segmented control All · Vulnerabilities · Licences with counts; the Review status filter listing **Needs attention** (with the Needs-attention count, UX-DR38) above the five statuses with counts, default Not reviewed yet, never mixed with the severity groups; the search "Find a package or vulnerability" (`/`). Long groups end in an "N more High" row; the pager reads "1–25 of 312 · page 1 of 13", 25 per page, never infinite scroll. Row click or `J`/`K` selects and fills the detail column (UX-DR26); the row-level "Explore in graph" is replaced by See exposure / See the map in the detail.
- UX-DR12: Coverage-gap row ("Not checked yet") — sits in the list where the missing rows would be (Software, Exposure list and table, Home band); title + count in `text-3` and one plain sentence naming the count and where ("…including 212 in prod-eu-west. Their issues are unknown, not absent."); no tint, no dashes; not dismissible or collapsible; click-through to cause (unscanned artifacts, unreachable registry, disconnected agent, unmatched running digests).
- UX-DR13: Checking band — an edge-to-edge `paper` band on Software and Home whenever first-check or re-evaluation backlog exists: title "Checking 671 more pieces of software…" with an estimate in words ("about 2 h left"), an 8px determinate bar (`forest-ink` on `forest-wash`) with "3,176 of 3,847 checked (82%)", and "You can keep working: numbers update as each one finishes." Names appear at once and counts fill in; rows show step text ("Reading packages · step 2 of 3", "Waiting its turn"); `chip` skeletons only where data is missing; progress is a polite `role="status"`. Never modal, blocking or a spinner.
- UX-DR14: Retired 2026-11-07 — the stacked severity band is not in ux-Armoury-2026-11-06. Home's **Open issues** summary rows replace it: Licences first (hidden at 0), then Critical with "N actively exploited", High, Medium, Low, Negligible and Not rated yet (the last two hidden at 0), each with its count (UX-DR22). What a click on those rows does is not drawn (EXPERIENCE Open item 18).
- UX-DR15: Freshness strip — one row on `paper` at the bottom of Home's detail column: each source in plain words with its age and the technical term small in `text-3` ("Vulnerability data 41 min ago · Exploited list KEV 6 Nov · Packages 38 min ago · 2 clusters reporting"; every attributed enrichment source per FR12 appears); a stale source turns `amber` with its age in words, an `amber-dot` and a clock; a "Sources" link opens Settings → Sources. Exposure and Software detail carry provenance inline ("Answered 38 min ago", "How we know: Syft v… · Grype DB v… · checked …", "Last checked"); whether the full strip also appears there is open (EXPERIENCE Open item 19), and so is whether end-of-life data (FR33) appears on the strip or only in Settings → Sources (O15).
- UX-DR16: Review panel — in the Issues detail column (Review tab), replacing the slide-over triage drawer; the list stays visible. A scope segmented control comes first: **"All N places"** (default) or **"Only this software"**, which reveals a `Select` of the places and is pre-filled when Review was opened from a piece of software. Question 1, "Does this vulnerability impact us?": **No, not impacted** → Not impacted; **Yes** → question 2, "What will we do?": **Fix it** → Fix planned, **Reduce the risk** → Mitigated, **Accept the risk** → Risk accepted. Each option shows the status chip it produces. "Why? (shown in the audit report)" is required for Not impacted, Mitigated and Risk accepted, and optional for Fix planned (D7). Lime **Save and next ⌘↵** stays disabled until a question is answered; it records status, justification, author, timestamp and scope (FR14), updates the row chip in place ("Mixed" when places now differ) and moves to the next issue in the current filter. Grey **Decide later** moves on without recording. Hint: "Saved with your name in the audit trail." A later all-places decision does not overwrite places with their own status, and the panel says how many keep theirs (decided; ARCH38). A failed save shows the inline error (UX-DR41) and does not advance. The panel ends with the technical-details block (the vulnerability ID and its other aliases, KEV, CVSS, raw EPSS, source, check time). Status never changes inline. Review buttons on Home, the Exposure inspector and Software open the issue in Issues on its Review tab (decided 2026-11-07; the drawn behaviour). Home's **Review all N** opens Issues with the Needs attention filter (UX-DR11), and Save and next walks that set. Not yet drawn but still required: licence-review copy (Open item 16), and vendor VEX claims with attribution plus "the decision that applies now and its source" (FR15; Open item 17). Agree both with UX before the stories that build them. Vendor VEX claims are display-only (decided 2026-11-07): shown in the panel with their source, they never set a status, a count, a filter match or Needs attention until a person records a decision, and emitted VEX states only people's decisions (ARCH38).
- UX-DR17: Exposure graph language — hairline, left to right, four sentence-case tiers with counts: Vulnerability · Package · Software · Where it runs. Circular nodes (`canvas` fill, `forest-ink` or `forest-2` ring); only the vulnerability node takes clay (`clay-wash` fill, `clay-dot` ring, pulse icon when actively exploited). Deployed edges solid `forest-2`; not-deployed edges dashed `slate-dot`, with not-deployed software below a dashed rule labelled "Not deployed" (never colour alone). The selected path is heavier `forest-ink`; the selected node is lime with "Selected on the map". Roll-up text nodes ("8 more", "5 more places") expand; edge labels read like "direct · in 12". Legend, zoom (+ / − / Fit) and the caveat line sit in a footer. Nodes are focusable with an `aria-label` (name + tier + state), and the map has an `aria-label` summarising the answer. Hover or focus highlights the direct path; `Esc` unpins. The moved-map (ego view) visuals are in UX-DR24.
- UX-DR18: Inspector — under the Exposure map (not a side panel), two cells for the selected node: identity (title with version and "Selected on the map"; Name, Fingerprint in mono, Runs in, Copies, How it got it) and "What to do" (The fix, the review-status chip, lime Review, grey Open software); it ends with "How we know: Syft v… · Grype DB v… · checked 38 min ago". On a map centred on a piece of software the identity cell adds Issues ("2 open: 1 Critical, 1 Low"), the lime action is **Open software**, **Show only this** stays grey, and a hint reads "Click any node to move the map to it. Enter does the same from the keyboard." Selection carries across Graph and Table; `Esc` unpins.
- UX-DR19: Signature status (Reports → audit report → Overview, beside Coverage) — **verified:** a `forest-wash` disc with a tick, "Signature verified" and the signer key, then a code block (UX-DR42) with the copyable offline `cosign verify-blob` command ("Auditors can run this themselves, without Armoury."; operator public key by default; the keyless command only when keyless signing is enabled, never when air-gapped). **Does not verify:** an error band in place of the disc, naming the file and the reason ("The signature on pack.pdf does not verify: the file has changed since it was signed.") and linking to the audit-trail entry for the signing; downloads stay available.
- UX-DR20: Audit report generator — one click on lime **Generate audit report** (Reports, ⌘K) with smart defaults (last 12 months, whole fleet); window, scope and framework adjustable after the click, never a wizard before (FR22; how is not drawn — EXPERIENCE Open item 22); the user keeps working and the report appears in Reports → Audit reports when signed (PDF + package lists (SBOM) + review decisions (VEX)); a failure to start shows the inline error (UX-DR41); async progress per section; fails closed naming the failing section; retry re-runs failed sections only.
- UX-DR21: Export — `Export` (and `x`) on Exposure, Issues and Software exports the current view as CSV by default, with JSON as an option (PROC2); on a moved Exposure map it exports the current centre. Every export carries the same caveats and provenance as the screen ("The 2 not checked yet travel with the CSV and the audit report") and is **stored as evidence**: it lands in Reports → Exports with an audit-trail entry (who, when, which view and query) and the same retention as audit reports (24 months, never below the floor); each row says what and where from ("Exposure: log4j-core 2.17.0 · CSV · 14 rows · from Exposure · 6 Nov"). Exposure also offers **"Audit report for this answer"**: the PDF answer report (Story 6.5, UX-DR46 print rules), stored and listed in Reports → Exports like any export. Home has no Export; the posture summary is shared as the audit report. Export is a read action, available to auditors. A failed export shows the inline error (UX-DR41).

**Surfaces**

- UX-DR22: Home surface (`/`; was Posture). List column: "Home" + a scoped summary ("You are in good shape. 3 things need attention today."; it gains a scoped caveat when a source is stale) + "Last checked 38 min ago"; **Needs attention N** (UX-DR38; right column = places); **Open issues N** summary rows (Licences first and hidden at 0, then Critical with "N actively exploited", High, Medium, Low, Negligible and Not rated yet, the last two hidden at 0); "312 not reviewed yet · 782 reviewed · See all" (opens Issues); lime **Review all N** (opens Issues with the Review status filter set to Needs attention; Save and next walks that set, UX-DR11, UX-DR16). Detail column for the selected issue: tabs Overview · Exposure · How to fix · Details (only Overview is drawn; the Exposure tab is a reduced summary of the Exposure page with a button that opens it — Open item 14). Overview holds the title, the first sentence of the advisory description as is, with its source (FR12; no plain-language rewrite; no sentence when there is no description), severity, exploited pill + KEV tag, Vulnerability (the key ID: the CVE ID, else the original ID such as a GHSA ID; ARCH38), Found in, The fix and Review status; grey Review and See exposure; and an Exposure cell (All / Deployed / Not deployed) with "See all N on the map". Below it, a separate "Across all software" `paper` band: Checked gauge ("671 are waiting their turn"), Open issues (30-day sparkline, delta chip) and Audit report (last 12 months, signed, coverage, Download / Preview). **No data-quality reading on Home** (D2). The freshness strip sits at the bottom (UX-DR15). The order within Needs attention is not decided (Open item 21). Every reassuring sentence is scoped to what was checked.
- UX-DR23: Exposure surface (`/exposure?q=…[&view=table]`; was Blast radius and absorbs Graph explorer). A full-width header across list and map: "Exposure" + the question ("Where are we exposed to log4j-core?"), the query button showing the subject (opens ⌘K), the Graph · Table switch, grey Export and "Audit report for this answer". The answer comes first, in words ("14 pieces of software have it. 9 are deployed, 5 are not deployed."), then a meta line (exploited pill, KEV tag, severity, CVSS, "Answered 38 min ago") and deployed/not-deployed split bars. List column: Deployed N, Not deployed N, then the "Not checked yet" row. Graph (UX-DR17) with the inspector (UX-DR18). Table: the same answer in the same order (deployed first), with sortable sentence-case headers (Software, Version, Deployed? Yes/No, Where it runs, Copies, Severity, Review), selection carried across, and "2 not checked yet, not listed". Every partial answer carries its caveat line. Progressive partial results (polled) appear after 2 s with a scope line ("Checking — 1,204 of 3,000 pieces of software so far"). Queries accept a vulnerability ID, `package@version` or a fingerprint; a fingerprint query centres on that piece of software (the prior digest layout). Moving the map is UX-DR24; the no-query, unknown-vulnerability and coverage-scoped-zero states are UX-DR40.
- UX-DR24: Moving around the Exposure map (the prior Graph explorer's traversal, kept inside Exposure; "Explore in graph" and the Graph explorer screen are retired). One rule for every node: **click or `Enter` moves the map to that node** (ego view): the centre sits in the true centre (`forest` disc, `forest-ink` ring, lime inner dot, 28px outer ring, name, version, "Centre of the map" and the fingerprint); what it contains is on the left, where it runs and its copies on the right; the node you came from carries the "Came from here" marker; packages with no known issues roll up ("212 more packages · No known issues") with a caveat line. An **Exposure trail** (`exposure-trail`) sits directly above the moved map: Back, the previous steps as link chips, the current step in bold, key hints "↵ Move the map · ⌫ Back"; Back, `Backspace` (outside text fields), any earlier step or the browser Back returns to that map with its selection. The question, query button, answer line, list column, Export, "Audit report for this answer" and the URL (`&from=` the previous step) follow the centre, so a trail can be shared and reloaded; ⌘K starts a new trail; the Table lists the centre's neighbours. One motion moment: the centre ring scales in once (0.62 → 1, 200 ms), none under reduced motion. The trail is a `nav` named "How you got here" with `aria-current="location"` on the current step; [ASSUMPTION] focus goes to the new centre and the new answer is announced politely (Open item 12). Only a software centre is drawn; package, vulnerability, place and roll-up centres follow the same rule but are not drawn, nor is a long trail or the Table of a moved map (Open item 19). Contextual entry: See exposure, See the map, See all N on the map and Exposure results in ⌘K open Exposure for that subject.
- UX-DR25: Software surface (`/software/<name>`; was Artifacts). "Software" + "3,847 pieces of software. 1,126 deployed, 2,721 not deployed." The real fleet is grouped **Deployed N** (second line "prod-eu-west · 4 copies") and **Not deployed N** (second line "Last deployed 12 days ago" or "Never deployed"; the hint "Not seen running in any connected cluster." shows on hover and focus); the right column is the issue count; then the "Not checked yet" row (UX-DR12), the pager and lime **Add software** (destination not drawn — Open item 18). No data-quality grade in list rows. Detail tabs are Overview · Issues · Packages · Audit trail, with "Deployed" status at the end of the bar. Overview, in this order: (1) **Info** (left): Name, Fingerprint (mono, Copy), Runs in, Copies, **Built**, Last checked, **Data quality** (UX-DR10 value), **Signed** (FR32, D10); grey **Check again** (re-queues the SBOM and scan for this one piece of software) and Audit report; beside it **Packages** ("214 packages · SBOM", Direct / Indirect, a licence line and an **end-of-life** line — FR33, D10) over **Where it runs**; (2) **Issues** full width with Review; (3) the **Issues trend** chart; (4) **Data quality** ("How much you can trust these numbers": the quality meter, UX-DR10); (5) **Latest in the audit trail** ("Entries are never edited or removed"). The words for each signature state and for end-of-life lines other than "No package is past its end of life." are not written (O7, O14); what Data quality shows before a score exists is open (Open item 32).
- UX-DR26: Issues surface (`/issues?review=not-reviewed`; was Findings) — "Issues" + "3 need attention today. 312 not reviewed yet."; the grouped list (UX-DR11) and review panel (UX-DR16) serve vulnerabilities and licences alike (no dedicated licence dashboard). Detail tabs: Review · Exposure · History (Exposure and History are not drawn — EXPERIENCE Open item 15). The Review tab holds the summary (title, severity, pill, KEV), the Exposure count with "See the map", What to do, Review status, the review panel and the technical details.
- UX-DR27: Reports and the audit trail (was Evidence). Reports (`/reports/<id>`) holds exactly three groups — **Audit reports N**, **Exports N** and **Audit trail** (D9) — with lime Generate audit report; any other report type needs a Correct Course. **Audit reports** detail: tabs Overview · Files · Audit trail, with "Generated today, 08:31, by …" in the bar; Overview: title, lead, Download all / Preview; row 1 Coverage when it was made | Signature (UX-DR19); row 2 Data quality, full width ("Data quality 84 B+ when it was made", the fleet quality meter, UX-DR10 — the only place the fleet five-part breakdown appears in the product); then Files (pack.pdf; sboms.tar.gz "Package lists … SBOM"; vex.json "review decisions … VEX") and What it says. **Exports** (UX-DR21): newest first; the detail of a selected export is not drawn (EXPERIENCE Open item 15). **Audit trail** (fleet-wide, D9): ledger entries newest first (type, subject with its plain label and technical ID, actor, time, tool/feed versions), filters by type, subject and time window, the chain verification ("Chain intact — N entries, verified 4 min ago" or the first broken entry), the latest signed checkpoint and the anchoring status (mode, latest anchored checkpoint, pending anchors); the group is not yet drawn (U-edits, O16). The append-only trail also shows per item as tabs (a software's Audit trail, an issue's History, a report's Audit trail): no edit or delete affordances; a correction is a new entry superseding the old, and both stay visible; "Entries are never edited or removed."
- UX-DR28: Settings — a panel list in the list column ([ASSUMPTION], EXPERIENCE Open item 6), one route per panel (`/settings/<panel>`) so links (the freshness strip's "Sources", "Open connection settings") open a panel directly. **Connections**: registry connections (FR1), package feeds (FR29), agent install (copy-paste one-liner in a code block, read-only trust posture and the exact RBAC shown before install). **Sources**: feed status and history, feed-bundle import (FR10), end-of-life data source (FR33). **Policy**: licence policy (FR27), signature policy — trusted keys and keyless identities (FR32), CI policy (Epic 11), evidence retention (the UI never permits below the 24-month floor, FR23). **Access**: users and roles, the read-only resolved auth configuration, CI tokens (Epic 11). **Signals**: Prometheus endpoint URL + metric list, read-only with copy (FR20); signing public key. **Personal**: theme, the keyboard shortcut list and the single-key shortcut switch. Edit controls are absent for roles without write access; OIDC is declarative only, never a UI wizard (NFR6); a save failure shows the inline error (UX-DR41). The panels for FR32 and FR33 are spine-only, like the rest of Settings (see U-edits).

**States**

- UX-DR29: Pre-setup empty Home — the page title plus exactly the two setup actions (connect a registry, install a cluster agent), each with a copy-paste one-liner in a code block (UX-DR42); no illustration. When a registry is unreachable, Software shows an edge-to-edge `clay-wash` error band ("We can't reach registry.acme.internal": since when, what it affects, what still works, likely cause). Its lime **Try again** is the view's one lime action (Add software turns grey), with grey **Open connection settings** → Settings → Connections. Affected rows read "As of 14:02 · registry" in amber with a clock; nothing is removed; Home carries a gap row naming the registry.
- UX-DR30: Degraded states — **stale source:** its age turns `amber` with the age in words, an amber dot and a clock, and the Home summary gains a scoped caveat, so "good shape" is never claimed on old data (reflected in the Freshness part of data quality where it is shown). **Disconnected agent:** "N clusters reporting", and that cluster's runtime data is marked "as of", not removed (heartbeat 30 s, stale after 5 min, disconnected after 60 min, Helm values); air-gapped mode always uses operator-key signing copy (keyless copy never appears), shows bundle age and "import bundle", and has no phone-home affordances.
- UX-DR31: Read-only auditor — Review (the review panel and Review actions), Add software, Generate audit report (and audit-report configuration) and Settings mutations are absent, not disabled; Check again follows its declared minimum role (O4); every read surface, Export, and viewing, downloading and verifying audit reports remain available; the same sidebar, words and numbers as the analyst. Pack generation appears for auditors only when an admin enables `rbac.auditorCanGeneratePacks` (Helm value, default off).
- UX-DR32: Loading/errors — cold load uses shadcn `Skeleton` mirroring the real layout; a failed save or start shows the inline error (UX-DR41) where the action was taken; a failed connection or source shows the error band in the affected view; error copy names the problem in plain words (from the typed envelope `message`) and what still works; never a bare or unexplained spinner, never a toast.

**Voice, accessibility, platform**

- UX-DR33: Voice and vocabulary — calm, plain, honest: counts and verbs, no exclamation marks, no fear, no jargon in primary labels; definitive only when scoped to what was checked; identical words and numbers for leader, analyst and auditor. The plain-language glossary (EXPERIENCE "Glossary: plain label → technical term") replaces the locked glossary: the plain label comes first, with the technical term small and grey beside it, never removed. Pairs: Home (posture), Software (artifact), Issues (findings), Exposure (blast radius), Reports / Audit report (evidence packs; "Audit report for this answer" is the PDF answer report, listed under Exports — D3), Audit trail / History (evidence trail), Vulnerability (CVE), Actively exploited (KEV), Licence, Packages (SBOM components), Direct / Indirect, Deployed / Not deployed (running / shipped, not running), Copies, Where it runs, Fingerprint (image digest), Checked / Not checked yet, Check again, Data quality (data-quality score), Review / Review status (triage). Statuses: Not reviewed yet · Not impacted · Fix planned · Mitigated · Risk accepted (untriaged / not affected / fix planned / mitigated / accepted); Why? (justification). Exports, audit reports and VEX companions keep the technical terms. UI copy is British English ("Licences"). Retired labels never appear in the UI (UX-DR47). Domain, data and API names (artifact, finding, triage, posture, blast radius, evidence pack, KEV, EPSS, VEX, SBOM, `untriaged`) stay unchanged in code, API and docs. All strings are externalised from day 1 (no concatenation, no text in static SVG).
- UX-DR34: Accessibility floor — WCAG 2.2 AA in both themes (no separate high-contrast theme; confirm AA-only — EXPERIENCE Open item 25). (a) Full keyboard operability, with `Tab` order = reading order and a visible 2px focus ring on every interactive element (`focus`; lime on the sidebar and on forest selection); (b) field edges ≥ 3:1 at rest (`field-border`, 1.4.11); (c) reflow and resize (1.4.10, 1.4.4) through the icon rail and stacked layout (UX-DR35) — the Exposure map and wide tables may scroll in two directions while their header, answer and inspector reflow; (d) single-key shortcuts only outside text fields, with an off switch (2.1.4); (e) `aria-current` on selected rows, `aria-pressed` on segmented controls, `aria-current="location"` on the current trail step; (f) the surface is announced on navigation as title + summary; live changes via polite `aria-live` / `role="status"`, errors via `role="alert"`; (g) never colour alone — severity word + marker, exploited word + icon, status word + icon, deployed solid vs dashed plus a label, stale amber + clock + words, data quality always as printed score and letter with the weakest part named in words, and selection changes the text colour; (h) hover hints also available on focus; ⌘K is a real modal dialog (focus trapped, returned on `Esc`); (i) `prefers-reduced-motion` turns all motion off (0.16 s transitions, skeleton pulse, the map's centre-ring scale-in) and progress updates in steps; every graph is fully readable as a table.
- UX-DR35: Responsive/platform — ≥ 1440px is the designed layout; at 1280–1439px the three columns stay and the detail column absorbs the loss; at 1024–1279px the sidebar becomes an **icon rail** (icons only, labels as tooltips on hover and focus and as accessible names, search as a ⌘K icon button, the user menu as the avatar) with list and detail side by side; below 1024px the icon rail stays and list and detail **stack in one column** with a **Back** link (`forest-ink`) that returns to the same place and selection, at the same URL, fully operable (this covers 400% zoom at 1280px and 200% text). No other breakpoints. Web only, last-2-versions evergreen browsers; fonts self-hosted.
- UX-DR36: Banned patterns (enforced across all surfaces) — no in-product notifications or toasts (as alerts or for save results); no badge counts for *new* findings (the Issues Needs-attention badge, UX-DR38, counts what needs a decision and is allowed); no OIDC wizard; no evidence edit/delete (including stored exports); no infinite scroll; no modal deeper than one (the ⌘K dialog is the only modal; no drawers); no hover-only affordances; no celebratory animation; no second lime action in a view (one primary per view plus the active nav item and the agreed lime exceptions; while an error band shows, its recovery action is the one lime button); no red, red fills or severity-coloured backgrounds; no status-coloured chips; no combined risk or EPSS rating; no Compact density or density toggle; no eyebrows, kickers or tracked-caps labels; no nested cards or shadows on in-page elements; no type sizes outside the nine plus the wordmark; no opacity on elements with text except disabled controls at 0.45; no dedicated licence dashboard; no data-quality grade in list rows and no big data-quality numeral in the app; no separate graph-explorer screen.
- UX-DR37: Three-column master-detail — sidebar · list column (`paper`: page title, summary line, filters, grouped list with counts in group headings, pager, then the view's one primary action) · tabbed detail column (`canvas`: 64px tabs with counts, the active tab a forest block, position and keys at the bar's end "1 of 3 · J K"; a grid of cells divided by 1px rules, never cards). **One list-row shape everywhere:** line 1 is name + version (version in `text-3`); line 2 is severity · actively exploited · where; one right column. Click or `J`/`K` selects and fills the detail, and the list keeps its place. Groups too long for the page end in an "N more …" row; 25 per page; never infinite scroll. Segmented controls use one style everywhere. Exposure is the exception: a full-width header spans the list and detail columns.
- UX-DR38: Needs attention and the Issues badge — an issue needs attention when it is Not reviewed yet (in any place) AND it is Actively exploited OR Critical; every licence **violation** issue that is Not reviewed yet also needs attention; licence **warnings** never do (D8). A Mixed issue stays until none of its places is Not reviewed yet. The same number appears on Home ("Needs attention N"), in the Issues summary, as the count of the Issues "Needs attention" filter option (UX-DR11) and as the Issues nav badge (`nav-badge`, lime count on `ink-2`); no badge at 0. The number is always fleet-wide: the Issues type filter and search never change it, including on the filter option. The badge is a count of what needs a decision, not a new-findings notification. The order within Home's Needs attention is not decided (EXPERIENCE Open item 21).
- UX-DR39: Issue unit and Mixed — one Issues row is one vulnerability (or one licence) in one package version across every place it affects ("14 places"). Counts on every surface (not reviewed yet, open, the badge) count issues, not places. The issue-wide status is the latest All places decision, or Not reviewed yet when there is none. When N > 0, the chip reads **Mixed · N of M** (layers icon, neutral; N = places whose own per-artifact decision differs from the issue-wide status, M = the place count; accessible name "Mixed: 3 of 14 places have a different status"; when N equals M the chip reads **Mixed** with no count, accessible name "All M places have their own status"). The Review status filter matches an issue when any of its places has that status, so a Mixed issue can appear under more than one status (decided 2026-11-07). A place's effective status is its own per-artifact decision if present, else the All places decision; VEX states each product's effective status, and chips and filters use it.
- UX-DR40: Exposure query states — **no query** (`/exposure` from the sidebar): "Ask about a vulnerability, a package or a fingerprint." with examples ("CVE-2026-23012 · log4j-core@2.17.0 · sha256:…"), and the query button opens ⌘K. **Unknown vulnerability** (the vulnerability data — Grype DB, the matching database — has no affected-package data for the queried ID or any alias of it, checked with `grype db search --vuln <ID>`; a record without package data counts as unknown, even if the CVE List or another source already lists it): "Armoury has no data for <ID> yet. Vulnerability data updated <age> ago." with lime **Check again** (re-asks against the latest vulnerability data; no rescan); no map, no zero, never "No software has it". **Known vulnerability, no matches:** the coverage-scoped zero ("No software has it — across the 3,176 pieces of software we've checked (82%)"), with the unchecked remainder one click away. Copy for an unknown `package@version` or fingerprint is not written (Open item 29).
- UX-DR41: Inline error — a failed save or start (review panel, Export, Generate audit report, Check again, Settings panels) shows one line in that panel, full width: `clay-wash` fill, a `clay` alert icon, a message in plain words ("Your decision wasn't saved: Armoury can't reach its database."), optional detail in `text-2`, and a grey small **Try again**. Nothing advances or closes; every entered value (choices, scope, "Why?") stays. Announced with `role="alert"`; cleared on a successful retry; never a toast; no border, shadow or red.
- UX-DR42: Code block — a copyable command or one-liner (setup `helm install`, agent install, `cosign verify-blob`, Prometheus endpoint, a CI token shown once, fingerprint): `paper` fill, Plex Mono 12px, and a grey small **Copy** that copies the whole command, never a truncated one. The label changes to "Copied" for 2 s and is announced politely; Copy is keyboard reachable and the text is selectable; long commands scroll horizontally and are never cut off.
- UX-DR43: User menu — at the sidebar foot: a 40px round avatar (`forest-3` → `forest` gradient, `on-forest` initials), the name in `on-ink`, the role in `side-muted`. It opens a `DropdownMenu` with the name and role, **Personal settings** (Settings → Personal) and **Sign out**. `Enter`/`Space` opens it, arrows move, and `Esc` closes it and returns focus. On the icon rail only the avatar shows.
- UX-DR44: Help — the Help item sits in the sidebar below the divider (UX-DR5). The Help screen is not designed and is deferred to a later UX update (EXPERIENCE Open item 24; `?` opens the ⌘K palette's Keyboard shortcuts view, not Help — UX-DR7). No story invents Help content; until that update the item opens a placeholder that says Help is coming (copy to confirm with UX — O17).
- UX-DR45: Zero and empty states — **All clear** (Home): "Nothing needs you today." with the scope sentence ("That covers the 3,176 pieces of software we've checked; 671 are still waiting their turn."), three stats (0 Need attention · N Open, all reviewed · N% Checked), the severity line, grey See open issues, lime Audit report, a `lime-wash` sprout disc, and no Issues badge. **Nothing to review** (Issues filter at 0): "No issues are waiting for review." plus the coverage scope and grey **Show all statuses**. **Search no match:** "No issues match “<text>” with these filters." with grey **Clear search**, keeping the filters. **Reports, nothing yet:** "No audit reports yet" with lime Generate audit report; Exports: "No exports yet. Make one from Exposure, Issues or Software with Export." **Licences 0:** the group is hidden, and the type filter still shows "Licences 0".
- UX-DR46: Printed report (audit report PDF via Typst, the answer report and printed exports) — a print-only light palette (`print-*` tokens) independent of the app theme; IBM Plex Sans text ([ASSUMPTION], EXPERIENCE Open item 5) and IBM Plex Mono for every ID, fingerprint and command; body 9.5pt, tables 8.5pt; A4 by default with US Letter as an option. The audit report's cover sheet comes first and states coverage ("Covers 3,176 of 3,847 (82%)"), listing the not-checked software; then the **data-quality block** (`print-cover-dq`: "84 B+" at 30px with the letter at 20px in `print-dq` — the only big data-quality numeral anywhere; the five parts with plain names and the technical term beside each; "Lowest part: …"); then Signature (operator key and the `cosign verify-blob` line) and a sign-off line (name and role, date). Every page has a footer with report ID, time window, generation time and page number. Severity always shows as word + 4-step marker, with no red. Long tables repeat their header row. Plain labels carry the technical term beside them; the companions (SBOM, VEX) keep technical names. Preview is available in the product before download.
- UX-DR47: Retired UI labels — these never appear in UI strings: Posture, Findings, Blast radius, Graph explorer, Artifacts, Evidence, triage, Things to look at, Where it's affected, Weakness, ingredients, What's inside, Chosen by your team, Came along with them, Running (as a group or status label; the hint "Not seen running…" is allowed — EXPERIENCE Open item 35), Shipped not running, Undeployed, Being attacked in the wild, chance of attack, Doesn't affect us, Fixed for now, Workaround in place, Mark reviewed, Plan the fix, Skip. They are checked against the externalised message catalogue; code, API and docs may keep the domain terms (UX-DR33).
- UX-DR48: CI-scan landing (FR31) — the link the CI step prints opens that piece of software in Software. Not decided (EXPERIENCE Open item 28): how CI-submitted software that is in no connected registry is grouped (it fits neither Deployed nor Not deployed), the label that says where it came from, and where the CI verdict and its history show in Software detail. Resolve with a UX update before the Epic 11 UI work; CI policy and CI tokens live in Settings → Policy and Settings → Access (UX-DR28).

### FR Coverage Map

FR1: Epic 2 - Registry connection and enumeration
FR2: Epic 2 - Central Syft SBOM generation
FR3: Epic 3 - Live cluster inventory via read-only agent
FR4: Epic 3 - Shipped-vs-running reconciliation
FR5: Epic 2 (registry/scan gaps) + Epic 3 (agent and unmatched-digest gaps) - Coverage visibility
FR6: Epic 2 - Uniform fleet-wide Grype scanning
FR7: Epic 4 - Feed-driven re-evaluation (feed-delta join)
FR8: Epic 2 (scan time, tool versions) + Epic 4 (feed versions) - Evaluation provenance
FR9: Epic 2 - Continuous onboarding within 1 hour
FR10: Epic 4 - Signed offline feed bundles (air gap)
FR11: Epic 4 - Multi-source enrichment (KEV, EPSS, CNA, OSV)
FR12: Epic 4 - Enrichment source attribution
FR13: Epic 5 - Deterministic, explainable ordering: severity groups (Licences first), actively exploited (KEV) first in each, EPSS next, stated in words
FR14: Epic 5 - Triage decisions as first-class data
FR15: Epic 5 - VEX ingest and emit
FR16: Epic 2 - Fleet posture view (UI: Home; extended by Epics 5, 8)
FR17: Epic 6 - Blast-radius query with provenance (UI: Exposure, including moving the map)
FR18: Epic 2 - Artifact detail (UI: Software detail; extended by Epics 3, 4, 5, 7, 8)
FR19: Epic 6 - Shareable answers (CSV/JSON export from Exposure, Issues and Software, the PDF answer report; all stored as evidence in Reports → Exports)
FR20: Epic 8 - Prometheus metrics (pull-only)
FR21: Epic 9 - CRA compliance pack
FR22: Epic 9 - Pack architecture (framework-extensible)
FR23: Epic 9 - Continuous evidence, on-demand generation, retention floor
FR24: Epic 9 - PDF + machine-readable companions
FR25: Epic 9 - Signed evidence packs (keyless / operator key)
FR26: Epic 7 - Grant license evaluation
FR27: Epic 7 - Fleet license policy as findings
FR28: Epic 9 - License section in evidence packs
FR29: Epic 2 - Package feed connection
FR30: Epic 8 (score, Software detail) + Epic 9 (audit report detail, cover page) - Data-quality score
FR31: Epic 11 - Optional CI scan with server-side evaluation and result URL
FR32: Epic 4 - Artifact signature verification against trusted signers (UI: Software detail "Signed")
FR33: Epic 4 - End-of-life data for packages (UI: Software detail Packages)

**NFR placement:** NFR1 E2 (gate checked again at E3) · NFR2 E6 · NFR3 load tests in E2/E4/E6 · NFR4 E1 (install), E4 (air-gapped feeds), E10 (end-to-end proof) · NFR5 E4 · NFR6 E1 · NFR7 E10 · NFR8 E2/E3/E4/E8 · NFR9 E3 · NFR10 E1 (durable volumes) · NFR11 E2 (ledger, history tables), E5 (superseding decisions), E9 (sealed packs) · NFR12 E2 (central pipeline), E3 (agent reports digests only), E7 (Grant on server), E11 (CI scan).

## Epic List

Order follows the user journeys: UJ-1 (Epics 1–3), UJ-2 (Epics 4–6), UJ-3 (Epic 9). Each epic builds only on earlier epics. Epic 1 Story 1 is the scaffold; Agent Readiness (Linear INF-12) runs after it and before any further story starts Build (PROC1).

### Epic 1: Install, sign in, and the Armoury shell
A SecOps engineer installs the control plane with one `helm install`, signs in with the bootstrap admin (OIDC and the three roles optional via Helm values), and lands in the Armoury shell — labelled black sidebar, ⌘K command palette, Light (default) and Dark themes — on an empty Home page offering the two setup actions.
**FRs covered:** none (NFR-only delivery epic for the UJ-1 install/sign-in path) — NFR4, NFR6, NFR10; ARCH1, ARCH4 (queue proof), ARCH12, ARCH13, ARCH16, ARCH22, ARCH23 (ci.yml, build.yml), ARCH34; PROC3; UX-DR1–7, UX-DR29, UX-DR31–37, UX-DR41–44, UX-DR47.

### Epic 2: Fleet inventory and uniform scanning, shown as a populating posture view
The engineer connects a registry or package feed and watches Armoury enumerate, SBOM and scan the fleet with one Grype config, every scan recorded as evidence, while Home and Software fill in live under the Checking band, with gaps shown openly as "Not checked yet" rows (minute 29, registry-side).
**FRs covered:** FR1, FR2, FR5 (registry/scan gaps), FR6, FR8 (scan time, tool versions), FR9, FR16, FR18, FR29 — NFR1, NFR3, NFR8, NFR11 (ledger, history), NFR12; ARCH2–5, ARCH7, ARCH14, ARCH15, ARCH17, ARCH28 (R11), ARCH31, ARCH32, ARCH35, ARCH38 (Needs attention count); UX-DR9, UX-DR12, UX-DR13, UX-DR15, UX-DR22, UX-DR25, UX-DR38.

### Epic 3: Running inventory from read-only cluster agents
The engineer installs the agent with a second one-liner; running workloads appear linked to registry artifacts, so Software splits into Deployed and Not deployed and "is this running anywhere?" is answerable; disconnected agents and unmatched running digests surface as gaps.
**FRs covered:** FR3, FR4, FR5 (agent and unmatched-digest gaps) — NFR8, NFR9; ARCH8–11. First story closes the enrollment gap (ARCH10).

### Epic 4: Fresh, enriched findings, connected or air-gapped
When vulnerability or enrichment feeds update — online or by signed offline bundle — stored SBOMs are re-evaluated within an hour without rescans, and every finding carries source-attributed KEV, EPSS, CNA and OSV data. Packages carry attributed end-of-life data, and registry artifacts are checked against trusted signers — both connected or air-gapped.
**FRs covered:** FR7, FR8 (feed versions), FR10, FR11, FR12, FR32, FR33 — NFR4, NFR5, NFR12; ARCH6, ARCH19–21, ARCH28 (R2), ARCH40, ARCH41; UX-DR15, UX-DR25 (Signed, end-of-life lines), UX-DR28 (Sources, Policy).

### Epic 5: Prioritise and triage findings
The analyst works the Issues list — Licences (hidden at 0), then Critical, High, Medium, Low, Negligible and Not rated yet (the last two hidden at 0), actively exploited first in each group, the order stated in words — and reviews each issue in the detail-column review panel (two questions; scope All N places or Only this software; a reason where required). Decisions are recorded with author and time, propagate everywhere and feed Home's Needs attention and the Issues badge; the fleet-wide audit trail is readable in Reports; Armoury ingests and emits VEX.
**FRs covered:** FR13, FR14, FR15 — NFR11 (superseding decisions); UX-DR11, UX-DR16, UX-DR26, UX-DR27 (Audit trail group, per-item tabs), UX-DR38, UX-DR39, UX-DR45 (All clear, Nothing to review, Search no match); ARCH38; ARCH29 (ranking formula, VEX formats).

### Epic 6: Blast radius and graph exploration
On CVE day the engineer types a CVE ID, `package@version` or fingerprint into ⌘K, and within seconds Exposure answers in words — which software has it, deployed and not deployed, and where it runs — then as a map or a table with its caveat line and "How we know". She exports it (stored as evidence in Reports → Exports) and moves the map to any node to follow it further. The Epic 6 title keeps its domain wording.
**FRs covered:** FR17, FR19 — NFR2; UX-DR17, UX-DR18, UX-DR21, UX-DR23, UX-DR24, UX-DR40, UX-DR45 (Exports nothing yet), UX-DR46 (renderer); ARCH39; ARCH28 (R1).

### Epic 7: License compliance
Grant evaluates every artifact against a fleet allow/deny policy; violations and warnings appear as neutral Licence issues — the Licences group at the top of Issues and of Home's Open issues (hidden at 0), with a "Licence" kind tag (and the word "Warning" for warnings), and in a software's Packages and Issues — and are reviewed with the same decision model; only violations count toward Needs attention (licence review copy not yet drawn — EXPERIENCE Open item 16).
**FRs covered:** FR26, FR27; UX-DR9 (licence marker, "Warning"), UX-DR11 (Licences group), UX-DR38 (violations only).

### Epic 8: Fleet signals — Prometheus metrics and data quality
The team's own Grafana alerts on new KEV findings, coverage gaps, stale feeds and agent health; every piece of software and the fleet get an explainable data-quality score, shown in Software detail (Epic 8) and in audit reports (Epic 9); not on Home and not in list rows.
**FRs covered:** FR20, FR30 — NFR8; UX-DR10, UX-DR28 (Signals panel), UX-DR42 (endpoint copy); ARCH24; ARCH29 (DQ scoring model, first story).

### Epic 9: Signed CRA evidence packs
The compliance lead generates a CRA pack (an "audit report" in the UI) in one click from Reports for any past window — PDF plus package lists (SBOM) and review decisions (VEX), with its own coverage stated first and its data quality second, on screen and on the cover page, signed and verifiable offline — with retention never below 24 months.
**FRs covered:** FR21, FR22, FR23, FR24, FR25, FR28 — NFR11; ARCH18, ARCH30 (signed checkpoints and archive), ARCH37 (optional Rekor anchoring); UX-DR10 (Reports row, cover), UX-DR19, UX-DR20, UX-DR27 (Audit reports; checkpoint and anchoring status in the Audit trail group), UX-DR42, UX-DR45 (Reports nothing yet), UX-DR46.

### Epic 10: Verifiable, air-gapped delivery of Armoury itself
Buyers can verify Armoury's own images, charts and feed bundles (cosign + SLSA provenance) and run the whole product end to end with no internet access.
**FRs covered:** none (NFR-only) — NFR4 (end-to-end proof), NFR7; ARCH19 (outbound boundary check), ARCH23 (release.yml).

### Epic 11: Scan in CI and see the result in Armoury
A developer adds one optional step to a pipeline. The step submits the built artifact to Armoury; the server SBOMs, scans and license-checks it with the fleet toolchain, applies the fleet CI policy, and the step prints the verdict and a link to the artifact (that piece of software in Software; its grouping and verdict display are open — UX-DR48). Central scanning needs no CI change; this epic adds a faster, earlier path. Builds on Epics 2, 4, 5, 6, 7 and 10 (scan pipeline, KEV enrichment, triage decisions, the long-operation pattern from Story 6.2, license results, the release workflow from Story 10.1); numbered 11 so the published keys of Epics 3–10 stay stable.
**FRs covered:** FR31 — NFR6 (CI tokens), NFR12; ARCH31, ARCH33, ARCH36; UX-DR28 (CI policy, CI tokens), UX-DR42, UX-DR48.

## Epic 1: Install, sign in, and the Armoury shell

A SecOps engineer installs the control plane with one `helm install`, signs in with the bootstrap admin (OIDC and the three roles optional via Helm values), and lands in the Armoury shell — labelled black sidebar, command palette, Light and Dark themes — on an empty Home page. Story 1.1 is readiness-enabling work: Agent Readiness (INF-12) runs after it and must be ready before Stories 1.2+ start Build (PROC1).

### Story 1.1: Monorepo scaffold with an aggregate local gate and CI

As the Armoury developer,
I want the agreed monorepo scaffolded with one local check command mirrored in CI,
So that every later story — and Agent Readiness — has a real codebase, toolchain and feedback loop to build on.

**Acceptance Criteria:**

**Given** a fresh clone
**When** the developer runs the documented init/check task (`mise run check`)
**Then** a Cargo workspace (resolver 3, Rust 2024) builds `control-plane` (binary `armoury`), `agent` (binary `armoury-agent`) and `agent-proto` (tonic/prost codegen from `proto/agent/v1/agent.proto`) (ARCH1)
**And** `web/` is a SvelteKit app with Tailwind v4, shadcn-svelte initialised, `@xyflow/svelte` installed, `adapter-static` and SSR disabled in the root layout
**And** `charts/armoury` exists as an umbrella chart with `control-plane` and `agent` subcharts, `api/openapi.yaml` exists, `mise.toml` pins every tool and `mise-tasks/` holds the tasks as mise file tasks (ARCH1)
**And** tool and dependency versions are pinned (lockfiles committed; no floating `latest`).

**Given** the scaffold
**When** `mise run check` runs
**Then** it executes rustfmt check, `clippy -D warnings`, `cargo nextest` (including `#[sqlx::test]` against `apache/age:release_PG18_1.8.0`, pinned by digest), web lint, `svelte-check` and Vitest, and fails non-zero on any failure (ARCH23, ARCH27)
**And** each Rust binary, the web app and the chart contain at least one trivial passing test or lint target so every check has something real to run.

**Given** `api/openapi.yaml`
**When** `mise run gen:api` runs
**Then** it generates the Rust server types with `openapi-generator` (run from its pinned container image, no local Java) and the TS client with `openapi-typescript` + `openapi-fetch` (ARCH12)
**And** `mise run check` fails if the generated code differs from the committed code.

**Given** the repository
**When** the images are built
**Then** multi-stage Dockerfiles build the control-plane image (`armoury` binary plus the SPA build) and the agent image (`armoury-agent` only, no scanner tools), with base images pinned by digest (ARCH34).
**And** the dev loop uses a debug build profile and a cached dependency layer (for example `cargo-chef`), so a code change redeploys without a full dependency rebuild; a `ponytail:` comment records the ceiling (slow Rust rebuilds) and the upgrade path (a remote build cache).

**Given** a developer workstation with mise and access to the dev cluster (kube context, in-cluster BuildKit, dev registry)
**When** `mise run dev` runs
**Then** Skaffold builds both images on the in-cluster BuildKit, pushes them to the dev registry, deploys the chart to the developer's namespace with the images as `repo:tag@digest`, port-forwards the UI and API to `localhost:8080`, and redeploys after a code change (ARCH34, PROC3)
**And** no image build, database or cluster runs on the workstation.

**Given** the Skaffold deployment
**When** `mise run e2e` runs
**Then** a Playwright smoke test loads the web app from it and passes; CI runs the same task.

**Given** a push or pull request
**When** `.github/workflows/ci.yml` runs
**Then** it installs mise with `jdx/mise-action` (pinned by commit), runs the fast tier on GitHub-hosted runners for every event, and runs the full `mise run check` gate and `mise run e2e` on ARC runners in the dev cluster for pushes and same-repository pull requests; a fork pull request never reaches an ARC runner, and a required gate job fails unless every tier passed (ARCH23).

**Given** a push
**When** `.github/workflows/build.yml` runs
**Then** it builds both images on the in-cluster BuildKit from an ARC runner and packages the chart; on `main` it pushes them to GHCR (`ghcr.io`) by digest (ARCH23, ARCH34).

**Given** the repository root
**When** an agent or developer opens it
**Then** `AGENTS.md` (no `CLAUDE.md`) states the Locality of Behaviour rules and layout from the architecture (ARCH25) and PROC3 (keep `mise run dev` running during every development step), and `README.md` documents the init, check, e2e and dev-loop commands and the dev-cluster prerequisites.

### Story 1.2: Install the control plane with one Helm command, durable storage included

As a SecOps engineer,
I want to install Armoury into my existing cluster with one `helm install`,
So that I get a running control plane without tickets to the platform team.

**Acceptance Criteria:**

**Given** a Kubernetes cluster where the engineer has Helm rights
**When** they run the documented one-line `helm install` with default values
**Then** the control plane, bundled Postgres with Apache AGE and bundled SeaweedFS start, Postgres and SeaweedFS on persistent volumes (NFR10, ARCH2, ARCH3, ARCH22)
**And** a migration Job (`armoury migrate`, same image, Helm post-install and pre-upgrade hook, so the bundled database and its logins exist first) runs as `armoury_owner`: it runs the River migrations (`riverqueue-migrate`) and then forward-only `sqlx` migrations, creates the AGE graph, grants `armoury_app` its rights, and, from Story 2.1 onward, creates monthly partitions 3 months ahead; it retries the database connection for up to 10 minutes, so it can start before the bundled Postgres accepts connections; the control plane starts as `armoury_app` and reports not ready until the schema version is at least its expected version, then ready on a health endpoint
**And** a fresh `helm install` with the bundled database succeeds with one command, proven by the Story 1.2 install test; the documented one-liner does not use `--wait` or `--atomic`, because Helm then runs the post-install hook only after the not-ready control plane is ready
**And** for the bundled database the chart creates both logins (`armoury_owner`, `armoury_app`) and the AGE extension, with passwords in two Secrets; the control-plane pod mounts only the `armoury_app` Secret
**And** the bundled database is `apache/age:release_PG18_1.8.0`, pinned by digest (ARCH2).

**Given** the Skaffold `ci` profile from Story 1.1
**When** it deploys the chart into a fresh, uniquely named namespace of the dev cluster (from an ARC runner in CI, or with `mise run` locally)
**Then** the install, durability and same-origin checks in this story run against that deployment, so they exercise the built images, not placeholders, and the namespace is deleted afterwards (ARCH34).

**Given** the job queue (`riverqueue =0.5.0`, ARCH4)
**When** a test enqueues a job inside a database transaction and commits
**Then** a worker runs the job, and a job enqueued in a rolled-back transaction never runs
**And** if this cannot be made to pass, the queue switches to the fallback `graphile_worker` in this story, before any later story depends on it.

**Given** values that point at an external Postgres-AGE and an external S3 endpoint
**When** the chart is installed
**Then** the bundled database/object store are not deployed and the control plane uses the external ones
**And** the external database needs two logins (an owner that can create schemas, and an application login) and the AGE extension installed once by a database administrator; the chart documentation states the exact rights, confirmed in this story, and the migration Job fails with a clear message when one is missing.

**Given** the control plane pod is deleted and rescheduled
**When** it starts again
**Then** previously stored data is still present (durability check, NFR10).

**Given** the install with `airGapped: true`
**When** the control plane runs
**Then** it makes no outbound network connections (verified by a network-policy or egress-capture test, in a namespace of the dev cluster whose CNI enforces NetworkPolicy egress rules), and the air-gap mode is exposed read-only via the API (NFR4, ARCH19).

**Given** the control plane is running
**When** a browser requests `/`
**Then** the control plane serves the static SPA build and `/api/v1/*` from the same origin.

**Given** the chart values
**When** the chart is rendered
**Then** the control plane has a separate agent port with its own Service, exposed as `LoadBalancer` (default) or `NodePort`, or through an ingress with TLS passthrough (PROC2, ARCH8)
**And** the chart documentation states that an ingress that ends TLS is not supported for the agent port, because the control plane ends mTLS itself (the listener arrives in Story 3.1).

### Story 1.3: Sign in with the bootstrap admin

As a SecOps engineer installing Armoury,
I want to sign in with a bootstrap admin set in my Helm values,
So that SSO never stands between me and a working posture view.

**Acceptance Criteria:**

**Given** a bootstrap admin credential supplied through Helm values / a referenced k8s Secret
**When** the user signs in with it on the sign-in page
**Then** an httpOnly, Secure, SameSite session cookie is issued and the user lands in the app as admin (NFR6, ARCH16)
**And** no token is stored in JavaScript-accessible storage.

**Given** wrong credentials
**When** the user signs in
**Then** sign-in fails with a generic message, the attempt is logged without the credential, and repeated failures are rate-limited: after 5 failed sign-ins for one username in 15 min, sign-in for that username is blocked for 15 min, and each source IP address can try 20 times in 15 min (Helm values, PROC2).

**Given** no session
**When** any `/api/v1/*` endpoint other than sign-in/health is called
**Then** it returns 401 with the uniform `{error:{code,message,details}}` envelope (ARCH13).

**Given** a signed-in user
**When** they sign out
**Then** the session is invalidated server-side and the cookie cleared.

**Given** the session store
**When** a session is created
**Then** it is a row in the PostgreSQL `sessions` table that stores only a hash of the random session ID held in the cookie; sessions survive a control-plane restart; sign-out deletes the row (ARCH16)
**And** the idle timeout and maximum lifetime come from Helm values (defaults 8 h idle, 24 h maximum, PROC2), and an expired session returns 401

**Given** the install output / chart NOTES
**When** the install completes
**Then** it tells the user how to retrieve the bootstrap credential, without printing a secret into logs.

### Story 1.4: Declarative OIDC sign-in and role-based access

As an admin,
I want OIDC SSO and role mapping configured purely through Helm values,
So that my team signs in with company identity and each person gets only the access their role allows.

**Acceptance Criteria:**

**Given** OIDC issuer, client and role-claim mapping set in Helm values
**When** a user signs in via the OIDC code flow
**Then** they get a cookie session with the role mapped from their claims: admin, analyst or auditor (NFR6, ARCH16)
**And** a user whose claims map to no role is denied with a clear message, not given a default role.

**Given** OIDC values are absent
**When** the chart is installed
**Then** install succeeds and only bootstrap-admin sign-in is offered — OIDC never blocks the install path.

**Given** the IdP is unreachable
**When** the bootstrap admin signs in
**Then** sign-in still succeeds (IdP-outage recovery).

**Given** RBAC middleware
**When** an auditor or analyst calls an endpoint above their role
**Then** the API returns 403 with the error envelope, enforced server-side for every route
**And** every operation in `openapi.yaml` declares `x-armoury-role: admin | analyst | auditor`, which the middleware reads; a spec test fails on any operation without it (ARCH12)
**And** a route test calls every route with every role and expects 403 below the declared role and no 403 at or above it
**And** the middleware supports `x-armoury-role-setting: <setting>`: when the named setting is `true`, the route also accepts the next lower role; the route test calls such a route with both setting values (a test-only route proves it here; Story 9.5 adds the pack route)
**And** the middleware supports CI tokens (`Authorization: Bearer`): the route test adds a "CI token" caller that succeeds only on routes marked `x-armoury-ci-token: true` and gets 403 on every other route; this story proves it with a test-only marked route, and Story 11.1 adds the real CI routes, which the same test then covers.

**Given** any role
**When** `GET /api/v1/auth/config` is called
**Then** it returns the resolved auth configuration with secrets redacted; there is no API to change it (no UI wizard).

### Story 1.5: Design tokens and the Light and Dark themes

As a SecOps engineer,
I want the Light (default) and Dark themes with Armoury's typography (IBM Plex Sans and IBM Plex Mono),
So that the product looks calm and like itself from the first screen, in either theme.

**Acceptance Criteria:**

**Given** the web app
**When** it renders
**Then** semantic colour tokens map onto shadcn-svelte CSS variables with the exact DESIGN.md values for Light (unsuffixed keys) and Dark (`-dark` keys), following the DESIGN.md "shadcn mapping" table — including the sidebar (`ink`, `ink-2`, `ink-line`, `side-text`, `side-muted`, `on-ink`), `lime*`, `forest*`, the severity roles (`clay`, `amber`, `slate`, `forest-ink`) and `field-border` — plus `--paper`, `--dq`, `--dq-muted` and `--dq-wash` as extra variables; the `print-*` tokens feed only the Typst template (UX-DR1)
**And** a lint/test fails if any component references a raw hex or a theme-suffixed variable instead of a semantic role.

**Given** typography, shape and spacing tokens
**When** components use them
**Then** IBM Plex Sans (variable 100–700), IBM Plex Sans Bold Italic (wordmark only) and IBM Plex Mono 400 (IDs, fingerprints, commands, keys only) are bundled locally (SIL OFL 1.1, no CDN; works air-gapped); only the nine sizes 12 · 13 · 14 · 15 · 17 · 20 · 24 · 30 · 40 are used, plus the 22px wordmark as the single exception; weights are 400 / 500 / 600; numerals use `tabular-nums` in every data role; a lint fails on any other size or a third family (UX-DR2, UX-DR3, NFR4)
**And** radii (xs 3, sm 4, md 6, lg 10, pill, full) and the layout tokens (sidebar 252, list column 376 / 500 / 420, list gutter 32, detail cell 30 × 34, row padding 17 / 14 / 12, nav item 54, tab 64, button 42 / 32 / 54, field 42, query 44, pager 32) match DESIGN.md; there is one density only.

**Given** a signed-in user
**When** their theme preference is set through `PUT /api/v1/me/preferences`
**Then** the web app applies it instantly without reload, it persists per user in the `user_preferences` table (keyed by OIDC issuer + `sub`, or the fixed bootstrap-admin ID) and follows them to another browser; every role can change its own preference; new users get Light; no OS-preference detection ([ASSUMPTION], EXPERIENCE Open item 3) (UX-DR4); the same preferences also hold the single-key shortcut switch (Story 1.8); the picker arrives in Story 1.6
**And** an automated contrast check confirms AA (4.5:1) for every text pair in the DESIGN.md Contrast table in Light and Dark (lowest 4.9:1), including the selection pairs on `forest`, text on `lime`, and `dq` / `dq-muted` on canvas, paper, chip and `dq-wash`, and ≥3:1 for `field-border` against canvas, paper and chip and for the focus ring; markers below 3:1 (`amber-dot`, `slate-dot`, the dark `forest` fill) are allowed only beside a word
**And** a lint/test fails if a component applies opacity below 1 to an element that contains text, except disabled controls at 0.45 (DESIGN.md); quieter states use `text-2` / `text-3`, and low data-quality grades use `dq-muted`.

### Story 1.6: App shell, sidebar navigation and the empty Home page

As a SecOps engineer,
I want a consistent shell with a labelled sidebar and an honest empty Home page,
So that I can move between surfaces and immediately see what Armoury is waiting for.

**Acceptance Criteria:**

**Given** a signed-in user
**When** the app loads
**Then** a 252px black sidebar shows the wordmark, the "Search or jump to… ⌘K" field, the nav Home · Software · Issues · Exposure · Reports, a divider, then Settings · Help (20px icon + label, 54px items), with the active item lime (ink text, weight 600) mirroring the route, and the user menu at the foot; there is no top nav and no page header (UX-DR5, UX-DR43)
**And** every surface uses the three-column master-detail layout (sidebar · list column · tabbed detail column) with the page title equal to the sidebar label and one summary line under it (UX-DR37); surfaces without content yet show a calm "nothing here yet" line — no eyebrow, heading block, accent rule or illustration
**And** the user menu shows the signed-in name and role and opens Personal settings (Settings → Personal) and Sign out (Story 1.3); `Enter`/`Space` opens it, arrows move, and `Esc` closes it and returns focus; Help opens a placeholder until its screen is designed (EXPERIENCE Open item 24, O17) (UX-DR4, UX-DR5, UX-DR43, UX-DR44).

**Given** nothing is connected
**When** Home loads
**Then** it shows the title "Home" and states that no sources are connected yet (UX-DR29 base; setup actions arrive with Stories 2.2 and 3.2).

**Given** Settings
**When** it opens
**Then** it shows a panel list in the list column, grouped as Connections, Sources, Policy, Access, Signals and Personal, each panel on its own route `/settings/<panel>` (UX-DR28)
**And** this story fills Settings → Personal (the Light / Dark theme switch, which applies instantly and persists, Story 1.5; the keyboard shortcut list and the switch that turns single-key shortcuts off, wired in Story 1.8) and Settings → Access (the read-only resolved auth configuration and the users/roles view); later stories add their panels to the same list.

**Given** an auditor session
**When** any surface renders
**Then** mutation controls are absent from the DOM rather than disabled (UX-DR31), proven by a component test.

**Given** the web app structure
**When** the shell is built
**Then** server state uses TanStack `svelte-query` over the generated TS client, local state uses Svelte 5 runes, surface components live with their routes, and only shared shadcn-svelte primitives live in `lib/components/ui` (ARCH26, ARCH12).

**Given** a slow or failing API
**When** a surface loads
**Then** a layout-mirroring `Skeleton` appears during the cold load and errors render the envelope `message` — never a bare spinner (UX-DR32).

### Story 1.7: Accessibility, message catalogue and responsive baseline

As a SecOps engineer (and as the compliance buyer who requires WCAG 2.2 AA),
I want the shell to be accessible, keyboard-operable and consistently worded from day one,
So that every later surface inherits a floor it cannot silently drop below.

**Acceptance Criteria:**

**Given** the shell from Story 1.6
**When** automated accessibility checks (axe, through the Playwright setup from Story 1.1) run in `mise run e2e` and CI
**Then** there are no WCAG 2.2 AA violations on any shell route, and a newly introduced violation fails the gate (UX-DR34)
**And** the check is wired so later stories' routes are included automatically, not opt-in.

**Given** keyboard-only use
**When** the user tabs through the shell
**Then** every control is reachable with a visible focus ring, tab order follows reading order, and no affordance is hover-only; selected rows use `aria-current`, segmented controls use `aria-pressed`, and field edges meet 3:1 at rest (UX-DR34, UX-DR36).

**Given** navigation between surfaces
**When** the route changes
**Then** a polite `aria-live` region announces the surface by title and summary ("Issues — 3 need attention today").

**Given** `prefers-reduced-motion: reduce`
**When** any transition would run
**Then** it is suppressed or reduced globally, via one shared motion setting rather than per-component checks; normal motion is quiet (0.16 s colour and background transitions, skeleton pulse) and progress updates in steps when reduced.

**Given** UI copy
**When** a component renders text
**Then** the string comes from an externalised message catalogue, with no concatenated sentences and no text baked into SVG; a lint/test fails on hard-coded user-facing strings in components (UX-DR33)
**And** the plain-label glossary (EXPERIENCE Glossary) and the five review-status labels — Not reviewed yet, Not impacted, Fix planned, Mitigated, Risk accepted — are defined once in the catalogue; UI copy is British English ("Licences"); a lint/test fails on any retired label from UX-DR47, with "Running" banned only as a group or status label (EXPERIENCE Open item 35).

**Given** viewport widths ≥ 1280px, 1024–1279px and < 1024px
**When** the shell renders
**Then** it shows respectively: the full sidebar with three columns; the icon rail (icons only, labels as tooltips on hover and focus and as accessible names, the search field as a ⌘K icon button, the user menu as the avatar) with list and detail side by side; and the icon rail with list and detail stacked in one column, where opening an item shows its detail with a Back link that returns to the list at the same place and selection, at the same URL — every layout fully operable (UX-DR35)
**And** a Playwright test checks every shell route at 1440, 1100 and 900 px wide, at 320 CSS px (400% zoom at 1280) and with 200% text: there is no horizontal page scroll (only the Exposure map and wide tables scroll inside their own area), and every control is visible and reachable by keyboard.

### Story 1.8: Command palette and keyboard map

As a SecOps engineer working under pressure,
I want every action reachable from `⌘K` and the keyboard,
So that I never hunt through menus.

**Acceptance Criteria:**

**Given** any surface
**When** the user presses `⌘K` / `Ctrl+K`
**Then** the shadcn `Command` palette opens as a 660px dialog with results grouped Issues · Software · Exposure · Actions (first result = best match); `↵` opens, `Esc` closes and returns focus; it traps focus, dims the page and never navigates on its own; results announce via polite `aria-live` (UX-DR6); a Recent group is not drawn (EXPERIENCE Open item 20)
**And** it offers navigation to every surface and "Switch theme…" (Light / Dark)
**And** the sidebar "Search or jump to…" field (Story 1.6) opens the same palette; typing a CVE ID, `package@version` or fingerprint routes to an Exposure answer once Story 6.3 lands; until then it shows the normal palette.

**Given** palette actions
**When** a later story adds an action
**Then** it registers into one palette action registry (composition, ARCH25), and a test asserts every registered keyboard shortcut also has a palette entry.

**Given** no match
**When** the user types an unknown term
**Then** the palette shows "No matches. Try a CVE ID, package@version or fingerprint." plus common actions.

**Given** the keyboard map
**When** the user presses `g` + a surface letter, `J`/`K`, `/`, `⌘↵`, `x`, `?` or `Esc`
**Then** they navigate (letters show beside each nav item after `G`), move through the list, focus the list search, save and go to the next issue, export, open the ⌘K palette on its Keyboard shortcuts view (the same dialog, no new modal), or close the topmost layer, and the same map is listed in Settings → Personal (UX-DR6, UX-DR7)
**And** the `g` letters for the renamed surfaces, any new meanings for `t` and `e`, and the layout of the palette's Keyboard shortcuts view are set in EXPERIENCE.md before this story starts Build (EXPERIENCE Open item 13)
**And** single-key shortcuts never fire while focus is in a text field, and a switch in Settings → Personal turns them off (persisted in `user_preferences`, WCAG 2.1.4); `⌘K` and `⌘↵` stay on.
**And** the bindings are fixed for v1; there is no custom key-binding setting (UX-DR7).

### Story 1.9: Banned-pattern guards

As a SecOps engineer,
I want the product's banned UI patterns blocked by checks, not by memory,
So that later surfaces cannot drift into alerts, noise or nested overlays.

**Acceptance Criteria:**

**Given** the banned UI patterns (UX-DR36)
**When** the frontend guide and shared components are set up
**Then** the guide lists every banned pattern, and one shared overlay component allows one modal — the ⌘K dialog — and no drawer or stacked modal, proven by a component test.

**Given** the shadcn `Toast`
**When** a component uses it
**Then** it is never used — not as an alert, not for new findings and not for a failed save or start (failures use the inline error in the panel where the action was taken, UX-DR41) — and a lint/test enforces this.

**Given** any surface
**When** `mise run check` runs
**Then** a lint/test fails on more than one lime primary action per view (besides the active nav item; while an error band shows, its Try again is the one lime action and the list column's primary turns grey), on lime used outside its agreed jobs (active nav, the one primary action, selected map node including the centre dot of a moved Exposure map, Issues badge, text selection, the focus ring on the sidebar, on forest selection and in dark, and the all-clear tints `lime-wash` and `lime-ring`; DESIGN.md → Accent and selection), on a Compact density toggle, on a data-quality grade in a list row, or on celebratory animation classes.

## Epic 2: Fleet inventory and uniform scanning, shown as a populating posture view

The engineer connects a registry or package feed and watches Armoury enumerate, SBOM and scan the fleet with one Grype config, every scan recorded as tamper-evident evidence, while Home and Software fill in live with gaps shown openly. Issues are grouped by severity from the start; Epic 5 settles the order within each group (D1).

### Story 2.1: Tamper-evident evidence ledger

As a compliance lead,
I want every recorded event to land in an append-only, hash-chained ledger,
So that nothing Armoury later claims about scans, feeds or decisions can be silently edited.

**Acceptance Criteria:**

**Given** the `evidence` schema
**When** a capability appends an entry (type, subject, payload digest, tool/feed versions, actor, UUIDv7 id, RFC 3339 UTC time)
**Then** the entry stores the hash of the previous entry and its own hash, in the same transaction as the data it records (NFR11, ARCH5)
**And** an event that is itself the fact (for example a triage decision) keeps its full content in the entry; large content (SBOMs, scan output) is referenced by digest in the object store, content-addressed and never overwritten inside retention (ARCH32)
**And** the ledger table is partitioned by month on entry time from its first migration, so later archiving drops whole partitions (ARCH30)
**And** the control-plane login `armoury_app` has no UPDATE or DELETE grant on ledger tables, proven by a test that attempts both as `armoury_app` and fails
**And** a test proves that `armoury_app` owns no schema and no table.
**And** all ledger appends go through one append function that serializes them with a PostgreSQL advisory lock; a test runs concurrent appends from several workers and proves that the result is one linear hash chain.

**Given** an evidence-bearing table (the pattern every later evidence table follows)
**When** a row is updated or deleted
**Then** a database trigger copies the old version into its insert-only history table with `valid_from` and `valid_to`, partitioned by month on `valid_to`, so a closed version always goes into the current month; the closed version ends at the exact moment the new version starts (ARCH32)
**And** a test changes rows many times across a month boundary and checks with a query that no two versions of one row overlap
**And** a test drops the partition of an old month itself, then closes a version whose `valid_from` is in that month, and the insert into the history table succeeds
**And** a write that does not change the row's content creates no history version (rule 1)
**And** `armoury_app` has no UPDATE or DELETE grant on history tables, proven by a test that runs as `armoury_app`.

**Given** the monthly partitions of the ledger and history tables
**When** the maintenance CronJob runs (daily, as `armoury_owner`)
**Then** it creates any missing partition so that partitions always exist 3 months ahead, proven by a test that removes future partitions and runs the job
**And** when less than 1 month of partitions remains, the health endpoint shows a warning (Story 8.3 adds the metric; Story 9.7 later adds archive and drop to the same CronJob).

**Given** every application schema
**When** the history coverage test runs (in `mise run check`)
**Then** it fails if any table has neither a history table nor an explicit "not evidence" marker (rule 2)
**And** the operational tables that exist before this story (`sessions`, `user_preferences`, the River queue tables, the `_sqlx_migrations` table and the AGE graph tables created in Story 1.2) carry the "not evidence" marker.

**Given** a fixture where current rows were changed after recorded events
**When** the state at an earlier time T is rebuilt from the history tables
**Then** it equals the state recorded at T (reconstruction test; Story 9.1 builds on it).

**Given** any connection type with credentials
**When** its rows, history and ledger entries are written
**Then** a test proves that no credential or secret appears in the ledger or in history.

**Given** a ledger with entries
**When** `GET /api/v1/evidence/verification` is called
**Then** it recomputes the chain and reports `intact` or the first broken entry
**And** a test that tampers with a row directly as a superuser makes verification report the break.

**Given** a correction is needed
**When** a capability records it
**Then** it is a new superseding entry referencing the original; the original stays readable.

**Given** ledger, history and operational data share Postgres
**When** the health endpoint is called
**Then** it reports ledger and history size and database volume headroom — for bundled Postgres, the size of its PersistentVolumeClaim (the control plane gets read access to that one PVC only) minus `pg_database_size`, an approximation that ignores WAL and file-system overhead (`ponytail:` note; upgrade path a sidecar in the database pod); for external Postgres, size against a configurable budget — with a warning threshold (default 80 % used) (R9)
**And** external Postgres has no default budget: with no budget set, the health endpoint reports ledger and history size only, with the note "no budget set — headroom unknown" and no warning.

### Story 2.2: Connect a container registry and enumerate its images

As a SecOps engineer,
I want to paste read-only registry credentials and see Armoury discover every repository and image digest,
So that the fleet inventory fills without any CI changes or dev-team help.

**Acceptance Criteria:**

**Given** the empty Home page or Settings → Connections (registries)
**When** an admin adds a registry (URL, auth type, read-only credentials) and runs "Test connection"
**Then** the connection is validated before saving, and credentials are envelope-encrypted at rest with key material from the k8s Secret (FR1, ARCH17)
**And** credentials never appear in API responses, logs or subprocess argv
**And** encryption follows ARCH17 (AES-256-GCM via `aws-lc-rs`, one data key per credential, record ID as AAD, key ID for rotation); a test proves that a ciphertext copied to another record fails to decrypt, and that a master-key rotation re-encrypts every data key without data loss.

**Given** a connection (registry access through the `oci-client` crate, ARCH35)
**When** the admin chooses its discovery mode (PROC2)
**Then** they can pick **catalog** (default for generic registries), **provider API** (ECR, Artifact Registry, Docker Hub, with the same read-only credentials) or **repository list** (names or a prefix)
**And** "Test connection" states when the registry has no catalog endpoint and which mode to use.

**Given** a saved connection
**When** enumeration runs as a `riverqueue` job enqueued in the same transaction as the connection row (ARCH4)
**Then** repositories and image digests are recorded as artifacts (UUIDv7), each discovery appended to the evidence ledger
**And** enumeration is paginated and resumable so a large registry doesn't exceed the job timeout.

**Given** a registry that is unreachable or rejects credentials
**When** enumeration runs
**Then** the connection status shows the error and last success time in Settings, and the state is queryable for coverage reporting (FR5, NFR8); the job retries with exponential backoff (1 min first wait, doubled after each failure, at most 1 h, no retry limit), Settings shows the next retry time, and the job never silently drops the registry.

**Given** an analyst or auditor
**When** they view Settings → Connections (registries)
**Then** they see connection status read-only; add/edit/delete controls are absent.

### Story 2.3: Central SBOM generation with Syft

As a SecOps engineer,
I want every discovered image SBOM'd centrally the same way,
So that the whole fleet has an inventory of its contents with no per-repo setup.

**Acceptance Criteria:**

**Given** a discovered image digest without an SBOM
**When** the SBOM job runs
**Then** the `tools` module runs the pinned Syft CLI (`syft <ref> -o syft-json`) with registry credentials in per-invocation env, a timeout and stderr capture (FR2, ARCH7)
**And** the SBOM is stored in the object store via the `blob` module, keyed by digest, with the Syft version recorded
**And** the pinned Syft binary is added to the control-plane image and verified against its published checksum (ARCH7)
**And** Syft runs only in the control plane; no SBOM produced elsewhere is used (ARCH31, NFR12).

**Given** a successful SBOM
**When** it is stored
**Then** its packages are indexed for querying, and an evidence entry records digest, SBOM content hash and Syft version.

**Given** Syft fails or times out
**When** the job ends
**Then** the artifact is marked `sbom_failed` with the captured reason and retried with backoff; it stays visible as a coverage gap, not dropped.

**Given** many pending images
**When** SBOM jobs run
**Then** they use a bounded worker pool so the control plane stays responsive; the default worker count is the CPU limit of the control-plane pod, at least 2 (Helm value, PROC2).

### Story 2.4: Uniform vulnerability scanning of stored SBOMs

As a SecOps engineer,
I want every SBOM scanned by Grype with one fleet-wide configuration,
So that the same artifact always produces the same findings and no team has a snowflake setup.

**Acceptance Criteria:**

**Given** connected mode
**When** the control plane starts with no vulnerability DB
**Then** the `feeds` module fetches the Grype DB into its own version directory (`<feeds-dir>/grype/<db-version>/`) and records its version; Grype runs with `GRYPE_DB_AUTO_UPDATE=false` (ARCH7, ARCH19)
**And** the pinned Grype binary is added to the control-plane image and verified against its published checksum.

**Given** air-gapped mode and no DB imported yet
**When** scans would run
**Then** no scan runs and the state is reported as "no vulnerability database — import a feed bundle", which later posture stories show as a coverage gap — never as zero findings (NFR8).

**Given** a stored SBOM and a DB
**When** the scan job runs `grype sbom:<file> -o json --by-cve` with the single fleet-wide config
**Then** vulnerability findings are stored with typed severity — every level Grype reports, Negligible and Unknown included; Unknown or no severity becomes the `unrated` group (ARCH38) — and the locked `Finding` vocabulary (ARCH15), each recording last-evaluated time, Grype version and DB version (FR6, FR8)
**And** an evidence entry records the scan, inputs and versions.
**And** each finding stores its vulnerability ID — the CVE ID when the vulnerability has one, else the original ID (GHSA, OSV or distro ID) — and every alias of the vulnerability; the finding group (issue) is keyed on that ID (ARCH38).

**Given** the same SBOM and the same DB version
**When** it is scanned twice
**Then** the stored findings are identical (determinism test).

**Given** the scan configuration
**When** any API or per-artifact override is attempted
**Then** none exists — the configuration is fleet-wide only.

### Story 2.5: Continuous onboarding within one hour

As a SecOps engineer,
I want new images picked up, SBOM'd and scanned automatically,
So that the inventory stays complete without me triggering anything.

**Acceptance Criteria:**

**Given** a connected registry
**When** a new image digest is pushed
**Then** re-enumeration every 15 min (Helm value, PROC2) discovers it within 15 min, and it is SBOM'd and scanned within one hour of discovery, with no manual trigger (FR9)
**And** an integration test against a test registry asserts the full discovery → findings path.

**Given** the job pipeline
**When** queried
**Then** the backlog (queued, running, failed counts per stage) and a completion estimate are available for posture and later metrics.

**Given** a digest removed from the registry
**When** re-enumeration runs
**Then** the artifact is marked no-longer-present with a timestamp; its history and evidence remain.

### Story 2.6: Package feed connections — npm and PyPI

As a SecOps engineer,
I want to connect npm and PyPI registries (public or internal mirrors),
So that packages we ship are inventoried and scanned the same uniform way as images.

**Acceptance Criteria:**

**Given** Settings → Connections (package feeds)
**When** an admin adds an npm or PyPI feed (endpoint URL, scope/namespace filter, read-only credentials) and tests it
**Then** it is saved with the same validation, envelope encryption and status handling as registry connections (FR29, ARCH17).

**Given** a connected feed
**When** enumeration runs
**Then** the in-scope packages and versions become artifacts (type `package`, ecosystem `npm`/`pypi`), and each version's published archive (npm tarball, PyPI wheel or sdist) is fetched, checked against the feed checksum, unpacked into a temporary folder (path traversal and links outside the folder rejected) and SBOM'd with `syft dir:<path>`, then scanned by the same Grype pipeline with no ecosystem-specific scan config (FR2, FR6, ARCH35)
**And** a package artifact whose archive has no lock file carries the caveat that dependency versions are not exact, and the story records the actual Syft output observed per ecosystem
**And** enumeration is scoped by the configured filter so connecting a public registry never tries to inventory the whole registry.

**Given** a connected feed
**When** a new in-scope package version is published
**Then** re-enumeration every 15 min discovers it, and it is SBOM'd and scanned within one hour of discovery with no manual trigger, proven by one integration test per connector type (FR9); connectors added in Story 2.7 inherit this criterion and its test.

**Given** the connector design
**When** this story lands
**Then** package feeds register in one connector collection alongside the registry connector, and the pipeline does not branch on ecosystem beyond the connector (composition, ARCH25).

**Given** air-gapped mode
**When** a feed is configured
**Then** there is no default public endpoint — the admin must supply one (internal mirror), so nothing reaches the internet implicitly (NFR4).

### Story 2.7: Package feed connections — Maven, Cargo and Go modules

As a SecOps engineer,
I want Maven repositories, Cargo registries and Go module proxies connected too,
So that JVM, Rust and Go packages are covered by the same inventory and scans.

**Acceptance Criteria:**

**Given** the connector collection from Story 2.6
**When** an admin adds a Maven repository (group filter), a Cargo registry (sparse index, crate filter) or a Go module proxy (`GOPROXY` protocol, module-path filter)
**Then** each connects, validates and reports status exactly as npm/PyPI feeds do (FR29).

**Given** a connected Maven, Cargo or Go feed
**When** enumeration runs
**Then** in-scope versions become artifacts (ecosystem `maven`/`cargo`/`go`), their archives (JAR/POM, `.crate`, module zip) are SBOM'd by Syft as in Story 2.6 (`syft file:<path>` for JAR files) and scanned by the same pipeline, with the Story 2.6 one-hour onboarding test per connector (FR2, FR6, FR9).

**Given** each of the five package ecosystems
**When** the integration tests run against seeded test feeds
**Then** at least one known-vulnerable package version per ecosystem produces the expected finding end to end.

### Story 2.8: OCI artifacts beyond container images

As a SecOps engineer,
I want non-image OCI artifacts in my connected registries (for example Helm charts) inventoried too,
So that everything we ship through the registry is under management, not just images.

**Acceptance Criteria:**

**Given** a registry connected in Story 2.2
**When** enumeration finds OCI artifacts that are not container images (identified by artifact/media type)
**Then** they are recorded as artifacts of type `oci_artifact` with their media type, using the existing registry credentials — no second connection (FR1, FR29).

**Given** an OCI artifact whose content Syft can catalogue
**When** the SBOM job runs
**Then** it is pulled, SBOM'd and scanned through the same pipeline.

**Given** an OCI artifact type Syft cannot catalogue
**When** it is discovered
**Then** it appears as a coverage gap ("N pieces of software of a type we can't check yet", with `<media type>` small as the technical term — copy to confirm with UX) rather than being skipped or shown as clean (FR5, NFR8).

### Story 2.9: Home summary — checking, coverage and freshness

As a SecOps engineer at minute 29,
I want Home to show what is known, what isn't yet, and how fresh it is,
So that I can trust the view before the first full scan has finished.

**Acceptance Criteria:**

**Given** `GET /api/v1/posture`
**When** it responds
**Then** it returns fleet counts plus the mandatory `provenance` block — sources with versions and retrieval times, coverage (in scope / SBOM'd / scanned / failed), per-feed freshness, and `caveats[]` when partial (FR16, ARCH14)
**And** a contract test asserts every answer-bearing endpoint in `openapi.yaml` declares `provenance`.

**Given** sources are connected and work is queued
**When** Home renders
**Then** it shows the title "Home" with one plain summary line and "Last checked N min ago", and the Checking band — determinate progress ("3,176 of 3,847 checked (82%)"), an estimate in words ("about 2 h left") and "You can keep working: numbers update as each one finishes." — refreshed by polling the Home summary about every 10 s while backlog exists; it never blocks and is never a spinner or a modal (UX-DR13, NFR1, ARCH33)
**And** the "Across all software" band shows Checked as a gauge with "N are waiting their turn"; skeletons appear only where data is missing; progress is a polite `role="status"` and updates in steps under reduced motion.

**Given** coverage gaps (unscanned artifacts, failed SBOMs, unreachable registry or feed, no vulnerability DB)
**When** Home and Software render
**Then** each appears as a plain gap row where the missing data would be ("Not checked yet N"), naming the count and where ("including 212 in prod-eu-west") and saying "Their issues are unknown, not absent."; it is not dismissible or collapsible and links to its cause (FR5, UX-DR12, NFR8).

**Given** the freshness strip
**When** Home renders
**Then** it lists each source in plain words with its age ("Vulnerability data 41 min ago · Packages 38 min ago"), with the technical term (Grype DB, SBOM index) small in `text-3`; a source past its threshold turns amber with its age in words and an amber dot; a "Sources" link at the end opens Settings → Sources (UX-DR15)
**And** the uniformity claim keeps its meaning in plain labels — "All N pieces of software checked the same way — Syft vX · Grype vY", where N is the checked count, not the discovered count; where it sits on Home is set by UX before Build (O18).

**Given** no sources are connected
**When** Home renders
**Then** it shows the title and the setup action "Connect a registry" with its copy-paste one-liner in a code block with Copy; no illustration (UX-DR29, UX-DR42; Story 3.2 adds the second action).

### Story 2.10: Home — Needs attention and open issues by severity

As a SecOps engineer,
I want to see what needs attention today and the open issues by severity,
So that I can see where the problems are across everything checked.

**Acceptance Criteria:**

**Given** the open question Q2 (how the issue sentence is cut from the Grype DB description and how its source is labelled beside it; sprint-change-proposal-2026-11-07-readiness.md)
**When** this story is planned
**Then** the decision is recorded in `architecture.md` (Issues and review → Issue sentence) and EXPERIENCE.md (Home → Overview) and approved by the user before implementation.

**Given** the open question Q4 (the Negligible and Not rated yet severity markers, proposed in DESIGN.md but not drawn in the mock: confirm or redraw; sprint-change-proposal-2026-11-07-readiness.md)
**When** this story is planned
**Then** the decision is recorded in DESIGN.md (Components → Severity) and approved by the user before implementation.

**Given** scanned findings
**When** Home renders
**Then** the list column shows **Needs attention N** — issues (one vulnerability or licence in one package version, across all its places; UX-DR39) that are Not reviewed yet in any place AND Actively exploited or Critical, plus every Not-reviewed-yet licence violation (never a licence warning, D8) — as standard rows (name + version · severity · Actively exploited · where; right column places, "14 places"), then **Open issues N** as summary rows: Licences first (hidden at 0), then Critical (with "N actively exploited"), High, Medium, Low, Negligible and Not rated yet (the last two hidden at 0) with counts, then "N not reviewed yet · N reviewed · See all" (UX-DR22, UX-DR38)
**And** until Epic 4 loads the exploited list and Epic 5 records reviews, every issue is Not reviewed yet and none is marked Actively exploited; the rule is applied unchanged and computed on the server (ARCH38)
**And** the sidebar Issues item shows a badge with the Needs-attention count, and no badge at 0; it counts decisions due, never new findings.

**Given** the selected issue
**When** the detail column renders
**Then** it shows tabs Overview · Exposure · How to fix · Details; Overview holds the title, the first sentence of the advisory description from the vulnerability record, unchanged, with its source (FR12; no rewrite; no sentence when there is no description), severity as a word + 4-step marker (UX-DR9), Vulnerability (the key ID in mono: the CVE ID when the vulnerability has one, else the original ID such as a GHSA ID; ARCH38), Found in, The fix and Review status (Not reviewed yet until Epic 5); the Exposure tab arrives with Story 6.3, and How to fix and Details wait for UX (EXPERIENCE Open item 14)
**And** the findings API returns finding groups (ARCH38) with place counts and per-group counts, cursor-paginated with a total (ARCH13)
**And** the "Across all software" band adds Open issues (last 30 days, sparkline, delta chip such as "247 fewer") computed from history (ARCH32).

**Given** nothing that needs attention, over partial coverage
**When** Home renders
**Then** it reads "Nothing needs you today." with the scope sentence ("That covers the N pieces of software we've checked; M are still waiting their turn."), shows no Issues badge, and the view's one lime action follows EXPERIENCE (Review all N from Story 5.4; Audit report from Story 9.5) (UX-DR45).

### Story 2.11: Software list and software detail

As a SecOps engineer,
I want to open any piece of software and see its packages, issues and how it was checked,
So that I can answer "what's in this and how do we know?" for one piece of software.

**Acceptance Criteria:**

**Given** the Software surface
**When** it loads
**Then** the list column shows "Software" and a summary line ("3,847 pieces of software."), standard rows (name + version; line 2 where it runs; right column the issue count "2 issues"; no data-quality grade), the "Not checked yet N" gap row in place, the pager "1–25 of N · page 1 of M" (25 per page, never infinite scroll) and the lime Add software (its destination is set by UX before Build, EXPERIENCE Open item 18); while backlog exists the Checking band shows, with per-row step text ("Reading packages · step 2 of 3", "Waiting its turn")
**And** until a cluster agent reports (Epic 3) the list is not split into Deployed / Not deployed; Story 3.5 adds the groups
**And** each piece of software keeps its type (`image`, `package`, `oci_artifact`, `filesystem`) and source (registry, package feed, CI scan, CI upload) in its detail; how CI-submitted software is grouped and labelled is EXPERIENCE Open item 28.

**Given** an artifact
**When** its detail opens via `GET /api/v1/artifacts/{id}` (with `provenance`)
**Then** it shows tabs Overview · Issues · Packages · Audit trail; Overview, in the order of UX-DR25, holds **Info** — Name, Fingerprint (mono, Copy), Runs in, Copies, **Built** (the creation time the artifact records — for an image, the `created` time in its image config — or "Unknown"; copy to confirm), Last checked, Data quality (filled by Story 8.2; what it shows before a score exists is EXPERIENCE Open item 32) and **Signed** (filled by Story 4.10; until then it says the signature is not checked yet) — beside the Packages cell ("214 packages · SBOM", Direct / Indirect; the licence line arrives with Epic 7 and the end-of-life line with Story 4.9) over Where it runs; then Issues, the Issues trend and "Latest in the audit trail" ("Entries are never edited or removed"); provenance is inline ("Last checked", "How we know: Syft v… · Grype DB v…") instead of a freshness strip (FR18, FR8, UX-DR25)
**And** the Where it runs cell reads "No cluster agent connected — where it runs is unknown" until Epic 3 provides data.

**Given** an artifact whose SBOM or scan failed
**When** its detail opens
**Then** the failure reason and retry status are shown in place of the Issues cell, never as zero issues.

**Given** a connected registry that is unreachable
**When** Software renders
**Then** an edge-to-edge error band names it ("We can't reach registry.acme.internal") with since when, what it affects, what still works and the likely cause; the lime **Try again** is the view's one lime action and Add software turns grey; the grey **Open connection settings** opens Settings → Connections; affected rows say "As of 14:02 · registry" in amber with a clock; nothing is removed (FR5, NFR8, UX-DR29).

**Given** Software detail
**When** a user presses the grey **Check again**
**Then** the SBOM and the scan of that one piece of software are queued again at once, through the same pipeline and fleet toolchain (NFR12); the row and the detail show step text until done ("Reading packages · step 2 of 3"); the request is appended to the evidence ledger with who and when; and a failure to start shows the inline error with Try again (FR18, UX-DR41, D10)
**And** the operation declares its minimum role with `x-armoury-role` in `openapi.yaml` (the role is chosen when the story is planned — O4), and Check again is absent for roles below it (UX-DR31).

### Story 2.12: Prove minute 29 — scripted install-to-posture run

As the Armoury product owner,
I want the 30-minute install-to-posture gate measured by a repeatable script,
So that NFR1 is a checked product gate, not a claim.

**Acceptance Criteria:**

**Given** a fresh, uniquely named namespace in the dev cluster and a seeded test registry
**When** the scripted run deploys the chart into that namespace with Skaffold (ARCH34), then times the customer steps — bootstrap sign-in and registry connection — with no other manual step
**Then** Home and Software are live and visibly checking (Checking band, Checked gauge, "Not checked yet" rows) in under 30 minutes, with the elapsed time per step recorded (NFR1)
**And** the script fails if any step needs input beyond the documented values and credentials
**And** the script deletes the namespace when it finishes, pass or fail.

**Given** the run
**When** it completes
**Then** the timing is appended to a committed performance record, and a miss is raised as a blocking finding against the install path rather than accepted.

**Given** the script
**When** it is invoked
**Then** it runs as its own mise task outside the default `mise run check`, and is reusable by Epic 3 to add the agent install step.

### Story 2.13: Prove the scale anchor — initial-evaluation load test

As the Armoury product owner,
I want initial evaluation and read latency measured at the scale anchor,
So that NFR3 and the 24-hour initial-scan bound hold before more features are layered on.

**Acceptance Criteria:**

**Given** a seeded fleet at the scale anchor (hundreds of repositories, thousands of images)
**When** initial evaluation runs
**Then** throughput is measured for at least 1 hour after a 10-minute warm-up, and the projected completion is 18 hours or less (a 25 % margin to the 24-hour bound), and per-SBOM Syft and Grype subprocess costs (spawn, DB open, run) are recorded (NFR1, NFR3, ARCH28 R11).

**Given** that load
**When** posture, findings-table pages and artifact list endpoints are called
**Then** the posture, findings page (50 rows) and artifact list endpoints each have p95 ≤ 500 ms while the initial evaluation runs
**And** when 10 % of the backlog is done, the Checking band's estimate is within ±25 % of the actual completion time.

**Given** the results
**When** the story completes
**Then** they are written to the committed performance record; any miss is a blocking finding with the R11 fallback (long-lived Go matcher sidecar) evaluated rather than silently accepted.

**Given** the load test
**When** it is invoked
**Then** it runs as its own mise task outside `mise run check`, with fixtures reusable by the Epic 4 (R2) and Epic 6 (R1) load tests.

## Epic 3: Running inventory from read-only cluster agents

The engineer installs the agent with a second one-liner; running workloads appear linked to registry artifacts, so Software splits into Deployed and Not deployed and "is this running anywhere?" is answerable; disconnected agents and unmatched running digests surface as gaps. Story 3.1 closes the open enrollment gap (ARCH10) before any agent code depends on it.

### Story 3.1: Agent enrollment and mTLS identity

As a SecOps engineer,
I want a cluster agent to enrol with the control plane from a single install command,
So that it gets a trusted identity without me running a PKI or opening inbound ports.

**Acceptance Criteria:**

**Given** the open architecture gap ARCH10
**When** this story is planned
**Then** the enrollment design (token format and lifetime, identity issuance, rotation, revocation) is recorded as an amendment to `architecture.md` and approved by the user before implementation (ARCH10)
**And** the design keeps the agent outbound-only and works with operator-supplied CAs and egress proxies (R4).

**Given** the agent port from Story 1.2
**When** this story lands
**Then** the control plane serves enrollment, certificate renewal and the revocation check on that port and ends TLS itself with `rustls` (ARCH8); a connection with a revoked or invalid client certificate is refused, proven by a test.

**Given** Settings → Connections (agent install, admin only)
**When** the admin creates an enrollment for a named cluster
**Then** a single-use, time-limited enrollment token is issued and shown once, and only its hash is stored.

**Given** an agent started with the control-plane address and a valid token
**When** it enrols
**Then** it generates its own key, receives a short-lived client certificate bound to that cluster identity, and the token is consumed; a reused or expired token is rejected with a clear error
**And** the agent renews its certificate before expiry without re-enrolment.

**Given** an enrolled cluster
**When** the admin revokes it in Settings
**Then** subsequent agent connections are refused and the cluster is marked revoked with the revocation time; its data is never deleted (Story 3.2 marks its runtime data stale).

**Given** each enrollment, renewal and revocation
**When** it happens
**Then** an evidence entry records it without any secret material.

### Story 3.2: Read-only agent reports running workloads

As a SecOps engineer,
I want the agent to report what is running in each cluster using only watch/list access,
So that I can install it in prod without asking for cluster-admin.

**Acceptance Criteria:**

**Given** the agent subchart
**When** it is rendered
**Then** its ClusterRole grants only `get`/`list`/`watch` on the workload resources it reads (pods and their owners), and a chart test fails if any other verb or resource is added (NFR9)
**And** the agent image and its registry are configurable so air-gapped installs pull from an internal mirror (NFR4).

**Given** an enrolled agent
**When** it runs
**Then** `kube-runtime` reflectors maintain the set of running containers with cluster, namespace, workload (owner kind/name), container name and resolved image digest, and stream deltas to the control plane over outbound mTLS gRPC defined in `proto/agent/v1` (FR3, ARCH8)
**And** the control plane serves agents on its separate agent port and ends mTLS itself with `rustls`, so it reads the client certificate; a test proves that a reporting connection without a valid client certificate is refused (enrollment in Story 3.1 is the only call that needs no client certificate, and it needs a valid enrollment token instead)
**And** containers whose image digest cannot be resolved are reported with their image reference and an `unresolved` flag, never dropped.

**Given** the control plane's `agentgw`
**When** deltas arrive
**Then** the cluster's running inventory is updated, and the agent's heartbeat time is recorded; the agent sends a heartbeat every 30 s.

**Given** a cluster revoked in Story 3.1
**When** its running inventory is queried
**Then** its runtime data is marked stale-as-of the revocation time, not deleted.

**Given** the agent
**When** it reports
**Then** it sends only running digests and workload locations; it never generates SBOMs or findings (ARCH31, NFR12).

**Given** Settings → Connections (agent install)
**When** an admin opens it
**Then** it shows the copy-paste `helm install` one-liner with the control-plane address and token filled in, states the trust posture ("read-only — watch/list only, never cluster-admin") and shows the exact RBAC rules before install (UX-DR28)
**And** the one-liner sits in a code block with Copy ("Copied" for 2 s, announced politely) (UX-DR42)
**And** the empty Home now offers exactly two setup actions — connect a registry and install a cluster agent — each with its one-liner in a code block (UX-DR29).

**Given** the agent
**When** it is tested
**Then** unit tests run against a mocked kube client and an integration test runs in a temporary namespace of the dev cluster on an ARC runner in CI, with the agent's own read-only ClusterRole, asserting only on workloads in its namespace (ARCH27).

### Story 3.3: Reconnect by stateless re-derive, without storms

As a SecOps engineer,
I want agents to recover cleanly after a control-plane restart or network break,
So that the running inventory never silently drifts out of date.

**Acceptance Criteria:**

**Given** an agent that loses its connection
**When** it reconnects
**Then** it relists from the Kubernetes API and sends a full snapshot, and the control plane reconciles it against stored state — adding, updating and ending running records — with no agent-side buffer (ARCH9, R3).

**Given** ten agents reconnecting after a control-plane restart
**When** they reconnect
**Then** reconnects are jittered and the control plane bounds the reconciliation rate, so the recovered control plane stays responsive; a test simulates ten clusters reconnecting at once and asserts that API p95 stays below 1 s.

**Given** an agent whose heartbeat is older than the warn threshold (default 5 min), then the disconnect threshold (default 60 min), both Helm values (PROC2)
**When** the state is queried
**Then** the cluster is reported `stale` then `disconnected` with its last-seen time, and its runtime data is kept and marked stale-as-of that time, not removed (NFR8, UX-DR30).

### Story 3.4: HTTPS long-poll fallback for locked-down networks

As a SecOps engineer in a regulated network,
I want the agent to work through proxies that block gRPC streaming,
So that runtime inventory works where our most security-conscious environments live.

**Acceptance Criteria:**

**Given** an environment where gRPC streaming fails (simulated by a proxy that blocks HTTP/2 upgrades)
**When** the agent connects
**Then** it falls back to HTTPS long-poll over the same mTLS identity, on the same agent port, and delivers the same deltas and snapshots (ARCH8, R4).

**Given** an egress proxy configured in agent values (including a custom CA bundle)
**When** the agent connects
**Then** it uses the proxy and trusts the supplied CA.

**Given** either transport
**When** the agent reports
**Then** the control plane records which transport is in use, visible in Settings → Connections for that cluster.

### Story 3.5: Shipped-vs-running reconciliation

As a SecOps engineer,
I want every artifact linked to where it runs, and every running image linked to an artifact,
So that "is this running anywhere?" has an answer — and running images we can't match are never invisible.

**Acceptance Criteria:**

**Given** running containers and registry artifacts
**When** reconciliation runs
**Then** running records are linked to artifacts by image digest (not tag), and each artifact exposes its running locations (cluster/namespace/workload) with first-seen and last-seen times (FR4)
**And** the links are stored in relational tables only; Story 6.1 projects them into the AGE graph.

**Given** a running digest that matches no artifact from any connected source (unconnected registry, mirror digest, mutable tag, third-party sidecar)
**When** reconciliation runs
**Then** it is recorded as `unmatched` with its image reference and location, and counted for coverage reporting (ARCH11, R7).

**Given** Software detail
**When** a piece of software runs somewhere
**Then** the Where it runs cell lists each copy as a path ("prod-eu-west/payments"), replacing the "No cluster agent connected" message from Story 2.11, and the Software list splits into **Deployed N** (line 2 "prod-eu-west · 4 copies") and **Not deployed N** (line 2 "Last deployed 12 days ago" or "Never deployed"; hint "Not seen running in any connected cluster.", also on focus), with the summary "N deployed, M not deployed" (FR18, UX-DR25).

**Given** an artifact no longer running anywhere
**When** reconciliation runs
**Then** its past running locations remain queryable with their end times.

### Story 3.6: Runtime coverage on Home and Software, and minute 29 with the agent

As a SecOps engineer,
I want Home and Software to show what is deployed, where agents are missing or stale, and what we can't match,
So that the fleet view never needs a caveat the UI doesn't already show.

**Acceptance Criteria:**

**Given** connected agents
**When** Home and Software render
**Then** the Software summary line counts deployed and not-deployed software, and the freshness strip shows "N clusters reporting" (each cluster's last heartbeat is in Settings → Connections) (FR16, UX-DR15).

**Given** a stale or disconnected agent, or unmatched running digests
**When** Home and Software render
**Then** a disconnected cluster's runtime data is marked "as of 14:02", not removed, and each gap appears as a plain gap row ("37 running fingerprints we can't match to any connected source" — copy to confirm with UX) linking to its cause (FR5, UX-DR12, UX-DR30, NFR8)
**And** the posture API's `provenance.coverage` includes these counts and a caveat when runtime data is partial (ARCH14).

**Given** the Story 2.12 install-to-posture script
**When** it is extended with the agent `helm install` step
**Then** Home and Software show deployed software and runtime coverage within the 30-minute gate, and the timing is recorded (NFR1).

## Epic 4: Fresh, enriched findings, connected or air-gapped

When vulnerability or enrichment feeds update — online or by signed offline bundle — stored SBOMs are re-evaluated within an hour without rescans, and every finding carries source-attributed KEV, EPSS, CNA and OSV data. Issues stay grouped by severity; Epic 5 settles the order within each group, and enrichment is visible on issues (the Actively exploited marker, technical details) from this epic on. The epic ends with two more external sources of knowledge, both connected or air-gapped: end-of-life data for packages (Story 4.9, FR33) and signature checks against trusted signers (Story 4.10, FR32).

### Story 4.1: Scheduled vulnerability database updates with versioned history

As a SecOps engineer,
I want the vulnerability database kept current automatically, with every version recorded,
So that findings can prove which intel they were evaluated against.

**Acceptance Criteria:**

**Given** connected mode
**When** the update schedule fires (default every 6 h, Helm value, PROC2)
**Then** the `feeds` module downloads the latest Grype DB to a staging location, validates its checksum from the Grype DB listing and its schema version, and only then atomically activates it as the current version (FR7, ARCH20 R8)
**And** each activated version (version, build time, checksum, source, retrieved_at) is stored and appended to the evidence ledger.

**Given** a download that fails or a database that fails validation
**When** the update runs
**Then** the previous version stays active, the feed is reported stale with the failure reason, and nothing partial is ever activated (fail closed).

**Given** air-gapped mode
**When** the schedule would fire
**Then** no outbound request is made; only bundle import (Story 4.6) can change the database (NFR4, ARCH19).

**Given** previous database versions
**When** retention runs
**Then** at least the current and previous versions are kept so the next re-evaluation can compute a delta.

### Story 4.2: Feed-delta re-evaluation of stored SBOMs

As a SecOps engineer,
I want existing SBOMs re-evaluated against new intel as soon as the database updates,
So that findings are already current on CVE day — no rebuilds, no rescans.

**Acceptance Criteria:**

**Given** a newly activated database version
**When** re-evaluation runs
**Then** `reeval` computes the delta from the previous version with `grype db diff -o json <previous-db> <current-db>` through `tools` (packages with changed matches; added, changed and withdrawn vulnerability records), selects only the stored SBOMs containing those packages through the package index, and re-matches that subset with `scan`'s Grype matcher (FR7, ARCH6)
**And** Armoury never reads the Grype SQLite schema itself.
**And** no image is pulled and no SBOM is regenerated.

**Given** a fixture fleet and two database versions
**When** delta re-evaluation and a full rescan are both run
**Then** they produce identical findings (equivalence test — the delta selects work, it never changes results, FR6).

**Given** re-evaluated findings
**When** they are stored
**Then** each records its new evaluation time and database version; new findings are added, findings no longer matched are marked resolved-by-feed with the version that resolved them, and every change is appended to the evidence ledger (FR8, NFR11)
**And** unaffected findings get no new history version (ARCH32 rule 1); one run entry records "fleet evaluated against Grype DB vX", and their provenance reads that run entry, so no finding shows a stale "last evaluated" time.

**Given** a re-evaluation still running when the next database version activates
**When** the new version lands
**Then** work is coalesced to the newest version and the backlog is surfaced (Checking band and pipeline state), never hidden (R2, NFR8).

**Given** Software detail, Exposure answers and the posture `provenance`
**When** they render after a re-evaluation
**Then** they show the evaluation inline — "Last checked", "How we know: Syft v… · Grype DB vX · checked N min ago" and, on Exposure, "Answered N min ago" — and no rescan is needed (UX-DR15, UX-DR23).

### Story 4.3: KEV and EPSS enrichment with source attribution

As a SecOps engineer,
I want findings marked when they are on the CISA KEV list and scored with EPSS,
So that I can see which findings are exploited or likely to be.

**Acceptance Criteria:**

**Given** connected mode
**When** the enrichment schedule fires (default every 6 h, Helm value, PROC2)
**Then** the `enrichment` module fetches the CISA KEV catalogue and EPSS scores, validates them, and stores each snapshot with source, source version/date and retrieved_at, appended to the evidence ledger (FR11, FR12, ARCH21).

**Given** a new enrichment snapshot
**When** it is applied
**Then** findings are re-joined to the new enrichment without re-matching SBOMs, matching KEV entries and EPSS scores on any alias of the finding's vulnerability (ARCH38), and each enrichment datum on a finding carries its source and retrieval time.

**Given** an issue in the UI (Home, Issues, Software detail)
**When** it is KEV-listed (the KEV catalogue lists any alias of its vulnerability, ARCH38)
**Then** list rows show "Actively exploited" as clay text with a pulse icon (never dropped when a row truncates), detail views show the Actively exploited pill with a grey "KEV" tag, and the technical-details block lists KEV, CVSS and the raw EPSS value with source and retrieval time; EPSS is never shown as a rating, tag, column or hover score (UX-DR9, FR12).

**Given** a fetch or validation failure
**When** enrichment runs
**Then** the previous snapshot stays active and the source is reported stale — never partially applied (ARCH20 R8).

**Given** air-gapped mode
**When** the schedule would fire
**Then** no outbound request is made; enrichment arrives only by bundle (NFR4).

### Story 4.4: OSV and CNA record enrichment

As a SecOps engineer,
I want findings enriched from OSV and CVE (CNA) records,
So that severity, affected ranges and descriptions don't depend on NVD alone.

**Acceptance Criteria:**

**Given** the open question Q2 (which description the issue sentence uses when more than one source has one — the Grype DB record, the CVE List CNA container or OSV; sprint-change-proposal-2026-11-07-readiness.md)
**When** this story is planned
**Then** the decision is recorded in `architecture.md` (Issues and review → Issue sentence) and approved by the user before implementation.

**Given** connected mode
**When** the enrichment schedule fires (default every 6 h, Helm value, PROC2)
**Then** the full CVE List v5 (CNA-supplied CVSS, descriptions, affected data) is mirrored — an initial full snapshot, then the official daily delta files — and validated and stored as versioned, source-attributed snapshots (FR11, FR12, ARCH21)
**And** OSV records are fetched in one of two configurable modes (PROC2): **fleet-scoped** (default — the CVEs/aliases in fleet findings plus advisories for packages in stored SBOMs, across every ecosystem those SBOMs contain, including OS distro packages) or **full mirror** (all OSV, ~2.7 GB), set via Helm values.
**And** CVE List and OSV records join to a finding on any alias of its vulnerability (ARCH38).

**Given** sources that disagree (for example CNA CVSS vs. Grype DB severity)
**When** a finding is displayed
**Then** each value is shown with its own source label; no source is silently overwritten by another.

**Given** Software detail and the Issues detail
**When** an issue renders
**Then** its technical-details block lists every source used with retrieval time (the vulnerability ID and its other aliases, KEV, CVSS, EPSS, source, check time), and the freshness strip gains an entry per enrichment source in plain words with the technical term small ("Exploited list KEV 6 Nov"; the labels for CNA, OSV and EPSS are not drawn in the spine — copy to confirm with UX) (UX-DR15).

**Given** a later enrichment correction
**When** it changes data already used by a finding
**Then** the change is recorded as a superseding enrichment version, so earlier evidence remains explainable (R10).

### Story 4.5: Offline feed bundle format and creation

As a SecOps engineer running an air-gapped Armoury,
I want to build a signed bundle of all feeds on a connected machine,
So that I can carry current intel across the air gap.

**Acceptance Criteria:**

**Given** the open enrichment-bundle format gap (ARCH20)
**When** this story is planned
**Then** the bundle format (manifest, contents, versioning, signature scheme) is recorded as an amendment to `architecture.md` and approved by the user before implementation.

**Given** a connected machine
**When** the operator runs the documented bundle command (`armoury bundle create`, shipped as part of the control-plane binary or image)
**Then** it produces one archive containing the Grype DB and the KEV, EPSS, OSV and CNA snapshots, with a manifest listing each component's source, version, retrieved_at and checksum (FR10, ARCH20)
**And** CVE List v5 is carried as daily deltas against the base version the manifest names (a full snapshot only when the target instance has no base), and OSV is carried in the instance's configured mode (fleet-scoped by default; full mirror if chosen), so a routine fleet-scoped bundle stays in the low hundreds of MB rather than ~3.5 GB (measured 2026-11-04: Grype DB 190 MB, CVE v5 full 621 MB / delta ~3 MB, OSV full 2.7 GB).

**Given** OSV must be fleet-scoped but the bundle is built on a separate connected machine
**When** the operator creates a bundle
**Then** in fleet-scoped mode they supply a scope manifest exported from the air-gapped instance (`armoury bundle scope`, listing CVE IDs and package coordinates only — no credentials or internal hostnames), and the bundle command uses it.

**Given** an operator signing key
**When** the bundle is created
**Then** the manifest is signed with cosign, and a matching offline verification command is printed (ARCH18)
**And** this story creates the `signing` module (key signing and verification, used for bundles here; Story 9.4 extends it to packs and checkpoints), and adds the pinned cosign binary to the control-plane image, verified against its published checksum.

**Given** a bundle
**When** it is tampered with (any byte of any component or the manifest)
**Then** verification fails — proven by a test.

### Story 4.6: Import an offline bundle into an air-gapped instance

As a SecOps engineer running an air-gapped Armoury,
I want to import a bundle and have the whole fleet re-evaluated against it,
So that air-gapped posture is as current as connected posture.

**Acceptance Criteria:**

**Given** Settings → Sources (bundle import, admin only) or the import API
**When** an admin uploads a bundle
**Then** the signature is verified against the trusted public keys listed in chart values (operator keys; an operator can remove any key) — every component checksum and schema is validated, and only then are all components activated together in one step (FR10, ARCH20 R8)
**And** a partial, corrupt, unsigned or untrusted bundle is rejected as a whole, the previous feeds stay active and are reported stale, and the reason is shown.

**Given** a successfully activated bundle
**When** activation completes
**Then** feed-delta re-evaluation (Story 4.2) and enrichment re-join (Story 4.3) run exactly as for online updates, and the import is appended to the evidence ledger with the bundle's manifest digest (FR7, FR8).

**Given** a bundle older than or equal to the active feed versions
**When** it is imported
**Then** it is refused with "This bundle is not newer than the active feeds", so intel never goes backwards silently.

**Given** air-gapped mode
**When** the freshness strip renders
**Then** it shows the bundle age alongside feed ages, and offers an "Import bundle" action to admins (UX-DR30).

### Story 4.7: Honest feed staleness across Home and Issues

As a SecOps engineer,
I want stale or failing feeds to change what Home says,
So that I never read a confident answer resting on old intel.

**Acceptance Criteria:**

**Given** per-feed freshness thresholds, configurable via Helm values (PROC2) — defaults: in connected mode each daily feed (Grype DB, KEV, EPSS, CVE List, OSV) is stale after 48 h; in air-gapped mode the active bundle is stale after 7 days
**When** a feed exceeds its threshold or its last update failed
**Then** its freshness-strip age turns amber with the age in words and an amber dot, the Home summary line gains a scoped caveat (for example "The exploited list (KEV) is 3 days old, so Actively exploited may be out of date." — copy to confirm with UX), "good shape" is never claimed on old data, and the posture API `provenance.caveats[]` carries the same text (NFR8, UX-DR30, ARCH14).

**Given** a feed that has never been loaded
**When** Home renders
**Then** it appears as a coverage-gap row naming the missing feed, not as an empty enrichment column.

**Given** the "Sources" link on the freshness strip
**When** it is clicked
**Then** it opens Settings → Sources, showing each feed's version history, last success, last failure and reason (UX-DR15).

### Story 4.8: Prove one-hour re-evaluation at the scale anchor

As the Armoury product owner,
I want feed-update re-evaluation measured at the scale anchor,
So that NFR5 and the CVE-day "already re-evaluated" promise are known to hold.

**Acceptance Criteria:**

**Given** the Story 2.13 scale-anchor fixtures and two realistic database versions (including a large feed delta)
**When** the new version activates
**Then** fleet-wide re-evaluation completes within one hour, with the delta-computation stage (`grype db diff`), subset size and re-match time each measured separately (NFR5, ARCH28 R2)
**And** a full re-check of every stored SBOM is measured on the same fixtures, and both results are recorded; choose the full re-check only if it completes in 45 minutes or less (a 25 % margin to the one-hour bound), otherwise keep `grype db diff`; record the choice in `architecture.md` (ARCH6).

**Given** an enrichment-only update (KEV, EPSS, OSV or CNA re-join)
**When** it activates
**Then** the re-join completes within the same one-hour bound.

**Given** an offline bundle import of the same delta
**When** it activates
**Then** it meets the same bound.

**Given** the results
**When** the story completes
**Then** they are appended to the committed performance record; a miss is a blocking finding with the R11 fallback evaluated rather than accepted.

**Given** the load test
**When** it is invoked
**Then** it runs as its own mise task outside `mise run check`.

### Story 4.9: End-of-life data for packages

As a SecOps engineer,
I want to see which packages in a piece of software have reached their end of life,
So that I can plan upgrades before a package stops getting security fixes.

**Acceptance Criteria:**

**Given** the open end-of-life data decision (FR33, ARCH41)
**When** this story is planned
**Then** the end-of-life data source and its licence, what it covers (package ecosystems; whether runtimes and OS releases are included), how packages are matched to it (exact identifiers only), and its staleness threshold (PROC2 default) are recorded as an amendment to `architecture.md` and approved by the user before implementation.

**Given** connected mode
**When** the enrichment schedule fires (default every 6 h, Helm value, PROC2)
**Then** the `enrichment` module fetches the end-of-life dataset, validates it and stores it as a versioned, source-attributed snapshot (source, version or date, retrieved_at), appended to the evidence ledger (FR33, FR12, ARCH21)
**And** a fetch or validation failure keeps the previous snapshot active and reports the source stale; nothing is ever partially applied (ARCH20 R8).

**Given** a new snapshot
**When** it is applied
**Then** every package in every stored SBOM is re-joined to it through the package index without re-matching SBOMs, and each package records its end-of-life date and status — past end of life, supported or unknown — with source and retrieval time (FR33, FR7)
**And** a package the data does not cover is "unknown", never "supported", proven by a test.

**Given** air-gapped mode
**When** the schedule would fire
**Then** no outbound request is made; the dataset arrives only as one more component of the offline bundle — this story extends the Story 4.5 manifest and the Story 4.6 import, so it is verified and activated together with the other components (FR10, NFR4, ARCH19, ARCH20).

**Given** Software detail
**When** the Packages cell and the Packages tab render
**Then** the cell carries one end-of-life line scoped to the data ("No package is past its end of life." only when every package is covered and none is past; otherwise the count past end of life and the count with no end-of-life data, in plain words — copy to confirm with UX, O14), and each package in the Packages tab shows its end-of-life date or that there is no end-of-life data, with the source small (UX-DR25)
**And** end-of-life status is stated in words, has no severity colour, creates no issue and does not count toward Needs attention (O13).

**Given** `GET /api/v1/artifacts/{id}`
**When** it responds
**Then** each package carries its end-of-life status, date and source, and the source's version and age are in `provenance.sources` (ARCH14).

**Given** Settings → Sources and the Story 4.7 freshness rules
**When** the source is past its threshold or its last update failed
**Then** Settings → Sources lists it with version history, last success, last failure and reason, and the Software detail end-of-life line carries a scoped caveat; whether the source also appears on the Home freshness strip is set by UX before Build (O15) (UX-DR15, UX-DR28).

**Given** the Story 4.8 scale-anchor fixtures
**When** an end-of-life re-join runs
**Then** it completes within the one-hour enrichment re-join bound, and the result is appended to the committed performance record.

### Story 4.10: Verify artifact signatures against trusted signers

As a SecOps engineer,
I want Armoury to check whether each image is signed by someone we trust,
So that I can tell software someone vouched for from software nobody did.

**Acceptance Criteria:**

**Given** the open signature-verification decision (FR32, ARCH40)
**When** this story is planned
**Then** the trust configuration (public keys and keyless signer identities; fleet-wide or per registry connection), the result states and their names, the signature formats read from the registry, the artifact types in scope, and how the Sigstore trusted root reaches air-gapped instances are recorded as an amendment to `architecture.md` and approved by the user before implementation.

**Given** Settings → Policy (signature policy, admin only) or Helm values
**When** an admin adds or removes trusted signers
**Then** they can add public keys and keyless signer identities (OIDC issuer and subject); the default is none (PROC2), so a default install verifies nothing and says so; each change is a new policy version appended to the evidence ledger; analysts and auditors see the policy read-only with edit controls absent (UX-DR28, UX-DR31).

**Given** a container image or other OCI artifact in a connected registry
**When** it is discovered, or the signature policy changes
**Then** the control plane runs the pinned cosign CLI (added in Story 4.5) through `tools` to verify its signatures, read from the same registry with the connection's read-only credentials in per-invocation env (never argv), and records the result with the signer, the trust-policy version, the cosign version and the check time, appended to the evidence ledger (FR32, NFR12, ARCH7, ARCH40)
**And** a policy change re-checks signatures without rescanning SBOMs.

**Given** air-gapped mode
**When** a signature is verified
**Then** key-based verification makes no network call, and keyless verification uses only the offline trusted root from the approved amendment; no call is made to public Fulcio, Rekor or the Sigstore TUF repository, proven by the Story 1.2 air-gap test (NFR4, ARCH19).

**Given** Software detail
**When** the Info list renders
**Then** "Signed" reads "Yes" when a signature from a trusted signer verifies, and plain words for every other state (copy to confirm with UX, O7), with the signer and check time in the technical details; a missing or failed signature is never hidden and never shown in a severity colour (FR32, NFR8, UX-DR25)
**And** an artifact type this story does not check says that it is not checked, never "No" (O10).

**Given** a tampered image, a signature by a removed key or a keyless identity that does not match
**When** verification runs
**Then** the result is not "verified", proven by tests.

**Given** `GET /api/v1/artifacts/{id}`
**When** it responds
**Then** it includes the signature result (state, signer, trust-policy version, cosign version, check time) (ARCH14).

## Epic 5: Prioritise and triage findings

The analyst works the Issues list — grouped by severity, Actively exploited first in each group, the order stated in words — and records decisions with their reason in the review panel, which propagate everywhere the issue appears, and ingests and emits VEX. Decisions are append-only evidence: corrections supersede, never overwrite.

### Story 5.1: Deterministic, explainable issue order

As a SecOps engineer on a small team,
I want issues grouped by severity with Actively exploited first in each group, in an order I can read in words,
So that I work the findings that matter instead of ten thousand rows.

**Acceptance Criteria:**

**Given** the open ranking-formula decision (ARCH29)
**When** this story is planned
**Then** the exact order (severity groups and severity-source precedence, Actively exploited first within a group, the raw EPSS value as the next key, the stable tie-breaker, licences in their own group) is recorded as an amendment to `architecture.md` and approved by the user before implementation.

**Given** findings with enrichment
**When** `ranking` computes order
**Then** each issue falls into the Licences group or the Critical / High / Medium / Low / Negligible / Not rated yet group of its severity (Not rated yet = Grype Unknown or no severity, ARCH38); every Actively exploited issue sorts above every other issue in its group, and the rest follow the approved within-group order, and ties break on a stable key so the same inputs always give the same order (FR13)
**And** a property test asserts determinism and the exploited-first-within-group invariant over generated issues.

**Given** any finding
**When** `GET /api/v1/findings/{id}` is called
**Then** it returns an order explanation — each input (severity and its source, KEV status, the raw EPSS value) with its source and retrieval time, and the resulting group and position — in words a human can read; the UI shows it only in the technical-details block, never as a rating.

**Given** new enrichment or a re-evaluation
**When** it is applied
**Then** affected rankings are recomputed without re-matching SBOMs.

**Given** license findings (Epic 7) or findings without enrichment
**When** they are ranked
**Then** licence issues sit in the Licences group (no severity; hidden at 0) and issues without enrichment take an explicit place in their severity group (documented in the amendment), never by accident of nulls; an issue with no severity sits in Not rated yet, never in Low.

### Story 5.2: Issues list — severity groups, filters and the Home summary

As a SecOps engineer,
I want an Issues surface that lists every open issue grouped by severity,
So that I have one place to review the fleet's issues.

**Acceptance Criteria:**

**Given** the open question Q5 (the URL value of the Needs attention filter option, and whether Review all N clears the type filter and search; the walk order is already decided — `needs_attention=true` keeps the Issues order, architecture.md → Issues and review; sprint-change-proposal-2026-11-07-readiness.md)
**When** this story is planned
**Then** the decision is recorded in EXPERIENCE.md (Issues → Filters) and approved by the user before implementation.

**Given** the Issues surface
**When** it loads
**Then** the list column shows "Issues" and a summary line ("3 need attention today. 312 not reviewed yet."); issues (one vulnerability or licence in one package version, across its places — UX-DR39) grouped Licences (hidden at 0), Critical, High, Medium, Low, Negligible (hidden at 0) and Not rated yet (hidden at 0), each with its count; standard rows (name + version · severity · Actively exploited · where; right column the review-status chip, and "Mixed · N of M" once Story 5.8 adds per-software decisions); "N more High" rows for long groups; the pager "1–25 of 312 · page 1 of 13" (25 per page, never infinite scroll); and coverage-gap rows in place (UX-DR9, UX-DR11, UX-DR26, ARCH38)
**And** the order is stated above the list in words: "Actively exploited sorts first in each group"; EPSS is never shown.

**Given** the filters — the type segmented control All · Vulnerabilities · Licences with counts ("Licences 0" stays visible), the Review status filter listing **Needs attention** — the issues counted as Needs attention (`needs_attention=true`, ARCH38), with that count — above the five statuses with counts (default Not reviewed yet) and the search field ("Find a package or vulnerability", `/`)
**When** applied
**Then** they narrow the list server-side with the grouping and order preserved, and the active scope is stated above the list; a Mixed issue matches every status any of its places has (decided 2026-11-07; ARCH38); counts count issues, not places; the Needs attention option's count is always the fleet-wide Needs-attention number, whatever the type filter and search (UX-DR38)
**And** at 0 it reads "No issues are waiting for review." with the coverage scope and the grey Show all statuses; a search with no match reads "No issues match "<text>" with these filters." with the grey Clear search (UX-DR45).

**Given** Home's Open issues summary and Needs attention from Story 2.10
**When** this story lands
**Then** they use the same groups, order and counts, and the Needs-attention count is the same number on Home, in the Issues summary and on the sidebar badge (UX-DR38).

**Given** the keyboard
**When** the user presses `J`/`K` or clicks a row
**Then** the next or previous issue is selected (`aria-current`), announced, and fills the detail column (tabs Review · Exposure · History, "1 of 3 · J K" at the bar's end) while the list keeps its place; every row action is reachable without a pointer; the Exposure and History tabs are not drawn (EXPERIENCE Open item 15).

### Story 5.3: Record triage decisions as evidence

As an analyst,
I want to record a status and justification on a finding,
So that handling is documented once and shows up everywhere it matters.

**Acceptance Criteria:**

**Given** an analyst or admin, using the decision API (the form arrives in Story 5.4)
**When** they `POST` a decision with status (`not_affected` / `mitigated` / `accepted` / `fix_planned`) and a justification — required for `not_affected`, `mitigated` and `accepted`, optional for `fix_planned` (D7)
**Then** it is stored with author, UTC timestamp and UUIDv7, and appended to the evidence ledger in the same transaction (FR14, NFR11, ARCH15)
**And** a missing required justification or a status outside the locked enum is rejected with 422
**And** the UI shows the statuses as Not impacted, Mitigated, Risk accepted and Fix planned, and the derived `untriaged` as Not reviewed yet; the API enums, exports and VEX keep the technical terms (ARCH15).

**Given** an existing decision
**When** a new decision is recorded for the same issue
**Then** it supersedes the old one; both remain in history, and there is no update or delete endpoint
**And** every decision in this story has scope All places (`all_places`): this vulnerability or licence in this package version on every piece of software that has it, including software found later (FR14, ARCH38); the issue-wide status is the latest All places decision, or Not reviewed yet when there is none; per-software decisions ("Only this software") arrive in Story 5.8.

**Given** an auditor
**When** they attempt to record a decision
**Then** the API returns 403 (Story 5.4 keeps the review panel absent for auditors).

**Given** a recorded decision
**When** Home, Issues, Software detail and the posture API render
**Then** they show the current status and use it in counts, counting issues, not places (for example "2 Critical not reviewed yet"), consistently across every surface (FR14 propagation)
**And** the findings API returns the current decision on every finding, so other teams can consume it (FR14 team consumption; VEX export follows in Story 5.6, the `triage_status` metric label in Story 8.3).

**Given** a finding that is resolved by a feed update and later reappears
**When** it reappears
**Then** its previous decisions are still attached and visible.

### Story 5.4: Review panel in the Issues detail column

As an analyst working through a list,
I want to review an issue in the detail column without leaving the list,
So that review is fast and every decision has its reason.

**Acceptance Criteria:**

**Given** the open question Q5 (the URL value of the Needs attention filter option, and whether Review all N clears the type filter and search; the walk order is already decided — `needs_attention=true` keeps the Issues order, architecture.md → Issues and review; sprint-change-proposal-2026-11-07-readiness.md)
**When** this story is planned
**Then** the decision is recorded in EXPERIENCE.md (Issues → Filters) and approved by the user before implementation.

**Given** the Issues list
**When** an issue is selected
**Then** its Review tab shows the summary (title, severity, Actively exploited pill + KEV tag), the places count with "See the map", What to do, the review status, the review panel and the technical-details block (the vulnerability ID and its other aliases, KEV, CVSS, EPSS, source and check time, plus the order explanation from Story 5.1); decision history is on the History tab (not drawn, EXPERIENCE Open item 15) (FR8, FR12, FR13, UX-DR16).

**Given** the review panel
**When** the analyst answers "Does this vulnerability impact us?" (No, not impacted → Not impacted; Yes → "What will we do?": Fix it → Fix planned; Reduce the risk → Mitigated; Accept the risk → Risk accepted), each option showing the status chip it produces, and fills "Why? (shown in the audit report)" where required (every status except Fix planned)
**Then** Save and next ⌘↵ (lime, disabled at 0.45 until a question is answered) records the decision for All places (Story 5.3), updates the row's chip in place and selects the next issue in the current filter; Decide later moves on without recording; the hint reads "Saved with your name in the audit trail."
**And** status can never be changed inline in a list — only in the review panel.
**And** the panel has no scope control and no chip shows Mixed in this story; "Only this software" and "Mixed · N of M" arrive in Story 5.8 (UX-DR16, UX-DR39).

**Given** a save that fails
**When** the API returns an error
**Then** an inline error line in the panel names the problem ("Your decision wasn't saved: Armoury can't reach its database.") with Try again, announced with `role="alert"`; Save and next does not advance; the chosen options and "Why?" text stay filled in; no toast appears (UX-DR41).

**Given** the "Review" palette action and the Review buttons on Home, the Exposure inspector and Software
**When** used
**Then** they open the issue in Issues on its Review tab (decided 2026-11-07), and Home's lime "Review all N" opens Issues with the Review status filter set to Needs attention (Story 5.2), so Save and next walks only the issues that need attention (UX-DR6, UX-DR11, UX-DR22).

**Given** an auditor
**When** they open an issue
**Then** the summary, technical details and history show, and the review panel is absent (UX-DR31).

### Story 5.5: Audit trail in Reports and on every item

As a compliance lead,
I want to read the append-only audit trail of the whole fleet in Reports, and of any piece of software, issue or audit report,
So that I can see every scan, feed version and decision, and how corrections were made.

**Acceptance Criteria:**

**Given** Reports (`/reports`), whose first group this story adds
**When** the user opens **Audit trail**
**Then** it lists the whole fleet's ledger entries newest first with type, subject (plain label with its technical ID small in mono), actor, time and tool/feed versions, 25 per page with cursor pagination and a pager total, and filters by type, subject and time window (D9, UX-DR27)
**And** Reports shows only the groups that exist so far — Audit trail now; Exports arrive in Story 6.5 and Audit reports in Story 9.5 — and auditors see all of it.

**Given** a superseded entry
**When** it renders
**Then** both the original and the superseding entry are visible and linked; no edit or delete affordance exists anywhere (NFR11, UX-DR36).

**Given** the chain verification from Story 2.1
**When** Reports → Audit trail renders
**Then** it shows the current verification result ("Chain intact — N entries, verified 4 min ago") or the first broken entry, named in plain words with a link to it; the layout and wording of the broken-chain state are set by UX before Build (O16); Stories 9.6 and 9.9 add the checkpoint and anchoring status to the same group.

**Given** a piece of software, an issue or (from Story 9.5) an audit report
**When** the user opens its Audit trail tab (Software, Reports) or History tab (Issues; not drawn — EXPERIENCE Open item 15)
**Then** it lists that subject's entries newest first under "Entries are never edited or removed.", with a link that opens Reports → Audit trail filtered to that subject.

### Story 5.6: Emit VEX from review decisions

As a SecOps engineer,
I want our triage decisions exported as standard VEX,
So that downstream consumers and auditors get machine-readable handling statements.

**Acceptance Criteria:**

**Given** the VEX-format decision (ARCH29, agreed 2026-11-04, recorded in `architecture.md`)
**When** this story lands
**Then** OpenVEX and CycloneDX VEX are both supported and the user picks the format per export; CSAF VEX is deferred until a customer needs it.

**Given** the open VEX status-mapping decision (ARCH29)
**When** this story is planned
**Then** the mapping of the locked statuses to each format's states and justifications — including `accepted` and `fix_planned`, and a `fix_planned` decision with no justification, whose action statement comes from the planned fix ("Update log4j-core to 2.17.2") (D7) — is recorded as an amendment to `architecture.md` and approved by the user before implementation.

**Given** decisions on an artifact or across the fleet
**When** VEX export is requested for a scope
**Then** a valid document in each agreed format is produced, mapping the locked statuses to the format's states and justifications, with author and timestamp (FR15); when an issue is Mixed, each product's statement carries its own effective status — its per-software decision if present, else the All places decision (ARCH38); in the UI the file is listed as "review decisions (VEX)"
**And** emitted documents validate against the format's published schema in tests.

**Given** an `accepted` or `fix_planned` decision
**When** it is mapped to a format with no direct equivalent
**Then** it follows the approved status-mapping amendment above, never silently dropped.

### Story 5.7: Ingest vendor VEX

As a SecOps engineer,
I want to import vendors' VEX documents and apply their not-affected claims,
So that upstream knowledge reduces noise — with credit to who said it.

**Acceptance Criteria:**

**Given** an admin or analyst
**When** they upload a VEX document in an agreed format (Story 5.6) through the UI or the API (this also serves air-gapped instances)
**Then** it is validated, stored with its source/author, and appended to the evidence ledger; invalid documents are rejected with the reason (FR15).

**Given** a vendor statement
**When** Armoury matches its product to the fleet
**Then** it uses exact identifiers only, in this order: image digest; purl with version; purl without version — no fuzzy name or CPE matching (architecture.md, Vendor VEX matching)
**And** a statement with no fleet match is stored and shown as "no fleet match", never dropped, and each applied match records the rule that matched.

**Given** a vendor `not_affected` statement matching a fleet finding (product and vulnerability)
**When** it is applied
**Then** the review panel shows the vendor claim with its source ("Not impacted — per <vendor> VEX, <date>"), distinct from the team's own decisions; the claim is display-only — it never sets the issue's status, its counts, a Review status filter match or Needs attention, and the place stays Not reviewed yet until a person records a decision (ARCH38)
**And** VEX export (Story 5.6) states only people's decisions; a vendor claim is never emitted as Armoury's statement.

**Given** the Issues Review tab
**When** an issue has vendor VEX
**Then** it shows the vendor, statement, justification, document and the matching rule (UX-DR16); the presentation is not drawn (EXPERIENCE Open item 17) and is designed before this story starts Build.

**Given** a later vendor document that withdraws or changes a claim
**When** it is ingested
**Then** the change supersedes the earlier claim, the review panel shows the current claim, and history is kept; no status changes, because a claim never set one.

### Story 5.8: Review scope — all places or only this software

As an analyst,
I want one decision to cover every place an issue affects, or only one piece of software,
So that I do not repeat the same decision on every piece of software.

**Acceptance Criteria:**

**Given** the decision API from Story 5.3, where every decision covers All places
**When** an analyst records a decision
**Then** they can choose **Only this software** (scope `artifact`: one piece of software, pre-filled when Review was opened from it) instead of the default **All N places** (D6, Story 5.3: this vulnerability or licence in this package version, across every piece of software that has it, including software found later)
**And** the decision is stored and appended to the ledger exactly as in Story 5.3.

**Given** a fleet-wide decision and a per-artifact decision on the same finding
**When** the current status is computed
**Then** the per-artifact decision overrides the fleet-wide one for that artifact, and superseding an All-places decision leaves per-software decisions in place, and the panel says how many keep theirs ("2 places keep their own status"; decided, ARCH38; EXPERIENCE Open item 9 resolved).

**Given** the review panel from Story 5.4
**When** it opens on an issue
**Then** it shows the decision that applies now and its source in plain words (for example "All places — Priya, 3 Nov" or "Only this software — differs from the other places"; copy to confirm with UX) (UX-DR16)
**And** the scope segmented control above the questions offers "All N places" (default) and "Only this software" (which reveals a select of the places), with the number of places the choice changes now; a failed save keeps the chosen scope with the other answers (UX-DR41)
**And** the findings API and VEX export (Story 5.6) use the resulting current status per place; the row's chip shows that status, or "Mixed · N of M" when N > 0 (issue-wide status = the latest All places decision, or Not reviewed yet when there is none; N = places whose own per-software decision differs from it; M = the place count; accessible name "Mixed: 3 of 14 places have a different status"; when N equals M the chip reads "Mixed" with no count, accessible name "All M places have their own status"); an issue stays Not reviewed yet and in Needs attention while any place is Not reviewed yet (UX-DR38, UX-DR39, ARCH38).

## Epic 6: Blast radius and graph exploration

On CVE day the engineer types a CVE ID or `package@version` into ⌘K and within seconds sees on Exposure which software has it, deployed and not deployed, and where it runs — answered in words first, then as a map or a table, with "Answered N min ago" and "How we know" — exports it (stored as evidence in Reports → Exports), and moves the map to any node to explore further.

### Story 6.1: Graph projection of inventory and findings

As a SecOps engineer,
I want the fleet's CVEs, packages, artifacts and workloads connected in one graph,
So that blast-radius and exploration queries are traversals, not ad hoc joins.

**Acceptance Criteria:**

**Given** relational inventory, SBOM packages, findings and running records
**When** they change
**Then** the AGE graph is created and updated from the relational tables in the same transaction or by a transactionally enqueued job — vertices `Cve`, `Package`, `Artifact`, `Workload`, `Cluster`; edges `AFFECTS`, `CONTAINS`/`DEPENDS_ON`, `RUNS_IN` (ARCH2 naming)
**And** graph schema changes are versioned migrations, and the graph tables are marked "not evidence" (the relational tables hold the history, ARCH32).

**Given** the relational tables are the source of truth
**When** `armoury graph rebuild` (or the admin API) runs
**Then** the graph is rebuilt from them, and a test asserts the rebuilt graph equals the incrementally maintained one on a fixture fleet (R1: the rebuild path is tested, not assumed).

**Given** the graph and relational data disagree (detected by a consistency check that runs once a day by default, Helm value)
**When** the check runs
**Then** the drift is reported as a health finding and the answer provenance carries a caveat until a rebuild completes.

### Story 6.2: Blast-radius query API

As a SecOps engineer,
I want to ask "who is affected by this CVE or package version?" and get a complete, honest answer,
So that I can tell the CTO the exposure before he's read the news.

**Acceptance Criteria:**

**Given** `POST /api/v1/blast-radius-queries` with a vulnerability ID (a CVE ID or any other alias, such as a GHSA ID; it matches every finding whose key ID or any alias equals it, ARCH38), a `package@version`, or a package with a version range (for example `log4j-core@2.x`), and `GET /api/v1/blast-radius-queries/{id}` to read it (long-operation pattern, ARCH33)
**When** it runs
**Then** the response has `status` (`running` / `completed` / `failed`), `progress` (artifacts evaluated of total) and the partial results so far; a fast query returns `completed` on the first response, so no second request is needed
**And** the completed answer contains affected packages, affected artifacts (shipped and running), and where each runs (cluster/namespace/workload), with counts for the answer headline (FR17)
**And** triage status and vendor VEX are included per finding, so not-affected decisions are visible in the answer.

**Given** any answer
**When** it is returned
**Then** it carries the `provenance` block: sources (registry-derived SBOMs, live inventory) with versions and freshness, coverage (artifacts in scope, scanned, unscanned, unmatched running digests, disconnected clusters) and `caveats[]` scoping the claim ("2 pieces of software haven't been checked yet and aren't on the map. This answer covers the 3,176 we have checked.") (FR17, ARCH14, NFR8).

**Given** no affected artifacts
**When** the answer returns
**Then** it is a coverage-scoped zero ("No software has it — across the N pieces of software we've checked (82%)"), only for a known vulnerability — `grype db search --vuln <ID>` returns affected packages for the queried ID or any alias of it — never a bare empty list.

**Given** an image digest as the query (PROC2)
**When** it runs
**Then** it answers from that artifact outward: the vulnerabilities that affect it (in Issues order, with review status), its vulnerable packages, and where it runs — with the same `provenance` block
**And** a digest that matches no artifact returns a coverage-scoped answer that says whether the digest runs somewhere unmatched (R7).

**Given** an unknown vulnerability ID (a CVE ID or any other alias) or malformed query
**When** it runs
**Then** the API returns a 422 envelope distinguishing "not a valid identifier" from "no record in the vulnerability data" — the active Grype DB has no record for the ID or any alias of it, even when the CVE List (Story 4.4) or another enrichment feed knows it — (with feed versions and their age); the UI never turns the second into "No software has it" (Story 6.3)
**And** the record check runs `grype db search --vuln <ID>` through `tools` against the active DB directory; Armoury never reads the Grype SQLite schema (architecture.md → Honest-degradation metadata)
**And** an ID is known only when that search returns affected packages for the ID or any alias of it; a record with no affected-package data gets the "no record in the vulnerability data" error (decided 2026-11-07).

**Given** a CVE that matches no fleet package
**When** it runs
**Then** the answer still includes the CVE's metadata from the Grype DB and CNA record (Story 4.4).

### Story 6.3: Exposure surface — answer and table, from ⌘K

As a SecOps engineer,
I want to type a CVE or package into ⌘K and land on the answer,
So that the log4shell moment takes seconds from anywhere in the product.

**Acceptance Criteria:**

**Given** the open question Q1 (whether the unknown-vulnerability state adds "Published <date>; package data is not available yet." when the CVE List knows the ID, with a reworded first sentence; sprint-change-proposal-2026-11-07-readiness.md)
**When** this story is planned
**Then** the decision is recorded in EXPERIENCE.md (State Patterns → Unknown vulnerability) and approved by the user before implementation.

**Given** the palette
**When** the user types a vulnerability ID (a CVE ID or any other alias, such as a GHSA ID) or `package@version`
**Then** an Exposure result ("Where are we exposed to log4j-core?") routes to Exposure with that query, and any alias of the same vulnerability gives the same answer (ARCH38); a fingerprint gives two results — its Exposure answer (Story 6.2) and its Software detail (UX-DR6).

**Given** an answer
**When** the surface renders
**Then** a full-width header shows "Exposure", the question, the query button showing the subject (it opens ⌘K), the Graph · Table switch, grey Export and "Audit report for this answer" (both Story 6.5), and the answer in words first ("14 pieces of software have it. 9 are deployed, 5 are not deployed.") with its meta line (Actively exploited pill, KEV tag, severity, CVSS, "Answered 38 min ago") and the deployed / not-deployed split; the list column holds Deployed N, Not deployed N and the "Not checked yet" gap row; the Table reading lists Software, Version, Deployed? (Yes/No), Where it runs, Copies, Severity and Review, deployed first, with sortable sentence-case headers and "N not checked yet, not listed"; a caveat line scopes the answer (UX-DR23, UX-DR15)
**And** Home's Exposure tab (a reduced summary with a button to the full page), See exposure, See the map and "See all 14 on the map" open Exposure for that query.

**Given** Exposure with a vulnerability ID Armoury has no data for (the Story 6.2 "no record in the vulnerability data" error: Grype DB has no record for it or any alias of it, or a record with no affected-package data — an ID is known only when `grype db search --vuln <ID>` returns affected packages — even if the CVE List already lists it)
**When** it renders
**Then** the answer reads "Armoury has no data for <ID> yet. Vulnerability data updated <age> ago." with the lime Check again (re-asks against the latest data; no rescan), with no map and no zero (UX-DR40).

**Given** a known vulnerability with no matches
**When** it renders
**Then** the coverage-scoped zero from Story 6.2 shows, with the unchecked remainder one click away (UX-DR40).

**Given** a fingerprint query
**When** the answer renders
**Then** the same surface centres on that piece of software: the answer in plain words names its open issues, the packages they come from and where it runs (as drawn for a moved map: "payments-api 3.4.1 has 2 open issues. It runs in 1 place, with 4 copies."), and the table lists its issues grouped by severity, Actively exploited first, with review status (UX-DR23); the copy for an unknown package or fingerprint is set by UX before Build (EXPERIENCE Open item 29).

**Given** a row in the answer
**When** the user chooses Review in the inspector
**Then** the issue opens in Issues on its Review tab (Story 5.4); the meaning of `t` is open (EXPERIENCE Open item 13).

**Given** a query whose operation is still `running` after 2 seconds
**When** the surface polls it (about every 1 s, ARCH33)
**Then** partial results appear from each poll with an explicit scope line built from `progress` ("Checking — 1,204 of 3,000 pieces of software so far"); never an unexplained spinner (UX-DR23, UX-DR32).

### Story 6.4: Exposure map reading

As a SecOps engineer,
I want the same answer as a four-tier graph,
So that I can see the path from the vulnerability to where it runs at a glance.

**Acceptance Criteria:**

**Given** an answer
**When** the user toggles to Graph
**Then** Svelte Flow renders a hairline map, left to right, with four tiers labelled in sentence case with counts — Vulnerability · Package · Software · Where it runs; circular nodes; deployed edges solid (`forest-2`); not-deployed edges dashed (`slate-dot`), with not-deployed software below a dashed rule labelled "Not deployed"; the selected path heavier (`forest-ink`) and the selected node lime with "Selected on the map"; only the vulnerability node takes clay (`clay-wash` fill, `clay-dot` ring, a pulse icon when actively exploited); edge labels ("direct · in 12"); soft bezier edges; the legend, zoom (+ / − / Fit) and the caveat line in a footer; no opacity on text (UX-DR17, UX-DR23).

**Given** a digest answer
**When** the user toggles to Graph
**Then** the map is centred on that piece of software with the same layout as a moved map (Story 6.6: its contents on the left, where it runs and its copies on the right) (UX-DR23, UX-DR24).

**Given** large result sets
**When** a tier exceeds the display limit (25 nodes per tier)
**Then** it rolls up as text nodes ("8 more", "5 more places") with expand-to-enumerate.

**Given** keyboard or screen-reader use
**When** the graph is focused
**Then** arrows/`Tab` move between nodes and show the focused node in the inspector, `+`/`−` zoom, each node's `aria-label` carries name, tier and state, the map has an `aria-label` summarising the answer, and the Graph/Table switch keeps the answer and the selection (UX-DR7, UX-DR34); `Enter` on a node moves the map (Story 6.6) and the node's detail opens from the inspector
**And** entrance/layout motion is disabled under reduced motion.

### Story 6.5: Export views as stored evidence, and the answer report

As a SecOps engineer,
I want to export what I see and have the export kept as evidence,
So that I can hand the CTO something he can trust without me annotating it, and anyone can later see exactly what was sent.

**Acceptance Criteria:**

**Given** an Exposure answer (on a moved map, its current centre), the Issues list or the Software list
**When** the user chooses Export (or presses `x`)
**Then** they get a CSV of the current view by default, with JSON as an option (PROC2), each carrying the same caveats and provenance as the screen ("The 2 not checked yet travel with the CSV and the audit report") (FR19, UX-DR21)
**And** a test asserts the export's caveats equal the API response's caveats.

**Given** an export
**When** it is made
**Then** the file is stored in the object store through `blob` (content-addressed), an insert-only export record and a ledger entry record who, when, the view and the query or filters, the format, the row count, the caveats and the file digest, and the export is listed in Reports → Exports, newest first ("Exposure: log4j-core 2.17.0 · CSV · 14 rows · from Exposure · 6 Nov") (FR19, ARCH39)
**And** stored exports have no edit or delete endpoint and follow the evidence-pack retention (default and minimum 24 months, ARCH30); the owning module is settled when the story is planned (O1).

**Given** Exposure
**When** the user chooses "Audit report for this answer"
**Then** the PDF answer report below is produced for the current answer (or the current centre of a moved map) and stored and listed in Reports → Exports like any export (D3).

**Given** an export that fails to start or to store
**When** it fails
**Then** the inline error with Try again appears in the Export row, nothing partial is stored or listed, and no toast appears (UX-DR41).

**Given** Reports with no exports yet
**When** the Exports group renders
**Then** it reads "No exports yet. Make one from Exposure, Issues or Software with Export." (UX-DR45).

**Given** the PDF report
**When** it is generated
**Then** it uses plain labels with the technical term beside them (machine-readable companions keep SBOM and VEX names), IBM Plex Mono for every ID, fingerprint and command, and the generation time, and is rendered by Typst — a pinned static binary run through `tools`, with no network access and the bundled IBM Plex Sans and IBM Plex Mono fonts ([ASSUMPTION] print face, EXPERIENCE Open item 5) — from a template in a named home reusable by evidence packs (Epic 9) (ARCH35)
**And** the pinned Typst binary is added to the control-plane image and verified against its published checksum
**And** the report follows DESIGN.md "Printed report": the print-only light palette (`print-*` tokens, independent of the app theme), A4 by default with US Letter as an option (PROC2), a footer with report ID, time window, generation time and page number on each page, severity as its word plus the 4-step marker and a colour (no red), body 9.5pt and tables 8.5pt, and table headers repeated on each page (UX-DR46).

**Given** an auditor
**When** they export
**Then** export is available (it is a read action), and their exports are stored and attributed like anyone else's.

### Story 6.6: Exposure map traversal and inspector

As a SecOps engineer,
I want to move the Exposure map to any vulnerability, package or piece of software and follow its connections,
So that I can answer questions the first answer doesn't ask directly.

**Acceptance Criteria:**

**Given** Exposure with no query (opened from the sidebar)
**When** it opens
**Then** the answer slot reads "Ask about a vulnerability, a package or a fingerprint." with examples ("CVE-2026-23012 · log4j-core@2.17.0 · sha256:…"), and the query button opens ⌘K (UX-DR40).

**Given** a node on the Exposure map
**When** the user clicks it or presses `Enter` on it
**Then** the map moves to that node: `GET /api/v1/graph/neighbours` returns bounded, paginated neighbours with provenance; the centre sits in the true centre, its contents on the left and where it runs and its copies on the right; the node you came from carries "Came from here"; packages with no known issues roll up ("212 more packages · No known issues") with a caveat line; and the map uses the Story 6.4 visual language with the centre-ring scale-in once (none under reduced motion) (FR17, FR18, UX-DR24)
**And** the question, query button, answer line, list column, Export, "Audit report for this answer" and the URL (`&from=` the previous step) follow the centre, so reloading or sharing the URL restores that map.

**Given** a moved map
**When** it renders
**Then** the trail above the map shows Back, the previous steps as link chips, the current step in bold and the hints "↵ Move the map · ⌫ Back"; Back, `Backspace` (outside text fields), any earlier step or the browser Back returns to that map with its selection; asking a new question with ⌘K starts a new trail (UX-DR24)
**And** the trail is a `nav` named "How you got here" with `aria-current="location"` on the current step; focus goes to the new centre and the new answer is announced politely ([ASSUMPTION], EXPERIENCE Open item 12).

**Given** a centre that is a package, a vulnerability other than the query, a place or a roll-up node, or a long trail
**When** this story is planned
**Then** their layouts follow the drawn software-centre rule and are confirmed with UX before Build (EXPERIENCE Open items 12 and 19).

**Given** a selected node
**When** it is selected
**Then** the inspector under the map pins it and shows identity (title with version and "Selected on the map"; Name, Fingerprint, Runs in, Copies, How it got it), What to do (the fix, the review-status chip, lime Review, grey Open software) and "How we know: Syft v… · Grype DB v… · checked N min ago"; on a map centred on a piece of software it adds Issues ("2 open: 1 Critical, 1 Low"), the lime action is Open software, Show only this stays grey and a hint reads "Click any node to move the map to it. Enter does the same from the keyboard."; `Esc` unpins (UX-DR18)
**And** hovering or focusing a node highlights its direct path.

**Given** an issue or piece of software elsewhere in the UI
**When** the user chooses See exposure, See the map or "See all N on the map"
**Then** Exposure opens for that subject (UX-DR11, UX-DR24); "Explore in graph" is retired, and the new meaning of `e` is open (EXPERIENCE Open item 13).

**Given** the Exposure map, moved or not
**When** Table is chosen
**Then** the current answer — on a moved map, the centre's neighbours: its issues, the packages they come from and where it runs — is fully readable as the Exposure table, keeping the selection (UX-DR34); the Table of a moved map is not drawn (EXPERIENCE Open item 19).

### Story 6.7: Prove sub-minute blast radius at the scale anchor

As the Armoury product owner,
I want blast-radius latency measured at the scale anchor,
So that NFR2 is known to hold before CVE day tests it for us.

**Acceptance Criteria:**

**Given** the Story 2.13 scale-anchor fixtures with up to ten clusters of running inventory
**When** a representative query set runs (widely used package, rare CVE, broad version range, no-match CVE)
**Then** p50 ≤ 5 s, p95 ≤ 30 s and every query completes in under 60 s, with graph traversal and provenance assembly timed separately (NFR2, ARCH28 R1).

**Given** the results
**When** the story completes
**Then** they are appended to the committed performance record, the query-latency SLO is exposed as a health signal (for Epic 8 metrics), and a miss is a blocking finding with mitigations (indexes, materialised paths, query rewrite) evaluated.

**Given** the load test
**When** it is invoked
**Then** it runs as its own mise task outside `mise run check`.

## Epic 7: License compliance

Grant evaluates every artifact against a fleet allow/deny policy. Violations and warnings appear as licence issues — no severity, a scale icon and a "Licence" tag (and the word "Warning" for warnings) — in the Licences group at the top of Issues and Home, and the team reviews them with the same decision model as vulnerabilities; only violations count toward Needs attention (D8). License data stays embedded, never headline: there is no license dashboard.

### Story 7.1: License evaluation of stored SBOMs with Grant

As a SecOps engineer,
I want the licenses of every artifact identified from its stored SBOM,
So that I know what licenses we ship without a second pipeline.

**Acceptance Criteria:**

**Given** a stored SBOM
**When** the license job runs
**Then** the `tools` module runs the pinned Grant CLI (`grant check`, JSON output) against the SBOM, with a timeout and stderr capture (FR26, ARCH7)
**And** the detected licenses per package (SPDX identifiers or expressions, plus unknown/unparseable values as-is) are stored with the Grant version and appended to the evidence ledger
**And** the pinned Grant binary is added to the control-plane image and verified against its published checksum; Grant runs only in the control plane (ARCH31, NFR12).

**Given** SBOMs stored before this story was deployed
**When** it is deployed
**Then** a one-time job evaluates every stored SBOM, and its backlog shows in the Checking band until it completes.

**Given** a new SBOM from Epic 2 onboarding
**When** it is stored
**Then** license evaluation runs automatically, in parallel with the Grype scan, not after it.

**Given** Grant fails on an SBOM
**When** the job ends
**Then** the artifact shows a license-evaluation failure with the reason and a retry, and counts as a coverage gap; it never shows as "no licence issues" (NFR8).

**Given** Software detail
**When** its Packages cell and Packages tab render
**Then** each package's licence shows as the licence marker (scale icon + SPDX ID in `text-2`), never in a severity colour, and the Packages cell carries one licence line ("All licences are fine to use." when nothing violates or warns) (UX-DR9, UX-DR25).

### Story 7.2: License evaluation of images and filesystems directly

As a SecOps engineer,
I want to run Grant against an image or a filesystem archive directly,
So that Armoury does not restrict what Grant can already check.

**Acceptance Criteria:**

**Given** the license evaluation source setting (PROC2)
**When** an admin configures it
**Then** they choose **SBOM** (default, no image pull) or **image** (Grant reads the image directly, with registry credentials in per-invocation env), fleet-wide or per connection (FR26).

**Given** an admin or analyst
**When** they upload a filesystem archive (for example a tarball of a build output) through the API or Settings
**Then** Grant evaluates it, the result is stored as an artifact of type `filesystem` with its content hash, and it flows into the same policy and findings as other artifacts
**And** the upload has a configurable size limit (default 2 GiB) and rejects path traversal and symlinks that point outside the archive.

**Given** both SBOM and image evaluation exist for one artifact
**When** its licenses render
**Then** each result shows its evaluation source, and differences are visible, not merged silently.

### Story 7.3: Fleet license policy

As an admin,
I want one fleet-wide allow/deny license policy,
So that license violations are judged the same way for every artifact.

**Acceptance Criteria:**

**Given** Settings → Policy (licence policy, admin only)
**When** an admin edits the policy
**Then** they can set an allow list, a deny list, and the treatment of licenses on neither list and of unknown licenses — each **violation**, **warning** or **ignore** (PROC2) (FR27)
**And** the default policy is unopinionated: an empty allow list and an empty deny list, licenses on neither list are `ignore`, and unknown licenses are `warning`, so a default install shows no violations until the admin sets a policy
**And** entries accept SPDX identifiers and expressions, and invalid entries are rejected with the reason.

**Given** a saved policy change
**When** it is saved
**Then** it is a new policy version appended to the evidence ledger (author, time, diff); earlier versions stay readable, and there is no per-team or per-artifact policy.

**Given** a new policy version
**When** it activates
**Then** license findings for the whole fleet are recomputed from stored license data without re-running Grant, and the backlog shows in the Checking band while it runs.

**Given** an analyst or auditor
**When** they open the policy page
**Then** they see the current policy and its history read-only; edit controls are absent (UX-DR31).

### Story 7.4: Licence issues in Home, Issues and review

As a SecOps engineer,
I want licence violations listed with vulnerability issues and reviewed the same way,
So that I can act on them before audit day.

**Acceptance Criteria:**

**Given** a package whose license violates the active policy
**When** license findings are computed
**Then** a `Finding` of kind `license_violation` is stored with the package, license, policy version and evaluation provenance (FR27, ARCH15)
**And** a license that the policy marks **warning** is stored as a `Finding` of kind `license_warning`.

**Given** the "triage license warnings" setting (PROC2)
**When** it is on (default)
**Then** license warnings are triageable exactly like violations
**And** when an admin turns it off, warnings stay visible but have no review panel, and existing decisions on warnings stay in history
**And** whether or not warnings are reviewable, only `license_violation` issues that are Not reviewed yet count toward Needs attention and the Issues badge; `license_warning` issues never do (D8, UX-DR38, ARCH38).

**Given** Home, Issues and Software detail
**When** they render licence issues
**Then** each sits in the Licences group at the top (violations and warnings together; hidden at 0), with the SPDX ID as the name, a "Licence" kind tag and the scale-icon licence marker, never a severity or an Actively exploited marker; line 2 of a Not-reviewed-yet violation reads "Licence · Needs a decision · <where>", and line 2 of a warning reads "Licence · Warning · <where>" (D8; styling per U19, O19); the Issues type filter All · Vulnerabilities · Licences keeps "Licences 0" visible (UX-DR9, UX-DR11, UX-DR26).

**Given** a license finding
**When** the analyst opens its Review tab
**Then** the same review panel, statuses, "Why?" rule, scope choice (All N places or Only this software) and evidence recording apply as for vulnerabilities (FR14, FR27, Story 5.3, Story 5.4, Story 5.8); the licence wording of the two questions is set by UX before Build (EXPERIENCE Open item 16)
**And** the technical-details block shows the policy rule that produced the issue instead of an order explanation.

**Given** the posture API
**When** it responds
**Then** license-finding counts are included alongside vulnerability counts, and license-evaluation coverage is in `provenance.coverage` (ARCH14).

## Epic 8: Fleet signals — Prometheus metrics and data quality

The team's own Grafana alerts on new KEV findings, coverage gaps, stale feeds and agent health. Every piece of software and the fleet get a data-quality (DQ) score that is explained by its five parts, shown in Software detail (this epic) and in the audit report detail and its printed cover page (Epic 9); not on Home and never in list rows (D2). Armoury sends no notifications itself: signals leave by Prometheus pull only.

### Story 8.1: Data-quality scoring model and artifact score

As a SecOps engineer,
I want each artifact to have a score for how trustworthy its data is,
So that I know how much to trust an answer, not only what the answer is.

**Acceptance Criteria:**

**Given** the open DQ scoring decision (ARCH29)
**When** this story is planned
**Then** the scoring model (dimensions, inputs, weights, 0–100 scale and letter-grade bands, including which grades count as low — the UX shows D and below in `dq-muted` as a placeholder, EXPERIENCE Open item 11 — and what is shown before a score exists, Open item 32) is recorded as an amendment to `architecture.md` and approved by the user before implementation; the five dimensions keep the plain UI names Package lists, Coverage, Freshness, Extra sources and Vulnerability records.

**Given** an artifact
**When** the `posture` capability computes its DQ score
**Then** the score uses the approved dimensions: SBOM depth and completeness, scan coverage, feed freshness, enrichment source coverage and CVE record quality (FR30)
**And** the same inputs always give the same score, proven by a test.

**Given** `GET /api/v1/artifacts/{id}`
**When** it responds
**Then** it includes the score, the grade and each dimension's value, inputs and source, so the score is explainable.

**Given** an input changes (new SBOM, feed update, enrichment refresh, agent state)
**When** the change is applied
**Then** the affected scores are recalculated without re-matching SBOMs.

**Given** the dimension weights (PROC2)
**When** an admin sets them through Helm values
**Then** the scores use those weights, and the approved defaults apply when no value is set
**And** every score response states the weight set that produced it.

### Story 8.2: Fleet data-quality score and the Software detail meter

As a SecOps engineer,
I want each piece of software and each audit report to say how much I can trust its numbers,
So that low-quality data is visible before someone acts on it.

**Acceptance Criteria:**

**Given** artifact scores
**When** the fleet score is computed
**Then** it aggregates the artifact scores by the rule in the approved model, and the posture API returns it in `provenance` with its dimension breakdown (FR30, ARCH14).

**Given** Home
**When** it renders
**Then** it shows no data-quality reading (D2; it may join the Home Details tab in a later UX update — EXPERIENCE Open item 14), while the posture API still returns the fleet score for evidence packs (UX-DR10, UX-DR22).

**Given** Software detail
**When** it renders
**Then** the Info list shows the data-quality value ("91 A−" in `dq`, accessible name in full), and the Data quality cell ("How much you can trust these numbers") shows the quality meter with the five parts, only the weakest emphasised and explained in one sentence with a link when there is something to do ("See them"), and the technical terms on one grey line and in `title` attributes (UX-DR10, UX-DR25)
**And** Software and Issues list rows carry no grade.

**Given** a low grade (bands from the approved Story 8.1 model)
**When** Software detail renders
**Then** the value and meter use `dq-muted`, keep their number and letter, never use opacity and never turn clay, amber or red; the two weakest parts each get one sentence of what it means; and a grey Check again (Story 2.11) is offered — a low grade takes no lime (UX-DR10, DESIGN.md).

**Given** blast-radius answers
**When** the API returns them
**Then** `provenance` includes the DQ scores of the software in the answer; Exposure shows no grade (D2 lists the surfaces).

### Story 8.3: Prometheus metrics endpoint

As a SecOps engineer,
I want posture signals exposed as Prometheus metrics,
So that my own Grafana alerts me with the observability stack I already run.

**Acceptance Criteria:**

**Given** the control plane
**When** Prometheus scrapes `/metrics`
**Then** it gets metrics for findings — the counter `armoury_findings_created_total{severity, kev}` (increases when a finding appears or becomes KEV-listed) and the gauge `armoury_findings_open{severity, kev, triage_status}` — so alerts compute "new" in Prometheus; and coverage gaps by kind, feed age and last update result per feed, agent state and last heartbeat per cluster, pipeline backlog per stage, fleet DQ score, blast-radius query latency (Story 6.7 SLO), ledger chain status, disk headroom and ledger and history partition runway in days (Story 2.1) (FR20, ARCH24, R9)
**And** metric names and labels follow Prometheus naming rules, and a test checks them with `promtool check metrics`.

**Given** label values
**When** metrics are exposed
**Then** labels are bounded (cluster, feed, severity, kind, stage), never per-artifact or per-CVE, so cardinality stays fixed at the scale anchor.

**Given** endpoint access (PROC2)
**When** an admin configures it in Helm values
**Then** they choose **bearer token** (default) or **no authentication on a separate metrics port** for in-cluster scraping
**And** the metrics never contain credentials, internal hostnames beyond cluster names, or SBOM contents.

**Given** the chart
**When** an admin enables the optional values
**Then** it installs a `ServiceMonitor` and a `PrometheusRule` with example alerts (new KEV finding via `increase(armoury_findings_created_total{kev="true"}[1h]) > 0`, untriaged KEV findings via `armoury_findings_open{kev="true", triage_status="untriaged"} > 0`, stale feed, disconnected agent, broken ledger chain); both are off by default (PROC2).

**Given** a triage decision recorded in Story 5.3
**When** Prometheus scrapes `/metrics`
**Then** the `triage_status` label on `armoury_findings_open` reflects it (FR14 team consumption).

**Given** Armoury
**When** any of these conditions happen
**Then** Armoury sends no email, webhook, toast or new-finding badge (the Issues nav badge counts Needs attention — decisions due — not new findings); the signal leaves only through `/metrics` (FR20, UX-DR36).

### Story 8.4: Prometheus panel in Settings → Signals

As an operator,
I want to see the metrics endpoint and the metric list in Settings,
So that I can wire Grafana without reading the source code.

**Acceptance Criteria:**

**Given** Settings → Signals
**When** it opens
**Then** it shows the endpoint URL, the configured access mode, and the list of exported metrics with their type, labels and help text, the endpoint URL in a code block with Copy and each metric with a Copy action (UX-DR28, UX-DR42)
**And** the panel is read-only for every role; configuration stays in Helm values.

**Given** the metric list
**When** a metric is added in code
**Then** the panel shows it without a UI change, because the list comes from the same registry that serves `/metrics`.

**Given** the bearer-token mode
**When** the panel renders
**Then** it states where the token comes from (the Secret name) but never shows the token.

## Epic 9: Signed CRA evidence packs

The compliance lead generates a CRA pack (an "audit report" in the UI) in one click from Reports for any past window. The pack is a PDF plus SBOM and VEX companions, states its own coverage and data quality, and is signed so an auditor can verify it offline. Packs draw only on evidence that Armoury already recorded. Retention is configurable but never below 24 months.

### Story 9.1: Point-in-time evidence queries for any window

As a compliance lead,
I want Armoury to tell me what the fleet state was at any past time,
So that any period the fleet was under management is reportable after the fact.

**Acceptance Criteria:**

**Given** the evidence ledger and stored history
**When** the `evidence` capability is asked for the state as of time T, or over a window T1–T2
**Then** it returns the inventory, SBOM versions, scans with tool and feed versions, findings, enrichment versions and triage decisions that were current at T, from the history tables and ledger only (FR23, ARCH32)
**And** it never uses data recorded after T to answer for T.

**Given** a time before the fleet was under management, or a gap in coverage
**When** it is queried
**Then** the answer states the gap explicitly with its start and end, instead of returning empty data.

**Given** a fixture ledger with known history
**When** the tests query several past times
**Then** the results match the recorded state at each time.

### Story 9.2: Pack architecture and the CRA pack definition

As the Armoury product owner,
I want packs built from framework definitions over the same evidence,
So that DORA, FedRAMP or PCI packs are additive later and CRA timing does not strand the work.

**Acceptance Criteria:**

**Given** the `packs` capability
**When** a pack definition is registered
**Then** it declares its framework, sections and the evidence queries each section uses, in a pack-definition collection (composition, ARCH25) (FR22)
**And** a test registers a second minimal test definition and proves it generates without changes to the pack engine.

**Given** the CRA definition
**When** a pack is generated for a window and scope
**Then** it has these sections: fleet inventory, proof of uniform scanning (single toolchain and versions), feed freshness over the window, findings with their handling decisions, and the license section (FR21, FR28)
**And** the license section draws from Epic 7 data and stays a section, never the headline.

**Given** a pack
**When** its cover sheet is built
**Then** it states the window, scope, coverage (in scope / scanned / gaps), data-quality score with its weight set, toolchain versions and the feed and enrichment versions used (FR21, FR30, R10).

**Given** a generated pack
**When** it is stored
**Then** its content, input evidence range and digest are recorded in the ledger, so the pack can be traced back to the evidence it used.

### Story 9.3: PDF report and machine-readable companions

As an auditor,
I want a polished PDF with machine-readable attachments,
So that I can read the pack and also check the data with my own tools.

**Acceptance Criteria:**

**Given** a generated pack
**When** its outputs are produced
**Then** the PDF uses the renderer from Story 6.5 and the DESIGN.md "Printed report" rules (print-only light palette, IBM Plex Sans text and Plex Mono for IDs — [ASSUMPTION] print face, EXPERIENCE Open item 5 — severity as word + 4-step marker, no red), with plain labels and the technical term beside them, and the cover sheet first: coverage ("Covers 3,176 of 3,847 (82%)", with the not-checked software listed), then the data-quality block ("84 B+", the five parts with plain names and the technical term beside each, and the lowest part named with its reason), then Signature and a sign-off line (FR24, FR30, UX-DR46)
**And** the story produces one sample CRA pack PDF from fixture data for user review before it is done.

**Given** the companions
**When** they are produced
**Then** the pack includes SBOMs for the artifacts in scope and VEX for the decisions in the window, in a smart default format (CycloneDX SBOM and OpenVEX) (PROC2)
**And** the user can choose SPDX or CycloneDX for SBOMs and OpenVEX or CycloneDX VEX for VEX.

**Given** the pack archive
**When** it is assembled
**Then** it contains the PDF, the companions and a manifest listing every file with its checksum.

**Given** companion files
**When** the tests run
**Then** each validates against its published schema.

### Story 9.4: Sign evidence packs

As an auditor,
I want every pack signed,
So that I can verify nothing was changed after it was generated.

**Acceptance Criteria:**

**Given** the `signing` module from Story 4.5
**When** a pack is generated
**Then** this story extends it to sign the pack manifest in the configured signing mode — `key` by default, with the operator key from the configured Secret, or a key the control plane generated on first start and stored in a named Secret when none was supplied (FR25, ARCH18)
**And** Settings → Signals shows the signing public key in use, and each public key is appended to the ledger so older packs stay verifiable after rotation.

**Given** an admin sets `signing.mode: keyless` (opt-in, PROC2)
**When** the control plane starts
**Then** it signs with a projected service-account token (audience `sigstore`) to public Fulcio, or to a configured private Fulcio, and records the signature in Rekor
**And** if the cluster's token issuer is not accepted (public Fulcio accepts only EKS, GKE and AKS issuers), startup fails with a clear message rather than at pack time.

**Given** air-gapped mode
**When** a pack is generated
**Then** it is signed with the operator-managed key from the configured Secret, and no network call is made (NFR4).

**Given** a signing failure
**When** generation runs
**Then** the pack fails closed and is not delivered unsigned.

**Given** a signed pack
**When** any byte of the manifest or any file changes
**Then** verification fails, proven by a test.

**Given** verification
**When** it runs, in the UI or by the offline command
**Then** it does not need internet access for operator-key packs, and keyless packs include the bundle needed for offline verification
**And** the signing mode and signer identity are recorded on each signature.

### Story 9.5: Generate audit reports and verify signatures in Reports

As a compliance lead,
I want one click to generate an audit report, with its signature checked for me,
So that the audit moment passes without a scramble.

**Acceptance Criteria:**

**Given** Reports or `⌘K`
**When** the user clicks the lime "Generate audit report"
**Then** generation starts at once as a long operation (ARCH33) with smart defaults (last 12 months as the window, the whole fleet as scope, CRA as the framework), with no wizard first (UX-DR20)
**And** the user can change the window, scope and framework after the click, which regenerates the pack.

**Given** generation in progress
**When** the user keeps browsing
**Then** progress shows per section from the operation's `progress`, polled about every 1 s; a failed section fails the pack closed and names the section, and retry re-runs only failed sections; the report appears in Reports → Audit reports when signed; a failure to start shows the inline error with Try again in the Generate row (UX-DR20, UX-DR41).

**Given** Reports with no audit reports
**When** it renders
**Then** the Audit reports group reads "No audit reports yet" with the lime Generate audit report (UX-DR45).

**Given** an audit report in Reports
**When** its Overview opens
**Then** row 1 shows Coverage when it was made beside Signature, and row 2 shows Data quality full width ("Data quality 84 B+ when it was made", the fleet quality meter with the weakest part and its reason, and the technical terms on one grey line) — the only place in the product the fleet five-part breakdown appears (FR30, UX-DR10, UX-DR27).

**Given** Home's "Across all software" band
**When** an audit report exists
**Then** its Audit report cell shows the latest report (last 12 months, signed, coverage) with Download and Preview, and on an all-clear Home the lime action is Audit report (UX-DR22, UX-DR45).

**Given** an audit report in Reports (detail tabs Overview · Files · Audit trail; files pack.pdf, sboms.tar.gz "Package lists … SBOM", vex.json "review decisions … VEX")
**When** its Overview opens
**Then** the Signature cell shows "Signature verified" with the signer key, and the offline command (cosign with the operator public key by default; the keyless command when keyless signing is enabled) in a code block with Copy — "Auditors can run this themselves, without Armoury."; when the signature does not verify, an error band names the file and the reason, links to the audit-trail entry for the signing, and hides no download (UX-DR19).

**Given** the auditor role and the default `rbac.auditorCanGeneratePacks: false` (Helm value, PROC2, PRD NFR6)
**When** an auditor opens Reports
**Then** they can view, download and verify packs, and the generate controls are absent (UX-DR31)
**And** the pack-generation API returns 403 for auditors.

**Given** an admin sets `rbac.auditorCanGeneratePacks: true`
**When** an auditor opens Reports
**Then** they can also generate packs, and the resolved auth configuration in Settings shows the setting read-only
**And** the Story 1.4 route-role test covers the pack-generation route for auditors with both values
**And** auditors can never change triage, policy or Settings.

**Given** an Exposure answer
**When** the user chooses "Audit report for this answer"
**Then** the Story 6.5 PDF answer report is produced and stored in Reports → Exports (D3); no evidence pack is scoped to a single answer (UX-DR21; O3 confirmed by Daniel 2026-11-07).

### Story 9.6: Signed ledger checkpoints

As a compliance lead,
I want the evidence ledger sealed at regular intervals by a signature,
So that even a database administrator cannot rewrite history without detection.

**Acceptance Criteria:**

**Given** the checkpoint interval setting
**When** no value is set
**Then** a checkpoint is made daily; an admin can set another interval in Helm values (ARCH30, PROC2).

**Given** the interval elapses
**When** the checkpoint job runs
**Then** it appends a checkpoint entry with the chain head hash, entry count and covered time range, signed by the `signing` capability in the configured signing mode (Story 9.4) (NFR11, ARCH18)
**And** a signing failure leaves the previous checkpoint in force, is reported as a health signal and a `/metrics` value, and is retried; no unsigned checkpoint is ever written.

**Given** chain verification (Story 2.1)
**When** it runs
**Then** it also verifies every checkpoint signature and that each checkpoint matches the chain at its position
**And** a test that rewrites and fully recomputes the chain as a superuser makes verification fail at the first checkpoint after the change.

**Given** Reports → Audit trail (Story 5.5)
**When** it renders the verification result
**Then** it shows the latest signed checkpoint and its time, and gives a copyable offline verification command for checkpoints.

### Story 9.7: Retention with archiving to the object store

As an admin,
I want evidence older than the retention period moved out of the database but kept verifiable and reportable,
So that the database does not grow without limit and no past window becomes unreportable.

**Acceptance Criteria:**

**Given** the retention setting
**When** no value is set
**Then** retention is 24 months; an admin can set a longer value in Helm values or Settings → Policy (retention), and any value below 24 months is rejected by the API and is not offered in the UI (FR23, UX-DR28, PROC2).

**Given** a monthly ledger or history-table partition (ARCH32) that is wholly older than retention and covered by a signed checkpoint
**When** the archive job runs as the maintenance CronJob with the `armoury_owner` login (the control-plane pod never holds that login)
**Then** it exports the partition to the object store as a compressed archive segment, verifies the segment against the checkpoint, appends a ledger entry with the segment digest through the same ledger append function as the control plane, which serializes appends with a PostgreSQL advisory lock so the hash chain stays in order, and only then drops the partition (ARCH30)
**And** if any step fails, the partition stays in place and the failure is reported; `armoury_app` still has no DELETE grant, proven by the Story 2.1 test.

**Given** an archived window
**When** a point-in-time query (Story 9.1) or a pack (Story 9.5) covers it
**Then** it reads the archive segment, verifies it against its checkpoint first, and returns the same result as before archiving — proven by a test that archives a fixture partition and compares the answers.

**Given** chain verification after archiving
**When** it runs
**Then** it starts from the oldest hot checkpoint and reports intact; each archive segment can also be verified on its own with the offline command.

**Given** the archive segments
**When** this story is done
**Then** they are kept forever; SBOM compaction and the optional purge arrive in Story 9.8.

### Story 9.8: SBOM compaction and archive purge

As an admin,
I want stored SBOMs de-duplicated and an optional purge of very old archives,
So that object storage stays bounded without losing any evidence inside retention.

**Acceptance Criteria:**

**Given** historical SBOM blobs
**When** compaction runs
**Then** identical SBOMs are stored once (content-addressed) and an SBOM snapshot moves to the archive prefix of the object store 90 days after a newer snapshot replaces it (Helm value), with point-in-time answers unchanged — proven by a test that compares answers before and after compaction.

**Given** the archive purge option
**When** it is off (default)
**Then** archive segments are kept forever
**And** when an admin turns it on with a further period, segments older than retention plus that period are deleted, each deletion recorded as a ledger entry with the segment digest; nothing inside retention is ever removed (NFR11, PROC2).


### Story 9.9: Anchor ledger checkpoints in a Rekor transparency log

As a compliance lead,
I want each signed ledger checkpoint recorded in a transparency log that Armoury does not control,
So that an administrator who controls the cluster, the database and the signing key has a harder time rewriting history unseen.

**Acceptance Criteria:**

**Given** the setting `rekor.anchoring.mode`
**When** no value is set
**Then** it is `disabled`, and Armoury sends nothing to any Rekor (PROC2, NFR4)
**And** an admin can choose `external` (a Rekor URL and its public key in Helm values: the public `rekor.sigstore.dev` or a Rekor that another team runs) or `bundled` (the chart deploys `rekor-tiles` with the POSIX storage backend on its own persistent volume) (ARCH37).

**Given** the `rekor` section of the chart `values.yaml`
**When** an admin reads it
**Then** its comments state that `external` is recommended, because only a log outside the administrator's control can show a full rebuild; that `bundled` shows accidental damage, but an administrator of the same cluster can rebuild it; that with `bundled` an optional witness outside the cluster (`rekor.bundled.witnessPolicy`) is recommended but not required; and that each entry publishes only the checkpoint digest, its signature and the public key, and the public key links the entries of one installation.

**Given** `bundled` mode
**When** the chart is installed or upgraded
**Then** the Rekor log signing key is created once in a Secret and kept across upgrades, no witness is required, and the `rekor-tiles` image is pinned by digest and listed in the Story 10.3 mirror image list.

**Given** anchoring is enabled and a checkpoint is signed (Story 9.6)
**When** the anchoring job runs
**Then** the `signing` module submits the checkpoint digest, its signature and the public key as a `hashedrekord` entry through `tools` (the story confirms the Rekor v2 support of the pinned cosign CLI), and appends the returned inclusion proof and Rekor checkpoint to the ledger
**And** no evidence content, cluster name or internal URL is sent.

**Given** Rekor is unreachable or rejects the entry
**When** anchoring fails
**Then** the checkpoint stays valid, the anchor is marked pending and retried with the Story 2.2 backoff, a health signal and a `/metrics` value report pending anchors, and anchoring never blocks the ledger.

**Given** air-gapped mode
**When** anchoring is enabled
**Then** the public Rekor is refused at startup (a built-in public endpoint, ARCH19); `bundled`, or `external` with an admin-configured internal URL, works.

**Given** an anchored checkpoint
**When** verification runs in Reports → Audit trail or with the offline command
**Then** it checks the inclusion proof against the configured Rekor public key with no network access, and Reports → Audit trail shows the anchoring mode, the latest anchored checkpoint and any pending anchors
**And** a test that changes an anchored checkpoint makes verification fail, because the changed checkpoint no longer matches its Rekor entry
**And** evidence packs (Story 9.2) include the latest anchored checkpoint and its inclusion proof, so an auditor who keeps an earlier pack can detect a later rewrite.

**Given** the known limit of Rekor v2
**When** this story is done
**Then** `architecture.md` and the chart comments state that Rekor v2 returns no signed timestamp, so a full rebuild that is anchored again is found only by comparing with an earlier receipt or by monitoring the log for two checkpoints of one key that cover the same time range.

## Epic 10: Verifiable, air-gapped delivery of Armoury itself

Buyers can verify Armoury's own images, charts and feed bundles (cosign + SLSA provenance), and can run the whole product end to end with no internet access. A supply-chain security tool whose own supply chain cannot be verified is disqualified from its market (NFR7).

### Story 10.1: Signed, provenance-attested releases

As a buyer's security reviewer,
I want every Armoury release artifact signed and provenance-attested,
So that I can verify what I install came from Armoury's own build.

**Acceptance Criteria:**

**Given** a release tag
**When** `.github/workflows/release.yml` runs
**Then** it reuses the `build.yml` pipeline from Story 1.1 for the control-plane image (with the pinned Syft, Grype, Grant, cosign and Typst binaries), the agent image (agent binary only) and the Helm chart as an OCI artifact, tags them for the release in GHCR, signs each digest with cosign keyless, and attaches SLSA build provenance (NFR7, ARCH23)
**And** each image also gets an SBOM attestation generated by Syft.

**Given** the published artifacts
**When** the release workflow finishes
**Then** a verification job in the same workflow verifies every signature and provenance attestation from a clean runner, and fails the release if any check fails.

**Given** the release notes and `README.md`
**When** a reviewer reads them
**Then** they give copyable `cosign verify` and `cosign verify-attestation` commands with the expected identity and issuer.

**Given** Armoury's own images
**When** the release workflow installs the release in a temporary namespace of the dev cluster from an ARC runner, connects that instance to GHCR as a registry and lets it scan the release images
**Then** the result is published with the release, so Armoury reports on itself the same way it reports on a customer fleet
**And** the namespace is deleted when the run finishes.

### Story 10.2: Armoury-published signed feed bundles

As a SecOps engineer running an air-gapped Armoury,
I want ready-made signed feed bundles from Armoury,
So that I do not have to run my own connected bundle machine unless I want to.

**Acceptance Criteria:**

**Given** a scheduled publishing workflow
**When** it runs (default: daily)
**Then** it builds bundles with `armoury bundle create`, signs them with Armoury's bundle signing key and attaches SLSA provenance to each published bundle, signed with the same KMS bundle key (`cosign attest --key`), not keyless (FR10, NFR7)
**And** the bundle signing key is a long-lived key held in a cloud KMS that cosign supports (provider chosen in this story); the private key never leaves the KMS, and the workflow authenticates to the KMS with GitHub OIDC, so the repository stores no long-lived secret
**And** the chart adds Armoury's bundle public key to the Story 4.6 trusted-key list by default, so published bundles verify without extra setup; an operator can remove it (PROC2).

**Given** the published bundle variants (PROC2)
**When** an operator chooses one
**Then** they can pick **core** (Grype DB, KEV, EPSS and the full CVE List v5 snapshot — the whole core bundle is about 0.8 GB: Grype DB 190 MB plus CVE List v5 621 MB, measured 2026-11-04; OSV absent and stated as absent) or **full** (core plus the full OSV mirror)
**And** every published bundle is complete: it needs no earlier bundle, so any published bundle imports into any instance, including a fresh one or one that skipped days; operator-built bundles (Story 4.5) can still carry CVE List deltas
**And** a fleet-scoped OSV bundle is still built by the operator with `armoury bundle scope` (Story 4.5), because Armoury cannot see the fleet.

**Given** a published bundle
**When** it is imported
**Then** it verifies the bundle signature and the SLSA provenance offline with the bundle public key that the chart ships (no Sigstore trust root is needed), and it passes the same checks as an operator-built bundle (operator-built bundles keep the signature only); a test imports the latest published bundle into a fresh air-gapped instance, and a second test imports a bundle that is 7 days newer than the instance's active bundle.

**Given** the bundle signing key
**When** it is rotated
**Then** the chart ships the new and old public keys together for 12 months, and the release notes state the rotation.

### Story 10.3: Air-gapped installation from an internal mirror

As a SecOps engineer in a network with no internet,
I want to mirror everything Armoury needs and install from my own registry,
So that air-gapped install is as simple as connected install.

**Acceptance Criteria:**

**Given** each release
**When** it is published
**Then** it includes a list of every image the chart uses (control plane, agent, Postgres-AGE, SeaweedFS, and `rekor-tiles` for the optional bundled Rekor) by digest, and the documented commands to copy them and the chart to an internal registry (NFR4).

**Given** chart values
**When** an admin sets one registry override
**Then** every image in the chart, including the agent subchart, pulls from that registry by digest.

**Given** the two outbound endpoint classes (ARCH19)
**When** `mise run check` runs
**Then** a check fails if any module calls a built-in public endpoint (Grype DB, KEV, EPSS, OSV, CVE List, public Fulcio, public Rekor) other than `feeds`, `enrichment` and `signing`, or calls any endpoint that is not its own admin-configured connection (registries, package feeds, the OIDC issuer, a private Fulcio, a configured Rekor (ARCH37), proxies)
**And** in air-gapped mode no module calls a built-in public endpoint, proven by a test.

### Story 10.4: Prove the full air-gapped journey end to end

As the Armoury product owner,
I want the three user journeys proven with no internet at all,
So that "air-gapped is first-class" is a checked fact, not a claim.

**Acceptance Criteria:**

**Given** a temporary namespace of the dev cluster with a default-deny egress NetworkPolicy that allows only an internal registry and an internal package feed (the cluster CNI enforces and logs egress policy)
**When** the scripted run installs the control plane and agent from the mirror, signs in with the bootstrap admin, connects the registry and feed, and imports a bundle
**Then** Home and Software populate with issues, enrichment and runtime coverage within the 30-minute gate, with each step timed (NFR1, NFR4, UJ-1)
**And** the run records every attempted outbound connection and fails if any goes beyond the allowed internal endpoints.

**Given** the same instance
**When** the script runs a blast-radius query for a CVE in the bundle, records a triage decision, generates a CRA pack and verifies its operator-key signature offline
**Then** each step succeeds with no internet access (UJ-2, UJ-3, FR25).

**Given** the results
**When** the run completes
**Then** they are appended to the committed performance record, and the run is its own mise task outside `mise run check`, executed in CI on each release.

## Epic 11: Scan in CI and see the result in Armoury

A developer adds one optional step to a pipeline. The step submits the built artifact to Armoury. The server SBOMs, scans and license-checks it with the fleet toolchain, applies the fleet CI policy, and the step prints the verdict and a link to the artifact (that piece of software in Software; its grouping and verdict display are open — UX-DR48). The CI runner never scans: it only identifies the artifact or supplies its bytes (NFR12, ARCH31). Central scanning stays the default and needs no CI change (FR1). This epic builds on Epics 2, 4, 5, 6, 7 and 10: the verdict uses KEV status, triage decisions and license results; the CLI polls with the Story 6.2 long-operation pattern; Story 11.5 extends the Story 10.1 release workflow.

### Story 11.1: Submit a pushed image from CI by digest

As a developer,
I want one CI step to submit the image I just pushed,
So that Armoury scans it now with the fleet toolchain and gives me a link to the result.

**Acceptance Criteria:**

**Given** Settings → Access (CI tokens, admin only)
**When** an admin creates a token with a name and an optional expiry
**Then** the token is shown once and only its hash is stored; it can only submit CI scans and read their results, it is not a user and has no UI role, and it can be revoked (NFR6, FR31)
**And** creation and revocation are appended to the evidence ledger without the secret.

**Given** the CI routes (submit scan, read scan result)
**When** they are added to `openapi.yaml`
**Then** each declares `x-armoury-ci-token: true` as well as its user role, so the Story 1.4 route test covers them; a CI token gets 403 on every other route.

**Given** `armoury scan --image <ref@digest>` with the server URL and the token in environment variables
**When** it runs in a pipeline
**Then** the CLI sends only the image digest and build details (repository, commit, pipeline run URL); it contains and runs no Syft, Grype or Grant (ARCH31, ARCH36)
**And** the server matches the reference to a connected registry, pulls the image by digest with that connection's credentials, and runs it through the Epic 2 inventory → Syft → Grype/Grant pipeline.

**Given** an image reference that matches no connected registry
**When** it is submitted
**Then** the server refuses it with a 422 envelope that names the reason and points to upload mode (Story 11.2).

**Given** a large fleet backlog (for example the initial scan)
**When** a CI scan is queued
**Then** it runs at a higher queue priority, so it does not wait behind fleet work: a CI scan starts within 60 s of submission, even while the initial fleet scan runs, proven by a test.

**Given** build details from CI
**When** they are stored and shown
**Then** they are labelled "declared by CI", because the server cannot verify them
**And** the token never appears in argv, logs, API responses or the ledger.

### Story 11.2: Submit an artifact that is not in a connected registry

As a developer whose build output is not pushed to a connected registry,
I want to upload the built artifact itself,
So that it gets the same server-side scan.

**Acceptance Criteria:**

**Given** `armoury scan --upload <path>` with an OCI image archive or a package archive
**When** it runs
**Then** the CLI uploads the built artifact (never source code), and the server computes its digest or checksum itself, stores it in the object store through `blob`, and runs the same pipeline as Story 11.1 (FR31, ARCH36)
**And** if the CLI also declares a digest and it differs from the computed one, the submission is refused.

**Given** an upload
**When** it exceeds the configured size limit (Helm value, default 2 GiB, PROC2)
**Then** it is refused with the limit in the message.

**Given** a package archive upload
**When** it is unpacked for Syft
**Then** path traversal and links that point outside the folder are rejected (same rule as Story 2.6 and Story 7.2).

**Given** an uploaded artifact
**When** it is stored
**Then** it appears in Software with source "CI upload" (grouping and label set by UX before Build, EXPERIENCE Open item 28), and its stored bytes follow the evidence retention period.

### Story 11.3: Artifact identity and duplicate linking

As a SecOps engineer,
I want CI scans and registry discovery to land on the same artifact,
So that the inventory never shows one image twice.

**Acceptance Criteria:**

**Given** a submission
**When** the server identifies it
**Then** the identity is the image digest, or the package coordinates plus the archive checksum (ARCH36)
**And** the server derives the package coordinates itself from the archive metadata (for example `package.json`, wheel `METADATA`, `pom.xml`, `Cargo.toml`, `go.mod`); coordinates that the CLI declares are stored as "declared by CI" and never used as the identity (NFR12).

**Given** an artifact that already exists (for example from registry discovery)
**When** a CI scan submits it
**Then** no new artifact is created; the CI scan is added as a new source record, and the CI report says "already known — also in registry `<name>`".

**Given** an artifact first created by a CI scan
**When** registry discovery later finds the same digest
**Then** discovery links to the existing artifact instead of creating a second one.

**Given** an artifact whose content was already SBOM'd with the current Syft version
**When** it is submitted again
**Then** the server reuses the existing SBOM and findings rather than scanning the same content twice.

**Given** Software detail
**When** a piece of software has several sources
**Then** it lists each source record (registry, CI runs with their declared build details and times).

### Story 11.4: Fleet CI policy, server verdict and the CI report

As a SecOps engineer,
I want one fleet CI policy that the server enforces,
So that every pipeline is judged the same way and nobody can tune the result in the runner.

**Acceptance Criteria:**

**Given** Settings → Policy (CI policy, admin only)
**When** an admin edits it
**Then** they can set rules such as "fail on severity at or above <level>", "fail on KEV" and "fail on license violation"; the default policy is report only, so a new install fails no pipeline (PROC2)
**And** each saved policy is a new version appended to the evidence ledger (author, time, diff); analysts and auditors see it read-only.

**Given** a completed CI scan
**When** the server decides the verdict
**Then** it applies the active policy version to the server's findings for that artifact, using current triage decisions (a finding with a current `not_affected` or `mitigated` decision does not fail the policy) (FR14)
**And** a vendor VEX `not_affected` statement that matches the artifact exactly (Story 5.7 rules) never changes the policy result: vendor claims are display-only (ARCH38), so only a person's review decision keeps a finding from failing the policy; the CI report names a matching vendor statement as information (decided 2026-11-07)
**And** the CLI has no flag that changes the verdict; the verdict and policy version are appended to the ledger.

**Given** a submitted scan
**When** the CLI waits for it
**Then** it polls the CI-scan operation (long-operation pattern, ARCH33) and prints a short report: artifact, findings by severity, KEV findings, license violations, duplicate status, verdict, policy version and the Armoury URL of the artifact
**And** it always prints the URL, which lands on the piece of software in Software, including on failure or timeout; where the verdict and its history show in Software detail is set by UX before Build (EXPERIENCE Open item 28, UX-DR48).

**Given** the outcome
**When** the CLI exits
**Then** it exits `0` on pass, `1` on policy failure and `2` when there is no verdict (server unreachable, scan error, or timeout — configurable, default 10 minutes); after a timeout the scan continues on the server.

### Story 11.5: GitHub Action for CI scans

As a developer on GitHub Actions,
I want a ready-made action,
So that adding the CI scan is one step in my workflow.

**Acceptance Criteria:**

**Given** the published action
**When** a workflow uses it with the server URL, the CI token secret and an image digest or an upload path
**Then** it downloads the `armoury` CLI for its pinned version from the GitHub Release, verifies its checksum and its cosign signature, and runs `armoury scan` (Stories 11.1–11.4)
**And** a download whose checksum or signature does not verify fails the step and runs nothing.

**Given** a release tag
**When** the release workflow runs
**Then** it builds the standalone `armoury` CLI for Linux and macOS on x86-64 and arm64, and publishes each binary as a GitHub Release file with a checksum, a cosign signature and SLSA provenance (NFR7)
**And** the CLI contains no Syft, Grype or Grant (NFR12).

**Given** the repository
**When** the action is published
**Then** it lives in `action/` in this repository and uses the same version tags as the CLI.

**Given** a finished scan
**When** the step ends
**Then** it exposes the verdict and the artifact URL as step outputs, writes the CI report to the job summary, and passes or fails the step by the CLI exit code.

**Given** the README
**When** a developer reads it
**Then** it gives a copyable example workflow for digest mode and for upload mode.
