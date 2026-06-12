# Armoury UX Research Digest

(Subagent extraction, 2026-06-12, from PRD + brief + market research.)

## A. Users & Personas

**Primary user: SME SecOps engineer.** Canonical persona is "Priya" — senior and *only* dedicated security engineer at a ~200-person company `[ASSUMPTION 1]`, covering a much larger engineering org. **Emotional state is explicit:** "they have just survived a stressful audit" (last audit = "three weeks of spreadsheet archaeology") and are "freshly determined... that the next one won't be assembled by hand." Skill level: comfortable with `helm install`, Kubernetes admin on at least one cluster `[ASSUMPTION 2]`, runs Prometheus/Grafana and wires her own alerting `[ASSUMPTION 5]`. She acts **alone — zero dev-team cooperation** is a hard product gate.

**Secondary persona: "Marta," compliance lead** — the champion who sold Armoury to the CTO; uses the **read-only auditor role** at audit time (UJ-3).

**Buyer vs user:** buyer is the **CTO, with legal/compliance as champion**. "The pitch to the buyer leads with evidence and compliance; the pitch to the user leads with 'stop hand-assembling audits.'" Roles (NFR6, `[ASSUMPTION 13]`): **admin** (configuration, connections), **analyst** (triage decisions, pack generation), **read-only auditor**.

Market research adds: practitioners suffer alert fatigue (73% name false positives top challenge; 62% would trade missed true positives for less noise; 16+ tools correlates with 50% burnout).

## B. Surfaces & Screens Implied

- **Fleet posture view (FR16)** — "the web UI's landing state — fleet-wide summary of artifacts, findings by priority, coverage gaps, and feed freshness. This is what appears at minute 29." Must show inventory *visibly populating* with explicit coverage indicator (NFR1).
- **Blast-radius query (FR17)** — input: CVE ID or package+version ("who uses log4j 2.x?"); output: affected artifacts, shipped vs running, deployed where (cluster/namespace/workload), in seconds. Every answer carries **data provenance** (sources, coverage, freshness) — "definitive in tone only when the data earns it."
- **Artifact detail (FR18)** — SBOM contents, findings (vulnerability *and* license) with triage status, evaluation provenance, running locations.
- **Coverage/gaps surfacing (FR5, NFR8)** — discovered-but-not-yet-SBOM'd images, unreachable registries, disconnected agents, stale feeds; "the fleet posture must never need a caveat the UI doesn't already show."
- **Ranking explainability (FR13)** — deterministic: KEV first, then EPSS-weighted severity; "the UI can always show why a finding ranks where it does."
- **Triage decision recording (FR14)** — status (not affected / mitigated / accepted / fix planned), justification, author, timestamp; decisions propagate to posture views and evidence packs.
- **VEX (FR15)** — express decisions as VEX statements; ingest vendor VEX with attribution shown on findings.
- **License findings (FR26–FR28)** — surface as findings **in the same posture/artifact views** alongside CVEs, same triage model; "embedded, never headline" (addendum: dedicated license dashboard explicitly rejected). License policy = fleet-wide allow/deny (FR27).
- **Data-quality score (FR30)** — second score alongside risk: SBOM depth, scan coverage, feed freshness, enrichment coverage, CVE record quality; surfaced at **artifact and fleet level** in posture views and evidence packs. (Scoring model is "architecture/UX decisions" — open for UX.)
- **Source attribution (FR12)** — every enrichment datum labeled with source + retrieval time.
- **Evaluation provenance (FR8)** — when last evaluated, against which feed versions.
- **Export/share (FR19)** — blast-radius result or posture summary as report/CSV — "the thing the SecOps engineer hands the CTO before being asked."
- **CRA evidence pack generation (FR21–FR25)** — time-window selection; pack states its own coverage/data quality; PDF + machine-readable companions (SBOMs, VEX); signed (Sigstore or operator keys air-gapped); pack architecture is framework-extensible (FR22).
- **Admin/setup**: registry connection (FR1), package feed connection (FR29), cluster-agent install (second one-line helm install, UJ-1), air-gapped signed feed-bundle import (FR10). OIDC is **declarative only** — "env vars / Helm values / config file, never a UI wizard" (NFR6); bootstrap admin for first sign-in.
- **Metrics, not notifications (FR20)** — Prometheus endpoint (new critical/KEV findings, coverage gaps, feed freshness, agent health); v1 pull-only, "Armoury sends no notifications itself."

## C. Key Moments & Journeys

