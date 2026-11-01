---
status: final
stepsCompleted: [1, 2, 3]
inputDocuments:
  - _bmad-output/planning-artifacts/prds/prd-Armoury-2026-06-11/prd.md
  - _bmad-output/planning-artifacts/prds/prd-Armoury-2026-06-11/addendum.md
  - _bmad-output/planning-artifacts/architecture.md
  - _bmad-output/planning-artifacts/ux-designs/ux-Armoury-2026-06-12/DESIGN.md
  - _bmad-output/planning-artifacts/ux-designs/ux-Armoury-2026-06-12/EXPERIENCE.md
---

# Armoury - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for Armoury, decomposing the requirements from the PRD, UX Design if it exists, and Architecture requirements into implementable stories.

## Requirements Inventory

### Functional Requirements

FR IDs are the PRD's stable IDs (FR29–FR30 were added at finalize and sit out of numeric sequence).

**Fleet Inventory**

- FR1: Registry connection — SecOps supplies container registry credentials; Armoury enumerates repositories and image digests with no CI changes.
- FR29: Package feed connection — SecOps connects package feeds and artifact repositories (language-ecosystem registries, internal mirrors); Armoury enumerates packages and SBOMs them uniformly.
- FR2: Central SBOM generation — Syft SBOMs for every discovered artifact, centrally and uniformly, with no per-repo configuration.
- FR3: Live cluster inventory — a cluster agent watches the Kubernetes API and maintains a live record of running image digests (cluster/namespace/workload), reported to the control plane.
- FR4: Shipped-vs-running reconciliation — registry artifacts and running workloads are linked in one inventory; "is this running anywhere?" is answerable per artifact.
- FR5: Coverage visibility — the inventory shows its own gaps: discovered-but-not-SBOM'd images, unreachable registries, disconnected agents.

**Consistent Scanning & Lifecycle Freshness**

- FR6: Uniform scanning — every SBOM is scanned by Grype with one fleet-wide configuration and policy; the same artifact always produces the same result.
- FR7: Feed-driven re-evaluation — when vulnerability feeds update, existing SBOMs are re-evaluated automatically, without rebuilds or manual rescans.
- FR8: Evaluation provenance — every finding records when it was last evaluated and against which feed versions.
- FR9: Continuous onboarding — newly discovered images/packages are SBOM'd and scanned automatically within one hour of discovery.
- FR10: Air-gapped feed updates — vulnerability and enrichment feeds can be imported as a signed offline bundle built on a connected machine.

**Enrichment & Prioritization**

- FR11: Multi-source enrichment — findings enriched from CISA KEV, EPSS, CNA records and OSV.
- FR12: Source attribution — every enrichment datum is labelled with its source and retrieval time.
- FR13: Risk-based prioritization — deterministic, explainable ranking: KEV-listed first, then EPSS-weighted severity; the UI can always show why a finding ranks where it does.
- FR14: Triage decisions as first-class data — status (not affected / mitigated / accepted / fix planned), justification, author and timestamp; decisions propagate to posture views, team consumption and evidence packs.
- FR15: VEX support — triage decisions are expressible as standard VEX; vendor VEX documents are ingested and their not-affected claims applied (with attribution) to fleet findings.

**Blast-Radius Query & Posture View**

- FR16: Fleet posture view — landing state: fleet summary of artifacts, findings by priority, coverage gaps and feed freshness.
- FR17: Blast-radius query — given a CVE ID or package+version, answer which artifacts (shipped and running) are affected and where deployed (cluster/namespace/workload), in seconds, with data provenance (sources, coverage, freshness).
- FR18: Artifact detail — SBOM contents, findings (vulnerability and license) with triage status, evaluation provenance and running locations.
- FR19: Shareable answers — blast-radius results and posture summaries export as report/CSV.
- FR20: Prometheus metrics — posture signals exposed as metrics (new critical/KEV findings, coverage gaps, feed freshness, agent health); pull-only, no notifications.
- FR30: Data-quality score — a score grading the trustworthiness of the underlying data (SBOM depth/completeness, scan coverage, feed freshness, enrichment source coverage, CVE record quality), at artifact and fleet level, in posture views and evidence packs.

**Compliance Evidence**

- FR21: CRA compliance pack — evidence report for a chosen time window: inventory, proof of uniform scanning and feed freshness, findings with handling decisions, license section; states its own coverage and data quality.
- FR22: Compliance packs as a layer — CRA is the first instance of a pack architecture (framework report definitions over the same evidence) so DORA/FedRAMP/PCI are additive.
- FR23: Evidence collected continuously, generated on demand — any period under management is reportable after the fact; configurable retention with a compliance floor (default ≥ 24 months).
- FR24: Auditor-consumable formats — PDF plus machine-readable companions (SBOMs, VEX).
- FR25: Signed evidence packs — tamper-verifiable; Sigstore keyless when connected, operator-managed keys when air-gapped; verification never requires internet.

**License Compliance**

- FR26: License evaluation — Grant across its full surface (SBOMs, container images, filesystems); defaults to Armoury-generated SBOMs without restricting Grant's capability.
- FR27: License policy — fleet-wide allow/deny policy; violations surface as findings in the same posture/artifact views, triagable with the FR14 model.
- FR28: License evidence — the license section of evidence packs draws from this data; embedded, never headline.

### NonFunctional Requirements

- NFR1: Time to value — `helm install` to first fleet-wide posture view in < 30 min by one SecOps engineer with no dev-team cooperation; posture live and visibly populating with an explicit coverage indicator; full initial evaluation within 24 h at the scale anchor. Product gate: anything that breaks it doesn't ship in the install path.
- NFR2: Query performance — blast-radius answers in seconds, under a minute worst case, at the scale anchor.
- NFR3: Scale anchor — hundreds of repositories, thousands of container images, up to ten connected clusters.
- NFR4: Deployment — self-hosted Helm chart into existing Kubernetes; fully air-gapped capable; no phone-home, nothing silently requiring internet.
- NFR5: Freshness — after a feed update (online or offline bundle), fleet-wide re-evaluation completes within one hour at the scale anchor.
- NFR6: Access control — OIDC SSO configured declaratively (env / Helm values / config file, never a UI wizard); bootstrap admin for first sign-in and IdP-outage recovery; OIDC optional at install; roles admin / analyst / read-only auditor.
- NFR7: Armoury's own provenance — images, charts and feed bundles signed and SLSA provenance-attested via Sigstore.
- NFR8: Honest degradation — disconnected agents, stale feeds and unscanned artifacts surface in posture and metrics; the posture never needs a caveat the UI doesn't already show.
- NFR9: Agent footprint — cluster agents lightweight and read-only: watch/list only, never cluster-admin.
- NFR10: Availability — single-instance control plane in v1 (no HA); loss of the control plane never loses recorded evidence.
- NFR11: Evidence integrity — the evidence store is append-only and tamper-evident; scans, feed versions and triage decisions cannot be silently edited or deleted.

### Additional Requirements

From `architecture.md` (revised 2026-11-01, Rust backend). IDs are local to this document.

**Starter / scaffold (→ Epic 1 Story 1)**

- ARCH1: **No off-the-shelf starter; a monorepo scaffold is the first implementation story.** Cargo workspace (`control-plane`, `agent`, `agent-proto`, resolver 3, Rust 2024); `web/` via `npx sv create web --template minimal --types ts --add tailwindcss` + `shadcn-svelte init` + `@xyflow/svelte`, `adapter-static` with SSR off; `cargo new` for control plane (`axum`, `tokio`, `sqlx` postgres/rustls/uuid/migrate) and agent (`kube` runtime+rustls, `k8s-openapi`, `tokio`); `agent-proto` lib with tonic/prost codegen from `proto/agent/v1`; `helm create charts/armoury` stripped to control-plane + agent subcharts; `Taskfile.yaml`; `api/openapi.yaml`; `.github/workflows/ci.yml`. Pin versions at init.

**Platform & data**

- ARCH2: PostgreSQL + Apache AGE is the single source of truth — relational tables, AGE graph for traversals, and separate schemas for inventory / evidence / graph; forward-only `sqlx migrate` migrations with the AGE graph schema versioned alongside.
- ARCH3: SeaweedFS (bundled, S3-compatible; external S3 opt-in) holds SBOM blobs and compacted historical snapshots, accessed only via the `blob` module.
- ARCH4: Jobs via River's Rust client `riverqueue` (pinned; fallback `graphile_worker`) with transactional enqueue (job inserted in the same transaction as its data).
- ARCH5: Evidence ledger — append-only, hash-chained rows in Postgres; no UPDATE/DELETE grants on ledger tables; corrections are superseding entries; ledger quota separated from operational state, with disk headroom exposed as a health metric (R5, R9).
- ARCH6: Re-evaluation is a feed-delta join — changed CVEs/ranges select the bounded subset of stored SBOMs, which are re-matched with `scan`'s Grype matcher; never a fleet rescan. The delta stage is measurable and backpressure is surfaced honestly (R2).
- ARCH7: Substrate tools module — Syft/Grype/Grant/cosign run as pinned CLI subprocesses bundled in the control-plane image through one `tools` module (timeouts, JSON decoding, stderr capture, version capture). Tool versions are recorded on every finding and evidence entry; credentials go via per-invocation env, never argv; `GRYPE_DB_AUTO_UPDATE=false`; bounded parallel worker pool. A long-lived Go matcher sidecar is allowed only if the CLI fails the NFR5 bar (R11).

**Agent**

- ARCH8: Agent transport is agent-initiated outbound mTLS gRPC streaming over `proto/agent/v1` (HTTPS long-poll fallback where proxies block gRPC); no inbound connections to prod clusters (R4).
- ARCH9: Agent recovery is stateless re-derive — relist from the K8s API on reconnect and let the control plane reconcile, with jittered reconnect and a bounded reconciliation rate (R3).
- ARCH10: **Open gap:** agent enrollment and identity bootstrap — how the one-line agent `helm install` obtains its mTLS identity, control-plane address and enrollment token. On the UJ-1 30-minute critical path; must be defined before the agent slice.
- ARCH11: Running digests unmatched to any connected source are surfaced as a first-class coverage row (R7).

**API & security**

- ARCH12: OpenAPI-first — `api/openapi.yaml` is the contract; server types are generated (`openapi-generator` rust-axum, fallback code-first `utoipa` with CI failing on spec diff), plus a generated TS client (`openapi-typescript`/orval). Generated code is never hand-edited.
- ARCH13: API conventions — `/api/v1/<plural-noun>`, snake_case JSON and query params, resources returned unwrapped, lists as `{items, page}` with cursor pagination (no offset), uniform `{error:{code,message,details}}` envelope, UUIDv7 IDs, RFC 3339 UTC timestamps, durations in integer seconds, `X-Armoury-*` custom headers.
- ARCH14: Mandatory `provenance` block (`sources[]`, `coverage`, `freshness`, `caveats[]` when partial) on every answer-bearing response (posture, blast radius, artifact, packs).
- ARCH15: Locked domain vocabulary and triage status set (`not_affected` / `mitigated` / `accepted` / `fix_planned`, derived `untriaged`) as typed enums in Rust, OpenAPI and TS.
- ARCH16: Auth — OIDC code flow (`openidconnect` crate), declarative config, bootstrap admin, httpOnly secure cookie session for the SPA; RBAC enforced in API middleware.
- ARCH17: Registry/feed credentials are envelope-encrypted at rest, with key material from a k8s Secret / Helm value.
- ARCH18: Signing via `cosign` — keyless + Rekor when connected, operator-managed keys when air-gapped; verification never requires internet (`sigstore` crate or cosign CLI).

**Air gap**

- ARCH19: Air-gap is an instance-mode flag that reshapes feed ingress, enrichment ingress and signing. All outbound network access funnels through `feeds`, `enrichment` and `signing` only.
- ARCH20: Offline bundles cover both vulnerability feeds **and** enrichment sources (KEV/EPSS/OSV/CNA). Bundles are atomically validated and signature-checked before they can drive re-evaluation; a partial or failed import fails closed as stale (R8). The enrichment bundle format is an open minor gap.
- ARCH21: Record enrichment/feed source versions on findings and pack covers, so later corrections are explainable rather than locked (R10).

**Delivery, CI, observability**

