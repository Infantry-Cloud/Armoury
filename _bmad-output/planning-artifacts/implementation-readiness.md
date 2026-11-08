---
status: concerns-accepted
accepted: 2026-11-07 — Daniel explicitly accepted the CONCERNS verdict (third rerun); story-local concerns go to each story's Build planning
gate: CONCERNS
date: 2026-11-07
history:
  - "2026-11-05 CONCERNS — Daniel chose: fix first, then rerun."
  - "2026-11-05/06 fixed by Correct Course (sprint-change-proposal-2026-11-05.md, decisions R1–R11); four independent gate reruns; final rerun: no blockers, two text concerns fixed and checked."
  - "2026-11-06 PASS — assessed against ux-Armoury-2026-06-12 (now superseded)."
  - "2026-11-07 FAIL — rerun after sprint-change-proposal-2026-11-07.md (Greenhouse UX, FR32, FR33): 8 blockers. Daniel chose: fix the blockers, then rerun."
  - "2026-11-07 FAIL (narrow) — second rerun after sprint-change-proposal-2026-11-07-readiness.md: blockers 1–8 closed; 1 new blocker (vulnerability ID aliases). Daniel chose: fix it with the cheap concerns, then rerun."
  - "2026-11-07 CONCERNS — third rerun after sprint-change-proposal-2026-11-07-aliases.md: blockers 1–9 closed; missing story gates (N1–N6, N9, N10, O2, O20) added as follow-up-2; story-local concerns remain."
sprint_status: _bmad-output/implementation-artifacts/sprint-status.yaml (11 epics, 79 stories, in sync, validated)
linear: INF-11 (planning:sprint)
evidence: _bmad-output/planning-artifacts/readiness-2026-11-07/ (three independent read-only review lenses)
inputs:
  - _bmad-output/planning-artifacts/prds/prd-Armoury-2026-06-11/prd.md
  - _bmad-output/planning-artifacts/architecture.md
  - _bmad-output/planning-artifacts/ux-designs/ux-Armoury-2026-11-06/DESIGN.md
  - _bmad-output/planning-artifacts/ux-designs/ux-Armoury-2026-11-06/EXPERIENCE.md
  - _bmad-output/planning-artifacts/epics.md
  - _bmad-output/planning-artifacts/sprint-change-proposal-2026-11-07.md
---

# Implementation Readiness — Armoury

**Current verdict: CONCERNS, accepted by Daniel (2026-11-07, third rerun).** No blockers. Story 1.1 can start after its
planned Build re-plan.

## Third rerun — 2026-11-07: CONCERNS

Rerun after `sprint-change-proposal-2026-11-07-aliases.md`. Evidence:
`readiness-2026-11-07/rerun-3-blocker-9-closure.md` and `rerun-3-fresh-gate.md`.

- **Blocker 9 is closed.** `--by-cve`, the CVE-first issue key, stored aliases and matching on any
  alias are consistent in every artifact. An ID is known only when `grype db search --vuln <ID>`
  returns affected packages. Vendor VEX is display-only, also for the CI policy (Story 11.4).
- **Blockers 1–8 are still closed.** `sprint_plan.py --dry-run`: `in_sync: true` (11 epics, 79 stories).
- **One reviewer raised a blocker:** the open questions N1–N6 and N9 of the aliases change record had
  no story gate, so a changed issue key (N3) could drop recorded decisions. The record's own success
  criterion 8 required those gates. They were added (follow-up-2): Stories 2.4 (N1, N2, N3, new N10),
  5.3 (N3 test), 6.1 (N2), 6.2 (N5), 6.3 (N4), 5.2 (N4, N9), 5.6 and 5.7 (N6), and 6.5 (O2, O20 of
  `sprint-change-proposal-2026-11-07.md`). A mechanical check finds a gate AC for every open question.
