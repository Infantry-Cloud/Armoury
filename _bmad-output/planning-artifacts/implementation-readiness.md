---
status: pass
gate: PASS
date: 2026-11-06
history:
  - "2026-11-05 CONCERNS — Daniel chose: fix first, then rerun."
  - "2026-11-05/06 fixed by Correct Course (sprint-change-proposal-2026-11-05.md, decisions R1–R11); four independent gate reruns; final rerun: no blockers, two text concerns fixed and checked."
  - "2026-11-07 UX spines replaced by ux-Armoury-2026-11-06 (supersedes ux-Armoury-2026-06-12) and FR32/FR33 added (sprint-change-proposal-2026-11-07.md); this verdict predates them (the plan is now 11 epics, 79 stories) — rerun readiness after the Correct Course is applied."
sprint_status: _bmad-output/implementation-artifacts/sprint-status.yaml (11 epics, 77 stories, validated)
linear: INF-11 (planning:sprint)
inputs:
  - _bmad-output/planning-artifacts/prds/prd-Armoury-2026-06-11/prd.md
  - _bmad-output/planning-artifacts/architecture.md
  - _bmad-output/planning-artifacts/ux-designs/ux-Armoury-2026-06-12/DESIGN.md
  - _bmad-output/planning-artifacts/ux-designs/ux-Armoury-2026-06-12/EXPERIENCE.md
  - _bmad-output/planning-artifacts/epics.md
---

# Implementation Readiness — Armoury

**Current verdict: PASS (2026-11-06) — stale: assessed against ux-Armoury-2026-06-12, which ux-Armoury-2026-11-06 superseded; rerun after the 2026-11-07 Correct Course.** The findings below are the first run (CONCERNS). The
Correct Course change record `sprint-change-proposal-2026-11-05.md` resolved them; see its
gate-rerun sections for later findings and fixes.

Question: could a developer implement these epics without inventing decisions nothing records?

Verdict: **CONCERNS.** Traceability holds: every PRD FR/NFR is backed by story acceptance criteria;
all ACs are Given/When/Then; the parser dry run finds 10 epics / 68 stories, matching the Linear
manifest. The gaps below are story-local, not plan-wide. Fix them with `bmad-correct-course`
(cross-cutting) or the owning plan skill, then rerun `bmad-sprint-planning`.

## Fix before the affected story starts

| # | Gap | Stories | Evidence | Owner skill |
|---|-----|---------|----------|-------------|
| 1 | No story builds a container image (multi-stage Dockerfile with SPA + pinned tools, agent image, kind load) before Story 10.1. Story 1.2 therefore depends forward on 10.1. | 1.1/1.2, 2.3, 2.4, 2.12, 7.1 | `epics.md:296-345, 591, 805, 1994`; `architecture.md:340` | bmad-correct-course |
| 2 | Ledger entries store only a payload digest. Story 9.1 must reconstruct any past window "from recorded evidence only" (FR23). History written in Epics 2–8 cannot be backfilled. Keep full payloads or append-only history from day one, with a reconstruct test. | 2.1 → 9.1 | `epics.md:540, 1803` | bmad-correct-course |
| 3 | Feed-delta computation between two Grype DB versions is undecided (read SQLite directly? schema version? per-version cache dirs?). Core of NFR5. | 4.2 | `epics.md:1032`; `architecture.md:61, 427` | bmad-architecture (amendment) |
| 4 | Runtime keyless signing has no identity source: public Fulcio does not trust an in-cluster service-account issuer. Record the identity, or make operator key the runtime default and keep keyless for CI. | 9.4, 9.6, ARCH30 checkpoints | `architecture.md:174, 214, 430`; `epics.md:1875, 1938` | bmad-architecture (amendment) |
| 5 | No streaming / live-update pattern (SSE, cursor polling, async query resource). Changes the 6.2 API contract. | 2.9, 6.2, 6.3 | `epics.md:739, 1427, 1474`; `architecture.md:175, 301` | bmad-architecture (amendment) |
| 6 | Story 9.5 lets auditors generate packs by default; PRD makes auditor read-only and gives pack generation to analyst. Pack generation writes ledger entries. | 9.5 | `prd.md:48, 113`; `epics.md:1917`; `EXPERIENCE.md:142` | bmad-correct-course |
| 7 | `architecture.md` still lists VEX formats and retention as open; ARCH29, ARCH30 and PROC2 exist only in `epics.md`. Its data boundary omits the partition-dropping maintenance role. Story 5.6 cites a VEX mapping amendment that does not exist. | 2.1, 5.6, 9.6, 9.7 | `architecture.md:399, 462-464`; `epics.md:139-142, 1364` | bmad-architecture (update) |

## Concerns

### Story 1.1 (next story) gaps
- OpenAPI server/TS generation with a CI diff check (ARCH12) is assigned to no story; Story 1.6 assumes a generated TS client (`epics.md:302, 456`).
- Postgres with AGE is not provisioned for `#[sqlx::test]` in `task check` and CI.
- Playwright is not set up, but Story 1.7 axe checks need it.
- `riverqueue` is not added; current crate is v0.5 (architecture says v0.4), needs `sqlx ^0.9` and `jiff`; its migrator (`riverqueue-migrate`) vs `sqlx migrate` is unstated. No story proves the client runs jobs, not only inserts them (fallback `graphile_worker`).

