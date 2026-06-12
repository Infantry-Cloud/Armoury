# Adversarial Review — Armoury PRD + Addendum

**Reviewed:** `prd.md`, `addendum.md` (prd-Armoury-2026-06-11)
**Posture:** Cynical review. Deliberate choices (quality-bar success criteria, parked commercial model) were not penalized. Everything else was.

**Verdict:** The PRD is well-written and self-aware in places, but its three headline promises — 30-minute install, blast-radius-in-seconds, and audit-grade evidence — each rest on a contradiction the document never resolves. Air-gap support (FR10/NFR4) is asserted, not designed: at least three v1 capabilities (Sigstore signing, OIDC, multi-source enrichment) have unexamined internet dependencies. Several scope boundaries leak. Not ready to hand to architecture without a revision pass.

---

## Critical findings

### 1. The 30-minute promise contradicts the scale anchor — and the PRD's own counter-signal forbids the only escape hatch
NFR1 demands `helm install` → fleet posture in <30 minutes. NFR3 demands comfort at **thousands of container images**. Central SBOM generation (FR2) means pulling every image's layers through the control plane and running Syft on each — at thousands of images that is hours-to-days of registry I/O and CPU on a **single-instance control plane** (NFR10), before Grype scanning and enrichment even start. The obvious dodge — show a partial posture at minute 29 with "coverage gaps honestly displayed" (UJ-1 step 5) — is explicitly disallowed by the PRD's own counter-signal: *"Install speed must not be bought with posture completeness — a fast install that silently skips half the registry fails bar 4."* UJ-1 isn't silent skipping, but the PRD never defines what fraction of the fleet must be SBOM'd-and-scanned for minute 29 to count as a "fleet posture view" rather than a progress bar. As written, NFR1 + NFR3 + the counter-signal cannot all be true. Define the minute-29 acceptance state quantitatively (e.g. "full inventory enumerated, ≥N% scanned, completion ETA displayed") or drop one of the three claims.

### 2. Sigstore signing is incompatible with air-gap as specified
FR25 and NFR7 require Sigstore signing; FR10/NFR4 require fully supported air-gapped operation with "no capability that silently requires internet access." Sigstore's keyless flow depends on public Fulcio, Rekor, and an OIDC identity provider — all internet services. Air-gapped Sigstore means either (a) deploying a private Sigstore stack (Fulcio + Rekor + CT log + trust-root distribution — a substantial product in itself, and fatal to the 30-minute install), or (b) falling back to plain key-based cosign, which abandons most of what "Sigstore-signed" implies and still needs a key-distribution/verification story for the auditor in UJ-3 step 2 ("the auditor can verify nothing was edited"). Verify *against what trust root, delivered how, in an air-gapped org*? The PRD treats "Sigstore" as a magic word. This needs an explicit FR-level decision, not an architecture punt.

### 3. The signed evidence pack proves the wrong thing — "audit-grade" is overstated
UJ-3 promises the auditor can verify "nothing was edited **after generation**." That is precisely the weak guarantee: the underlying evidence (scan results, triage decisions, timestamps) lives in a mutable store before generation. An admin can edit history and then generate a freshly-signed, fully-verifiable pack. Nothing in FR21–FR25 or NFR10 requires tamper-evidence, append-only semantics, or integrity protection of the evidence store itself — only durability. For a product whose flagship claim is "audit-grade evidence" and whose stated failure mode is "a beautiful signed report over stale data," the absence of any evidence-integrity requirement is the single most damaging gap in the document. Either claim less ("packs are integrity-sealed at generation") or require more (append-only / hash-chained evidence log).

### 4. Blast-radius answers inherit registry-SBOM blind spots, and the PRD hides this from the moments it sells
SBOMs reconstructed from final images (Syft against registry artifacts) systematically miss build-context dependencies: statically linked libraries, vendored/shaded code, stripped binaries, multi-stage build leftovers. The roadmap *admits this* — build-time integration "upgrades evidence from 'reconstructed from images' to 'captured at build'" — yet UJ-2 presents "14 affected images, 9 running" as a definitive answer exported to the CTO, and FR14/FR21 turn *negative* results into audit evidence. A confident false-negative blast-radius answer is worse than no answer. NFR8 ("honest degradation") covers only *operational* gaps (disconnected agents, stale feeds), not *epistemic* gaps (SBOM completeness limits). Require blast-radius results and evidence packs to carry an explicit evidence-quality qualifier ("derived from image analysis; build-time provenance unavailable").

