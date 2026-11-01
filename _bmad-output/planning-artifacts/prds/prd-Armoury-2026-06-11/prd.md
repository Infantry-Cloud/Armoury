---
title: Armoury PRD
status: final
created: 2026-06-11
updated: 2026-06-12
---

# Armoury PRD

## Vision

Armoury is a self-hosted control plane that makes a software fleet's vulnerability posture **operationally consistent and provable**. It orchestrates the open-source stack the industry already trusts — Syft, Grype, GUAC, Grant, Sigstore — so that every package and container image in the fleet is SBOM'd and scanned the same way, on a lifecycle: re-evaluated when vulnerability feeds change, not just when a build runs. Findings are enriched from multiple post-NVD sources, and every result is recorded as audit-grade evidence.

**Detection insight is the output; consistency is the product.** The layers have names. The **engine** is detection — commodity by design: free CVE data and the OSS scanners everyone already uses, fully embraced rather than reinvented. The **chassis** is the product — uniform execution across the fleet, lifecycle freshness, multi-source enrichment, and an evidence trail built for regulators. The chassis is what the invoice says: we sell the hard part, not the free part. The **hero moments** are the payoff — the **log4shell moment**, when a critical CVE drops and Armoury answers "which of our software, shipped and running, is affected?" in seconds; and the **audit moment**, when the evidence pack already exists instead of being hand-assembled from spreadsheets and screenshots.

The 2–3 year ambition: become the default operational layer over the OSS supply chain stack — the thing you install *because* you use Syft, Grype, and GUAC, the way Grafana became the default face of Prometheus.

The primary surface is a web UI: the first fleet-wide posture view and the blast-radius query both live there.

## Users & Journeys

The primary user is the SecOps team at an SME — a small team covering a much larger engineering org, freshly determined after a stressful audit that the next one won't be assembled by hand. The buyer is the CTO; the champion is legal/compliance. The pitch is dual: the buyer hears evidence and regulatory defensibility; the user hears "stop hand-assembling audits."

### UJ-1 — The first 30 minutes

Priya is the senior — and only dedicated — security engineer at a 200-person company `[ASSUMPTION: size/shape of the SME]`. Last month's audit cost her three weeks of spreadsheet archaeology. Today she carves out a morning to try Armoury.

1. She runs `helm install` for the control plane into the ops cluster she already administers. No tickets to the platform team `[ASSUMPTION: SecOps has helm rights on at least one cluster]`.
2. She opens the web UI and signs in with the bootstrap admin she set in her Helm values. The company OIDC provider is a few more config values — she'll add them on the next `helm upgrade`. SSO is never allowed to stand between her and minute 29.
3. Setup asks for a registry connection: she pastes read-only credentials for the company registry `[ASSUMPTION: a single primary registry in the first session]`. Armoury starts enumerating images and generating SBOMs immediately — she can watch the inventory fill.
4. She installs the cluster agent into the prod cluster with a second one-line `helm install`. Running workloads start appearing, linked to the registry artifacts.
5. At minute 29 she's looking at the fleet posture view: every image SBOM'd and scanned the same way, findings ranked by KEV/EPSS priority, coverage gaps honestly displayed. For the first time, the whole fleet is in one place she doesn't have to caveat.

### UJ-2 — CVE day

Three weeks later, a critical CVE in a popular logging library hits the news and lands on the KEV list. Priya's feeds updated overnight, and Armoury has already re-evaluated every SBOM — no rescans, no rebuilds.