### Dependencies and missing links
- Story 4.4 AC tests a blast-radius/CVE-detail lookup (`epics.md:1093`); blast radius arrives in 6.2 (already restated at `1449-1451`). Move the AC.
- `signing` module owner unclear: 4.5 signs bundles, 4.6 verifies, 9.4 describes it as new (`epics.md:1132, 1146, 1875`; ARCH19).
- Story 5.7 imports vendor VEX "in an air-gapped bundle" (`epics.md:1379`); 4.5 bundle contents exclude VEX (`1123`), 4.6 never ingests it.
- FR9 one-hour onboarding covers images and packages (`prd.md:71`); only 2.5 tests images (`epics.md:646-650`); 2.6/2.7 omit it.
- NFR7 requires feed bundles signed and SLSA-attested (`prd.md:114`); 10.2 only signs (`epics.md:2023`).
- Story 7.1 covers new SBOMs only; no licence backfill for SBOMs stored before Epic 7 (`epics.md:1586`).
- Minor backward references to later stories: 1.5 theme change before the picker (1.6/1.8); 3.1 revocation marks runtime data stale before 3.2; 5.3 refers to the 5.4 decision form.

### Undecided technical details
- "New critical/KEV findings" metric semantics (counter vs gauge, window, baseline) (`prd.md:89`; `epics.md:1748`).
- Ledger "reserved quota/tablespace" is not buildable (Postgres has no tablespace quotas; impossible on external DB) (`epics.md:556`).
- PDF renderer (air-gap safe) for 6.5/9.3 (`epics.md:1514, 1850`).
- OCI registry client and repository discovery (ECR, Docker Hub, GAR lack `_catalog`) for 2.2.
- Bundled Postgres-with-AGE image and chart dependency (`architecture.md:189`) for 1.2/10.3.
- Syft invocation for package archives (fetch + `file:`/`dir:` sources) for 2.6/2.7 (`architecture.md:211`).
- Agent gRPC listener port and mTLS termination (in-process rustls vs ingress) for 1.2/3.2/3.4.
- Air-gap egress rule lists only `feeds`, `enrichment`, `signing` (`architecture.md:400`), but `auth` (OIDC) and `inventory`/`tools` (registries) also call out; 10.3 adds an admin-endpoint exception the architecture lacks.
- Story 10.1 puts Syft/Grype/Grant/cosign in the agent image; architecture puts them in the control-plane image only (`epics.md:1998`; `architecture.md:145, 372`).
- Smaller: session store location; `openapi-typescript` vs orval; `openapi-generator` needs Java in CI; how OpenAPI marks a route's role (1.4 test); Grype DB publishes checksums, not signatures (4.1); envelope-encryption cipher.
- Vendor VEX product matching (purl / CPE / digest → artifact) unspecified (5.7, `epics.md:1382`).

### UX (historical — refers to ux-Armoury-2026-06-12: Forge/Gunmetal, page header, DQ badge opacity; superseded)
- Opacity dimming fails the 1.7 WCAG AA gate: DQ badge at 0.65 (~3.9:1 Forge, ~3.5:1 Gunmetal) and "not running" node at 0.5 (~2.4:1) (`DESIGN.md:205-206, 293, 300`; `epics.md:470-473, 1488, 1732`).
- Theme persistence store/endpoint undefined; UX marks it [ASSUMPTION] handed to architecture, never closed (`EXPERIENCE.md:76`; `.decision-log.md:66`; `epics.md:426`).
- Page header (search + compact theme switcher) owned by no story; only `mockups/hybrid-posture-v2.html:128, 371-376` defines it; 6.3 assumes it exists (`epics.md:1468`).
- Settings has no navigation pattern; new panels (licence-warning toggle, pack restriction, retention) are outside UX-DR28 (`epics.md:1627, 1657-1660, 1917, 1960`).
- Digest-rooted blast-radius answers have no tier order, headline or graph direction (`epics.md:1440-1443, 1463`; `EXPERIENCE.md:99`).
- PDF report has no visual/print spec (6.5, 9.3).
- Triage scope choice and "which decision applies" display are not designed or in 5.4 (`epics.md:1275-1276`).
- Key bindings are [ASSUMPTION] in UX but locked in UX-DR7/1.8 (`EXPERIENCE.md:84, 152`; `epics.md:164, 522-525`).
- `DESIGN.md:238` still says "shadcn/ui + Tailwind" (pre-Svelte leftover).

### Size and testability
- Too large for one cycle: 1.7, 9.7, 5.3.
- 3.1, 4.5, 5.1, 8.1 combine a user-approved architecture amendment with the build; consider a spike per decision and split 3.1 (enrol vs renew/revoke). They are correctly gated, not invented.
- ACs without numbers: "latency budget recorded… stated tolerance" (`832`), "within budget" (`921`), "a few seconds" (`1474`), "p50 answers in seconds" (`1559`), "nothing broken" (`494`), "sensible defaults" (`1171`), "documented defaults" (`1629`, conflicts with PROC2), heartbeat thresholds (`923`), "lower" DQ grade (`1732`).

## Minor
- Artifact types `oci_artifact` (2.8) and `filesystem` (7.2) are absent from the PRD glossary (`prd.md:157`) and the Artifacts list "image/package" (`epics.md:786`).
- No PRD basis recorded for 10.2 daily Armoury-published bundles with key rotation, and the 10.1 self-scan publication.
- NFR1 24-hour initial scan is projected, not measured (`epics.md:828`); 4.8 bounds only the Grype DB delta, not enrichment-only re-joins.
- FR14 "team consumption" has no explicit AC.
- Architecture Go leftovers: `control-plane/internal` (`architecture.md:397`), "packages" for Rust modules (`400, 404`).

## Next
1. Run `bmad-correct-course` with this file for items 1, 2, 6 and the epics-side concerns.
2. Run `bmad-architecture` (update) for items 3, 4, 5, 7 and the undecided technical details.
3. Rerun `bmad-sprint-planning`; on PASS (or accepted CONCERNS) it generates `sprint-status.yaml` and closes INF-11.