- ARCH22: Helm umbrella chart with control-plane and agent subcharts; Postgres-AGE and SeaweedFS bundled by default, external DB/S3 opt-in; values cover the air-gap flag, OIDC, retention and connections. The SPA is served by the control plane.
- ARCH23: CI/CD on GitHub Actions — `ci.yml` (rustfmt, `clippy -D warnings`, `cargo nextest`, web lint/tests) and `release.yml` (SLSA provenance + cosign-signed images, charts and feed bundles).
- ARCH24: Observability — Prometheus `/metrics`, pull-only; structured `tracing` JSON logs that never contain credentials or full SBOM payloads; no in-product notifications.

**Code & test patterns (apply to every story)**

- ARCH25: Locality of Behaviour — module-by-capability (`inventory`, `feeds`, `scan`, `reeval`, `enrichment`, `ranking`, `triage`, `license`, `posture`, `blastradius`, `graph`, `evidence`, `packs`, `signing`, `metrics`, `auth`, `agentgw`, `tools`, `postgres`, `blob`, `httpapi`); max 3 layers; explicit dependencies wired only in `main.rs`; no globals/singletons; traits only at the third occurrence; one `thiserror` enum per capability; no `unwrap`/`expect` outside tests/startup; no `unsafe`; no `utils/`/`helpers/`/`common/`; files 100–400 lines.
- ARCH26: Frontend — TanStack `svelte-query` for server state, Svelte 5 runes for local state, components co-located with their routes, shadcn-svelte primitives in `lib/components/ui`, and a table equivalent for every graph view.
- ARCH27: Tests co-located — `cargo nextest` + `#[sqlx::test]`; agent tested against a mocked kube client plus a kind cluster in CI; Vitest + Playwright (`web/e2e/`) for the SPA.

**Validation & open decisions**

- ARCH28: Performance validation — a load test at the NFR3 scale anchor for R1 (AGE blast-radius latency, NFR2), R2 (re-eval delta throughput, NFR5) and R11 (per-SBOM Grype subprocess cost), with the query-latency SLO surfaced through the NFR8 path from day one.
- ARCH29: Decisions to close before their dependent slice — FR30 scoring model and grade banding; FR13 exact ranking formula; FR15 VEX formats (decided 2026-11-04: OpenVEX + CycloneDX VEX, CSAF deferred); FR23 retention mechanism (decided 2026-11-04, see ARCH30).
- ARCH30: **Evidence retention mechanism — signed checkpoints, then archive** (decided by Daniel, 2026-11-04). (1) The ledger table is partitioned by month from its first migration. (2) At a configurable interval (default: daily), a checkpoint entry records the chain head hash, entry count and covered time range, and is signed by the `signing` capability (keyless + Rekor when connected, operator key when air-gapped). Signed checkpoints also detect a full-chain recompute by a database superuser, which the hash chain alone cannot. (3) When a whole monthly partition is older than the retention period (default and minimum 24 months) and is covered by a signed checkpoint, a separate maintenance role exports it to the object store as an archive segment (compressed, with its digest referenced by a ledger entry), verifies the segment against the checkpoint, and only then drops the partition. The application role keeps no DELETE grant. (4) Chain verification starts from the oldest hot checkpoint; archived segments verify independently against their checkpoint. (5) Point-in-time queries and packs for archived windows read verified archive segments, so the window stays reportable. (6) Archive segments are kept forever by default; an admin can enable a purge after a further configurable period, recorded as a ledger entry and never silent (PROC2, NFR11 "never silently deleted").

**Process constraint (project workflow, not architecture)**

- PROC2: **Offer options rather than forcing one approach, with smart defaults** (Daniel, 2026-11-04). Where more than one valid approach is available and supportable — scopes, formats, modes, sources, weights — make it a configurable option instead of picking one for the user. Every option has a smart default, so a default install needs no configuration at all; options are there for users who go looking for them, never a required setup step (protects NFR1). Stories record the default and the alternatives.
- PROC1: The scaffold story is readiness-enabling work. Agent Readiness (Linear INF-12) runs after it and must be ready before product stories start Build (the `bmad-build` / `bmad-code-review` readiness gate).

### UX Design Requirements

From `DESIGN.md` + `EXPERIENCE.md` (ux-Armoury-2026-06-12, both final). Token names refer to DESIGN.md frontmatter.

**Design tokens & theming**

- UX-DR1: Semantic colour token layer on shadcn-svelte CSS variables, with three dark themes shipped day 1 — Forge (default), High Signal, Gunmetal — using the exact DESIGN.md values (including `rail-*` and `data-quality`). Components reference semantic roles only and never theme-specific hexes. No light mode.
- UX-DR2: Typography tokens — Inter Display (hero-numeral 76/200, co-stat 34/200, page-title 23/500, answer-headline 21/300), Inter (body 14, body-dense 12, micro-label/eyebrow 10/600 tracked), IBM Plex Mono (mono-identifier 11.5, mono-meta 10.5). Every technical identifier is mono; numerals are `tabular-nums`; no invented intermediate sizes.
- UX-DR3: Shape, spacing and elevation tokens — rounded sm 5 / default 8 / md 9 / lg 12 / node 11; zone-gap 48–56, page-gutter 52, rail-width 58, data-row 30, stat-gap 44. Depth is tonal layering with 1px borders; shadows only on true overlays.
- UX-DR4: Theme switcher in Settings, a compact header affordance (swatch + name) and a `⌘K` action. Live preview on focus, instant apply with no reload, persisted per user server-side, Forge fallback for new users, no OS-preference detection.

**App shell & navigation**

- UX-DR5: App shell — 58px icon rail with 7 surfaces (Posture, Blast radius, Graph explorer, Artifacts, Findings, Evidence, Settings pinned bottom), active state mirroring the route (raised tint + 2px accent indicator) and tooltips on hover/focus; no top nav. Left-aligned heading block (eyebrow → title → subtitle ≤ 620px → 46×2px accent rule).
- UX-DR6: Command palette (`⌘K`/`Ctrl+K`, shadcn `Command`) — every product action invocable; typing a CVE ID, `package@version` or digest routes to a blast-radius answer; result groups Answers → Navigate → Actions → Recent; `aria-live` results; no-match copy "No matches. Try a CVE ID, package@version, or digest."; the Posture header search is the same palette, pre-scoped.
- UX-DR7: Keyboard map — `g`+`p/b/g/a/f/e` surface navigation, `t` triage drawer, `⌘Enter` record and advance, `Esc` close topmost layer, `e` explore in graph, `x` export, `?` shortcut map (also listed in Settings); graph: arrows/`Tab` traverse, `Enter` open, `+`/`−` zoom.

**Components**

- UX-DR8: Hero stat + co-stat band — at most one hero numeral per surface, co-stats in a hairline-divided band (never a KPI card grid), count-up on populate (stepped under reduced motion).
- UX-DR9: Finding marks — severity chip (uppercase micro label on a 0.13–0.16-alpha tint); KEV tag (mono, dark on critical, always adjacent to the CVE ID, never truncated away); license chip (neutral, never severity-hued); triage pill (outlined, locked status set + untriaged, status-hued per DESIGN.md).
- UX-DR10: DQ badge/score — always `data-quality` hue in every theme; 0–100 score with letter grade (grade-only in table rows); expandable to dimension breakdown; lower grades dim and never turn red; corrective action offered alongside.
- UX-DR11: Findings table — 30px rows, hairline rules, mono identifiers; default KEV-first then EPSS-weighted sort with the header sentence "KEV first, then EPSS-weighted. Severity alone does not rank."; row click or `t` opens triage drawer; row hover/focus reveals "Explore in graph"; pagination, never infinite scroll.
- UX-DR12: Coverage-gap row — inline at the position of the missing data; dashed warning styling; names counts and locations; not dismissible or collapsible; click-through to cause (unscanned artifacts, unreachable registry, disconnected agent, unmatched running digests).
- UX-DR13: Populating banner — warning-tinted, under the heading block on Posture/Artifacts whenever first-scan or re-evaluation backlog exists; states queue count and estimate; live progress; never modal or blocking.
- UX-DR14: Severity band — 30px stacked distribution with soft fills (0.6–0.85), 4px segment radius; segments click-filter the findings table; always scope-labelled ("scanned artifacts only").
- UX-DR15: Freshness strip — on Posture, Blast radius and Artifact detail; each feed (Grype DB, KEV, EPSS, CNA, OSV, SBOM index, runtime observation) with version and age in mono, success/warning coloured by threshold; each entry clicks through to its Settings page.
- UX-DR16: Triage drawer (shadcn `Sheet`, right) — ranking explanation, VEX context with vendor attribution, full provenance, and a decision form (status + required justification). Submitting records author/timestamp, updates the row in place and keeps the user in the list; `⌘Enter` records and advances, `Esc` closes. Status never changes inline.
- UX-DR17: Graph node/edge language — node-radius surface rect with mono identifier + meta line; severity hue only on the affected path; running = accent ring + pip + label; shipped-not-running = dashed, 0.5 opacity; soft bezier edges. Nodes focusable with `aria-label` (identifier + tier + state); hover highlights the direct path; selection pins.
- UX-DR18: Node inspector — right side panel in Graph explorer showing identity, knowledge and provenance, with actions open detail / view evidence / blast radius from here; `Esc` unpins.
- UX-DR19: Evidence pack card — in-UI "Verify signature" showing result + signer identity, plus a copyable offline verification command (cosign keyless, or operator-key equivalent when air-gapped).
- UX-DR20: Evidence pack generator — one-click "Generate CRA pack" with smart defaults (last audit window, whole fleet), configuration (window, scope, framework) after the click and never a wizard before; async progress per section; fails closed naming the failing section; retry re-runs failed sections only.
- UX-DR21: Export (report/CSV/evidence-pack report) from Blast radius and Posture always carries the same provenance footer and caveats as the on-screen answer.

**Surfaces**

- UX-DR22: Posture surface — heading block; hero + co-stats (including coverage and fleet DQ); severity band; findings table with inline coverage-gap rows; freshness strip; uniformity claim ("All N artifacts SBOM'd and scanned the same way — Syft vX · Grype vY"); zero states paired with coverage scope.
- UX-DR23: Blast radius surface — answer headline ("14 affected artifacts · 9 running · 2 clusters"); 4-tier left-to-right graph (CVE → packages → artifacts → clusters/workloads) with Graph/Table toggle; roll-up "+ N more" with expand; caveat chip; provenance footer stating re-evaluation recency; progressive streaming with a scope line; coverage-scoped zero.
- UX-DR24: Graph explorer — search-first empty state ("Start from a CVE, package, or artifact"); "Explore in graph" from any artifact, finding or CVE opens pre-centred on that node; every node resolves to its detail surface and its evidence.
- UX-DR25: Artifacts — list → detail with DQ header, SBOM contents, vulnerability and license findings with triage status, evaluation provenance, running locations and freshness strip.
- UX-DR26: Findings surface — ranked triage workbench (UX-DR11 + UX-DR16) including license findings with the same triage flow.
- UX-DR27: Evidence surface — append-only trail with no edit/delete affordances; corrections shown as superseding entries with both visible; pack list and generator.
- UX-DR28: Settings panels — registry connections, package feeds, agent install (copy-paste one-liner, read-only trust posture and the exact RBAC shown before install), feed-bundle import, license policy authoring, evidence retention (UI never permits below the 24-month floor), Prometheus panel (read-only endpoint URL + metric list with copy), theme, users/roles, read-only display of the resolved auth configuration, shortcut list.

**States**

- UX-DR29: Pre-setup empty Posture — heading block plus exactly two setup actions (connect registry, install agent) with mono copy-paste one-liners; no illustrations. Registry unreachable → error in Settings **and** a named coverage-gap row on Posture.
- UX-DR30: Degraded states — stale feed flips age to warning and adds a scoped posture caveat (reflected in DQ); disconnected agent shows last heartbeat with runtime data marked stale-as-of, not removed; air-gapped mode substitutes operator-key signing copy, shows bundle age and "import bundle", and has no phone-home affordances.
- UX-DR31: Read-only auditor — triage forms, pack-config edits and Settings mutations are absent (not disabled); all read surfaces and pack generation/viewing remain available.
- UX-DR32: Loading/errors — cold load uses shadcn `Skeleton` mirroring the real layout; API errors render the typed envelope `message`; never a bare or unexplained spinner.