- **UJ-1 — the first 30 minutes / minute-29:** helm install → sign in with bootstrap admin ("SSO is never allowed to stand between her and minute 29") → paste read-only registry creds → "watch the inventory fill" → agent install → minute 29: full posture view, findings ranked by KEV/EPSS, "coverage gaps honestly displayed... the whole fleet in one place she doesn't have to caveat." NFR1: minute 29 honestly = posture live and *visibly populating*, not a completed scan; full evaluation within 24h `[ASSUMPTION 11]`.
- **UJ-2 — CVE day (the log4shell moment):** Grafana alert → type CVE into blast-radius query → "Seconds later: 14 affected images, 9 running — which clusters, which namespaces, which workloads" → export to CTO "before he's read the news" → triage with justifications → all already in the evidence trail. NFR2: seconds, under a minute worst case.
- **UJ-3 — audit day (the audit moment):** auditor role; generate CRA pack for the window; Sigstore-signed, tamper-verifiable; "three weeks of spreadsheet archaeology is now a generated, signed document."
- Time bounds: discovery-to-scan ≤1h (FR9); feed-update-to-fleet-re-evaluation ≤1h (NFR5).

## D. Constraints Affecting UX

- **Deployment:** self-hosted Helm only; control plane (web UI, graph, evidence store) + read-only cluster agents; air-gap fully supported, "no phone-home" (NFR4, FR10). Single instance, no HA in v1 (NFR10).
- **No CI changes (FR1), zero dev-team cooperation** — everything operable by SecOps alone.
- **Pull-only notifications** — no in-product alerting/push; customer-owned Grafana ethos.
- **Honest degradation (NFR8)** and the counter-signals: "a quiet dashboard is not the same as a safe fleet"; "evidence-pack polish must never outrun data integrity." Honesty/provenance is a core UI voice.
- **Scale anchor (NFR3):** hundreds of repos, thousands of images, ≤10 clusters — list/table design target.
- **Evidence is append-only, tamper-evident (NFR11)** — no silent edit/delete affordances on recorded history.
- **Terminology (Glossary):** *Artifact*, *Fleet*, *Finding* (vuln match or license violation), *Posture* ("fleet-wide, freshness-labeled state of findings and coverage"), *Evidence*, *Evidence pack*, *Control plane / cluster agent*. Triage statuses: not affected, mitigated, accepted, fix planned.
- **Positioning/tone:** "Detection insight is the output; consistency is the product"; engine/chassis/hero-moment framing; "consistency-and-evidence layer... not a better scanner"; Grafana-to-Prometheus analogy. No dark/light mode guidance exists in any doc.

## E. Non-Goals / Out of Scope

UI must not grow into: **host/VM scanning; runtime behavior analysis/threat detection** (eBPF — "'live' means workload inventory, not Falco/Wiz territory"); **SaaS offering; SAST; auto-remediation PRs; multi-scanner orchestration/normalization** (rejected-not-deferred — "go hard on Syft and Grype"); **reachability analysis** (deliberately unclaimed v1); vendor SBOM ingestion (unadopted); dedicated license dashboard (rejected); in-product push notifications; OIDC UI wizard; dev-team handoff workflows (outside Armoury in v1 `[ASSUMPTION 6]`); MCP/AI (roadmap).

## F. Competitor UX Context (market research)

- **Anchore**: "complex setup, steep learning curve, docs gaps... weak commercialization of its own tools' UX"; the <30-min deploy "directly attacks Anchore's documented setup complexity."
- **Snyk**: "fragmented post-acquisition UI," false positives surfacing months after import, expensive.
- **Trivy criticized for CVSS-only severity**, while "Grype's EPSS/KEV scoring and Snyk's reachability are praised differentiators."
- Alert noise dominates: ~960 alerts/day, 40% never investigated; buyers pay for "the operational wrapper... not detection"; POC wins on "lowest false-positive noise."
- Black Duck: docs/UI complaints, "incumbency without love." Sigstore self-hosting: only 2 of 13 practitioners succeeded. "UI polish complaints" rated *low-priority* pain — table stakes, not differentiator.

## G. Open Questions for UX

1. **FR30 data-quality score model and presentation** — addendum: "scoring inputs... and the scoring model itself are architecture/UX decisions."
2. **Minute-29 partial-state design** — how the posture view communicates "visibly populating" + coverage honesty before full evaluation.
3. **Blast-radius provenance tone calibration** — how "definitive in tone only when the data earns it" renders visually.
4. Several `[ASSUMPTION]` tags UX inherits: single registry in first session, role granularity, 1-hour bounds.
5. Visual identity — no doc specifies anything; only positioning cues (Grafana/Prometheus ethos, "Armoury" name, engine/chassis metaphor).
6. Hub-and-spoke agent health presentation (agent buffering/outage behavior deferred to architecture but surfaces in NFR8 UI).