- **Concerns that remain** (story-local; each is resolved by its story's Build planning or by an
  existing gate):
  - **Story 1.1:** the spec still describes the kind/Podman loop; the Skaffold `ci` profile is not in
    its acceptance criteria. The planned Build re-plan covers both.
  - **Epic 1:** the sign-in page is not designed; global states (session expired, control plane
    unreachable) are open (EXPERIENCE Open item 31); the Settings → Access users view has no data
    source; the icon-rail width is not a token.
  - **Epic 2:** the order inside Needs attention (Open item 21); Open-issues row clicks and "N more"
    rows (Open item 18); Data quality before a score exists (Open item 32); the "Connect a registry"
    one-liner; direct vs indirect package classification.
  - **Epics 5, 6, 9:** API contracts not yet named (issue list and detail, review decisions, exports,
    neighbours, the Reports → Audit trail listing and verification schedule); undrawn detail tabs
    (Open items 14, 15); concurrent reviews (Open item 30); regenerating an audit report (Open item 22);
    the Exposure query grammar; forward links from 6.3 and 6.4 to parts of 6.6.
  - **Epic 10:** Stories 10.2 and 10.3 do not include FR33 end-of-life data or the FR32 trusted root.
  - **Wording:** FR15 and the Story 5.7 statement still say vendor claims are "applied" (N8).


## Second rerun — 2026-11-07: FAIL (narrow)

Rerun after `sprint-change-proposal-2026-11-07-readiness.md`. Evidence:
`readiness-2026-11-07/rerun-1-blocker-closure.md` and `rerun-2-fresh-gate.md`.

- Blockers 1–8 below are **closed** in every artifact. `sprint_plan.py --dry-run`: `in_sync: true`.
- **New blocker 9 — vulnerability ID aliases.** Issues are keyed on one vulnerability ID
  (`architecture.md:257`; ARCH38). Story 2.4 stores the ID Grype reports (`epics.md:783`), and for
  language packages Grype reports GHSA IDs by default (`--by-cve` is optional). KEV and Exposure
  queries use CVE IDs (`epics.md:1254`, `:1258`, `:1738`). The Grype DB has the CVE record, so the
  unknown rule does not apply, and a CVE query answers "No software has it": the CVE-day false zero.
  Stories 2.4, 2.10, 4.3, 5.x, 6.2, 6.3. Epic 1 is not affected.
- **Concerns:** readiness-record questions Q1, Q2, Q4, Q5 are not gated by their stories; vendor VEX
  claims (Story 5.7) are outside the status rule; no lookup method is recorded for "the Grype DB has
  a record"; the Needs attention count vs the type filter and search; Story 5.8 keeps a stale
  [ASSUMPTION]; Story 1.1 CI "fast tier" and the Skaffold `ci` profile (for the Build re-plan).
- **Decision (Daniel):** fix blocker 9 (CVE first, keep all aliases), gate and record the cheap
  concerns, make vendor VEX claims display-only; then rerun.

## First rerun — 2026-11-07: FAIL

Rerun after the Correct Course
`sprint-change-proposal-2026-11-07.md` (Greenhouse UX spines, FR32, FR33).

Question: could a developer implement these epics without inventing decisions nothing records?

Traceability holds. Every FR1–FR33 and NFR1–NFR12 is cited in story acceptance criteria.
UX-DR1–UX-DR48 are covered (UX-DR8 and UX-DR14 are retired) and ARCH1–ARCH41 are cited.
The `sprint_plan.py generate --dry-run` reports `in_sync: true`: 11 epics, 79 stories, 0 orphans.
But the Correct Course left 8 gaps. In each gap, a developer must invent behaviour, or two
artifacts disagree. Full evidence with file:line quotes is in `readiness-2026-11-07/`
(lens A: traceability and structure; lens B: UX, stories and architecture; lens C: open
decisions and the next stories).

Story 1.1 is not blocked. Blockers 7 and 8 block Stories 1.8 and 1.9. The other blockers
block Epics 2, 5 and 6.

## Blockers — fix before the affected story starts

