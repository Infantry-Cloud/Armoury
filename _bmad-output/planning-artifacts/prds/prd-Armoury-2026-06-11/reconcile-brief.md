# Reconciliation: Brief → PRD (Armoury, 2026-06-11)

Input: `briefs/brief-Armoury-2026-06-11/brief.md` + `addendum.md`
Output checked: `prds/prd-Armoury-2026-06-11/prd.md` + `addendum.md`

Items the brief contains that the PRD neither captures nor deliberately excludes. Honoured exclusions (not flagged): commercial model, business-metric success criteria, rejected alternatives.

## Gaps — concrete capability / constraint

### G1 — Package feeds as an inventory source (HIGH)
Brief v1 scope, data source 1: "*Static/registry*: Armoury connects to container registries **and package feeds**, generates SBOMs centrally (Syft) and scans them (Grype)." The brief consistently says "every **package** and container image" (exec summary, solution).
PRD status: the Vision repeats "every package and container image," but the FRs only deliver containers — FR1 is container-registry-only ("container registry credentials; enumerates repositories and image digests"), and no FR covers connecting to package feeds / non-container package artifacts. FR9 mentions "newly discovered images and packages" but there is no FR through which a non-container package can be discovered. Either an FR is missing or the narrowing to containers-only was a silent, unrecorded scope cut.

### G2 — CRA deadline as a delivery constraint (HIGH)
Brief: CRA reporting obligations begin **2026-09-11**; "turns 'nice to have' into 'need by Q3'"; CRA compliance packs as "the GTM spearhead" and the forcing function for the whole product.
PRD status: CRA appears as a feature (FR21) and FR22 hedges against "CRA timeline slippage," but the date itself, the Q3 urgency, and the implication that v1 timing is anchored to 2026-09-11 appear nowhere. A PRD reader cannot recover why v1 has a deadline or what it is.

## Gaps — positioning / philosophy / voice

### G3 — Competitive positioning: "the lane is vacant" (MEDIUM)
Brief ("What Makes This Different"): scanner market saturated (Wiz, Snyk, Qualys); nobody owns the consistency-and-evidence layer — "Kusari has drifted, Anchore is a government niche, Stacklok exited." Also: self-hosted/air-gapped as "a moat against SaaS-only competitors."
PRD status: no competitive framing anywhere. Out-of-scope entries name Falco/Wiz/Semgrep only as category boundaries. The why-this-wins argument — including the moat rationale behind NFR4's self-hosted-only stance — is unrecoverable from the PRD. (May be a deliberate PRD-vs-brief division of labour, but it is not recorded as such anywhere; one addendum line would fix it.)

### G4 — "We sell the hard part, not the free part" / the invoice line (MEDIUM)
Brief: "CVE data is free; Grype is free. The genuinely hard problems ... are what the invoice says."
PRD status: "commodity by design" and "consistency is the product" survive, but the sharper value-capture phrasing — *what the invoice says* — is gone. It borders the parked commercial model but is really a product-identity statement (what Armoury is allowed to be mediocre at vs. must be excellent at). Worth one line in the PRD addendum as a design compass.

### G5 — The Engine / Chassis / Hero-moment three-layer model (MEDIUM)
Brief names a three-layer architecture of meaning: **Engine** (commodity detection), **Chassis** (the product), **Hero moment** (the payoff).
PRD status: "chassis" appears once and the two moments survive as narrative, but the named three-layer model itself — a memorable organizing vocabulary for the team — was dropped. Cheap to preserve in vision or addendum.

### G6 — Dual-pitch persona nuance (LOW-MEDIUM)
Brief: "The pitch to the buyer leads with evidence and compliance; the pitch to the user leads with 'stop hand-assembling audits.'"
PRD status: buyer/champion/user roles are present, but the messaging split — which should shape UX emphasis (what Marta sees first vs. what Priya sees first) — is not.

## Gaps — minor nuances

### G7 — Build-time integration trigger condition (LOW)
Brief roadmap: build-time integration comes "once Armoury has earned org-wide buy-in" (addendum: day-one value must not depend on dev-team adoption). PRD roadmap lists the item but drops the sequencing condition that explains *when* it unlocks.

### G8 — AI remediation grounded in the evidence graph (LOW)
Brief vision: assistive AI remediation "sits on top of the evidence graph, suggesting fixes grounded in what's actually deployed." PRD roadmap keeps "assistive, not autonomous" but loses the grounding idea — the differentiator vs. generic AI-fix bots.

### G9 — Traceability pointer (LOW)
Brief addendum lists source artifacts (brainstorming session, market research with the validated wedge + four sharpenings). The PRD/addendum contain no pointer back to the brief or research; the document chain breaks at the PRD.

## Verified as captured (no action)
- "Operationally consistent and provable"; "Detection insight is the output; consistency is the product" — verbatim.
- Log4shell moment, audit moment; "just survived a stressful audit" persona beat; "before the CTO asks" beat.
- NVD-enrichment-abandonment rationale (FR11); snowflake-configs language (FR6); no-caveats philosophy (NFR8, success bar 4).
- 30-minute / SecOps-alone bar (NFR1, success bar 3); air-gap (FR10/NFR4); provenance-attested releases (NFR7).
- Grant question from brief addendum — resolved (FR26–28 + PRD addendum); live-vs-runtime fence; all five out-of-scope items; Grafana/Prometheus analogy; "tool earns its place first" pointer.
