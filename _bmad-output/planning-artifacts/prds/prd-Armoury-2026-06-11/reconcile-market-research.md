# Reconciliation: Market Research → PRD

**Input:** `research/market-software-supply-chain-security-research-2026-06-11.md`
**Outputs checked:** `prd.md`, `addendum.md`
**Date:** 2026-06-12

Deliberate exclusions honored (not flagged): GTM/sales KPIs, commercial model, launch-grade GTM depth.

## What the PRD captures well (no action)

- NVD enrichment vacuum → FR11–FR13 (multi-source enrichment, attribution, prioritization)
- Trivy-compromise trust shock → NFR7 (provenance-attested Armoury releases)
- Air-gapped/self-hosted demand of regulated buyers → FR10, NFR4
- CRA-slippage risk → FR22 pack architecture explicitly insulates ("CRA timeline slippage does not strand the work")
- SBOM operationalization (store/query/monitor; Shai-Hulud lesson that query beats rescan) → FR7, FR16–FR18
- Anchore's documented setup pain → NFR1 30-minute gate (the contrast exists, but uncited — see A3)
- VEX (record + ingest) → FR14–FR15; AI hedge (assistive, ~2027) → roadmap; alert-fatigue pain → FR13 + counter-signal 2
- PCI component inventory, DORA, FedRAMP → roadmap packs on FR22

## A. Missing and should be added