| # | Gap | Stories | Evidence | Owner skill |
|---|---|---|---|---|
| 1 | Story 5.4 saves a review from an issue that covers many places, but Story 5.3 limits a decision to one place and the scope control arrives in Story 5.8 (forward dependency). | 5.3, 5.4, 5.8 | `epics.md:1557`, `:1592`; `prd.md:95`; lens A 1, lens B 3 | bmad-correct-course |
| 2 | "Issue-wide status" is not defined, so the row chip, "Mixed · N of M", the review-status filter counts and VEX output cannot be computed. | 2.10, 5.2, 5.6, 5.8 | `architecture.md:257`; `epics.md:1701`; `DESIGN.md:710`; lens B 2 | bmad-architecture + bmad-correct-course |
| 3 | Grype also reports Negligible and Unknown severities. The issue groups are a closed list (licence, critical, high, medium, low) and have no place for them. | 2.10, 5.1, 5.2 | `architecture.md:257`; lens A 2, lens B 7 | bmad-ux + bmad-architecture |
| 4 | UX shows "Armoury has no data for <ID> yet" when the vulnerability data lacks the ID. The architecture and Story 6.2 check "any loaded feed", including the CVE List. A published CVE without package data then gets "No software has it": the CVE-day false zero. | 6.2, 6.3 | `EXPERIENCE.md:110`, `:180`, `:394`; `architecture.md:336`; `epics.md:1757`; lens B 1 | bmad-architecture |
| 5 | Nothing records the source of the "one plain sentence of what it means" for an issue. | 2.10, Home, UJ-4 | `epics.md:931`; `EXPERIENCE.md:62`; `prd.md:61`; lens A 3, lens B 8 | bmad-architecture + bmad-ux |
| 6 | "Review all N" has no mechanism. Issues has no Needs-attention filter, and Save and next walks the current filter (312 issues), not the 3 that need attention. | 5.4 | `epics.md:1595`; `EXPERIENCE.md:243`; lens B 4 | bmad-correct-course |
| 7 | The `?` shortcut map has nowhere to open. The only allowed modal is ⌘K, and Help is deferred. | 1.8 | `epics.md:190`, `:618`, `:633`; `EXPERIENCE.md:510`; lens C 1 | bmad-ux |
| 8 | The Story 1.9 lime lint forbids lime that DESIGN.md requires: the focus ring on the sidebar, on selection and in dark, the centre dot of the moved Exposure map, and the all-clear tints. | 1.9, 1.7 | `epics.md:641`; `DESIGN.md:26-27`, `:113`, `:466`, `:568`, `:594`; lens C 2 | bmad-ux + bmad-correct-course |

## Concerns — fix when the affected story is planned

Grouped. Each item is numbered in the lens files.

- **API contracts missing in architecture:** the Reports → Audit trail listing and the
  verification schedule ("verified 4 min ago"); issue IDs and deep links; issue list and
  detail, review-decision, export create and download, packs and neighbours endpoints
  (lens B 5, 6).
- **Open items built without a gate:** order inside Needs attention (Open item 21);
  "You are in good shape" rule; Open-issues row clicks and "N more" rows (Open item 18);
  undrawn detail tabs (Open items 14, 15); Data quality before a score exists (Open item 32);
  regenerating an audit report (Open item 22); concurrent reviews (Open item 30); session
  expiry and other global states (Open item 31); export placement on Issues and Software;
  the moved-map Table; the Exposure query grammar (lens A 7–13, 16; lens B 9–18, 23, 24;
  lens C 5, 14, 15, 17–19).
- **Change-record open questions not gated:** O2 and O20 (Story 6.5, 6.3, 9.5); O14, O16,
  O17 and O19 are only partly gated. Success criterion 9 of the change record is therefore
  not met (lens A 14, 20; lens C 7, 10–13, 20).
- **FR32 and FR33 follow-through:** Stories 10.2 and 10.3 leave out end-of-life data and the
  Sigstore trusted root; the Story 4.10 gate does not cover connected-mode refresh and the
  Rekor/TUF calls against the ARCH19 outbound rule; Story 4.10 does not restate the O13
  answer (lens A 15; lens C 9, 21).
- **Undecided rules:** GHSA/OSV-to-CVE alias mapping; direct vs indirect package
  classification; the "Connect a registry" one-liner (lens A 5, 6, 17; lens B 20).
- **Epic 1 details:** the sign-in page is not designed; the users/roles view in Settings →
  Access has no data source; the icon-rail width is not a token; the Story 1.1 spec still
  describes the kind/Podman loop and needs the planned Build re-plan (lens C 3, 4, 6, 8).
- **Other:** forward dependencies inside Epic 6 (6.3 and 6.4 need parts of 6.6); the Software
  detail "Audit report" button has no story; the "triage licence warnings = off" setting is
  not in the spines (lens A 4; lens B 21, 22).

## Next step

Daniel chose (2026-11-07): fix the 8 blockers with one Correct Course, then rerun this gate.
INF-11 stays In Progress until the gate passes.

---

# History

