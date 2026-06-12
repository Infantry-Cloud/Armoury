# PRD Quality Review — Armoury

Calibration: serious side project, ~5–8 pages, real product discipline but not launch-grade GTM/compliance exhaustiveness. Success criteria are deliberately quality bars, not business metrics, and the commercial model is deliberately parked (addendum) — neither is treated as a defect.

## Overall verdict

This is a genuinely good PRD: it has a real thesis ("Detection insight is the output; consistency is the product"), decisions stated as decisions with rejected alternatives preserved in the addendum, and NFRs with product-specific numbers instead of adjectives. What's at risk is downstream extraction, not strategy — a handful of FRs leave "done" underdefined (prioritization behavior, discovery-to-scan latency, evidence retention), and the missing Glossary and Assumptions Index will cost friction when architecture and story creation try to source-extract from it. Nothing here is broken; the fixes are tightening, not rethinking.

## Decision-readiness — strong

Decisions read as decisions. "Air-gap operation is a v1 requirement, not a roadmap note" (FR10), "v1 is pull-only; Armoury sends no notifications itself" (FR20), "SaaS would dilute the self-hosted wedge" (Non-Goals), and NFR1's "this bar is a product gate, not a marketing line: any v1 feature that breaks it doesn't ship in the install path" — each gives a decision-maker something to push against. The addendum's "Options considered" section names what was given up (dedicated license dashboard, push notifications, v1 MCP server) and why, which is exactly the trade-off honesty the rubric asks for. The counter-signals under Success Criteria ("a quiet dashboard is not the same as a safe fleet") show the author anticipating how the bars could be gamed — rare and valuable.

