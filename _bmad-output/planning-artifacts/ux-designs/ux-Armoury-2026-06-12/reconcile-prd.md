# PRD Reconciliation — Armoury UX Spines

Audit of `prd.md` + `addendum.md` (prd-Armoury-2026-06-11) against `DESIGN.md` and `EXPERIENCE.md`. Statuses: **Covered** / **Partial** / **Excluded** (intentional, cited) / **Dropped** (UI-relevant, absent from both spines). This is an audit, not a redesign proposal.

## Coverage table

| Item | Status | Where / gap |
|---|---|---|
| FR1 Registry connection | Covered | EXPERIENCE: Settings IA, Flow 1 steps 3–4, registry-unreachable failure path |
| FR2 Central SBOM generation | Covered | Populating banner/count-up; Artifact detail SBOM contents |
| FR3 Live cluster inventory | Covered | Agent install (Settings, Flow 1), runtime entries in freshness strip, heartbeat state |
| FR4 Shipped-vs-running | Covered | Blast-radius graph: ember ring vs dashed "shipped, not running" (DESIGN graph-node states) |
| FR5 Coverage visibility | Covered | Coverage-gap rows as first-class, click-through to cause |
| FR6 Uniform scanning | **Partial** | Uniformity is never a user-facing claim: no UI copy, posture stat, or Settings surface says "scanned the same way / one fleet-wide config" — the PRD's chassis promise (and UJ-1's climax phrasing) is invisible |
| FR7 Feed-driven re-evaluation | Covered | Freshness strip, populating banner covers re-evaluation backlog, stale-feed state |
| FR8 Evaluation provenance | Covered | Honest Provenance; triage drawer; freshness strip |
| FR9 Continuous onboarding | Covered | Populating banner appears for any first-scan backlog; live progress |
| FR10 Air-gapped bundles | Covered | Settings feed-bundle import; air-gapped mode state; "import bundle" action on stale feeds |
| FR11 Multi-source enrichment | **Partial** | Attribution covered (FR12), but the freshness strip enumerates "Grype DB, KEV, EPSS, SBOM index, runtime" — CNA records and OSV are absent from any named UI list |
| FR12 Source attribution | Covered | Honest Provenance: source + retrieval time on hover/expansion |
| FR13 Explainable ranking | Covered | Table header states sort logic in words; drawer ranking explanation |
| FR14 Triage as data | Covered | Triage drawer, author+timestamp, propagation, locked status set |
| FR15 VEX support | Covered | Drawer VEX context w/ vendor attribution; VEX companions in packs |
| FR16 Posture view | Covered | Posture surface; Flow 1 climax |
| FR17 Blast-radius query | Covered | Blast radius surface, ⌘K query, caveat chip + provenance footer |
| FR18 Artifact detail | Covered | Artifacts surface (list → detail) |
| FR19 Shareable answers | Covered | Export (report/CSV) carrying same caveats |
| FR20 Prometheus metrics | **Partial** | Pull-only philosophy fully honored (notifications banned), but where an operator *finds* the metrics endpoint in the UI is unspecified |
| FR21 CRA pack | Covered | Evidence surface, Flow 3, cover-sheet coverage/DQ |
| FR22 Pack architecture | Covered | "framework — FR22 extensible" in generator config |
| FR23 Continuous evidence / retention | **Partial** | On-demand generation over recorded evidence covered; retention configuration (24-month floor) absent from Settings IA |
| FR24 Auditor formats | Covered | PDF + machine-readable companions |
| FR25 Signed packs | Covered | Sigstore / operator keys; air-gapped copy swap |
| FR26 License evaluation | Covered | License findings embedded in Posture/Findings/Artifact detail |
| FR27 License policy | **Partial** | Violations-as-findings covered; the fleet-wide allow/deny policy *authoring* UI has no home in the Settings IA |
| FR28 License evidence | Covered | Embedded, never headline; pack section implied via FR21 coverage |
| FR29 Package feeds | Covered | Settings IA names FR29 |
| FR30 Data-quality score | Covered | Dedicated EXPERIENCE section; DQ hue rule in DESIGN |
| NFR1 Minute-29 | Covered | Populating state pattern; Flow 1; "honest, partial, alive" |
| NFR2 Query in seconds | Covered | Flow 2; Blast radius purpose row |
| NFR3 Scale anchor | Covered | Pagination not infinite scroll; table density sized to anchor |
| NFR4 Self-hosted / air-gapped | Covered | Foundation; no phone-home affordances |
| NFR5 1-hour re-eval | Covered | Bound itself non-UI; stale/fresh states carry the UI half |
| NFR6 Declarative OIDC | Covered | "OIDC is declarative — never a UI wizard"; read-only resolved config; bootstrap admin |
| NFR7 Armoury's own provenance | Excluded | Release/chart signing is non-UI; no spine surface required. (No .decision-log.md entry — excluded by nature, not by decision) |
| NFR8 Honest degradation | Covered | The signature pattern (Honest Provenance) is this NFR |
| NFR9 Agent footprint | **Partial** | Read-only agent exists, but the "watch/list only, never cluster-admin" reassurance never appears in agent-install copy — a trust nuance the PRD leans on |
| NFR10 Single instance | Covered | Foundation |
| NFR11 Evidence integrity | Covered | Append-only state pattern; banned edit/delete affordances |
| UJ-1 First 30 minutes | Covered | Flow 1, incl. failure path |
| UJ-2 CVE day | Covered | Flow 2, incl. no-match zero-scoping |
| UJ-3 Audit day | Covered | Flow 3, incl. fail-closed packs |
| Addendum: license dashboard rejected | Excluded | EXPERIENCE IA: "no dedicated license dashboard"; addendum option B rejected |
| Addendum: push notifications rejected | Covered | Banned-everywhere list; Prometheus-only exit |
| Addendum: MCP/AI deferred | Excluded | Out of v1 per PRD roadmap; spines silent correctly |
| Decision log: brainstorming notes | Excluded | .decision-log.md 2026-06-12 setup: "Brainstorming notes excluded" |

**Counts (44 PRD items: 30 FR + 11 NFR + 3 UJ): Covered 37 · Partial 6 · Excluded 1 (NFR7) · Dropped 0.**

## Dropped or at-risk (qualitative ideas)

1. **Uniformity as a felt UI claim** — "every image SBOM'd and scanned the same way" (UJ-1 climax, FR6, FR21 "proof of uniform scanning") never surfaces as copy, stat, or settings; the product's core chassis promise is invisible in both spines.
2. **The "no rescans, no rebuilds" moment** — PRD UJ-2's quiet magic ("Armoury has already re-evaluated every SBOM") isn't narrated in Flow 2 or surfaced as a state; only FR8 provenance carries it indirectly.
3. **License policy authoring (FR27)** — fleet-wide allow/deny configuration has no home in the Settings IA.
4. **Evidence retention setting (FR23)** — configurable retention with the 24-month compliance floor is absent from Settings.
5. **Read-only agent reassurance (NFR9)** — "watch/list access only, never cluster-admin" trust copy missing from the agent-install flow.
6. **CNA + OSV visibility (FR11)** — omitted from the freshness strip's enumerated feeds.
7. **Prometheus endpoint discoverability (FR20)** — the stance is honored, the doorway is unspecified.
8. **Auditor verification affordance (UJ-3/FR25)** — packs are "tamper-verifiable," but how Marta or the auditor actually verifies the signature is never specified.
9. **Glossary completeness** — PRD glossary includes *Control plane* / *Cluster agent*; EXPERIENCE's locked glossary omits both.