## Earlier runs (2026-11-05 and 2026-11-06)

**Current verdict: PASS (2026-11-06) — stale: assessed against ux-Armoury-2026-06-12, which ux-Armoury-2026-11-06 superseded; rerun after the 2026-11-07 Correct Course.** The findings below are the first run (CONCERNS). The
Correct Course change record `sprint-change-proposal-2026-11-05.md` resolved them; see its
gate-rerun sections for later findings and fixes.

Question: could a developer implement these epics without inventing decisions nothing records?

Verdict: **CONCERNS.** Traceability holds: every PRD FR/NFR is backed by story acceptance criteria;
all ACs are Given/When/Then; the parser dry run finds 10 epics / 68 stories, matching the Linear
manifest. The gaps below are story-local, not plan-wide. Fix them with `bmad-correct-course`
(cross-cutting) or the owning plan skill, then rerun `bmad-sprint-planning`.

### Fix before the affected story starts

| # | Gap | Stories | Evidence | Owner skill |
|---|-----|---------|----------|-------------|
| 1 | No story builds a container image (multi-stage Dockerfile with SPA + pinned tools, agent image, kind load) before Story 10.1. Story 1.2 therefore depends forward on 10.1. | 1.1/1.2, 2.3, 2.4, 2.12, 7.1 | `epics.md:296-345, 591, 805, 1994`; `architecture.md:340` | bmad-correct-course |
| 2 | Ledger entries store only a payload digest. Story 9.1 must reconstruct any past window "from recorded evidence only" (FR23). History written in Epics 2–8 cannot be backfilled. Keep full payloads or append-only history from day one, with a reconstruct test. | 2.1 → 9.1 | `epics.md:540, 1803` | bmad-correct-course |
| 3 | Feed-delta computation between two Grype DB versions is undecided (read SQLite directly? schema version? per-version cache dirs?). Core of NFR5. | 4.2 | `epics.md:1032`; `architecture.md:61, 427` | bmad-architecture (amendment) |
| 4 | Runtime keyless signing has no identity source: public Fulcio does not trust an in-cluster service-account issuer. Record the identity, or make operator key the runtime default and keep keyless for CI. | 9.4, 9.6, ARCH30 checkpoints | `architecture.md:174, 214, 430`; `epics.md:1875, 1938` | bmad-architecture (amendment) |
| 5 | No streaming / live-update pattern (SSE, cursor polling, async query resource). Changes the 6.2 API contract. | 2.9, 6.2, 6.3 | `epics.md:739, 1427, 1474`; `architecture.md:175, 301` | bmad-architecture (amendment) |
| 6 | Story 9.5 lets auditors generate packs by default; PRD makes auditor read-only and gives pack generation to analyst. Pack generation writes ledger entries. | 9.5 | `prd.md:48, 113`; `epics.md:1917`; `EXPERIENCE.md:142` | bmad-correct-course |
| 7 | `architecture.md` still lists VEX formats and retention as open; ARCH29, ARCH30 and PROC2 exist only in `epics.md`. Its data boundary omits the partition-dropping maintenance role. Story 5.6 cites a VEX mapping amendment that does not exist. | 2.1, 5.6, 9.6, 9.7 | `architecture.md:399, 462-464`; `epics.md:139-142, 1364` | bmad-architecture (update) |

### Concerns

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

### Minor
- Artifact types `oci_artifact` (2.8) and `filesystem` (7.2) are absent from the PRD glossary (`prd.md:157`) and the Artifacts list "image/package" (`epics.md:786`).
- No PRD basis recorded for 10.2 daily Armoury-published bundles with key rotation, and the 10.1 self-scan publication.
- NFR1 24-hour initial scan is projected, not measured (`epics.md:828`); 4.8 bounds only the Grype DB delta, not enrichment-only re-joins.
- FR14 "team consumption" has no explicit AC.
- Architecture Go leftovers: `control-plane/internal` (`architecture.md:397`), "packages" for Rust modules (`400, 404`).

### Next
1. Run `bmad-correct-course` with this file for items 1, 2, 6 and the epics-side concerns.
2. Run `bmad-architecture` (update) for items 3, 4, 5, 7 and the undecided technical details.
3. Rerun `bmad-sprint-planning`; on PASS (or accepted CONCERNS) it generates `sprint-status.yaml` and closes INF-11.