### A1. Scanner neutrality / cross-scanner normalization — the PRD is silent on its biggest research finding
The research names **"neutral multi-scanner orchestration + normalization at the OSS layer" the strongest whitespace** (Whitespace #1), documents the pain in hard numbers (Trivy 247 vs Grype 203 CVEs on the same image; inter-tool SBOM consistency as low as 7.8–12.8%; "run two scanners" is standing practitioner advice), and makes neutrality the named moat against platform bundling ("orchestrate any scanner incl. Trivy, ingest from GitHub/GitLab — bundling becomes input, not threat").

The PRD hard-codes a single scanner (FR6: "every SBOM is scanned (Grype)") and a single generator (FR2: Syft) and never mentions the choice. Single-engine v1 is defensible — it *is* how you get uniform results — but the PRD currently neither claims the normalization lane nor reserves it. **Recommended:** state the single-engine v1 decision explicitly, and add multi-scanner orchestration/normalization to the roadmap (or explicitly reject it). Otherwise the strongest validated whitespace and the principal bundling-defense have no home anywhere in the artifact set.

### A2. Vendor / third-party SBOM ingestion — named unmet need, absent everywhere
Research lists vendor SBOM ingestion as a market gap (Unmet Needs), a high-value opportunity (#1: "store/query/monitor/**ingest vendor SBOMs**"), and the expansion lever that "extends the buyer from engineering to procurement." The PRD's inventory is exclusively registry-enumerated + cluster-observed; SBOMs are only ever *generated* by Armoury (FR2). A fleet's posture includes software you bought, not just software you built — and CRA evidence ultimately spans both. Likely out of v1 scope (it complicates the "zero dev-team cooperation" install), but it should be **named on the roadmap**; today it's invisible.

Related scope tension: the Vision says "every **package** and container image in the fleet," but FR1–FR4 only source from container registries and clusters. Non-container artifacts have no ingestion path; vendor-SBOM ingestion is the natural future answer. Worth one clarifying line.

### A3. Competitive/why-now grounding — the PRD asserts bars the research can substantiate
The PRD cites no competitive or market facts. Three of its boldest stances have direct research backing that a reviewer (or future contributor) can't see:
- NFR1's 30-minute gate ↔ Anchore's documented setup complexity, Dependency-Track's scaling pain (Backbase needed EKS orchestration + Aurora HA for 200 repos), Sigstore's 2-of-13 private-deploy success rate;
- self-hosted-only (NFR4) ↔ the underserved tier between Dependency-Track DIY and $50–200K cloud-only SaaS, and cloud-only being the documented blocker for regulated buyers;
- the vacant lane ↔ "no one found offering Syft+Grype+GUAC+Sigstore as one consistent, managed product" (Anchore niched, Kusari drifted, Stacklok exited).

**Recommended:** a short "Why now / positioning" paragraph (or addendum section) citing these. Stakes are "serious side project," so brief — but a PRD whose central NFRs look arbitrary without the research is fragile.

### A4. Customer-contract evidence as a pack use case (CRA-slip hedge, second leg)
FR22's pack architecture insulates the *build investment* against CRA slippage; the research's contingency plan adds a *demand-side* hedge: "if CRA slips — pivot spearhead to customer-contract evidence (74% have had to prove security controls to close a deal; 88.5% say requirements are rising)." Evidence packs currently exist only for the regulator/auditor persona (UJ-3). One line acknowledging packs also answer customer security questionnaires / contract evidence makes the product deadline-independent. Cheap addition, completes the insulation argument.

## B. Defensibly out of v1 — but should be named in roadmap or out-of-scope

### B1. Reachability analysis
Research: false positives are the #1 practitioner pain (73%); reachability is the praised differentiator (Endor "97% noise cut"; Snyk's reachability); 62% would trade missed true positives for less noise. PRD's answer is KEV/EPSS prioritization (FR13) — good, but a different mechanism. Reachability is heavy and arguably scanner-territory, so out of v1 is fine; it should appear in out-of-scope (alongside SAST) or roadmap so the omission reads as a decision, not an oversight. Note: FR14's "not affected — code path not invoked" triage (UJ-2 step 4) is *manual* reachability; a future assist fits the 2027 assistive-AI item.

### B2. SPDX ↔ CycloneDX format support/conversion
Research flags conversion friction as a named solution gap. The PRD never mentions SBOM formats — not even for FR24's machine-readable exports or future vendor-SBOM ingestion. Probably an architecture decision, but one sentence (e.g. "packs export SBOMs in both SPDX and CycloneDX" or a roadmap note) would close it.

### B3. Ingesting platform-generated SBOMs/findings (GitHub/GitLab/Dependency-Track)
Research's bundling-mitigation: treat free platform SBOM features as *inputs*. Also relevant: Dependency-Track v5 GA (20K+ orgs) is the largest installed base to win migrations from. Roadmap candidate under the same neutrality umbrella as A1.

### B4. Artifact signature/attestation *verification* as a fleet capability
The validated wedge phrase includes Sigstore, but the PRD uses Sigstore only to sign Armoury's own outputs (FR25, NFR7). Verifying *fleet* artifacts' signatures/attestations (is this image signed? does provenance check out?) is unaddressed in v1. The roadmap's build-time item covers *producing* attestations; verification of third-party/existing signatures could be named there explicitly. Also note the research's Sigstore-private-deploy pain (2 of 13 succeeded) — if signed evidence packs must work air-gapped (FR10/NFR4 imply they must), key/signing infrastructure without public Fulcio/Rekor is a known-hard problem worth one architecture-flag line.

## C. Noted, no action recommended

- **Adoption-reality gap** (<50% actual SBOM usage vs stated priority; only 13% fully automate): tempering signal for expectations, but the PRD's success criteria are quality bars, not adoption targets — consistent with the calibrated stakes.
- **AWS Marketplace, SOC 2, trust center, OpenSSF/CNCF engagement, upstream contribution**: GTM/trust-asset territory — excluded by design per the known exclusions, though upstream OSS standing doubles as competitive defense; revisit if stakes rise.
- **VulnCheck-class commercial enrichment sources**: FR11's source list (KEV/EPSS/CNA/OSV) is open-data-only; fine for v1, architecture can keep the source list pluggable (FR12 already implies it).
- **Per-image pricing aversion** (Anchore complaint): commercial-model territory — parked by design.