### Findings
- **low** No Open Questions section (§ whole document) — Everything genuinely open is carried as inline `[ASSUMPTION]` tags (e.g. UJ-2's "handoff to dev teams happens outside Armoury in v1"). That works at this stakes level, but a decision-maker skimming for "what's still unsettled" has to hunt for bracketed tags across five sections. *Fix:* a 4–6 bullet "Open items" list (or the Assumptions Index below) would make the open surface scannable.

## Substance over theater — strong

No furniture detected. The personas are exactly two (Priya, Marta), carried inside the journeys, and both drive real requirements: Priya's "no tickets to the platform team" becomes FR1's "No CI changes required" and NFR1's no-dev-cooperation gate; Marta's "read-only auditor role" becomes a third of NFR6. The Vision could not swap into another product — "the thing you install *because* you use Syft, Grype, and GUAC, the way Grafana became the default face of Prometheus" is a specific, falsifiable positioning. NFRs carry numbers (30 minutes, 1 hour, hundreds of repos / thousands of images / ten clusters), and NFR7's "A supply chain security tool whose own supply chain can't be verified is disqualified from its own market" is an earned, product-specific security requirement rather than boilerplate.

## Strategic coherence — strong

The thesis is stated in bold in the Vision and every feature group serves it: Fleet Inventory and Uniform Scanning deliver "consistency is the product"; FR7/FR8 deliver lifecycle freshness; FR21–FR25 deliver the "audit moment"; FR16–FR17 deliver the "log4shell moment." The two payoff moments named in the Vision map one-to-one onto UJ-2 and UJ-3, and onto Success Criteria bars 2 and 1 respectively. Counter-metrics exist (the three counter-signals), and FR22's pack-architecture framing ("CRA timeline slippage does not strand the work") shows the roadmap hedging a real external risk rather than listing aspirations. MVP scope kind is problem-solving and the scope logic matches — the deferred MCP server (addendum) was cut specifically "to protect the <30-min wow."

## Done-ness clarity — adequate

Most FRs carry a testable consequence: FR4's "is this running anywhere?' is answerable per artifact," FR8's provenance recording, FR17 bounded by NFR2, FR6's "the same artifact always produces the same result." The weak spots are where behavior, not capability, is the deliverable:

### Findings
- **medium** Prioritization behavior undefined (§ FR13) — Inputs are named (KEV, EPSS, severity) but not how they combine: composite score, tiering, sort order? An engineer cannot know when FR13 is done, and "the findings that matter, not ten thousand rows" is not testable. *Fix:* state a minimum v1 behavior (e.g. KEV membership trumps, then EPSS above threshold, then severity) or explicitly delegate the model to architecture with an `[ASSUMPTION]`.
- **medium** No latency bound on continuous onboarding (§ FR9) — NFR5 bounds feed-driven re-evaluation (1 hour) but nothing bounds discovery-to-scanned for a newly pushed image. "Automatically on discovery" could mean minutes or a nightly batch and both would satisfy the text. *Fix:* add a bound or assumption parallel to NFR5.
- **medium** Evidence retention unbounded (§ FR23) — "Any period the fleet was under management is reportable after the fact" implies indefinite retention of scans, feed versions, and decisions, with storage-growth consequences NFR10's "durable storage" doesn't address. *Fix:* name a retention floor (e.g. "evidence retained ≥ N years `[ASSUMPTION]`") so architecture sizes storage against something.
- **low** "Polished documents" (§ FR24) — adjective without a bar; the testable part (PDF + machine-readable companions) is fine, "polished" adds nothing verifiable. *Fix:* drop the word or define it (e.g. "suitable to hand to an auditor without editing").
- **low** "Lightweight" agent (§ NFR9) — the permission bound (watch/list only, never cluster-admin) is testable; the resource footprint is not. *Fix:* a rough envelope (CPU/memory ceiling) or an explicit deferral to architecture.

## Scope honesty — strong

The Non-Goals section does real work — each exclusion carries a reason ("Falco/Wiz territory," "Semgrep/SonarQube/CodeQL territory") that tells a reader *why* the line is drawn, not just where. Twelve `[ASSUMPTION]` tags sit on genuine inferences (audit cadence, helm rights, cluster ceiling, 1-hour bound), and the open-items density is appropriate for the stakes. De-scoping is done in the open: the addendum documents the MCP deferral and the parked commercial model with the reasoning preserved.

### Findings
- **medium** No Assumptions Index (§ end of document) — ~12 inline `[ASSUMPTION]` tags are never collected. The rubric's roundtrip check fails trivially because there is nothing to round-trip to, and downstream consumers (architecture especially — cluster ceiling, read-only agent scope, single-instance control plane) will need these as a checklist, not a scavenger hunt. *Fix:* append an Assumptions Index listing each tag with its location.
- **low** Bare assumption tag (§ NFR10) — "HA is not a v1 requirement `[ASSUMPTION]`" is the only tag with no body text; every other tag states what is being assumed. *Fix:* "`[ASSUMPTION: single-instance is acceptable for v1 operators]`" or similar.

## Downstream usability — adequate

This is a chain-top PRD (it will feed architecture and stories), so this dimension carries weight. IDs are clean: FR1–FR28 and NFR1–NFR10 contiguous, UJ-1–3 with named protagonists, and every cross-reference (FR14 from FR27, FR21 from FR28, FR5/FR20 from NFR8, FR10 from NFR4, FR22's pack architecture) resolves. Sections extract reasonably alone — "Fleet" is even defined inline in the Features preamble. What's missing is the formal layer:

### Findings
- **medium** No Glossary (§ whole document) — Load-bearing nouns ("artifact," "finding," "evidence pack," "posture view," "fleet," "feed") are used consistently but never defined. "Artifact" matters most: FR1–FR2 imply container images, FR26 says "any artifact Armoury can inventory" including filesystems, and an architecture pass will have to guess whether v1 inventory is images-only. *Fix:* a six-to-eight-term Glossary; define "artifact" with its v1 extent explicitly.
- **low** "Artifact" v1 extent ambiguous (§ FR2 vs FR26) — FR2 SBOMs "every discovered artifact"; discovery in v1 appears to be registry images + running workloads only, but FR26's wider Grant surface ("container images, and filesystems") leaves it inferable rather than stated. *Fix:* one sentence in Fleet Inventory stating what artifact types v1 discovers.

## Shape fit — strong

The shape matches the product: multi-stakeholder B2B (SecOps operator, CTO buyer, compliance champion, auditor consumer) with three load-bearing UJs that map to the product's two named payoff moments plus onboarding. The feature section is capability-spec in style — appropriate for an infrastructure product — while the UJs carry the human context. Length and rigor sit squarely in the agreed ~5–8-page band; nothing is over-formalized (no UJ padding, no persona roster) and nothing essential is under-formalized. The addendum is used correctly: depth that belongs downstream (topology, Grant surface, options considered) is parked there instead of bloating the body.

## Mechanical notes

- **Assumptions Index roundtrip:** fails — no index exists (see Scope honesty finding). Inline tags themselves are well-formed except NFR10's bare tag.
- **ID continuity:** FR1–FR28 contiguous, no gaps or duplicates; NFR1–NFR10 contiguous; UJ-1–UJ-3 contiguous. All inline cross-references (FR5, FR10, FR14, FR20, FR21, FR22, FR26–FR28) resolve.
- **Glossary drift:** no glossary to drift from; usage is nonetheless consistent — "evidence pack" / "compliance pack" / "CRA pack" are used near-interchangeably (FR21–FR25, UJ-3) and a glossary should pick one canonical term.
- **UJ protagonists:** all named (Priya ×2, Marta), context carried inline. The CTO appears as buyer in two UJs but never acts — acceptable, he's a recipient, not a user.
- **Addendum hygiene:** good — "Commercial model (parked — do not import into PRD)" is exactly the right boundary discipline, and the brief addendum cross-reference path is plausible.

## Finding totals

| Severity | Count |
|---|---|
| critical | 0 |
| high | 0 |
| medium | 5 |
| low | 5 |
