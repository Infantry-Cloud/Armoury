# Addendum — Armoury Product Brief

Depth that belongs downstream (PRD, architecture) or was deliberately parked, preserved here so it isn't lost.

## Open for the PRD: Grant / license compliance integration

Decided IN for v1 as an embedded supporting capability (not a headline), but the integration mechanics are unresolved — Daniel: "should be embedded from day 1, just need to work out how." The PRD must answer where license findings surface (same posture views? separate report? part of the compliance pack?).

## Parked: commercial model

Deliberately unresolved. The brief is a builder's document; Daniel declined business-style success criteria ("this is all about building a good tool"). When the question returns: open-core is the natural candidate for self-hosted security tooling (OSS chassis, paid compliance packs), and the CRA spearhead implies an eventual paid compliance-pack SKU. Revisit once the tool has real users.

## Rejected alternatives (rationale worth keeping)

- **Host/VM scanning ("servers")** — Daniel's initial fleet definition included servers; cut as too large a scope. Different capability and competitive set from the artifact-centric Syft/Grype/GUAC stack. Cutting hosts does NOT cut *live workload inventory*: watching the Kubernetes API for running image digests is in v1 and essential to the blast-radius answer.
- **Runtime behavior analysis / eBPF / threat detection** — explicitly fenced off from the "live" data source. Falco/Wiz territory; would re-import the cut servers scope through the back door.
- **Build-time-first integration (Option B as v1)** — rejected for v1 because day-one value would depend on dev-team adoption across hundreds of pipelines, killing the <30-minute wow and mismatching the SecOps-acting-alone user. Roadmap, not never: build provenance + Sigstore attestation upgrade evidence quality from "reconstructed from images" to "captured at build." Phasing — Daniel: "ultimately we need both, but A from day 1 ... it needs to scan the deployed/live workloads too so three data sources, build, static/registry, live."
- **SAST / source-code scanning** — different engines, findings, and competitive set (Semgrep, SonarQube, CodeQL); would blur the known-vulnerabilities-in-artifacts wedge.

## Source artifacts

- Brainstorming session: `_bmad-output/brainstorming/brainstorming-session-2026-06-03-2216.md`
- Market research (validated wedge + four sharpenings): `_bmad-output/planning-artifacts/research/market-software-supply-chain-security-research-2026-06-11.md`
