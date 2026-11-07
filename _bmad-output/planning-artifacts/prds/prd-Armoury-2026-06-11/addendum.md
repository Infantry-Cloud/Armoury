# Armoury PRD Addendum

Depth that belongs downstream (architecture, UX), or that earned a record here but not a place in the PRD body.

## Deployment topology (→ architecture)

Daniel's call: hub-and-spoke — a **control plane** (web UI, GUAC graph, evidence store) plus a lightweight **cluster agent** per Kubernetes cluster feeding inventory back to the control plane. Transport/protocol between agent and control plane, agent install/upgrade mechanics, and whether agents buffer during control-plane outages are architecture decisions, not PRD content.

## Options considered

- **License surfacing** (resolved → FR26–FR28): (A) finding type in the same posture views + evidence-pack section — chosen; (B) dedicated license dashboard — rejected, promotes a supporting capability to headline; (C) evidence-pack-only — rejected, SecOps couldn't act before audit day.
- **Triage/VEX sizing** (resolved → FR14–FR15): full VEX (record + ingest vendor VEX) chosen over internal-triage-only or deferral. Daniel: decisions must be "recorded/justified ... which drips down into team consumption and reports etc, thats helpful data."
- **Notifications** (resolved → FR20): pull-only v1; push notifications rejected in favor of Prometheus metrics + customer-owned alerting ("the secops team would set up some sort of alerting"). Fits the Grafana/Prometheus ethos.
- **AI/MCP** (deferred): read-only MCP query server considered for v1 as a 7th feature group; deferred to roadmap to protect the <30-min wow and keep v1 at six groups. Distinct from (and smaller than) the ~2027 assistive-AI-remediation deferral.

## Scanner neutrality — deliberately rejected (finalized 2026-06-11)

Market research named multi-scanner neutrality/normalization as whitespace and a bundling-defense moat. Daniel rejected it: "just go hard on grype and syft, the scanner neutrality was mainly static analysis which this doesn't currently aggregate anyway so doesn't matter." Recorded in the PRD's out-of-scope section as rejected-not-deferred. Related research signal left unadopted (neither v1 nor roadmap): **vendor/third-party SBOM ingestion** — revisit if procurement-driven demand appears.

## Data-quality score genesis (FR30)

Born from the adversarial finding on blast-radius false confidence. Daniel's enhancement: "if we have like the cve scores and stuff perhaps make another score for the ops/security team which scores the quality of the data and sboms and cve reports etc." Scoring inputs (SBOM depth, scan coverage, feed freshness, enrichment coverage, CVE record quality) and the scoring model itself are architecture/UX decisions. Placement (Correct Course 2026-11-07, D2): the UX spine ux-Armoury-2026-11-06 shows the score in Software detail (a score and letter plus a five-part quality meter), in the audit report detail in Reports and on the printed cover page; not on Home (it may join the Home Details tab later) and never in list rows. Grade bands are a UX placeholder until the scoring model (Story 8.1) exists.

## Grant capability note (→ architecture)

Grant natively evaluates licenses in SBOMs, container images, and filesystems. FR26 deliberately preserves the full surface — Daniel rejected an SBOM-only framing as "limiting the grant functionality that already exists for no good reason." Default pipeline runs Grant against Armoury-generated SBOMs; the wider surface stays available.

## Commercial model (parked — do not import into PRD)

Deliberately undecided; open-core (OSS chassis, paid compliance packs) is the natural candidate. Details live in the product brief addendum (`_bmad-output/planning-artifacts/briefs/brief-Armoury-2026-06-11/addendum.md`). "The tool earns its place first."

## UX spine change (2026-11-06/07) (→ UX, architecture)

The UX spine ux-Armoury-2026-11-06 supersedes ux-Armoury-2026-06-12: a light default plus one calm dark theme, a labelled sidebar (Home · Software · Issues · Exposure · Reports · Settings · Help), three-column master-detail, plain-language UI labels over this PRD's domain terms (Glossary → UI labels), severity groups instead of one ranked list (FR13), a review panel with per-issue scope (FR14), stored exports (FR19) and the Monday check for the engineering leader (UJ-4). PRD terms stay the domain and API vocabulary. Open UX gaps against PRD requirements: vendor VEX claims with attribution (FR15) have no surface; the CI-scan landing in Software (FR31) is undecided; licence review copy is not drawn (FR27).

## Signature verification and end-of-life data (FR32, FR33) (→ architecture, UX)

Daniel's call (2026-11-07, Correct Course D10): the approved UX shows "Signed" and end-of-life lines in Software detail, so both enter v1 by PRD change rather than being dropped from the design. Left to architecture (amendments approved before Stories 4.9 and 4.10): the trust configuration for signatures (keys, keyless identities, per registry or fleet-wide), how the Sigstore trusted root reaches air-gapped instances, which signature formats and artifact types are checked; the end-of-life data source and its licence, what it covers, how packages are matched and its staleness threshold. Left to UX: the words for each signature state and the end-of-life lines. Decided for v1 (2026-11-07, O13): signature and end-of-life results are shown only; they create no issues and do not change counts. The "Build-time integration" roadmap item is unchanged: it captures Armoury-side build provenance; FR32 verifies signatures that already exist.
