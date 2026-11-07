---
status: approved
approved: 2026-11-07 — Daniel approved the whole proposal ("Yes, apply it"); O3, O5 and O13 answered with the recommended options
applied: 2026-11-07 — all section-4 edits applied to 10 files (P1–P27, U1–U20, A1–A57, E1–E86, S1–S189, C1–C17 by hand, Y1–Y3, R1–R3); answered O3/O13 wording updated in A18, P26, S179; Y4 dry-run and validate pass (11 epics, 79 stories)
linear: reconciled 2026-11-07 — 64 issues refreshed (21 retitled), Stories 4.9 (INF-112) and 4.10 (INF-113) created in Epic 4 with blocked-by links, 69 activity notes, INF-11 reopened to Todo; baseline recorded for 108 items; final plan --check leaves only the earlier Story 1.1 status difference (Linear In Progress, sprint-status backlog), not changed
date: 2026-11-07
workflow: bmad-correct-course (batch)
trigger: UX spines ux-Armoury-2026-11-06 (final 2026-11-06, updated 2026-11-07) — DESIGN.md, EXPERIENCE.md, .memlog.md, mockups/greenhouse-final.html
scope: major — the PRD gains two FRs (FR32, FR33), a second primary user and journey (UJ-4), and new wording for FR13, FR14, FR16–FR19, FR27 and FR30; the architecture gains four decisions (issue read model, stored exports, signature verification, end-of-life data); all 36 UX-DRs are edited (two of them retired) and 12 are added; 21 stories are retitled, 54 existing stories change, and 2 stories are added (4.9, 4.10). No code exists and no story contract is approved, so nothing is rolled back.
memlog_numbering: 'memlog N = line N of ux-designs/ux-Armoury-2026-11-06/.memlog.md (the memlog''s own convention, for example line 104 "Overrides memlog 93")'
decisions:
  - "D1 FR13 — Licences group first (hidden at 0), then Critical/High/Medium/Low; actively exploited (KEV) first within each group; EPSS orders within a group after exploited items and is never shown as a rating (memlog 39, 40, 42, 72, 76, 77)"
  - "D2 FR30 kept — surfaces: Software detail (Info value + quality meter), Reports audit report detail and the printed cover; not on Home (maybe the Home Details tab later); not in list rows (memlog 93, 98, 99, 100, 103, 104, 105, 107, 108)"
  - "D3 FR19 — CSV of the current view from Exposure, Issues and Software (JSON optional, PROC2); every export stored as evidence (file + ledger entry, audit-report retention) and listed in Reports → Exports; the posture summary is covered by the audit report; 'Audit report for this answer' = the Story 6.5 PDF answer report, relabelled, also listed in Reports → Exports (memlog 56, 94; architecture analysis recommendation A)"
  - "D4 Graph traversal kept inside Exposure (Story 6.6) — click/Enter re-centres the map (ego view), trail with Back, neighbours API stays (memlog 95, 97, 101, 102, 103)"
  - "D5 Tom Reid, Head of Engineering = Admin role; second primary user mapped to the CTO buyer; new journey UJ-4 'The Monday check' (memlog 7, 11, 96)"
  - "D6 Issue unit — one Issues row = one vulnerability (or licence) in one package version; a review applies to all places by default with per-software exceptions ('Mixed · N of M'); per-place findings kept plus a derived finding group (architecture recommendation A); metrics count places (memlog 87)"
  - "D7 'Why?' required for Not impacted, Mitigated and Risk accepted; optional for Fix planned; the VEX action statement comes from the fix text (memlog 50)"
  - "D8 Licence warnings — only licence violations count toward Needs attention and the Issues badge; warnings show in the Licences group with the word 'Warning'; unknown licences stay 'warning' by default (memlog 111, refining 76 and 80)"
  - "D9 Reports gains a fleet-wide 'Audit trail' group (ledger entries newest first, filters, chain verification, checkpoint and anchoring status); per-item trail tabs stay; Stories 5.5, 9.6 and 9.9 point at it (memlog 112)"
  - "D10 Software detail — 'Built' and 'Check again' are built; 'Signed' (verify signatures of customer artifacts) and end-of-life data for packages are added to v1 by PRD change (FR32, FR33) (memlog 113)"
  - "D11 All other UX changes follow the spines — light default + one dark theme, Greenhouse tokens, IBM Plex Sans + Mono, labelled sidebar, three-column master-detail, plain UI labels (domain/API terms stay), review panel, one density, Needs attention, Issues badge, unknown-vulnerability state, inline save errors, responsive rule, single-key shortcut switch, data-quality tokens (memlog 9, 13, 29, 30, 36, 46, 49, 53, 54, 60, 62, 64, 69, 78, 81, 82, 85, 86, 88, 108, 109)"
  - "Mode: batch (memlog 110)"
---

# Sprint Change Proposal — align planning with the Greenhouse UX spines

This proposal applies Daniel's decisions D1–D11 (frontmatter) to the PRD, the architecture,
`epics.md`, the Epic 1 context, the readiness record, `sprint-status.yaml` and, for D3 and D8–D10, the
UX spines themselves. It reopens none of them. Where a detail is not decided, it is listed in
section 6 (Open questions) and not decided here.

Edit notation used in section 4:

- Each edit has an ID, a location (heading and **current** line number), `OLD` and `NEW` text, and a
  one-line rationale ("Why").
- `OLD: ⟦…⟧` is an exact substring of the current file and is replaced by `NEW: ⟦…⟧`.
- `OLD (line starts): ⟦…⟧` means the whole line that starts with that text is replaced.
- `OLD (anchor, kept): ⟦…⟧` means the anchor stays and `NEW` is inserted directly after it.
- Every OLD quote was checked mechanically against the current files on 2026-11-07. The four impact
  analyses in `/tmp/cc/` were written against an earlier spine version; their open-item numbers are
  remapped here to the current EXPERIENCE.md numbering (Open items 1–35).
- Domain, data and API terms (artifact, finding, posture, blast radius, evidence pack, triage, KEV,
  EPSS, VEX, SBOM, `untriaged` / `not_affected` / …) stay wherever they name data, APIs, exports or
  requirements. Only UI-label uses change.

## 1. Issue summary

**Problem.** On 2026-11-06 the UX spines `ux-Armoury-2026-06-12` (three dark themes, 58px rail,
"locked glossary", one KEV-first ranked list, triage drawer) were replaced by
`ux-Armoury-2026-11-06` ("Greenhouse"). On 2026-11-07 the spines were updated again (data quality,
Exposure traversal, stored exports, Tom Reid as Admin). Every downstream planning artifact still
describes the old design, and several new UX decisions conflict with the PRD and the architecture.

**Type.** A deliberate product and design change, found before implementation. No story has started
Build; Story 1.1's contract is a draft.

**How it was found.** EXPERIENCE.md "Changes from ux-Armoury-2026-06-12" and Open item 26 ask for this
Correct Course; memlog 90 records "Downstream Correct Course needed for PRD, architecture and epics".
Four read-only impact analyses (PRD, architecture, epics requirements, epics stories) found 12 product
decisions; Daniel answered them (memlog 92–96, 104, 110–113 and D1–D11).

**Evidence.**

- PRD FR13 (`prd.md:80`): "KEV-listed findings first, then EPSS-weighted severity". The UX groups by
  severity with exploited items first in each group (EXPERIENCE "Severity groups"; memlog 39).
- PRD FR19 (`prd.md:89`): "a blast-radius result or posture summary can be exported (report/CSV)".
  The UX stores CSV exports from Exposure, Issues and Software in Reports (EXPERIENCE "Reports";
  memlog 94).
- PRD FR14 (`prd.md:81`) has no review scope; the UX defaults to "All 14 places" (memlog 87, 50).
- The PRD has one primary user; the UX has two, with equal weight, and Tom Reid is Admin (memlog 7,
  96).