**Voice, accessibility, platform**

- UX-DR33: Voice and vocabulary — calm, count-and-verb microcopy; definitive only when scoped to scanned data; locked glossary and lowercase triage statuses everywhere; identical words for auditor and analyst; all strings externalised from day 1 (no concatenation, no text in SVG).
- UX-DR34: Accessibility floor — WCAG 2.2 AA; full keyboard operability with visible focus rings and reading-order tab order; surface and live-change announcements via polite `aria-live`; severity/triage/running state never colour-only; `prefers-reduced-motion` honoured globally; every graph fully readable as a table.
- UX-DR35: Responsive/platform — ≥ 1280px primary; 1024–1279px tolerant degradation (tighter gutters, horizontal table scroll before columns drop, graph pans); < 1024px best-effort read-only; web only, last-2-versions evergreen browsers.
- UX-DR36: Banned patterns (enforced across all surfaces) — no in-product notifications, toasts-as-alerts or new-finding badges; no OIDC wizard; no evidence edit/delete; no infinite scroll on fleet tables; modal depth ≤ drawer + dialog; no hover-only affordances; no celebratory animation; at most one primary button per surface.

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
FR13: Epic 5 - Deterministic, explainable KEV-first/EPSS ranking
FR14: Epic 5 - Triage decisions as first-class data
FR15: Epic 5 - VEX ingest and emit
FR16: Epic 2 - Fleet posture view (extended by Epics 5, 8)
FR17: Epic 6 - Blast-radius query with provenance
FR18: Epic 2 - Artifact detail (extended by Epics 3, 5, 7, 8)
FR19: Epic 6 - Shareable answers (report/CSV export)
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
FR30: Epic 8 - Data-quality score

**NFR placement:** NFR1 E2 (gate checked again at E3) · NFR2 E6 · NFR3 load tests in E2/E4/E6 · NFR4 E1 (install), E4 (air-gapped feeds), E10 (end-to-end proof) · NFR5 E4 · NFR6 E1 · NFR7 E10 · NFR8 E2/E3/E4/E8 · NFR9 E3 · NFR10 E1 (durable volumes) · NFR11 E2 (ledger), E5 (superseding decisions), E9 (sealed packs).

## Epic List

Order follows the user journeys: UJ-1 (Epics 1–3), UJ-2 (Epics 4–6), UJ-3 (Epic 9). Each epic builds only on earlier epics. Epic 1 Story 1 is the scaffold; Agent Readiness (Linear INF-12) runs after it and before any further story starts Build (PROC1).

### Epic 1: Install, sign in, and the Armoury shell
A SecOps engineer installs the control plane with one `helm install`, signs in with the bootstrap admin (OIDC and the three roles optional via Helm values), and lands in the themed shell — rail, command palette, three themes — on an empty Posture page offering the two setup actions.
**FRs covered:** none (NFR-only delivery epic for the UJ-1 install/sign-in path) — NFR4, NFR6, NFR10; ARCH1, ARCH12, ARCH13, ARCH16, ARCH22, ARCH23 (ci.yml); UX-DR1–7, UX-DR29, UX-DR31–36.

### Epic 2: Fleet inventory and uniform scanning, shown as a populating posture view
The engineer connects a registry or package feed and watches Armoury enumerate, SBOM and scan the fleet with one Grype config, every scan recorded as evidence, while Posture and Artifacts populate live with gaps shown openly (minute 29, registry-side).
**FRs covered:** FR1, FR2, FR5 (registry/scan gaps), FR6, FR8 (scan time, tool versions), FR9, FR16, FR18, FR29 — NFR1, NFR3, NFR8, NFR11 (ledger); ARCH2–5, ARCH7, ARCH14, ARCH15, ARCH17, ARCH28 (R11).

### Epic 3: Running inventory from read-only cluster agents
The engineer installs the agent with a second one-liner; running workloads appear linked to registry artifacts so "is this running anywhere?" is answerable; disconnected agents and unmatched running digests surface as gaps.
**FRs covered:** FR3, FR4, FR5 (agent and unmatched-digest gaps) — NFR8, NFR9; ARCH8–11. First story closes the enrollment gap (ARCH10).

### Epic 4: Fresh, enriched findings, connected or air-gapped
When vulnerability or enrichment feeds update — online or by signed offline bundle — stored SBOMs are re-evaluated within an hour without rescans, and every finding carries source-attributed KEV, EPSS, CNA and OSV data.
**FRs covered:** FR7, FR8 (feed versions), FR10, FR11, FR12 — NFR4, NFR5; ARCH6, ARCH19–21, ARCH28 (R2).

### Epic 5: Prioritise and triage findings
The analyst works a KEV-first, EPSS-weighted findings list that explains each ranking, records justified decisions that propagate everywhere, and ingests and emits VEX.
**FRs covered:** FR13, FR14, FR15 — NFR11 (superseding decisions); UX-DR11, UX-DR16, UX-DR26, UX-DR27; ARCH29 (ranking formula, VEX formats).

### Epic 6: Blast radius and graph exploration
On CVE day the engineer types a CVE ID or `package@version` into ⌘K and within seconds sees affected artifacts, shipped and running, and where they run — as graph or table with a provenance footer — exports it, and explores further in the graph.
**FRs covered:** FR17, FR19 — NFR2; UX-DR17, UX-DR18, UX-DR21, UX-DR23, UX-DR24; ARCH28 (R1).

### Epic 7: License compliance
Grant evaluates every artifact against a fleet allow/deny policy; violations appear as neutral license findings in the same views and are triaged with the same decision model.
**FRs covered:** FR26, FR27.

### Epic 8: Fleet signals — Prometheus metrics and data quality
The team's own Grafana alerts on new KEV findings, coverage gaps, stale feeds and agent health; every answer carries an explainable data-quality score.
**FRs covered:** FR20, FR30 — NFR8; UX-DR10; ARCH24; ARCH29 (DQ scoring model, first story).

### Epic 9: Signed CRA evidence packs
The compliance lead generates a CRA pack in one click for any past window — PDF plus SBOM/VEX companions, stating its own coverage and data quality, signed and verifiable offline — with retention never below 24 months.
**FRs covered:** FR21, FR22, FR23, FR24, FR25, FR28 — NFR11; ARCH18, ARCH30 (signed checkpoints and archive); UX-DR19, UX-DR20.

### Epic 10: Verifiable, air-gapped delivery of Armoury itself
Buyers can verify Armoury's own images, charts and feed bundles (cosign + SLSA provenance) and run the whole product end to end with no internet access.
**FRs covered:** none (NFR-only) — NFR4 (end-to-end proof), NFR7; ARCH19 (air-gap funnel check), ARCH23 (release.yml).

## Epic 1: Install, sign in, and the Armoury shell

A SecOps engineer installs the control plane with one `helm install`, signs in with the bootstrap admin (OIDC and the three roles optional via Helm values), and lands in the themed shell — rail, command palette, three themes — on an empty Posture page. Story 1.1 is readiness-enabling work: Agent Readiness (INF-12) runs after it and must be ready before Stories 1.2+ start Build (PROC1).

### Story 1.1: Monorepo scaffold with an aggregate local gate and CI

As the Armoury developer,
I want the agreed monorepo scaffolded with one local check command mirrored in CI,
So that every later story — and Agent Readiness — has a real codebase, toolchain and feedback loop to build on.

**Acceptance Criteria:**

**Given** a fresh clone
**When** the developer runs the documented init/check task (`task check`)
**Then** a Cargo workspace (resolver 3, Rust 2024) builds `control-plane` (binary `armoury`), `agent` (binary `armoury-agent`) and `agent-proto` (tonic/prost codegen from `proto/agent/v1/agent.proto`) (ARCH1)
**And** `web/` is a SvelteKit app with Tailwind v4, shadcn-svelte initialised, `@xyflow/svelte` installed, `adapter-static` and SSR disabled in the root layout
**And** `charts/armoury` exists as an umbrella chart with `control-plane` and `agent` subcharts, `api/openapi.yaml` exists, and `Taskfile.yaml` orchestrates all of it
**And** tool and dependency versions are pinned (lockfiles committed; no floating `latest`).

**Given** the scaffold
**When** `task check` runs
**Then** it executes rustfmt check, `clippy -D warnings`, `cargo nextest`, web lint, `svelte-check` and Vitest, and fails non-zero on any failure (ARCH23, ARCH27)
**And** each Rust binary, the web app and the chart contain at least one trivial passing test or lint target so every check has something real to run.

**Given** a push or pull request
**When** `.github/workflows/ci.yml` runs
**Then** it runs the same `task check` gate as local and fails on the same conditions.

**Given** the repository root
**When** an agent or developer opens it
**Then** a `CLAUDE.md`/`AGENTS.md` states the Locality of Behaviour rules and layout from the architecture (ARCH25), and `README.md` documents the init and check commands.

### Story 1.2: Install the control plane with one Helm command, durable storage included

As a SecOps engineer,
I want to install Armoury into my existing cluster with one `helm install`,
So that I get a running control plane without tickets to the platform team.

**Acceptance Criteria:**

**Given** a Kubernetes cluster where the engineer has Helm rights
**When** they run the documented one-line `helm install` with default values
**Then** the control plane, bundled Postgres with Apache AGE and bundled SeaweedFS start, Postgres and SeaweedFS on persistent volumes (NFR10, ARCH2, ARCH3, ARCH22)
**And** the control plane runs forward-only `sqlx` migrations at startup, creates the AGE extension and graph, and reports ready on a health endpoint.

**Given** values that point at an external Postgres-AGE and an external S3 endpoint
**When** the chart is installed
**Then** the bundled database/object store are not deployed and the control plane uses the external ones.

**Given** the control plane pod is deleted and rescheduled
**When** it starts again
**Then** previously stored data is still present (durability check, NFR10).

**Given** the install with `airGapped: true`
**When** the control plane runs
**Then** it makes no outbound network connections (verified by a network-policy or egress-capture test), and the air-gap mode is exposed read-only via the API (NFR4, ARCH19).

**Given** the control plane is running
**When** a browser requests `/`
**Then** the control plane serves the static SPA build and `/api/v1/*` from the same origin.

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
**Then** sign-in fails with a generic message, the attempt is logged without the credential, and repeated failures are rate-limited.

**Given** no session
**When** any `/api/v1/*` endpoint other than sign-in/health is called
**Then** it returns 401 with the uniform `{error:{code,message,details}}` envelope (ARCH13).

**Given** a signed-in user
**When** they sign out
**Then** the session is invalidated server-side and the cookie cleared.

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
**Then** the API returns 403 with the error envelope, enforced server-side for every mutating route
**And** a test enumerates every mutating route in `openapi.yaml` and asserts its required role.

**Given** any role
**When** `GET /api/v1/auth/config` is called
**Then** it returns the resolved auth configuration with secrets redacted; there is no API to change it (no UI wizard).

### Story 1.5: Design tokens and the three themes

As a SecOps engineer,
I want the Forge, High Signal and Gunmetal themes with Armoury's typography,
So that the product looks like itself from the first screen and I can pick a high-contrast option.

**Acceptance Criteria:**

**Given** the web app
**When** it renders
**Then** semantic colour tokens map onto shadcn-svelte CSS variables with the exact DESIGN.md values for all three themes, including `rail-*` and `data-quality` (UX-DR1)
**And** a lint/test fails if any component references a raw hex or a theme-suffixed variable instead of a semantic role.

**Given** typography, shape and spacing tokens
**When** components use them
**Then** Inter Display, Inter and IBM Plex Mono are bundled locally (no CDN; works air-gapped), sizes match DESIGN.md exactly, and numerals use `tabular-nums` (UX-DR2, UX-DR3, NFR4)
**And** radii, zone gaps, rail width, data-row height and stat gap match DESIGN.md.

**Given** a signed-in user
**When** they change theme
**Then** it applies instantly without reload, persists per user server-side, and follows them to another browser; new users get Forge; no OS-preference detection (UX-DR4)
**And** an automated contrast check confirms AA for all text roles in Forge and Gunmetal and the AAA target for High Signal primary text.

### Story 1.6: App shell, navigation and the empty Posture page

