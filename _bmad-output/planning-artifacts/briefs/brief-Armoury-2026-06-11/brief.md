---
title: "Product Brief: Armoury"
status: final
created: 2026-06-11
updated: 2026-06-11
---

# Product Brief: Armoury

## Executive Summary

Armoury is a self-hosted control plane that makes a software fleet's vulnerability posture **operationally consistent and provable**. Enterprises have already standardized on the open-source supply chain security stack — Syft, Grype, GUAC — but can't operate it at scale: scanning is inconsistent across hundreds of repos, results go stale between builds, and nothing produced survives contact with an auditor. Armoury orchestrates that trusted OSS stack so every package and container image is SBOM'd and scanned the same way, on a lifecycle, with findings enriched from multiple post-NVD sources and recorded as audit-grade evidence.

The payoff lands at two moments. When a headline CVE drops, Armoury answers "which of our software — shipped *and running* — is affected?" in seconds instead of weeks. And when the auditor arrives, the evidence pack already exists. The EU Cyber Resilience Act's reporting obligations (from 2026-09-11) turn that second moment from a nice-to-have into a deadline, and the competitive lane — the consistency-and-evidence layer over the OSS stack — is currently vacant.

This brief is a builder's document: it defines what Armoury is, who it serves, and where its v1 boundaries sit, as the input to the PRD.

## The Problem

Enterprises have already standardized on the open-source supply chain security stack — Syft for SBOMs, Grype for scanning, GUAC for the graph — but they cannot operate it at scale. The tooling runs differently in every repo: 17 snowflake CI configs, inconsistent versions and flags, scans that only happen when a build happens. The result is a posture nobody can trust or prove.

The cost shows up at two moments:

1. **The log4shell moment.** A critical CVE drops and the question "which of our software and deployed fleet is running the affected version?" takes weeks of grep and spreadsheets to answer — because there is no fresh, uniform, queryable inventory of what is actually shipped.
2. **The audit moment.** The EU Cyber Resilience Act (reporting obligations from 2026-09-11) demands evidence of vulnerability handling, not intentions. Inconsistent ad-hoc scanning produces no evidence trail an auditor will accept.

Meanwhile, the data layer underneath is decaying: NIST abandoned universal NVD enrichment in April 2026, so any team relying on a single free feed is increasingly flying blind.

## The Solution

Armoury orchestrates the OSS stack the industry already trusts (Syft, Grype, GUAC, Grant, Sigstore) so that every package and container image in the fleet is SBOM'd and scanned the same way, on a lifecycle — re-evaluated when vulnerability feeds change, not just when a build runs. Findings are enriched from multiple post-NVD sources, and every result is recorded as audit-grade evidence.

The architecture is three layers:

- **Engine** — detection. Commodity by design: the free CVE data and OSS scanners everyone already uses, fully embraced rather than reinvented.
- **Chassis** — the product. Uniform execution across the fleet, lifecycle freshness, multi-source enrichment, and an evidence trail built for regulators (CRA compliance packs as the GTM spearhead).
- **Hero moment** — the payoff. When CVE X drops, Armoury answers "which of our software and deployed fleet is affected?" in seconds, because the chassis guarantees a fresh, uniform, queryable graph of everything shipped.

Detection insight is the output; consistency is the product.

## What Makes This Different

- **The lane is vacant.** The scanner market is saturated (Wiz, Snyk, Qualys), but nobody owns the consistency-and-evidence layer over the OSS stack: Kusari has drifted, Anchore is a government niche, Stacklok exited.
- **We sell the hard part, not the free part.** CVE data is free; Grype is free. The genuinely hard problems — identical execution across hundreds of repos and thousands of images, feed-driven rescanning, post-NVD enrichment, auditor-acceptable evidence — are what the invoice says.
- **Regulation is the forcing function.** CRA's 2026-09-11 reporting deadline turns "nice to have" into "need by Q3," and compliance packs make Armoury the cheapest path to a defensible answer.
- **Self-hosted and air-gapped from day one**, with provenance-attested delivery — table stakes for the enterprises that feel this pain most, and a moat against SaaS-only competitors.