### 5. OIDC-only sign-in breaks both the 30-minute journey and the no-tickets claim
NFR6 mandates OIDC SSO with no mention of a bootstrap/local-admin path. In UJ-1, Priya signs in via "the company's existing OIDC provider" at minute ~5 — but registering a new OIDC client in a corporate IdP is, at most 200-person companies, exactly the IT ticket the journey claims doesn't exist ("No tickets to the platform team"). Chicken-and-egg: who configures OIDC before anyone can log in to configure anything? Air-gap doubles the problem if the IdP is cloud-hosted (Okta, Entra ID — the common SME case). A break-glass local admin and an explicit "IdP client registration is a prerequisite, not part of the 30 minutes" statement are required, or NFR1's clock is fiction.

## Major findings

### 6. "No dev-team cooperation" quietly assumes SecOps has helm rights on production clusters
UJ-1's assumption tag covers helm rights on "at least one cluster" — the ops cluster. Step 4 then installs the agent **into prod**. At a 200-person company, deploying a workload with Kubernetes API watch/list access into production clusters is normally gated by the platform team. The "zero dev-team cooperation" differentiator (Features intro, NFR1, success bar 3) silently depends on an unstated and frequently-false assumption. Tag it, or scope bar 3 to clusters SecOps administers.

### 7. The agent–control-plane trust model is missing entirely — in a security product
FR3/NFR9 specify what agents read, but nothing specifies how agents authenticate to the control plane, how a registration is authorized, or how a spoofed/compromised agent is prevented from poisoning the inventory ("nothing is running anywhere" is a lovely thing to feed an evidence pack). Transport mechanics belong in architecture; *the requirement that agent identity be authenticated and inventory be attributable* is product-level and absent. The addendum punts even agent buffering — see next finding.

### 8. Inventory staleness is unbounded, which undermines blast-radius and NFR8
FR3 promises a "live record"; the addendum defers "whether agents buffer during control-plane outages" to architecture. But staleness is a product question: when Priya reads "9 running," how old is that answer allowed to be? No NFR bounds agent-report staleness or requires the UI to display data age per cluster. NFR8 says posture must never need an unshown caveat — data age *is* that caveat. Add a staleness bound or a mandatory last-seen indicator requirement.

### 9. FR26 "filesystems" leaks straight through the "no host/VM scanning" scope fence
Out-of-scope says host scanning is "a different capability and competitive set." FR26 then preserves Grant's filesystem-scanning surface because limiting it would be "for no good reason" (addendum). Pick one: either filesystems are scannable (host scanning by another name — scope leak, plus a new attack/permission surface), or the FR is dead text, since nothing in FR1–FR5 can inventory a filesystem ("any artifact Armoury can inventory can be license-checked" — filesystems are not inventoriable). The asymmetry is also incoherent: licenses get a filesystem surface that vulnerabilities are explicitly denied.

### 10. Vendor VEX ingestion (FR15) has no trust model — it's an auto-suppression channel
FR15 applies upstream vendors' not-affected claims to fleet findings "with attribution." Attribution is not verification. Nothing requires VEX documents to be signature-verified, nothing defines precedence when vendor VEX conflicts with an internal triage decision (FR14), and nothing states whether vendor claims suppress findings from posture views/metrics or merely annotate them. Unverified third-party documents that silently downgrade findings is a textbook supply-chain attack vector in a supply-chain security tool. Also unanswered: how VEX documents arrive in an air-gapped deployment.

### 11. Air-gapped enrichment hand-waves a hosted dependency the business model has parked
FR10's "signed offline bundle" must carry Grype DB + KEV + EPSS (updated daily) + CNA records + OSV (enormous, ecosystem-wide). Someone must aggregate, package, sign, and host these bundles continuously — that is operated infrastructure with real cost, for a project whose commercial model is deliberately parked and whose NFR4 says "no phone-home." Who runs the bundle service, at what cadence, and how does the air-gapped customer meet NFR5's one-hour freshness when freshness is bounded by sneakernet? UJ-2's "feeds updated overnight" silently assumes the connected deployment; the air-gapped CVE-day story is never told.

### 12. FR6's determinism claim is contradicted by FR7 by design
FR6: "the same artifact always produces the same result." FR7: results change whenever feeds update — that's the product's whole point. The claim is only true conditioned on (feed version, Grype version, policy version), which FR8 records but FR6 doesn't reference. As written, FR6 is falsified daily. Reword: "the same artifact, evaluated against the same feed and policy versions, produces the same result."

## Minor findings