As a SecOps engineer,
I want a consistent shell with the icon rail and an honest empty Posture page,
So that I can move between surfaces and immediately see what Armoury is waiting for.

**Acceptance Criteria:**

**Given** a signed-in user
**When** the app loads
**Then** a 58px icon rail shows the seven surfaces (Posture, Blast radius, Graph explorer, Artifacts, Findings, Evidence, Settings pinned bottom), with the active item mirroring the route, tooltips on hover and focus, and no top nav (UX-DR5)
**And** surfaces without content yet render the left-aligned heading block (eyebrow → title → subtitle → accent rule) and a calm "nothing here yet" line — no illustrations.

**Given** nothing is connected
**When** Posture loads
**Then** it shows the pre-setup heading block and states that no sources are connected yet (UX-DR29 base; setup actions arrive with Stories 2.2 and 3.2).

**Given** Settings
**When** it opens
**Then** it shows the theme picker, the read-only resolved auth configuration, the users/roles view and the keyboard shortcut list placeholder (UX-DR28 subset).

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
**When** automated accessibility checks (axe) run in `task check` and CI
**Then** there are no WCAG 2.2 AA violations on any shell route, and a newly introduced violation fails the gate (UX-DR34)
**And** the check is wired so later stories' routes are included automatically, not opt-in.

**Given** keyboard-only use
**When** the user tabs through the shell
**Then** every control is reachable with a visible focus ring, tab order follows reading order, and no affordance is hover-only (UX-DR34, UX-DR36).

**Given** navigation between surfaces
**When** the route changes
**Then** a polite `aria-live` region announces the surface name.

**Given** `prefers-reduced-motion: reduce`
**When** any transition would run
**Then** it is suppressed or reduced globally, via one shared motion setting rather than per-component checks.

**Given** UI copy
**When** a component renders text
**Then** the string comes from an externalised message catalogue, with no concatenated sentences and no text baked into SVG; a lint/test fails on hard-coded user-facing strings in components (UX-DR33)
**And** locked glossary terms and the lowercase triage status labels are defined once in the catalogue.

**Given** viewport widths ≥ 1280px, 1024–1279px and < 1024px
**When** the shell renders
**Then** it shows the full layout, the tolerant layout (tighter gutters, horizontal scroll before columns drop), and a best-effort read-only layout respectively, with nothing broken (UX-DR35).

**Given** the banned UI patterns (UX-DR36)
**When** the frontend guide and shared components are set up
**Then** the guide lists every banned pattern, and one shared overlay component allows at most a drawer plus one dialog, proven by a component test
**And** the shadcn `Toast` is used only to confirm a user's own action, never as an alert for new findings, and a lint/test fails on more than one primary button per surface or on celebratory animation classes.

### Story 1.8: Command palette and keyboard map

As a SecOps engineer working under pressure,
I want every action reachable from `⌘K` and the keyboard,
So that I never hunt through menus.

**Acceptance Criteria:**

**Given** any surface
**When** the user presses `⌘K` / `Ctrl+K`
**Then** the shadcn `Command` palette opens with groups Answers → Navigate → Actions → Recent, `Enter` fires, `Esc` closes, and results announce via `aria-live` (UX-DR6)
**And** it offers navigation to every surface and "Switch theme…" with live preview.

**Given** palette actions
**When** a later story adds an action
**Then** it registers into one palette action registry (composition, ARCH25), and a test asserts every registered keyboard shortcut also has a palette entry.

**Given** no match
**When** the user types an unknown term
**Then** the palette shows "No matches. Try a CVE ID, package@version, or digest." plus common actions.

**Given** the keyboard map
**When** the user presses `g`+`p/b/g/a/f/e`, `?` or `Esc`
**Then** they navigate, open the shortcut map, or close the topmost layer respectively, and the same map is listed in Settings (UX-DR7)
**And** shortcuts never fire while focus is in a text input.

## Epic 2: Fleet inventory and uniform scanning, shown as a populating posture view

The engineer connects a registry or package feed and watches Armoury enumerate, SBOM and scan the fleet with one Grype config, every scan recorded as tamper-evident evidence, while Posture and Artifacts populate live with gaps shown openly. Ranking here is severity-only and labelled as such; Epic 5 replaces it with KEV-first/EPSS ranking.

### Story 2.1: Tamper-evident evidence ledger

As a compliance lead,
I want every recorded event to land in an append-only, hash-chained ledger,
So that nothing Armoury later claims about scans, feeds or decisions can be silently edited.

**Acceptance Criteria:**

**Given** the `evidence` schema
**When** a capability appends an entry (type, subject, payload digest, tool/feed versions, actor, UUIDv7 id, RFC 3339 UTC time)
**Then** the entry stores the hash of the previous entry and its own hash, in the same transaction as the data it records (NFR11, ARCH5)
**And** the ledger table is partitioned by month from its first migration, so later archiving drops whole partitions (ARCH30).
**And** the application's database role has no UPDATE or DELETE grant on ledger tables, proven by a test that attempts both and fails.

**Given** a ledger with entries
**When** `GET /api/v1/evidence/verification` is called
**Then** it recomputes the chain and reports `intact` or the first broken entry
**And** a test that tampers with a row directly as a superuser makes verification report the break.

**Given** a correction is needed
**When** a capability records it
**Then** it is a new superseding entry referencing the original; the original stays readable.

**Given** ledger and operational data share Postgres
**When** the chart is installed
**Then** ledger storage has its own reserved quota/tablespace setting, and disk headroom for each is exposed through the health endpoint (R9).

### Story 2.2: Connect a container registry and enumerate its images

As a SecOps engineer,
I want to paste read-only registry credentials and see Armoury discover every repository and image digest,
So that the fleet inventory fills without any CI changes or dev-team help.

**Acceptance Criteria:**

**Given** the empty Posture page or Settings → Registry connections
**When** an admin adds a registry (URL, auth type, read-only credentials) and runs "Test connection"
**Then** the connection is validated before saving, and credentials are envelope-encrypted at rest with key material from the k8s Secret (FR1, ARCH17)
**And** credentials never appear in API responses, logs or subprocess argv.

**Given** a saved connection
**When** enumeration runs as a `riverqueue` job enqueued in the same transaction as the connection row (ARCH4)
**Then** repositories and image digests are recorded as artifacts (UUIDv7), each discovery appended to the evidence ledger
**And** enumeration is paginated and resumable so a large registry doesn't exceed the job timeout.

**Given** a registry that is unreachable or rejects credentials
**When** enumeration runs
**Then** the connection status shows the error and last success time in Settings, and the state is queryable for coverage reporting (FR5, NFR8); the job retries with backoff and never silently drops the registry.

**Given** an analyst or auditor
**When** they view Settings → Registry connections
**Then** they see connection status read-only; add/edit/delete controls are absent.

### Story 2.3: Central SBOM generation with Syft

As a SecOps engineer,
I want every discovered image SBOM'd centrally the same way,
So that the whole fleet has an inventory of its contents with no per-repo setup.

**Acceptance Criteria:**

**Given** a discovered image digest without an SBOM
**When** the SBOM job runs
**Then** the `tools` module runs the pinned Syft CLI (`syft <ref> -o syft-json`) with registry credentials in per-invocation env, a timeout and stderr capture (FR2, ARCH7)
**And** the SBOM is stored in the object store via the `blob` module, keyed by digest, with the Syft version recorded.

**Given** a successful SBOM
**When** it is stored
**Then** its packages are indexed for querying, and an evidence entry records digest, SBOM content hash and Syft version.

**Given** Syft fails or times out
**When** the job ends
**Then** the artifact is marked `sbom_failed` with the captured reason and retried with backoff; it stays visible as a coverage gap, not dropped.

**Given** many pending images
**When** SBOM jobs run
**Then** they use a bounded, configurable worker pool so the control plane stays responsive.

### Story 2.4: Uniform vulnerability scanning of stored SBOMs

As a SecOps engineer,
I want every SBOM scanned by Grype with one fleet-wide configuration,
So that the same artifact always produces the same findings and no team has a snowflake setup.

**Acceptance Criteria:**

**Given** connected mode
**When** the control plane starts with no vulnerability DB
**Then** the `feeds` module fetches the Grype DB into its owned directory and records its version; Grype runs with `GRYPE_DB_AUTO_UPDATE=false` (ARCH7, ARCH19).

**Given** air-gapped mode and no DB imported yet
**When** scans would run
**Then** no scan runs and the state is reported as "no vulnerability database — import a feed bundle", which later posture stories show as a coverage gap — never as zero findings (NFR8).

**Given** a stored SBOM and a DB
**When** the scan job runs `grype sbom:<file> -o json` with the single fleet-wide config
**Then** vulnerability findings are stored with typed severity and the locked `Finding` vocabulary (ARCH15), each recording last-evaluated time, Grype version and DB version (FR6, FR8)
**And** an evidence entry records the scan, inputs and versions.

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
**Then** periodic re-enumeration discovers it and it is SBOM'd and scanned within one hour of discovery, with no manual trigger (FR9)
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

**Given** Settings → Package feeds
**When** an admin adds an npm or PyPI feed (endpoint URL, scope/namespace filter, read-only credentials) and tests it
**Then** it is saved with the same validation, envelope encryption and status handling as registry connections (FR29, ARCH17).

**Given** a connected feed
**When** enumeration runs
**Then** the in-scope packages and versions become artifacts (type `package`, ecosystem `npm`/`pypi`), and each version's published archive (npm tarball, PyPI wheel or sdist) is fetched and SBOM'd by Syft, then scanned by the same Grype pipeline with no ecosystem-specific scan config (FR2, FR6)
**And** enumeration is scoped by the configured filter so connecting a public registry never tries to inventory the whole registry.

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
**Then** in-scope versions become artifacts (ecosystem `maven`/`cargo`/`go`), their archives (JAR/POM, `.crate`, module zip) are SBOM'd by Syft and scanned by the same pipeline (FR2, FR6).

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
**Then** it appears as a coverage gap ("N OCI artifacts of unsupported type `<media type>`") rather than being skipped or shown as clean (FR5, NFR8).

### Story 2.9: Posture summary — populating, coverage and freshness

As a SecOps engineer at minute 29,
I want Posture to show what is known, what isn't yet, and how fresh it is,
So that I can trust the view before the first full scan has finished.

**Acceptance Criteria:**