## Who This Serves

**Primary user: the SecOps team at an SME** — typically small, covering a much larger engineering organization. The entry moment is sharp: *they have just survived a stressful audit* and are determined the next one won't be assembled by hand from spreadsheets, CI logs, and screenshots. Today they cope with ad-hoc scanner output scattered across repos and a compliance story they reconstruct after the fact. Success for them: the next audit's evidence is a report Armoury already generated, and when a critical CVE drops they answer the blast-radius question before the CTO asks it.

**Buyer: the CTO, with legal/compliance as champion.** CRA reporting obligations put the regulatory risk on their desk; Armoury is the cheapest defensible answer. The pitch to the buyer leads with evidence and compliance; the pitch to the user leads with "stop hand-assembling audits."

**Form factor: a Helm chart.** Armoury deploys into the customer's existing Kubernetes cluster — self-hosted by default, air-gap capable. Target: from `helm install` to first fleet-wide posture view in under 30 minutes.

## Scope

**v1 — what's in:**

- **Two data sources, zero dev-team cooperation required.** (1) *Static/registry*: Armoury connects to container registries and package feeds, generates SBOMs centrally (Syft) and scans them (Grype). (2) *Live cluster inventory*: Armoury watches the Kubernetes API for running image digests — what is actually deployed, where. Together these power the blast-radius answer for shipped *and* running software, installable by SecOps alone.
- **Lifecycle re-evaluation** — findings refreshed when vulnerability feeds change, not just when builds run.
- **Multi-source post-NVD enrichment** of findings.
- **CRA compliance pack** — audit-grade evidence reports as the flagship output.
- **License compliance (Grant)** — embedded in the orchestrated stack from day one as a supporting capability, not a headline. (Integration mechanics to be worked out in the PRD.)
- **Self-hosted Helm deployment**, air-gap capable, provenance-attested releases.

**Roadmap — deliberately later:**

- **Build-time integration** (blessed CI steps, build provenance, Sigstore attestation) — deepens evidence quality from "reconstructed from images" to "captured at build," once Armoury has earned org-wide buy-in. Ultimately the third data source: build, static, live.
- **Assistive AI remediation** (~2027, per market research).

**Explicitly out:**

- **Host/VM scanning** — different capability, different competitive set.
- **Runtime behavior analysis / threat detection** (eBPF, agents) — "live" means workload inventory, not Falco/Wiz territory.
- **SaaS-hosted offering** — self-hosted only to start; SaaS would dilute the wedge.
- **Source-code scanning (SAST)** — first-party code analysis is a different engine and competitive set (Semgrep, SonarQube); Armoury's domain is known vulnerabilities in shipped artifacts.
- **Auto-remediation PRs** — deferred with assistive AI remediation (~2027).

## What Good Looks Like

This is a builder's brief, so success is a quality bar for the tool, not a revenue target:

- **Audits get efficient.** A SecOps team walks into their next audit with an Armoury-generated evidence pack instead of weeks of hand-assembled spreadsheets — and it's accepted.
- **Threats surface effortlessly.** When a headline CVE drops, the blast-radius question — what's affected, what's running right now — is answered from Armoury in under a minute, not reconstructed by hand.
- **Deploy is genuinely 30 minutes.** From `helm install` to first fleet-wide posture view, by a SecOps engineer acting alone, with no dev-team cooperation.
- **Posture is trustworthy.** Every artifact in the fleet was scanned the same way with fresh feeds — no snowflakes, no stale results, no gaps anyone has to caveat.

## Vision

In 2–3 years, Armoury is the default operational layer over the OSS supply chain stack — the thing you install *because* you use Syft, Grype, and GUAC, the way Grafana became the default face of Prometheus. Build-time integration closes the loop so every artifact carries provenance from build through registry to live workload; compliance packs grow beyond CRA to the wider regulatory wave; and assistive AI remediation (~2027) sits on top of the evidence graph, suggesting fixes grounded in what's actually deployed. The commercial shape (open-core or otherwise) is deliberately undecided — the tool earns its place first.