### 13. "Every discovered artifact" (FR2) is unbounded — registries are landfills
Hundreds of repos can mean tens of thousands of stale tags. No retention window, tag-filtering, or digest-vs-tag policy is specified, which inflates the scale anchor, the 30-minute clock, and storage costs. Even "scan everything by default" needs a stated default scope (e.g. tags pulled/pushed within N days, or running-referenced digests first).

### 14. The CVE-day SLA rides entirely on customer-built alerting
UJ-2's "pinged before coffee" depends on the `[ASSUMPTION: she wired alerting in week one]` and FR20's pull-only metrics. Alerting on *a specific new KEV CVE* via Prometheus metrics is awkward (per-CVE label cardinality or a generic "new KEV count" that says nothing about *which* CVE). The flagship moment's first beat is delegated to infrastructure Armoury doesn't ship and a metric design the PRD doesn't specify. State which signals FR20 must expose with enough granularity to support the UJ-2 alert.

### 15. Blast-radius for workloads with no registry-linked artifact is unaddressed
FR4 reconciles registry artifacts with running digests — but clusters run images from registries SecOps hasn't connected (third-party, public, sideloaded). Those workloads have no SBOM, so the blast-radius answer for them is "unknown," yet UJ-2 reports a clean "14 affected, 9 running" with no unknown-count. FR5 covers this for inventory; FR17/FR19 must require the unknown set to appear in query results and exports, or the export handed to the CTO is silently incomplete.

### 16. GUAC appears in the vision and topology but in zero requirements
The vision sells orchestrating GUAC; the addendum puts a "GUAC graph" in the control plane; no FR mentions it. GUAC is operationally heavy (multiple services + backing store) — material to both the 30-minute helm install footprint and NFR10's single-instance framing. Either a requirement depends on it (which one?) or it's an architecture choice that shouldn't be in the product vision's promise list.

### 17. "Audit-grade" CRA pack (FR21) is asserted with no mapping to CRA obligations
No reference to which CRA articles/annex requirements the pack satisfies, and success bar 1 ("accepted by the auditor") is untestable for a side project with no auditors on hand. Also absent: evidence retention duration (CRA-adjacent regimes demand multi-year retention — NFR10 requires durability but never says *for how long*). A one-page CRA-requirement-to-pack-section mapping is the minimum for the word "audit-grade" to be honest.

### 18. NFR2's bar slides between three values
"Answered in seconds" (FR17), "in seconds — under a minute worst case" (NFR2), "under a minute" (success bar 2). UJ-2 says "Seconds later." Pick one number with a percentile (e.g. p95 < 10s, p100 < 60s at the scale anchor) — "seconds" is marketing, not a requirement.

### 19. Registry credential handling is unspecified for a security product
FR1 ingests read-only registry credentials; nothing covers secret storage, rotation, or least-privilege guidance. For a tool whose pitch includes "a supply chain security tool whose own supply chain can't be verified is disqualified" (NFR7), the same disqualification logic applies to one that stores fleet-wide registry credentials with no stated protection requirement.

### 20. The external auditor's access path contradicts OIDC-only
UJ-3's Marta is internal — fine. But the realistic audit moment includes an *external* auditor, and NFR6 offers no path that doesn't mean provisioning an outsider in the corporate IdP. Either the signed pack alone is the auditor interface (then say so, and the read-only auditor role is for internal compliance), or NFR6 needs a guest-access story.

---

## Summary table

| # | Severity | Finding |
|---|----------|---------|
| 1 | Critical | 30-min install vs scale anchor vs own counter-signal — mutually unsatisfiable as written |
| 2 | Critical | Sigstore signing incompatible with air-gap as specified |
| 3 | Critical | Signed packs prove post-generation integrity only; evidence store mutability unaddressed |
| 4 | Critical | Registry-only SBOM blind spots hidden from blast-radius/evidence claims |
| 5 | Critical | OIDC-only sign-in breaks 30-min clock and no-tickets claim |
| 6 | Major | Prod-cluster helm rights silently assumed under "no dev-team cooperation" |
| 7 | Major | No agent authentication/trust requirement |
| 8 | Major | Inventory staleness unbounded |
| 9 | Major | FR26 filesystems leak through "no host scanning" fence |
| 10 | Major | VEX ingestion lacks trust model — auto-suppression vector |
| 11 | Major | Air-gap feed bundle implies unowned hosted infrastructure; NFR5 unmeetable offline |
| 12 | Major | FR6 determinism contradicted by FR7 |
| 13–20 | Minor | Unbounded artifact scope; alerting granularity; unknown-workload blast radius; GUAC orphaned; CRA mapping absent; sliding latency bar; credential handling; external auditor access |