**Given** `GET /api/v1/posture`
**When** it responds
**Then** it returns fleet counts plus the mandatory `provenance` block — sources with versions and retrieval times, coverage (in scope / SBOM'd / scanned / failed), per-feed freshness, and `caveats[]` when partial (FR16, ARCH14)
**And** a contract test asserts every answer-bearing endpoint in `openapi.yaml` declares `provenance`.

**Given** sources are connected and work is queued
**When** Posture renders
**Then** it shows the heading block, one hero numeral with a co-stat band (artifacts, scanned coverage, findings), and a populating banner stating queue count and estimate, updating live without blocking (UX-DR8, UX-DR13, NFR1)
**And** numerals count up on populate, stepped under reduced motion.

**Given** coverage gaps (unscanned artifacts, failed SBOMs, unreachable registry or feed, no vulnerability DB)
**When** Posture renders
**Then** each appears as a named, non-dismissible coverage-gap row with counts and locations, linking to its cause (FR5, UX-DR12, NFR8).

**Given** the freshness strip
**When** Posture renders
**Then** it lists the Grype DB and SBOM index with version and age in mono, coloured by threshold, each linking to Settings (UX-DR15)
**And** the uniformity claim reads "All N artifacts SBOM'd and scanned the same way — Syft vX · Grype vY", where N is the scanned count, not the discovered count.

**Given** no sources are connected
**When** Posture renders
**Then** the empty state offers "Connect registry" with its Settings link (UX-DR29).

### Story 2.10: Posture findings — severity band and findings table

As a SecOps engineer,
I want to see the fleet's findings distributed by severity and listed densely,
So that I can see where the problems are across everything scanned.

**Acceptance Criteria:**

**Given** scanned findings
**When** Posture renders
**Then** a 30px soft severity band shows the distribution, labelled "scanned artifacts only", and clicking a segment filters the table below (UX-DR14).

**Given** the findings table
**When** it renders
**Then** it has 30px rows, mono identifiers (CVE, `package@version`, digest), severity chips with text, cursor pagination (no offset, no infinite scroll) and coverage-gap rows inline (UX-DR9 severity chip, UX-DR11 base, ARCH13)
**And** the header honestly states the current order: "Sorted by severity — KEV/EPSS ranking arrives with enrichment."

**Given** zero findings over partial coverage
**When** Posture renders
**Then** the zero is scoped: "0 critical findings across the N% of the fleet that is scanned."

### Story 2.11: Artifacts list and artifact detail

As a SecOps engineer,
I want to open any artifact and see its SBOM, findings and how it was evaluated,
So that I can answer "what's in this and how do we know?" for a single artifact.

**Acceptance Criteria:**

**Given** the Artifacts surface
**When** it loads
**Then** a paginated list shows each artifact's identifier (mono), type (image/package), source, SBOM/scan status and finding counts, with coverage-gap rows inline and a populating banner while backlog exists.

**Given** an artifact
**When** its detail opens via `GET /api/v1/artifacts/{id}` (with `provenance`)
**Then** it shows SBOM contents (packages and versions), vulnerability findings, evaluation provenance (last evaluated, Syft/Grype/DB versions) and a freshness strip (FR18, FR8, UX-DR25)
**And** the running-locations section honestly reads "No cluster agent connected — running locations unknown" until Epic 3 provides data.

**Given** an artifact whose SBOM or scan failed
**When** its detail opens
**Then** the failure reason and retry status are shown instead of an empty findings list.

### Story 2.12: Prove minute 29 — scripted install-to-posture run

As the Armoury product owner,
I want the 30-minute install-to-posture gate measured by a repeatable script,
So that NFR1 is a checked product gate, not a claim.

**Acceptance Criteria:**

**Given** a kind cluster and a seeded test registry
**When** the scripted run performs `helm install`, bootstrap sign-in and registry connection with no other manual step
**Then** Posture is live and visibly populating (populating banner, coverage co-stat, coverage-gap rows) in under 30 minutes, with the elapsed time per step recorded (NFR1)
**And** the script fails if any step needs input beyond the documented values and credentials.

**Given** the run
**When** it completes
**Then** the timing is appended to a committed performance record, and a miss is raised as a blocking finding against the install path rather than accepted.

**Given** the script
**When** it is invoked
**Then** it runs as its own task outside the default `task check`, and is reusable by Epic 3 to add the agent install step.

### Story 2.13: Prove the scale anchor — initial-evaluation load test

As the Armoury product owner,
I want initial evaluation and read latency measured at the scale anchor,
So that NFR3 and the 24-hour initial-scan bound hold before more features are layered on.

**Acceptance Criteria:**

**Given** a seeded fleet at the scale anchor (hundreds of repositories, thousands of images)
**When** initial evaluation runs
**Then** the measured throughput projects completion within 24 hours, and per-SBOM Syft and Grype subprocess costs (spawn, DB open, run) are recorded (NFR1, NFR3, ARCH28 R11).

**Given** that load
**When** posture, findings-table pages and artifact list endpoints are called
**Then** they stay within the latency budget recorded in the performance record (p95), and the populating banner's estimate stays within a stated tolerance of actual completion.

**Given** the results
**When** the story completes
**Then** they are written to the committed performance record; any miss is a blocking finding with the R11 fallback (long-lived Go matcher sidecar) evaluated rather than silently accepted.

**Given** the load test
**When** it is invoked
**Then** it runs as its own task outside `task check`, with fixtures reusable by the Epic 4 (R2) and Epic 6 (R1) load tests.

## Epic 3: Running inventory from read-only cluster agents

The engineer installs the agent with a second one-liner; running workloads appear linked to registry artifacts so "is this running anywhere?" is answerable; disconnected agents and unmatched running digests surface as gaps. Story 3.1 closes the open enrollment gap (ARCH10) before any agent code depends on it.

### Story 3.1: Agent enrollment and mTLS identity

As a SecOps engineer,
I want a cluster agent to enrol with the control plane from a single install command,
So that it gets a trusted identity without me running a PKI or opening inbound ports.

**Acceptance Criteria:**

**Given** the open architecture gap ARCH10
**When** this story is planned
**Then** the enrollment design (token format and lifetime, identity issuance, rotation, revocation) is recorded as an amendment to `architecture.md` and approved by the user before implementation (ARCH10)
**And** the design keeps the agent outbound-only and works with operator-supplied CAs and egress proxies (R4).

**Given** Settings → Agent install (admin only)
**When** the admin creates an enrollment for a named cluster
**Then** a single-use, time-limited enrollment token is issued and shown once, and only its hash is stored.

**Given** an agent started with the control-plane address and a valid token
**When** it enrols
**Then** it generates its own key, receives a short-lived client certificate bound to that cluster identity, and the token is consumed; a reused or expired token is rejected with a clear error
**And** the agent renews its certificate before expiry without re-enrolment.

**Given** an enrolled cluster
**When** the admin revokes it in Settings
**Then** subsequent agent connections are refused and the cluster's runtime data is marked stale-as-of the revocation, not deleted.

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
**And** containers whose image digest cannot be resolved are reported with their image reference and an `unresolved` flag, never dropped.

**Given** the control plane's `agentgw`
**When** deltas arrive
**Then** the cluster's running inventory is updated, and the agent's heartbeat time is recorded.

**Given** Settings → Agent install
**When** an admin opens it
**Then** it shows the copy-paste `helm install` one-liner with the control-plane address and token filled in, states the trust posture ("read-only — watch/list only, never cluster-admin") and shows the exact RBAC rules before install (UX-DR28)
**And** the empty Posture page now offers "Install agent" alongside "Connect registry" (UX-DR29).

**Given** the agent
**When** it is tested
**Then** unit tests run against a mocked kube client and an integration test runs against a kind cluster in CI (ARCH27).

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
**Then** reconnects are jittered and the control plane bounds the reconciliation rate, so the recovered control plane stays responsive; a test simulates ten clusters reconnecting at once and asserts API latency stays within budget.

**Given** an agent whose heartbeat is older than the warn threshold, then the disconnect threshold (both configurable)
**When** the state is queried
**Then** the cluster is reported `stale` then `disconnected` with its last-seen time, and its runtime data is kept and marked stale-as-of that time, not removed (NFR8, UX-DR30).

### Story 3.4: HTTPS long-poll fallback for locked-down networks

As a SecOps engineer in a regulated network,
I want the agent to work through proxies that block gRPC streaming,
So that runtime inventory works where our most security-conscious environments live.

**Acceptance Criteria:**

**Given** an environment where gRPC streaming fails (simulated by a proxy that blocks HTTP/2 upgrades)
**When** the agent connects
**Then** it falls back to HTTPS long-poll over the same mTLS identity and delivers the same deltas and snapshots (ARCH8, R4).

**Given** an egress proxy configured in agent values (including a custom CA bundle)
**When** the agent connects
**Then** it uses the proxy and trusts the supplied CA.

**Given** either transport
**When** the agent reports
**Then** the control plane records which transport is in use, visible in Settings for that cluster.

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

**Given** Artifact detail
**When** an artifact runs somewhere
**Then** the running-locations section lists clusters, namespaces and workloads in mono, replacing the "no cluster agent connected" message from Story 2.11; shipped-but-not-running artifacts say so explicitly (FR18).

**Given** an artifact no longer running anywhere
**When** reconciliation runs
**Then** its past running locations remain queryable with their end times.

### Story 3.6: Runtime coverage on Posture, and minute 29 with the agent

As a SecOps engineer,
I want Posture to show what is running, where agents are missing or stale, and what we can't match,
So that the fleet view never needs a caveat the UI doesn't already show.

**Acceptance Criteria:**

**Given** connected agents
**When** Posture renders
**Then** the co-stat band includes running artifacts and connected clusters, and the freshness strip includes a runtime-observation entry per cluster with last heartbeat (FR16, UX-DR15).

**Given** a stale or disconnected agent, or unmatched running digests
**When** Posture and Artifacts render
**Then** each appears as a named coverage-gap row ("Cluster `prod-eu-west` disconnected — runtime data as of 14:02", "37 running digests not matched to any connected source") linking to its cause (FR5, UX-DR12, UX-DR30, NFR8)
**And** the posture API's `provenance.coverage` includes these counts and a caveat when runtime data is partial (ARCH14).

**Given** the Story 2.12 install-to-posture script
**When** it is extended with the agent `helm install` step
**Then** Posture shows running workloads and runtime coverage within the 30-minute gate, and the timing is recorded (NFR1).

## Epic 4: Fresh, enriched findings, connected or air-gapped

When vulnerability or enrichment feeds update — online or by signed offline bundle — stored SBOMs are re-evaluated within an hour without rescans, and every finding carries source-attributed KEV, EPSS, CNA and OSV data. Ranking stays severity-only until Epic 5, but enrichment is visible on findings from this epic on.

### Story 4.1: Scheduled vulnerability database updates with versioned history

As a SecOps engineer,
I want the vulnerability database kept current automatically, with every version recorded,
So that findings can prove which intel they were evaluated against.

**Acceptance Criteria:**

**Given** connected mode
**When** the configurable update schedule fires
**Then** the `feeds` module downloads the latest Grype DB to a staging location, validates its checksum/signature and schema, and only then atomically activates it as the current version (FR7, ARCH20 R8)
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
**Then** `reeval` computes the delta from the previous version (added, changed and withdrawn vulnerabilities and affected ranges), selects only the stored SBOMs containing affected packages, and re-matches that subset with `scan`'s Grype matcher (FR7, ARCH6)
**And** no image is pulled and no SBOM is regenerated.

**Given** a fixture fleet and two database versions
**When** delta re-evaluation and a full rescan are both run
**Then** they produce identical findings (equivalence test — the delta selects work, it never changes results, FR6).

**Given** re-evaluated findings
**When** they are stored
**Then** each records its new evaluation time and database version; new findings are added, findings no longer matched are marked resolved-by-feed with the version that resolved them, and every change is appended to the evidence ledger (FR8, NFR11)
**And** unaffected findings keep their evaluation record but their provenance states they were current as of the new version (no stale "last evaluated" on findings the delta proved unaffected).

**Given** a re-evaluation still running when the next database version activates
**When** the new version lands
**Then** work is coalesced to the newest version and the backlog is surfaced (populating banner and pipeline state), never hidden (R2, NFR8).

**Given** Artifact detail and the posture `provenance`
**When** they render after a re-evaluation
**Then** they state "Re-evaluated against Grype DB vX, N min ago — no rescan needed" (UX-DR15, UX-DR23 footer wording).

### Story 4.3: KEV and EPSS enrichment with source attribution

As a SecOps engineer,
I want findings marked when they are on the CISA KEV list and scored with EPSS,
So that I can see which findings are exploited or likely to be.

**Acceptance Criteria:**

**Given** connected mode
**When** the enrichment schedule fires
**Then** the `enrichment` module fetches the CISA KEV catalogue and EPSS scores, validates them, and stores each snapshot with source, source version/date and retrieved_at, appended to the evidence ledger (FR11, FR12, ARCH21).

**Given** a new enrichment snapshot
**When** it is applied
**Then** findings are re-joined to the new enrichment without re-matching SBOMs, and each enrichment datum on a finding carries its source and retrieval time.

**Given** a finding in the UI (Posture table, Artifact detail)
**When** it is KEV-listed
**Then** the KEV tag renders adjacent to the CVE ID and survives every compact view; EPSS score and percentile show with source and retrieval time on hover/focus (UX-DR9, FR12).

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

**Given** connected mode
**When** the enrichment schedule fires
**Then** the full CVE List v5 (CNA-supplied CVSS, descriptions, affected data) is mirrored — an initial full snapshot, then the official daily delta files — and validated and stored as versioned, source-attributed snapshots (FR11, FR12, ARCH21)
**And** OSV records are fetched in one of two configurable modes (PROC2): **fleet-scoped** (default — the CVEs/aliases in fleet findings plus advisories for packages in stored SBOMs, across every ecosystem those SBOMs contain, including OS distro packages) or **full mirror** (all OSV, ~2.7 GB), set via Helm values.

**Given** a blast-radius or detail lookup on a CVE with no fleet match
**When** it renders
**Then** it still shows Grype DB metadata and the CNA record; the absence of OSV data is stated, not hidden.

**Given** sources that disagree (for example CNA CVSS vs. Grype DB severity)
**When** a finding is displayed
**Then** each value is shown with its own source label; no source is silently overwritten by another.

**Given** Artifact detail and the findings table
**When** a finding renders
**Then** its enrichment panel lists every source used with retrieval time, and the freshness strip gains KEV, EPSS, CNA and OSV entries (UX-DR15).

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

**Given** an operator signing key (or Sigstore keyless when the build machine is connected)
**When** the bundle is created
**Then** the manifest is signed with cosign, and a matching offline verification command is printed (ARCH18).

**Given** a bundle
**When** it is tampered with (any byte of any component or the manifest)
**Then** verification fails — proven by a test.

### Story 4.6: Import an offline bundle into an air-gapped instance

As a SecOps engineer running an air-gapped Armoury,
I want to import a bundle and have the whole fleet re-evaluated against it,
So that air-gapped posture is as current as connected posture.

**Acceptance Criteria:**

**Given** Settings → Feed-bundle import (admin only) or the import API
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

### Story 4.7: Honest feed staleness across Posture and findings

As a SecOps engineer,
I want stale or failing feeds to change what Posture says,
So that I never read a confident answer resting on old intel.

**Acceptance Criteria:**

**Given** per-feed freshness thresholds (configurable via Helm values, sensible defaults)
**When** a feed exceeds its threshold or its last update failed
**Then** its freshness-strip age turns warning, the posture headline gains a scoped caveat ("KEV catalogue 3 days old — exploited-status may be out of date"), and the posture API `provenance.caveats[]` carries the same text (NFR8, UX-DR30, ARCH14).

**Given** a feed that has never been loaded
**When** Posture renders
**Then** it appears as a coverage-gap row naming the missing feed, not as an empty enrichment column.

**Given** every freshness-strip entry
**When** it is clicked
**Then** it opens the feed's Settings page, showing version history, last success, last failure and reason (UX-DR15).

### Story 4.8: Prove one-hour re-evaluation at the scale anchor

As the Armoury product owner,
I want feed-update re-evaluation measured at the scale anchor,
So that NFR5 and the CVE-day "already re-evaluated" promise are known to hold.

**Acceptance Criteria:**

**Given** the Story 2.13 scale-anchor fixtures and two realistic database versions (including a large feed delta)
**When** the new version activates
**Then** fleet-wide re-evaluation completes within one hour, with the delta-computation stage, subset size and re-match time each measured separately (NFR5, ARCH28 R2).

**Given** an offline bundle import of the same delta
**When** it activates
**Then** it meets the same bound.

**Given** the results
**When** the story completes
**Then** they are appended to the committed performance record; a miss is a blocking finding with the R11 fallback evaluated rather than accepted.

**Given** the load test
**When** it is invoked
**Then** it runs as its own task outside `task check`.

## Epic 5: Prioritise and triage findings

The analyst works a KEV-first, EPSS-weighted findings list that explains each ranking, records justified decisions that propagate everywhere the finding appears, and ingests and emits VEX. Decisions are append-only evidence: corrections supersede, never overwrite.

### Story 5.1: Deterministic, explainable ranking

As a SecOps engineer on a small team,
I want findings ranked KEV first, then by EPSS-weighted severity, with the reason shown,
So that I work the findings that matter instead of ten thousand rows.

**Acceptance Criteria:**

**Given** the open ranking-formula decision (ARCH29)
**When** this story is planned
**Then** the exact formula (KEV tier, EPSS weighting, severity source precedence, tie-breakers) is recorded as an amendment to `architecture.md` and approved by the user before implementation.

**Given** findings with enrichment
**When** `ranking` computes order
**Then** every KEV-listed finding ranks above every non-KEV finding, the rest are ordered by the approved EPSS-weighted severity, and ties break on a stable key so the same inputs always give the same order (FR13)
**And** a property test asserts determinism and the KEV-first invariant over generated findings.

**Given** any finding
**When** `GET /api/v1/findings/{id}` is called
**Then** it returns a ranking explanation — each input (KEV status, EPSS score/percentile, severity and its source) with its source and retrieval time, and the resulting rank tier — in words a human can read.

**Given** new enrichment or a re-evaluation
**When** it is applied
**Then** affected rankings are recomputed without re-matching SBOMs.

**Given** license findings (Epic 7) or findings without enrichment
**When** they are ranked
**Then** the formula defines their place explicitly (documented in the amendment), never by accident of nulls.

### Story 5.2: Findings workbench and ranked Posture table

As a SecOps engineer,
I want a Findings surface that lists every finding in ranked order,
So that I have one place to work through the fleet's findings.

**Acceptance Criteria:**

**Given** the Findings surface
**When** it loads
**Then** it lists findings across the fleet in ranked order with 30px rows, mono identifiers, KEV tag beside the CVE ID, severity chip, EPSS, artifact, a triage pill (`untriaged` until decided), cursor pagination and inline coverage-gap rows (UX-DR9, UX-DR11, UX-DR26)
**And** the header reads "KEV first, then EPSS-weighted. Severity alone does not rank."

**Given** filters (severity, KEV, triage status, artifact, ecosystem)
**When** applied
**Then** they narrow the list server-side with the order preserved, and the active scope is stated above the table.

**Given** Posture's findings table from Story 2.10
**When** this story lands
**Then** it uses the same ranked order and header sentence, replacing the interim "sorted by severity" header.

**Given** the keyboard
**When** the user moves through rows with arrow keys
**Then** the highlighted row is announced, and the row actions are reachable without a pointer.

### Story 5.3: Record triage decisions as evidence

As an analyst,
I want to record a status and justification on a finding,
So that handling is documented once and shows up everywhere it matters.

**Acceptance Criteria:**

**Given** the decision form or API
**When** an analyst records a decision
**Then** they choose its scope — **this artifact** (one finding on one artifact) or **fleet-wide** (this vulnerability + package across every artifact, including artifacts discovered later) — defaulting to this artifact (PROC2)
**And** a per-artifact decision overrides a fleet-wide one for that artifact, and the UI shows which decision applies and where it came from.

**Given** an analyst or admin
**When** they `POST` a decision with status (`not_affected` / `mitigated` / `accepted` / `fix_planned`) and a non-empty justification
**Then** it is stored with author, UTC timestamp and UUIDv7, and appended to the evidence ledger in the same transaction (FR14, NFR11, ARCH15)
**And** a missing justification or a status outside the locked enum is rejected with 422.

**Given** an existing decision
**When** a new decision is recorded for the same finding
**Then** it supersedes the old one at the same scope; both remain in history, and there is no update or delete endpoint
**And** superseding a fleet-wide decision leaves per-artifact overrides in place.

**Given** an auditor
**When** they attempt to record a decision
**Then** the API returns 403, and the UI has no decision form.

**Given** a recorded decision
**When** Posture, Findings, Artifact detail and the posture API render
**Then** they show the current status and use it in counts (for example "untriaged critical"), consistently across every surface (FR14 propagation).

**Given** a finding that is resolved by a feed update and later reappears
**When** it reappears
**Then** its previous decisions are still attached and visible.

### Story 5.4: Triage drawer

As an analyst working through a list,
I want a drawer that shows why a finding ranks where it does and lets me decide without leaving the list,
So that triage is fast and every decision has its context.

**Acceptance Criteria:**

**Given** any findings list
**When** the user clicks a row or presses `t`
**Then** a right-side `Sheet` opens showing the ranking explanation, full provenance (evaluation time, tool/DB versions, enrichment sources with retrieval times) and decision history (FR8, FR12, FR13, UX-DR16).

**Given** the decision form
**When** the analyst picks a status, writes a justification and submits (or presses `⌘Enter`)
**Then** the decision is recorded, the row updates in place, and on `⌘Enter` the drawer advances to the next finding; `Esc` closes it
**And** status can never be changed inline in a table — only through the drawer.

**Given** "Record triage decision" and "Open triage drawer"
**When** the palette is opened on a highlighted finding
**Then** both are available as palette actions (UX-DR6).

**Given** an auditor
**When** they open the drawer
**Then** it shows explanation, provenance and history, with the form absent (UX-DR31).

### Story 5.5: Evidence trail surface

As a compliance lead,
I want to browse the append-only evidence trail,
So that I can see every scan, feed version and decision, and how corrections were made.

**Acceptance Criteria:**

**Given** the Evidence surface
**When** it loads
**Then** it lists ledger entries newest first with type, subject (mono identifier), actor, time and tool/feed versions, with cursor pagination and filters by type, subject and time window (UX-DR27).

**Given** a superseded entry
**When** it renders
**Then** both the original and the superseding entry are visible and linked; no edit or delete affordance exists anywhere (NFR11, UX-DR36).

**Given** the chain verification from Story 2.1
**When** the surface renders
**Then** it shows the current verification result ("Chain intact — N entries, verified 4 min ago") or the first broken entry.

**Given** a finding, artifact or decision elsewhere in the UI
**When** the user chooses "View evidence"
**Then** the Evidence surface opens filtered to that subject.

### Story 5.6: Emit VEX from triage decisions

As a SecOps engineer,
I want our triage decisions exported as standard VEX,
So that downstream consumers and auditors get machine-readable handling statements.

**Acceptance Criteria:**

**Given** the VEX-format decision (ARCH29, agreed 2026-11-04)
**When** this story lands
**Then** OpenVEX and CycloneDX VEX are both supported, the user picks the format per export, and the decision is recorded in `architecture.md`; CSAF VEX is deferred until a customer needs it.

**Given** decisions on an artifact or across the fleet
**When** VEX export is requested for a scope
**Then** a valid document in each agreed format is produced, mapping the locked statuses to the format's states and justifications, with author and timestamp (FR15)
**And** emitted documents validate against the format's published schema in tests.

**Given** an `accepted` or `fix_planned` decision
**When** it is mapped to a format with no direct equivalent
**Then** the mapping is the documented one from the amendment, never silently dropped.

### Story 5.7: Ingest vendor VEX

As a SecOps engineer,
I want to import vendors' VEX documents and apply their not-affected claims,
So that upstream knowledge reduces noise — with credit to who said it.

**Acceptance Criteria:**

**Given** an admin or analyst
**When** they upload a VEX document in an agreed format (Story 5.6), or point to one in an air-gapped bundle
**Then** it is validated, stored with its source/author, and appended to the evidence ledger; invalid documents are rejected with the reason (FR15).

**Given** a vendor `not_affected` statement matching a fleet finding (product and vulnerability)
**When** it is applied
**Then** the finding shows a vendor-attributed status ("not affected — per <vendor> VEX, <date>") distinct from the team's own decisions, and the team can still record their own decision, which takes precedence and is shown alongside.

**Given** the triage drawer
**When** a finding has vendor VEX
**Then** the VEX context panel shows the vendor, statement, justification and document (UX-DR16).

**Given** a later vendor document that withdraws or changes a claim
**When** it is ingested
**Then** the change supersedes the earlier claim, and affected findings return to their prior status with history kept.

## Epic 6: Blast radius and graph exploration

On CVE day the engineer types a CVE ID or `package@version` into ⌘K and within seconds sees affected artifacts, shipped and running, and where they run — as graph or table, with a provenance footer — exports it, and explores further in the graph.

### Story 6.1: Graph projection of inventory and findings

As a SecOps engineer,
I want the fleet's CVEs, packages, artifacts and workloads connected in one graph,
So that blast-radius and exploration queries are traversals, not ad hoc joins.

**Acceptance Criteria:**

**Given** relational inventory, SBOM packages, findings and running records
**When** they change
**Then** the AGE graph is created and updated from the relational tables in the same transaction or by a transactionally enqueued job — vertices `Cve`, `Package`, `Artifact`, `Workload`, `Cluster`; edges `AFFECTS`, `CONTAINS`/`DEPENDS_ON`, `RUNS_IN` (ARCH2 naming)
**And** graph schema changes are versioned migrations.

**Given** the relational tables are the source of truth
**When** `armoury graph rebuild` (or the admin API) runs
**Then** the graph is rebuilt from them, and a test asserts the rebuilt graph equals the incrementally maintained one on a fixture fleet (R1: the rebuild path is tested, not assumed).

**Given** the graph and relational data disagree (detected by a periodic consistency check)
**When** the check runs
**Then** the drift is reported as a health finding and the answer provenance carries a caveat until a rebuild completes.

### Story 6.2: Blast-radius query API

As a SecOps engineer,
I want to ask "who is affected by this CVE or package version?" and get a complete, honest answer,
So that I can tell the CTO the exposure before he's read the news.

**Acceptance Criteria:**

**Given** `GET /api/v1/blast-radius` with a CVE ID, a `package@version`, or a package with a version range (for example `log4j-core@2.x`)
**When** it runs
**Then** it returns affected packages, affected artifacts (shipped and running), and where each runs (cluster/namespace/workload), with counts for the answer headline (FR17)
**And** triage status and vendor VEX are included per finding, so not-affected decisions are visible in the answer.

**Given** any answer
**When** it is returned
**Then** it carries the `provenance` block: sources (registry-derived SBOMs, live inventory) with versions and freshness, coverage (artifacts in scope, scanned, unscanned, unmatched running digests, disconnected clusters) and `caveats[]` scoping the claim ("2 artifacts in scope have no SBOM yet and are not represented") (FR17, ARCH14, NFR8).

**Given** no affected artifacts
**When** the answer returns
**Then** it is a coverage-scoped zero ("No artifacts affected — across the N% of the fleet that is scanned"), never a bare empty list.

**Given** an image digest as the query (PROC2)
**When** it runs
**Then** it answers from that artifact outward: the CVEs that affect it (ranked, with triage status), its vulnerable packages, and where it runs — with the same `provenance` block
**And** a digest that matches no artifact returns a coverage-scoped answer that says whether the digest runs somewhere unmatched (R7).

**Given** an unknown CVE ID or malformed query
**When** it runs
**Then** the API returns a 422 envelope distinguishing "not a valid identifier" from "CVE not in any loaded feed" (with feed versions).

**Given** a CVE that matches no fleet package
**When** it runs
**Then** the answer still includes the CVE's metadata from the Grype DB and CNA record (Story 4.4).

### Story 6.3: Blast-radius surface — answer and table, from ⌘K

As a SecOps engineer,
I want to type a CVE or package into ⌘K and land on the answer,
So that the log4shell moment takes seconds from anywhere in the product.

**Acceptance Criteria:**

**Given** the palette
**When** the user types a CVE ID or `package@version`
**Then** an "Answers" result routes to the Blast radius surface with that query; a digest gives two results — the digest blast-radius answer (Story 6.2) and the artifact detail (UX-DR6).

**Given** an answer
**When** the surface renders
**Then** it shows the answer headline ("14 affected artifacts · 9 running · 2 clusters"), a caveat chip when partial, the table reading (artifact, package@version, running locations, triage status — mono identifiers, KEV tag), and the provenance footer stating re-evaluation recency ("Re-evaluated against Grype DB vX, 41 min ago — no rescan needed") (UX-DR23, UX-DR15)
**And** the Posture header search opens the same palette pre-scoped.

**Given** a row in the answer
**When** the user presses `t`
**Then** the triage drawer opens for that finding (Story 5.4).

**Given** a query that takes longer than a few seconds
**When** it is running
**Then** partial results stream in with an explicit scope line ("searching — 1,204 of 3,000 artifacts evaluated"); never an unexplained spinner (UX-DR23, UX-DR32).

### Story 6.4: Blast-radius graph reading

As a SecOps engineer,
I want the same answer as a four-tier graph,
So that I can see the path from CVE to running workload at a glance.

**Acceptance Criteria:**

**Given** an answer
**When** the user toggles to Graph
**Then** Svelte Flow renders CVE → vulnerable packages → affected artifacts → clusters/workloads left to right, with severity hue only on the affected path, running nodes with accent ring + pip + label, shipped-not-running nodes dashed at 0.5 opacity, and soft bezier edges (UX-DR17, UX-DR23).

**Given** large result sets
**When** a tier exceeds the display limit
**Then** it rolls up ("+ 9 more artifacts") with expand-to-enumerate.

**Given** keyboard or screen-reader use
**When** the graph is focused
**Then** arrows/`Tab` traverse nodes, `Enter` opens node detail, `+`/`−` zoom, each node's `aria-label` carries identifier, tier and state, and the Graph/Table toggle preserves the answer (UX-DR7, UX-DR34)
**And** entrance/layout motion is disabled under reduced motion.

### Story 6.5: Export blast-radius and posture answers

As a SecOps engineer,
I want to export an answer exactly as I see it,
So that I can hand the CTO something he can trust without me annotating it.

**Acceptance Criteria:**

**Given** a blast-radius answer or the posture summary
**When** the user chooses Export (or presses `x`)
**Then** they can pick CSV, JSON or a PDF report (PROC2), each carrying the same provenance footer, coverage and caveats as the on-screen answer (FR19, UX-DR21)
**And** a test asserts the export's caveats equal the API response's caveats.

**Given** the PDF report
**When** it is generated
**Then** it uses the locked glossary, mono identifiers and the generation time, and the PDF renderer lives in a named home reusable by evidence packs (Epic 9).

**Given** an auditor
**When** they export
**Then** export is available (it is a read action).

### Story 6.6: Graph explorer and node inspector

As a SecOps engineer,
I want to start from any CVE, package or artifact and explore its connections,
So that I can answer questions the blast-radius query doesn't ask directly.

**Acceptance Criteria:**

**Given** the Graph explorer surface with no start node
**When** it opens
**Then** it shows the search-first empty state "Start from a CVE, package, or artifact" (UX-DR24).

**Given** a start node
**When** the user expands neighbours
**Then** `GET /api/v1/graph/neighbours` returns bounded, paginated neighbours with provenance, and the graph uses the Story 6.4 visual language (FR17, FR18).

**Given** a selected node
**When** it is selected
**Then** the node inspector pins it and shows identity, knowledge and provenance, with actions open detail / view evidence / blast radius from here; `Esc` unpins (UX-DR18)
**And** hovering a node highlights its direct path.

**Given** any artifact, finding or CVE elsewhere in the UI
**When** the user chooses "Explore in graph" (row hover/focus, or `e`)
**Then** the explorer opens pre-centred on that node (UX-DR11, UX-DR24).

**Given** the explorer
**When** the Table reading is chosen
**Then** the current neighbourhood is fully readable as a table (UX-DR34).

### Story 6.7: Prove sub-minute blast radius at the scale anchor

As the Armoury product owner,
I want blast-radius latency measured at the scale anchor,
So that NFR2 is known to hold before CVE day tests it for us.

**Acceptance Criteria:**

**Given** the Story 2.13 scale-anchor fixtures with up to ten clusters of running inventory
**When** a representative query set runs (widely used package, rare CVE, broad version range, no-match CVE)
**Then** p50 answers in seconds and every query completes in under a minute, with graph traversal and provenance assembly timed separately (NFR2, ARCH28 R1).

**Given** the results
**When** the story completes
**Then** they are appended to the committed performance record, the query-latency SLO is exposed as a health signal (for Epic 8 metrics), and a miss is a blocking finding with mitigations (indexes, materialised paths, query rewrite) evaluated.

**Given** the load test
**When** it is invoked
**Then** it runs as its own task outside `task check`.

## Epic 7: License compliance

Grant evaluates every artifact against a fleet allow/deny policy. Violations appear as neutral license findings in the same views, and the team triages them with the same decision model as vulnerability findings. License data stays embedded, never headline: there is no license dashboard.

### Story 7.1: License evaluation of stored SBOMs with Grant

As a SecOps engineer,
I want the licenses of every artifact identified from its stored SBOM,
So that I know what licenses we ship without a second pipeline.

**Acceptance Criteria:**

**Given** a stored SBOM
**When** the license job runs
**Then** the `tools` module runs the pinned Grant CLI (`grant check`, JSON output) against the SBOM, with a timeout and stderr capture (FR26, ARCH7)
**And** the detected licenses per package (SPDX identifiers or expressions, plus unknown/unparseable values as-is) are stored with the Grant version and appended to the evidence ledger.

**Given** a new SBOM from Epic 2 onboarding
**When** it is stored
**Then** license evaluation runs automatically, in parallel with the Grype scan, not after it.

**Given** Grant fails on an SBOM
**When** the job ends
**Then** the artifact shows a license-evaluation failure with the reason and a retry, and counts as a coverage gap; it never shows as "no license issues" (NFR8).

**Given** Artifact detail
**When** it renders
**Then** the SBOM package list shows each package's license as a neutral license chip in mono (UX-DR9).

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
**And** the upload has a configurable size limit and rejects path traversal and symlinks that point outside the archive.

**Given** both SBOM and image evaluation exist for one artifact
**When** its licenses render
**Then** each result shows its evaluation source, and differences are visible, not merged silently.

### Story 7.3: Fleet license policy

As an admin,
I want one fleet-wide allow/deny license policy,
So that license violations are judged the same way for every artifact.

**Acceptance Criteria:**

**Given** Settings → License policy (admin only)
**When** an admin edits the policy
**Then** they can set an allow list, a deny list, and the treatment of licenses on neither list and of unknown licenses — each **violation**, **warning** or **ignore** (PROC2), with documented defaults (FR27)
**And** entries accept SPDX identifiers and expressions, and invalid entries are rejected with the reason.

**Given** a saved policy change
**When** it is saved
**Then** it is a new policy version appended to the evidence ledger (author, time, diff); earlier versions stay readable, and there is no per-team or per-artifact policy.

**Given** a new policy version
**When** it activates
**Then** license findings for the whole fleet are recomputed from stored license data without re-running Grant, and the backlog shows in the populating banner while it runs.

**Given** an analyst or auditor
**When** they open the policy page
**Then** they see the current policy and its history read-only; edit controls are absent (UX-DR31).

### Story 7.4: License findings in Posture, Findings and triage

As a SecOps engineer,
I want license violations listed with vulnerability findings and triaged the same way,
So that I can act on them before audit day.

**Acceptance Criteria:**

**Given** a package whose license violates the active policy
**When** license findings are computed
**Then** a `Finding` of kind `license_violation` is stored with the package, license, policy version and evaluation provenance (FR27, ARCH15)
**And** a license that the policy marks **warning** is stored as a `Finding` of kind `license_warning`.

**Given** the "triage license warnings" setting (PROC2)
**When** it is on (default)
**Then** license warnings are triageable exactly like violations
**And** when an admin turns it off, warnings stay visible but have no decision form, and existing decisions on warnings stay in history.

**Given** Posture, Findings and Artifact detail
**When** they render license findings
**Then** each shows the neutral license chip, never a severity hue or a KEV tag, placed in rank order by the documented rule from Story 5.1, and filterable by kind (vulnerability / license) (UX-DR9, UX-DR26).

**Given** a license finding
**When** the analyst opens the triage drawer
**Then** the same drawer, statuses, justification rule, scope choice (this artifact or fleet-wide) and evidence recording apply as for vulnerability findings (FR14, FR27, Story 5.3, Story 5.4)
**And** the drawer shows the policy rule that produced the violation instead of a ranking explanation.

**Given** the posture API
**When** it responds
**Then** license-finding counts are included alongside vulnerability counts, and license-evaluation coverage is in `provenance.coverage` (ARCH14).

## Epic 8: Fleet signals — Prometheus metrics and data quality

The team's own Grafana alerts on new KEV findings, coverage gaps, stale feeds and agent health. Every answer carries a data-quality (DQ) score that the user can expand to see how it was calculated. Armoury sends no notifications itself: signals leave by Prometheus pull only.

### Story 8.1: Data-quality scoring model and artifact score

As a SecOps engineer,
I want each artifact to have a score for how trustworthy its data is,
So that I know how much to trust an answer, not only what the answer is.

**Acceptance Criteria:**

**Given** the open DQ scoring decision (ARCH29)
**When** this story is planned
**Then** the scoring model (dimensions, inputs, weights, 0–100 scale and letter-grade bands) is recorded as an amendment to `architecture.md` and approved by the user before implementation.

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

### Story 8.2: Fleet data quality on Posture and Artifacts

As a SecOps engineer,
I want data quality shown next to risk on every surface that gives an answer,
So that a low-quality answer is visible before someone acts on it.

**Acceptance Criteria:**

**Given** artifact scores
**When** the fleet score is computed
**Then** it aggregates the artifact scores by the rule in the approved model, and the posture API returns it in `provenance` with its dimension breakdown (FR30, ARCH14).

**Given** Posture
**When** it renders
**Then** the co-stat band includes the fleet DQ score and grade in the `data-quality` colour, never a severity colour (UX-DR10, UX-DR22).

**Given** Artifact detail and artifact or finding table rows
**When** they render
**Then** the detail header shows the score and grade, and table rows show a grade-only DQ badge (UX-DR10, UX-DR25).

**Given** any DQ score or badge
**When** the user clicks or focuses it
**Then** it expands to the dimension breakdown, and each low dimension offers its corrective action (for example "connect feed", "rescan", "import bundle")
**And** lower grades dim to 0.65 opacity and never turn red.

**Given** blast-radius answers
**When** they render
**Then** the provenance footer includes the DQ score of the artifacts in the answer.

### Story 8.3: Prometheus metrics endpoint

As a SecOps engineer,
I want posture signals exposed as Prometheus metrics,
So that my own Grafana alerts me with the observability stack I already run.

**Acceptance Criteria:**

**Given** the control plane
**When** Prometheus scrapes `/metrics`
**Then** it gets metrics for findings by severity, KEV status and triage status, new critical and new KEV findings, coverage gaps by kind, feed age and last update result per feed, agent state and last heartbeat per cluster, pipeline backlog per stage, fleet DQ score, blast-radius query latency (Story 6.7 SLO), ledger chain status and disk headroom (FR20, ARCH24, R9)
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
**Then** it installs a `ServiceMonitor` and a `PrometheusRule` with example alerts (new KEV finding, stale feed, disconnected agent, broken ledger chain); both are off by default (PROC2).

**Given** Armoury
**When** any of these conditions happen
**Then** Armoury sends no email, webhook, toast or badge; the signal leaves only through `/metrics` (FR20, UX-DR36).

### Story 8.4: Prometheus panel in Settings

As an operator,
I want to see the metrics endpoint and the metric list in Settings,
So that I can wire Grafana without reading the source code.

**Acceptance Criteria:**

**Given** Settings → Metrics
**When** it opens
**Then** it shows the endpoint URL, the configured access mode, and the list of exported metrics with their type, labels and help text, each with a copy action (UX-DR28)
**And** the panel is read-only for every role; configuration stays in Helm values.

**Given** the metric list
**When** a metric is added in code
**Then** the panel shows it without a UI change, because the list comes from the same registry that serves `/metrics`.

**Given** the bearer-token mode
**When** the panel renders
**Then** it states where the token comes from (the Secret name) but never shows the token.

## Epic 9: Signed CRA evidence packs

The compliance lead generates a CRA pack in one click for any past window. The pack is a PDF plus SBOM and VEX companions, states its own coverage and data quality, and is signed so an auditor can verify it offline. Packs draw only on evidence that Armoury already recorded. Retention is configurable but never below 24 months.

### Story 9.1: Point-in-time evidence queries for any window

As a compliance lead,
I want Armoury to tell me what the fleet state was at any past time,
So that any period the fleet was under management is reportable after the fact.

**Acceptance Criteria:**

**Given** the evidence ledger and stored history
**When** the `evidence` capability is asked for the state as of time T, or over a window T1–T2
**Then** it returns the inventory, SBOM versions, scans with tool and feed versions, findings, enrichment versions and triage decisions that were current at T, from recorded evidence only (FR23)
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
**Then** the PDF uses the renderer from Story 6.5, with the locked glossary, mono identifiers and the cover sheet first (FR24).

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

**Given** connected mode
**When** a pack is generated
**Then** the `signing` capability signs the pack manifest with cosign keyless and records the signature in Rekor, by default (FR25, ARCH18)
**And** an admin can choose an operator-managed key instead (PROC2).

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
**Then** it does not need internet access for operator-key packs, and keyless packs include the bundle needed for offline verification.

### Story 9.5: Generate packs and verify signatures in the UI

As a compliance lead,
I want one click to generate a pack and one click to verify it,
So that the audit moment passes without a scramble.

**Acceptance Criteria:**

**Given** the Evidence surface or `⌘K`
**When** the user clicks "Generate CRA pack"
**Then** generation starts at once with smart defaults (last 12 months as the window, the whole fleet as scope, CRA as the framework), with no wizard first (UX-DR20)
**And** the user can change the window, scope and framework after the click, which regenerates the pack.

**Given** generation in progress
**When** the user keeps browsing
**Then** progress shows per section; a failed section fails the pack closed and names the section, and retry re-runs only failed sections (UX-DR20).

**Given** a pack card
**When** the user clicks "Verify signature"
**Then** the UI shows the result and signer identity, and gives a copyable offline verification command (cosign keyless, or the operator-key equivalent) (UX-DR19).

**Given** the auditor role
**When** an auditor opens Evidence
**Then** they can generate, view, download and verify packs by default, as in Flow 3; an admin can restrict generation to admin and analyst (PROC2)
**And** auditors can never change triage, policy or Settings (UX-DR31).

**Given** a blast-radius answer
**When** the user chooses "Export evidence pack"
**Then** a pack scoped to that answer is generated with the same pipeline, caveats and signing (UX-DR21).

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
**Then** it appends a checkpoint entry with the chain head hash, entry count and covered time range, signed by the `signing` capability from Story 9.4 — keyless + Rekor when connected, operator key when air-gapped (NFR11, ARCH18)
**And** a signing failure leaves the previous checkpoint in force, is reported as a health signal and a `/metrics` value, and is retried; no unsigned checkpoint is ever written.

**Given** chain verification (Story 2.1)
**When** it runs
**Then** it also verifies every checkpoint signature and that each checkpoint matches the chain at its position
**And** a test that rewrites and fully recomputes the chain as a superuser makes verification fail at the first checkpoint after the change.

**Given** the Evidence surface
**When** it renders the verification result
**Then** it shows the latest signed checkpoint and its time, and gives a copyable offline verification command for checkpoints.

### Story 9.7: Retention with archiving to the object store

As an admin,
I want evidence older than the retention period moved out of the database but kept verifiable and reportable,
So that the database does not grow without limit and no past window becomes unreportable.

**Acceptance Criteria:**

**Given** the retention setting
**When** no value is set
**Then** retention is 24 months; an admin can set a longer value in Helm values or Settings, and any value below 24 months is rejected by the API and is not offered in the UI (FR23, UX-DR28, PROC2).

**Given** a monthly ledger partition that is wholly older than retention and covered by a signed checkpoint
**When** the archive job runs under its separate maintenance database role
**Then** it exports the partition to the object store as a compressed archive segment, verifies the segment against the checkpoint, appends a ledger entry with the segment digest, and only then drops the partition (ARCH30)
**And** if any step fails, the partition stays in place and the failure is reported; the application role still has no DELETE grant, proven by the Story 2.1 test.

**Given** an archived window
**When** a point-in-time query (Story 9.1) or a pack (Story 9.5) covers it
**Then** it reads the archive segment, verifies it against its checkpoint first, and returns the same result as before archiving — proven by a test that archives a fixture partition and compares the answers.

**Given** chain verification after archiving
**When** it runs
**Then** it starts from the oldest hot checkpoint and reports intact; each archive segment can also be verified on its own with the offline command.

**Given** historical SBOM blobs
**When** compaction runs
**Then** identical SBOMs are stored once (content-addressed) and older snapshots move to the archive prefix of the object store, with point-in-time answers unchanged.

**Given** the archive purge option
**When** it is off (default)
**Then** archive segments are kept forever
**And** when an admin turns it on with a further period, segments older than retention plus that period are deleted, each deletion recorded as a ledger entry with the segment digest; nothing inside retention is ever removed (NFR11, PROC2).

## Epic 10: Verifiable, air-gapped delivery of Armoury itself

Buyers can verify Armoury's own images, charts and feed bundles (cosign + SLSA provenance), and can run the whole product end to end with no internet access. A supply-chain security tool whose own supply chain cannot be verified is disqualified from its market (NFR7).

### Story 10.1: Signed, provenance-attested releases

As a buyer's security reviewer,
I want every Armoury release artifact signed and provenance-attested,
So that I can verify what I install came from Armoury's own build.

**Acceptance Criteria:**

**Given** a release tag
**When** `.github/workflows/release.yml` runs
**Then** it builds the control-plane and agent images (with the pinned Syft, Grype, Grant and cosign binaries) and the Helm chart as an OCI artifact, signs each with cosign keyless, and attaches SLSA build provenance (NFR7, ARCH23)
**And** each image also gets an SBOM attestation generated by Syft.

**Given** the published artifacts
**When** the release workflow finishes
**Then** a verification job in the same workflow verifies every signature and provenance attestation from a clean runner, and fails the release if any check fails.

**Given** the release notes and `README.md`
**When** a reviewer reads them
**Then** they give copyable `cosign verify` and `cosign verify-attestation` commands with the expected identity and issuer.

**Given** Armoury's own images
**When** they are scanned by Armoury
**Then** the result is published with the release, so Armoury reports on itself the same way it reports on a customer fleet.

### Story 10.2: Armoury-published signed feed bundles

As a SecOps engineer running an air-gapped Armoury,
I want ready-made signed feed bundles from Armoury,
So that I do not have to run my own connected bundle machine unless I want to.

**Acceptance Criteria:**

**Given** a scheduled publishing workflow
**When** it runs (default: daily)
**Then** it builds bundles with `armoury bundle create` and signs them with Armoury's release signing key (FR10, NFR7)
**And** the chart adds Armoury's release public key to the Story 4.6 trusted-key list by default, so published bundles verify without extra setup; an operator can remove it (PROC2).

**Given** the published bundle variants (PROC2)
**When** an operator chooses one
**Then** they can pick **core** (Grype DB, KEV, EPSS and CVE v5 delta; OSV absent and stated as absent) or **full** (core plus the full OSV mirror)
**And** a fleet-scoped OSV bundle is still built by the operator with `armoury bundle scope` (Story 4.5), because Armoury cannot see the fleet.

**Given** a published bundle
**When** it is imported
**Then** it verifies with the release key and passes the same checks as an operator-built bundle; a test imports the latest published bundle into a fresh air-gapped instance.

**Given** the release signing key
**When** it is rotated
**Then** the chart ships the new and old public keys for an overlap period, and the rotation is stated in the release notes.

### Story 10.3: Air-gapped installation from an internal mirror

As a SecOps engineer in a network with no internet,
I want to mirror everything Armoury needs and install from my own registry,
So that air-gapped install is as simple as connected install.

**Acceptance Criteria:**

**Given** each release
**When** it is published
**Then** it includes a list of every image the chart uses (control plane, agent, Postgres-AGE, SeaweedFS) by digest, and the documented commands to copy them and the chart to an internal registry (NFR4).

**Given** chart values
**When** an admin sets one registry override
**Then** every image in the chart, including the agent subchart, pulls from that registry by digest.

**Given** the air-gap boundary rule (ARCH19)
**When** `task check` runs
**Then** a check fails if code outside `feeds`, `enrichment` and `signing` makes an outbound call to any endpoint that an admin did not configure (registry and feed connections are admin-configured)
**And** in air-gapped mode, `feeds`, `enrichment` and `signing` make no outbound call, proven by a test.

### Story 10.4: Prove the full air-gapped journey end to end

As the Armoury product owner,
I want the three user journeys proven with no internet at all,
So that "air-gapped is first-class" is a checked fact, not a claim.

**Acceptance Criteria:**

**Given** a kind cluster with all egress blocked except to an internal registry and an internal package feed
**When** the scripted run installs the control plane and agent from the mirror, signs in with the bootstrap admin, connects the registry and feed, and imports a bundle
**Then** Posture populates with findings, enrichment and runtime coverage within the 30-minute gate, with each step timed (NFR1, NFR4, UJ-1)
**And** the run records every attempted outbound connection and fails if any goes beyond the allowed internal endpoints.

**Given** the same instance
**When** the script runs a blast-radius query for a CVE in the bundle, records a triage decision, generates a CRA pack and verifies its operator-key signature offline
**Then** each step succeeds with no internet access (UJ-2, UJ-3, FR25).

**Given** the results
**When** the run completes
**Then** they are appended to the committed performance record, and the run is its own task outside `task check`, executed in CI on each release.