1. Her own Grafana alert (built on Armoury's Prometheus metrics) pinged her before she'd finished her coffee `[ASSUMPTION: she wired alerting in week one]`.
2. She opens Armoury, types the CVE ID into the blast-radius query. Seconds later: 14 affected images, 9 running — which clusters, which namespaces, which workloads.
3. She exports the result and posts it to the CTO — before he's read the news.
4. She triages: two services don't invoke the vulnerable code path — she records *not affected* with justification; the rest get flagged for the owning teams `[ASSUMPTION: handoff to dev teams happens outside Armoury in v1]`.
5. Every step — detection, decision, justification — is already in the evidence trail for the next audit.

### UJ-3 — Audit day

Six months in, the annual audit lands `[ASSUMPTION: audit cadence]`. Marta, the compliance lead who championed Armoury to the CTO, opens Armoury with the read-only auditor role.

1. Priya generates a CRA evidence pack for the audit window: inventory, scan uniformity, feed freshness, every finding with its documented handling decision, the license compliance section.
2. The pack is Sigstore-signed; the auditor can verify nothing was edited after generation.
3. What was three weeks of spreadsheet archaeology is now a generated, signed document plus machine-readable attachments. The audit moment passes without a scramble.

## Features

Armoury v1 ships six feature groups. Deployment topology: a **control plane** (hosting the web UI, graph, and evidence store) installed via Helm, plus a lightweight **cluster agent** per Kubernetes cluster that reports workload inventory back to the control plane. FR IDs are stable and never renumbered; FR29–FR30 were added at finalize and sit out of numeric sequence.

### 1. Fleet Inventory

Two data sources, both operable by SecOps alone — zero dev-team cooperation.

- **FR1** — Registry connection: SecOps provides container registry credentials; Armoury enumerates repositories and image digests. No CI changes required.
- **FR29** — Package feed connection: beyond container registries, SecOps connects package feeds and artifact repositories (language-ecosystem registries, internal artifact mirrors); Armoury enumerates packages and SBOMs them the same uniform way.
- **FR2** — Central SBOM generation: Armoury generates SBOMs (Syft) for every discovered artifact, centrally and uniformly — no per-repo configuration.
- **FR3** — Live cluster inventory: a cluster agent watches the Kubernetes API in each connected cluster and maintains a live record of running image digests — what is deployed, where (cluster/namespace/workload) — reported back to the control plane.
- **FR4** — Shipped-vs-running reconciliation: registry artifacts and running workloads are linked in one inventory, so "is this running anywhere?" is answerable per artifact.
- **FR5** — Coverage visibility: the inventory shows its own gaps — discovered-but-not-yet-SBOM'd images, unreachable registries, disconnected agents — so posture is never silently incomplete.

### 2. Consistent Scanning & Lifecycle Freshness

- **FR6** — Uniform scanning: every SBOM is scanned (Grype) with one fleet-wide configuration and policy. No per-artifact or per-team snowflake configs — the same artifact always produces the same result.
- **FR7** — Feed-driven re-evaluation: when vulnerability feeds update, Armoury automatically re-evaluates existing SBOMs against the new intel. Findings stay current without rebuilds or manual rescans.
- **FR8** — Evaluation provenance: every finding records when it was last evaluated and against which feed versions — posture views and evidence packs prove freshness rather than assert it.
- **FR9** — Continuous onboarding: newly discovered images and packages are SBOM'd and scanned automatically, within one hour of discovery `[ASSUMPTION: 1-hour discovery-to-scan bound]` — no manual triggering.
- **FR10** — Air-gapped feed updates: vulnerability and enrichment feeds can be imported as a signed offline bundle, downloaded on a connected machine and applied to an air-gapped Armoury. Air-gapped operation is a v1 requirement, not a roadmap note.

### 3. Enrichment & Prioritization

- **FR11** — Multi-source enrichment: findings are enriched from multiple post-NVD sources — CISA KEV, EPSS, CNA records, OSV — closing the gap NIST left when it abandoned universal NVD enrichment.
- **FR12** — Source attribution: every enrichment datum is labeled with its source and retrieval time, so an auditor can see where a severity or exploited-status claim came from.
- **FR13** — Risk-based prioritization: posture views rank findings using enrichment signals so a small SecOps team sees the findings that matter, not ten thousand rows. Ranking is deterministic and explainable — KEV-listed findings first, then EPSS-weighted severity — and the UI can always show why a finding ranks where it does.
- **FR14** — Triage decisions as first-class data: an analyst can record a handling decision on any finding — status (e.g. not affected, mitigated, accepted, fix planned), justification, author, timestamp. Decisions propagate everywhere the finding appears: posture views, team consumption, and evidence packs, where they constitute documented vulnerability handling.
- **FR15** — VEX support: triage decisions are expressible as standard VEX statements, and Armoury ingests VEX documents from upstream vendors, applying their not-affected claims (with attribution) to fleet findings.

### 4. Blast-Radius Query & Posture View

- **FR16** — Fleet posture view: the web UI's landing state — fleet-wide summary of artifacts, findings by priority, coverage gaps, and feed freshness. This is what appears at minute 29 of the install.
- **FR17** — Blast-radius query: given a CVE ID or a package+version ("who uses log4j 2.x?"), Armoury answers which artifacts — shipped and running — are affected, and where they are deployed (cluster/namespace/workload). Answered in seconds. Every answer carries its data provenance: which sources it rests on (registry-derived SBOM, live inventory), and their coverage and freshness — the answer is definitive in tone only when the data earns it.
- **FR18** — Artifact detail: per artifact — SBOM contents, findings (vulnerability and license) with triage status, evaluation provenance, and running locations.
- **FR19** — Shareable answers: a blast-radius result or posture summary can be exported (report/CSV) — the thing the SecOps engineer hands the CTO before being asked.
- **FR20** — Prometheus metrics: the control plane exposes posture signals as Prometheus metrics — new critical/KEV findings, coverage gaps, feed freshness, agent health — so teams build alerting with the observability stack they already run. v1 is pull-only; Armoury sends no notifications itself.
- **FR30** — Data-quality score: alongside risk scores, Armoury computes a data-quality score for the security team — grading the trustworthiness of the underlying data itself: SBOM depth and completeness, scan coverage, feed freshness, enrichment source coverage, and CVE record quality. Surfaced at artifact and fleet level in posture views and evidence packs, so consumers know how much to trust an answer, not just what the answer is.

### 5. Compliance Evidence

- **FR21** — CRA compliance pack: generate an audit-grade evidence report for a chosen time window — fleet inventory, proof of uniform scanning and feed freshness, findings with their documented handling decisions, and a license compliance section. Packs state their own coverage and data provenance (FR30): what was under management, with what data quality, for the window reported. The flagship output: the audit that is already assembled.
- **FR22** — Compliance packs as a layer: the CRA pack is the first instance of a pack architecture — framework-specific report definitions over the same evidence graph — so future frameworks (DORA, FedRAMP, PCI) are additive, and CRA timeline slippage does not strand the work.
- **FR23** — Evidence collected continuously, generated on demand: packs draw on evidence Armoury already recorded (scans, feed versions, decisions), not on a scramble at generation time. Any period the fleet was under management is reportable after the fact. Evidence retention is configurable with a compliance floor — default at least 24 months `[ASSUMPTION: retention default]`.
- **FR24** — Auditor-consumable formats: packs export as polished documents (PDF) with machine-readable companions (SBOMs, VEX) attached.
- **FR25** — Signed evidence packs: generated packs are signed, so an auditor or regulator can verify a pack has not been altered since generation. Connected deployments may use Sigstore keyless signing; air-gapped deployments sign with operator-managed keys — verifiability never depends on internet access.

### 6. License Compliance

- **FR26** — License evaluation: Grant evaluates licenses across the full surface it supports — SBOMs, container images, and filesystems. Armoury runs it against the SBOMs it generates by default, but does not restrict Grant's existing capability; any artifact Armoury can inventory can be license-checked.
- **FR27** — License policy: a fleet-wide allow/deny license policy; violations surface as findings alongside CVEs in the same posture and artifact views, and are triagable with the same decision model (FR14).
- **FR28** — License evidence: the license section of evidence packs (FR21) draws from this data — embedded, never headline.

## Non-Functional Requirements

- **NFR1 — Time to value:** `helm install` to first fleet-wide posture view in under 30 minutes, performed by a single SecOps engineer with no dev-team cooperation. Minute 29 is defined honestly: control plane installed, sources connected, posture view live and *visibly populating* with an explicit coverage indicator — not a completed fleet scan. Full initial evaluation completes within 24 hours at the scale anchor `[ASSUMPTION: 24-hour initial-scan bound]`. This bar is a product gate, not a marketing line: any v1 feature that breaks it doesn't ship in the install path.
- **NFR2 — Query performance:** blast-radius queries answer in seconds — under a minute worst case — at the scale anchor below.
- **NFR3 — Scale anchor:** v1 must be comfortable at hundreds of repositories, thousands of container images, and up to ten connected clusters `[ASSUMPTION: cluster count ceiling]`.
- **NFR4 — Deployment:** self-hosted only, delivered as a Helm chart into the customer's existing Kubernetes. Air-gapped operation is fully supported (see FR10) — no phone-home, no capability that silently requires internet access.
- **NFR5 — Freshness:** after a feed update lands (online or via offline bundle), fleet-wide re-evaluation completes within one hour at the scale anchor `[ASSUMPTION: 1-hour bound]`.
- **NFR6 — Access control:** sign-in via OIDC SSO, configured declaratively — environment variables / Helm values / config file, never a UI wizard. A bootstrap admin field in the same config provides first sign-in and IdP-outage recovery. OIDC is optional at install: its absence never blocks the install path. Three roles: admin (configuration, connections), analyst (triage decisions, pack generation), read-only auditor `[ASSUMPTION: role set]`.
- **NFR7 — Armoury's own provenance:** releases (images, charts, feed bundles) are signed and provenance-attested (SLSA via Sigstore). A supply chain security tool whose own supply chain can't be verified is disqualified from its own market.
- **NFR8 — Honest degradation:** failures degrade visibly, never silently — disconnected agents, stale feeds, and unscanned artifacts are surfaced in the posture view and metrics (FR5, FR20). The fleet posture must never need a caveat the UI doesn't already show.
- **NFR9 — Agent footprint:** cluster agents are lightweight and read-only — they require only watch/list access to the Kubernetes API and never need cluster-admin `[ASSUMPTION: read-only scope is sufficient for v1 inventory]`.
- **NFR10 — Availability:** v1 targets single-instance control plane; HA is not a v1 requirement `[ASSUMPTION]`. Loss of the control plane never loses recorded evidence (durable storage).
- **NFR11 — Evidence integrity:** the evidence store is append-only and tamper-evident — recorded scans, feed versions, and triage decisions cannot be silently edited or deleted. Pack signing (FR25) seals a snapshot; this requirement makes the history beneath it trustworthy.

## Scope & Roadmap

**No deadlines.** v1 ships when it meets the quality bars below. EU CRA reporting obligations (from 2026-09-11) remain market context — they explain why buyers care — not a delivery date.

### Explicitly out of scope

- **Host/VM scanning** — a different capability and competitive set; Armoury's domain is shipped artifacts.
- **Runtime behavior analysis / threat detection** (eBPF, agents-watching-syscalls) — "live" means workload inventory, not Falco/Wiz territory.
- **SaaS-hosted offering** — would dilute the self-hosted wedge.
- **SAST / source-code scanning** — Semgrep/SonarQube/CodeQL territory; Armoury's domain is known vulnerabilities in shipped artifacts.
- **Auto-remediation PRs** — deferred with the AI work.
- **Multi-scanner orchestration / cross-scanner normalization** — deliberately rejected, not deferred: Armoury goes hard on Syft and Grype. The research's neutrality whitespace was largely about aggregating static-analysis scanners, which Armoury does not do.
- **Reachability analysis** — the top practitioner-requested noise-reduction differentiator, deliberately unclaimed in v1; revisit alongside the AI work.

### Roadmap (deliberately after v1)

- **Build-time integration** — blessed CI steps, build provenance, Sigstore attestation at build. Upgrades evidence from "reconstructed from images" to "captured at build" and completes the three-source model: build, static/registry, live.
- **MCP query server** — read-only interface letting AI assistants query posture and blast radius; rides the same query layer as the web UI.
- **Assistive AI remediation** (~2027) — assistive, not autonomous.
- **Additional compliance packs** — DORA, FedRAMP, PCI on the pack architecture (FR22).

## Success Criteria

Success is a quality bar for the tool, not a revenue target. Four bars:

1. **Audits get efficient** — an Armoury-generated evidence pack replaces weeks of hand-assembled spreadsheets, *and it's accepted by the auditor*.
2. **Threats surface effortlessly** — the blast-radius question is answered from Armoury in under a minute.
3. **Deploy is genuinely 30 minutes** — by one SecOps engineer, alone, with no dev-team cooperation.
4. **Posture is trustworthy** — uniform scanning, fresh feeds, no caveats anyone has to append by hand.

Counter-signals to watch (the bars must not be gamed):

- Install speed must not be bought with posture completeness — a fast install that silently skips half the registry fails bar 4, not passes bar 3.
- Prioritization and triage must reduce noise without burying true positives — a quiet dashboard is not the same as a safe fleet.
- Evidence-pack polish must never outrun data integrity — a beautiful signed report over stale data is the failure mode the whole product exists to prevent.

## Glossary

- **Artifact** — a unit Armoury inventories and evaluates: in v1, a container image (FR1) or a package from a connected feed (FR29). Grant can additionally evaluate filesystems (FR26).
- **Fleet** — everything across all connected clusters, registries, and feeds.
- **Finding** — an evaluated condition against an artifact: a vulnerability match or a license-policy violation, carrying enrichment, triage status, and provenance.
- **Posture** — the fleet-wide, freshness-labeled state of findings and coverage.
- **Evidence** — the append-only record of what was scanned, with which feeds, what was found, and what was decided (NFR11).
- **Evidence pack** — a signed, auditor-consumable report generated from evidence for a time window (FR21).
- **Control plane / cluster agent** — the central install (web UI, graph, evidence store) / the per-cluster read-only inventory reporter.

## Assumptions Index

All inline `[ASSUMPTION]` tags, collected for downstream consumers:

1. SME shape: ~200-person company, lone dedicated security engineer (UJ-1)
2. SecOps has helm rights on at least one cluster (UJ-1)
3. Single primary registry in the first session (UJ-1)
4. OIDC configured declaratively (env vars / Helm values / config), optional at install; bootstrap admin field for first sign-in (UJ-1, NFR6)
5. Alerting wired via Prometheus/Grafana in week one (UJ-2)
6. Dev-team handoff happens outside Armoury in v1 (UJ-2)
7. Annual audit cadence (UJ-3)
8. Discovery-to-scan bound: one hour (FR9)
9. Evidence retention default: at least 24 months, configurable (FR23)
10. Scale ceiling: up to ten connected clusters (NFR3)
11. Initial full-fleet evaluation within 24 hours at scale anchor (NFR1)
12. Feed-update-to-re-evaluation bound: one hour (NFR5)
13. Role set: admin / analyst / read-only auditor (NFR6)
14. Read-only agent scope sufficient for v1 inventory (NFR9)
15. No HA in v1; evidence storage durable (NFR10)