- The UX shows "Signed" and an end-of-life line in Software detail (mock: "Signed Yes", "No package
  is past its end of life."). `architecture.md:502` says "Verifying inbound customer-artifact
  signatures is roadmap, not v1" (memlog 113).
- `epics.md:166` sources every UX-DR from the superseded spine; `architecture.md:160` names
  "Forge/High-Signal/Gunmetal" and `:270` "Inter"; the readiness verdict (PASS) was assessed against
  the old spines (`implementation-readiness.md:13-14`).

## 2. Impact analysis

### Epic impact

| Epic | Impact |
|---|---|
| 1 Shell | UX rewritten: two themes, Plex fonts, labelled sidebar, three-column master-detail, user menu, Help item, responsive rule, shortcut switch, new banned patterns. Stories 1.5–1.9 change; 1.5 and 1.6 retitled. Story 1.1's text is unchanged; one of its architecture sources changes (see Contract status). |
| 2 Inventory | Posture → Home, Artifacts → Software. Needs attention and the Issues badge arrive in 2.10. Software detail gains Built and Check again, with placeholders for Signed, end-of-life and data quality. 2.9, 2.10 and 2.11 retitled. |
| 3 Agent | Deployed / Not deployed grouping, Settings → Connections. 3.6 retitled. |
| 4 Feeds | Plain freshness strip, Settings → Sources. **Two new stories:** 4.9 (end-of-life data, FR33) and 4.10 (signature verification, FR32). 4.7 retitled. |
| 5 Review | Severity groups (D1), review panel, scope and Mixed (D6), optional "Why?" for Fix planned (D7), the fleet-wide Audit trail in Reports (D9). 5.1, 5.2, 5.4, 5.5, 5.6 and 5.8 retitled. |
| 6 Exposure | Blast radius + Graph explorer → Exposure with traversal (D4), the unknown-vulnerability state, stored exports and the answer report (D3). 6.3–6.6 retitled. |
| 7 Licences | Licences group, the word "Warning", only violations need attention (D8). 7.4 retitled. |
| 8 Signals / DQ | DQ surfaces are now designed (D2): Software detail and Reports, not Home. 8.2 and 8.4 retitled. |
| 9 Packs | Evidence → Reports, the audit report detail with a DQ row, signature status, the Audit trail group (D9). 9.5 retitled. The answer-scoped pack AC in 9.5 is replaced by the 6.5 answer report (D3). |
| 10 Release | One wording edit (10.4). |
| 11 CI scan | Lands in Software; the grouping of CI-only software stays open (Open item 28). |

No epic is added, removed or renumbered. Epic titles keep their domain wording (posture view, blast
radius, triage), so the Linear epic identities stay stable.

### Story impact

- **Retitled (21):** 1.5, 1.6, 2.9, 2.10, 2.11, 3.6, 4.7, 5.1, 5.2, 5.4, 5.5, 5.6, 5.8, 6.3, 6.4,
  6.5, 6.6, 7.4, 8.2, 8.4, 9.5 (table in 4.4).
- **New (2):** Story 4.9 "End-of-life data for packages" (FR33); Story 4.10 "Verify artifact
  signatures against trusted signers" (FR32).
- **Changed acceptance criteria:** 54 existing stories across Epics 1–11 (section 4.4).
- **Story in flight:** none. Story 1.1 has a draft spec (Revision 1, never approved).

### Artifact conflicts

| Artifact | Conflict | Edits |
|---|---|---|
| `prd.md` | FR13 ordering, FR14 scope and justification, FR16–FR19 surfaces, FR19 exports, FR27 Licences group, FR30 surfaces, a single primary user, no FR for signatures or end-of-life | P1–P23 |
| `addendum.md`, `.decision-log.md` | No record of the UX change or the new FRs | P24–P27 |
| `architecture.md` | Old themes and fonts, old routes, locked glossary, KEV-first ranking, no issue read model, no stored exports, signature verification on the roadmap, no end-of-life source | A1–A57 |
| `epics.md` front matter and requirements | FR mirrors, ARCH15/16/19/20/25/29/33/35, all UX-DR1–36 sourced from the old spine, FR coverage map, Epic List | E1–E86 |
| `epics.md` stories | UI labels and behaviour in 54 stories; two new stories | S1–S189 |
| `epic-1-context.md` | UX section fully stale | C1–C17 |
| `implementation-readiness.md` | PASS predates the new spines | R1–R3 |
| `sprint-status.yaml` | 21 retitled keys, 2 new stories | Y1–Y4 |
| UX spines | D8 and D9 change the approved spine; D3 label note; D10 settings and coverage | U1–U20 |

### Technical impact

- **Data model (D6):** findings stay per place. A derived finding group (UI "issue") is added as a
  read model. Needs attention and group counts are computed on the server. Metrics keep counting
  findings (places).
- **New persistence (D3):** stored exports (object store + record + ledger entry, evidence-pack
  retention). A new capability module is recommended (`exports`, open question O1).
- **New capabilities (D10):** `cosign verify` of customer artifacts read from connected registries,
  against admin-configured trust; an end-of-life dataset as one more enrichment source that rides the
  offline bundle. Both run only on the control plane (NFR12) and work air-gapped (NFR4).
- **Frontend:** theme maps, fonts, shell, routes (`/`, `/software`, `/issues`, `/exposure`,
  `/reports`, `/settings/<panel>`, Help), and brand-layer components in `lib/design/`.
- **No infrastructure or deployment change.** No rollback: no code exists.

### Contract status (Story 1.1)

`spec-1-1-monorepo-scaffold-with-an-aggregate-local-gate-and-ci.md`: Contract Approval **draft**,
Revision 1, digest pending, never approved. Its sources include
`architecture.md#Complete Project Directory Structure`, which this proposal edits (A34–A41: module
comments, `web/src/lib/theme/`, the new `lib/design/`, route names, the recommended `exports/` module),
and `epics.md#ARCH25` (E19, module list). Story 1.1's own text in `epics.md` (lines 310–359) is not
edited. Because the contract was never approved, **no contract revision is needed**: Build re-plans
from the updated sources at CHECKPOINT 1 (the spec is already `status: 'draft'`). See the Contract
Change Record in section 5.

## 3. Recommended approach

**Direct Adjustment, with a PRD scope addition.** Edit the planning artifacts in place, add two
stories at the end of Epic 4, and keep every epic and story number.

- **Rollback:** not applicable — nothing is built.
- **MVP review:** v1 scope grows by FR32 and FR33 (D10). Nothing else is removed or added. The
  answer-scoped evidence pack AC in Story 9.5 is replaced by the Story 6.5 answer report under D3
  (confirm in O3).
- **Why this path:** the UX was approved and validated (memlog 78, 89–91, 108), every product
  conflict now has Daniel's decision, and no implementation exists, so the cost of the change is
  documents only.
- **Effort:** about one working day to apply and check the planning edits; then a small UX update
  for D8/D9 and the architecture amendments for FR32/FR33 at story planning (the plan already uses
  this pattern for 4.5, 5.6 and 8.1). Implementation grows by two stories, and Stories 2.11, 5.5,
  6.5 and 6.6 get larger.
- **Risk:** medium. The largest risks are the stored-export and issue-group designs (new
  architecture) and the two new FRs, whose data source and trust model are still open (section 6).
  Each is gated by an AC that says "recorded as an amendment to `architecture.md` and approved before
  implementation", as the plan already does for undecided details.
- **Timeline:** the PRD has no deadlines. Story 1.1 is not affected in substance and can proceed once
  Agent Readiness passes. Epic 1–2 UI stories should not start Build before this proposal is applied.

**Placement of the new stories.** Both go at the end of Epic 4 (next free numbers 4.9 and 4.10).
Epic 4 already owns external data that rides the signed offline bundle (Stories 4.5, 4.6), creates
the `signing` module and adds the pinned cosign binary (4.5). End-of-life data is one more enrichment
source; signature verification reuses cosign and the trusted-key pattern without moving any tool
earlier. Software detail (Story 2.11) shows "Signed" and the end-of-life line as not checked yet until
then, the same way it already handles "Where it runs" before Epic 3. (Alternative: FR32 at the end of
Epic 2, which would move cosign from Story 4.5 into Epic 2 — O5.)

## 4. Detailed change proposals

### 4.1 PRD

<!-- file: _bmad-output/planning-artifacts/prds/prd-Armoury-2026-06-11/prd.md -->

#### prd.md

**P1 · front matter · L5**
OLD: ⟦updated: 2026-11-05⟧
NEW: ⟦updated: 2026-11-07⟧
Why: the PRD changes under this Correct Course.

**P2 · Vision · L18**
OLD: ⟦The primary surface is a web UI: the first fleet-wide posture view and the blast-radius query both live there.⟧
NEW: ⟦The primary surface is a web UI: the first fleet-wide posture view (Home in the UI) and the blast-radius query (Exposure in the UI) both live there. The UI uses plain labels over the technical terms in this document (see Glossary → UI labels).⟧
Why: the PRD names the UI here; the surfaces were renamed (D11).

**P3 · Users & Journeys intro · L22 (D5)**
OLD: ⟦The pitch is dual: the buyer hears evidence and regulatory defensibility; the user hears "stop hand-assembling audits."⟧
NEW: ⟦The pitch is dual: the buyer hears evidence and regulatory defensibility; the user hears "stop hand-assembling audits."

The CTO buyer is also a second primary user, with equal weight in the UI: a non-technical engineering leader (in the UX, Tom Reid, Head of Engineering) who needs to know in a minute whether the fleet is safe and what needs attention, without decoding security jargon. He signs in with the admin role (NFR6). One layout and the same words and numbers serve both primary users.⟧
Why: D5 — the UX names a second equal-weight user mapped to the CTO buyer, with the Admin role.

**P4 · UJ-1 step 5 · L32 (D1)**
OLD: ⟦findings ranked by KEV/EPSS priority, coverage gaps honestly displayed⟧
NEW: ⟦the findings that need attention today on top, the rest grouped by severity with KEV-listed (actively exploited) findings first in each group, coverage gaps honestly displayed⟧
Why: D1 replaces the single KEV-then-EPSS ranking.

**P5 · UJ-2 step 2 · L39**
OLD: ⟦She opens Armoury, types the CVE ID into the blast-radius query.⟧
NEW: ⟦She opens Armoury, types the CVE ID into the blast-radius query (Exposure in the UI, reachable from ⌘K).⟧
Why: UI label. "14 affected images, 9 running" stays: it is data, and the UI says "9 are deployed".

**P6 · UJ-2 step 3 · L40 (D3)**
OLD: ⟦3. She exports the result and posts it to the CTO — before he's read the news.⟧
NEW: ⟦3. She exports the result and posts it to the CTO — before he's read the news. The export is kept with the evidence, under her name (FR19).⟧
Why: D3 — every export is stored as evidence.

**P7 · UJ-2 step 4 · L41 (D6)**
OLD: ⟦She triages: two services don't invoke the vulnerable code path — she records *not affected* with justification; the rest get flagged for the owning teams⟧
NEW: ⟦She triages: she records *fix planned* once for every affected artifact, then, for the two services that don't invoke the vulnerable code path, records *not affected* (UI: "Not impacted") for those artifacts only, with justification; the rest get flagged for the owning teams⟧
Why: mirrors EXPERIENCE Flow 2 step 7 (scope "All 14 places", then "Only this software", giving "Mixed · 2 of 14"). The `[ASSUMPTION…]` tag stays.

**P8 · new UJ-4 after UJ-3 · after L50 (D5)**
OLD (anchor, kept): ⟦3. What was three weeks of spreadsheet archaeology is now a generated, signed document plus machine-readable attachments. The audit moment passes without a scramble.⟧
NEW: ⟦
### UJ-4 — The Monday check

Tom Reid is Head of Engineering: the CTO buyer's side of the house, not a security specialist. On Monday morning he has a minute.

1. He opens Armoury, signed in with the admin role. It lands on the fleet posture view (Home in the UI); the navigation shows that 3 issues need attention.
2. One line answers the question he came with — "You are in good shape. 3 things need attention today." — scoped to what was checked and when it was last checked.
3. The three issues that need a decision are listed in plain words: an actively exploited critical vulnerability, a license-policy violation and a critical vulnerability, each with where it is found. No acronyms to decode.
4. For the first one he reads one plain sentence of what it means, the fix and its review status, and sees how many pieces of software have it and how many are deployed, with a link to the full blast-radius answer.
5. Coverage, the 30-day trend of open issues, the latest signed evidence pack and feed freshness sit on the same screen. In under a minute he knows whether the fleet is safe, which three things need a decision and how fresh the numbers are. He can review them himself or leave them for Priya; nothing alarmed him or needed translating.⟧
Why: D5 — mirrors EXPERIENCE Flow 4 ("the Monday one-minute check").

**P9 · Features intro · L54**
OLD: ⟦FR29–FR30 were added at finalize and FR31 on 2026-11-05, so they sit out of numeric sequence.⟧
NEW: ⟦FR29–FR30 were added at finalize, FR31 on 2026-11-05 and FR32–FR33 on 2026-11-07, so they sit out of numeric sequence.⟧
Why: D10 adds FR32 and FR33 (the highest existing FR is FR31; IDs are never renumbered).

**P10 · new FR32 · "### 1. Fleet Inventory", after FR31 (L65) (D10)**
OLD (anchor, kept): ⟦The step always prints the verdict and a link to the artifact in Armoury. Central scanning (FR1, FR2) stays the default; no team has to change CI.⟧
NEW: ⟦
- **FR32** — Artifact signature verification: Armoury checks whether each container image and other OCI artifact in a connected registry is signed by a signer the organisation trusts — public keys or keyless signer identities that an admin configures — and records the result, the signer and the time of the check as evidence. Verification runs only on the control plane with the pinned toolchain (NFR12) and works air-gapped: key-based verification needs no network, and keyless verification uses trust material supplied offline (NFR4). The result is shown per artifact in artifact detail (FR18); a missing or failed signature is shown, never hidden (NFR8).⟧
Why: D10 — "Signed" in Software detail Info is added to v1 by PRD change. Open details: O6–O10.

**P11 · new FR33 · "### 3. Enrichment & Prioritization", after FR12 (L79) (D10)**
OLD (anchor, kept): ⟦- **FR12** — Source attribution: every enrichment datum is labeled with its source and retrieval time, so an auditor can see where a severity or exploited-status claim came from.⟧
NEW: ⟦- **FR33** — End-of-life data: for the packages in every stored SBOM, Armoury records whether each package version has reached its end of life, from an attributed end-of-life data source that is refreshed like the enrichment feeds (FR11, FR12), re-joined to stored SBOMs without rescans (FR7) and carried in the signed offline bundle (FR10). It is shown per artifact in artifact detail (FR18). A package the data does not cover is shown as unknown, never as supported.⟧
Why: D10 — the Packages "end-of-life lines" in Software detail are added to v1. Open details: O11–O15.

**P12 · FR13 · L80 (D1)**
OLD (line starts): ⟦- **FR13** — Risk-based prioritization:⟧
NEW: ⟦- **FR13** — Risk-based prioritization: posture views group findings so a small SecOps team sees the findings that matter, not ten thousand rows. The order is deterministic and explainable: license-policy findings first, in their own group (they carry no severity; the group is hidden when empty), then vulnerability findings by severity — Critical, High, Medium, Low. Within each group, KEV-listed (actively exploited) findings come first, then the rest are ordered by EPSS. The UI states the order in words above every grouped list. EPSS is never presented as a rating, score or column; its raw value appears only in a finding's technical details.⟧
Why: D1.

**P13 · FR14 · L81 (D6, D7)**
OLD: ⟦an analyst can record a handling decision on any finding — status (e.g. not affected, mitigated, accepted, fix planned), justification, author, timestamp. Decisions propagate everywhere the finding appears:⟧
NEW: ⟦an analyst can record a handling decision on any finding — status (not affected, mitigated, accepted, fix planned; a finding with no decision is untriaged), justification (required for not affected, mitigated and accepted; optional for fix planned, whose VEX action statement then comes from the planned fix), author, timestamp and scope. By default one decision covers every artifact affected by the same vulnerability or license violation in the same package version, including artifacts found later; a decision can instead cover one artifact, which then keeps its own status, and when affected artifacts differ, every view says so. Decisions propagate everywhere the finding appears:⟧
Why: D6 (scope, "Mixed") and D7 ("Why?" optional for Fix planned).

**P14 · FR16 · L86 (D1, D11)**
OLD: ⟦- **FR16** — Fleet posture view: the web UI's landing state — fleet-wide summary of artifacts, findings by priority, coverage gaps, and feed freshness.⟧
NEW: ⟦- **FR16** — Fleet posture view: the web UI's landing state (Home in the UI) — fleet-wide summary of artifacts, the findings that need attention today, open findings by group (FR13), coverage gaps, and feed freshness.⟧
Why: "by priority" referred to the old ranking; Home leads with Needs attention.

**P15 · FR17 (query) · L87**
OLD: ⟦- **FR17** — Blast-radius query: given a CVE ID or a package+version ("who uses log4j 2.x?"), Armoury answers⟧
NEW: ⟦- **FR17** — Blast-radius query (Exposure in the UI): given a CVE ID, a package+version ("who uses log4j 2.x?") or an image digest, Armoury answers⟧
Why: both UX spines accept fingerprint (digest) queries; Story 6.2 already implements them.

**P16 · FR17 (unknown answer) · L87**
OLD: ⟦— the answer is definitive in tone only when the data earns it.⟧
NEW: ⟦— the answer is definitive in tone only when the data earns it. A CVE ID that Armoury holds no vulnerability data for is answered as unknown, with the age of the vulnerability data, never as zero affected artifacts; a zero is always scoped to the artifacts actually scanned. The answer can be followed from any artifact, package or vulnerability in it to that node's own connections.⟧
Why: the unknown-vulnerability state (memlog 85) and D4 (traversal kept inside Exposure).

**P17 · FR18 · L88 (D10, D2)**
OLD: ⟦- **FR18** — Artifact detail: per artifact — SBOM contents, findings (vulnerability and license) with triage status, evaluation provenance, and running locations.⟧
NEW: ⟦- **FR18** — Artifact detail (Software detail in the UI): per artifact — SBOM contents, findings (vulnerability and license) with triage status, evaluation provenance, running locations, its signature status (FR32), the end-of-life status of its packages (FR33) and its data-quality score (FR30). An analyst can ask for the artifact to be checked again (SBOM and scan re-queued).⟧
Why: D10 (Signed, end-of-life, Check again) and D2 (artifact-level DQ in detail).

**P18 · FR19 · L89 (D3)**
OLD (line starts): ⟦- **FR19** — Shareable answers:⟧
NEW: ⟦- **FR19** — Shareable answers: the current view of a blast-radius answer, the findings list or the artifact list can be exported as CSV (JSON as an option), carrying the same caveats and provenance as the screen; a blast-radius answer can also be exported as a PDF report. Every export is stored as evidence — the file plus an evidence-trail entry (who, when, which view and query) — kept with the same retention as evidence packs (FR23) and listed with them. The fleet posture summary is shared as an evidence pack (FR21). This is the thing the SecOps engineer hands the CTO before being asked.⟧
Why: D3. The "Check again" role in P17 is open (O4).

**P19 · FR30 · L91 (D2)**
OLD: ⟦Surfaced at artifact and fleet level in posture views and evidence packs, so consumers know how much to trust an answer, not just what the answer is.⟧
NEW: ⟦Surfaced at artifact level in artifact detail and at fleet level in evidence packs (in their in-product detail and on their printed cover page), never as a grade in list rows, so consumers know how much to trust an answer, not just what the answer is.⟧
Why: D2 — not on Home, not in list rows; Software detail, Reports and the cover page.

**P20 · FR27 · L104 (D1, D8)**
OLD: ⟦violations surface as findings alongside CVEs in the same posture and artifact views, and are triagable with the same decision model (FR14).⟧
NEW: ⟦violations surface as findings alongside CVEs in the same posture, findings and artifact views (in the UI: a Licences group listed before the severity groups and hidden when empty, and a Licences type filter), and are triagable with the same decision model (FR14).⟧
Why: the Licences group (D1). The violation/warning rule for Needs attention (D8) is UI-level and lives in UX-DR38 and ARCH38.

**P21 · NFR6 · L114 (D5)**
OLD: ⟦Three roles: admin (configuration, connections), analyst (triage decisions, pack generation), read-only auditor `[ASSUMPTION: role set]`.⟧
NEW: ⟦Three roles: admin (configuration, connections), analyst (triage decisions, pack generation), read-only auditor `[ASSUMPTION: role set]`. Roles are ordered: an admin can also do everything an analyst can, and an analyst everything an auditor can.⟧
Why: D5 gives Tom Reid the Admin role and the UX shows him Review (EXPERIENCE Open item 10). The architecture already declares a minimum role per operation (`architecture.md:299`, "403 below the role, no 403 at or above it"), so this states existing behaviour; it closes Open item 10.

**P22 · Glossary · after L162 (D6)**
OLD (anchor, kept): ⟦- **Finding** — an evaluated condition against an artifact: a vulnerability match or a license-policy violation, carrying enrichment, triage status, and provenance.⟧
NEW: ⟦- **Issue** (UI term) — one vulnerability or license-policy finding in one package version, grouping the findings it produces across every affected artifact ("places"). UI counts are issues, not findings; a decision covers all of an issue's artifacts by default (FR14). Prometheus metrics count findings (one per place).⟧
Why: D6 — the UX unit is a grouping over per-artifact findings.

**P23 · Glossary · after L166 (D11)**
OLD (anchor, kept): ⟦- **Control plane / cluster agent** — the central install (web UI, graph, evidence store) / the per-cluster read-only inventory reporter.⟧
NEW: ⟦- **UI labels** — the web UI shows plain labels with the technical term small beside them; this PRD, the API, exports and machine-readable companions (SBOM, VEX) keep the technical terms. Mapping (UX spine ux-Armoury-2026-11-06, EXPERIENCE.md → Glossary): posture view → Home · artifact → Software / piece of software · finding → Issue · blast radius → Exposure · evidence trail → Audit trail / History · evidence packs and exports → Reports · evidence pack → Audit report · triage → Review · KEV-listed → Actively exploited · SBOM components → Packages · running / shipped, not running → Deployed / Not deployed · image digest → Fingerprint · scanned / unscanned → Checked / Not checked yet · data-quality score → Data quality · untriaged / not affected / fix planned / mitigated / accepted → Not reviewed yet / Not impacted / Fix planned / Mitigated / Risk accepted · justification → Why? · EPSS → not shown as a label (technical details only).⟧
Why: replaces the old UX "locked glossary" with one authoritative mapping; the PRD keeps its domain terms.

<!-- file: _bmad-output/planning-artifacts/prds/prd-Armoury-2026-06-11/addendum.md -->

#### addendum.md

**P24 · "## Data-quality score genesis (FR30)" · L22 (D2)**
OLD: ⟦Scoring inputs (SBOM depth, scan coverage, feed freshness, enrichment coverage, CVE record quality) and the scoring model itself are architecture/UX decisions.⟧
NEW: ⟦Scoring inputs (SBOM depth, scan coverage, feed freshness, enrichment coverage, CVE record quality) and the scoring model itself are architecture/UX decisions. Placement (Correct Course 2026-11-07, D2): the UX spine ux-Armoury-2026-11-06 shows the score in Software detail (a score and letter plus a five-part quality meter), in the audit report detail in Reports and on the printed cover page; not on Home (it may join the Home Details tab later) and never in list rows. Grade bands are a UX placeholder until the scoring model (Story 8.1) exists.⟧
Why: records where FR30 is surfaced.

**P25 · new section at the end of addendum.md (D11)**
OLD (anchor, kept): ⟦Deliberately undecided; open-core (OSS chassis, paid compliance packs) is the natural candidate. Details live in the product brief addendum (`_bmad-output/planning-artifacts/briefs/brief-Armoury-2026-06-11/addendum.md`). "The tool earns its place first."⟧
NEW: ⟦
## UX spine change (2026-11-06/07) (→ UX, architecture)

The UX spine ux-Armoury-2026-11-06 supersedes ux-Armoury-2026-06-12: a light default plus one calm dark theme, a labelled sidebar (Home · Software · Issues · Exposure · Reports · Settings · Help), three-column master-detail, plain-language UI labels over this PRD's domain terms (Glossary → UI labels), severity groups instead of one ranked list (FR13), a review panel with per-issue scope (FR14), stored exports (FR19) and the Monday check for the engineering leader (UJ-4). PRD terms stay the domain and API vocabulary. Open UX gaps against PRD requirements: vendor VEX claims with attribution (FR15) have no surface; the CI-scan landing in Software (FR31) is undecided; licence review copy is not drawn (FR27).⟧
Why: gives downstream readers the reason for the UI labels and the PRD-relevant UX gaps.

**P26 · new section at the end of addendum.md, after P25 (D10)**
OLD (anchor, kept): same anchor as P25 (insert after the P25 section).
NEW: ⟦
## Signature verification and end-of-life data (FR32, FR33) (→ architecture, UX)

Daniel's call (2026-11-07, Correct Course D10): the approved UX shows "Signed" and end-of-life lines in Software detail, so both enter v1 by PRD change rather than being dropped from the design. Left to architecture (amendments approved before Stories 4.9 and 4.10): the trust configuration for signatures (keys, keyless identities, per registry or fleet-wide), how the Sigstore trusted root reaches air-gapped instances, which signature formats and artifact types are checked; the end-of-life data source and its licence, what it covers, how packages are matched and its staleness threshold. Left to UX: the words for each signature state and the end-of-life lines. Not decided: whether signature or end-of-life status feeds issues, the CI policy or evidence packs. The "Build-time integration" roadmap item is unchanged: it captures Armoury-side build provenance; FR32 verifies signatures that already exist.⟧
Why: records the scope decision and what is still open.

<!-- file: _bmad-output/planning-artifacts/prds/prd-Armoury-2026-06-11/.decision-log.md -->

#### .decision-log.md

**P27 · end of file · after L52**
OLD (anchor, kept): ⟦  - 2026-11-05 — NFR11: optional Rekor anchoring of signed ledger checkpoints (off by default; external recommended, bundled available) (Daniel; Decision R10, Story 9.9).⟧
NEW: ⟦- 2026-11-07 — **Correct Course (UX spines ux-Armoury-2026-11-06)**, sprint-change-proposal-2026-11-07.md. Daniel's decisions D1–D11:
  - **FR13** amended to severity groups: licence findings first (hidden when empty), then Critical/High/Medium/Low; KEV-listed first within each group, then EPSS; EPSS never a rating (D1).
  - **FR30** kept; surfaced in artifact detail and in evidence packs (in-product detail and cover page); not on Home, not in list rows (D2).
  - **FR19** reworded: CSV (JSON optional) of the current view from blast radius, findings and artifacts, plus a PDF answer report; every export stored as evidence with pack retention; posture summary = the evidence pack (D3).
  - **FR17** accepts image digests, answers unknown CVE IDs as unknown (never zero), and its answers can be followed node by node (D4).
  - **Users:** the CTO buyer is also a second primary user (Tom Reid, Head of Engineering, admin role); new **UJ-4** "The Monday check"; NFR6 states that roles are ordered (D5).
  - **FR14:** decision scope (all affected artifacts by default, or one), "untriaged" named, justification optional only for fix planned (D6, D7). Glossary gains **Issue** and **UI labels** (D6, D11).
  - **FR32** (artifact signature verification) and **FR33** (end-of-life data) added to v1 (D10). FR18 names them, the data-quality score and "check again".⟧
Why: keeps the PRD decision trail complete.

### 4.2 Architecture

<!-- file: _bmad-output/planning-artifacts/architecture.md -->

Backend decisions (datastore, ledger, agents, signing of packs, River, tools) are unchanged. The edits
cover the frontend, the API shapes behind Issues and Exposure, ordering, stored exports, the two new
FRs, and stale UI wording. Module, table and enum names (`posture`, `blastradius`, `ranking`,
`triage`, `findings`, `triage_decisions`, `untriaged`, AGE labels, metric labels) are kept on purpose.

**A1 · front matter · L7**
OLD: ⟦amendedAt: '2026-11-05'  # Correct Course: sprint-change-proposal-2026-11-05.md (readiness fixes, FR31/NFR12)⟧
NEW: ⟦amendedAt: '2026-11-07'  # Correct Course: sprint-change-proposal-2026-11-07.md (UX spines ux-Armoury-2026-11-06; FR32/FR33); earlier: sprint-change-proposal-2026-11-05.md (readiness fixes, FR31/NFR12)⟧
Why: records the amendment in the single YAML key.

**A2 · front matter `inputDocuments` · L12–13**
OLD: ⟦  - _bmad-output/planning-artifacts/ux-designs/ux-Armoury-2026-06-12/DESIGN.md
  - _bmad-output/planning-artifacts/ux-designs/ux-Armoury-2026-06-12/EXPERIENCE.md⟧
NEW: ⟦  - _bmad-output/planning-artifacts/ux-designs/ux-Armoury-2026-11-06/DESIGN.md
  - _bmad-output/planning-artifacts/ux-designs/ux-Armoury-2026-11-06/EXPERIENCE.md⟧
Why: the old spines are superseded.

**A3 · Requirements Overview · L31**
OLD: ⟦**Functional Requirements (31 across 6 groups):**⟧
NEW: ⟦**Functional Requirements (33 across 6 groups):**⟧
Why: FR32 and FR33 (D10).

**A4 · Requirements Overview, Fleet Inventory · L33**
OLD: ⟦- **Fleet Inventory (FR1–FR5, FR29, FR31):**⟧
NEW: ⟦- **Fleet Inventory (FR1–FR5, FR29, FR31, FR32):**⟧
Why: FR32 belongs to the Fleet Inventory group.

**A5 · Requirements Overview, Fleet Inventory · L33**
OLD: ⟦joined into one inventory with shipped-vs-running reconciliation (FR4) and honest coverage gaps (FR5).⟧
NEW: ⟦joined into one inventory with shipped-vs-running reconciliation (FR4), honest coverage gaps (FR5) and the signature status of registry artifacts, verified against trusted signers (FR32).⟧
Why: D10.

**A6 · Requirements Overview, Enrichment · L35 (D1, D10)**
OLD: ⟦- **Enrichment & Prioritization (FR11–FR15):** Multi-source post-NVD enrichment (KEV, EPSS, CNA, OSV) with per-datum source attribution (FR11–FR12); deterministic, explainable ranking (FR13);⟧
NEW: ⟦- **Enrichment & Prioritization (FR11–FR15, FR33):** Multi-source post-NVD enrichment (KEV, EPSS, CNA, OSV) with per-datum source attribution (FR11–FR12); end-of-life data for packages, attributed the same way (FR33); deterministic, explainable ordering in severity groups (FR13);⟧
Why: FR33 and the D1 ordering.

**A7 · Requirements Overview, Blast-Radius & Posture · L36 (D3)**
OLD: ⟦exportable answers (FR19)⟧
NEW: ⟦exportable answers, stored as evidence (FR19)⟧
Why: D3.

**A8 · Cross-Cutting Concerns · L76**
OLD: ⟦- **Observability** — Prometheus pull-only; _no_ in-product notifications anywhere.⟧
NEW: ⟦- **Observability** — Prometheus pull-only; _no_ in-product notifications anywhere. (The Issues nav badge shows the Needs-attention count — what needs a decision — and is not a new-findings notification; badges for new findings stay banned.)⟧
Why: the UX adds a nav badge and narrows the ban to new-finding counts.

**A9 · Cross-Cutting Concerns · L77 (D1)**
OLD: ⟦ranking (FR13) and data-quality (FR30) must be reproducible and inspectable.⟧
NEW: ⟦issue ordering (FR13: severity groups, actively exploited first within each) and data-quality (FR30) must be reproducible and inspectable.⟧
Why: D1.

**A10 · Starter Options · L108**
OLD: ⟦file-based routing for the 7 surfaces.⟧
NEW: ⟦file-based routing for the seven sidebar surfaces (Home, Software, Issues, Exposure, Reports, Settings, Help).⟧
Why: the surface set and names changed (the count is still seven).

**A11 · Starter Options · L109 (D4)**
OLD: ⟦**Graph library — Svelte Flow (`@xyflow/svelte`, stable v1.6.0).** Stable 1.x release⟧
NEW: ⟦**Graph library — Svelte Flow (`@xyflow/svelte`, stable v1.6.0)** for the Exposure map (hairline four-tier graph with circular nodes; Blast radius and Graph explorer merged into Exposure, which keeps moving the map to any node). Stable 1.x release⟧
Why: graph surfaces merged and restyled; traversal kept (D4).

**A12 · Selected Stack & Scaffold · L129**
OLD: ⟦# Svelte Flow (stable) for blast-radius + graph explorer⟧
NEW: ⟦# Svelte Flow (stable) for the Exposure map (Graph view; the Table view is the equivalent)⟧
Why: old UI surface names.

**A13 · Architectural decisions provided by this scaffold · L160 (D11)**
OLD: ⟦design tokens map straight onto the DESIGN.md theme system (Forge/High-Signal/Gunmetal).⟧
NEW: ⟦design tokens map onto shadcn CSS variables per DESIGN.md "shadcn mapping" (ux-Armoury-2026-11-06): two themes over the same semantic roles — Light (default, unsuffixed tokens) and Dark (`-dark` tokens) — plus `--paper`, `--dq`, `--dq-muted` and `--dq-wash`; `print-*` tokens feed the Typst templates only. Fonts: IBM Plex Sans and IBM Plex Mono, self-hosted (SIL OFL 1.1).⟧
Why: three dark themes dropped; light default plus one dark; Plex replaces Inter; data-quality roles added.

**A14 · Downstream doc fix note · L167**
OLD: ⟦**Downstream doc fix (done 2026-11-01):** DESIGN.md / EXPERIENCE.md now name Svelte (SvelteKit + shadcn-svelte); visual identity and tokens unaffected.⟧
NEW: ⟦**Downstream doc fix (done 2026-11-01):** DESIGN.md / EXPERIENCE.md now name Svelte (SvelteKit + shadcn-svelte); visual identity and tokens unaffected. **Superseded 2026-11-06:** the UX spines are now `ux-Armoury-2026-11-06` (Greenhouse: light default + one dark theme, IBM Plex, labelled sidebar, three-column master-detail); still SvelteKit + shadcn-svelte + Tailwind.⟧
Why: the historical note otherwise implies the old visual identity is current.

**A15 · Decision Priority Analysis, Auth · L182**
OLD: ⟦User preferences (theme) live in `user_preferences`⟧
NEW: ⟦User preferences (theme `light` | `dark`, default `light` when none is stored; single-key keyboard shortcuts on or off, default on — WCAG 2.1.4) live in `user_preferences`⟧
Why: theme values changed; Settings → Personal adds the shortcut switch.

**A16 · Frontend server-state · L197**
OLD: ⟦**`@tanstack/svelte-query`** for posture/blast-radius caching; Svelte 5 runes for local state.⟧
NEW: ⟦**`@tanstack/svelte-query`** for server-state caching (the Home summary and Needs-attention count from the posture API, Exposure answers from the blast-radius API, the Issues, Software and Reports lists); Svelte 5 runes for local state.⟧
Why: surface names changed; API terms kept.

**A17 · Observability · L202 (D6)**
OLD: ⟦Labels stay bounded; never per artifact or per CVE.⟧
NEW: ⟦Labels stay bounded; never per artifact or per CVE. These metrics count findings (one per place); the UI counts issues (finding groups), so a metric total can be higher than the number on screen.⟧
Why: D6 — metrics count places.

**A18 · new decisions after Vendor VEX matching · after L203 (D3, D10)**
OLD (anchor, kept): ⟦- **Vendor VEX matching (FR15, amended 2026-11-05):** exact identifiers only, in this order: image digest; purl with version; purl without version. No fuzzy name or CPE matching. A statement with no fleet match is stored and shown as "no fleet match". Each applied match records the rule that matched.⟧
NEW: ⟦- **Stored exports (FR19, decided 2026-11-07, Correct Course D3).** Export (a CSV of the current view; JSON as an option, PROC2) from Exposure, Issues and Software, and "Audit report for this answer" (the Story 6.5 PDF answer report), are stored as evidence. The file goes to the object store through `blob`, content-addressed. An `exports` row records who, when, the view (`exposure` | `issues` | `software`), the query or filters, the format, the row count, the caveats and the file digest; the same transaction appends a ledger entry with that digest. Stored exports are insert-only (no update or delete endpoint, no UPDATE or DELETE grant) and follow the evidence-pack retention (ARCH30: default and minimum 24 months, archive path, never deleted by hand). `GET /api/v1/exports` lists them newest first for Reports → Exports. Auditors can export (a read action); their exports are stored and attributed like anyone else's. Owner: a new `exports` capability (recommended — O1). Not decided: whether stored export files are also cosign-signed (O2).
- **Artifact signature verification (FR32, added 2026-11-07, Correct Course D10).** Runs only in the control plane (NFR12). After discovery, and again when the trust policy changes, `inventory` runs the pinned cosign CLI through `tools` (`cosign verify` with a configured public key, or with a keyless identity — certificate OIDC issuer and subject) against signatures read from the same connected registry with that connection's read-only credentials (per-invocation env, never argv). Trust is admin-configured (Settings → Policy and Helm values; PROC2 default: none, so nothing is verified and the UI says so) and each trust-policy version is appended to the ledger. Each result (state, signer, trust-policy version, cosign version, check time) is appended to the ledger and returned by `GET /api/v1/artifacts/{id}`. Air-gapped: key-based verification makes no network call; keyless verification uses an offline Sigstore trusted root and the signature's own bundle, with no call to public Fulcio, Rekor or the Sigstore TUF repository. Registry reads are admin-configured endpoints owned by `inventory`. Open before Story 4.10 (an amendment approved by the user): the result states and their names, per-registry or fleet-wide trust, the signature formats read (cosign signatures, OCI referrers and attestations), how the trusted root is delivered and refreshed (offline bundle, admin-supplied file, or an online refresh in connected mode as a built-in public endpoint owned by `signing`), and whether artifacts from package feeds are in scope (O6–O10).
- **End-of-life data (FR33, added 2026-11-07, Correct Course D10).** One more enrichment source, owned by `enrichment`: an attributed end-of-life dataset, fetched on the enrichment schedule in connected mode (a built-in public endpoint with an offline-bundle equivalent, off in air-gapped mode), validated, stored as a versioned snapshot (source, version or date, retrieved_at) and appended to the ledger (ARCH21). A new snapshot is re-joined to the packages of stored SBOMs through the package index without re-matching SBOMs, like the KEV/EPSS re-join. Each package gets an end-of-life date and a status (past end of life, supported or unknown; never "supported" by default), with source and retrieval time, served per package by `GET /api/v1/artifacts/{id}`; the source's age is in `provenance.sources`. Air-gapped: the dataset is one more component of the signed offline bundle (Story 4.5 format, Story 4.6 import). Open before Story 4.9 (an amendment approved by the user): the source (neither the PRD nor this document names one) and its licence, its coverage (package ecosystems; runtimes and OS releases), the exact matching rule and the staleness threshold (O11–O15). In this proposal end-of-life status creates no finding and does not count toward Needs attention; O13 asks whether it should.⟧
Why: D3 needs storage and retention the architecture did not have; D10 moves signature verification from the roadmap into v1 and adds an end-of-life source.

**A19 · Long operations · L250**
OLD: ⟦about 10 s for the Posture summary while backlog exists⟧
NEW: ⟦about 10 s for the Home summary (posture API, including the Needs-attention count behind the Issues badge) while backlog exists⟧
Why: Posture → Home; the badge needs the same refresh.

**A20 · Long operations · after L251**
OLD (anchor, kept): ⟦- `ponytail:` partial blast-radius results are held in control-plane memory for about 10 minutes (single instance, NFR10); a restart loses them and the user runs the query again. Upgrade path: store them in PostgreSQL if more than one control plane runs. SSE stays a later option if polling delay is measured as too slow.⟧
NEW: ⟦- An Exposure query still running after 2 s renders its partial results with a scope line (EXPERIENCE → Long-running operations); the ~1 s poll above serves it.⟧
Why: a new UX timing rule, already met by the polling design.

**A21 · new paragraph before "### Frontend Architecture" · L253 (D1, D6, D7, D8)**
OLD: ⟦### Frontend Architecture⟧
NEW: ⟦**Issues and review (amended 2026-11-07, Correct Course D1, D6–D8).** A finding stays one match on one artifact (a "place"). The Issues surface lists **finding groups** (UI label "issue"): a read model over findings, keyed by vulnerability ID and package purl@version, or by licence, finding kind (`license_violation` | `license_warning`) and package purl@version. Per group the list response gives `group` (`licence` | `critical` | `high` | `medium` | `low`), `kev`, the place count, the issue-wide `triage_status`, `mixed` with the number of places that differ from the issue-wide status, and `needs_attention`; the page carries counts per group and per triage status (a group matches a status filter when any place has that status; counts are groups, not places) and the total for the pager. Ordering is server-side and deterministic (`ranking`, FR13). **Needs attention:** a vulnerability group with any place `untriaged` AND (`kev` OR severity critical); a `license_violation` group with any place `untriaged`; `license_warning` groups never (D8). It is computed only on the server, so the Issues badge, Home and the Issues summary show the same number. **Decisions** carry scope `all_places` (default: this vulnerability or licence in this package version on every artifact, including artifacts found later) or `artifact`; a per-artifact decision overrides `all_places`, and a later `all_places` decision leaves per-artifact decisions in place (Story 5.8). `justification` is required for `not_affected`, `mitigated` and `accepted` and optional for `fix_planned` (D7). `mixed` is derived, never stored.

### Frontend Architecture⟧
Why: the issue unit, scope, Mixed, Needs attention and the "Why?" rule need an API contract; none existed.

**A22 · Frontend Architecture · L255 (D4, D11)**
OLD: ⟦SvelteKit static SPA · shadcn-svelte · Tailwind v4 · Svelte Flow (graph) · TanStack Svelte Query (server state) · command palette (shadcn `Command`). Every graph view has a table equivalent (accessibility + graph-lib de-risk).⟧
NEW: ⟦SvelteKit static SPA · shadcn-svelte · Tailwind v4 · Svelte Flow (Exposure map) · TanStack Svelte Query (server state) · command palette (shadcn `Command` + `Dialog`). Every graph view has a table equivalent (accessibility + graph-lib de-risk). UI source of truth: `ux-designs/ux-Armoury-2026-11-06/` DESIGN.md (tokens, components) and EXPERIENCE.md (behaviour).

- **Shell:** black labelled sidebar (shadcn `Sidebar`: Home · Software · Issues · Exposure · Reports, then Settings · Help; the ⌘K search field; the user menu) and three-column master-detail on every surface (sidebar · grouped list column · tabbed detail column); Exposure has a full-width header over the list and the map. Below 1280px the sidebar becomes an icon rail; below 1024px list and detail stack with a Back link, at the same URL. One density only.
- **Themes:** Light (default) and Dark, two value maps over the same semantic roles, applied as shadcn CSS variables (plus `--paper` and the `--dq*` roles) by a root class; switching is instant and persisted in `user_preferences`. No other themes. The printed report never follows the theme.
- **Fonts:** IBM Plex Sans (variable, plus Bold Italic for the wordmark) and IBM Plex Mono, self-hosted in the SPA bundle (no network at view time, NFR4); the same files feed Typst.
- **Review:** the review panel lives in the Issues detail column (Review tab); no slide-over drawer. The ⌘K dialog is the only modal. Status changes happen only in the panel.
- **Exposure traversal (D4):** click or `Enter` on any node moves the map to it (ego view) using the `graph` neighbours API; the trail, question, answer, Export, "Audit report for this answer" and the URL (`&from=` the previous step) follow the centre; Back, `Backspace` or the browser Back returns a step; ⌘K starts a new trail.
- **Keyboard:** single-key shortcuts (`J`, `K`, `/`, `x`, `?`, `g` + letter, `Backspace` on the map) work only outside text fields and can be turned off per user; `⌘K` and `⌘↵` always work.
- **Counts are server-derived:** Needs attention, group and status counts, and "Mixed · N of M" come from the API, never from summing a page in the SPA.
- **Accessibility:** WCAG 2.2 AA in both themes; reflow at 400% zoom through the responsive rule above; all strings externalised (British English); UI labels mapped from API enums in one place.⟧
Why: the frontend contract must name the new shell, themes, fonts, review placement, traversal and responsive rule.

**A23 · Substrate Integration, cosign · L269 (D10)**
OLD: ⟦- **cosign:** `cosign sign-blob --bundle` in the configured signing mode (`key` by default; see Signing). Verification may use the `sigstore` crate (verification-focused, pre-1.0) or the cosign CLI.⟧
NEW: ⟦- **cosign:** `cosign sign-blob --bundle` in the configured signing mode (`key` by default; see Signing). Verification may use the `sigstore` crate (verification-focused, pre-1.0) or the cosign CLI. `cosign verify` also checks customer artifact signatures against admin-configured trust (FR32, Story 4.10), with registry credentials in per-invocation env.⟧
Why: D10.

**A24 · Substrate Integration, Typst · L270 (D3, D11)**
OLD: ⟦for the blast-radius/posture report (Story 6.5) and evidence packs (Story 9.3). Templates live in the module that owns the report; the bundled Inter and IBM Plex Mono fonts are passed to Typst.⟧
NEW: ⟦for the Exposure answer report (Story 6.5; shown in the UI as "Audit report for this answer" and stored with the exports) and evidence packs (audit reports, Story 9.3). Templates live in the module that owns the report; the bundled IBM Plex Sans and IBM Plex Mono fonts (the files the SPA self-hosts) are passed to Typst, and templates use DESIGN.md's `print-*` palette, never the app theme.⟧
Why: Inter dropped; surfaces renamed; D3 relabels the answer report.

**A25 · Decision Impact Analysis · L278 (D4)**
OLD: ⟦AGE graph schema underpins blast-radius _and_ graph explorer;⟧
NEW: ⟦AGE graph schema underpins blast-radius queries and moving the Exposure map (which absorbed the former Graph explorer);⟧
Why: Graph explorer is a retired UI label; traversal is kept.

**A26 · Critical Conflict Points · L286**
OLD: ⟦the locked domain vocabulary, and honest-degradation metadata.⟧
NEW: ⟦the locked domain vocabulary (code, API, exports) versus the plain UI labels, and honest-degradation metadata.⟧
Why: the UX replaced the "locked glossary" with plain labels.

**A27 · Format Patterns, Lists · L311**
OLD: ⟦**Lists** use `{ "items": [...], "page": {...} }` with cursor pagination (no offset at NFR3 scale).⟧
NEW: ⟦**Lists** use `{ "items": [...], "page": {...} }` with cursor pagination (no offset at NFR3 scale). `page` carries `total` (and group counts for grouped lists), so the SPA shows "1–25 of 312 · page 1 of 13" with previous and next only; 25 per page; no jump-to-page, no infinite scroll.⟧
Why: the UX pager needs totals; still cursor-compatible.

**A28 · Honest-degradation metadata · L321**
OLD: ⟦This is the API-side contract behind NFR8 / the honest-provenance UX. No answer ships without it.⟧
NEW: ⟦This is the API-side contract behind NFR8 / the honest-provenance UX. No answer ships without it. A blast-radius query for a CVE ID that no loaded feed contains returns the Story 6.2 error (a `code` distinct from "not a valid identifier") with the active feed versions and their age in `details`; the SPA shows it as the unknown-vulnerability state ("Armoury has no data for <ID> yet"), never as a zero. Only a known vulnerability gets the coverage-scoped zero. "Check again" on that state re-runs the query against the latest data; it is not a rescan.⟧
Why: the unknown-vulnerability state (memlog 85) must be distinguishable; Story 6.2 already returns a distinct 422.

**A29 · Domain vocabulary · L325 (D11)**
OLD (line starts): ⟦**Domain vocabulary is locked, not free text.**⟧
NEW: ⟦**Domain vocabulary is locked in code, API and exports, not free text.** The domain terms (`Artifact`, `Fleet`, `Finding`, `Posture`, `Evidence`, `Evidence pack`, `Control plane`, `Cluster agent`) and the triage status set (`not_affected` / `mitigated` / `accepted` / `fix_planned`, plus derived `untriaged`) are **typed enums** in Rust (`serde` `snake_case`), the OpenAPI schema, and TS — never stringly-typed, never synonymized. VEX and machine-readable exports keep these technical terms. **UI copy uses the plain labels** of EXPERIENCE.md's glossary (ux-Armoury-2026-11-06) — Home, Software, Issues, Exposure, Reports, Audit report; Not reviewed yet / Not impacted / Fix planned / Mitigated / Risk accepted; Actively exploited (KEV); Deployed / Not deployed; Packages (SBOM) — with the technical term small beside the label. Labels map from the enums in one place in the externalised strings; enums are never renamed to match a label. `mixed` is a derived display state, never stored.⟧
Why: the old "locked glossary" is retired in the UI; enums stay.

**A30 · Structure Patterns, Svelte SPA · L352**
OLD: ⟦(`routes/posture/`, `routes/blast-radius/`); only genuinely shared primitives sit in `lib/components/ui` (shadcn-svelte).⟧
NEW: ⟦(`routes/issues/`, `routes/exposure/`); only genuinely shared primitives sit in `lib/components/ui` (shadcn-svelte), and the Armoury brand-layer components every surface uses (shell, list row, severity and exploited markers, status chip, coverage-gap row, freshness strip, inline error, code block, data-quality value and meter) earn the named home `lib/design/`.⟧
Why: routes renamed; the shared master-detail components pass the rule of three across five surfaces.

**A31 · Process Patterns · L360**
OLD: ⟦- **SPA state/errors:** TanStack Query owns server-state; skeletons mirror layout; render the typed error envelope's `message`; never a bare spinner.⟧
NEW: ⟦- **SPA state/errors:** TanStack Query owns server-state; skeletons mirror layout; render the typed error envelope's `message`; never a bare spinner. A failed save or start (review, export, generate audit report, Check again, settings) shows an inline error in the panel where it happened, with Try again; nothing advances and entered values stay; no toasts.⟧
Why: the inline-error rule (memlog 86).

**A32 · Enforcement · L368**
OLD: ⟦- Use the **locked enums/glossary**; no invented status or entity synonyms.⟧
NEW: ⟦- Use the **locked enums** in code, API and exports, and EXPERIENCE.md's plain labels in UI copy; no invented status or entity synonyms in either.⟧
Why: the locked glossary is replaced in the UI.

**A33 · Anti-patterns · L375**
OLD: ⟦single-implementation interfaces; `Manager`/`Factory`/`Provider` layers.⟧
NEW: ⟦single-implementation interfaces; `Manager`/`Factory`/`Provider` layers; enum values shown as UI labels or UI labels used as enum values; counts summed in the SPA from a page of rows.⟧
Why: guards the label/enum split and server-derived counts.

**A34 · Directory structure, `inventory` · L409 (D10)**
OLD: ⟦│   │   ├── inventory/            # FR1–FR5, FR29  registry/feed connect, Syft SBOM, reconcile, coverage⟧
NEW: ⟦│   │   ├── inventory/            # FR1–FR5, FR29, FR32  registry/feed connect, Syft SBOM, reconcile, coverage, signature checks⟧
Why: FR32.

**A35 · Directory structure, `enrichment` · L414 (D10)**
OLD: ⟦│   │   ├── enrichment/           # FR11, FR12     KEV/EPSS/OSV/CNA aggregation + attribution⟧
NEW: ⟦│   │   ├── enrichment/           # FR11, FR12, FR33  KEV/EPSS/OSV/CNA + end-of-life aggregation + attribution⟧
Why: FR33.

**A36 · Directory structure, `ranking` · L415 (D1)**
OLD: ⟦│   │   ├── ranking/              # FR13           deterministic KEV-first/EPSS ranking⟧
NEW: ⟦│   │   ├── ranking/              # FR13           deterministic grouping + order: Licences, Critical…Low; KEV first in a group, then raw EPSS, then a stable tie-break⟧
Why: D1.

**A37 · Directory structure, `posture` · L418 (D2, D6)**
OLD: ⟦│   │   ├── posture/              # FR16, FR30     fleet posture + data-quality score⟧
NEW: ⟦│   │   ├── posture/              # FR16, FR30     fleet posture (Home summary, Needs attention, finding groups) + data-quality score⟧
Why: maps the module to Home and the issue read model.

**A38 · Directory structure, new `exports` · after L419 (D3)**
OLD (anchor, kept): ⟦│   │   ├── blastradius/          # FR17, FR19     AGE Cypher traversal + provenance assembly⟧
NEW: ⟦│   │   ├── exports/              # FR19           stored exports: file → blob, record + ledger entry, Reports → Exports list (recommended, O1)⟧
Why: D3 stored exports need an owner; depends on O1.

**A39 · Directory structure, `graph` · L420 (D4)**
OLD: ⟦│   │   ├── graph/                # FR17, FR18     graph-explorer queries⟧
NEW: ⟦│   │   ├── graph/                # FR17, FR18     neighbour queries for moving the Exposure map (ego view, roll-ups)⟧
Why: D4 — traversal kept inside Exposure; the neighbours API stays.

**A40 · Directory structure, web `lib` · L449 (D11)**
OLD: ⟦│       │   └── theme/            # Forge / High-Signal / Gunmetal token maps⟧
NEW: ⟦│       │   ├── design/           # Armoury brand-layer components shared by every surface (DESIGN.md Components)
│       │   └── theme/            # Light (default) / Dark token maps → shadcn CSS variables (+ --paper, --dq*); self-hosted IBM Plex Sans + Mono⟧
Why: three dark themes dropped; fonts self-hosted; shared brand components need a home (A30).

**A41 · Directory structure, web routes · L451 (D11)**
OLD: ⟦│           ├── posture/          # + blast-radius/ graph/ artifacts/ findings/ evidence/ settings/⟧
NEW: ⟦│           ├── +page.svelte      # Home (/) + software/ issues/ exposure/ reports/ settings/[panel]/ help/ (Help content open, EXPERIENCE Open item 24)⟧
Why: new surfaces and URLs (EXPERIENCE → Information Architecture).

**A42 · Architectural Boundaries, scanning · L466 (D10)**
OLD: ⟦- **Scanning boundary (NFR12):** Syft, Grype, Grant and policy evaluation run only in the control plane through `tools`.⟧
NEW: ⟦- **Scanning boundary (NFR12):** Syft, Grype, Grant, policy evaluation and signature verification (cosign, FR32) run only in the control plane through `tools`.⟧
Why: FR32.

**A43 · Outbound boundary, built-in endpoints · L469 (D10)**
OLD: ⟦  - **Built-in public endpoints** — Grype DB, KEV, EPSS, OSV, CVE List, public Fulcio and Rekor. Only the `feeds`, `enrichment` and `signing` modules call them.⟧
NEW: ⟦  - **Built-in public endpoints** — Grype DB, KEV, EPSS, OSV, CVE List, the end-of-life data source (FR33), public Fulcio and Rekor. Only the `feeds`, `enrichment` and `signing` modules call them.⟧
Why: FR33 adds a public source; air-gapped mode turns it off. (A Sigstore TUF refresh for FR32 would join this list only if O8 decides it.)

**A44 · Requirements → Structure, Fleet Inventory · L476**
OLD: ⟦| Fleet Inventory (FR1–5,29)          | `inventory`, `agentgw`, `agent/watch`       |⟧
NEW: ⟦| Fleet Inventory (FR1–5,29,32)       | `inventory`, `agentgw`, `agent/watch`       |⟧
Why: FR32.

**A45 · Requirements → Structure, Enrichment · L478**
OLD: ⟦| Enrichment & Prioritization (FR11–15) | `enrichment`, `ranking`, `triage`         |⟧
NEW: ⟦| Enrichment & Prioritization (FR11–15,33) | `enrichment`, `ranking`, `triage`      |⟧
Why: FR33.

**A46 · Requirements → Structure, Blast-Radius & Posture · L479 (D3)**
OLD: ⟦| Blast-Radius & Posture (FR16–20,30) | `posture`, `blastradius`, `graph`, `metrics` |⟧
NEW: ⟦| Blast-Radius & Posture (FR16–20,30) | `posture`, `blastradius`, `graph`, `exports`, `metrics` |⟧
Why: stored exports (O1).

**A47 · Data Flow, licence findings · L498 (D1, D8)**
OLD: ⟦License findings skip enrichment/ranking (no KEV/EPSS) but are triagable with the same decision model (FR14) and embedded in the same surfaces (FR28).⟧
NEW: ⟦License findings skip enrichment (no KEV/EPSS) and have no severity; `ranking` places them in the Licences group, listed first and hidden at 0 (violations and warnings; only untriaged violations need attention). They are triagable with the same decision model (FR14) and embedded in the same surfaces (FR28).⟧
Why: the Licences group (D1) and D8.

**A48 · Data Flow, evidence · L500 (D3, D10)**
OLD: ⟦- **Evidence:** every scan, feed version, and triage decision appends to the `evidence` hash-chained ledger (NFR11).⟧
NEW: ⟦- **Evidence:** every scan, feed version, triage decision, stored export and signature check appends to the `evidence` hash-chained ledger (NFR11).⟧
Why: D3 and FR32 create ledger entries.

**A49 · Data Flow, CI scan · L501**
OLD: ⟦prints the verdict and artifact URL.⟧
NEW: ⟦prints the verdict and artifact URL (the piece of software in Software; how CI-only software is grouped there is open, EXPERIENCE Open item 28).⟧
Why: the UI destination is renamed; the grouping is a UX open item.

**A50 · Data Flow, signing · L502 (D10)**
OLD: ⟦Verifying inbound customer-artifact signatures is roadmap, not v1.⟧
NEW: ⟦Verifying customer-artifact signatures is a separate, read-only role (FR32, in v1 since 2026-11-07): `inventory` runs `cosign verify` through `tools` against admin-configured trust; it never signs anything.⟧
Why: D10 moves inbound verification into v1.

**A51 · Coherence Validation · L511**
OLD: ⟦Locked enums match the UX spec's locked glossary.⟧
NEW: ⟦Locked enums carry the technical terms that the UX glossary (ux-Armoury-2026-11-06) keeps for exports, VEX and docs; UI labels map from them in one place.⟧
Why: the UX locked glossary no longer exists.

**A52 · Requirements Coverage · L517**
OLD: ⟦**Functional (31/31 mapped):**⟧
NEW: ⟦**Functional (33/33 mapped):**⟧
Why: FR32, FR33.

**A53 · Gap Analysis, important gap 1 · L527 (D2)**
OLD: ⟦need definition before the posture/pack DQ surfaces.⟧
NEW: ⟦need definition before the DQ API fields and the surfaces in ux-Armoury-2026-11-06 (Software detail value and quality meter, audit report detail, printed cover page; not on Home, not in list rows). The UX grade bands are a placeholder until then (EXPERIENCE Open item 11).⟧
Why: D2.

**A54 · Gap Analysis, minor · L533 (D1)**
OLD (line starts): ⟦- FR13 exact ranking formula⟧
NEW: ⟦- FR13 exact ordering (severity groups Critical/High/Medium/Low with a Licences group first; KEV first within each group, then raw EPSS — never shown as a rating — then a stable tie-breaker). _Open — Story 5.1 amendment fixes the tie-breaker._⟧
Why: D1.

**A55 · Gap Analysis, VEX mapping · L534 (D6, D7)**
OLD: ⟦The **VEX status mapping** (locked statuses → each format's states and justifications, including `accepted` and `fix_planned`) stays open⟧
NEW: ⟦The **VEX status mapping** (locked statuses → each format's states and justifications, including `accepted` and `fix_planned`; decisions per place give one statement per product, so a "Mixed" issue states each product's own status; a `fix_planned` decision without a justification uses the planned fix, for example "Update log4j-core to 2.17.2", as its action statement) stays open⟧
Why: D6 and D7.

**A56 · Gap Analysis, minor · L536 (D3, D10)**
OLD: ⟦- Air-gapped _enrichment_ bundle format (R8 covers feeds; enrichment sources need the same offline path). _Open — Story 4.5 amendment._⟧
NEW: ⟦- Air-gapped _enrichment_ bundle format (R8 covers feeds; enrichment sources need the same offline path). _Open — Story 4.5 amendment._ The end-of-life dataset (FR33) rides the same bundle (Story 4.9 extends the manifest); whether the Sigstore trusted root for keyless signature verification (FR32) does too is open (O8).
- FR32 signature verification details (trust configuration, result states, formats, trusted-root delivery, artifact types). _Open — Story 4.10 amendment._
- FR33 end-of-life source, licence, coverage, matching rule and staleness threshold. _Open — Story 4.9 amendment._
- Stored exports: owning module and whether files are signed. _Open — Story 6.5 planning (O1, O2)._⟧
Why: records the new open details where the architecture tracks gaps.

**A57 · Architecture Readiness, future enhancements · L555 (D10)**
OLD: ⟦build provenance capture + inbound-artifact signature verification;⟧
NEW: ⟦build provenance capture;⟧
Why: inbound verification is now v1 (FR32).

### 4.3 Epics — front matter, requirements, UX-DRs, coverage map, Epic List

<!-- file: _bmad-output/planning-artifacts/epics.md -->

UX-DR numbers stay stable: retired items stay as "Retired" so story references resolve; new items
start at UX-DR37. Where the spine leaves a detail open, the UX-DR cites the EXPERIENCE Open item
number; stories must not invent it.

#### Front matter and Functional Requirements

**E1 · front matter `inputDocuments` · L8–9**
OLD: ⟦  - _bmad-output/planning-artifacts/ux-designs/ux-Armoury-2026-06-12/DESIGN.md
  - _bmad-output/planning-artifacts/ux-designs/ux-Armoury-2026-06-12/EXPERIENCE.md⟧
NEW: ⟦  - _bmad-output/planning-artifacts/ux-designs/ux-Armoury-2026-11-06/DESIGN.md
  - _bmad-output/planning-artifacts/ux-designs/ux-Armoury-2026-11-06/EXPERIENCE.md⟧
Why: the new spines supersede the old ones.

**E2 · front matter `amendments` · after L11**
OLD (anchor, kept): ⟦  - 2026-11-05 Correct Course — _bmad-output/planning-artifacts/sprint-change-proposal-2026-11-05.md (readiness fixes; FR31 and NFR12; Epic 11)⟧
NEW: ⟦  - 2026-11-06 Correct Course — _bmad-output/planning-artifacts/sprint-change-proposal-2026-11-06.md (cluster-based dev loop and CI)
  - 2026-11-07 Correct Course — _bmad-output/planning-artifacts/sprint-change-proposal-2026-11-07.md (UX spines ux-Armoury-2026-11-06; FR32, FR33; Stories 4.9, 4.10)⟧
Why: records this trigger; the applied 2026-11-06 change was also missing from the list.

**E3 · Functional Requirements intro · L24**
OLD: ⟦FR IDs are the PRD's stable IDs (FR29–FR30 were added at finalize and FR31 on 2026-11-05, so they sit out of numeric sequence).⟧
NEW: ⟦FR IDs are the PRD's stable IDs (FR29–FR30 were added at finalize, FR31 on 2026-11-05 and FR32–FR33 on 2026-11-07, so they sit out of numeric sequence).⟧
Why: mirrors P9.

**E4 · new FR32 · Fleet Inventory, after FR31 (L33)**
OLD (anchor, kept): ⟦links known artifacts instead of duplicating them, and the step always prints the verdict and the artifact URL. Central scanning stays the default.⟧
NEW: ⟦- FR32: Artifact signature verification — container images and other OCI artifacts in connected registries are checked against signers an admin trusts (public keys or keyless identities); the result, signer and check time are recorded as evidence and shown in artifact detail; verification runs only on the control plane and works air-gapped (key-based with no network, keyless with trust material supplied offline).⟧
Why: mirrors P10.

**E5 · new FR33 · Enrichment & Prioritization, after FR12 (L47)**
OLD (anchor, kept): ⟦- FR12: Source attribution — every enrichment datum is labelled with its source and retrieval time.⟧
NEW: ⟦- FR33: End-of-life data — for the packages in every stored SBOM, whether each package version has reached its end of life, from an attributed source refreshed like the enrichment feeds, re-joined without rescans and carried in the offline bundle; shown in artifact detail; uncovered packages are "unknown", never "supported".⟧
Why: mirrors P11.

**E6 · FR13 · L48 (D1)**
OLD: ⟦deterministic, explainable ranking: KEV-listed first, then EPSS-weighted severity; the UI can always show why a finding ranks where it does.⟧
NEW: ⟦deterministic, explainable ordering: licence findings as their own group first (hidden when empty), then severity groups Critical, High, Medium, Low; KEV-listed (actively exploited) first within each group, then by EPSS; EPSS is never presented as a rating; the UI states the order in words.⟧
Why: mirrors P12.

**E7 · FR14 · L49 (D6, D7)**
OLD: ⟦status (not affected / mitigated / accepted / fix planned), justification, author and timestamp; decisions propagate⟧
NEW: ⟦status (not affected / mitigated / accepted / fix planned; untriaged when none), justification (required except for fix planned, whose VEX action statement then comes from the planned fix), author, timestamp and scope (every artifact with the same vulnerability or licence in the same package version by default, or one artifact); decisions propagate⟧
Why: mirrors P13.

**E8 · FR16 · L54**
OLD: ⟦- FR16: Fleet posture view — landing state: fleet summary of artifacts, findings by priority, coverage gaps and feed freshness.⟧
NEW: ⟦- FR16: Fleet posture view — landing state (UI: Home): fleet summary of artifacts, the findings that need attention today, open findings by group (FR13), coverage gaps and feed freshness.⟧
Why: mirrors P14.

**E9 · FR17 · L55 (D4)**
OLD: ⟦- FR17: Blast-radius query — given a CVE ID or package+version, answer which artifacts⟧
NEW: ⟦- FR17: Blast-radius query (UI: Exposure) — given a CVE ID, package+version or image digest, answer which artifacts⟧
Why: mirrors P15.

**E10 · FR17 (end) · L55**
OLD: ⟦in seconds, with data provenance (sources, coverage, freshness).⟧
NEW: ⟦in seconds, with data provenance (sources, coverage, freshness); an unknown CVE ID is answered as unknown with the data's age, never as zero; any node of the answer can be followed to its own connections.⟧
Why: mirrors P16.

**E11 · FR18 · L56 (D2, D10)**
OLD: ⟦- FR18: Artifact detail — SBOM contents, findings (vulnerability and license) with triage status, evaluation provenance and running locations.⟧
NEW: ⟦- FR18: Artifact detail (UI: Software detail) — SBOM contents, findings (vulnerability and license) with triage status, evaluation provenance, running locations, signature status (FR32), package end-of-life status (FR33) and the data-quality score (FR30); "check again" re-queues the SBOM and scan.⟧
Why: mirrors P17.

**E12 · FR19 · L57 (D3)**
OLD: ⟦- FR19: Shareable answers — blast-radius results and posture summaries export as report/CSV.⟧
NEW: ⟦- FR19: Shareable answers — the current view of a blast-radius answer, the findings list or the artifact list exports as CSV (JSON optional), with the screen's caveats and provenance, and a blast-radius answer also as a PDF report; every export is stored as evidence (file + ledger entry, evidence-pack retention) and listed with the packs; the posture summary is shared as an evidence pack.⟧
Why: mirrors P18.

**E13 · FR30 · L59 (D2)**
OLD: ⟦at artifact and fleet level, in posture views and evidence packs.⟧
NEW: ⟦at artifact level in artifact detail and at fleet level in evidence packs (their in-product detail and printed cover page); never in list rows.⟧
Why: mirrors P19.

**E14 · FR27 · L72 (D1)**
OLD: ⟦violations surface as findings in the same posture/artifact views, triagable with the FR14 model.⟧
NEW: ⟦violations surface as findings in the same posture/findings/artifact views (UI: a Licences group listed first and hidden when empty, and a Licences type filter), triagable with the FR14 model.⟧
Why: mirrors P20.

#### Additional Requirements (ARCH)

**E15 · ARCH15 · L119 (D11)**
OLD: ⟦as typed enums in Rust, OpenAPI and TS.⟧
NEW: ⟦as typed enums in Rust, OpenAPI and TS. UI labels come from the plain-language glossary (UX-DR33: Not reviewed yet · Not impacted · Fix planned · Mitigated · Risk accepted); enum values and API names do not change.⟧
Why: separates data enums from UI labels; mirrors A29.

**E16 · ARCH16 · L120**
OLD: ⟦User preferences (theme) live in `user_preferences`⟧
NEW: ⟦User preferences (theme Light/Dark, default Light; the single-key shortcut switch from Settings → Personal, default on) live in `user_preferences`⟧
Why: mirrors A15.

**E17 · ARCH19 · L126 (D10)**
OLD: ⟦**built-in public endpoints** (Grype DB, KEV, EPSS, OSV, CVE List, public Fulcio, public Rekor — called only by `feeds`, `enrichment` and `signing`, and turned off completely in air-gapped mode).⟧
NEW: ⟦**built-in public endpoints** (Grype DB, KEV, EPSS, OSV, CVE List, the end-of-life data source (FR33), public Fulcio, public Rekor — called only by `feeds`, `enrichment` and `signing`, and turned off completely in air-gapped mode).⟧
Why: mirrors A43.

**E18 · ARCH20 · L127 (D10)**
OLD: ⟦- ARCH20: Offline bundles cover both vulnerability feeds **and** enrichment sources (KEV/EPSS/OSV/CNA).⟧
NEW: ⟦- ARCH20: Offline bundles cover both vulnerability feeds **and** enrichment sources (KEV/EPSS/OSV/CNA, and end-of-life data from Story 4.9).⟧
Why: FR33 rides the bundle.

**E19 · ARCH25 · L138 (D3; depends on O1)**
OLD: ⟦`posture`, `blastradius`, `graph`, `evidence`,⟧
NEW: ⟦`posture`, `blastradius`, `graph`, `exports`, `evidence`,⟧
Why: the recommended owner of stored exports (A38). This line is a source of Story 1.1 (see Contract status).

**E20 · ARCH29 · L145 (D1, D2)**
OLD: ⟦FR30 scoring model and grade banding; FR13 exact ranking formula;⟧
NEW: ⟦FR30 scoring model and grade banding (the UX bands are a placeholder — EXPERIENCE Open item 11); FR13 within-group order (actively exploited first, then raw EPSS, then a stable tie-breaker — EXPERIENCE Open item 1);⟧
Why: D1 and D2.

**E21 · ARCH33 · L152**
OLD: ⟦about 10 s for the Posture summary while backlog exists⟧
NEW: ⟦about 10 s for the Home summary (posture endpoint, including the Needs-attention count) while backlog exists⟧
Why: mirrors A19.

**E22 · ARCH35 · L154 (D11)**
OLD: ⟦PDFs are rendered by Typst, a pinned static binary run through `tools`, with the bundled fonts.⟧
NEW: ⟦PDFs are rendered by Typst, a pinned static binary run through `tools`, with the bundled IBM Plex Sans and IBM Plex Mono fonts and the DESIGN.md `print-*` palette (Inter is no longer used).⟧
Why: mirrors A24.

**E23 · new ARCH38–ARCH41 · after ARCH37 (L156)**
OLD (anchor, kept): ⟦Known limit: Rekor v2 returns no signed timestamp, so detection of a full rebuild that is re-anchored depends on an earlier receipt (for example in an evidence pack) or on a monitor of the log; an RFC 3161 timestamp authority is a later option.⟧
NEW: ⟦
**Amendments 2026-11-07 (Correct Course; also recorded in `architecture.md`)**

- ARCH38: **Issues read model and review scope** (D1, D6–D8). Findings stay per place (one match on one artifact). The API adds **finding groups** (UI "issue"), keyed by vulnerability ID + package purl@version, or licence + finding kind + package purl@version, with `group` (`licence`/`critical`/`high`/`medium`/`low`), `kev`, place count, issue-wide `triage_status`, derived `mixed` with the count of places that differ, and `needs_attention`; per-group and per-status counts and a pager total come from the server. Needs attention = any place `untriaged` AND (`kev` OR critical) for vulnerabilities; any place `untriaged` for `license_violation`; never for `license_warning`. Decisions carry scope `all_places` (default; covers artifacts found later) or `artifact`; per-artifact decisions override and survive a later `all_places` decision. `justification` is required except for `fix_planned`. Metrics keep counting findings (places).
- ARCH39: **Stored exports** (D3, FR19). Export (CSV of the current view; JSON option) from Exposure, Issues and Software, and the Story 6.5 answer report, are stored: the file in the object store (content-addressed, via `blob`), an insert-only `exports` record and a ledger entry with the file digest (who, when, view, query or filters, format, row count, caveats). Evidence-pack retention (ARCH30); no edit or delete. Listed newest first in Reports → Exports. Owner module `exports` (recommended, O1).
- ARCH40: **Artifact signature verification** (FR32). Control plane only: `inventory` runs `cosign verify` through `tools` against signatures read from the connected registry (credentials in per-invocation env), using admin-configured trust (public keys, keyless identities; default none). Results and trust-policy versions go to the ledger and the artifact API. Air-gapped: no network for key-based checks; keyless checks use an offline trusted root. The trust model, result states, formats, trusted-root delivery and artifact types are recorded as an amendment approved before Story 4.10.
- ARCH41: **End-of-life data** (FR33). One more `enrichment` source (a built-in public endpoint with an offline-bundle equivalent), stored as versioned, attributed snapshots, re-joined to stored SBOM packages without re-matching; status past end of life / supported / unknown per package; carried in the offline bundle. The source, licence, coverage, matching rule and staleness threshold are recorded as an amendment approved before Story 4.9.⟧
Why: the new architecture decisions, mirrored like ARCH31–ARCH37.

#### UX Design Requirements

**E24 · header · L166**
OLD: ⟦From `DESIGN.md` + `EXPERIENCE.md` (ux-Armoury-2026-06-12, both final). Token names refer to DESIGN.md frontmatter.⟧
NEW: ⟦From `DESIGN.md` + `EXPERIENCE.md` (ux-Armoury-2026-11-06, both final, updated 2026-11-07; they supersede ux-Armoury-2026-06-12 — Correct Course 2026-11-07). Token names refer to DESIGN.md frontmatter. UX-DR numbers are stable: retired items stay as "Retired" so story references resolve; new items start at UX-DR37. Where a requirement is not yet drawn, the item cites the EXPERIENCE "Open items" number — do not invent it.⟧
Why: new source and the numbering rule.

**E25 · UX-DR1 · L170 (D11, D2)**
OLD (line starts): ⟦- UX-DR1: Semantic colour token layer⟧
NEW: ⟦- UX-DR1: Semantic colour token layer on shadcn-svelte CSS variables (DESIGN.md "shadcn mapping", plus `--paper`, `--dq`, `--dq-muted` and `--dq-wash`), with two themes shipped day 1 — **Light** (default; unsuffixed tokens) and **Dark** (`-dark` tokens) — sharing the same roles, layout and density, using the exact DESIGN.md values. Components reference semantic roles only, never a theme-specific hex. `lime` only for the active nav item and the one primary action per view, plus the agreed exceptions (the selected graph node and "Selected on the map", the Issues nav badge count, text selection); `forest` for selection, the active tab and the active segment, with the text colour switching with the fill (`on-forest`, `sage`, `sage-hi`, `sel-chip`); `dq` and `dq-muted` only for data quality. No red anywhere. `print-*` tokens feed the Typst template only and never follow the app theme. Both themes hold WCAG AA (lowest text pair 4.9:1); there is no separate high-contrast theme (confirm — EXPERIENCE Open item 25).⟧
Why: three dark themes → Light + one Dark; the old `rail-*`, `data-quality`, `accent`, `success`, `warning` tokens no longer exist.

**E26 · UX-DR2 · L171 (D11)**
OLD (line starts): ⟦- UX-DR2: Typography tokens⟧
NEW: ⟦- UX-DR2: Typography tokens — **IBM Plex Sans** (variable) for everything; IBM Plex Sans Bold Italic only for the 22px wordmark; **IBM Plex Mono** 400 only for IDs, fingerprints, commands and keys. All SIL OFL 1.1, self-hosted (no network at view time; air-gap safe). Nine sizes only — 12 · 13 · 14 · 15 · 17 · 20 · 24 · 30 · 40 — plus the 22px wordmark as the single exception; roles per DESIGN.md (page-title 30/600, headline-number 30/500, group-heading and detail-title 24/600, answer 24/400, inspector-title 20/600, cell-heading 17/600, body and row-title 15, secondary 14, meta, severity-label and mono-id 13, button-label and mono-small 12). Weights 400 / 500 / 600; `tabular-nums` in every data role; sentence case everywhere (uppercase only for button labels, the Graph/Table switch and zoom labels); no eyebrows, kickers or tracked-caps labels.⟧
Why: Inter, the hero numeral and micro-labels are dropped.

**E27 · UX-DR3 · L172 (D11)**
OLD (line starts): ⟦- UX-DR3: Shape, spacing and elevation tokens⟧
NEW: ⟦- UX-DR3: Shape, spacing and elevation tokens — rounded xs 3 / sm (= DEFAULT) 4 / md 6 / lg 10 / pill 999 / full; layout tokens sidebar-width 252, list-width 376 (Issues 500, Reports 420), list-gutter 32, detail cell 30 × 34, row-y 17 (Issues 14, summary rows 12), nav-item-height 54, tab-height 64, button-height 42 (sm 32, wide 54), field-height 42, query-height 44, pager-button 32, table-cell-y 12. **One density only** (no Compact mode or toggle). Depth is flat and tonal (ink → paper → canvas → chip) with 1px `rule` lines, never nested cards; the only shadow is the ⌘K dialog over `scrim`. Disabled controls at 0.45 opacity — the only opacity on elements with text.⟧
Why: none of the old spacing tokens exist.

**E28 · UX-DR4 · L173 (D11)**
OLD (line starts): ⟦- UX-DR4: Theme switcher in Settings⟧
NEW: ⟦- UX-DR4: Theme switch — a Light / Dark segmented control in Settings → Personal and a ⌘K action ("Switch theme…"); no header switcher (the header is gone). Applies instantly with no reload; persisted per user server-side (`user_preferences`, `GET`/`PUT /api/v1/me/preferences`); new users get **Light**. Whether to follow `prefers-color-scheme` is not decided (EXPERIENCE Open item 3) — do not detect OS preference until it is. The printed report never follows the theme.⟧
Why: the Forge fallback and the header affordance are gone.

**E29 · UX-DR5 · L177 (D11)**
OLD (line starts): ⟦- UX-DR5: App shell⟧
NEW: ⟦- UX-DR5: App shell — black sidebar (`sidebar`, 252px): wordmark; a "Search or jump to… ⌘K" field that opens the palette; seven labelled items **Home · Software · Issues · Exposure · Reports**, a divider, **Settings · Help** (20px icon + label, 54px tall); the user menu at the foot (UX-DR43). The active item mirrors the route (`lime` fill, `ink` text, weight 600); hover `ink-2`. Issues carries the Needs-attention badge (UX-DR38). No top nav and no page header: every surface opens with a page title equal to its sidebar label plus one summary line with key numbers in bold ("Issues" + "3 need attention today. 312 not reviewed yet."). Routes `/`, `/software/<name>`, `/issues`, `/exposure?q=…[&view=table]`, `/reports/<id>`, `/settings/<panel>`. Below 1280px the sidebar becomes an icon rail (UX-DR35).⟧
Why: the 58px rail, page header, breadcrumb, accent rule and old surface names are gone.

**E30 · UX-DR6 · L178 (D11)**
OLD: ⟦typing a CVE ID, `package@version` or digest routes to a blast-radius answer; result groups Answers → Navigate → Actions → Recent; `aria-live` results; no-match copy "No matches. Try a CVE ID, package@version, or digest."; the Posture header search is the same palette, pre-scoped.⟧
NEW: ⟦opened from anywhere, from the sidebar search field and from the Exposure query button; a 660px `Dialog` that traps focus, dims the page, never navigates on its own and returns focus on `Esc`; actions include Review, Export, Generate audit report and Switch theme; typing a CVE ID, `package@version` or fingerprint routes to an Exposure answer (a new question on Exposure starts a new trail); results grouped **Issues · Software · Exposure · Actions** with counts, best match first, matched text underlined; `↑`/`↓` move, `↵` open, `esc` close; results announced via polite `aria-live`; no-match copy "No matches. Try a CVE ID, package@version or fingerprint." plus common actions. The prior "Recent" group is not drawn (EXPERIENCE Open item 20).⟧
Why: new groups; digest → fingerprint; no header search.

**E31 · UX-DR7 · L179 (D4, D11)**
OLD (line starts): ⟦- UX-DR7: Keyboard map⟧
NEW: ⟦- UX-DR7: Keyboard map — `⌘K`/`Ctrl+K` search or jump; `g` + letter goes to a surface (letters show beside each nav item after pressing `g`; the letters for the renamed surfaces are not yet assigned — EXPERIENCE Open item 13); `J`/`K` next / previous list item; `/` focus the list search; `⌘↵` Save and next in the review panel; `Esc` closes the topmost layer (the palette) or unpins the graph selection; `x` exports the current view; `?` shortcut map (also listed in Settings → Personal); graph: arrows/`Tab` move between nodes, `↵` moves the map to the focused node (UX-DR24), `Backspace` goes back one step, `+`/`−` zoom, Fit; the node's detail opens from the inspector. The prior `t` (triage drawer) and `e` (explore in graph) bindings are retired until new meanings are agreed (Open item 13). Single-key shortcuts (`J`, `K`, `/`, `x`, `?`, `g`+letter, `Backspace` on the map) work only outside text fields and can be turned off in Settings → Personal (WCAG 2.1.4); modified shortcuts stay on. No custom key bindings in v1.⟧
Why: old g-letters, `t` and `e` map retired surfaces; J/K, `/`, map moves and the off switch are new.

**E32 · UX-DR8 · L183 — retire**
OLD (line starts): ⟦- UX-DR8: Hero stat + co-stat band⟧
NEW: ⟦- UX-DR8: Retired 2026-11-07 — ux-Armoury-2026-11-06 has no hero numeral, co-stat band or count-up. Home's fleet readings are the summary line, Needs attention, Open issues and the "Across all software" band (UX-DR22).⟧
Why: removed from the design; the number stays for Story 2.9's reference.

**E33 · UX-DR9 · L184 (D8, D11)**
OLD (line starts): ⟦- UX-DR9: Finding marks⟧
NEW: ⟦- UX-DR9: Issue marks — three separate axes, never combined. **Severity** as word + 4-step level marker (Critical 4 bars `clay`, High 3 `amber`, Medium 2 `slate`, Low 1 `forest-ink`), text colour only, no fills, no red. **Actively exploited** (KEV) as quiet clay text with a pulse icon in list rows and palette results, and a `clay-wash` pill in detail panels and the Exposure answer; never dropped when a row truncates; a small grey mono "KEV" tag beside the pill in detail views and technical details only. **Licence** as the neutral `text-2` scale icon + word plus a "Licence" kind tag, never severity-hued; a licence warning (policy treatment "warning") also carries the word "Warning" on line 2, a not-reviewed violation "Needs a decision" (D8). **Review status** as a neutral chip with a drawn icon and its word — Not reviewed yet (open circle), Not impacted (tick), Fix planned (arrow), Mitigated (half-filled circle), Risk accepted (flag) — plus Mixed (UX-DR39). On a selected row every mark switches to `sage-hi` (chips on `sel-chip`). EPSS is never shown as a rating, tag or column; the raw value appears only in the technical-details block.⟧
Why: tinted chips, the critical-hued KEV tag and status-hued pills are gone; D8 adds the "Warning" word.

**E34 · UX-DR10 · L185 (D2)**
OLD (line starts): ⟦- UX-DR10: DQ badge/score⟧
NEW: ⟦- UX-DR10: Data quality (FR30) — a small violet reading, never a threat. The value (`dq-value`): score + letter ("91 A−") in `dq`, `dq-muted` for low grades (D and below; the bands are a placeholder until the Story 8.1 model — EXPERIENCE Open item 11); never clay, amber or red, never opacity, never a big numeral in the app; accessible name in full ("Data quality 91 out of 100, grade A−"). The **quality meter** (`quality-meter`): five parts, each out of 100 — Package lists, Coverage, Freshness, Extra sources, Vulnerability records — with only the weakest part emphasised in `dq` and explained in one sentence, with a `forest-ink` link when there is something to do ("See them"); at a low grade the two weakest parts each get a sentence and a grey Check again appears; the technical terms sit on one grey line and in each name's `title` attribute. Placements: Software detail (the Info value and the Data quality cell, UX-DR25), the audit report detail in Reports (a full-width Data quality row with the fleet reading "when it was made", UX-DR27) and the printed cover page (UX-DR46). **Not on Home** (it may join the Home Details tab later — Open item 14) and **never in list rows**. What shows before a score exists is open (Open item 32).⟧
Why: D2 — the old DQ badge, hue, `data-quality-muted` token and grade-in-row rules are replaced by the new design.

**E35 · UX-DR11 · L186 (D1, D6, D8)**
OLD (line starts): ⟦- UX-DR11: Findings table⟧
NEW: ⟦- UX-DR11: Issues list — grouped, not a single ranked table. A **Licences** group at the top (violations and warnings; hidden at 0, while the type filter still shows "Licences 0"), then **Critical · High · Medium · Low** with counts; within each group Actively exploited first, then by raw EPSS (never shown; EXPERIENCE Open item 1); the order stated in words above the list ("Actively exploited sorts first in each group"). One row per issue (UX-DR39) with the review-status chip (or "Mixed · N of M") as the one right column. Filters: the type segmented control All · Vulnerabilities · Licences with counts; the Review status filter listing the five statuses with counts, default Not reviewed yet, never mixed with the severity groups; the search "Find a package or vulnerability" (`/`). Long groups end in an "N more High" row; the pager reads "1–25 of 312 · page 1 of 13", 25 per page, never infinite scroll. Row click or `J`/`K` selects and fills the detail column (UX-DR26); the row-level "Explore in graph" is replaced by See exposure / See the map in the detail.⟧
Why: severity groups replace the KEV-then-EPSS ranking (D1); 30px rows and the drawer are gone.

**E36 · UX-DR12 · L187**
OLD: ⟦- UX-DR12: Coverage-gap row — inline at the position of the missing data; dashed warning styling; names counts and locations;⟧
NEW: ⟦- UX-DR12: Coverage-gap row ("Not checked yet") — sits in the list where the missing rows would be (Software, Exposure list and table, Home band); title + count in `text-3` and one plain sentence naming the count and where ("…including 212 in prod-eu-west. Their issues are unknown, not absent."); no tint, no dashes;⟧
Why: the `warning` token and dashed styling are gone; the rest of the bullet is kept.

**E37 · UX-DR13 · L188 (D11)**
OLD (line starts): ⟦- UX-DR13: Populating banner⟧
NEW: ⟦- UX-DR13: Checking band — an edge-to-edge `paper` band on Software and Home whenever first-check or re-evaluation backlog exists: title "Checking 671 more pieces of software…" with an estimate in words ("about 2 h left"), an 8px determinate bar (`forest-ink` on `forest-wash`) with "3,176 of 3,847 checked (82%)", and "You can keep working: numbers update as each one finishes." Names appear at once and counts fill in; rows show step text ("Reading packages · step 2 of 3", "Waiting its turn"); `chip` skeletons only where data is missing; progress is a polite `role="status"`. Never modal, blocking or a spinner.⟧
Why: the warning-tinted banner, heading block and Posture/Artifacts names are gone.

**E38 · UX-DR14 · L189 — retire**
OLD (line starts): ⟦- UX-DR14: Severity band⟧
NEW: ⟦- UX-DR14: Retired 2026-11-07 — the stacked severity band is not in ux-Armoury-2026-11-06. Home's **Open issues** summary rows replace it: Licences first (hidden at 0), then Critical with "N actively exploited", High, Medium and Low, each with its count (UX-DR22). What a click on those rows does is not drawn (EXPERIENCE Open item 18).⟧
Why: soft fills and the click-filter band are removed.

**E39 · UX-DR15 · L190 (D11)**
OLD (line starts): ⟦- UX-DR15: Freshness strip⟧
NEW: ⟦- UX-DR15: Freshness strip — one row on `paper` at the bottom of Home's detail column: each source in plain words with its age and the technical term small in `text-3` ("Vulnerability data 41 min ago · Exploited list KEV 6 Nov · Packages 38 min ago · 2 clusters reporting"; every attributed enrichment source per FR12 appears); a stale source turns `amber` with its age in words, an `amber-dot` and a clock; a "Sources" link opens Settings → Sources. Exposure and Software detail carry provenance inline ("Answered 38 min ago", "How we know: Syft v… · Grype DB v… · checked …", "Last checked"); whether the full strip also appears there is open (EXPERIENCE Open item 19), and so is whether end-of-life data (FR33) appears on the strip or only in Settings → Sources (O15).⟧
Why: success/warning tokens, mono feed versions and old surface names are gone.

**E40 · UX-DR16 · L191 (D6, D7)**
OLD (line starts): ⟦- UX-DR16: Triage drawer⟧
NEW: ⟦- UX-DR16: Review panel — in the Issues detail column (Review tab), replacing the slide-over triage drawer; the list stays visible. A scope segmented control comes first: **"All N places"** (default) or **"Only this software"**, which reveals a `Select` of the places and is pre-filled when Review was opened from a piece of software. Question 1, "Does this vulnerability impact us?": **No, not impacted** → Not impacted; **Yes** → question 2, "What will we do?": **Fix it** → Fix planned, **Reduce the risk** → Mitigated, **Accept the risk** → Risk accepted. Each option shows the status chip it produces. "Why? (shown in the audit report)" is required for Not impacted, Mitigated and Risk accepted, and optional for Fix planned (D7). Lime **Save and next ⌘↵** stays disabled until a question is answered; it records status, justification, author, timestamp and scope (FR14), updates the row chip in place ("Mixed" when places now differ) and moves to the next issue in the current filter. Grey **Decide later** moves on without recording. Hint: "Saved with your name in the audit trail." A later all-places decision does not overwrite places with their own status, and the panel says how many keep theirs ([ASSUMPTION], EXPERIENCE Open item 9). A failed save shows the inline error (UX-DR41) and does not advance. The panel ends with the technical-details block (CVE, KEV, CVSS, raw EPSS, source, check time). Status never changes inline. Review buttons on Home, the Exposure inspector and Software open the issue in Issues on its Review tab ([ASSUMPTION], Open item 4). Not yet drawn but still required: licence-review copy (Open item 16), and vendor VEX claims with attribution plus "the decision that applies now and its source" (FR15; Open item 17). Agree both with UX before the stories that build them.⟧
Why: the drawer becomes the review panel with two questions; the default scope is all places (D6).

**E41 · UX-DR17 · L192 (D11)**
OLD (line starts): ⟦- UX-DR17: Graph node/edge language⟧
NEW: ⟦- UX-DR17: Exposure graph language — hairline, left to right, four sentence-case tiers with counts: Vulnerability · Package · Software · Where it runs. Circular nodes (`canvas` fill, `forest-ink` or `forest-2` ring); only the vulnerability node takes clay (`clay-wash` fill, `clay-dot` ring, pulse icon when actively exploited). Deployed edges solid `forest-2`; not-deployed edges dashed `slate-dot`, with not-deployed software below a dashed rule labelled "Not deployed" (never colour alone). The selected path is heavier `forest-ink`; the selected node is lime with "Selected on the map". Roll-up text nodes ("8 more", "5 more places") expand; edge labels read like "direct · in 12". Legend, zoom (+ / − / Fit) and the caveat line sit in a footer. Nodes are focusable with an `aria-label` (name + tier + state), and the map has an `aria-label` summarising the answer. Hover or focus highlights the direct path; `Esc` unpins. The moved-map (ego view) visuals are in UX-DR24.⟧
Why: the `node-inactive-border`, `text-muted` and `accent` tokens and the rect nodes are gone.

**E42 · UX-DR18 · L193 (D4)**
OLD (line starts): ⟦- UX-DR18: Node inspector⟧
NEW: ⟦- UX-DR18: Inspector — under the Exposure map (not a side panel), two cells for the selected node: identity (title with version and "Selected on the map"; Name, Fingerprint in mono, Runs in, Copies, How it got it) and "What to do" (The fix, the review-status chip, lime Review, grey Open software); it ends with "How we know: Syft v… · Grype DB v… · checked 38 min ago". On a map centred on a piece of software the identity cell adds Issues ("2 open: 1 Critical, 1 Low"), the lime action is **Open software**, **Show only this** stays grey, and a hint reads "Click any node to move the map to it. Enter does the same from the keyboard." Selection carries across Graph and Table; `Esc` unpins.⟧
Why: Graph explorer and its side panel are gone; the inspector supports traversal (D4).

**E43 · UX-DR19 · L194 (D11)**
OLD (line starts): ⟦- UX-DR19: Evidence pack card⟧
NEW: ⟦- UX-DR19: Signature status (Reports → audit report → Overview, beside Coverage) — **verified:** a `forest-wash` disc with a tick, "Signature verified" and the signer key, then a code block (UX-DR42) with the copyable offline `cosign verify-blob` command ("Auditors can run this themselves, without Armoury."; operator public key by default; the keyless command only when keyless signing is enabled, never when air-gapped). **Does not verify:** an error band in place of the disc, naming the file and the reason ("The signature on pack.pdf does not verify: the file has changed since it was signed.") and linking to the audit-trail entry for the signing; downloads stay available.⟧
Why: "Evidence pack card" becomes the audit report's signature status, with a failure state.

**E44 · UX-DR20 · L195**
OLD: ⟦- UX-DR20: Evidence pack generator — one-click "Generate CRA pack" with smart defaults (last audit window, whole fleet), configuration (window, scope, framework) after the click and never a wizard before;⟧
NEW: ⟦- UX-DR20: Audit report generator — one click on lime **Generate audit report** (Reports, ⌘K) with smart defaults (last 12 months, whole fleet); window, scope and framework adjustable after the click, never a wizard before (FR22; how is not drawn — EXPERIENCE Open item 22); the user keeps working and the report appears in Reports → Audit reports when signed (PDF + package lists (SBOM) + review decisions (VEX)); a failure to start shows the inline error (UX-DR41);⟧
Why: the UI label becomes "Audit report"; the rest of the bullet is kept.

**E45 · UX-DR21 · L196 (D3)**
OLD (line starts): ⟦- UX-DR21: Export⟧
NEW: ⟦- UX-DR21: Export — `Export` (and `x`) on Exposure, Issues and Software exports the current view as CSV by default, with JSON as an option (PROC2); on a moved Exposure map it exports the current centre. Every export carries the same caveats and provenance as the screen ("The 2 not checked yet travel with the CSV and the audit report") and is **stored as evidence**: it lands in Reports → Exports with an audit-trail entry (who, when, which view and query) and the same retention as audit reports (24 months, never below the floor); each row says what and where from ("Exposure: log4j-core 2.17.0 · CSV · 14 rows · from Exposure · 6 Nov"). Exposure also offers **"Audit report for this answer"**: the PDF answer report (Story 6.5, UX-DR46 print rules), stored and listed in Reports → Exports like any export. Home has no Export; the posture summary is shared as the audit report. Export is a read action, available to auditors. A failed export shows the inline error (UX-DR41).⟧
Why: D3; Blast radius and Posture are gone.

**E46 · UX-DR22 · L200 (D2, D11)**
OLD (line starts): ⟦- UX-DR22: Posture surface⟧
NEW: ⟦- UX-DR22: Home surface (`/`; was Posture). List column: "Home" + a scoped summary ("You are in good shape. 3 things need attention today."; it gains a scoped caveat when a source is stale) + "Last checked 38 min ago"; **Needs attention N** (UX-DR38; right column = places); **Open issues N** summary rows (Licences first and hidden at 0, then Critical with "N actively exploited", High, Medium, Low); "312 not reviewed yet · 782 reviewed · See all" (opens Issues); lime **Review all N** (opens the Needs-attention issues in Issues one after another [ASSUMPTION, Open item 4]). Detail column for the selected issue: tabs Overview · Exposure · How to fix · Details (only Overview is drawn; the Exposure tab is a reduced summary of the Exposure page with a button that opens it — Open item 14). Overview holds the title, one plain sentence of what it means, severity, exploited pill + KEV tag, Vulnerability (CVE ID), Found in, The fix and Review status; grey Review and See exposure; and an Exposure cell (All / Deployed / Not deployed) with "See all N on the map". Below it, a separate "Across all software" `paper` band: Checked gauge ("671 are waiting their turn"), Open issues (30-day sparkline, delta chip) and Audit report (last 12 months, signed, coverage, Download / Preview). **No data-quality reading on Home** (D2). The freshness strip sits at the bottom (UX-DR15). The order within Needs attention is not decided (Open item 21). Every reassuring sentence is scoped to what was checked.⟧
Why: Posture's hero, co-stats and severity band are gone; D2 keeps DQ off Home.

**E47 · UX-DR23 · L201 (D11)**
OLD (line starts): ⟦- UX-DR23: Blast radius surface⟧
NEW: ⟦- UX-DR23: Exposure surface (`/exposure?q=…[&view=table]`; was Blast radius and absorbs Graph explorer). A full-width header across list and map: "Exposure" + the question ("Where are we exposed to log4j-core?"), the query button showing the subject (opens ⌘K), the Graph · Table switch, grey Export and "Audit report for this answer". The answer comes first, in words ("14 pieces of software have it. 9 are deployed, 5 are not deployed."), then a meta line (exploited pill, KEV tag, severity, CVSS, "Answered 38 min ago") and deployed/not-deployed split bars. List column: Deployed N, Not deployed N, then the "Not checked yet" row. Graph (UX-DR17) with the inspector (UX-DR18). Table: the same answer in the same order (deployed first), with sortable sentence-case headers (Software, Version, Deployed? Yes/No, Where it runs, Copies, Severity, Review), selection carried across, and "2 not checked yet, not listed". Every partial answer carries its caveat line. Progressive partial results (polled) appear after 2 s with a scope line ("Checking — 1,204 of 3,000 pieces of software so far"). Queries accept a vulnerability ID, `package@version` or a fingerprint; a fingerprint query centres on that piece of software (the prior digest layout). Moving the map is UX-DR24; the no-query, unknown-vulnerability and coverage-scoped-zero states are UX-DR40.⟧
Why: Blast radius and Graph explorer merge into Exposure.

**E48 · UX-DR24 · L202 (D4)**
OLD (line starts): ⟦- UX-DR24: Graph explorer⟧
NEW: ⟦- UX-DR24: Moving around the Exposure map (the prior Graph explorer's traversal, kept inside Exposure; "Explore in graph" and the Graph explorer screen are retired). One rule for every node: **click or `Enter` moves the map to that node** (ego view): the centre sits in the true centre (`forest` disc, `forest-ink` ring, lime inner dot, 28px outer ring, name, version, "Centre of the map" and the fingerprint); what it contains is on the left, where it runs and its copies on the right; the node you came from carries the "Came from here" marker; packages with no known issues roll up ("212 more packages · No known issues") with a caveat line. An **Exposure trail** (`exposure-trail`) sits directly above the moved map: Back, the previous steps as link chips, the current step in bold, key hints "↵ Move the map · ⌫ Back"; Back, `Backspace` (outside text fields), any earlier step or the browser Back returns to that map with its selection. The question, query button, answer line, list column, Export, "Audit report for this answer" and the URL (`&from=` the previous step) follow the centre, so a trail can be shared and reloaded; ⌘K starts a new trail; the Table lists the centre's neighbours. One motion moment: the centre ring scales in once (0.62 → 1, 200 ms), none under reduced motion. The trail is a `nav` named "How you got here" with `aria-current="location"` on the current step; [ASSUMPTION] focus goes to the new centre and the new answer is announced politely (Open item 12). Only a software centre is drawn; package, vulnerability, place and roll-up centres follow the same rule but are not drawn, nor is a long trail or the Table of a moved map (Open item 19). Contextual entry: See exposure, See the map, See all N on the map and Exposure results in ⌘K open Exposure for that subject.⟧
Why: D4 — traversal kept inside Exposure with the ego view, trail and Back.

**E49 · UX-DR25 · L203 (D2, D10)**
OLD (line starts): ⟦- UX-DR25: Artifacts⟧
NEW: ⟦- UX-DR25: Software surface (`/software/<name>`; was Artifacts). "Software" + "3,847 pieces of software. 1,126 deployed, 2,721 not deployed." The real fleet is grouped **Deployed N** (second line "prod-eu-west · 4 copies") and **Not deployed N** (second line "Last deployed 12 days ago" or "Never deployed"; the hint "Not seen running in any connected cluster." shows on hover and focus); the right column is the issue count; then the "Not checked yet" row (UX-DR12), the pager and lime **Add software** (destination not drawn — Open item 18). No data-quality grade in list rows. Detail tabs are Overview · Issues · Packages · Audit trail, with "Deployed" status at the end of the bar. Overview, in this order: (1) **Info** (left): Name, Fingerprint (mono, Copy), Runs in, Copies, **Built**, Last checked, **Data quality** (UX-DR10 value), **Signed** (FR32, D10); grey **Check again** (re-queues the SBOM and scan for this one piece of software) and Audit report; beside it **Packages** ("214 packages · SBOM", Direct / Indirect, a licence line and an **end-of-life** line — FR33, D10) over **Where it runs**; (2) **Issues** full width with Review; (3) the **Issues trend** chart; (4) **Data quality** ("How much you can trust these numbers": the quality meter, UX-DR10); (5) **Latest in the audit trail** ("Entries are never edited or removed"). The words for each signature state and for end-of-life lines other than "No package is past its end of life." are not written (O7, O14); what Data quality shows before a score exists is open (Open item 32).⟧
Why: Artifacts becomes Software with Deployed/Not deployed; D2 and D10 add the detail fields.

**E50 · UX-DR26 · L204**
OLD (line starts): ⟦- UX-DR26: Findings surface⟧
NEW: ⟦- UX-DR26: Issues surface (`/issues?review=not-reviewed`; was Findings) — "Issues" + "3 need attention today. 312 not reviewed yet."; the grouped list (UX-DR11) and review panel (UX-DR16) serve vulnerabilities and licences alike (no dedicated licence dashboard). Detail tabs: Review · Exposure · History (Exposure and History are not drawn — EXPERIENCE Open item 15). The Review tab holds the summary (title, severity, pill, KEV), the Exposure count with "See the map", What to do, Review status, the review panel and the technical details.⟧
Why: Findings and triage are retired UI labels.

**E51 · UX-DR27 · L205 (D2, D3, D9)**
OLD (line starts): ⟦- UX-DR27: Evidence surface⟧
NEW: ⟦- UX-DR27: Reports and the audit trail (was Evidence). Reports (`/reports/<id>`) holds exactly three groups — **Audit reports N**, **Exports N** and **Audit trail** (D9) — with lime Generate audit report; any other report type needs a Correct Course. **Audit reports** detail: tabs Overview · Files · Audit trail, with "Generated today, 08:31, by …" in the bar; Overview: title, lead, Download all / Preview; row 1 Coverage when it was made | Signature (UX-DR19); row 2 Data quality, full width ("Data quality 84 B+ when it was made", the fleet quality meter, UX-DR10 — the only place the fleet five-part breakdown appears in the product); then Files (pack.pdf; sboms.tar.gz "Package lists … SBOM"; vex.json "review decisions … VEX") and What it says. **Exports** (UX-DR21): newest first; the detail of a selected export is not drawn (EXPERIENCE Open item 15). **Audit trail** (fleet-wide, D9): ledger entries newest first (type, subject with its plain label and technical ID, actor, time, tool/feed versions), filters by type, subject and time window, the chain verification ("Chain intact — N entries, verified 4 min ago" or the first broken entry), the latest signed checkpoint and the anchoring status (mode, latest anchored checkpoint, pending anchors); the group is not yet drawn (U-edits, O16). The append-only trail also shows per item as tabs (a software's Audit trail, an issue's History, a report's Audit trail): no edit or delete affordances; a correction is a new entry superseding the old, and both stay visible; "Entries are never edited or removed."⟧
Why: Evidence becomes Reports; D9 adds the fleet-wide Audit trail group; D2 adds the DQ row.

**E52 · UX-DR28 · L206 (D10, D11)**
OLD (line starts): ⟦- UX-DR28: Settings⟧
NEW: ⟦- UX-DR28: Settings — a panel list in the list column ([ASSUMPTION], EXPERIENCE Open item 6), one route per panel (`/settings/<panel>`) so links (the freshness strip's "Sources", "Open connection settings") open a panel directly. **Connections**: registry connections (FR1), package feeds (FR29), agent install (copy-paste one-liner in a code block, read-only trust posture and the exact RBAC shown before install). **Sources**: feed status and history, feed-bundle import (FR10), end-of-life data source (FR33). **Policy**: licence policy (FR27), signature policy — trusted keys and keyless identities (FR32), CI policy (Epic 11), evidence retention (the UI never permits below the 24-month floor, FR23). **Access**: users and roles, the read-only resolved auth configuration, CI tokens (Epic 11). **Signals**: Prometheus endpoint URL + metric list, read-only with copy (FR20); signing public key. **Personal**: theme, the keyboard shortcut list and the single-key shortcut switch. Edit controls are absent for roles without write access; OIDC is declarative only, never a UI wizard (NFR6); a save failure shows the inline error (UX-DR41). The panels for FR32 and FR33 are spine-only, like the rest of Settings (see U-edits).⟧
Why: Feeds becomes Sources; the panels move to the list column; the shortcut switch and the D10 settings are new.

**E53 · UX-DR29 · L210 (D11)**
OLD (line starts): ⟦- UX-DR29: Pre-setup empty Posture⟧
NEW: ⟦- UX-DR29: Pre-setup empty Home — the page title plus exactly the two setup actions (connect a registry, install a cluster agent), each with a copy-paste one-liner in a code block (UX-DR42); no illustration. When a registry is unreachable, Software shows an edge-to-edge `clay-wash` error band ("We can't reach registry.acme.internal": since when, what it affects, what still works, likely cause). Its lime **Try again** is the view's one lime action (Add software turns grey), with grey **Open connection settings** → Settings → Connections. Affected rows read "As of 14:02 · registry" in amber with a clock; nothing is removed; Home carries a gap row naming the registry.⟧
Why: Posture and the heading block are gone; the error band is new.

**E54 · UX-DR30 · L211**
OLD: ⟦- UX-DR30: Degraded states — stale feed flips age to warning and adds a scoped posture caveat (reflected in DQ); disconnected agent shows last heartbeat with runtime data marked stale-as-of, not removed;⟧
NEW: ⟦- UX-DR30: Degraded states — **stale source:** its age turns `amber` with the age in words, an amber dot and a clock, and the Home summary gains a scoped caveat, so "good shape" is never claimed on old data (reflected in the Freshness part of data quality where it is shown). **Disconnected agent:** "N clusters reporting", and that cluster's runtime data is marked "as of", not removed (heartbeat 30 s, stale after 5 min, disconnected after 60 min, Helm values);⟧
Why: the `warning` token and the posture label are gone; the air-gapped clause is kept with "shows bundle age" read as "shows source bundle age".

**E55 · UX-DR31 · L212**
OLD: ⟦- UX-DR31: Read-only auditor — triage forms, pack-config edits, pack generation and Settings mutations are absent (not disabled); all read surfaces and pack viewing, download and verification remain available.⟧
NEW: ⟦- UX-DR31: Read-only auditor — Review (the review panel and Review actions), Add software, Generate audit report (and audit-report configuration) and Settings mutations are absent, not disabled; Check again follows its declared minimum role (O4); every read surface, Export, and viewing, downloading and verifying audit reports remain available; the same sidebar, words and numbers as the analyst.⟧
Why: triage and pack are now the UI labels Review and Audit report; the `rbac.auditorCanGeneratePacks` sentence is kept.

**E56 · UX-DR32 · L213**
OLD: ⟦API errors render the typed envelope `message`; never a bare or unexplained spinner.⟧
NEW: ⟦a failed save or start shows the inline error (UX-DR41) where the action was taken; a failed connection or source shows the error band in the affected view; error copy names the problem in plain words (from the typed envelope `message`) and what still works; never a bare or unexplained spinner, never a toast.⟧
Why: the inline-error and error-band patterns.

**E57 · UX-DR33 · L217 (D3, D11)**
OLD (line starts): ⟦- UX-DR33: Voice and vocabulary⟧
NEW: ⟦- UX-DR33: Voice and vocabulary — calm, plain, honest: counts and verbs, no exclamation marks, no fear, no jargon in primary labels; definitive only when scoped to what was checked; identical words and numbers for leader, analyst and auditor. The plain-language glossary (EXPERIENCE "Glossary: plain label → technical term") replaces the locked glossary: the plain label comes first, with the technical term small and grey beside it, never removed. Pairs: Home (posture), Software (artifact), Issues (findings), Exposure (blast radius), Reports / Audit report (evidence packs; "Audit report for this answer" is the PDF answer report, listed under Exports — D3), Audit trail / History (evidence trail), Vulnerability (CVE), Actively exploited (KEV), Licence, Packages (SBOM components), Direct / Indirect, Deployed / Not deployed (running / shipped, not running), Copies, Where it runs, Fingerprint (image digest), Checked / Not checked yet, Check again, Data quality (data-quality score), Review / Review status (triage). Statuses: Not reviewed yet · Not impacted · Fix planned · Mitigated · Risk accepted (untriaged / not affected / fix planned / mitigated / accepted); Why? (justification). Exports, audit reports and VEX companions keep the technical terms. UI copy is British English ("Licences"). Retired labels never appear in the UI (UX-DR47). Domain, data and API names (artifact, finding, triage, posture, blast radius, evidence pack, KEV, EPSS, VEX, SBOM, `untriaged`) stay unchanged in code, API and docs. All strings are externalised from day 1 (no concatenation, no text in static SVG).⟧
Why: "locked glossary" and "lowercase triage statuses" are superseded.

**E58 · UX-DR34 · L218 (D2, D4, D11)**
OLD (line starts): ⟦- UX-DR34: Accessibility floor⟧
NEW: ⟦- UX-DR34: Accessibility floor — WCAG 2.2 AA in both themes (no separate high-contrast theme; confirm AA-only — EXPERIENCE Open item 25). (a) Full keyboard operability, with `Tab` order = reading order and a visible 2px focus ring on every interactive element (`focus`; lime on the sidebar and on forest selection); (b) field edges ≥ 3:1 at rest (`field-border`, 1.4.11); (c) reflow and resize (1.4.10, 1.4.4) through the icon rail and stacked layout (UX-DR35) — the Exposure map and wide tables may scroll in two directions while their header, answer and inspector reflow; (d) single-key shortcuts only outside text fields, with an off switch (2.1.4); (e) `aria-current` on selected rows, `aria-pressed` on segmented controls, `aria-current="location"` on the current trail step; (f) the surface is announced on navigation as title + summary; live changes via polite `aria-live` / `role="status"`, errors via `role="alert"`; (g) never colour alone — severity word + marker, exploited word + icon, status word + icon, deployed solid vs dashed plus a label, stale amber + clock + words, data quality always as printed score and letter with the weakest part named in words, and selection changes the text colour; (h) hover hints also available on focus; ⌘K is a real modal dialog (focus trapped, returned on `Esc`); (i) `prefers-reduced-motion` turns all motion off (0.16 s transitions, skeleton pulse, the map's centre-ring scale-in) and progress updates in steps; every graph is fully readable as a table.⟧
Why: new reflow, 2.1.4, 1.4.11, trail and DQ rules; High Signal's role is gone.

**E59 · UX-DR35 · L219 (D11)**
OLD (line starts): ⟦- UX-DR35: Responsive/platform⟧
NEW: ⟦- UX-DR35: Responsive/platform — ≥ 1440px is the designed layout; at 1280–1439px the three columns stay and the detail column absorbs the loss; at 1024–1279px the sidebar becomes an **icon rail** (icons only, labels as tooltips on hover and focus and as accessible names, search as a ⌘K icon button, the user menu as the avatar) with list and detail side by side; below 1024px the icon rail stays and list and detail **stack in one column** with a **Back** link (`forest-ink`) that returns to the same place and selection, at the same URL, fully operable (this covers 400% zoom at 1280px and 200% text). No other breakpoints. Web only, last-2-versions evergreen browsers; fonts self-hosted.⟧
Why: best-effort read-only becomes a fully operable stacked layout (memlog 88).

**E60 · UX-DR36 · L220 (D2, D4, D11)**
OLD (line starts): ⟦- UX-DR36: Banned patterns⟧
NEW: ⟦- UX-DR36: Banned patterns (enforced across all surfaces) — no in-product notifications or toasts (as alerts or for save results); no badge counts for *new* findings (the Issues Needs-attention badge, UX-DR38, counts what needs a decision and is allowed); no OIDC wizard; no evidence edit/delete (including stored exports); no infinite scroll; no modal deeper than one (the ⌘K dialog is the only modal; no drawers); no hover-only affordances; no celebratory animation; no second lime action in a view (one primary per view plus the active nav item and the agreed lime exceptions; while an error band shows, its recovery action is the one lime button); no red, red fills or severity-coloured backgrounds; no status-coloured chips; no combined risk or EPSS rating; no Compact density or density toggle; no eyebrows, kickers or tracked-caps labels; no nested cards or shadows on in-page elements; no type sizes outside the nine plus the wordmark; no opacity on elements with text except disabled controls at 0.45; no dedicated licence dashboard; no data-quality grade in list rows and no big data-quality numeral in the app; no separate graph-explorer screen.⟧
Why: "drawer + dialog" and "one primary button per surface" are superseded; new bans are added.

**E61 · new UX-DR37–UX-DR48 · after UX-DR36 (L220)**
OLD (anchor, kept): the UX-DR36 line as rewritten by E60.
NEW: ⟦- UX-DR37: Three-column master-detail — sidebar · list column (`paper`: page title, summary line, filters, grouped list with counts in group headings, pager, then the view's one primary action) · tabbed detail column (`canvas`: 64px tabs with counts, the active tab a forest block, position and keys at the bar's end "1 of 3 · J K"; a grid of cells divided by 1px rules, never cards). **One list-row shape everywhere:** line 1 is name + version (version in `text-3`); line 2 is severity · actively exploited · where; one right column. Click or `J`/`K` selects and fills the detail, and the list keeps its place. Groups too long for the page end in an "N more …" row; 25 per page; never infinite scroll. Segmented controls use one style everywhere. Exposure is the exception: a full-width header spans the list and detail columns.
- UX-DR38: Needs attention and the Issues badge — an issue needs attention when it is Not reviewed yet (in any place) AND it is Actively exploited OR Critical; every licence **violation** issue that is Not reviewed yet also needs attention; licence **warnings** never do (D8). A Mixed issue stays until none of its places is Not reviewed yet. The same number appears on Home ("Needs attention N"), in the Issues summary and as the Issues nav badge (`nav-badge`, lime count on `ink-2`); no badge at 0. The badge is a count of what needs a decision, not a new-findings notification. The order within Home's Needs attention is not decided (EXPERIENCE Open item 21).
- UX-DR39: Issue unit and Mixed — one Issues row is one vulnerability (or one licence) in one package version across every place it affects ("14 places"). Counts on every surface (not reviewed yet, open, the badge) count issues, not places. When an issue's places have different statuses, its chip reads **Mixed · N of M** (layers icon, neutral; N = places that differ from the issue-wide status; accessible name "Mixed: 3 of 14 places have a different status"). The Review status filter matches an issue when any of its places has that status, so a Mixed issue can appear under more than one status ([ASSUMPTION], Open item 9). VEX states each product's own status. Chips reflect the latest recorded decision per place.
- UX-DR40: Exposure query states — **no query** (`/exposure` from the sidebar): "Ask about a vulnerability, a package or a fingerprint." with examples ("CVE-2026-23012 · log4j-core@2.17.0 · sha256:…"), and the query button opens ⌘K. **Unknown vulnerability** (no data for the queried ID): "Armoury has no data for <ID> yet. Vulnerability data updated <age> ago." with lime **Check again** (re-asks against the latest vulnerability data; no rescan); no map, no zero, never "No software has it". **Known vulnerability, no matches:** the coverage-scoped zero ("No software has it — across the 3,176 pieces of software we've checked (82%)"), with the unchecked remainder one click away. Copy for an unknown `package@version` or fingerprint is not written (Open item 29).
- UX-DR41: Inline error — a failed save or start (review panel, Export, Generate audit report, Check again, Settings panels) shows one line in that panel, full width: `clay-wash` fill, a `clay` alert icon, a message in plain words ("Your decision wasn't saved: Armoury can't reach its database."), optional detail in `text-2`, and a grey small **Try again**. Nothing advances or closes; every entered value (choices, scope, "Why?") stays. Announced with `role="alert"`; cleared on a successful retry; never a toast; no border, shadow or red.
- UX-DR42: Code block — a copyable command or one-liner (setup `helm install`, agent install, `cosign verify-blob`, Prometheus endpoint, a CI token shown once, fingerprint): `paper` fill, Plex Mono 12px, and a grey small **Copy** that copies the whole command, never a truncated one. The label changes to "Copied" for 2 s and is announced politely; Copy is keyboard reachable and the text is selectable; long commands scroll horizontally and are never cut off.
- UX-DR43: User menu — at the sidebar foot: a 40px round avatar (`forest-3` → `forest` gradient, `on-forest` initials), the name in `on-ink`, the role in `side-muted`. It opens a `DropdownMenu` with the name and role, **Personal settings** (Settings → Personal) and **Sign out**. `Enter`/`Space` opens it, arrows move, and `Esc` closes it and returns focus. On the icon rail only the avatar shows.
- UX-DR44: Help — the Help item sits in the sidebar below the divider (UX-DR5). The Help screen is not designed and is deferred to a later UX update (EXPERIENCE Open item 24; the `?` shortcut map may belong there). No story invents Help content; until that update the item opens a placeholder that says Help is coming (copy to confirm with UX — O17).
- UX-DR45: Zero and empty states — **All clear** (Home): "Nothing needs you today." with the scope sentence ("That covers the 3,176 pieces of software we've checked; 671 are still waiting their turn."), three stats (0 Need attention · N Open, all reviewed · N% Checked), the severity line, grey See open issues, lime Audit report, a `lime-wash` sprout disc, and no Issues badge. **Nothing to review** (Issues filter at 0): "No issues are waiting for review." plus the coverage scope and grey **Show all statuses**. **Search no match:** "No issues match “<text>” with these filters." with grey **Clear search**, keeping the filters. **Reports, nothing yet:** "No audit reports yet" with lime Generate audit report; Exports: "No exports yet. Make one from Exposure, Issues or Software with Export." **Licences 0:** the group is hidden, and the type filter still shows "Licences 0".
- UX-DR46: Printed report (audit report PDF via Typst, the answer report and printed exports) — a print-only light palette (`print-*` tokens) independent of the app theme; IBM Plex Sans text ([ASSUMPTION], EXPERIENCE Open item 5) and IBM Plex Mono for every ID, fingerprint and command; body 9.5pt, tables 8.5pt; A4 by default with US Letter as an option. The audit report's cover sheet comes first and states coverage ("Covers 3,176 of 3,847 (82%)"), listing the not-checked software; then the **data-quality block** (`print-cover-dq`: "84 B+" at 30px with the letter at 20px in `print-dq` — the only big data-quality numeral anywhere; the five parts with plain names and the technical term beside each; "Lowest part: …"); then Signature (operator key and the `cosign verify-blob` line) and a sign-off line (name and role, date). Every page has a footer with report ID, time window, generation time and page number. Severity always shows as word + 4-step marker, with no red. Long tables repeat their header row. Plain labels carry the technical term beside them; the companions (SBOM, VEX) keep technical names. Preview is available in the product before download.
- UX-DR47: Retired UI labels — these never appear in UI strings: Posture, Findings, Blast radius, Graph explorer, Artifacts, Evidence, triage, Things to look at, Where it's affected, Weakness, ingredients, What's inside, Chosen by your team, Came along with them, Running (as a group or status label; the hint "Not seen running…" is allowed — EXPERIENCE Open item 35), Shipped not running, Undeployed, Being attacked in the wild, chance of attack, Doesn't affect us, Fixed for now, Workaround in place, Mark reviewed, Plan the fix, Skip. They are checked against the externalised message catalogue; code, API and docs may keep the domain terms (UX-DR33).
- UX-DR48: CI-scan landing (FR31) — the link the CI step prints opens that piece of software in Software. Not decided (EXPERIENCE Open item 28): how CI-submitted software that is in no connected registry is grouped (it fits neither Deployed nor Not deployed), the label that says where it came from, and where the CI verdict and its history show in Software detail. Resolve with a UX update before the Epic 11 UI work; CI policy and CI tokens live in Settings → Policy and Settings → Access (UX-DR28).⟧
Why: new layout, rules, states and components not covered by any existing UX-DR.

#### FR Coverage Map

**E62 · L236 (D1)**
OLD: ⟦FR13: Epic 5 - Deterministic, explainable KEV-first/EPSS ranking⟧
NEW: ⟦FR13: Epic 5 - Deterministic, explainable ordering: severity groups (Licences first), actively exploited (KEV) first in each, EPSS next, stated in words⟧
Why: D1.

**E63 · L239**
OLD: ⟦FR16: Epic 2 - Fleet posture view (extended by Epics 5, 8)⟧
NEW: ⟦FR16: Epic 2 - Fleet posture view (UI: Home; extended by Epics 5, 8)⟧
Why: adds the UI label.

**E64 · L240**
OLD: ⟦FR17: Epic 6 - Blast-radius query with provenance⟧
NEW: ⟦FR17: Epic 6 - Blast-radius query with provenance (UI: Exposure, including moving the map)⟧
Why: UI label; D4.

**E65 · L241 (D10)**
OLD: ⟦FR18: Epic 2 - Artifact detail (extended by Epics 3, 5, 7, 8)⟧
NEW: ⟦FR18: Epic 2 - Artifact detail (UI: Software detail; extended by Epics 3, 4, 5, 7, 8)⟧
Why: Epic 4 now adds Signed and end-of-life (4.9, 4.10).

**E66 · L242 (D3)**
OLD: ⟦FR19: Epic 6 - Shareable answers (report/CSV export)⟧
NEW: ⟦FR19: Epic 6 - Shareable answers (CSV/JSON export from Exposure, Issues and Software, the PDF answer report; all stored as evidence in Reports → Exports)⟧
Why: D3.

**E67 · L253 (D2)**
OLD: ⟦FR30: Epic 8 - Data-quality score⟧
NEW: ⟦FR30: Epic 8 (score, Software detail) + Epic 9 (audit report detail, cover page) - Data-quality score⟧
Why: D2 — the Reports and cover placements are built in Epic 9.

**E68 · new rows · after L254 (D10)**
OLD (anchor, kept): ⟦FR31: Epic 11 - Optional CI scan with server-side evaluation and result URL⟧
NEW: ⟦FR32: Epic 4 - Artifact signature verification against trusted signers (UI: Software detail "Signed")
FR33: Epic 4 - End-of-life data for packages (UI: Software detail Packages)⟧
Why: the two new FRs.

#### Epic List

**E69 · Epic 1 summary · L263 (D11)**
OLD: ⟦and lands in the themed shell — rail, command palette, three themes — on an empty Posture page offering the two setup actions.⟧
NEW: ⟦and lands in the Armoury shell — labelled black sidebar, ⌘K command palette, Light (default) and Dark themes — on an empty Home page offering the two setup actions.⟧
Why: the rail, three themes and Posture are gone.

**E70 · Epic 1 coverage · L264**
OLD: ⟦UX-DR1–7, UX-DR29, UX-DR31–36.⟧
NEW: ⟦UX-DR1–7, UX-DR29, UX-DR31–37, UX-DR41–44, UX-DR47.⟧
Why: assigns the new shell-level items.

**E71 · Epic 2 summary · L267**
OLD: ⟦while Posture and Artifacts populate live with gaps shown openly (minute 29, registry-side)⟧
NEW: ⟦while Home and Software fill in live under the Checking band, with gaps shown openly as "Not checked yet" rows (minute 29, registry-side)⟧
Why: retired labels. The Epic 2 title keeps "posture view" (a domain term).

**E72 · Epic 2 coverage · L268**
OLD: ⟦ARCH31, ARCH32, ARCH35.⟧
NEW: ⟦ARCH31, ARCH32, ARCH35, ARCH38 (Needs attention count); UX-DR9, UX-DR12, UX-DR13, UX-DR15, UX-DR22, UX-DR25, UX-DR38.⟧
Why: these items are cited by Epic 2 stories.

**E73 · Epic 3 summary · L271 and Epic 3 intro L980 (both occurrences)**
OLD: ⟦running workloads appear linked to registry artifacts so "is this running anywhere?" is answerable;⟧
NEW: ⟦running workloads appear linked to registry artifacts, so Software splits into Deployed and Not deployed and "is this running anywhere?" is answerable;⟧
Why: the new UI grouping; "artifacts" stays as a data term. Apply to both lines (the Epic 3 intro repeats the summary).

**E74 · Epic 4 summary and coverage · L275–276 (D10)**
OLD: ⟦and every finding carries source-attributed KEV, EPSS, CNA and OSV data.
**FRs covered:** FR7, FR8 (feed versions), FR10, FR11, FR12 — NFR4, NFR5; ARCH6, ARCH19–21, ARCH28 (R2).⟧
NEW: ⟦and every finding carries source-attributed KEV, EPSS, CNA and OSV data. Packages carry attributed end-of-life data, and registry artifacts are checked against trusted signers — both connected or air-gapped.
**FRs covered:** FR7, FR8 (feed versions), FR10, FR11, FR12, FR32, FR33 — NFR4, NFR5, NFR12; ARCH6, ARCH19–21, ARCH28 (R2), ARCH40, ARCH41; UX-DR15, UX-DR25 (Signed, end-of-life lines), UX-DR28 (Sources, Policy).⟧
Why: Stories 4.9 and 4.10. (The Epic 4 intro L1144 repeats the first sentence; S64 edits the intro.)

**E75 · Epic 5 summary · L279 (D1, D6, D9)**
OLD: ⟦The analyst works a KEV-first, EPSS-weighted findings list that explains each ranking, records justified decisions that propagate everywhere, and ingests and emits VEX.⟧
NEW: ⟦The analyst works the Issues list — Licences (hidden at 0), then Critical, High, Medium and Low, actively exploited first in each group, the order stated in words — and reviews each issue in the detail-column review panel (two questions; scope All N places or Only this software; a reason where required). Decisions are recorded with author and time, propagate everywhere and feed Home's Needs attention and the Issues badge; the fleet-wide audit trail is readable in Reports; Armoury ingests and emits VEX.⟧
Why: D1, the review panel, D9.

**E76 · Epic 5 coverage · L280**
OLD: ⟦UX-DR11, UX-DR16, UX-DR26, UX-DR27;⟧
NEW: ⟦UX-DR11, UX-DR16, UX-DR26, UX-DR27 (Audit trail group, per-item tabs), UX-DR38, UX-DR39, UX-DR45 (All clear, Nothing to review, Search no match); ARCH38;⟧
Why: new items.

**E77 · Epic 6 summary · L283 (D3, D4)**
OLD: ⟦On CVE day the engineer types a CVE ID or `package@version` into ⌘K and within seconds sees affected artifacts, shipped and running, and where they run — as graph or table with a provenance footer — exports it, and explores further in the graph.⟧
NEW: ⟦On CVE day the engineer types a CVE ID, `package@version` or fingerprint into ⌘K, and within seconds Exposure answers in words — which software has it, deployed and not deployed, and where it runs — then as a map or a table with its caveat line and "How we know". She exports it (stored as evidence in Reports → Exports) and moves the map to any node to follow it further. The Epic 6 title keeps its domain wording.⟧
Why: Exposure wording, D3 and D4.

**E78 · Epic 6 coverage · L284**
OLD: ⟦UX-DR17, UX-DR18, UX-DR21, UX-DR23, UX-DR24;⟧
NEW: ⟦UX-DR17, UX-DR18, UX-DR21, UX-DR23, UX-DR24, UX-DR40, UX-DR45 (Exports nothing yet), UX-DR46 (renderer); ARCH39;⟧
Why: new items.

**E79 · Epic 7 summary · L287 (D8)**
OLD: ⟦violations appear as neutral license findings in the same views and are triaged with the same decision model.⟧
NEW: ⟦violations and warnings appear as neutral Licence issues — the Licences group at the top of Issues and of Home's Open issues (hidden at 0), with a "Licence" kind tag (and the word "Warning" for warnings), and in a software's Packages and Issues — and are reviewed with the same decision model; only violations count toward Needs attention (licence review copy not yet drawn — EXPERIENCE Open item 16).⟧
Why: the Licences placement and D8.

**E80 · Epic 7 coverage · L288**
OLD: ⟦**FRs covered:** FR26, FR27.⟧
NEW: ⟦**FRs covered:** FR26, FR27; UX-DR9 (licence marker, "Warning"), UX-DR11 (Licences group), UX-DR38 (violations only).⟧
Why: the licence UI now has explicit UX-DRs.

**E81 · Epic 8 summary · L291 (D2)**
OLD: ⟦every answer carries an explainable data-quality score.⟧
NEW: ⟦every piece of software and the fleet get an explainable data-quality score, shown in Software detail (Epic 8) and in audit reports (Epic 9); not on Home and not in list rows.⟧
Why: D2.

**E82 · Epic 8 coverage · L292**
OLD: ⟦UX-DR10;⟧
NEW: ⟦UX-DR10, UX-DR28 (Signals panel), UX-DR42 (endpoint copy);⟧
Why: D2 plus the code block.

**E83 · Epic 9 summary · L295 (D2)**
OLD: ⟦The compliance lead generates a CRA pack in one click for any past window — PDF plus SBOM/VEX companions, stating its own coverage and data quality,⟧
NEW: ⟦The compliance lead generates a CRA pack (an "audit report" in the UI) in one click from Reports for any past window — PDF plus package lists (SBOM) and review decisions (VEX), with its own coverage stated first and its data quality second, on screen and on the cover page,⟧
Why: the UI label; D2. The epic title keeps "evidence packs".

**E84 · Epic 9 coverage · L296 (D2, D9)**
OLD: ⟦UX-DR19, UX-DR20.⟧
NEW: ⟦UX-DR10 (Reports row, cover), UX-DR19, UX-DR20, UX-DR27 (Audit reports; checkpoint and anchoring status in the Audit trail group), UX-DR42, UX-DR45 (Reports nothing yet), UX-DR46.⟧
Why: new items.

**E85 · Epic 11 summary · L303 and Epic 11 intro L2357 (both occurrences)**
OLD: ⟦the step prints the verdict and a link to the artifact.⟧
NEW: ⟦the step prints the verdict and a link to the artifact (that piece of software in Software; its grouping and verdict display are open — UX-DR48).⟧
Why: the FR31 landing gap. Apply to both lines (the Epic 11 intro repeats the sentence).

**E86 · Epic 11 coverage · L304**
OLD: ⟦ARCH31, ARCH33, ARCH36.⟧
NEW: ⟦ARCH31, ARCH33, ARCH36; UX-DR28 (CI policy, CI tokens), UX-DR42, UX-DR48.⟧
Why: new items.

### 4.4 Epics — stories

<!-- file: _bmad-output/planning-artifacts/epics.md -->

#### Story title changes (numbers never change)

| Story | Linear | Old title | New title | Decision |
|---|---|---|---|---|
| 1.5 (L475) | INF-27 | Design tokens and the three themes | Design tokens and the Light and Dark themes | D11 |
| 1.6 (L499) | INF-28 | App shell, navigation and the empty Posture page | App shell, sidebar navigation and the empty Home page | D11 |
| 2.9 (L858) | INF-39 | Posture summary — populating, coverage and freshness | Home summary — checking, coverage and freshness | D11 |
| 2.10 (L889) | INF-40 | Posture findings — severity band and findings table | Home — Needs attention and open issues by severity | D1, D8 |
| 2.11 (L910) | INF-41 | Artifacts list and artifact detail | Software list and software detail | D10 |
| 3.6 (L1121) | INF-49 | Runtime coverage on Posture, and minute 29 with the agent | Runtime coverage on Home and Software, and minute 29 with the agent | D11 |
| 4.7 (L1310) | INF-56 | Honest feed staleness across Posture and findings | Honest feed staleness across Home and Issues | D11 |
| 5.1 (L1363) | INF-58 | Deterministic, explainable ranking | Deterministic, explainable issue order | D1 |
| 5.2 (L1392) | INF-59 | Findings workbench and ranked Posture table | Issues list — severity groups, filters and the Home summary | D1 |
| 5.4 (L1448) | INF-61 | Triage drawer | Review panel in the Issues detail column | D7, D11 |
| 5.5 (L1473) | INF-62 | Evidence trail surface | Audit trail in Reports and on every item | D9 |
| 5.6 (L1497) | INF-63 | Emit VEX from triage decisions | Emit VEX from review decisions | D7 |
| 5.8 (L1551) | INF-98 | Fleet-wide triage decisions | Review scope — all places or only this software | D6 |
| 6.3 (L1634) | INF-67 | Blast-radius surface — answer and table, from ⌘K | Exposure surface — answer and table, from ⌘K | D11 |
| 6.4 (L1663) | INF-68 | Blast-radius graph reading | Exposure map reading | D11 |
| 6.5 (L1688) | INF-69 | Export blast-radius and posture answers | Export views as stored evidence, and the answer report | D3 |
| 6.6 (L1711) | INF-70 | Graph explorer and node inspector | Exposure map traversal and inspector | D4 |
| 7.4 (L1841) | INF-75 | License findings in Posture, Findings and triage | Licence issues in Home, Issues and review | D8 |
| 8.2 (L1906) | INF-77 | Fleet data quality on Posture and Artifacts | Fleet data-quality score and the Software detail meter | D2 |
| 8.4 (L1969) | INF-79 | Prometheus panel in Settings | Prometheus panel in Settings → Signals | D11 |
| 9.5 (L2102) | INF-84 | Generate packs and verify signatures in the UI | Generate audit reports and verify signatures in Reports | D9, D11 |

New stories: **4.9 End-of-life data for packages** (FR33) and **4.10 Verify artifact signatures
against trusted signers** (FR32). Unchanged on purpose (domain or API terms): Epic titles 1–11 and
Stories 1.1–1.4, 2.1, 2.12, 3.5, 6.1, 6.2, 6.7, 9.1–9.4, 9.6–9.9, 10.x, 11.x.

Each title edit below replaces the `### Story N.M:` heading text only.

#### Epic 1 — intro and Stories 1.5–1.9

**S1 · Epic 1 intro · L308 (D11)**
OLD: ⟦lands in the themed shell — rail, command palette, three themes — on an empty Posture page. Story 1.1⟧
NEW: ⟦lands in the Armoury shell — labelled black sidebar, command palette, Light and Dark themes — on an empty Home page. Story 1.1⟧
Why: same as E69.

**S2 · Story 1.5 title · L475**
OLD: ⟦### Story 1.5: Design tokens and the three themes⟧
NEW: ⟦### Story 1.5: Design tokens and the Light and Dark themes⟧
Why: two themes.

**S3 · Story 1.5 user story · L478–479**
OLD: ⟦I want the Forge, High Signal and Gunmetal themes with Armoury's typography,
So that the product looks like itself from the first screen and I can pick a high-contrast option.⟧
NEW: ⟦I want the Light (default) and Dark themes with Armoury's typography (IBM Plex Sans and IBM Plex Mono),
So that the product looks calm and like itself from the first screen, in either theme.⟧
Why: High Signal is dropped; AA-only still needs confirming (EXPERIENCE Open item 25).

**S4 · Story 1.5 AC · L485**
OLD: ⟦with the exact DESIGN.md values for all three themes, including `rail-*` and `data-quality` (UX-DR1)⟧
NEW: ⟦with the exact DESIGN.md values for Light (unsuffixed keys) and Dark (`-dark` keys), following the DESIGN.md "shadcn mapping" table — including the sidebar (`ink`, `ink-2`, `ink-line`, `side-text`, `side-muted`, `on-ink`), `lime*`, `forest*`, the severity roles (`clay`, `amber`, `slate`, `forest-ink`) and `field-border` — plus `--paper`, `--dq`, `--dq-muted` and `--dq-wash` as extra variables; the `print-*` tokens feed only the Typst template (UX-DR1)⟧
Why: the old tokens are gone (checked against the new DESIGN.md frontmatter).

**S5 · Story 1.5 AC · L490**
OLD: ⟦Inter Display, Inter and IBM Plex Mono are bundled locally (no CDN; works air-gapped), sizes match DESIGN.md exactly, and numerals use `tabular-nums` (UX-DR2, UX-DR3, NFR4)⟧
NEW: ⟦IBM Plex Sans (variable 100–700), IBM Plex Sans Bold Italic (wordmark only) and IBM Plex Mono 400 (IDs, fingerprints, commands, keys only) are bundled locally (SIL OFL 1.1, no CDN; works air-gapped); only the nine sizes 12 · 13 · 14 · 15 · 17 · 20 · 24 · 30 · 40 are used, plus the 22px wordmark as the single exception; weights are 400 / 500 / 600; numerals use `tabular-nums` in every data role; a lint fails on any other size or a third family (UX-DR2, UX-DR3, NFR4)⟧
Why: Inter is dropped; new type scale.

**S6 · Story 1.5 AC · L491**
OLD: ⟦**And** radii, zone gaps, rail width, data-row height and stat gap match DESIGN.md.⟧
NEW: ⟦**And** radii (xs 3, sm 4, md 6, lg 10, pill, full) and the layout tokens (sidebar 252, list column 376 / 500 / 420, list gutter 32, detail cell 30 × 34, row padding 17 / 14 / 12, nav item 54, tab 64, button 42 / 32 / 54, field 42, query 44, pager 32) match DESIGN.md; there is one density only.⟧
Why: the rail, zone-gap and data-row tokens are gone.

**S7 · Story 1.5 AC · L495**
OLD: ⟦new users get Forge; no OS-preference detection (UX-DR4); the picker that sets it arrives in Story 1.6⟧
NEW: ⟦new users get Light; no OS-preference detection ([ASSUMPTION], EXPERIENCE Open item 3) (UX-DR4); the same preferences also hold the single-key shortcut switch (Story 1.8); the picker arrives in Story 1.6⟧
Why: the new default; the shortcut switch persists here.

**S8 · Story 1.5 AC · L496 (D2)**
OLD: ⟦an automated contrast check confirms AA (4.5:1) for all text roles in Forge and Gunmetal, including `data-quality-muted` and `text-muted`, 3:1 for `node-inactive-border`, the AAA target for High Signal primary text and ≥7:1 for High Signal `text-muted`; it also checks `data-quality-muted` at 4.5:1 and `node-inactive-border` at 3:1 in all three themes⟧
NEW: ⟦an automated contrast check confirms AA (4.5:1) for every text pair in the DESIGN.md Contrast table in Light and Dark (lowest 4.9:1), including the selection pairs on `forest`, text on `lime`, and `dq` / `dq-muted` on canvas, paper, chip and `dq-wash`, and ≥3:1 for `field-border` against canvas, paper and chip and for the focus ring; markers below 3:1 (`amber-dot`, `slate-dot`, the dark `forest` fill) are allowed only beside a word⟧
Why: the old themes and tokens are gone; the data-quality roles are new.

**S9 · Story 1.5 AC · L497**
OLD: ⟦a lint/test fails if a component applies opacity below 1 to an element that contains text; quieter states use the muted tokens (DESIGN.md).⟧
NEW: ⟦a lint/test fails if a component applies opacity below 1 to an element that contains text, except disabled controls at 0.45 (DESIGN.md); quieter states use `text-2` / `text-3`, and low data-quality grades use `dq-muted`.⟧
Why: the 0.45 disabled exception; there are no "muted tokens" any more.

**S10 · Story 1.6 title · L499**
OLD: ⟦### Story 1.6: App shell, navigation and the empty Posture page⟧
NEW: ⟦### Story 1.6: App shell, sidebar navigation and the empty Home page⟧
Why: rename.

**S11 · Story 1.6 user story · L502**
OLD: ⟦I want a consistent shell with the icon rail and an honest empty Posture page,⟧
NEW: ⟦I want a consistent shell with a labelled sidebar and an honest empty Home page,⟧
Why: the rail is retired.

**S12 · Story 1.6 AC · L509**
OLD: ⟦a 58px icon rail shows the seven surfaces (Posture, Blast radius, Graph explorer, Artifacts, Findings, Evidence, Settings pinned bottom), with the active item mirroring the route, tooltips on hover and focus, and no top nav (UX-DR5)⟧
NEW: ⟦a 252px black sidebar shows the wordmark, the "Search or jump to… ⌘K" field, the nav Home · Software · Issues · Exposure · Reports, a divider, then Settings · Help (20px icon + label, 54px items), with the active item lime (ink text, weight 600) mirroring the route, and the user menu at the foot; there is no top nav and no page header (UX-DR5, UX-DR43)⟧
Why: new IA and sidebar.

**S13 · Story 1.6 AC · L510**
OLD: ⟦surfaces without content yet render the left-aligned heading block (eyebrow → title → subtitle → accent rule) and a calm "nothing here yet" line — no illustrations⟧
NEW: ⟦every surface uses the three-column master-detail layout (sidebar · list column · tabbed detail column) with the page title equal to the sidebar label and one summary line under it (UX-DR37); surfaces without content yet show a calm "nothing here yet" line — no eyebrow, heading block, accent rule or illustration⟧
Why: the heading block and eyebrows are banned.

**S14 · Story 1.6 AC · L511**
OLD: ⟦**And** every surface has the page header row: breadcrumb, the search field ("Blast radius — CVE, package, or digest", `⌘K` hint) and the compact theme switcher (swatch + name) (UX-DR4, UX-DR5, DESIGN.md Page header).⟧
NEW: ⟦**And** the user menu shows the signed-in name and role and opens Personal settings (Settings → Personal) and Sign out (Story 1.3); `Enter`/`Space` opens it, arrows move, and `Esc` closes it and returns focus; Help opens a placeholder until its screen is designed (EXPERIENCE Open item 24, O17) (UX-DR4, UX-DR5, UX-DR43, UX-DR44).⟧
Why: the page header and the header theme switcher are gone; user menu and Help are new.

**S15 · Story 1.6 AC · L514–515**
OLD: ⟦**When** Posture loads
**Then** it shows the pre-setup heading block and states that no sources are connected yet⟧
NEW: ⟦**When** Home loads
**Then** it shows the title "Home" and states that no sources are connected yet⟧
Why: Home; no heading block.

**S16 · Story 1.6 AC · L519**
OLD: ⟦it shows an in-page left list of panels, grouped as Connections, Feeds, Policy, Access, Signals and Personal⟧
NEW: ⟦it shows a panel list in the list column, grouped as Connections, Sources, Policy, Access, Signals and Personal⟧
Why: Feeds → Sources; the panel list sits in the list column (EXPERIENCE Open item 6).

**S17 · Story 1.6 AC · L520**
OLD: ⟦this story fills the theme picker (choosing a theme applies it instantly and persists it, Story 1.5), the read-only resolved auth configuration, the users/roles view and the keyboard shortcut list placeholder⟧
NEW: ⟦this story fills Settings → Personal (the Light / Dark theme switch, which applies instantly and persists, Story 1.5; the keyboard shortcut list and the switch that turns single-key shortcuts off, wired in Story 1.8) and Settings → Access (the read-only resolved auth configuration and the users/roles view)⟧
Why: new panel contents.

**S18 · Story 1.7 AC · L549**
OLD: ⟦and no affordance is hover-only (UX-DR34, UX-DR36).⟧
NEW: ⟦and no affordance is hover-only; selected rows use `aria-current`, segmented controls use `aria-pressed`, and field edges meet 3:1 at rest (UX-DR34, UX-DR36).⟧
Why: new accessibility floor items.

**S19 · Story 1.7 AC · L553**
OLD: ⟦a polite `aria-live` region announces the surface name.⟧
NEW: ⟦a polite `aria-live` region announces the surface by title and summary ("Issues — 3 need attention today").⟧
Why: EXPERIENCE Accessibility Floor.

**S20 · Story 1.7 AC · L557**
OLD: ⟦via one shared motion setting rather than per-component checks.⟧
NEW: ⟦via one shared motion setting rather than per-component checks; normal motion is quiet (0.16 s colour and background transitions, skeleton pulse) and progress updates in steps when reduced.⟧
Why: the new motion rule.

**S21 · Story 1.7 AC · L562 (D11)**
OLD: ⟦**And** locked glossary terms and the lowercase triage status labels are defined once in the catalogue.⟧
NEW: ⟦**And** the plain-label glossary (EXPERIENCE Glossary) and the five review-status labels — Not reviewed yet, Not impacted, Fix planned, Mitigated, Risk accepted — are defined once in the catalogue; UI copy is British English ("Licences"); a lint/test fails on any retired label from UX-DR47, with "Running" banned only as a group or status label (EXPERIENCE Open item 35).⟧
Why: the locked glossary is replaced.

**S22 · Story 1.7 AC · L564–567 (D11)**
OLD: ⟦**Then** it shows the full layout, the tolerant layout (tighter gutters, horizontal scroll before columns drop), and a best-effort read-only layout respectively (UX-DR35)
**And** a Playwright test checks every shell route at 1440, 1100 and 900 px wide: the page has no horizontal scroll (only tables and graphs scroll inside their own area), and every control is visible and reachable by keyboard.⟧
NEW: ⟦**Then** it shows respectively: the full sidebar with three columns; the icon rail (icons only, labels as tooltips on hover and focus and as accessible names, the search field as a ⌘K icon button, the user menu as the avatar) with list and detail side by side; and the icon rail with list and detail stacked in one column, where opening an item shows its detail with a Back link that returns to the list at the same place and selection, at the same URL — every layout fully operable (UX-DR35)
**And** a Playwright test checks every shell route at 1440, 1100 and 900 px wide, at 320 CSS px (400% zoom at 1280) and with 200% text: there is no horizontal page scroll (only the Exposure map and wide tables scroll inside their own area), and every control is visible and reachable by keyboard.⟧
Why: the responsive rule (memlog 88) replaces "best-effort read-only".

**S23 · Story 1.8 AC · L579**
OLD: ⟦the shadcn `Command` palette opens with groups Answers → Navigate → Actions → Recent, `Enter` fires, `Esc` closes, and results announce via `aria-live` (UX-DR6)⟧
NEW: ⟦the shadcn `Command` palette opens as a 660px dialog with results grouped Issues · Software · Exposure · Actions (first result = best match); `↵` opens, `Esc` closes and returns focus; it traps focus, dims the page and never navigates on its own; results announce via polite `aria-live` (UX-DR6); a Recent group is not drawn (EXPERIENCE Open item 20)⟧
Why: new groups.

**S24 · Story 1.8 AC · L580**
OLD: ⟦**And** it offers navigation to every surface and "Switch theme…" with live preview⟧
NEW: ⟦**And** it offers navigation to every surface and "Switch theme…" (Light / Dark)⟧
Why: no live preview in the spine; two themes.

**S25 · Story 1.8 AC · L581**
OLD: ⟦**And** the page-header search field (Story 1.6) opens the same palette, pre-scoped to blast radius; until Story 6.3 adds answers, it shows the normal palette.⟧
NEW: ⟦**And** the sidebar "Search or jump to…" field (Story 1.6) opens the same palette; typing a CVE ID, `package@version` or fingerprint routes to an Exposure answer once Story 6.3 lands; until then it shows the normal palette.⟧
Why: no page header.

**S26 · Story 1.8 AC · L589**
OLD: ⟦**Then** the palette shows "No matches. Try a CVE ID, package@version, or digest."⟧
NEW: ⟦**Then** the palette shows "No matches. Try a CVE ID, package@version or fingerprint."⟧
Why: digest → fingerprint.

**S27 · Story 1.8 AC · L592–595 (D11)**
OLD: ⟦**When** the user presses `g`+`p/b/g/a/f/e`, `?` or `Esc`
**Then** they navigate, open the shortcut map, or close the topmost layer respectively, and the same map is listed in Settings (UX-DR7)
**And** shortcuts never fire while focus is in a text input.⟧
NEW: ⟦**When** the user presses `g` + a surface letter, `J`/`K`, `/`, `⌘↵`, `x`, `?` or `Esc`
**Then** they navigate (letters show beside each nav item after `G`), move through the list, focus the list search, save and go to the next issue, export, open the shortcut map, or close the topmost layer, and the same map is listed in Settings → Personal (UX-DR7)
**And** the `g` letters for the renamed surfaces and any new meanings for `t` and `e` are set in EXPERIENCE.md before this story starts Build (EXPERIENCE Open item 13)
**And** single-key shortcuts never fire while focus is in a text field, and a switch in Settings → Personal turns them off (persisted in `user_preferences`, WCAG 2.1.4); `⌘K` and `⌘↵` stay on.⟧
Why: the old letters map retired surfaces; a UX blocker is named.

**S28 · Story 1.9 AC · L607**
OLD: ⟦one shared overlay component allows at most a drawer plus one dialog, proven by a component test.⟧
NEW: ⟦one shared overlay component allows one modal — the ⌘K dialog — and no drawer or stacked modal, proven by a component test.⟧
Why: the drawer is gone.

**S29 · Story 1.9 AC · L611**
OLD: ⟦it confirms only a user's own action, never an alert for new findings, and a lint/test enforces this.⟧
NEW: ⟦it is never used — not as an alert, not for new findings and not for a failed save or start (failures use the inline error in the panel where the action was taken, UX-DR41) — and a lint/test enforces this.⟧
Why: the inline-error rule; toasts are banned (UX-DR36).

**S30 · Story 1.9 AC · L615 (D2, D11)**
OLD: ⟦a lint/test fails on more than one primary button per surface or on celebratory animation classes.⟧
NEW: ⟦a lint/test fails on more than one lime primary action per view (besides the active nav item; while an error band shows, its Try again is the one lime action and the list column's primary turns grey), on lime used outside its agreed jobs (active nav, the one primary action, selected map node, Issues badge, text selection), on a Compact density toggle, on a data-quality grade in a list row, or on celebratory animation classes.⟧
Why: the DESIGN lime rule, one density, D2.

#### Epic 2 — intro and Stories 2.2–2.13

**S31 · Epic 2 intro · L619 (D1)**
OLD: ⟦while Posture and Artifacts populate live with gaps shown openly. Ranking here is severity-only and labelled as such; Epic 5 replaces it with KEV-first/EPSS ranking.⟧
NEW: ⟦while Home and Software fill in live with gaps shown openly. Issues are grouped by severity from the start; Epic 5 settles the order within each group (D1).⟧
Why: severity groups replace the interim ranking.

**S32 · Story 2.2 AC · L686**
OLD: ⟦**Given** the empty Posture page or Settings → Registry connections⟧
NEW: ⟦**Given** the empty Home page or Settings → Connections (registries)⟧
Why: Settings panel names.

**S33 · Story 2.2 AC · L707**
OLD: ⟦they view Settings → Registry connections⟧
NEW: ⟦they view Settings → Connections (registries)⟧
Why: same.

**S34 · Story 2.6 AC · L796**
OLD: ⟦**Given** Settings → Package feeds⟧
NEW: ⟦**Given** Settings → Connections (package feeds)⟧
Why: same.

**S35 · Story 2.8 AC · L856**
OLD: ⟦("N OCI artifacts of unsupported type `<media type>`")⟧
NEW: ⟦("N pieces of software of a type we can't check yet", with `<media type>` small as the technical term — copy to confirm with UX)⟧
Why: plain label first.

**S36 · Story 2.9 title · L858**
OLD: ⟦### Story 2.9: Posture summary — populating, coverage and freshness⟧
NEW: ⟦### Story 2.9: Home summary — checking, coverage and freshness⟧
Why: rename.

**S37 · Story 2.9 user story · L861**
OLD: ⟦I want Posture to show what is known⟧
NEW: ⟦I want Home to show what is known⟧
Why: rename.

**S38 · Story 2.9 AC · L872–874 (D11)**
OLD: ⟦**When** Posture renders
**Then** it shows the heading block, one hero numeral with a co-stat band (artifacts, scanned coverage, findings), and a populating banner stating queue count and estimate, refreshed by polling the Posture summary about every 10 s while backlog exists, without blocking (UX-DR8, UX-DR13, NFR1, ARCH33)
**And** numerals count up on populate, stepped under reduced motion.⟧
NEW: ⟦**When** Home renders
**Then** it shows the title "Home" with one plain summary line and "Last checked N min ago", and the Checking band — determinate progress ("3,176 of 3,847 checked (82%)"), an estimate in words ("about 2 h left") and "You can keep working: numbers update as each one finishes." — refreshed by polling the Home summary about every 10 s while backlog exists; it never blocks and is never a spinner or a modal (UX-DR13, NFR1, ARCH33)
**And** the "Across all software" band shows Checked as a gauge with "N are waiting their turn"; skeletons appear only where data is missing; progress is a polite `role="status"` and updates in steps under reduced motion.⟧
Why: the hero numeral, co-stat band (UX-DR8 retired), populating banner and count-up are gone.

**S39 · Story 2.9 AC · L877–878**
OLD: ⟦**When** Posture renders
**Then** each appears as a named, non-dismissible coverage-gap row with counts and locations, linking to its cause (FR5, UX-DR12, NFR8).⟧
NEW: ⟦**When** Home and Software render
**Then** each appears as a plain gap row where the missing data would be ("Not checked yet N"), naming the count and where ("including 212 in prod-eu-west") and saying "Their issues are unknown, not absent."; it is not dismissible or collapsible and links to its cause (FR5, UX-DR12, NFR8).⟧
Why: the new coverage-gap row.

**S40 · Story 2.9 AC · L880–883**
OLD: ⟦**Given** the freshness strip
**When** Posture renders
**Then** it lists the Grype DB and SBOM index with version and age in mono, coloured by threshold, each linking to Settings (UX-DR15)
**And** the uniformity claim reads "All N artifacts SBOM'd and scanned the same way — Syft vX · Grype vY", where N is the scanned count, not the discovered count.⟧
NEW: ⟦**Given** the freshness strip
**When** Home renders
**Then** it lists each source in plain words with its age ("Vulnerability data 41 min ago · Packages 38 min ago"), with the technical term (Grype DB, SBOM index) small in `text-3`; a source past its threshold turns amber with its age in words and an amber dot; a "Sources" link at the end opens Settings → Sources (UX-DR15)
**And** the uniformity claim keeps its meaning in plain labels — "All N pieces of software checked the same way — Syft vX · Grype vY", where N is the checked count, not the discovered count; where it sits on Home is set by UX before Build (O18).⟧
Why: the new freshness strip; the spine no longer draws the uniformity claim on Home.

**S41 · Story 2.9 AC · L886–887**
OLD: ⟦**When** Posture renders
**Then** the empty state offers "Connect registry" with its Settings link (UX-DR29).⟧
NEW: ⟦**When** Home renders
**Then** it shows the title and the setup action "Connect a registry" with its copy-paste one-liner in a code block with Copy; no illustration (UX-DR29, UX-DR42; Story 3.2 adds the second action).⟧
Why: the empty Home state.

**S42 · Story 2.10 title · L889**
OLD: ⟦### Story 2.10: Posture findings — severity band and findings table⟧
NEW: ⟦### Story 2.10: Home — Needs attention and open issues by severity⟧
Why: the severity band and findings table are retired.

**S43 · Story 2.10 user story · L892–893**
OLD: ⟦I want to see the fleet's findings distributed by severity and listed densely,
So that I can see where the problems are across everything scanned.⟧
NEW: ⟦I want to see what needs attention today and the open issues by severity,
So that I can see where the problems are across everything checked.⟧
Why: dense listing is rejected (one calm density).

**S44 · Story 2.10 AC · L897–899 (D1, D6, D8)**
OLD: ⟦**When** Posture renders
**Then** a 30px soft severity band shows the distribution, labelled "scanned artifacts only", and clicking a segment filters the table below (UX-DR14).⟧
NEW: ⟦**When** Home renders
**Then** the list column shows **Needs attention N** — issues (one vulnerability or licence in one package version, across all its places; UX-DR39) that are Not reviewed yet in any place AND Actively exploited or Critical, plus every Not-reviewed-yet licence violation (never a licence warning, D8) — as standard rows (name + version · severity · Actively exploited · where; right column places, "14 places"), then **Open issues N** as summary rows: Licences first (hidden at 0), then Critical (with "N actively exploited"), High, Medium and Low with counts, then "N not reviewed yet · N reviewed · See all" (UX-DR22, UX-DR38)
**And** until Epic 4 loads the exploited list and Epic 5 records reviews, every issue is Not reviewed yet and none is marked Actively exploited; the rule is applied unchanged and computed on the server (ARCH38)
**And** the sidebar Issues item shows a badge with the Needs-attention count, and no badge at 0; it counts decisions due, never new findings.⟧
Why: Home IA, the Needs-attention rule (D8) and the badge.

**S45 · Story 2.10 AC · L901–904 (D6)**
OLD: ⟦**Given** the findings table
**When** it renders
**Then** it has 30px rows, mono identifiers (CVE, `package@version`, digest), severity chips with text, cursor pagination (no offset, no infinite scroll) and coverage-gap rows inline (UX-DR9 severity chip, UX-DR11 base, ARCH13)
**And** the header honestly states the current order: "Sorted by severity — KEV/EPSS ranking arrives with enrichment."⟧
NEW: ⟦**Given** the selected issue
**When** the detail column renders
**Then** it shows tabs Overview · Exposure · How to fix · Details; Overview holds the title, one plain sentence of what it means, severity as a word + 4-step marker (UX-DR9), Vulnerability (CVE ID in mono), Found in, The fix and Review status (Not reviewed yet until Epic 5); the Exposure tab arrives with Story 6.3, and How to fix and Details wait for UX (EXPERIENCE Open item 14)
**And** the findings API returns finding groups (ARCH38) with place counts and per-group counts, cursor-paginated with a total (ARCH13)
**And** the "Across all software" band adds Open issues (last 30 days, sparkline, delta chip such as "247 fewer") computed from history (ARCH32).⟧
Why: no findings table on Home; the issue unit.

**S46 · Story 2.10 AC · L906–908**
OLD: ⟦**Given** zero findings over partial coverage
**When** Posture renders
**Then** the zero is scoped: "0 critical findings across the N% of the fleet that is scanned."⟧
NEW: ⟦**Given** nothing that needs attention, over partial coverage
**When** Home renders
**Then** it reads "Nothing needs you today." with the scope sentence ("That covers the N pieces of software we've checked; M are still waiting their turn."), shows no Issues badge, and the view's one lime action follows EXPERIENCE (Review all N from Story 5.4; Audit report from Story 9.5) (UX-DR45).⟧
Why: the all-clear state.

**S47 · Story 2.11 title · L910**
OLD: ⟦### Story 2.11: Artifacts list and artifact detail⟧
NEW: ⟦### Story 2.11: Software list and software detail⟧
Why: rename.

**S48 · Story 2.11 user story · L913–914**
OLD: ⟦I want to open any artifact and see its SBOM, findings and how it was evaluated,
So that I can answer "what's in this and how do we know?" for a single artifact.⟧
NEW: ⟦I want to open any piece of software and see its packages, issues and how it was checked,
So that I can answer "what's in this and how do we know?" for one piece of software.⟧
Why: plain labels.

**S49 · Story 2.11 AC · L918–920**
OLD: ⟦**Given** the Artifacts surface
**When** it loads
**Then** a paginated list shows each artifact's identifier (mono), type (`image`, `package`, `oci_artifact` or `filesystem`), source (registry, package feed, CI scan or CI upload), SBOM/scan status and finding counts, with coverage-gap rows inline and a populating banner while backlog exists.⟧
NEW: ⟦**Given** the Software surface
**When** it loads
**Then** the list column shows "Software" and a summary line ("3,847 pieces of software."), standard rows (name + version; line 2 where it runs; right column the issue count "2 issues"; no data-quality grade), the "Not checked yet N" gap row in place, the pager "1–25 of N · page 1 of M" (25 per page, never infinite scroll) and the lime Add software (its destination is set by UX before Build, EXPERIENCE Open item 18); while backlog exists the Checking band shows, with per-row step text ("Reading packages · step 2 of 3", "Waiting its turn")
**And** until a cluster agent reports (Epic 3) the list is not split into Deployed / Not deployed; Story 3.5 adds the groups
**And** each piece of software keeps its type (`image`, `package`, `oci_artifact`, `filesystem`) and source (registry, package feed, CI scan, CI upload) in its detail; how CI-submitted software is grouped and labelled is EXPERIENCE Open item 28.⟧
Why: Software IA.

**S50 · Story 2.11 AC · L922–925 (D2, D10)**
OLD: ⟦**Then** it shows SBOM contents (packages and versions), vulnerability findings, evaluation provenance (last evaluated, Syft/Grype/DB versions) and a freshness strip (FR18, FR8, UX-DR25)
**And** the running-locations section honestly reads "No cluster agent connected — running locations unknown" until Epic 3 provides data.⟧
NEW: ⟦**Then** it shows tabs Overview · Issues · Packages · Audit trail; Overview, in the order of UX-DR25, holds **Info** — Name, Fingerprint (mono, Copy), Runs in, Copies, **Built** (the creation time the artifact records — for an image, the `created` time in its image config — or "Unknown"; copy to confirm), Last checked, Data quality (filled by Story 8.2; what it shows before a score exists is EXPERIENCE Open item 32) and **Signed** (filled by Story 4.10; until then it says the signature is not checked yet) — beside the Packages cell ("214 packages · SBOM", Direct / Indirect; the licence line arrives with Epic 7 and the end-of-life line with Story 4.9) over Where it runs; then Issues, the Issues trend and "Latest in the audit trail" ("Entries are never edited or removed"); provenance is inline ("Last checked", "How we know: Syft v… · Grype DB v…") instead of a freshness strip (FR18, FR8, UX-DR25)
**And** the Where it runs cell reads "No cluster agent connected — where it runs is unknown" until Epic 3 provides data.⟧
Why: the new detail layout; D10 fields and D2 placement with honest placeholders.

**S51 · Story 2.11 AC · L929, plus new ACs (D10)**
OLD: ⟦**Then** the failure reason and retry status are shown instead of an empty findings list.⟧
NEW: ⟦**Then** the failure reason and retry status are shown in place of the Issues cell, never as zero issues.

**Given** a connected registry that is unreachable
**When** Software renders
**Then** an edge-to-edge error band names it ("We can't reach registry.acme.internal") with since when, what it affects, what still works and the likely cause; the lime **Try again** is the view's one lime action and Add software turns grey; the grey **Open connection settings** opens Settings → Connections; affected rows say "As of 14:02 · registry" in amber with a clock; nothing is removed (FR5, NFR8, UX-DR29).

**Given** Software detail
**When** a user presses the grey **Check again**
**Then** the SBOM and the scan of that one piece of software are queued again at once, through the same pipeline and fleet toolchain (NFR12); the row and the detail show step text until done ("Reading packages · step 2 of 3"); the request is appended to the evidence ledger with who and when; and a failure to start shows the inline error with Try again (FR18, UX-DR41, D10)
**And** the operation declares its minimum role with `x-armoury-role` in `openapi.yaml` (the role is chosen when the story is planned — O4), and Check again is absent for roles below it (UX-DR31).⟧
Why: the registry-unreachable state and D10 "Check again".

**S52 · Story 2.12 AC · L941**
OLD: ⟦Posture is live and visibly populating (populating banner, coverage co-stat, coverage-gap rows)⟧
NEW: ⟦Home and Software are live and visibly checking (Checking band, Checked gauge, "Not checked yet" rows)⟧
Why: retired components.

**S53 · Story 2.13 AC · L968**
OLD: ⟦the populating banner's estimate⟧
NEW: ⟦the Checking band's estimate⟧
Why: rename. (L966–967 keep the API names; "findings page (50 rows)" stays as a stricter bound than the UI page of 25.)

#### Epic 3 — Stories 3.1–3.6

**S54 · Story 3.1 AC · L999**
OLD: ⟦**Given** Settings → Agent install (admin only)⟧
NEW: ⟦**Given** Settings → Connections (agent install, admin only)⟧
Why: panel names.

**S55 · Story 3.2 AC · L1047**
OLD: ⟦**Given** Settings → Agent install
**When**⟧
NEW: ⟦**Given** Settings → Connections (agent install)
**When**⟧
Why: same.

**S56 · Story 3.2 AC · L1049–1050**
OLD: ⟦**And** the empty Posture page now offers "Install agent" alongside "Connect registry" (UX-DR29).⟧
NEW: ⟦**And** the one-liner sits in a code block with Copy ("Copied" for 2 s, announced politely) (UX-DR42)
**And** the empty Home now offers exactly two setup actions — connect a registry and install a cluster agent — each with its one-liner in a code block (UX-DR29).⟧
Why: the code-block component; Home.

**S57 · Story 3.4 AC · L1094**
OLD: ⟦visible in Settings for that cluster.⟧
NEW: ⟦visible in Settings → Connections for that cluster.⟧
Why: panel name.

**S58 · Story 3.5 AC · L1113–1115**
OLD: ⟦**Given** Artifact detail
**When** an artifact runs somewhere
**Then** the running-locations section lists clusters, namespaces and workloads in mono, replacing the "no cluster agent connected" message from Story 2.11; shipped-but-not-running artifacts say so explicitly (FR18).⟧
NEW: ⟦**Given** Software detail
**When** a piece of software runs somewhere
**Then** the Where it runs cell lists each copy as a path ("prod-eu-west/payments"), replacing the "No cluster agent connected" message from Story 2.11, and the Software list splits into **Deployed N** (line 2 "prod-eu-west · 4 copies") and **Not deployed N** (line 2 "Last deployed 12 days ago" or "Never deployed"; hint "Not seen running in any connected cluster.", also on focus), with the summary "N deployed, M not deployed" (FR18, UX-DR25).⟧
Why: Deployed / Not deployed replace running / shipped; paths are not mono (Plex Mono is for IDs).

**S59 · Story 3.6 title · L1121**
OLD: ⟦### Story 3.6: Runtime coverage on Posture, and minute 29 with the agent⟧
NEW: ⟦### Story 3.6: Runtime coverage on Home and Software, and minute 29 with the agent⟧
Why: rename.

**S60 · Story 3.6 user story · L1124**
OLD: ⟦I want Posture to show what is running⟧
NEW: ⟦I want Home and Software to show what is deployed⟧
Why: rename.

**S61 · Story 3.6 AC · L1130–1131**
OLD: ⟦**When** Posture renders
**Then** the co-stat band includes running artifacts and connected clusters, and the freshness strip includes a runtime-observation entry per cluster with last heartbeat (FR16, UX-DR15).⟧
NEW: ⟦**When** Home and Software render
**Then** the Software summary line counts deployed and not-deployed software, and the freshness strip shows "N clusters reporting" (each cluster's last heartbeat is in Settings → Connections) (FR16, UX-DR15).⟧
Why: no co-stat band.

**S62 · Story 3.6 AC · L1134–1135**
OLD: ⟦**When** Posture and Artifacts render
**Then** each appears as a named coverage-gap row ("Cluster `prod-eu-west` disconnected — runtime data as of 14:02", "37 running digests not matched to any connected source")⟧
NEW: ⟦**When** Home and Software render
**Then** a disconnected cluster's runtime data is marked "as of 14:02", not removed, and each gap appears as a plain gap row ("37 running fingerprints we can't match to any connected source" — copy to confirm with UX)⟧
Why: plain labels (digest → fingerprint).

**S63 · Story 3.6 AC · L1140**
OLD: ⟦**Then** Posture shows running workloads and runtime coverage within the 30-minute gate⟧
NEW: ⟦**Then** Home and Software show deployed software and runtime coverage within the 30-minute gate⟧
Why: rename.

#### Epic 4 — intro, Stories 4.2–4.7 and new Stories 4.9–4.10

**S64 · Epic 4 intro · L1144 (D1, D10)**
OLD: ⟦Ranking stays severity-only until Epic 5, but enrichment is visible on findings from this epic on.⟧
NEW: ⟦Issues stay grouped by severity; Epic 5 settles the order within each group, and enrichment is visible on issues (the Actively exploited marker, technical details) from this epic on. The epic ends with two more external sources of knowledge, both connected or air-gapped: end-of-life data for packages (Story 4.9, FR33) and signature checks against trusted signers (Story 4.10, FR32).⟧
Why: D1; the new stories.

**S65 · Story 4.2 AC · L1196**
OLD: ⟦(populating banner and pipeline state)⟧
NEW: ⟦(Checking band and pipeline state)⟧
Why: rename.

**S66 · Story 4.2 AC · L1198–1200**
OLD: ⟦**Given** Artifact detail and the posture `provenance`
**When** they render after a re-evaluation
**Then** they state "Re-evaluated against Grype DB vX, N min ago — no rescan needed" (UX-DR15, UX-DR23 footer wording).⟧
NEW: ⟦**Given** Software detail, Exposure answers and the posture `provenance`
**When** they render after a re-evaluation
**Then** they show the evaluation inline — "Last checked", "How we know: Syft v… · Grype DB vX · checked N min ago" and, on Exposure, "Answered N min ago" — and no rescan is needed (UX-DR15, UX-DR23).⟧
Why: there is no provenance footer in the new spine.

**S67 · Story 4.3 AC · L1218–1220 (D1)**
OLD: ⟦**Given** a finding in the UI (Posture table, Artifact detail)
**When** it is KEV-listed
**Then** the KEV tag renders adjacent to the CVE ID and survives every compact view; EPSS score and percentile show with source and retrieval time on hover/focus (UX-DR9, FR12).⟧
NEW: ⟦**Given** an issue in the UI (Home, Issues, Software detail)
**When** it is KEV-listed
**Then** list rows show "Actively exploited" as clay text with a pulse icon (never dropped when a row truncates), detail views show the Actively exploited pill with a grey "KEV" tag, and the technical-details block lists KEV, CVSS and the raw EPSS value with source and retrieval time; EPSS is never shown as a rating, tag, column or hover score (UX-DR9, FR12).⟧
Why: plain label; the EPSS rating is rejected (memlog 40).

**S68 · Story 4.4 AC · L1247–1249**
OLD: ⟦**Given** Artifact detail and the findings table
**When** a finding renders
**Then** its enrichment panel lists every source used with retrieval time, and the freshness strip gains KEV, EPSS, CNA and OSV entries (UX-DR15).⟧
NEW: ⟦**Given** Software detail and the Issues detail
**When** an issue renders
**Then** its technical-details block lists every source used with retrieval time (CVE, KEV, CVSS, EPSS, source, check time), and the freshness strip gains an entry per enrichment source in plain words with the technical term small ("Exploited list KEV 6 Nov"; the labels for CNA, OSV and EPSS are not drawn in the spine — copy to confirm with UX) (UX-DR15).⟧
Why: no enrichment panel; plain strip labels.

**S69 · Story 4.6 AC · L1293**
OLD: ⟦**Given** Settings → Feed-bundle import (admin only)⟧
NEW: ⟦**Given** Settings → Sources (bundle import, admin only)⟧
Why: panel name.

**S70 · Story 4.7 title · L1310**
OLD: ⟦### Story 4.7: Honest feed staleness across Posture and findings⟧
NEW: ⟦### Story 4.7: Honest feed staleness across Home and Issues⟧
Why: rename.

**S71 · Story 4.7 user story · L1313**
OLD: ⟦I want stale or failing feeds to change what Posture says,⟧
NEW: ⟦I want stale or failing feeds to change what Home says,⟧
Why: rename.

**S72 · Story 4.7 AC · L1320**
OLD: ⟦its freshness-strip age turns warning, the posture headline gains a scoped caveat ("KEV catalogue 3 days old — exploited-status may be out of date"),⟧
NEW: ⟦its freshness-strip age turns amber with the age in words and an amber dot, the Home summary line gains a scoped caveat (for example "The exploited list (KEV) is 3 days old, so Actively exploited may be out of date." — copy to confirm with UX), "good shape" is never claimed on old data,⟧
Why: no warning token or headline.

**S73 · Story 4.7 AC · L1323**
OLD: ⟦**Given** a feed that has never been loaded
**When** Posture renders⟧
NEW: ⟦**Given** a feed that has never been loaded
**When** Home renders⟧
Why: rename.

**S74 · Story 4.7 AC · L1326–1328**
OLD: ⟦**Given** every freshness-strip entry
**When** it is clicked
**Then** it opens the feed's Settings page, showing version history, last success, last failure and reason (UX-DR15).⟧
NEW: ⟦**Given** the "Sources" link on the freshness strip
**When** it is clicked
**Then** it opens Settings → Sources, showing each feed's version history, last success, last failure and reason (UX-DR15).⟧
Why: one Sources link.

**S75 · new Story 4.9 · after Story 4.8, before "## Epic 5" (L1357–1359) (D10, FR33)**
OLD (anchor, kept): ⟦**Then** it runs as its own mise task outside `mise run check`.

## Epic 5: Prioritise and triage findings⟧ (insert between the two)
NEW: ⟦### Story 4.9: End-of-life data for packages

As a SecOps engineer,
I want to see which packages in a piece of software have reached their end of life,
So that I can plan upgrades before a package stops getting security fixes.

**Acceptance Criteria:**

**Given** the open end-of-life data decision (FR33, ARCH41)
**When** this story is planned
**Then** the end-of-life data source and its licence, what it covers (package ecosystems; whether runtimes and OS releases are included), how packages are matched to it (exact identifiers only), and its staleness threshold (PROC2 default) are recorded as an amendment to `architecture.md` and approved by the user before implementation.

**Given** connected mode
**When** the enrichment schedule fires (default every 6 h, Helm value, PROC2)
**Then** the `enrichment` module fetches the end-of-life dataset, validates it and stores it as a versioned, source-attributed snapshot (source, version or date, retrieved_at), appended to the evidence ledger (FR33, FR12, ARCH21)
**And** a fetch or validation failure keeps the previous snapshot active and reports the source stale; nothing is ever partially applied (ARCH20 R8).

**Given** a new snapshot
**When** it is applied
**Then** every package in every stored SBOM is re-joined to it through the package index without re-matching SBOMs, and each package records its end-of-life date and status — past end of life, supported or unknown — with source and retrieval time (FR33, FR7)
**And** a package the data does not cover is "unknown", never "supported", proven by a test.

**Given** air-gapped mode
**When** the schedule would fire
**Then** no outbound request is made; the dataset arrives only as one more component of the offline bundle — this story extends the Story 4.5 manifest and the Story 4.6 import, so it is verified and activated together with the other components (FR10, NFR4, ARCH19, ARCH20).

**Given** Software detail
**When** the Packages cell and the Packages tab render
**Then** the cell carries one end-of-life line scoped to the data ("No package is past its end of life." only when every package is covered and none is past; otherwise the count past end of life and the count with no end-of-life data, in plain words — copy to confirm with UX, O14), and each package in the Packages tab shows its end-of-life date or that there is no end-of-life data, with the source small (UX-DR25)
**And** end-of-life status is stated in words, has no severity colour, creates no issue and does not count toward Needs attention (O13).

**Given** `GET /api/v1/artifacts/{id}`
**When** it responds
**Then** each package carries its end-of-life status, date and source, and the source's version and age are in `provenance.sources` (ARCH14).

**Given** Settings → Sources and the Story 4.7 freshness rules
**When** the source is past its threshold or its last update failed
**Then** Settings → Sources lists it with version history, last success, last failure and reason, and the Software detail end-of-life line carries a scoped caveat; whether the source also appears on the Home freshness strip is set by UX before Build (O15) (UX-DR15, UX-DR28).

**Given** the Story 4.8 scale-anchor fixtures
**When** an end-of-life re-join runs
**Then** it completes within the one-hour enrichment re-join bound, and the result is appended to the committed performance record.⟧
Why: D10 — FR33 needs its own story; Epic 4 owns attributed external data and the offline bundle.

**S76 · new Story 4.10 · directly after Story 4.9 (same insertion point) (D10, FR32)**
NEW: ⟦### Story 4.10: Verify artifact signatures against trusted signers

As a SecOps engineer,
I want Armoury to check whether each image is signed by someone we trust,
So that I can tell software someone vouched for from software nobody did.

**Acceptance Criteria:**

**Given** the open signature-verification decision (FR32, ARCH40)
**When** this story is planned
**Then** the trust configuration (public keys and keyless signer identities; fleet-wide or per registry connection), the result states and their names, the signature formats read from the registry, the artifact types in scope, and how the Sigstore trusted root reaches air-gapped instances are recorded as an amendment to `architecture.md` and approved by the user before implementation.

**Given** Settings → Policy (signature policy, admin only) or Helm values
**When** an admin adds or removes trusted signers
**Then** they can add public keys and keyless signer identities (OIDC issuer and subject); the default is none (PROC2), so a default install verifies nothing and says so; each change is a new policy version appended to the evidence ledger; analysts and auditors see the policy read-only with edit controls absent (UX-DR28, UX-DR31).

**Given** a container image or other OCI artifact in a connected registry
**When** it is discovered, or the signature policy changes
**Then** the control plane runs the pinned cosign CLI (added in Story 4.5) through `tools` to verify its signatures, read from the same registry with the connection's read-only credentials in per-invocation env (never argv), and records the result with the signer, the trust-policy version, the cosign version and the check time, appended to the evidence ledger (FR32, NFR12, ARCH7, ARCH40)
**And** a policy change re-checks signatures without rescanning SBOMs.

**Given** air-gapped mode
**When** a signature is verified
**Then** key-based verification makes no network call, and keyless verification uses only the offline trusted root from the approved amendment; no call is made to public Fulcio, Rekor or the Sigstore TUF repository, proven by the Story 1.2 air-gap test (NFR4, ARCH19).

**Given** Software detail
**When** the Info list renders
**Then** "Signed" reads "Yes" when a signature from a trusted signer verifies, and plain words for every other state (copy to confirm with UX, O7), with the signer and check time in the technical details; a missing or failed signature is never hidden and never shown in a severity colour (FR32, NFR8, UX-DR25)
**And** an artifact type this story does not check says that it is not checked, never "No" (O10).

**Given** a tampered image, a signature by a removed key or a keyless identity that does not match
**When** verification runs
**Then** the result is not "verified", proven by tests.

**Given** `GET /api/v1/artifacts/{id}`
**When** it responds
**Then** it includes the signature result (state, signer, trust-policy version, cosign version, check time) (ARCH14).⟧
Why: D10 — FR32 needs its own story; it reuses the cosign binary and trusted-key pattern of Stories 4.5–4.6.

#### Epic 5 — intro and Stories 5.1–5.8

**S77 · Epic 5 intro · L1361 (D1)**
OLD: ⟦The analyst works a KEV-first, EPSS-weighted findings list that explains each ranking, records justified decisions that propagate everywhere the finding appears,⟧
NEW: ⟦The analyst works the Issues list — grouped by severity, Actively exploited first in each group, the order stated in words — and records decisions with their reason in the review panel, which propagate everywhere the issue appears,⟧
Why: D1 and the review panel.

**S78 · Story 5.1 title · L1363**
OLD: ⟦### Story 5.1: Deterministic, explainable ranking⟧
NEW: ⟦### Story 5.1: Deterministic, explainable issue order⟧
Why: D1.

**S79 · Story 5.1 user story · L1366**
OLD: ⟦I want findings ranked KEV first, then by EPSS-weighted severity, with the reason shown,⟧
NEW: ⟦I want issues grouped by severity with Actively exploited first in each group, in an order I can read in words,⟧
Why: D1.

**S80 · Story 5.1 AC · L1373**
OLD: ⟦the exact formula (KEV tier, EPSS weighting, severity source precedence, tie-breakers)⟧
NEW: ⟦the exact order (severity groups and severity-source precedence, Actively exploited first within a group, the raw EPSS value as the next key, the stable tie-breaker, licences in their own group)⟧
Why: D1.

**S81 · Story 5.1 AC · L1377–1378**
OLD: ⟦every KEV-listed finding ranks above every non-KEV finding, the rest are ordered by the approved EPSS-weighted severity⟧
NEW: ⟦each issue falls into the Licences group or the Critical / High / Medium / Low group of its severity; every Actively exploited issue sorts above every other issue in its group, and the rest follow the approved within-group order⟧
Why: D1.

**S82 · Story 5.1 AC · L1378**
OLD: ⟦**And** a property test asserts determinism and the KEV-first invariant over generated findings.⟧
NEW: ⟦**And** a property test asserts determinism and the exploited-first-within-group invariant over generated issues.⟧
Why: D1.

**S83 · Story 5.1 AC · L1382**
OLD: ⟦it returns a ranking explanation — each input (KEV status, EPSS score/percentile, severity and its source) with its source and retrieval time, and the resulting rank tier — in words a human can read.⟧
NEW: ⟦it returns an order explanation — each input (severity and its source, KEV status, the raw EPSS value) with its source and retrieval time, and the resulting group and position — in words a human can read; the UI shows it only in the technical-details block, never as a rating.⟧
Why: EPSS is never a rating.

**S84 · Story 5.1 AC · L1390**
OLD: ⟦**Then** the formula defines their place explicitly (documented in the amendment), never by accident of nulls.⟧
NEW: ⟦**Then** licence issues sit in the Licences group (no severity; hidden at 0) and issues without enrichment take an explicit place in their severity group (documented in the amendment), never by accident of nulls.⟧
Why: the Licences group.

**S85 · Story 5.2 title · L1392**
OLD: ⟦### Story 5.2: Findings workbench and ranked Posture table⟧
NEW: ⟦### Story 5.2: Issues list — severity groups, filters and the Home summary⟧
Why: rename.

**S86 · Story 5.2 user story · L1395–1396**
OLD: ⟦I want a Findings surface that lists every finding in ranked order,
So that I have one place to work through the fleet's findings.⟧
NEW: ⟦I want an Issues surface that lists every open issue grouped by severity,
So that I have one place to review the fleet's issues.⟧
Why: rename.

**S87 · Story 5.2 AC · L1400–1403 (D1, D6)**
OLD: ⟦**Given** the Findings surface⟧ … through ⟦**And** the header reads "KEV first, then EPSS-weighted. Severity alone does not rank."⟧ (the whole first AC, L1400–1403)
NEW: ⟦**Given** the Issues surface
**When** it loads
**Then** the list column shows "Issues" and a summary line ("3 need attention today. 312 not reviewed yet."); issues (one vulnerability or licence in one package version, across its places — UX-DR39) grouped Licences (hidden at 0), Critical, High, Medium and Low, each with its count; standard rows (name + version · severity · Actively exploited · where; right column the review-status chip or "Mixed · N of M"); "N more High" rows for long groups; the pager "1–25 of 312 · page 1 of 13" (25 per page, never infinite scroll); and coverage-gap rows in place (UX-DR9, UX-DR11, UX-DR26, ARCH38)
**And** the order is stated above the list in words: "Actively exploited sorts first in each group"; EPSS is never shown.⟧
Why: the new Issues IA (D1).

**S88 · Story 5.2 AC · L1405–1407**
OLD: ⟦**Given** filters (severity, KEV, triage status, artifact, ecosystem)
**When** applied
**Then** they narrow the list server-side with the order preserved, and the active scope is stated above the table.⟧
NEW: ⟦**Given** the filters — the type segmented control All · Vulnerabilities · Licences with counts ("Licences 0" stays visible), the Review status filter listing the five statuses with counts (default Not reviewed yet) and the search field ("Find a package or vulnerability", `/`)
**When** applied
**Then** they narrow the list server-side with the grouping and order preserved, and the active scope is stated above the list; a Mixed issue matches every status any of its places has ([ASSUMPTION], EXPERIENCE Open item 9); counts count issues, not places
**And** at 0 it reads "No issues are waiting for review." with the coverage scope and the grey Show all statuses; a search with no match reads "No issues match "<text>" with these filters." with the grey Clear search (UX-DR45).⟧
Why: the new filters and states.

**S89 · Story 5.2 AC · L1409–1411**
OLD: ⟦**Given** Posture's findings table from Story 2.10
**When** this story lands
**Then** it uses the same ranked order and header sentence, replacing the interim "sorted by severity" header.⟧
NEW: ⟦**Given** Home's Open issues summary and Needs attention from Story 2.10
**When** this story lands
**Then** they use the same groups, order and counts, and the Needs-attention count is the same number on Home, in the Issues summary and on the sidebar badge (UX-DR38).⟧
Why: no Posture table.

**S90 · Story 5.2 AC · L1413–1415**
OLD: ⟦**When** the user moves through rows with arrow keys
**Then** the highlighted row is announced, and the row actions are reachable without a pointer.⟧
NEW: ⟦**When** the user presses `J`/`K` or clicks a row
**Then** the next or previous issue is selected (`aria-current`), announced, and fills the detail column (tabs Review · Exposure · History, "1 of 3 · J K" at the bar's end) while the list keeps its place; every row action is reachable without a pointer; the Exposure and History tabs are not drawn (EXPERIENCE Open item 15).⟧
Why: master-detail and J/K.

**S91 · Story 5.3 AC · L1426–1428 (D7)**
OLD: ⟦and a non-empty justification
**Then** it is stored with author, UTC timestamp and UUIDv7, and appended to the evidence ledger in the same transaction (FR14, NFR11, ARCH15)
**And** a missing justification or a status outside the locked enum is rejected with 422.⟧
NEW: ⟦and a justification — required for `not_affected`, `mitigated` and `accepted`, optional for `fix_planned` (D7)
**Then** it is stored with author, UTC timestamp and UUIDv7, and appended to the evidence ledger in the same transaction (FR14, NFR11, ARCH15)
**And** a missing required justification or a status outside the locked enum is rejected with 422
**And** the UI shows the statuses as Not impacted, Mitigated, Risk accepted and Fix planned, and the derived `untriaged` as Not reviewed yet; the API enums, exports and VEX keep the technical terms (ARCH15).⟧
Why: D7 and the UI labels.

**S92 · Story 5.3 AC · L1433**
OLD: ⟦each decision in this story applies to one finding on one artifact; the fleet-wide scope arrives in Story 5.8.⟧
NEW: ⟦each decision in this story applies to one finding on one piece of software (one place); the "All N places" scope arrives in Story 5.8.⟧
Why: scope labels.

**S93 · Story 5.3 AC · L1437**
OLD: ⟦(Story 5.4 keeps the form absent for auditors).⟧
NEW: ⟦(Story 5.4 keeps the review panel absent for auditors).⟧
Why: no drawer.

**S94 · Story 5.3 AC · L1440–1441 (D6)**
OLD: ⟦**When** Posture, Findings, Artifact detail and the posture API render
**Then** they show the current status and use it in counts (for example "untriaged critical"),⟧
NEW: ⟦**When** Home, Issues, Software detail and the posture API render
**Then** they show the current status and use it in counts, counting issues, not places (for example "2 Critical not reviewed yet"),⟧
Why: labels and the count unit.

**S95 · Story 5.4 title · L1448**
OLD: ⟦### Story 5.4: Triage drawer⟧
NEW: ⟦### Story 5.4: Review panel in the Issues detail column⟧
Why: the drawer is replaced.

**S96 · Story 5.4 user story · L1451–1452**
OLD: ⟦I want a drawer that shows why a finding ranks where it does and lets me decide without leaving the list,
So that triage is fast and every decision has its context.⟧
NEW: ⟦I want to review an issue in the detail column without leaving the list,
So that review is fast and every decision has its reason.⟧
Why: the review panel.

**S97 · Story 5.4 AC · L1456–1458**
OLD: ⟦**Given** any findings list
**When** the user clicks a row or presses `t`
**Then** a right-side `Sheet` opens showing the ranking explanation, full provenance (evaluation time, tool/DB versions, enrichment sources with retrieval times) and decision history (FR8, FR12, FR13, UX-DR16).⟧
NEW: ⟦**Given** the Issues list
**When** an issue is selected
**Then** its Review tab shows the summary (title, severity, Actively exploited pill + KEV tag), the places count with "See the map", What to do, the review status, the review panel and the technical-details block (CVE, KEV, CVSS, EPSS, source and check time, plus the order explanation from Story 5.1); decision history is on the History tab (not drawn, EXPERIENCE Open item 15) (FR8, FR12, FR13, UX-DR16).⟧
Why: no `Sheet`; `t` gets a new meaning later (Open item 13).

**S98 · Story 5.4 AC · L1460–1463, plus a new AC (D7)**
OLD: ⟦**Given** the decision form
**When** the analyst picks a status, writes a justification and submits (or presses `⌘Enter`)
**Then** the decision is recorded, the row updates in place, and on `⌘Enter` the drawer advances to the next finding; `Esc` closes it
**And** status can never be changed inline in a table — only through the drawer.⟧
NEW: ⟦**Given** the review panel
**When** the analyst answers "Does this vulnerability impact us?" (No, not impacted → Not impacted; Yes → "What will we do?": Fix it → Fix planned; Reduce the risk → Mitigated; Accept the risk → Risk accepted), each option showing the status chip it produces, and fills "Why? (shown in the audit report)" where required (every status except Fix planned)
**Then** Save and next ⌘↵ (lime, disabled at 0.45 until a question is answered) records the decision, updates the row's chip in place and selects the next issue in the current filter; Decide later moves on without recording; the hint reads "Saved with your name in the audit trail."
**And** status can never be changed inline in a list — only in the review panel.

**Given** a save that fails
**When** the API returns an error
**Then** an inline error line in the panel names the problem ("Your decision wasn't saved: Armoury can't reach its database.") with Try again, announced with `role="alert"`; Save and next does not advance; the chosen options, scope and "Why?" text stay filled in; no toast appears (UX-DR41).⟧
Why: the two-question review; D7; the inline save error (memlog 86).

**S99 · Story 5.4 AC · L1465–1467**
OLD: ⟦**Given** "Record triage decision" and "Open triage drawer"
**When** the palette is opened on a highlighted finding
**Then** both are available as palette actions (UX-DR6).⟧
NEW: ⟦**Given** the "Review" palette action and the Review buttons on Home, the Exposure inspector and Software
**When** used
**Then** they open the issue in Issues on its Review tab ([ASSUMPTION], EXPERIENCE Open item 4), and Home's lime "Review all N" opens the Needs-attention issues one after another (UX-DR6, UX-DR22).⟧
Why: one Review action.

**S100 · Story 5.4 AC · L1470–1471**
OLD: ⟦**When** they open the drawer
**Then** it shows explanation, provenance and history, with the form absent (UX-DR31).⟧
NEW: ⟦**When** they open an issue
**Then** the summary, technical details and history show, and the review panel is absent (UX-DR31).⟧
Why: no drawer.

**S101 · Story 5.5 title · L1473 (D9)**
OLD: ⟦### Story 5.5: Evidence trail surface⟧
NEW: ⟦### Story 5.5: Audit trail in Reports and on every item⟧
Why: D9.

**S102 · Story 5.5 user story · L1476 (D9)**
OLD: ⟦I want to browse the append-only evidence trail,⟧
NEW: ⟦I want to read the append-only audit trail of the whole fleet in Reports, and of any piece of software, issue or audit report,⟧
Why: D9 — fleet-wide group plus per-item tabs.

**S103 · Story 5.5 AC · L1481–1483 (D9)**
OLD: ⟦**Given** the Evidence surface
**When** it loads
**Then** it lists ledger entries newest first with type, subject (mono identifier), actor, time and tool/feed versions, with cursor pagination and filters by type, subject and time window (UX-DR27).⟧
NEW: ⟦**Given** Reports (`/reports`), whose first group this story adds
**When** the user opens **Audit trail**
**Then** it lists the whole fleet's ledger entries newest first with type, subject (plain label with its technical ID small in mono), actor, time and tool/feed versions, 25 per page with cursor pagination and a pager total, and filters by type, subject and time window (D9, UX-DR27)
**And** Reports shows only the groups that exist so far — Audit trail now; Exports arrive in Story 6.5 and Audit reports in Story 9.5 — and auditors see all of it.⟧
Why: D9 — the fleet-wide browser lives in Reports.

**S104 · Story 5.5 AC · L1489–1491 (D9)**
OLD: ⟦**When** the surface renders
**Then** it shows the current verification result ("Chain intact — N entries, verified 4 min ago") or the first broken entry.⟧
NEW: ⟦**When** Reports → Audit trail renders
**Then** it shows the current verification result ("Chain intact — N entries, verified 4 min ago") or the first broken entry, named in plain words with a link to it; the layout and wording of the broken-chain state are set by UX before Build (O16); Stories 9.6 and 9.9 add the checkpoint and anchoring status to the same group.⟧
Why: D9.

**S105 · Story 5.5 AC · L1493–1495 (D9)**
OLD: ⟦**Given** a finding, artifact or decision elsewhere in the UI
**When** the user chooses "View evidence"
**Then** the Evidence surface opens filtered to that subject.⟧
NEW: ⟦**Given** a piece of software, an issue or (from Story 9.5) an audit report
**When** the user opens its Audit trail tab (Software, Reports) or History tab (Issues; not drawn — EXPERIENCE Open item 15)
**Then** it lists that subject's entries newest first under "Entries are never edited or removed.", with a link that opens Reports → Audit trail filtered to that subject.⟧
Why: D9 — per-item tabs stay.

**S106 · Story 5.6 title · L1497**
OLD: ⟦### Story 5.6: Emit VEX from triage decisions⟧
NEW: ⟦### Story 5.6: Emit VEX from review decisions⟧
Why: "triage" is retired as a UI word (VEX stays).

**S107 · Story 5.6 AC · L1508 (D7)**
OLD: ⟦including `accepted` and `fix_planned` — is recorded as an amendment to `architecture.md` and approved by the user before implementation.⟧
NEW: ⟦including `accepted` and `fix_planned`, and a `fix_planned` decision with no justification, whose action statement comes from the planned fix ("Update log4j-core to 2.17.2") (D7) — is recorded as an amendment to `architecture.md` and approved by the user before implementation.⟧
Why: D7.

**S108 · Story 5.6 AC · L1513 (D6)**
OLD: ⟦with author and timestamp (FR15)⟧
NEW: ⟦with author and timestamp (FR15); when an issue is Mixed, each product's statement carries its own status; in the UI the file is listed as "review decisions (VEX)"⟧
Why: D6 and the plain file label.

**S109 · Story 5.7 AC · L1541**
OLD: ⟦("not affected — per <vendor> VEX, <date>")⟧
NEW: ⟦("Not impacted — per <vendor> VEX, <date>")⟧
Why: plain status label.

**S110 · Story 5.7 AC · L1543–1545**
OLD: ⟦**Given** the triage drawer
**When** a finding has vendor VEX
**Then** the VEX context panel shows the vendor, statement, justification, document and the matching rule (UX-DR16).⟧
NEW: ⟦**Given** the Issues Review tab
**When** an issue has vendor VEX
**Then** it shows the vendor, statement, justification, document and the matching rule (UX-DR16); the presentation is not drawn (EXPERIENCE Open item 17) and is designed before this story starts Build.⟧
Why: no drawer; a UX gap.

**S111 · Story 5.8 title · L1551 (D6)**
OLD: ⟦### Story 5.8: Fleet-wide triage decisions⟧
NEW: ⟦### Story 5.8: Review scope — all places or only this software⟧
Why: D6.

**S112 · Story 5.8 user story · L1554–1555 (D6)**
OLD: ⟦I want to record one decision for a vulnerability in a package across the whole fleet,
So that I do not repeat the same justified decision on every artifact.⟧
NEW: ⟦I want one decision to cover every place an issue affects, or only one piece of software,
So that I do not repeat the same decision on every piece of software.⟧
Why: D6.

**S113 · Story 5.8 AC · L1561 (D6)**
OLD: ⟦they choose its scope — **this artifact** (default, PROC2) or **fleet-wide** (this vulnerability + package across every artifact, including artifacts discovered later)⟧
NEW: ⟦they choose its scope — **All N places** (default, D6: this vulnerability or licence in this package version, across every piece of software that has it, including software found later) or **Only this software** (one piece of software, pre-filled when Review was opened from it)⟧
Why: D6 flips the default and fixes the unit to one package version.

**S114 · Story 5.8 AC · L1566**
OLD: ⟦superseding a fleet-wide decision leaves per-artifact overrides in place.⟧
NEW: ⟦superseding an All-places decision leaves per-software decisions in place, and the panel says how many keep theirs ("2 places keep their own status"; [ASSUMPTION], EXPERIENCE Open item 9).⟧
Why: the EXPERIENCE review flow.

**S115 · Story 5.8 AC · L1568–1572 (D6)**
OLD: ⟦**Given** the triage drawer from Story 5.4⟧ … through ⟦**And** the findings API and VEX export (Story 5.6) use the resulting current status, and table triage pills show it the same way for both scopes.⟧ (the whole AC, L1568–1572)
NEW: ⟦**Given** the review panel from Story 5.4
**When** it opens on an issue
**Then** it shows the decision that applies now and its source in plain words (for example "All places — Priya, 3 Nov" or "Only this software — differs from the other places"; copy to confirm with UX) (UX-DR16)
**And** the scope segmented control above the questions offers "All N places" (default) and "Only this software" (which reveals a select of the places), with the number of places the choice changes now
**And** the findings API and VEX export (Story 5.6) use the resulting current status per place; the row's chip shows that status, or "Mixed · N of M" (N = places that differ from the issue-wide status; accessible name "Mixed: 3 of 14 places have a different status"); an issue stays Not reviewed yet and in Needs attention while any place is Not reviewed yet (UX-DR38, UX-DR39, ARCH38).⟧
Why: the scope control and the Mixed chip (D6).

#### Epic 6 — intro and Stories 6.2–6.6

**S116 · Epic 6 intro · L1576 (D3, D4)**
OLD: ⟦sees affected artifacts, shipped and running, and where they run — as graph or table, with a provenance footer — exports it, and explores further in the graph.⟧
NEW: ⟦sees on Exposure which software has it, deployed and not deployed, and where it runs — answered in words first, then as a map or a table, with "Answered N min ago" and "How we know" — exports it (stored as evidence in Reports → Exports), and moves the map to any node to explore further.⟧
Why: same as E77.

**S117 · Story 6.2 AC · L1615**
OLD: ⟦("2 artifacts in scope have no SBOM yet and are not represented")⟧
NEW: ⟦("2 pieces of software haven't been checked yet and aren't on the map. This answer covers the 3,176 we have checked.")⟧
Why: the caveat text is user-facing (the export test compares it).

**S118 · Story 6.2 AC · L1619**
OLD: ⟦("No artifacts affected — across the N% of the fleet that is scanned")⟧
NEW: ⟦("No software has it — across the N pieces of software we've checked (82%)"), only for a vulnerability Armoury has data for⟧
Why: the coverage-scoped zero copy.

**S119 · Story 6.2 AC · L1623 (D1)**
OLD: ⟦the CVEs that affect it (ranked, with triage status)⟧
NEW: ⟦the vulnerabilities that affect it (in Issues order, with review status)⟧
Why: D1; labels.

**S120 · Story 6.2 AC · L1628**
OLD: ⟦from "CVE not in any loaded feed" (with feed versions).⟧
NEW: ⟦from "CVE not in any loaded feed" (with feed versions and their age); the UI never turns the second into "No software has it" (Story 6.3).⟧
Why: the unknown-vulnerability rule (memlog 85).

**S121 · Story 6.3 title · L1634**
OLD: ⟦### Story 6.3: Blast-radius surface — answer and table, from ⌘K⟧
NEW: ⟦### Story 6.3: Exposure surface — answer and table, from ⌘K⟧
Why: rename.

**S122 · Story 6.3 AC · L1644**
OLD: ⟦an "Answers" result routes to the Blast radius surface with that query; a digest gives two results — the digest blast-radius answer (Story 6.2) and the artifact detail (UX-DR6).⟧
NEW: ⟦an Exposure result ("Where are we exposed to log4j-core?") routes to Exposure with that query; a fingerprint gives two results — its Exposure answer (Story 6.2) and its Software detail (UX-DR6).⟧
Why: the new palette groups.

**S123 · Story 6.3 AC · L1648–1649, plus new ACs**
OLD: ⟦**Then** it shows the answer headline ("14 affected artifacts · 9 running · 2 clusters"), a caveat chip when partial, the table reading (artifact, package@version, running locations, triage status — mono identifiers, KEV tag), and the provenance footer stating re-evaluation recency ("Re-evaluated against Grype DB vX, 41 min ago — no rescan needed") (UX-DR23, UX-DR15)
**And** the page-header search field (Story 1.6) now routes blast-radius answers from the palette, pre-scoped to blast radius.⟧
NEW: ⟦**Then** a full-width header shows "Exposure", the question, the query button showing the subject (it opens ⌘K), the Graph · Table switch, grey Export and "Audit report for this answer" (both Story 6.5), and the answer in words first ("14 pieces of software have it. 9 are deployed, 5 are not deployed.") with its meta line (Actively exploited pill, KEV tag, severity, CVSS, "Answered 38 min ago") and the deployed / not-deployed split; the list column holds Deployed N, Not deployed N and the "Not checked yet" gap row; the Table reading lists Software, Version, Deployed? (Yes/No), Where it runs, Copies, Severity and Review, deployed first, with sortable sentence-case headers and "N not checked yet, not listed"; a caveat line scopes the answer (UX-DR23, UX-DR15)
**And** Home's Exposure tab (a reduced summary with a button to the full page), See exposure, See the map and "See all 14 on the map" open Exposure for that query.

**Given** Exposure with a CVE ID Armoury has no data for (the Story 6.2 "not in any loaded feed" error)
**When** it renders
**Then** the answer reads "Armoury has no data for <ID> yet. Vulnerability data updated <age> ago." with the lime Check again (re-asks against the latest data; no rescan), with no map and no zero (UX-DR40).

**Given** a known vulnerability with no matches
**When** it renders
**Then** the coverage-scoped zero from Story 6.2 shows, with the unchecked remainder one click away (UX-DR40).⟧
Why: the Exposure IA; the unknown-vulnerability state.

**S124 · Story 6.3 AC · L1651–1653**
OLD: ⟦**Given** a digest query
**When** the answer renders
**Then** the same surface is centred on the artifact: headline "12 CVEs · 7 vulnerable packages · runs in 3 workloads", and the table has one row per finding in ranked order (KEV first) with triage status (UX-DR23).⟧
NEW: ⟦**Given** a fingerprint query
**When** the answer renders
**Then** the same surface centres on that piece of software: the answer in plain words names its open issues, the packages they come from and where it runs (as drawn for a moved map: "payments-api 3.4.1 has 2 open issues. It runs in 1 place, with 4 copies."), and the table lists its issues grouped by severity, Actively exploited first, with review status (UX-DR23); the copy for an unknown package or fingerprint is set by UX before Build (EXPERIENCE Open item 29).⟧
Why: plain labels; D1.

**S125 · Story 6.3 AC · L1655–1657**
OLD: ⟦**When** the user presses `t`
**Then** the triage drawer opens for that finding (Story 5.4).⟧
NEW: ⟦**When** the user chooses Review in the inspector
**Then** the issue opens in Issues on its Review tab (Story 5.4); the meaning of `t` is open (EXPERIENCE Open item 13).⟧
Why: no drawer.

**S126 · Story 6.3 AC · L1661**
OLD: ⟦("searching — 1,204 of 3,000 artifacts evaluated")⟧
NEW: ⟦("Checking — 1,204 of 3,000 pieces of software so far")⟧
Why: plain copy.

**S127 · Story 6.4 title · L1663**
OLD: ⟦### Story 6.4: Blast-radius graph reading⟧
NEW: ⟦### Story 6.4: Exposure map reading⟧
Why: rename.

**S128 · Story 6.4 user story · L1667**
OLD: ⟦So that I can see the path from CVE to running workload at a glance.⟧
NEW: ⟦So that I can see the path from the vulnerability to where it runs at a glance.⟧
Why: plain labels.

**S129 · Story 6.4 AC · L1673 (D11)**
OLD: ⟦**Then** Svelte Flow renders CVE → vulnerable packages → affected artifacts → clusters/workloads left to right, with severity hue only on the affected path, running nodes with accent ring + pip + label, shipped-not-running nodes with a dashed `node-inactive-border`, `text-muted` text and the label "shipped, not running" (no opacity on text), and soft bezier edges (UX-DR17, UX-DR23).⟧
NEW: ⟦**Then** Svelte Flow renders a hairline map, left to right, with four tiers labelled in sentence case with counts — Vulnerability · Package · Software · Where it runs; circular nodes; deployed edges solid (`forest-2`); not-deployed edges dashed (`slate-dot`), with not-deployed software below a dashed rule labelled "Not deployed"; the selected path heavier (`forest-ink`) and the selected node lime with "Selected on the map"; only the vulnerability node takes clay (`clay-wash` fill, `clay-dot` ring, a pulse icon when actively exploited); edge labels ("direct · in 12"); soft bezier edges; the legend, zoom (+ / − / Fit) and the caveat line in a footer; no opacity on text (UX-DR17, UX-DR23).⟧
Why: the new graph spec; old tokens removed.

**S130 · Story 6.4 AC · L1677**
OLD: ⟦the tiers run CVEs → packages → artifact → clusters/workloads, left to right, centred on the artifact (UX-DR23).⟧
NEW: ⟦the map is centred on that piece of software with the same layout as a moved map (Story 6.6: its contents on the left, where it runs and its copies on the right) (UX-DR23, UX-DR24).⟧
Why: the fingerprint query uses the ego view (D4).

**S131 · Story 6.4 AC · L1681**
OLD: ⟦("+ 9 more artifacts")⟧
NEW: ⟦as text nodes ("8 more", "5 more places")⟧
Why: roll-up copy.

**S132 · Story 6.4 AC · L1685**
OLD: ⟦**Then** arrows/`Tab` traverse nodes, `Enter` opens node detail, `+`/`−` zoom, each node's `aria-label` carries identifier, tier and state, and the Graph/Table toggle preserves the answer (UX-DR7, UX-DR34)⟧
NEW: ⟦**Then** arrows/`Tab` move between nodes and show the focused node in the inspector, `+`/`−` zoom, each node's `aria-label` carries name, tier and state, the map has an `aria-label` summarising the answer, and the Graph/Table switch keeps the answer and the selection (UX-DR7, UX-DR34); `Enter` on a node moves the map (Story 6.6) and the node's detail opens from the inspector⟧
Why: D4 gives `Enter` the move; selection carries across.

**S133 · Story 6.5 title · L1688 (D3)**
OLD: ⟦### Story 6.5: Export blast-radius and posture answers⟧
NEW: ⟦### Story 6.5: Export views as stored evidence, and the answer report⟧
Why: D3.

**S134 · Story 6.5 user story · L1691–1692 (D3)**
OLD: ⟦I want to export an answer exactly as I see it,
So that I can hand the CTO something he can trust without me annotating it.⟧
NEW: ⟦I want to export what I see and have the export kept as evidence,
So that I can hand the CTO something he can trust without me annotating it, and anyone can later see exactly what was sent.⟧
Why: D3.

**S135 · Story 6.5 AC · L1696–1699, plus new ACs (D3)**
OLD: ⟦**Given** a blast-radius answer or the posture summary
**When** the user chooses Export (or presses `x`)
**Then** they can pick CSV, JSON or a PDF report (PROC2), each carrying the same provenance footer, coverage and caveats as the on-screen answer (FR19, UX-DR21)⟧
NEW: ⟦**Given** an Exposure answer (on a moved map, its current centre), the Issues list or the Software list
**When** the user chooses Export (or presses `x`)
**Then** they get a CSV of the current view by default, with JSON as an option (PROC2), each carrying the same caveats and provenance as the screen ("The 2 not checked yet travel with the CSV and the audit report") (FR19, UX-DR21)⟧
Why: D3 — CSV of the current view from three views; the posture summary is covered by the audit report.

**S136 · Story 6.5 new ACs · after L1699 (D3)**
OLD (anchor, kept): ⟦**And** a test asserts the export's caveats equal the API response's caveats.⟧
NEW: ⟦
**Given** an export
**When** it is made
**Then** the file is stored in the object store through `blob` (content-addressed), an insert-only export record and a ledger entry record who, when, the view and the query or filters, the format, the row count, the caveats and the file digest, and the export is listed in Reports → Exports, newest first ("Exposure: log4j-core 2.17.0 · CSV · 14 rows · from Exposure · 6 Nov") (FR19, ARCH39)
**And** stored exports have no edit or delete endpoint and follow the evidence-pack retention (default and minimum 24 months, ARCH30); the owning module is settled when the story is planned (O1).

**Given** Exposure
**When** the user chooses "Audit report for this answer"
**Then** the PDF answer report below is produced for the current answer (or the current centre of a moved map) and stored and listed in Reports → Exports like any export (D3).

**Given** an export that fails to start or to store
**When** it fails
**Then** the inline error with Try again appears in the Export row, nothing partial is stored or listed, and no toast appears (UX-DR41).

**Given** Reports with no exports yet
**When** the Exports group renders
**Then** it reads "No exports yet. Make one from Exposure, Issues or Software with Export." (UX-DR45).⟧
Why: D3 — stored as evidence, listed in Reports → Exports; the answer report is relabelled.

**S137 · Story 6.5 AC · L1703 (D11)**
OLD: ⟦it uses the locked glossary, mono identifiers and the generation time, and is rendered by Typst — a pinned static binary run through `tools`, with no network access and the bundled Inter and IBM Plex Mono fonts⟧
NEW: ⟦it uses plain labels with the technical term beside them (machine-readable companions keep SBOM and VEX names), IBM Plex Mono for every ID, fingerprint and command, and the generation time, and is rendered by Typst — a pinned static binary run through `tools`, with no network access and the bundled IBM Plex Sans and IBM Plex Mono fonts ([ASSUMPTION] print face, EXPERIENCE Open item 5)⟧
Why: Inter is dropped; the glossary is replaced.

**S138 · Story 6.5 AC · L1705**
OLD: ⟦print palette, A4 by default with US Letter as an option (PROC2), a footer with report ID, generation time and page number on each page, severity as a text label and a colour, and table headers repeated on each page.⟧
NEW: ⟦the print-only light palette (`print-*` tokens, independent of the app theme), A4 by default with US Letter as an option (PROC2), a footer with report ID, time window, generation time and page number on each page, severity as its word plus the 4-step marker and a colour (no red), body 9.5pt and tables 8.5pt, and table headers repeated on each page (UX-DR46).⟧
Why: DESIGN Printed report.

**S139 · Story 6.5 AC · L1709**
OLD: ⟦**Then** export is available (it is a read action).⟧
NEW: ⟦**Then** export is available (it is a read action), and their exports are stored and attributed like anyone else's.⟧
Why: D3 — every export is stored.

**S140 · Story 6.6 title · L1711 (D4)**
OLD: ⟦### Story 6.6: Graph explorer and node inspector⟧
NEW: ⟦### Story 6.6: Exposure map traversal and inspector⟧
Why: D4.

**S141 · Story 6.6 user story · L1714–1715 (D4)**
OLD: ⟦I want to start from any CVE, package or artifact and explore its connections,
So that I can answer questions the blast-radius query doesn't ask directly.⟧
NEW: ⟦I want to move the Exposure map to any vulnerability, package or piece of software and follow its connections,
So that I can answer questions the first answer doesn't ask directly.⟧
Why: D4.

**S142 · Story 6.6 AC · L1719–1721**
OLD: ⟦**Given** the Graph explorer surface with no start node
**When** it opens
**Then** it shows the search-first empty state "Start from a CVE, package, or artifact" (UX-DR24).⟧
NEW: ⟦**Given** Exposure with no query (opened from the sidebar)
**When** it opens
**Then** the answer slot reads "Ask about a vulnerability, a package or a fingerprint." with examples ("CVE-2026-23012 · log4j-core@2.17.0 · sha256:…"), and the query button opens ⌘K (UX-DR40).⟧
Why: the no-query state replaces the Graph explorer empty state.

**S143 · Story 6.6 AC · L1723–1725, plus trail ACs (D4)**
OLD: ⟦**Given** a start node
**When** the user expands neighbours
**Then** `GET /api/v1/graph/neighbours` returns bounded, paginated neighbours with provenance, and the graph uses the Story 6.4 visual language (FR17, FR18).⟧
NEW: ⟦**Given** a node on the Exposure map
**When** the user clicks it or presses `Enter` on it
**Then** the map moves to that node: `GET /api/v1/graph/neighbours` returns bounded, paginated neighbours with provenance; the centre sits in the true centre, its contents on the left and where it runs and its copies on the right; the node you came from carries "Came from here"; packages with no known issues roll up ("212 more packages · No known issues") with a caveat line; and the map uses the Story 6.4 visual language with the centre-ring scale-in once (none under reduced motion) (FR17, FR18, UX-DR24)
**And** the question, query button, answer line, list column, Export, "Audit report for this answer" and the URL (`&from=` the previous step) follow the centre, so reloading or sharing the URL restores that map.

**Given** a moved map
**When** it renders
**Then** the trail above the map shows Back, the previous steps as link chips, the current step in bold and the hints "↵ Move the map · ⌫ Back"; Back, `Backspace` (outside text fields), any earlier step or the browser Back returns to that map with its selection; asking a new question with ⌘K starts a new trail (UX-DR24)
**And** the trail is a `nav` named "How you got here" with `aria-current="location"` on the current step; focus goes to the new centre and the new answer is announced politely ([ASSUMPTION], EXPERIENCE Open item 12).

**Given** a centre that is a package, a vulnerability other than the query, a place or a roll-up node, or a long trail
**When** this story is planned
**Then** their layouts follow the drawn software-centre rule and are confirmed with UX before Build (EXPERIENCE Open items 12 and 19).⟧
Why: D4 — traversal kept inside Exposure (ego view, trail, Back); the neighbours API stays.

**S144 · Story 6.6 AC · L1729–1730 (D4)**
OLD: ⟦**Then** the node inspector pins it and shows identity, knowledge and provenance, with actions open detail / view evidence / blast radius from here; `Esc` unpins (UX-DR18)
**And** hovering a node highlights its direct path.⟧
NEW: ⟦**Then** the inspector under the map pins it and shows identity (title with version and "Selected on the map"; Name, Fingerprint, Runs in, Copies, How it got it), What to do (the fix, the review-status chip, lime Review, grey Open software) and "How we know: Syft v… · Grype DB v… · checked N min ago"; on a map centred on a piece of software it adds Issues ("2 open: 1 Critical, 1 Low"), the lime action is Open software, Show only this stays grey and a hint reads "Click any node to move the map to it. Enter does the same from the keyboard."; `Esc` unpins (UX-DR18)
**And** hovering or focusing a node highlights its direct path.⟧
Why: the new inspector.

**S145 · Story 6.6 AC · L1732–1734**
OLD: ⟦**Given** any artifact, finding or CVE elsewhere in the UI
**When** the user chooses "Explore in graph" (row hover/focus, or `e`)
**Then** the explorer opens pre-centred on that node (UX-DR11, UX-DR24).⟧
NEW: ⟦**Given** an issue or piece of software elsewhere in the UI
**When** the user chooses See exposure, See the map or "See all N on the map"
**Then** Exposure opens for that subject (UX-DR11, UX-DR24); "Explore in graph" is retired, and the new meaning of `e` is open (EXPERIENCE Open item 13).⟧
Why: contextual entry.

**S146 · Story 6.6 AC · L1736–1738**
OLD: ⟦**Given** the explorer
**When** the Table reading is chosen
**Then** the current neighbourhood is fully readable as a table (UX-DR34).⟧
NEW: ⟦**Given** the Exposure map, moved or not
**When** Table is chosen
**Then** the current answer — on a moved map, the centre's neighbours: its issues, the packages they come from and where it runs — is fully readable as the Exposure table, keeping the selection (UX-DR34); the Table of a moved map is not drawn (EXPERIENCE Open item 19).⟧
Why: rename; D4.

#### Epic 7 — intro and Stories 7.1–7.4

**S147 · Epic 7 intro · L1762 (D8)**
OLD: ⟦Violations appear as neutral license findings in the same views, and the team triages them with the same decision model as vulnerability findings.⟧
NEW: ⟦Violations and warnings appear as licence issues — no severity, a scale icon and a "Licence" tag (and the word "Warning" for warnings) — in the Licences group at the top of Issues and Home, and the team reviews them with the same decision model as vulnerabilities; only violations count toward Needs attention (D8).⟧
Why: the Licences group and D8.

**S148 · Story 7.1 AC · L1780**
OLD: ⟦its backlog shows in the populating banner until it completes.⟧
NEW: ⟦its backlog shows in the Checking band until it completes.⟧
Why: rename.

**S149 · Story 7.1 AC · L1788**
OLD: ⟦it never shows as "no license issues" (NFR8).⟧
NEW: ⟦it never shows as "no licence issues" (NFR8).⟧
Why: British UI copy.

**S150 · Story 7.1 AC · L1790–1792**
OLD: ⟦**Given** Artifact detail
**When** it renders
**Then** the SBOM package list shows each package's license as a neutral license chip in mono (UX-DR9).⟧
NEW: ⟦**Given** Software detail
**When** its Packages cell and Packages tab render
**Then** each package's licence shows as the licence marker (scale icon + SPDX ID in `text-2`), never in a severity colour, and the Packages cell carries one licence line ("All licences are fine to use." when nothing violates or warns) (UX-DR9, UX-DR25).⟧
Why: the `license-chip` is gone and mono is for IDs only; the licence line is drawn in the mock.

**S151 · Story 7.3 AC · L1823**
OLD: ⟦**Given** Settings → License policy (admin only)⟧
NEW: ⟦**Given** Settings → Policy (licence policy, admin only)⟧
Why: panel name. (The default that treats unknown licences as `warning` is kept — D8.)

**S152 · Story 7.3 AC · L1835**
OLD: ⟦the backlog shows in the populating banner while it runs.⟧
NEW: ⟦the backlog shows in the Checking band while it runs.⟧
Why: rename.

**S153 · Story 7.4 title · L1841**
OLD: ⟦### Story 7.4: License findings in Posture, Findings and triage⟧
NEW: ⟦### Story 7.4: Licence issues in Home, Issues and review⟧
Why: rename.

**S154 · Story 7.4 user story · L1844**
OLD: ⟦I want license violations listed with vulnerability findings and triaged the same way,⟧
NEW: ⟦I want licence violations listed with vulnerability issues and reviewed the same way,⟧
Why: labels.

**S155 · Story 7.4 AC · L1856–1857 (D8)**
OLD: ⟦**And** when an admin turns it off, warnings stay visible but have no decision form, and existing decisions on warnings stay in history.⟧
NEW: ⟦**And** when an admin turns it off, warnings stay visible but have no review panel, and existing decisions on warnings stay in history
**And** whether or not warnings are reviewable, only `license_violation` issues that are Not reviewed yet count toward Needs attention and the Issues badge; `license_warning` issues never do (D8, UX-DR38, ARCH38).⟧
Why: D8.

**S156 · Story 7.4 AC · L1859–1861 (D1, D8)**
OLD: ⟦**Given** Posture, Findings and Artifact detail
**When** they render license findings
**Then** each shows the neutral license chip, never a severity hue or a KEV tag, placed in rank order by the documented rule from Story 5.1, and filterable by kind (vulnerability / license) (UX-DR9, UX-DR26).⟧
NEW: ⟦**Given** Home, Issues and Software detail
**When** they render licence issues
**Then** each sits in the Licences group at the top (violations and warnings together; hidden at 0), with the SPDX ID as the name, a "Licence" kind tag and the scale-icon licence marker, never a severity or an Actively exploited marker; line 2 of a Not-reviewed-yet violation reads "Licence · Needs a decision · <where>", and line 2 of a warning reads "Licence · Warning · <where>" (D8; styling per U19, O19); the Issues type filter All · Vulnerabilities · Licences keeps "Licences 0" visible (UX-DR9, UX-DR11, UX-DR26).⟧
Why: the Licences group (D1) and the "Warning" word (D8).

**S157 · Story 7.4 AC · L1863–1866**
OLD: ⟦**When** the analyst opens the triage drawer
**Then** the same drawer, statuses, justification rule, scope choice (this artifact or fleet-wide) and evidence recording apply as for vulnerability findings (FR14, FR27, Story 5.3, Story 5.4)
**And** the drawer shows the policy rule that produced the violation instead of a ranking explanation.⟧
NEW: ⟦**When** the analyst opens its Review tab
**Then** the same review panel, statuses, "Why?" rule, scope choice (All N places or Only this software) and evidence recording apply as for vulnerabilities (FR14, FR27, Story 5.3, Story 5.4, Story 5.8); the licence wording of the two questions is set by UX before Build (EXPERIENCE Open item 16)
**And** the technical-details block shows the policy rule that produced the issue instead of an order explanation.⟧
Why: no drawer; a UX gap.

#### Epic 8 — intro and Stories 8.1–8.4

**S158 · Epic 8 intro · L1874 (D2)**
OLD: ⟦Every answer carries a data-quality (DQ) score that the user can expand to see how it was calculated.⟧
NEW: ⟦Every piece of software and the fleet get a data-quality (DQ) score that is explained by its five parts, shown in Software detail (this epic) and in the audit report detail and its printed cover page (Epic 9); not on Home and never in list rows (D2).⟧
Why: D2.

**S159 · Story 8.1 AC · L1886 (D2)**
OLD: ⟦**Then** the scoring model (dimensions, inputs, weights, 0–100 scale and letter-grade bands) is recorded as an amendment to `architecture.md` and approved by the user before implementation.⟧
NEW: ⟦**Then** the scoring model (dimensions, inputs, weights, 0–100 scale and letter-grade bands, including which grades count as low — the UX shows D and below in `dq-muted` as a placeholder, EXPERIENCE Open item 11 — and what is shown before a score exists, Open item 32) is recorded as an amendment to `architecture.md` and approved by the user before implementation; the five dimensions keep the plain UI names Package lists, Coverage, Freshness, Extra sources and Vulnerability records.⟧
Why: the UX placeholders depend on the model.

**S160 · Story 8.2 title · L1906 (D2)**
OLD: ⟦### Story 8.2: Fleet data quality on Posture and Artifacts⟧
NEW: ⟦### Story 8.2: Fleet data-quality score and the Software detail meter⟧
Why: D2 — no Home or list-row surface; the Reports placements are in Epic 9.

**S161 · Story 8.2 user story · L1909–1910 (D2)**
OLD: ⟦I want data quality shown next to risk on every surface that gives an answer,
So that a low-quality answer is visible before someone acts on it.⟧
NEW: ⟦I want each piece of software and each audit report to say how much I can trust its numbers,
So that low-quality data is visible before someone acts on it.⟧
Why: D2.

**S162 · Story 8.2 AC · L1918–1920 (D2)**
OLD: ⟦**Given** Posture
**When** it renders
**Then** the co-stat band includes the fleet DQ score and grade in the `data-quality` colour, never a severity colour (UX-DR10, UX-DR22).⟧
NEW: ⟦**Given** Home
**When** it renders
**Then** it shows no data-quality reading (D2; it may join the Home Details tab in a later UX update — EXPERIENCE Open item 14), while the posture API still returns the fleet score for evidence packs (UX-DR10, UX-DR22).⟧
Why: D2 — not on Home.

**S163 · Story 8.2 AC · L1922–1924 (D2)**
OLD: ⟦**Given** Artifact detail and artifact or finding table rows
**When** they render
**Then** the detail header shows the score and grade, and table rows show a grade-only DQ badge (UX-DR10, UX-DR25).⟧
NEW: ⟦**Given** Software detail
**When** it renders
**Then** the Info list shows the data-quality value ("91 A−" in `dq`, accessible name in full), and the Data quality cell ("How much you can trust these numbers") shows the quality meter with the five parts, only the weakest emphasised and explained in one sentence with a link when there is something to do ("See them"), and the technical terms on one grey line and in `title` attributes (UX-DR10, UX-DR25)
**And** Software and Issues list rows carry no grade.⟧
Why: D2 — Software detail (Info + meter); not in list rows.

**S164 · Story 8.2 AC · L1926–1929 (D2)**
OLD: ⟦**Given** any DQ score or badge
**When** the user clicks or focuses it
**Then** it expands to the dimension breakdown, and each low dimension offers its corrective action (for example "connect feed", "rescan", "import bundle")
**And** lower grades use the `data-quality-muted` token (never opacity), keep their grade letter and never turn red (DESIGN.md).⟧
NEW: ⟦**Given** a low grade (bands from the approved Story 8.1 model)
**When** Software detail renders
**Then** the value and meter use `dq-muted`, keep their number and letter, never use opacity and never turn clay, amber or red; the two weakest parts each get one sentence of what it means; and a grey Check again (Story 2.11) is offered — a low grade takes no lime (UX-DR10, DESIGN.md).⟧
Why: the meter replaces the expandable badge.

**S165 · Story 8.2 AC · L1931–1933 (D2)**
OLD: ⟦**Given** blast-radius answers
**When** they render
**Then** the provenance footer includes the DQ score of the artifacts in the answer.⟧
NEW: ⟦**Given** blast-radius answers
**When** the API returns them
**Then** `provenance` includes the DQ scores of the software in the answer; Exposure shows no grade (D2 lists the surfaces).⟧
Why: D2 — Exposure is not a DQ surface; the API keeps the data.

**S166 · Story 8.3 AC · L1967**
OLD: ⟦Armoury sends no email, webhook, toast or badge;⟧
NEW: ⟦Armoury sends no email, webhook, toast or new-finding badge (the Issues nav badge counts Needs attention — decisions due — not new findings);⟧
Why: the agreed badge exception.

**S167 · Story 8.4 title · L1969**
OLD: ⟦### Story 8.4: Prometheus panel in Settings⟧
NEW: ⟦### Story 8.4: Prometheus panel in Settings → Signals⟧
Why: panel name.

**S168 · Story 8.4 AC · L1977–1979**
OLD: ⟦**Given** Settings → Metrics⟧
NEW: ⟦**Given** Settings → Signals⟧
Why: panel name.

**S169 · Story 8.4 AC · L1979**
OLD: ⟦each with a copy action (UX-DR28)⟧
NEW: ⟦the endpoint URL in a code block with Copy and each metric with a Copy action (UX-DR28, UX-DR42)⟧
Why: the code block component.

#### Epic 9 — intro and Stories 9.3–9.9

**S170 · Epic 9 intro · L1992**
OLD: ⟦The compliance lead generates a CRA pack in one click for any past window.⟧
NEW: ⟦The compliance lead generates a CRA pack (an "audit report" in the UI) in one click from Reports for any past window.⟧
Why: the UI label.

**S171 · Story 9.3 AC · L2051 (D2, D11)**
OLD: ⟦the PDF uses the renderer from Story 6.5 and the DESIGN.md "Printed report" rules, with the locked glossary, mono identifiers and the cover sheet first, carrying the coverage and data-quality statement (FR24)⟧
NEW: ⟦the PDF uses the renderer from Story 6.5 and the DESIGN.md "Printed report" rules (print-only light palette, IBM Plex Sans text and Plex Mono for IDs — [ASSUMPTION] print face, EXPERIENCE Open item 5 — severity as word + 4-step marker, no red), with plain labels and the technical term beside them, and the cover sheet first: coverage ("Covers 3,176 of 3,847 (82%)", with the not-checked software listed), then the data-quality block ("84 B+", the five parts with plain names and the technical term beside each, and the lowest part named with its reason), then Signature and a sign-off line (FR24, FR30, UX-DR46)⟧
Why: the glossary is replaced; Inter is dropped; D2 puts DQ second on the cover.

**S172 · Story 9.4 AC · L2078**
OLD: ⟦**And** Settings shows the public key in use,⟧
NEW: ⟦**And** Settings → Signals shows the signing public key in use,⟧
Why: panel name.

**S173 · Story 9.5 title · L2102**
OLD: ⟦### Story 9.5: Generate packs and verify signatures in the UI⟧
NEW: ⟦### Story 9.5: Generate audit reports and verify signatures in Reports⟧
Why: Evidence → Reports.

**S174 · Story 9.5 user story · L2105**
OLD: ⟦I want one click to generate a pack and one click to verify it,⟧
NEW: ⟦I want one click to generate an audit report, with its signature checked for me,⟧
Why: the UI label; verification shows automatically.

**S175 · Story 9.5 AC · L2110–2111**
OLD: ⟦**Given** the Evidence surface or `⌘K`
**When** the user clicks "Generate CRA pack"⟧
NEW: ⟦**Given** Reports or `⌘K`
**When** the user clicks the lime "Generate audit report"⟧
Why: labels.

**S176 · Story 9.5 AC · L2117, plus new ACs (D2)**
OLD: ⟦and retry re-runs only failed sections (UX-DR20).⟧
NEW: ⟦and retry re-runs only failed sections; the report appears in Reports → Audit reports when signed; a failure to start shows the inline error with Try again in the Generate row (UX-DR20, UX-DR41).

**Given** Reports with no audit reports
**When** it renders
**Then** the Audit reports group reads "No audit reports yet" with the lime Generate audit report (UX-DR45).

**Given** an audit report in Reports
**When** its Overview opens
**Then** row 1 shows Coverage when it was made beside Signature, and row 2 shows Data quality full width ("Data quality 84 B+ when it was made", the fleet quality meter with the weakest part and its reason, and the technical terms on one grey line) — the only place in the product the fleet five-part breakdown appears (FR30, UX-DR10, UX-DR27).

**Given** Home's "Across all software" band
**When** an audit report exists
**Then** its Audit report cell shows the latest report (last 12 months, signed, coverage) with Download and Preview, and on an all-clear Home the lime action is Audit report (UX-DR22, UX-DR45).⟧
Why: Reports states, D2's Reports DQ row, the Home cell.

**S177 · Story 9.5 AC · L2119–2121**
OLD: ⟦**Given** a pack card
**When** the user clicks "Verify signature"
**Then** the UI shows the result and signer identity, and gives a copyable offline verification command (cosign with the operator public key by default; the keyless command when keyless signing is enabled) (UX-DR19).⟧
NEW: ⟦**Given** an audit report in Reports (detail tabs Overview · Files · Audit trail; files pack.pdf, sboms.tar.gz "Package lists … SBOM", vex.json "review decisions … VEX")
**When** its Overview opens
**Then** the Signature cell shows "Signature verified" with the signer key, and the offline command (cosign with the operator public key by default; the keyless command when keyless signing is enabled) in a code block with Copy — "Auditors can run this themselves, without Armoury."; when the signature does not verify, an error band names the file and the reason, links to the audit-trail entry for the signing, and hides no download (UX-DR19).⟧
Why: the signature-status component; no pack card.

**S178 · Story 9.5 AC · L2124 and L2129 (both occurrences)**
OLD: ⟦**When** an auditor opens Evidence⟧
NEW: ⟦**When** an auditor opens Reports⟧
Why: rename (apply to both lines).

**S179 · Story 9.5 AC · L2134–2136 (D3)**
OLD: ⟦**Given** a blast-radius answer
**When** the user chooses "Export evidence pack"
**Then** a pack scoped to that answer is generated with the same pipeline, caveats and signing (UX-DR21).⟧
NEW: ⟦**Given** an Exposure answer
**When** the user chooses "Audit report for this answer"
**Then** the Story 6.5 PDF answer report is produced and stored in Reports → Exports (D3); no evidence pack is scoped to a single answer (UX-DR21; confirm — O3).⟧
Why: D3 — "Audit report for this answer" is the relabelled Story 6.5 answer report (architecture recommendation A: no new pack scope).

**S180 · Story 9.6 AC · L2160–2162 (D9)**
OLD: ⟦**Given** the Evidence surface
**When** it renders the verification result⟧
NEW: ⟦**Given** Reports → Audit trail (Story 5.5)
**When** it renders the verification result⟧
Why: D9.

**S181 · Story 9.7 AC · L2174**
OLD: ⟦an admin can set a longer value in Helm values or Settings,⟧
NEW: ⟦an admin can set a longer value in Helm values or Settings → Policy (retention),⟧
Why: panel name.

**S182 · Story 9.9 AC · L2246–2247 (D9)**
OLD: ⟦**When** verification runs in the Evidence surface or with the offline command⟧
NEW: ⟦**When** verification runs in Reports → Audit trail or with the offline command⟧
Why: D9.

**S183 · Story 9.9 AC · L2247 (D9)**
OLD: ⟦and the Evidence surface shows the anchoring mode, the latest anchored checkpoint and any pending anchors⟧
NEW: ⟦and Reports → Audit trail shows the anchoring mode, the latest anchored checkpoint and any pending anchors⟧
Why: D9.

#### Epics 10–11

**S184 · Story 10.4 AC · L2344**
OLD: ⟦**Then** Posture populates with findings, enrichment and runtime coverage⟧
NEW: ⟦**Then** Home and Software populate with issues, enrichment and runtime coverage⟧
Why: rename (the L2348 script steps keep the API terms).

**S185 · Story 11.1 AC · L2367**
OLD: ⟦**Given** Settings → CI tokens (admin only)⟧
NEW: ⟦**Given** Settings → Access (CI tokens, admin only)⟧
Why: panel name; the token is shown once in a code block with Copy (UX-DR42).

**S186 · Story 11.2 AC · L2417**
OLD: ⟦**Then** it appears in Artifacts with source "CI upload",⟧
NEW: ⟦**Then** it appears in Software with source "CI upload" (grouping and label set by UX before Build, EXPERIENCE Open item 28),⟧
Why: rename; a UX gap.

**S187 · Story 11.3 AC · L2444**
OLD: ⟦**Given** Artifact detail
**When** an artifact has several sources⟧
NEW: ⟦**Given** Software detail
**When** a piece of software has several sources⟧
Why: rename.

**S188 · Story 11.4 AC · L2456**
OLD: ⟦**Given** Settings → CI policy (admin only)⟧
NEW: ⟦**Given** Settings → Policy (CI policy, admin only)⟧
Why: panel name.

**S189 · Story 11.4 AC · L2470**
OLD: ⟦**And** it always prints the URL, including on failure or timeout.⟧
NEW: ⟦**And** it always prints the URL, which lands on the piece of software in Software, including on failure or timeout; where the verdict and its history show in Software detail is set by UX before Build (EXPERIENCE Open item 28, UX-DR48).⟧
Why: a UX gap.

#### Kept as domain/API terms (no edit, by design)

- API paths and schemas: `/api/v1/posture`, `/api/v1/blast-radius-queries`, `/api/v1/artifacts/{id}`,
  `/api/v1/findings/{id}`, `/api/v1/graph/neighbours`, `/api/v1/evidence/verification`, `provenance`,
  `caveats[]` (the caveat *strings* are user-facing and change: S117, S118).
- Data and enums: `Finding`, `license_violation`, `license_warning`, `untriaged` / `not_affected` /
  `mitigated` / `accepted` / `fix_planned` (ARCH15), artifact types `image` / `package` /
  `oci_artifact` / `filesystem`, digest (in API and identity contexts), KEV, EPSS, CNA, OSV, SBOM,
  VEX, CVE.
- Modules and metrics: `posture`, `ranking`, `blastradius`, `graph`, `triage`, `evidence`, `packs`;
  `armoury_findings_created_total`, `armoury_findings_open{triage_status}`,
  `rbac.auditorCanGeneratePacks`.
- Planning prose and titles that name the domain, not a screen: Epic titles 1–11; Stories 1.3
  ("working posture view"), 2.1, 2.4, 2.5, 2.12 ("install-to-posture"), 3.5 ("Shipped-vs-running
  reconciliation"), 6.1, 6.2, 6.7, 9.1–9.4, 9.6–9.9 ("evidence pack", "CRA pack"), 10.x, 11.x
  ("artifact"). EXPERIENCE's glossary allows these in docs and APIs.

### 4.5 Epic 1 context

<!-- file: _bmad-output/implementation-artifacts/epic-1-context.md -->

The file says "Regenerate with compile-epic-context if planning docs change". **Recommended:**
regenerate it after `epics.md` and `architecture.md` are edited. The exact edits below apply if it is
patched by hand instead.

**C1 · Goal · L7**
OLD: ⟦reaches a themed, accessible, keyboard-first shell with an honest empty Posture page.⟧
NEW: ⟦reaches an accessible, keyboard-first shell — labelled black sidebar, Light (default) and Dark themes — with an honest empty Home page.⟧
Why: retired themes and label.

**C2 · Stories · L15–16**
OLD: ⟦- Story 1.5: Design tokens and the three themes
- Story 1.6: App shell, navigation and the empty Posture page⟧
NEW: ⟦- Story 1.5: Design tokens and the Light and Dark themes
- Story 1.6: App shell, sidebar navigation and the empty Home page⟧
Why: title changes.

**C3 · Requirements & Constraints · L27**
OLD: ⟦State is never shown by colour alone.⟧
NEW: ⟦State is never shown by colour alone. Single-key shortcuts can be turned off (2.1.4). Field edges are ≥3:1 at rest (1.4.11). Content reflows at 400% zoom and 200% text.⟧
Why: the new accessibility floor.

**C4 · Requirements & Constraints · L28**
OLD: ⟦≥1280px is the primary width. 1024–1279px degrades tolerantly. Below 1024px is best-effort read-only.⟧
NEW: ⟦≥1280px: full sidebar and three columns. 1024–1279px: icon rail, list and detail side by side. Below 1024px: icon rail, list and detail stacked with a Back link, fully operable.⟧
Why: the responsive rule.

**C5 · Technical Decisions, Frontend · L81**
OLD: ⟦  - The palette lives in `lib/command/` and the token maps in `lib/theme/`.⟧
NEW: ⟦  - The palette lives in `lib/command/`, the token maps in `lib/theme/`, and the brand-layer components every surface shares (shell, list row, markers, status chip, inline error, code block) in `lib/design/`.⟧
Why: mirrors A30/A40.

**C6 · UX › Tokens · L94–100**
OLD: ⟦  - There are three dark themes: Forge (default), High Signal and Gunmetal. There is no light mode and no OS-preference detection.
  - Semantic roles map onto shadcn CSS variables using the exact DESIGN.md values, including `rail-*`, `data-quality`, `data-quality-muted` and `node-inactive-border`. Components use roles only, never raw hex or theme-suffixed variables, and a lint enforces this.
  - Elements that contain text are never shown with opacity below 1; use the muted tokens instead.
  - Contrast tests:
    - AA (4.5:1) for all text roles in Forge and Gunmetal.
    - AAA for High Signal primary text, and ≥7:1 for High Signal muted text.
    - 4.5:1 for `data-quality-muted` and 3:1 for `node-inactive-border` in all three themes.⟧
NEW: ⟦  - Two themes over the same roles: Light (default, unsuffixed tokens) and Dark (`-dark`); new users get Light; no OS-preference detection.
  - Roles map onto shadcn variables per the DESIGN.md "shadcn mapping" table, plus `--paper`, `--dq`, `--dq-muted` and `--dq-wash`; `print-*` tokens feed only Typst. Components use roles only, never raw hex or theme-suffixed variables, and a lint enforces this.
  - No opacity below 1 on elements with text, except disabled controls at 0.45.
  - Contrast tests:
    - AA 4.5:1 for every text pair in the DESIGN.md Contrast table, in both themes (lowest 4.9:1), including `dq` and `dq-muted`.
    - ≥3:1 for `field-border` and the focus ring; markers below 3:1 only beside a word.⟧
Why: the old themes and tokens are gone.

**C7 · UX › Typography · L102–105**
OLD: ⟦  - Inter Display for numerals and titles, Inter for all UI text, IBM Plex Mono for every identifier. Numerals use `tabular-nums`.
  - Use the DESIGN.md sizes exactly, with no intermediate sizes.
  - Radii: 5/8/9/12/11. Spacing: rail 58, gutter 52, zone gap 48–56, data row 30, stat gap 44.
  - Depth comes from tonal layering and 1px borders. Shadows are used only on overlays.⟧
NEW: ⟦  - IBM Plex Sans for everything; Plex Sans Bold Italic for the wordmark only; Plex Mono only for IDs, fingerprints, commands and keys; all self-hosted (OFL). Numerals use `tabular-nums` in data.
  - Nine sizes 12 · 13 · 14 · 15 · 17 · 20 · 24 · 30 · 40, plus the 22px wordmark; weights 400/500/600. Sentence case; uppercase only on button labels; no eyebrows.
  - Radii 3 / 4 / 6 / 10, pill, full. Layout: sidebar 252, list column 376 / 500 / 420, gutter 32, detail cell 30 × 34, rows ≈78 / 72px; one density.
  - Depth is tone + 1px rules; the only shadow is the ⌘K dialog.⟧
Why: the new type and spacing.

**C8 · UX › Shell · L107–110**
OLD: ⟦  - A 58px icon rail holds 7 surfaces, with Settings pinned to the bottom. The active item gets a raised tint and a 2px accent indicator. Tooltips show on hover and focus. There is no top nav.
  - Every surface has a page header row with a breadcrumb, the blast-radius search field (opens the palette) and a compact theme switcher (swatch + name).
  - The heading block is left-aligned: eyebrow → title → subtitle (≤620px) → 46×2px accent rule.
  - Empty surfaces show a calm line with no illustrations. The empty Posture page says that no sources are connected yet.⟧
NEW: ⟦  - A 252px black sidebar: wordmark, "Search or jump to… ⌘K" field, Home · Software · Issues · Exposure · Reports, a divider, Settings · Help, and the user menu (name, role, Personal settings, Sign out) at the foot; the active item is lime. The Issues badge (Needs-attention count) arrives in Story 2.10. Help opens a placeholder until its screen is designed.
  - No top nav and no page header. Three-column master-detail; page title = sidebar label + one summary line.
  - Below 1280px the sidebar becomes an icon rail; below 1024px list and detail stack with a Back link.
  - Empty surfaces show a calm line with no illustrations. The empty Home says that no sources are connected yet.⟧
Why: the new shell.

**C9 · UX › Settings · L111**
OLD (line starts): ⟦- **Settings:** an in-page left list⟧
NEW: ⟦- **Settings:** a panel list in the list column, grouped as Connections, Sources, Policy, Access, Signals and Personal, with each panel at `/settings/<panel>`. Epic 1 fills Personal (the Light/Dark theme switch, instant apply; the shortcut list; the single-key shortcut switch) and Access (read-only auth configuration, users/roles).⟧
Why: Feeds → Sources; no live preview.

**C10 · UX › Loading and errors · L113**
OLD: ⟦Never show a bare spinner.⟧
NEW: ⟦Never show a bare spinner. A failed save or start shows an inline error line with Try again in the panel where it happened, never a toast.⟧
Why: inline errors.

**C11 · UX › Palette · L115–117**
OLD: ⟦  - `⌘K`/`Ctrl+K` opens a shadcn `Command` palette with groups Answers → Navigate → Actions → Recent. Results are announced through `aria-live`.
  - It includes "Switch theme…" with live preview.
  - The no-match copy is "No matches. Try a CVE ID, package@version, or digest."⟧
NEW: ⟦  - `⌘K`/`Ctrl+K` (and the sidebar search field) opens a 660px shadcn `Command` dialog with groups Issues · Software · Exposure · Actions (Recent is not drawn); it traps focus, dims the page and returns focus on `Esc`. Results are announced through polite `aria-live`.
  - It includes "Switch theme…" (Light / Dark).
  - The no-match copy is "No matches. Try a CVE ID, package@version or fingerprint."⟧
Why: the new palette.

**C12 · UX › Keys · L120**
OLD: ⟦  - `g`+`p/b/g/a/f/e` navigates.⟧
NEW: ⟦  - `g` + a surface letter navigates (letters set by UX before Story 1.8 Build, EXPERIENCE Open item 13); `J`/`K` move, `/` focuses search, `⌘↵` saves and goes to the next, `x` exports.⟧
Why: the old letters map retired surfaces.

**C13 · UX › Keys · L123**
OLD: ⟦  - Shortcuts never fire while focus is in a text input.⟧
NEW: ⟦  - Single-key shortcuts never fire while focus is in a text field and can be turned off in Settings → Personal; `⌘K` and `⌘↵` stay on.⟧
Why: WCAG 2.1.4.

**C14 · UX › Copy · L126**
OLD: ⟦  - The locked glossary and the lowercase triage statuses are defined once.⟧
NEW: ⟦  - The plain-label glossary (plain label first, technical term small and grey) and the five review statuses (Not reviewed yet, Not impacted, Fix planned, Mitigated, Risk accepted) are defined once; British English; retired labels fail a lint.⟧
Why: the glossary is replaced.

**C15 · UX › Banned patterns · L129, L130, L134, L136 (four lines)**
OLD: ⟦  - in-product notifications or toasts used as alerts; Toast may only confirm the user's own action⟧ → NEW: ⟦  - in-product notifications and toasts (as alerts or for save results)⟧
OLD: ⟦  - new-finding badges and celebratory animation⟧ → NEW: ⟦  - new-finding badges (the Needs-attention badge is allowed), celebratory animation, a Compact density toggle⟧
OLD: ⟦  - overlays deeper than a drawer plus one dialog, through one shared overlay component⟧ → NEW: ⟦  - any modal besides the ⌘K dialog, and any drawer (one shared overlay component)⟧
OLD: ⟦  - more than one primary button per surface⟧ → NEW: ⟦  - more than one lime primary action per view; lime outside its agreed jobs; red anywhere⟧
Why: the new banned list (UX-DR36).

**C16 · Cross-Story Dependencies · L145–146**
OLD: ⟦  - 1.6 adds the theme picker and the page header.
  - 1.8 adds palette theme switching and makes the 1.6 header search open the palette.⟧
NEW: ⟦  - 1.6 adds the sidebar, the user menu and the Settings → Personal theme switch.
  - 1.8 adds palette theme switching, makes the 1.6 sidebar search field open the palette, and adds the single-key shortcut switch.⟧
Why: there is no page header.

**C17 · Hooks for later epics · L149–150**
OLD: ⟦  - Posture setup actions and the empty state arrive in Stories 2.2 and 3.2.
  - Blast-radius answers in the palette arrive in Story 6.3.⟧
NEW: ⟦  - Home setup actions and the empty state arrive in Stories 2.2 and 3.2; the Issues badge arrives in Story 2.10.
  - Exposure answers in the palette arrive in Story 6.3.⟧
Why: renames.

### 4.6 Implementation readiness

<!-- file: _bmad-output/planning-artifacts/implementation-readiness.md -->

A historical gate record: its findings are not rewritten; it is marked stale so nobody reads the PASS
as covering the new UX.

**R1 · front matter `history` · after L7**
OLD (anchor, kept): ⟦  - "2026-11-05/06 fixed by Correct Course (sprint-change-proposal-2026-11-05.md, decisions R1–R11); four independent gate reruns; final rerun: no blockers, two text concerns fixed and checked."⟧
NEW: ⟦  - "2026-11-07 UX spines replaced by ux-Armoury-2026-11-06 (supersedes ux-Armoury-2026-06-12) and FR32/FR33 added (sprint-change-proposal-2026-11-07.md); this verdict predates them (the plan is now 11 epics, 79 stories) — rerun readiness after the Correct Course is applied."⟧
Why: the inputs (L13–14) point at the superseded spines.

**R2 · verdict banner · L20**
OLD: ⟦**Current verdict: PASS (2026-11-06).**⟧
NEW: ⟦**Current verdict: PASS (2026-11-06) — stale: assessed against ux-Armoury-2026-06-12, which ux-Armoury-2026-11-06 superseded; rerun after the 2026-11-07 Correct Course.**⟧
Why: honest status.

**R3 · UX heading · L73**
OLD: ⟦### UX⟧
NEW: ⟦### UX (historical — refers to ux-Armoury-2026-06-12: Forge/Gunmetal, page header, DQ badge opacity; superseded)⟧
Why: the bullets cite the retired design (L74–82).

### 4.7 Sprint status

<!-- file: _bmad-output/implementation-artifacts/sprint-status.yaml -->

Keys follow `sprint_plan.py` (`<epic>-<story>-<slug of the title, 60 characters>`). Every story is
`backlog` and no story file exists for a retitled story, so renaming keys loses nothing.

**Y1 · header · L32**
OLD: ⟦last_updated: 11-06-2026 00:18⟧
NEW: ⟦last_updated: 11-07-2026 <time the change is applied>⟧
Why: records the change.

**Y2 · retitled story keys (status stays `backlog`)**

| Line | OLD key | NEW key |
|---|---|---|
| L43 | `1-5-design-tokens-and-the-three-themes` | `1-5-design-tokens-and-the-light-and-dark-themes` |
| L44 | `1-6-app-shell-navigation-and-the-empty-posture-page` | `1-6-app-shell-sidebar-navigation-and-the-empty-home-page` |
| L59 | `2-9-posture-summary-populating-coverage-and-freshness` | `2-9-home-summary-checking-coverage-and-freshness` |
| L60 | `2-10-posture-findings-severity-band-and-findings-table` | `2-10-home-needs-attention-and-open-issues-by-severity` |
| L61 | `2-11-artifacts-list-and-artifact-detail` | `2-11-software-list-and-software-detail` |
| L72 | `3-6-runtime-coverage-on-posture-and-minute-29-with-the-agent` | `3-6-runtime-coverage-on-home-and-software-and-minute-29-with-the` |
| L82 | `4-7-honest-feed-staleness-across-posture-and-findings` | `4-7-honest-feed-staleness-across-home-and-issues` |
| L87 | `5-1-deterministic-explainable-ranking` | `5-1-deterministic-explainable-issue-order` |
| L88 | `5-2-findings-workbench-and-ranked-posture-table` | `5-2-issues-list-severity-groups-filters-and-the-home-summary` |
| L90 | `5-4-triage-drawer` | `5-4-review-panel-in-the-issues-detail-column` |
| L91 | `5-5-evidence-trail-surface` | `5-5-audit-trail-in-reports-and-on-every-item` |
| L92 | `5-6-emit-vex-from-triage-decisions` | `5-6-emit-vex-from-review-decisions` |
| L94 | `5-8-fleet-wide-triage-decisions` | `5-8-review-scope-all-places-or-only-this-software` |
| L100 | `6-3-blast-radius-surface-answer-and-table-from-k` | `6-3-exposure-surface-answer-and-table-from-k` |
| L101 | `6-4-blast-radius-graph-reading` | `6-4-exposure-map-reading` |
| L102 | `6-5-export-blast-radius-and-posture-answers` | `6-5-export-views-as-stored-evidence-and-the-answer-report` |
| L103 | `6-6-graph-explorer-and-node-inspector` | `6-6-exposure-map-traversal-and-inspector` |
| L111 | `7-4-license-findings-in-posture-findings-and-triage` | `7-4-licence-issues-in-home-issues-and-review` |
| L116 | `8-2-fleet-data-quality-on-posture-and-artifacts` | `8-2-fleet-data-quality-score-and-the-software-detail-meter` |
| L118 | `8-4-prometheus-panel-in-settings` | `8-4-prometheus-panel-in-settings-signals` |
| L126 | `9-5-generate-packs-and-verify-signatures-in-the-ui` | `9-5-generate-audit-reports-and-verify-signatures-in-reports` |

Why: keys are derived from titles; stale keys would fail `sprint_plan.py` reconciliation.

**Y3 · new stories · after L83**
OLD (anchor, kept): ⟦  4-8-prove-one-hour-re-evaluation-at-the-scale-anchor: backlog⟧
NEW: ⟦  4-9-end-of-life-data-for-packages: backlog
  4-10-verify-artifact-signatures-against-trusted-signers: backlog⟧
Why: D10 — Stories 4.9 and 4.10.

**Y4 · check after applying**
Run `uv run .agents/skills/bmad-sprint-planning/scripts/sprint_plan.py generate --epic-file _bmad-output/planning-artifacts/epics.md --status-file _bmad-output/implementation-artifacts/sprint-status.yaml --stories-dir _bmad-output/implementation-artifacts --project Armoury --date 2026-11-07 --dry-run`
and `… sprint_plan.py validate --status-file _bmad-output/implementation-artifacts/sprint-status.yaml`;
both must report 11 epics and 79 stories with no orphan or missing key.
Why: proves the keys match the edited `epics.md`.

### 4.8 UX spines (UI/UX)

The approved spines change only where D3, D8, D9 and D10 require it. The UX owner applies these edits,
records a memlog entry and re-runs the spine token check. Open UX details are added as Open items
36–39 (numbers 1–35 stay).

<!-- file: _bmad-output/planning-artifacts/ux-designs/ux-Armoury-2026-11-06/EXPERIENCE.md -->

#### EXPERIENCE.md

**U1 · Information Architecture table, Reports row · L51 (D9)**
OLD: ⟦| Reports | `/reports/<id>` | Audit reports and exports, both kept as evidence, nothing else (FR19, FR21–25). | Generate audit report |⟧
NEW: ⟦| Reports | `/reports/<id>` | Audit reports, exports (both kept as evidence) and the fleet-wide audit trail, nothing else (FR19, FR21–25, NFR11). | Generate audit report |⟧
Why: D9 grows Reports to three groups.

**U2 · Home, Needs attention rule · L58 (D8)**
OLD: ⟦Every licence issue that is Not reviewed yet also needs attention.* Rows use⟧
NEW: ⟦Every licence violation that is Not reviewed yet also needs attention; licence warnings never do.* Rows use⟧
Why: D8.

**U3 · Issues, Grouping · L71 (D8)**
OLD: ⟦**Licences** at the top (hidden when 0 — licence issues are rare and each needs a decision), then⟧
NEW: ⟦**Licences** at the top (hidden when 0 — licence issues are rare and each needs a decision); the group holds licence violations and licence warnings, and a warning row says "Warning" on line 2 ("Licence · Warning · <where>") and never needs attention; then⟧
Why: D8 — warnings show in the Licences group with the word "Warning".

**U4 · Reports, groups · L114 (D9)**
OLD: ⟦- **Audit reports N** and **Exports N**, nothing else. New report types (for example a management summary) are new scope and need Correct Course first.⟧
NEW: ⟦- **Audit reports N**, **Exports N** and **Audit trail**, nothing else (Audit trail added 2026-11-07, Correct Course D9). New report types (for example a management summary) are new scope and need Correct Course first.⟧
Why: D9.

**U5 · Reports, new Audit trail bullet · after L115 (D9)**
OLD (anchor, kept): ⟦Like audit reports, stored exports are never edited or removed by hand.⟧
NEW: ⟦
- **Audit trail** (fleet-wide, decided 2026-11-07): every ledger entry, newest first — type, subject (plain label with its technical ID small), actor, time, tool and feed versions — with filters by type, subject and time window and the pager. Its detail column shows the chain verification ("Chain intact — N entries, verified 4 min ago", or the first broken entry), the latest signed checkpoint, and the anchoring status (mode, latest anchored checkpoint, pending anchors). Per-item trails stay as tabs (a software's Audit trail, an issue's History, a report's Audit trail), each linking to this group filtered to that subject. Not drawn yet (Open item 36).⟧
Why: D9 — the fleet-wide group with verification, checkpoint and anchoring status.

**U6 · Settings panels · L122 (D10)**
OLD: ⟦**Sources** (feed status and history, bundle import FR10) · **Policy** (licence policy FR27, CI policy, retention — never below the 24-month floor, FR23)⟧
NEW: ⟦**Sources** (feed status and history, bundle import FR10, end-of-life data FR33) · **Policy** (licence policy FR27, signature policy — trusted keys and keyless signer identities FR32, CI policy, retention — never below the 24-month floor, FR23)⟧
Why: D10 needs a home for trust configuration and the end-of-life source.

**U7 · Glossary, Reports row · L160 (D9)**
OLD: ⟦| Reports | Evidence packs and exports | Docs; file names (`pack.pdf`) |⟧
NEW: ⟦| Reports | Evidence packs, exports and the evidence trail | Docs; file names (`pack.pdf`) |⟧
Why: D9.

**U8 · Glossary, Audit report row · L161 (D3)**
OLD: ⟦| Audit report | Evidence pack (CRA pack) | File names and the verification command |⟧
NEW: ⟦| Audit report | Evidence pack (CRA pack) | File names and the verification command. Exception: "Audit report for this answer" (Exposure) is the PDF answer report, not an evidence pack; it is stored under Reports → Exports (Correct Course D3) |⟧
Why: D3 relabels the answer report; the label otherwise means an evidence pack (O20).

**U9 · Glossary, new row · after L182 (D8)**
OLD (anchor, kept): ⟦| Needs a decision | Licence-policy violation, untriaged | Second line of a licence row that is Not reviewed yet ("AGPL-3.0 — Licence · Needs a decision · report-render") |⟧
NEW: ⟦| Warning | Licence-policy warning (`license_warning`; the policy marks the licence "warning", including unknown licences by default) | Second line of a licence warning row ("<licence> — Licence · Warning · <where>"); never counts toward Needs attention |⟧
Why: D8.

**U10 · Component Patterns, Needs attention row · L202 (D8)**
OLD: ⟦Every licence issue that is Not reviewed yet also needs attention. A Mixed issue stays in Needs attention⟧
NEW: ⟦Every licence violation that is Not reviewed yet also needs attention; licence warnings never do. A Mixed issue stays in Needs attention⟧
Why: D8.

**U11 · Flow 3 step 3 · L398 (D9)**
OLD: ⟦Marta reads the audit trail meanwhile (a software's Audit trail tab, an issue's History)⟧
NEW: ⟦Marta reads the audit trail meanwhile (Reports → Audit trail for the whole fleet, or a software's Audit trail tab, an issue's History)⟧
Why: D9.

**U12 · Coverage table, Reports row · L424 (D9)**
OLD: ⟦| Reports | Flow 2 (step 6, Exports), Flow 3 (data quality: step 5) |⟧
NEW: ⟦| Reports | Flow 2 (step 6, Exports), Flow 3 (step 3, Audit trail; data quality: step 5) |⟧
Why: D9.

**U13 · Stated-need table, new rows · after L437 (D10)**
OLD (anchor, kept): ⟦| Licence policy and findings (FR26–28) | Settings → Policy, Issues Licences group |⟧
NEW: ⟦| Artifact signature verification (FR32) | Software detail Info "Signed"; Settings → Policy (signature policy). Words for each signature state not written (Open item 38) |
| End-of-life data for packages (FR33) | Software detail Packages cell and tab; Settings → Sources. End-of-life lines other than "No package is past its end of life." not written (Open item 38) |⟧
Why: D10 — traceability for the new FRs.

**U14 · Changes, Navigation bullet · L452 (D9)**
OLD: ⟦Evidence becomes Reports (audit reports + exports only);⟧
NEW: ⟦Evidence becomes Reports (audit reports, exports and, from 2026-11-07, the fleet-wide audit trail);⟧
Why: D9.

**U15 · Changes, new bullet · after L470 (D8, D9, D10)**
OLD (anchor, kept): ⟦- **Primary users:** Priya and Marta, plus **Tom Reid, Head of Engineering** (Admin role), as an equal-weight non-technical protagonist.⟧
NEW: ⟦- **Correct Course 2026-11-07 (sprint-change-proposal-2026-11-07.md):** licence warnings show in the Licences group with the word "Warning" and never count toward Needs attention (D8); Reports gains the fleet-wide Audit trail group (D9); "Signed" and end-of-life data are v1 scope as PRD FR32 and FR33, with their settings in Policy and Sources (D10); "Audit report for this answer" is the PDF answer report, stored under Exports (D3).⟧
Why: keeps the change list complete.

**U16 · Open item 10 · L485 (D5)**
OLD: ⟦10. [ASSUMPTION] **Admin includes the analyst's actions** (review, audit report generation), which is why Tom Reid (Admin, decided 2026-11-07) sees Review and Review all 3.⟧
NEW: ⟦10. **Resolved 2026-11-07:** admin includes the analyst's actions (PRD NFR6, roles are ordered; architecture: each operation declares a minimum role), which is why Tom Reid (Admin) sees Review and Review all 3.⟧
Why: P21 closes it.

**U17 · Open item 26 · L507 (D1, D3)**
OLD: ⟦26. **PRD FR13** wording (KEV first, then EPSS-weighted) vs severity grouping; PRD glossary terms vs plain labels. **PRD FR19** wording must say exports are stored in Reports as evidence (audit-trail entry, audit-report retention).⟧
NEW: ⟦26. **Resolved 2026-11-07** (Correct Course): PRD FR13 now describes the severity groups; the PRD glossary gains UI labels; FR19 says exports are stored as evidence with evidence-pack retention.⟧
Why: P12, P18, P23 close it.

**U18 · Open items, new 36–39 · after L516**
OLD (anchor, kept): ⟦35. **Retired label "Running":** the ban should read "Running as a group or status label", since the hint "Not seen running…" and the glossary's "Running replicas" use the word.⟧
NEW: ⟦36. **Reports → Audit trail** (D9) is not drawn: the list rows, the filters, the verification cell, the checkpoint and anchoring cells, and the broken-chain state.
37. **Licence warning row** (D8): the "Warning" word's exact placement and style (proposed: line 2 in {colors.text-2}, never amber or clay); and the review-panel copy for warnings (with Open item 16).
38. **Signed and end-of-life words** (FR32, FR33): the words for each signature state other than "Yes" (not signed, signed by an untrusted signer, check failed, not checked for this type, no signature policy); end-of-life lines other than "No package is past its end of life."; the Signature policy panel and the end-of-life source in Settings.
39. **"Audit report for this answer"** (D3): confirm the label, since "Audit report" otherwise means an evidence pack.⟧
Why: records the open UX details this Correct Course creates.

<!-- file: _bmad-output/planning-artifacts/ux-designs/ux-Armoury-2026-11-06/DESIGN.md -->

#### DESIGN.md

**U19 · Components, List row · L703 (D8)**
OLD: ⟦Licence rows carry a small {components.kind-tag} "Licence". |⟧
NEW: ⟦Licence rows carry a small {components.kind-tag} "Licence"; a licence warning row adds the word "Warning" on line 2 in {colors.text-2} — never amber or clay, because a warning is neither a severity nor a stale state ([ASSUMPTION], EXPERIENCE Open item 37). |⟧
Why: D8 — the "Warning" word needs a visual rule.

**U20 · Components, new Audit trail row · after the Signature status row (L737) (D9)**
OLD (anchor, kept): ⟦a link to the audit trail entry in {colors.forest-ink}; the download buttons stay. |⟧
NEW: ⟦| Audit trail (Reports) | [ASSUMPTION, EXPERIENCE Open item 36] The Reports → Audit trail group uses the standard list row (line 1: what happened and its subject; line 2: actor · time · tool and feed versions; right column: the entry type) and the {components.pager}. The chain verification reuses the {components.signature-status} visuals: a {colors.forest-wash} disc with a tick and "Chain intact — N entries, verified …" in {typography.body}; a broken chain uses the {components.error-band} naming the first broken entry with a {colors.forest-ink} link to it. Checkpoint and anchoring status are cells with a definition list; the offline verification command sits in a {components.code-block}. |⟧
Why: D9 needs a visual rule; it reuses existing components and adds no token.

## 5. Implementation handoff

### Scope classification

**Major.** The change needs the PM (PRD: two new FRs, a new primary user and journey, five FRs
reworded), the Architect (four new decisions: issue read model, stored exports, signature
verification, end-of-life data) and the UX designer (D8/D9/D10 spine edits), as well as the PO/Dev
backlog work (every UX-DR, 21 retitles, 54 changed stories, 2 new stories, 23 new sprint keys or key
changes). It is not a replan of the epic structure: no epic is added, removed or reordered, and no
code is rolled back.

### Who applies what, in this order

| Step | Owner (skill) | Applies | Notes |
|---|---|---|---|
| 1 | PM — `bmad-prd` (update) | P1–P27 | PRD `updated` and decision log in the same change. |
| 2 | UX designer — `bmad-ux` (update) | U1–U20 | Add a memlog entry ("Correct Course 2026-11-07 applied: D3, D8, D9, D10"), set `updated`, re-run the spine token check; the Audit trail group and Warning word stay Open items 36–37 until drawn. |
| 3 | Architect — `bmad-architecture` (update) | A1–A57 | ARCH40/ARCH41 details stay open until the Story 4.9/4.10 amendments. |
| 4 | PO/Dev — Developer agent | E1–E86, S1–S189 | Keep UX-DR and story numbers; retired UX-DRs stay as "Retired". |
| 5 | Developer agent — `compile-epic-context` | regenerate `epic-1-context.md` (or C1–C17 by hand) | After steps 3–4. |
| 6 | Developer agent | Y1–Y4, R1–R3 | Run the Y4 dry-run and validate. |
| 7 | Test Architect / PO — `bmad-sprint-planning` | readiness rerun (INF-11) | The PASS is stale (R1–R2). |
| 8 | PO — Linear Reconcile | see "Linear impact" | Only after Daniel approves this proposal. |
| 9 | Story 1.1 owner — `bmad-build` | re-plan Story 1.1 at CHECKPOINT 1 | No contract revision (see the record below). |

Applied 2026-11-07 (steps 1–6): every section-4 edit is in place; `epic-1-context.md` was patched by hand (C1–C17), not regenerated. Because O3 and O13 are answered, A18, P26 and S179 state the answers instead of asking for them. Still to do: the UX memlog entry for step 2 (`.memlog.md` was not in the edit scope), the readiness rerun (step 7), Linear Reconcile (step 8) and the Story 1.1 re-plan (step 9).

### Success criteria

1. Every edit in section 4 is applied, and each OLD quote no longer appears where it was replaced.
2. `rg -n "Forge|High Signal|Gunmetal|Inter Display|58px|populating banner|triage drawer|Evidence surface|co-stat|locked glossary" _bmad-output/planning-artifacts/epics.md _bmad-output/planning-artifacts/architecture.md _bmad-output/implementation-artifacts/epic-1-context.md`
   finds only historical notes (A14 "Superseded 2026-11-06", retired UX-DR lines, R3).
3. The PRD lists 33 FRs; the epics FR list, the FR coverage map and the architecture
   Requirements → Structure table each include FR32 and FR33; the architecture says "33/33 mapped".
4. `epics.md` has UX-DR1–UX-DR48, with UX-DR8 and UX-DR14 marked "Retired"; every UX-DR cited by a
   story exists.
5. The Y4 dry-run and validate report 11 epics and 79 stories, with no orphan or missing key.
6. The readiness rerun returns PASS or CONCERNS that Daniel accepts.
7. `linear_reconcile.py plan --check` exits 0 after Reconcile.
8. `validate_story_contract.py validate --phase draft` passes for the Story 1.1 spec.
9. Every open question in section 6 has an owner and is either answered or carried by an
   "approved before implementation" AC.

### Linear impact

Follow Linear Correct Course and then the Linear Reconcile procedure (`_bmad/custom/linear-workflow.md`):
publish only approved scope changes against existing stable identities, comment on each changed
issue, keep history, never delete tickets and never import remote edits as local approval.

- **Planning issues (comment "changed: sprint-change-proposal-2026-11-07"):** `planning:prd` INF-7,
  `planning:ux` INF-8 (the spine itself changes for D3, D8–D10), `planning:architecture` INF-9,
  `planning:epics` INF-10, `planning:sprint` INF-11 (the readiness verdict is stale; reopen if it is
  Done).
- **Epics with changed summaries or coverage:** INF-13 (1), INF-14 (2), INF-15 (3), INF-16 (4),
  INF-17 (5), INF-18 (6), INF-19 (7), INF-20 (8), INF-21 (9), INF-91 (11). Epic titles are unchanged.
- **Retitled stories (21):** carry each new title onto the existing issue (table in 4.4: INF-27, 28,
  39, 40, 41, 49, 56, 58, 59, 61, 62, 63, 98, 67, 68, 69, 70, 75, 77, 79, 84). The reconcile helper
  matches retitled entries whose body also changed only by source ID plus a recorded user
  confirmation, so expect identity decisions for these.
- **Changed bodies (54 stories):** 1.5–1.9; 2.2, 2.6, 2.8–2.13; 3.1, 3.2, 3.4–3.6; 4.2–4.4, 4.6,
  4.7; 5.1–5.8; 6.2–6.6; 7.1, 7.3, 7.4; 8.1–8.4; 9.3–9.7, 9.9; 10.4; 11.1–11.4. Comment on each.
- **New stories to publish (2):** Story 4.9 "End-of-life data for packages" and Story 4.10 "Verify
  artifact signatures against trusted signers", under Epic 4 (INF-16), status backlog.
- **Removed work:** none. (The answer-scoped pack AC in Story 9.5 is reworded, not removed as an
  issue.) No cancellation approval is needed.
- **Story 1.1 tasks** (INF-101–INF-111): unchanged.
- **Commands:**
  `uv run _bmad/custom/scripts/linear_reconcile.py plan --root . --epics _bmad-output/planning-artifacts/epics.md --sprint-status _bmad-output/implementation-artifacts/sprint-status.yaml`
  → identity decisions with Daniel → apply → baseline →
  `uv run _bmad/custom/scripts/linear_reconcile.py plan --root . --epics _bmad-output/planning-artifacts/epics.md --sprint-status _bmad-output/implementation-artifacts/sprint-status.yaml --check`.

### Contract Change Record

| Field | Value |
|---|---|
| Affected contract | STORY-1.1 — `_bmad-output/implementation-artifacts/spec-1-1-monorepo-scaffold-with-an-aggregate-local-gate-and-ci.md` |
| Approval state before | Contract Approval **draft**; Approved by: pending; Contract digest: pending; never approved |
| Change class | **Source-artifact change to an unapproved draft contract.** Not editorial-only, not validation-mechanism-only, not a semantic change to an approved contract. The spec text, its ACs and VALs are not edited by this proposal. |
| Old / new revision | 1 / 1 (unchanged). A revision increment is required only for an approved contract. |
| Changed AC / VAL / source IDs | ACs: none. VALs: none. Sources whose content changes: `architecture.md#Complete Project Directory Structure` (A34–A41: module comments, `lib/design/`, `lib/theme/` comment, routes, the recommended `exports/` module) and `epics.md#ARCH25` (E19: `exports` module, depends on O1). The cited `epics.md#Story 1.1`, ARCH1, ARCH12, ARCH23, ARCH27, ARCH34, PROC1, PROC3 and the 2026-11-05 proposal Topic 1 are unchanged. |
| Impact on implementation | None today (no code). At Build planning the scaffold creates `web/src/lib/design/` and the routes named in A41, and (if O1 is accepted) an empty `exports` module. |
| Impact on tests / evidence | None. No locked tests, no delivery evidence, no digest exists. |
| Evidence invalidated | None. |
| Approvals required | Daniel approves this proposal (product). No Test Architect reapproval: no approved validation exists. Build re-runs planning and CHECKPOINT 1 from the updated sources (the spec already has `status: 'draft'`), where product and Test Architect approve the contract for the first time. |
| Edit guard | Not involved: the contract is not approved or locked, so no `/contract-unlock` is needed. |
| Validator command | `uv run _bmad/custom/scripts/validate_story_contract.py validate --phase draft _bmad-output/implementation-artifacts/spec-1-1-monorepo-scaffold-with-an-aggregate-local-gate-and-ci.md` |
| Other contracts | None: no other story has a spec. |
| Note | The Story 1.1 spec still mentions a `kind` profile and a local Podman machine, which the 2026-11-06 Correct Course replaced; that is outside this change and is picked up by the same re-plan. |

## 6. Open questions

Answered by Daniel on 2026-11-07 with the approval:

- **O3:** yes — the Story 6.5 PDF answer report replaces the signed pack scoped to one answer.
- **O5:** FR32 goes at the end of Epic 4 (Story 4.10).
- **O13:** no — in v1, signature and end-of-life results are shown only; they create no issues and do not change counts.

The other questions stay open.

None of these is decided by this proposal. Each has a suggested owner and, where it gates a story,
the AC that gates it.

| ID | Question | Owner | Gated by |
|---|---|---|---|
| O1 | Which module owns stored exports: a new `exports` capability (recommended in A38/E19) or an existing one (`packs`, `blastradius`)? | Architect | Story 6.5 planning |
| O2 | Are stored export files also cosign-signed, or is the ledger digest enough? | Architect + Daniel | Story 6.5 planning |
| O3 | Confirm dropping the signed evidence pack scoped to one blast-radius answer (old Story 9.5 AC), now that "Audit report for this answer" is the Story 6.5 PDF (D3, S179). | Daniel | Story 9.5 planning |
| O4 | Which minimum role does "Check again" declare in `openapi.yaml` (analyst seems natural; auditors would then not see it)? | Architect + Daniel | Story 2.11 planning |
| O5 | Placement of FR32: end of Epic 4 (proposed, reuses cosign from 4.5) or end of Epic 2 (next to Software detail, but cosign would move into Epic 2)? | PO + Daniel | before the epics edit is applied |
| O6 | FR32 trust configuration: fleet-wide only, or also per registry connection? | Architect + Daniel | Story 4.10 amendment |
| O7 | FR32 result states and their UI words (verified "Yes"; not signed; signed by an untrusted signer; check failed; not checked for this type; no signature policy). | Architect + UX | Story 4.10 amendment; EXPERIENCE Open item 38 |
| O8 | FR32 keyless verification air-gapped: how the Sigstore trusted root reaches the instance (offline bundle, admin-supplied file, chart default) and whether connected instances may refresh it online (a new built-in public endpoint). | Architect | Story 4.10 amendment |
| O9 | FR32 signature formats read from the registry (cosign signatures, OCI referrers, attestations; any other format). | Architect | Story 4.10 amendment |
| O10 | FR32 artifact types in scope: container images and OCI artifacts only, or also packages from feeds (for example npm provenance or PyPI attestations) and uploaded filesystems? | Daniel + Architect | Story 4.10 amendment |
| O11 | FR33 end-of-life data source (neither the PRD nor the architecture names one) and its licence. | Architect + Daniel | Story 4.9 amendment |
| O12 | FR33 coverage (package ecosystems; runtimes; OS releases) and the exact matching rule. | Architect | Story 4.9 amendment |
| O13 | Should signature status or end-of-life status ever create issues, count toward Needs attention, feed the CI policy (Epic 11) or appear in evidence packs? This proposal assumes no for v1. | Daniel | before Stories 4.9/4.10 Build |
| O14 | End-of-life UI copy beyond "No package is past its end of life." (counts past end of life, packages with no data). | UX | Story 4.9 Build; EXPERIENCE Open item 38 |
| O15 | FR33 staleness threshold default, and whether the end-of-life source appears on the Home freshness strip or only in Settings → Sources. | Architect + UX | Story 4.9 amendment |
| O16 | Reports → Audit trail design: list rows, filters, verification, checkpoint and anchoring cells, and the broken-chain state (U5, U20 propose reuse of existing components). | UX | Story 5.5 Build; EXPERIENCE Open item 36 |
| O17 | What the Help item shows before the Help screen is designed (placeholder copy). | UX | Story 1.6 Build; EXPERIENCE Open item 24 |
| O18 | Where the uniformity claim ("All N pieces of software checked the same way — Syft vX · Grype vY") sits on Home, since the spine no longer draws it there. | UX | Story 2.9 Build |
| O19 | Exact placement and style of the licence "Warning" word (U19 proposes line 2 in `text-2`), and review-panel copy for warnings. | UX | Story 7.4 Build; EXPERIENCE Open items 16, 37 |
| O20 | Confirm the label "Audit report for this answer" for the PDF answer report, since "Audit report" otherwise means an evidence pack. | UX + Daniel | Story 6.5 Build; EXPERIENCE Open item 39 |

Carried EXPERIENCE Open items that stories must not invent (already cited in the edits): 1, 3–6, 9,
11–25, 28, 29, 32, 35.

## 7. Change-analysis checklist (completed)

| Item | Status | Notes |
|---|---|---|
| 1.1 Triggering story | [x] | No story: the trigger is the replacement of the UX spines (`ux-Armoury-2026-11-06`, final 2026-11-06, updated 2026-11-07); memlog 90 asks for this Correct Course. |
| 1.2 Core problem | [x] | Deliberate design change plus new requirements from the stakeholder (D10); planning artifacts describe a superseded UI and conflict on FR13, FR14, FR19, FR30 and users. |
| 1.3 Evidence | [x] | Section 1 (quotes with file and line). |
| 2.1 Current epic | [x] | Epic 1 (Story 1.1 draft, nothing started). Its UX stories 1.5–1.9 change; it can complete as planned after the edits. |
| 2.2 Epic-level changes | [x] | No epic added, removed or renumbered; summaries and coverage change; Epic 4 gains Stories 4.9 and 4.10. |
| 2.3 Remaining epics | [x] | All of Epics 1–11 reviewed (section 2 table). |
| 2.4 Invalidated or new epics | [x] | None invalidated; no new epic needed. |
| 2.5 Epic order | [x] | Unchanged. Epic 1–2 UI stories should not start Build before the edits are applied. |
| 3.1 PRD | [x] | P1–P27; MVP grows by FR32, FR33. |
| 3.2 Architecture | [x] | A1–A57; new decisions for issue read model, stored exports, FR32, FR33. |
| 3.3 UI/UX | [x] | Spines change for D3, D8, D9, D10 (U1–U20); everything else follows the spines. |
| 3.4 Other artifacts | [x] | `epic-1-context.md` (C1–C17 or regenerate), `implementation-readiness.md` (R1–R3), `sprint-status.yaml` (Y1–Y4), Linear (section 5), Story 1.1 spec (Contract Change Record). No code, CI, tests or deployment exist to change. |
| 4.1 Direct adjustment | [x] | Viable. Effort: about a day of document edits plus two amendments at story planning. Risk: medium (new architecture, open FR32/FR33 details). |
| 4.2 Rollback | [N/A] | Nothing is built. |
| 4.3 PRD MVP review | [x] | MVP grows by FR32 and FR33 (D10); nothing removed except the answer-scoped pack AC (O3). Core goals unchanged. |
| 4.4 Recommended path | [x] | Direct Adjustment with a PRD scope addition (section 3). |
| 5.1 Issue summary | [x] | Section 1. |
| 5.2 Epic impact and artifact needs | [x] | Section 2. |
| 5.3 Path and rationale | [x] | Section 3. |
| 5.4 MVP impact and action plan | [x] | Sections 3 and 5. |
| 5.5 Handoff plan | [x] | Section 5 (PM, UX, Architect, PO/Dev, TEA, Build). |
| 6.1 Checklist complete | [x] | All applicable items addressed; action-needed items listed below. |
| 6.2 Proposal accuracy | [x] | OLD quotes checked mechanically against the current files on 2026-11-07. |
| 6.3 User approval | [!] | Pending: Daniel approves, edits or rejects this proposal. Status stays `draft` until then. |
| 6.4 Sprint status update | [!] | Proposed (Y1–Y4); applied only after approval. |
| 6.5 Next steps confirmed | [!] | Confirm the handoff order and owners with Daniel, and answer O3 and O5 before the epics edit. |
