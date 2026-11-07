---
status: approved
approved: 2026-11-07 — Daniel approved the whole proposal ("Yes, apply it"); Q3 and Q7 answered
applied: 2026-11-07 — all 102 section-4 edits applied mechanically (0 hand-resolved, 0 failed) plus Q3-a..d (UJ-4/Flow 4 wording) and Q7-a..f (Mixed with no count when N = M); old-wording grep clean; sprint_plan in sync (11 epics, 79 stories)
date: 2026-11-07
workflow: bmad-correct-course (batch)
trigger: implementation-readiness.md FAIL 2026-11-07 (8 blockers) — evidence in readiness-2026-11-07/ (lens A 1–3, lens B 1–4, lens C 1–2)
scope: moderate — 8 gaps are closed by wording and definitions across the PRD (2 sentences), the architecture (the issue read model, the unknown-vulnerability rule, the ranking groups), the UX spines and 12 stories. No FR, NFR, epic or story is added, removed, renumbered or renamed; no code exists. It is more than Minor because it changes product behaviour in four owner documents (PM, Architect, UX, PO/Dev) and the Linear story bodies; it is not Major because there is no replan and no scope change.
memlog_numbering: 'memlog N = line N of ux-designs/ux-Armoury-2026-11-06/.memlog.md. The four readiness decisions are its last four lines, 117–120 (the request called them entries 112–115; line 112 is the earlier Audit trail decision D9).'
decisions:
  - "B1 Stories 5.3 and 5.4 record decisions with scope All places (this vulnerability or licence in this package version on every artifact, including artifacts found later). Story 5.8 adds Only this software (per-artifact decisions) and the Mixed chip; 5.4 shows neither (memlog 120)"
  - "B2 Issue-wide status = the latest All places decision for the issue, else Not reviewed yet. In 'Mixed · N of M', N = places whose own per-artifact decision differs from the issue-wide status, M = place count; Mixed shows when N > 0. The review-status filter matches when any place has that status (decided, no longer an assumption). VEX states each product's effective status: its per-artifact decision if present, else the All places decision (memlog 120)"
  - "B3 Severity groups: Licences (top, hidden at 0), Critical, High, Medium, Low, Negligible (Grype Negligible; hidden at 0), Not rated yet (Grype Unknown or no severity; hidden at 0). Needs attention rule unchanged. Architecture `group` gains `negligible` and `unrated`. Markers proposed with existing tokens only: Negligible = no bar lit, unlit bars in slate-dot, word in text-3; Not rated yet = four empty bars with a dashed text-3 edge, word in text-3 (memlog 117)"
  - "B4 The Exposure unknown state shows when the matching database (Grype DB) has no record for the ID, even if the CVE List or another enrichment feed knows it (memlog 120)"
  - "B5 The issue sentence is the first sentence of the advisory description, as is, with its source (FR12); no plain-language rewrite; no sentence when there is no description (memlog 118)"
  - "B6 Issues review-status filter gains a 'Needs attention' option above the five statuses, with the Needs-attention count; Home's lime 'Review all N' opens Issues with it; Save and next walks that set. Review buttons outside Issues open the issue in Issues on its Review tab (the drawn behaviour; decided) (memlog 120)"
  - "B7 '?' opens the ⌘K palette on a 'Keyboard shortcuts' view; no new modal; Settings → Personal lists the same map (memlog 119)"
  - "B8 Lime is also allowed for focus rings (sidebar ink, forest selection, dark), the centre dot of a moved Exposure map (part of the selected map node) and the all-clear tints lime-wash and lime-ring; Story 1.9's lint and DESIGN.md list the same exceptions (memlog 120)"
---

# Sprint Change Proposal — close the 8 readiness blockers (2026-11-07)

This proposal applies Daniel's decisions B1–B8 (frontmatter; memlog 117–120) to the PRD, the
architecture, `epics.md`, the two UX spines and the Epic 1 context. It decides nothing else. The ~45
readiness concerns stay open unless a blocker edit touches the same sentence. Details the decisions
leave open are listed in section 6.

Edit notation used in section 4:

- Each edit has an ID, a location (heading and **current** line number), `OLD` and `NEW` text, and a
  one-line rationale ("Why"). The blocker it closes is in brackets after the line number.
- `OLD: ⟦…⟧` is an exact substring of the current file and is replaced by `NEW: ⟦…⟧`.
- `OLD (line starts): ⟦…⟧` means the whole line that starts with that text is replaced.
- `OLD (anchor, kept): ⟦…⟧` means the anchor stays and `NEW` is inserted directly after it (a NEW that
  starts on a new line is inserted as new lines).
- Every OLD quote was checked mechanically against the current files on 2026-11-07: each is found
  exactly once, on the stated line (checker: `/tmp/cc4/check_old.py`).
- Domain, data and API terms (`untriaged`, `all_places`, `artifact`, finding group, KEV, VEX, Grype DB)
  stay where they name data or APIs; UI words follow the EXPERIENCE glossary.

## 1. Issue summary

**Problem.** The implementation-readiness rerun after `sprint-change-proposal-2026-11-07.md` failed on
2026-11-07 with 8 blockers. In each, a developer would have to invent behaviour, or two planning
artifacts disagree. Story 1.1 is not blocked; Blockers 7 and 8 block Stories 1.8 and 1.9; the others
block Epics 2, 5 and 6.

**Type.** Gaps and contradictions in requirements found before implementation (a readiness gate), not
a change of direction.

**How it was found.** Three independent read-only review lenses (`readiness-2026-11-07/`); verdict and
table in `implementation-readiness.md`. Daniel chose: fix the blockers with one Correct Course, then
rerun the gate. He answered all 8 (memlog 117–120).

**Evidence (from the readiness table and lenses).**

| # | Gap | Evidence | Lens |
|---|---|---|---|
| 1 | Story 5.4 saves a review on a multi-place issue, but Story 5.3 limits a decision to one place and the scope control arrives in 5.8 (forward dependency). | `epics.md:1557`, `:1591`; `prd.md:95` | A1, B3 |
| 2 | "Issue-wide status" is undefined, so the chip, "Mixed · N of M", filter counts and VEX cannot be computed. | `architecture.md:257`; `epics.md:1701`; `DESIGN.md:710` | B2 |
| 3 | Grype also reports Negligible and Unknown; the `group` enum is closed at licence/critical/high/medium/low. | `architecture.md:257`; `epics.md:164` | A2, B7 |
| 4 | UX shows "no data" when the vulnerability data lacks the ID; architecture and Story 6.2 test "any loaded feed", which includes the CVE List — the CVE-day false zero. | `EXPERIENCE.md:110`, `:394`; `architecture.md:336`; `epics.md:1757` | B1 |
| 5 | No source for "one plain sentence of what it means". | `epics.md:931`; `EXPERIENCE.md:62`; `prd.md:61` | A3, B8 |
| 6 | "Review all N" has no mechanism; no Needs-attention filter; Save and next walks 312 issues, not 3. | `epics.md:1595`; `EXPERIENCE.md:243`, `:413` | B4 |
| 7 | `?` shortcut map has nowhere to open; ⌘K is the only modal; Help is deferred. | `epics.md:190`, `:618`; `EXPERIENCE.md:510` | C1 |
| 8 | Story 1.9's lime lint forbids lime that DESIGN.md requires (focus rings, moved-map centre dot, all-clear tints); `DESIGN.md:568` repeats the short list. | `epics.md:641`; `DESIGN.md:113`, `:466`, `:568`, `:594` | C2 |

## 2. Impact analysis

### Epic impact

| Epic | Impact |
|---|---|
| 1 Shell | Story 1.8 (`?` opens the palette's Keyboard shortcuts view, B7) and Story 1.9 (lime exceptions, B8). |
| 2 Inventory | Story 2.4 stores every Grype severity (B3); Story 2.10 gets the two new groups (B3) and the advisory sentence (B5). |
| 5 Review | Stories 5.1, 5.2 (groups, filter, Needs attention option), 5.3, 5.4, 5.8 (scope split, B1), 5.6 (VEX effective status, B2). Epic List summary gains the two groups. |
| 6 Exposure | Stories 6.2 and 6.3: "unknown" means no Grype DB record (B4). |
| 3, 4, 7–11 | No change. Story 7.4 already cites 5.3, 5.4 and 5.8 for the scope choice; it still holds. |

No epic is added, removed, renumbered or reordered.

### Story impact

- **Changed acceptance criteria (12):** 1.8, 1.9, 2.4, 2.10, 5.1, 5.2, 5.3, 5.4, 5.6, 5.8, 6.2, 6.3.
- **Retitled, added or removed:** none. `sprint-status.yaml` needs no change (checked: 11 epics,
  79 stories; every affected key, for example `5-8-review-scope-all-places-or-only-this-software`,
  keeps its title).
- **Story in flight:** none. Story 1.1 has a draft spec (Revision 1, never approved).

### Artifact conflicts

| Artifact | Conflict | Edits |
|---|---|---|
| `prd.md` | FR13 lists only Critical–Low (B3); UJ-4 step 4 promises a plain sentence (B5) | P1–P2 |
| `architecture.md` | `group` enum (B3); issue-wide status, Mixed N and effective status undefined (B2); no `needs_attention` list filter (B6); no issue-sentence source (B5); "no loaded feed contains" (B4); `ranking/` comment and gap list (B3); VEX status (B2) | A1–A11 |
| `epics.md` front matter and requirements | FR13, ARCH38, UX-DR1, 6, 7, 9, 11, 14, 16, 22, 38, 39, 40, 44, Epic List (Epic 5) | E1–E24 |
| `epics.md` stories | 12 stories (above) | S1–S25 |
| `DESIGN.md` | lime list and sidebar line (B8); severity marker, contrast, print (B3); Mixed N (B2); unknown wording (B4); palette view (B7) | U1–U11 |
| `EXPERIENCE.md` | issue unit, Home, Issues filters and grouping, glossary, component rows, review flow, states, primitives, Flow 4, Open items 4, 9, 13, 24 | U12–U38 |
| `epic-1-context.md` | `?` line (B7); lime line (B8) | C1–C2 |
| `sprint-status.yaml`, `implementation-readiness.md` | none (the gate rerun rewrites the readiness record) | — |

### Technical impact

- **API (architecture, ARCH38):** two more `group` values (`negligible`, `unrated`); a defined
  issue-wide `triage_status` and `mixed` count; an effective status per place; a `needs_attention=true`
  list filter and a Needs-attention count on the page; the issue detail carries the advisory's first
  sentence and its source. The Story 6.2 422 is keyed on "no Grype DB record", not "no loaded feed".
- **Frontend:** two neutral severity markers using existing tokens (`text-3`, `slate-dot`,
  `print-text-2`); a Keyboard shortcuts view inside the existing ⌘K dialog; one more filter option.
- **No new tokens, modules, infrastructure or deployment change.** No rollback: no code exists.

### Contract status (Story 1.1)

`spec-1-1-monorepo-scaffold-with-an-aggregate-local-gate-and-ci.md`: `status: 'draft'`, Revision 1,
never approved. Its sources include `architecture.md#Complete Project Directory Structure`; edit A9
changes one comment there (the `ranking/` line gains "Negligible, unrated"). No other edit touches its
sources (`epics.md#Story 1.1`, ARCH1, ARCH12, ARCH23, ARCH25, ARCH27, ARCH34, PROC1, PROC3 are
unchanged). **No contract revision is needed**; see the Contract Change Record in section 5.

## 3. Recommended approach

**Direct Adjustment.** Edit the planning artifacts in place. Keep every epic, story number and title.

- **Rollback:** not applicable — nothing is built.
- **MVP review:** not needed. No FR or NFR is added or removed; FR13 only names two more severity
  groups, and UJ-4 step 4 changes how the issue is described.
- **Why this path:** every blocker now has Daniel's decision (memlog 117–120); each fix is a definition
  or a reworded AC; no implementation exists.
- **Effort:** low — about half a day to apply and check 102 edits, then the readiness rerun.
- **Risk:** low. The main risk is a missed copy of old wording; success criterion 2 greps for it. Two
  new markers (B3) are proposed with existing tokens and are not drawn in the mock (Q4).
- **Timeline:** Story 1.1 can continue. Stories 1.8, 1.9 and the Epic 2, 5 and 6 stories above should
  not start Build before these edits are applied and the gate passes.

## 4. Detailed change proposals

### 4.1 PRD

<!-- file: _bmad-output/planning-artifacts/prds/prd-Armoury-2026-06-11/prd.md -->

#### prd.md

**P1 · Features → 3. Enrichment & Prioritization → FR13 · L94 (B3)**
OLD: ⟦then vulnerability findings by severity — Critical, High, Medium, Low.⟧
NEW: ⟦then vulnerability findings by severity — Critical, High, Medium, Low, Negligible, then unrated (findings the vulnerability data gives no severity; "Not rated yet" in the UI). The Negligible and unrated groups are also hidden when empty.⟧
Why: B3 — Grype also reports Negligible and Unknown; they get their own groups, never dropped or folded into Low.

**P2 · Users & Journeys → UJ-4 — The Monday check, step 4 · L61 (B5)**
OLD: ⟦4. For the first one he reads one plain sentence of what it means, the fix⟧
NEW: ⟦4. For the first one he reads the first sentence of the advisory's own description, as published and with its source (FR12), the fix⟧
Why: B5 — the sentence is the advisory's own text, not a plain-language rewrite.

### 4.2 Architecture

<!-- file: _bmad-output/planning-artifacts/architecture.md -->

#### architecture.md

**A1 · front matter · L7**
OLD: ⟦amendedAt: '2026-11-07'  # Correct Course: sprint-change-proposal-2026-11-07.md (UX spines ux-Armoury-2026-11-06; FR32/FR33);⟧
NEW: ⟦amendedAt: '2026-11-07'  # Correct Course: sprint-change-proposal-2026-11-07-readiness.md (readiness blockers B1–B8) and sprint-change-proposal-2026-11-07.md (UX spines ux-Armoury-2026-11-06; FR32/FR33);⟧
Why: records this amendment.

**A2 · API & Communication Patterns → Issues and review · L257 (B3)**
OLD: ⟦`group` (`licence` | `critical` | `high` | `medium` | `low`)⟧
NEW: ⟦`group` (`licence` | `critical` | `high` | `medium` | `low` | `negligible` | `unrated`; `negligible` is Grype's Negligible and `unrated` is Grype's Unknown or no severity, UI "Not rated yet"; both sort after `low` and, like `licence`, the UI hides them at 0)⟧
Why: B3 — the enum must hold every severity Grype reports.

**A3 · API & Communication Patterns → Issues and review · L257 (B2)**
OLD: ⟦the issue-wide `triage_status`, `mixed` with the number of places that differ from the issue-wide status,⟧
NEW: ⟦the issue-wide `triage_status` (the status of the latest `all_places` decision on the group; `untriaged` when there is none), `mixed` with the number of places whose own `artifact` decision differs from the issue-wide status (the UI shows "Mixed · N of M" when it is above 0; M is the place count),⟧
Why: B2 — defines issue-wide status and N.

**A4 · API & Communication Patterns → Issues and review · L257 (B6)**
OLD: ⟦(a group matches a status filter when any place has that status; counts are groups, not places) and the total for the pager.⟧
NEW: ⟦(a group matches a status filter when any place has that status; counts are groups, not places), the Needs-attention count, and the total for the pager. The list also takes `needs_attention=true`, which returns only groups with `needs_attention`, in the same order; the Issues "Needs attention" filter and Home's "Review all N" use it.⟧
Why: B6 — Review all N needs a list filter, not a client-side walk.

**A5 · API & Communication Patterns → Issues and review · L257 (B2)**
OLD: ⟦a per-artifact decision overrides `all_places`, and a later `all_places` decision leaves per-artifact decisions in place (Story 5.8).⟧
NEW: ⟦a per-artifact decision overrides `all_places`, and a later `all_places` decision leaves per-artifact decisions in place (Story 5.8). A place's effective status is its own `artifact` decision if present, else the issue-wide status; status filters, Needs attention and VEX (one statement per product) use effective statuses.⟧
Why: B2 — one rule for chips, filters, Needs attention and VEX.

**A6 · API & Communication Patterns → Issues and review · L257 (B5)**
OLD (anchor, kept): ⟦`mixed` is derived, never stored.⟧
NEW: ⟦ **Issue sentence (decided 2026-11-07):** the issue detail shows the first sentence of the advisory description in the vulnerability record (the record's description field), unchanged, with its source and retrieval time (FR12). Armoury never rewrites or generates it; when the record has no description, no sentence is shown.⟧
Why: B5 — records where the sentence comes from.

**A7 · Format Patterns → Honest-degradation metadata · L336 (B4)**
OLD: ⟦A blast-radius query for a CVE ID that no loaded feed contains returns the Story 6.2 error⟧
NEW: ⟦A blast-radius query for a vulnerability ID that the vulnerability data used for matching (the active Grype DB) has no record for — even when the CVE List or another enrichment feed already lists it — returns the Story 6.2 error⟧
Why: B4 — a CVE List entry without package data must not produce "No software has it".

**A8 · Format Patterns → Honest-degradation metadata · L336 (B4)**
OLD: ⟦Only a known vulnerability gets the coverage-scoped zero.⟧
NEW: ⟦Only a known vulnerability — one with a record in the active Grype DB — gets the coverage-scoped zero.⟧
Why: B4 — defines "known".

**A9 · Complete Project Directory Structure → `ranking/` · L430 (B3)**
OLD: ⟦Licences, Critical…Low; KEV first⟧
NEW: ⟦Licences, Critical…Low, Negligible, unrated; KEV first⟧
Why: B3. This comment is in a Story 1.1 source section (see Contract Change Record).

**A10 · Gap Analysis → Minor gaps → FR13 · L550 (B3)**
OLD: ⟦severity groups Critical/High/Medium/Low with a Licences group first;⟧
NEW: ⟦severity groups Critical/High/Medium/Low/Negligible/unrated with a Licences group first;⟧
Why: B3. The tie-breaker stays open for the Story 5.1 amendment.

**A11 · Gap Analysis → Minor gaps → VEX status mapping · L551 (B2)**
OLD: ⟦so a "Mixed" issue states each product's own status;⟧
NEW: ⟦so a "Mixed" issue states each product's own effective status (its per-artifact decision if present, else the All places decision);⟧
Why: B2. The format mapping itself stays open for the Story 5.6 amendment.

### 4.3 Epics — front matter, requirements, UX-DRs, Epic List

<!-- file: _bmad-output/planning-artifacts/epics.md -->

#### Front matter, FRs and ARCH

**E1 · front matter → amendments · L13**
OLD (anchor, kept): ⟦  - 2026-11-07 Correct Course — _bmad-output/planning-artifacts/sprint-change-proposal-2026-11-07.md (UX spines ux-Armoury-2026-11-06; FR32, FR33; Stories 4.9, 4.10)⟧
NEW: ⟦
  - 2026-11-07 Correct Course — _bmad-output/planning-artifacts/sprint-change-proposal-2026-11-07-readiness.md (readiness blockers B1–B8; no story added, removed or renamed)⟧
Why: records this amendment.

**E2 · Requirements Inventory → FR13 · L52 (B3)**
OLD: ⟦then severity groups Critical, High, Medium, Low;⟧
NEW: ⟦then severity groups Critical, High, Medium, Low, Negligible and unrated (UI "Not rated yet"; both hidden when empty);⟧
Why: mirrors P1.

**E3 · Amendments 2026-11-07 → ARCH38 · L164 (B3)**
OLD: ⟦with `group` (`licence`/`critical`/`high`/`medium`/`low`),⟧
NEW: ⟦with `group` (`licence`/`critical`/`high`/`medium`/`low`/`negligible`/`unrated`; `negligible` = Grype Negligible, `unrated` = Grype Unknown or no severity, UI "Not rated yet"),⟧
Why: mirrors A2.

**E4 · ARCH38 · L164 (B2)**
OLD: ⟦issue-wide `triage_status`, derived `mixed` with the count of places that differ,⟧
NEW: ⟦issue-wide `triage_status` (the latest `all_places` decision; `untriaged` when there is none), derived `mixed` with the count of places whose own `artifact` decision differs from it,⟧
Why: mirrors A3.

**E5 · ARCH38 · L164 (B6)**
OLD: ⟦per-group and per-status counts and a pager total come from the server.⟧
NEW: ⟦per-group, per-status and Needs-attention counts and a pager total come from the server; the list takes `needs_attention=true` (the Issues "Needs attention" filter and Home's "Review all N").⟧
Why: mirrors A4.

**E6 · ARCH38 · L164 (B2)**
OLD: ⟦per-artifact decisions override and survive a later `all_places` decision.⟧
NEW: ⟦per-artifact decisions override and survive a later `all_places` decision; a place's effective status is its own `artifact` decision if present, else the issue-wide status (used by status filters, Needs attention and VEX).⟧
Why: mirrors A5.

**E7 · ARCH38 · L164 (B5)**
OLD (anchor, kept): ⟦Metrics keep counting findings (places).⟧
NEW: ⟦ The issue sentence is the first sentence of the advisory description in the vulnerability record, unchanged, with its source (FR12); none when the record has no description.⟧
Why: mirrors A6.

#### UX Design Requirements

**E8 · UX-DR1 · L181 (B8)**
OLD: ⟦plus the agreed exceptions (the selected graph node and "Selected on the map", the Issues nav badge count, text selection);⟧
NEW: ⟦plus the agreed exceptions (the selected graph node and "Selected on the map", together with the centre dot of a moved Exposure map; the Issues nav badge count; text selection; the focus ring on the sidebar, on forest selection and in dark; and the all-clear tints `lime-wash` and `lime-ring`);⟧
Why: B8 — the token requirement lists every lime use DESIGN.md requires.

**E9 · UX-DR6 · L189 (B7)**
OLD: ⟦no-match copy "No matches. Try a CVE ID, package@version or fingerprint." plus common actions.⟧
NEW: ⟦no-match copy "No matches. Try a CVE ID, package@version or fingerprint." plus common actions. `?` opens the same dialog on a **Keyboard shortcuts** view that lists every shortcut (no other dialog; UX-DR7).⟧
Why: B7 — the palette gains the view.

**E10 · UX-DR7 · L190 (B7)**
OLD: ⟦`?` shortcut map (also listed in Settings → Personal);⟧
NEW: ⟦`?` opens the ⌘K palette on its Keyboard shortcuts view (no new modal; Settings → Personal lists the same map);⟧
Why: B7.

**E11 · UX-DR9 · L195 (B3)**
OLD: ⟦(Critical 4 bars `clay`, High 3 `amber`, Medium 2 `slate`, Low 1 `forest-ink`)⟧
NEW: ⟦(Critical 4 bars `clay`, High 3 `amber`, Medium 2 `slate`, Low 1 `forest-ink`; Negligible no bar lit, unlit bars in `slate-dot`; Not rated yet four empty bars with a dashed `text-3` edge; both words in `text-3`)⟧
Why: B3 — mirrors U2, U4, U7.

**E12 · UX-DR11 · L197 (B3)**
OLD: ⟦then **Critical · High · Medium · Low** with counts;⟧
NEW: ⟦then **Critical · High · Medium · Low · Negligible · Not rated yet** with counts (Negligible and Not rated yet hidden at 0);⟧
Why: B3.

**E13 · UX-DR11 · L197 (B6)**
OLD: ⟦the Review status filter listing the five statuses with counts, default Not reviewed yet, never mixed with the severity groups;⟧
NEW: ⟦the Review status filter listing **Needs attention** (with the Needs-attention count, UX-DR38) above the five statuses with counts, default Not reviewed yet, never mixed with the severity groups;⟧
Why: B6.

**E14 · UX-DR14 (retired) · L200 (B3)**
OLD: ⟦then Critical with "N actively exploited", High, Medium and Low, each with its count (UX-DR22).⟧
NEW: ⟦then Critical with "N actively exploited", High, Medium, Low, Negligible and Not rated yet (the last two hidden at 0), each with its count (UX-DR22).⟧
Why: B3 — the retired item still describes its replacement.

**E15 · UX-DR16 · L202 (B6)**
OLD: ⟦Review buttons on Home, the Exposure inspector and Software open the issue in Issues on its Review tab ([ASSUMPTION], Open item 4).⟧
NEW: ⟦Review buttons on Home, the Exposure inspector and Software open the issue in Issues on its Review tab (decided 2026-11-07; the drawn behaviour). Home's **Review all N** opens Issues with the Needs attention filter (UX-DR11), and Save and next walks that set.⟧
Why: B6 — removes the ungated assumption.

**E16 · UX-DR22 · L211 (B3)**
OLD: ⟦then Critical with "N actively exploited", High, Medium, Low);⟧
NEW: ⟦then Critical with "N actively exploited", High, Medium, Low, Negligible and Not rated yet, the last two hidden at 0);⟧
Why: B3.

**E17 · UX-DR22 · L211 (B6)**
OLD: ⟦lime **Review all N** (opens the Needs-attention issues in Issues one after another [ASSUMPTION, Open item 4]).⟧
NEW: ⟦lime **Review all N** (opens Issues with the Review status filter set to Needs attention; Save and next walks that set, UX-DR11, UX-DR16).⟧
Why: B6.

**E18 · UX-DR22 · L211 (B5)**
OLD: ⟦Overview holds the title, one plain sentence of what it means, severity,⟧
NEW: ⟦Overview holds the title, the first sentence of the advisory description as is, with its source (FR12; no plain-language rewrite; no sentence when there is no description), severity,⟧
Why: B5.

**E19 · UX-DR38 · L233 (B6)**
OLD: ⟦The same number appears on Home ("Needs attention N"), in the Issues summary and as the Issues nav badge⟧
NEW: ⟦The same number appears on Home ("Needs attention N"), in the Issues summary, as the count of the Issues "Needs attention" filter option (UX-DR11) and as the Issues nav badge⟧
Why: B6 — one number everywhere, including the new option.

**E20 · UX-DR39 · L234 (B2)**
OLD: ⟦When an issue's places have different statuses, its chip reads **Mixed · N of M** (layers icon, neutral; N = places that differ from the issue-wide status;⟧
NEW: ⟦The issue-wide status is the latest All places decision, or Not reviewed yet when there is none. When N > 0, the chip reads **Mixed · N of M** (layers icon, neutral; N = places whose own per-artifact decision differs from the issue-wide status, M = the place count;⟧
Why: B2.

**E21 · UX-DR39 · L234 (B2)**
OLD: ⟦so a Mixed issue can appear under more than one status ([ASSUMPTION], Open item 9). VEX states each product's own status. Chips reflect the latest recorded decision per place.⟧
NEW: ⟦so a Mixed issue can appear under more than one status (decided 2026-11-07). A place's effective status is its own per-artifact decision if present, else the All places decision; VEX states each product's effective status, and chips and filters use it.⟧
Why: B2 — "latest recorded decision per place" contradicted the rule that a later All places decision leaves per-artifact decisions in place.

**E22 · UX-DR40 · L235 (B4)**
OLD: ⟦**Unknown vulnerability** (no data for the queried ID):⟧
NEW: ⟦**Unknown vulnerability** (the vulnerability data — Grype DB, the matching database — has no record for the queried ID, even if the CVE List or another source already lists it):⟧
Why: B4.

**E23 · UX-DR44 · L239 (B7)**
OLD: ⟦(EXPERIENCE Open item 24; the `?` shortcut map may belong there)⟧
NEW: ⟦(EXPERIENCE Open item 24; `?` opens the ⌘K palette's Keyboard shortcuts view, not Help — UX-DR7)⟧
Why: B7.

#### Epic List

**E24 · Epic List → Epic 5 · L304 (B3)**
OLD: ⟦Licences (hidden at 0), then Critical, High, Medium and Low, actively exploited first in each group,⟧
NEW: ⟦Licences (hidden at 0), then Critical, High, Medium, Low, Negligible and Not rated yet (the last two hidden at 0), actively exploited first in each group,⟧
Why: B3.

### 4.4 Epics — stories

<!-- file: _bmad-output/planning-artifacts/epics.md -->

#### Stories (same file)

**S1 · Story 1.8: Command palette and keyboard map → keyboard map AC · L618 (B7)**
OLD: ⟦export, open the shortcut map, or close the topmost layer, and the same map is listed in Settings → Personal (UX-DR7)⟧
NEW: ⟦export, open the ⌘K palette on its Keyboard shortcuts view (the same dialog, no new modal), or close the topmost layer, and the same map is listed in Settings → Personal (UX-DR6, UX-DR7)⟧
Why: B7.

**S2 · Story 1.8 → keyboard map AC · L619 (B7)**
OLD: ⟦**And** the `g` letters for the renamed surfaces and any new meanings for `t` and `e` are set in EXPERIENCE.md before this story starts Build (EXPERIENCE Open item 13)⟧
NEW: ⟦**And** the `g` letters for the renamed surfaces, any new meanings for `t` and `e`, and the layout of the palette's Keyboard shortcuts view are set in EXPERIENCE.md before this story starts Build (EXPERIENCE Open item 13)⟧
Why: B7 — the view's layout is not drawn; it joins the existing gate (Q6).

**S3 · Story 1.9: Banned-pattern guards → lint AC · L641 (B8)**
OLD: ⟦on lime used outside its agreed jobs (active nav, the one primary action, selected map node, Issues badge, text selection),⟧
NEW: ⟦on lime used outside its agreed jobs (active nav, the one primary action, selected map node including the centre dot of a moved Exposure map, Issues badge, text selection, the focus ring on the sidebar, on forest selection and in dark, and the all-clear tints `lime-wash` and `lime-ring`; DESIGN.md → Accent and selection),⟧
Why: B8 — the lint must not fail on lime that DESIGN.md requires.

**S4 · Story 2.4: Uniform vulnerability scanning → scan AC · L782 (B3)**
OLD: ⟦vulnerability findings are stored with typed severity and the locked `Finding` vocabulary (ARCH15)⟧
NEW: ⟦vulnerability findings are stored with typed severity — every level Grype reports, Negligible and Unknown included; Unknown or no severity becomes the `unrated` group (ARCH38) — and the locked `Finding` vocabulary (ARCH15)⟧
Why: B3 — no severity is dropped at ingest.

**S5 · Story 2.10: Home — Needs attention and open issues by severity → list AC · L925 (B3)**
OLD: ⟦then Critical (with "N actively exploited"), High, Medium and Low with counts,⟧
NEW: ⟦then Critical (with "N actively exploited"), High, Medium, Low, Negligible and Not rated yet (the last two hidden at 0) with counts,⟧
Why: B3. The Needs-attention rule is unchanged.

**S6 · Story 2.10 → detail AC · L931 (B5)**
OLD: ⟦Overview holds the title, one plain sentence of what it means, severity as a word⟧
NEW: ⟦Overview holds the title, the first sentence of the advisory description from the vulnerability record, unchanged, with its source (FR12; no rewrite; no sentence when there is no description), severity as a word⟧
Why: B5.

**S7 · Story 5.1: Deterministic, explainable issue order → grouping AC · L1499 (B3)**
OLD: ⟦the Licences group or the Critical / High / Medium / Low group of its severity;⟧
NEW: ⟦the Licences group or the Critical / High / Medium / Low / Negligible / Not rated yet group of its severity (Not rated yet = Grype Unknown or no severity, ARCH38);⟧
Why: B3.

**S8 · Story 5.1 → licence and no-enrichment AC · L1512 (B3)**
OLD: ⟦and issues without enrichment take an explicit place in their severity group (documented in the amendment), never by accident of nulls.⟧
NEW: ⟦and issues without enrichment take an explicit place in their severity group (documented in the amendment), never by accident of nulls; an issue with no severity sits in Not rated yet, never in Low.⟧
Why: B3.

**S9 · Story 5.2: Issues list → list AC · L1524 (B3)**
OLD: ⟦grouped Licences (hidden at 0), Critical, High, Medium and Low, each with its count;⟧
NEW: ⟦grouped Licences (hidden at 0), Critical, High, Medium, Low, Negligible (hidden at 0) and Not rated yet (hidden at 0), each with its count;⟧
Why: B3.

**S10 · Story 5.2 → list AC · L1524 (B1)**
OLD: ⟦right column the review-status chip or "Mixed · N of M");⟧
NEW: ⟦right column the review-status chip, and "Mixed · N of M" once Story 5.8 adds per-software decisions);⟧
Why: B1 — Mixed cannot occur before Story 5.8.

**S11 · Story 5.2 → filters AC · L1527 (B6)**
OLD: ⟦the Review status filter listing the five statuses with counts (default Not reviewed yet)⟧
NEW: ⟦the Review status filter listing **Needs attention** — the issues counted as Needs attention (`needs_attention=true`, ARCH38), with that count — above the five statuses with counts (default Not reviewed yet)⟧
Why: B6.

**S12 · Story 5.2 → filters AC · L1529 (B2)**
OLD: ⟦a Mixed issue matches every status any of its places has ([ASSUMPTION], EXPERIENCE Open item 9);⟧
NEW: ⟦a Mixed issue matches every status any of its places has (decided 2026-11-07; ARCH38);⟧
Why: B2 — the filter rule is decided.

**S13 · Story 5.3: Record triage decisions as evidence → supersede AC · L1555 (B1)**
OLD: ⟦**When** a new decision is recorded for the same finding⟧
NEW: ⟦**When** a new decision is recorded for the same issue⟧
Why: B1 — an All places decision covers the issue, not one place.

**S14 · Story 5.3 → supersede AC · L1557 (B1, B2)**
OLD: ⟦**And** each decision in this story applies to one finding on one piece of software (one place); the "All N places" scope arrives in Story 5.8.⟧
NEW: ⟦**And** every decision in this story has scope All places (`all_places`): this vulnerability or licence in this package version on every piece of software that has it, including software found later (FR14, ARCH38); the issue-wide status is the latest All places decision, or Not reviewed yet when there is none; per-software decisions ("Only this software") arrive in Story 5.8.⟧
Why: B1 removes the forward dependency; B2 defines what the chip shows.

**S15 · Story 5.4: Review panel → save AC · L1586 (B1)**
OLD: ⟦records the decision, updates the row's chip in place and selects the next issue in the current filter;⟧
NEW: ⟦records the decision for All places (Story 5.3), updates the row's chip in place and selects the next issue in the current filter;⟧
Why: B1.

**S16 · Story 5.4 → save AC · L1587 (B1)**
OLD (anchor, kept): ⟦**And** status can never be changed inline in a list — only in the review panel.⟧
NEW: ⟦
**And** the panel has no scope control and no chip shows Mixed in this story; "Only this software" and "Mixed · N of M" arrive in Story 5.8 (UX-DR16, UX-DR39).⟧
Why: B1 — 5.4 must not show the scope control or Mixed.

**S17 · Story 5.4 → failed-save AC · L1591 (B1)**
OLD: ⟦the chosen options, scope and "Why?" text stay filled in; no toast appears (UX-DR41).⟧
NEW: ⟦the chosen options and "Why?" text stay filled in; no toast appears (UX-DR41).⟧
Why: B1 — there is no scope value in 5.4; S21 adds it to 5.8.

**S18 · Story 5.4 → Review entry points AC · L1595 (B6)**
OLD: ⟦**Then** they open the issue in Issues on its Review tab ([ASSUMPTION], EXPERIENCE Open item 4), and Home's lime "Review all N" opens the Needs-attention issues one after another (UX-DR6, UX-DR22).⟧
NEW: ⟦**Then** they open the issue in Issues on its Review tab (decided 2026-11-07), and Home's lime "Review all N" opens Issues with the Review status filter set to Needs attention (Story 5.2), so Save and next walks only the issues that need attention (UX-DR6, UX-DR11, UX-DR22).⟧
Why: B6 — a mechanism instead of an ungated assumption.

**S19 · Story 5.6: Emit VEX → export AC · L1644 (B2)**
OLD: ⟦when an issue is Mixed, each product's statement carries its own status;⟧
NEW: ⟦when an issue is Mixed, each product's statement carries its own effective status — its per-software decision if present, else the All places decision (ARCH38);⟧
Why: B2.

**S20 · Story 5.8: Review scope → scope AC · L1688 (B1)**
OLD: ⟦**Given** the decision API from Story 5.3
**When** an analyst records a decision
**Then** they choose its scope — **All N places** (default, D6: this vulnerability or licence in this package version, across every piece of software that has it, including software found later) or **Only this software** (one piece of software, pre-filled when Review was opened from it)⟧
NEW: ⟦**Given** the decision API from Story 5.3, where every decision covers All places
**When** an analyst records a decision
**Then** they can choose **Only this software** (scope `artifact`: one piece of software, pre-filled when Review was opened from it) instead of the default **All N places** (D6, Story 5.3: this vulnerability or licence in this package version, across every piece of software that has it, including software found later)⟧
Why: B1 — 5.8 adds the per-software scope on top of 5.3.

**S21 · Story 5.8 → panel AC · L1700 (B1)**
OLD: ⟦with the number of places the choice changes now⟧
NEW: ⟦with the number of places the choice changes now; a failed save keeps the chosen scope with the other answers (UX-DR41)⟧
Why: B1 — moved from 5.4 (S17).

**S22 · Story 5.8 → panel AC · L1701 (B2)**
OLD: ⟦or "Mixed · N of M" (N = places that differ from the issue-wide status;⟧
NEW: ⟦or "Mixed · N of M" when N > 0 (issue-wide status = the latest All places decision, or Not reviewed yet when there is none; N = places whose own per-software decision differs from it; M = the place count;⟧
Why: B2.

**S23 · Story 6.2: Blast-radius query API → zero AC · L1748 (B4)**
OLD: ⟦only for a vulnerability Armoury has data for, never a bare empty list.⟧
NEW: ⟦only for a vulnerability that has a record in the vulnerability data used for matching (Grype DB), never a bare empty list.⟧
Why: B4.

**S24 · Story 6.2 → unknown AC · L1757 (B4)**
OLD: ⟦from "CVE not in any loaded feed" (with feed versions and their age)⟧
NEW: ⟦from "no record in the vulnerability data" — the active Grype DB has no record for the ID, even when the CVE List (Story 4.4) or another enrichment feed knows it — (with feed versions and their age)⟧
Why: B4 — closes the CVE-day false zero.

**S25 · Story 6.3: Exposure surface → unknown AC · L1780 (B4)**
OLD: ⟦(the Story 6.2 "not in any loaded feed" error)⟧
NEW: ⟦(the Story 6.2 "no record in the vulnerability data" error: Grype DB has no record for it, even if the CVE List already lists it)⟧
Why: B4.

### 4.5 UX spines

<!-- file: _bmad-output/planning-artifacts/ux-designs/ux-Armoury-2026-11-06/DESIGN.md -->

#### DESIGN.md

Token check: every token used below exists in the DESIGN.md frontmatter in both themes —
`text-3` / `text-3-dark`, `slate-dot` / `slate-dot-dark`, `print-text-2` / `print-text-2-dark`,
`lime-wash` / `lime-wash-dark`, `lime-ring` / `lime-ring-dark`, `focus-dark`. No token is added.
`text-3` holds 4.9–5.7:1 (light) and 5.2–6.3:1 (dark) on every list surface; `print-text-2` is 7.5:1.

**U1 · front matter → colors → lime · L24 (B8)**
OLD: ⟦  lime: '#C8F169'           # active nav item + the one primary action per view⟧
NEW: ⟦  lime: '#C8F169'           # active nav item + the one primary action per view; agreed exceptions in Colors → Accent and selection⟧
Why: B8 — the comment no longer reads as the full list.

**U2 · front matter → components → severity-marker · L309 (B3)**
OLD (anchor, kept): ⟦    low: '{colors.forest-ink}'⟧
NEW: ⟦
    negligible: '{colors.text-3}'   # word; no bar lit, unlit bars in {colors.slate-dot}
    unrated: '{colors.text-3}'      # "Not rated yet"; four empty bars with a 1px dashed {colors.text-3} edge⟧
Why: B3 — markers for the two new groups, existing tokens only.

**U3 · Colors → Accent and selection · L568 (B8)**
OLD: ⟦Agreed exceptions: the **selected graph node** and its "Selected on the map" marker, the **Issues nav badge** count, and **text selection**. Ink text on lime (14.9:1). Never a chip, never a list marker, never text on the light canvas (1.3:1). Hover {colors.lime-hover}. Tints {colors.lime-wash} and {colors.lime-ring} appear only in the all-clear illustration.⟧
NEW: ⟦Agreed exceptions: the **selected graph node** and its "Selected on the map" marker, including the **centre dot of a moved Exposure map**; the **Issues nav badge** count; **text selection**; the **focus ring** on ink (sidebar), on forest (selection) and everywhere in dark (see Interaction); and the all-clear tints {colors.lime-wash} and {colors.lime-ring}, which appear only in the all-clear illustration. Nothing else is lime. Ink text on lime (14.9:1). Never a chip, never a list marker, never text on the light canvas (1.3:1). Hover {colors.lime-hover}.⟧
Why: B8 — one complete list, consistent with Interaction (L594), the focus-ring component and the moved-map centre node.

**U4 · Colors → Risk → Severity · L576 (B3)**
OLD: ⟦Critical {colors.clay}, High {colors.amber}, Medium {colors.slate}, Low {colors.forest-ink}. No fills, and **no red anywhere**.⟧
NEW: ⟦Critical {colors.clay}, High {colors.amber}, Medium {colors.slate}, Low {colors.forest-ink}. **Negligible** and **Not rated yet** (no severity in the vulnerability data) are neutral, with the word in {colors.text-3}: Negligible lights no bar (its unlit bars in {colors.slate-dot}); Not rated yet draws four empty bars with a dashed {colors.text-3} edge. No new colour family. No fills, and **no red anywhere**.⟧
Why: B3 — word always present; no new hue.

**U5 · Colors → Contrast (WCAG 2.x) · L628 (B3)**
OLD: ⟦| text-3 on canvas / paper / chip / row-hover |⟧
NEW: ⟦| text-3 (also the Negligible and Not rated yet words) on canvas / paper / chip / row-hover |⟧
Why: B3 — shows the new words already pass AA.

**U6 · Components → Sidebar & nav · L700 (B8)**
OLD: ⟦— the only lime in the sidebar besides the badge count.⟧
NEW: ⟦— the only lime in the sidebar besides the badge count and the focus ring (Interaction).⟧
Why: B8 — the sidebar focus ring is lime.

**U7 · Components → Severity · L706 (B3)**
OLD: ⟦(4 bars, filled by level: Critical 4, High 3, Medium 2, Low 1). Colour per level;⟧
NEW: ⟦(4 bars, filled by level: Critical 4, High 3, Medium 2, Low 1, Negligible 0; Not rated yet draws four empty bars with a dashed edge). Colour per level, {colors.text-3} for Negligible and Not rated yet;⟧
Why: B3.

**U8 · Components → Status chip · L710 (B2)**
OLD: ⟦with the count of places that differ from the issue-wide status ("Mixed · 3 of 14").⟧
NEW: ⟦with the count of places whose own decision differs from the issue-wide status — the latest All places decision, or Not reviewed yet when there is none ("Mixed · 3 of 14"; EXPERIENCE → The issue unit).⟧
Why: B2.

**U9 · Components → Exposure header · L722 (B4)**
OLD: ⟦with an ID Armoury has no data for,⟧
NEW: ⟦with an ID the vulnerability data (Grype DB) has no record for,⟧
Why: B4.

**U10 · Components → ⌘K palette · L729 (B7)**
OLD (anchor, kept): ⟦footer on paper with ↑ ↓ move · ↵ open · esc close and "Also finds CVE IDs, package@version and fingerprints".⟧
NEW: ⟦ `?` opens the same dialog on a **Keyboard shortcuts** view (EXPERIENCE → Interaction Primitives); its layout is not drawn (EXPERIENCE Open item 13).⟧
Why: B7 — the component lists its views.

**U11 · Components → Printed report → severity colours · L745 (B3)**
OLD: ⟦Low {colors.print-low} (12.1:1), each on white⟧
NEW: ⟦Low {colors.print-low} (12.1:1), Negligible and Not rated yet {colors.print-text-2} (7.5:1), each on white⟧
Why: B3 — print uses an existing token with the word beside it.

<!-- file: _bmad-output/planning-artifacts/ux-designs/ux-Armoury-2026-11-06/EXPERIENCE.md -->

#### EXPERIENCE.md

**U12 · Information Architecture → The issue unit · L39 (B2)**
OLD: ⟦When places differ, the row's status chip reads **Mixed** with the count of places that differ from the issue-wide status ("Mixed · 3 of 14").⟧
NEW: ⟦The **issue-wide status** is the latest All places decision, or Not reviewed yet when there is none. Each place's own status is its "Only this software" decision if it has one, else the issue-wide status. When any place's own decision differs from the issue-wide status, the row's status chip reads **Mixed · N of M**: N places differ, of M places ("Mixed · 3 of 14").⟧
Why: B2.

**U13 · Home → Open issues · L59 (B3)**
OLD: ⟦then Critical (with "1 actively exploited"), High, Medium, Low, each with its count.⟧
NEW: ⟦then Critical (with "1 actively exploited"), High, Medium, Low, Negligible and Not rated yet (the last two hidden at 0), each with its count.⟧
Why: B3.

**U14 · Home → list column · L60 (B6)**
OLD: ⟦then the lime **Review all 3**.⟧
NEW: ⟦then the lime **Review all 3**, which opens Issues with the Review status filter set to **Needs attention**; Save and next walks that set.⟧
Why: B6.

**U15 · Home → detail column → Overview · L62 (B5)**
OLD: ⟦Overview: title, one plain sentence of what it means ("…lets an attacker run their own code. People are using it in real attacks right now."), severity,⟧
NEW: ⟦Overview: title, the first sentence of the advisory description, as is, with its source (FR12) — no plain-language rewrite, and no sentence when there is no description (the mock's sentence is placeholder copy; the mock is not changed), severity,⟧
Why: B5.

**U16 · Issues → Filters · L70 (B6)**
OLD: ⟦a **Review status** filter listing all five statuses with counts, **default Not reviewed yet**;⟧
NEW: ⟦a **Review status** filter listing **Needs attention** (its count is the Needs-attention number) above all five statuses with counts, **default Not reviewed yet**;⟧
Why: B6.

**U17 · Issues → Grouping · L71 (B3)**
OLD: ⟦then **Critical · High · Medium · Low**. Within each group,⟧
NEW: ⟦then **Critical · High · Medium · Low**, then **Negligible** and **Not rated yet** (no severity in the vulnerability data), each hidden at 0. Within each group,⟧
Why: B3.

**U18 · Issues → Rows · L72 (B2)**
OLD: ⟦or **Mixed · N of M** when places differ.⟧
NEW: ⟦or **Mixed · N of M** when places differ from the issue-wide status (see The issue unit).⟧
Why: B2 — points at the rule.

**U19 · Issues → Review status filter rule · L73 (B2)**
OLD: ⟦- [ASSUMPTION] The **Review status** filter matches an issue when any of its places has that status,⟧
NEW: ⟦- The **Review status** filter matches an issue when any of its places has that status (decided 2026-11-07),⟧
Why: B2 — removes the [ASSUMPTION] tag.

**U20 · Exposure → Unknown vulnerability · L110 (B4)**
OLD: ⟦when Armoury has no data for the queried ID, the answer reads⟧
NEW: ⟦when the vulnerability data (Grype DB, the database Armoury matches against) has no record for the queried ID — even if the CVE List or another source already lists it — the answer reads⟧
Why: B4.

**U21 · Glossary → Mixed · N of M · L185 (B2)**
OLD: ⟦| Status chip on an issue whose places have different statuses; VEX states each product's own status |⟧
NEW: ⟦| Status chip on an issue where N places have their own decision that differs from the issue-wide status; VEX states each product's own status (its own decision, else the All places decision) |⟧
Why: B2.

**U22 · Glossary → Severity · L191 (B3)**
OLD: ⟦| Severity: Critical / High / Medium / Low | CVSS severity |⟧
NEW: ⟦| Severity: Critical / High / Medium / Low / Negligible / Not rated yet | CVSS severity (Not rated yet: Grype "Unknown", no severity) |⟧
Why: B3.

**U23 · Component Patterns → Severity groups · L205 (B3)**
OLD: ⟦Licences group first and hidden at 0; then Critical, High, Medium, Low; Actively exploited first within each.⟧
NEW: ⟦Licences group first and hidden at 0; then Critical, High, Medium, Low, Negligible, Not rated yet (the last two hidden at 0); Actively exploited first within each.⟧
Why: B3.

**U24 · Component Patterns → Review status filter · L207 (B6)**
OLD: ⟦| Review status filter | Issues | Five statuses with counts; default Not reviewed yet. Never mixed with the severity groups. |⟧
NEW: ⟦| Review status filter | Issues | **Needs attention** (with the Needs-attention count, the same number as Home and the badge) above the five statuses with counts; default Not reviewed yet. An issue matches a status when any of its places has it. Home's Review all N opens this filter on Needs attention. Never mixed with the severity groups. |⟧
Why: B6 (and the B2 filter rule).

**U25 · Component Patterns → Status chip · L209 (B2)**
OLD: ⟦when an issue's places have different statuses; N is the places that differ from the issue-wide status.⟧
NEW: ⟦when any place's own decision differs from the issue-wide status (the latest All places decision, or Not reviewed yet when there is none); N is the number of those places, M the number of places.⟧
Why: B2.

**U26 · Component Patterns → Status chip · L209 (B2)**
OLD: ⟦Reflects the latest recorded decision per place. |⟧
NEW: ⟦Reflects each place's own status: its "Only this software" decision if it has one, else the All places decision. |⟧
Why: B2 — "latest" contradicted "a later All places decision leaves per-software decisions in place".

**U27 · Component Patterns → Review action · L210 (B6)**
OLD: ⟦[ASSUMPTION] Outside Issues it opens that issue in Issues on its Review tab. |⟧
NEW: ⟦Outside Issues it opens that issue in Issues on its Review tab (decided 2026-11-07). Home's **Review all N** opens Issues with the Needs attention filter. |⟧
Why: B6.

**U28 · Component Patterns → ⌘K palette · L226 (B7)**
OLD: ⟦Every action is invocable here (Review, Export, Generate audit report, Switch theme). |⟧
NEW: ⟦Every action is invocable here (Review, Export, Generate audit report, Switch theme). `?` opens the palette on a **Keyboard shortcuts** view listing every shortcut (no other dialog). |⟧
Why: B7.

**U29 · Review flow · L243 (B6)**
OLD: ⟦and moves to the next issue in the current filter.⟧
NEW: ⟦and moves to the next issue in the current filter (after Review all N, the next issue that needs attention).⟧
Why: B6 — Save and next walks the Needs-attention set, not 312 issues.

**U30 · State Patterns → Empty answer (known vulnerability) · L255 (B4)**
OLD: ⟦Coverage-scoped zero, only for a vulnerability Armoury has data for:⟧
NEW: ⟦Coverage-scoped zero, only for a vulnerability the vulnerability data (Grype DB) has a record for:⟧
Why: B4.

**U31 · State Patterns → Unknown vulnerability · L256 (B4)**
OLD: ⟦| Unknown vulnerability | Exposure | Armoury has no data for the queried ID:⟧
NEW: ⟦| Unknown vulnerability | Exposure | The vulnerability data (Grype DB) has no record for the queried ID, even if the CVE List or another source lists it:⟧
Why: B4. The copy "Armoury has no data for <ID> yet…" is unchanged (see Q1).

**U32 · Interaction Primitives · L298 (B7)**
OLD: ⟦- From the prior spine: `x` export current view, `?` shortcut map.⟧
NEW: ⟦- From the prior spine: `x` export current view. `?` opens the ⌘K palette on its **Keyboard shortcuts** view (no new modal); Settings → Personal lists the same map.⟧
Why: B7.

**U33 · Key Flows → Flow 4, step 4 · L411 (B5)**
OLD: ⟦one plain sentence ("A vulnerability in a common logging library lets an attacker run their own code. People are using it in real attacks right now."), the fix⟧
NEW: ⟦the first sentence of the advisory description, as published, with its source, the fix⟧
Why: B5.

**U34 · Key Flows → Flow 4, step 6 · L413 (B6)**
OLD: ⟦[ASSUMPTION] Review all 3 opens the three Needs-attention issues in Issues, one after another.⟧
NEW: ⟦Review all 3 opens Issues filtered to Needs attention, and Save and next walks those three.⟧
Why: B6.

**U35 · Open items → 4 · L484 (B6)**
OLD (line starts): ⟦4. [ASSUMPTION] **Review buttons outside Issues**⟧
NEW: ⟦4. **Resolved 2026-11-07** (readiness blocker 6): Review buttons outside Issues (Home, Exposure inspector, Software) open the issue in Issues on its Review tab; **Review all 3** opens Issues with the Review status filter on **Needs attention**, and Save and next walks that set.⟧
Why: B6.

**U36 · Open items → 9 · L489 (B2)**
OLD: ⟦; the **Review status** filter matches an issue when any of its places has that status.⟧
NEW: ⟦. (Decided 2026-11-07: the **Review status** filter matches an issue when any of its places has that status.)⟧
Why: B2. The other half of item 9 (a later All places decision does not overwrite) stays an assumption.

**U37 · Open items → 13 · L496 (B7)**
OLD: ⟦the **g-key letters** for the new surfaces and new meanings for `t` / `e`.⟧
NEW: ⟦the **g-key letters** for the new surfaces and new meanings for `t` / `e`; the layout of the ⌘K palette's **Keyboard shortcuts** view (opened with `?`).⟧
Why: B7 — the undrawn layout joins the Story 1.8 gate (S2).

**U38 · Open items → 24 · L510 (B7)**
OLD: ⟦The `?` shortcut map may belong there.⟧
NEW: ⟦`?` opens the ⌘K palette's Keyboard shortcuts view, not Help (decided 2026-11-07).⟧
Why: B7.

### 4.6 Epic 1 context

<!-- file: _bmad-output/implementation-artifacts/epic-1-context.md -->

#### epic-1-context.md

**C1 · Technical Decisions → Keys · L120 (B7)**
OLD: ⟦  - `?` opens the shortcut map.⟧
NEW: ⟦  - `?` opens the ⌘K palette on its Keyboard shortcuts view (no new modal); Settings → Personal lists the same map.⟧
Why: B7.

**C2 · Banned patterns · L135 (B8)**
OLD: ⟦  - more than one lime primary action per view; lime outside its agreed jobs; red anywhere⟧
NEW: ⟦  - more than one lime primary action per view; lime outside its agreed jobs (active nav, the one primary action, the selected map node including a moved map's centre dot, the Issues badge, text selection, the focus ring on the sidebar, on forest selection and in dark, and the all-clear tints `lime-wash` and `lime-ring`); red anywhere⟧
Why: B8 — the Story 1.9 developer reads this list.

### 4.7 Edits by blocker

| Blocker | Edit IDs |
|---|---|
| B1 scope split (5.3/5.4 vs 5.8) | S10, S13, S14, S15, S16, S17, S20, S21 |
| B2 issue-wide status, Mixed N, filter rule, VEX | A3, A5, A11, E4, E6, E20, E21, S12, S14, S19, S22, U8, U12, U18, U19, U21, U25, U26, U36 |
| B3 Negligible and Not rated yet | P1, A2, A9, A10, E2, E3, E11, E12, E14, E16, E24, S4, S5, S7, S8, S9, U2, U4, U5, U7, U11, U13, U17, U22, U23 |
| B4 unknown = no Grype DB record | A7, A8, E22, S23, S24, S25, U9, U20, U30, U31 |
| B5 advisory sentence | P2, A6, E7, E18, S6, U15, U33 |
| B6 Needs attention filter, Review all N | A4, E5, E13, E15, E17, E19, S11, S18, U14, U16, U24, U27, U29, U34, U35 |
| B7 `?` → palette Keyboard shortcuts view | E9, E10, E23, S1, S2, U10, U28, U32, U37, U38, C1 |
| B8 lime exceptions | E8, S3, U1, U3, U6, C2 |
| Bookkeeping | A1, E1 |

S14 serves B1 and B2. Not changed, checked: PRD FR14 (already says the default covers every
artifact); architecture "Counts are server-derived" and Keyboard lines; UX-DR12 and DESIGN coverage-gap
"plain sentence" (coverage-gap copy, not issues); Story 2.10 all-clear AC; Story 5.4 summary AC;
Story 7.4 scope AC; `sprint-status.yaml`; the mock.

## 5. Implementation handoff

### Scope classification

**Moderate.** The fixes are definitions and reworded ACs, but they change product behaviour in four
owner documents (PRD, architecture, UX spines, epics) and twelve Linear story bodies, so PO/Dev applies
them with the PM, Architect and UX owners checking their own documents. No replan: no FR, NFR, epic or
story is added, removed, renamed or reordered, and no code exists.

### Who applies what, in this order

| Step | Owner (skill) | Applies | Notes |
|---|---|---|---|
| 1 | PM — `bmad-prd` (update) | P1–P2 | `updated` is already 2026-11-07. |
| 2 | UX designer — `bmad-ux` (update) | U1–U38 | Confirm the two proposed markers (U2, U4, U7) against the mock style and re-run the spine token check; add a memlog event "Readiness blockers B1–B8 applied (sprint-change-proposal-2026-11-07-readiness.md)". |
| 3 | Architect — `bmad-architecture` (update) | A1–A11 | — |
| 4 | PO/Dev — Developer agent | E1–E24, S1–S25 | Keep every story number and title. |
| 5 | Developer agent | C1–C2 by hand, or regenerate `epic-1-context.md` with `compile-epic-context` | After steps 2–4. |
| 6 | Test Architect / PO — `bmad-sprint-planning` | readiness gate rerun (INF-11) | Expect `sprint_plan.py generate --dry-run` unchanged: 11 epics, 79 stories, in sync. |
| 7 | PO — Linear Reconcile | see "Linear impact" | Only after Daniel approves this proposal. |
| 8 | Story 1.1 owner — `bmad-build` | nothing new | The planned Story 1.1 re-plan picks up A9 (see the record below). |

### Success criteria

1. Every edit in section 4 is applied; each OLD quote no longer appears where it was replaced.
2. `rg -n 'one plain sentence of what it means|not in any loaded feed|no loaded feed contains|shortcut map may belong|opens the shortcut map|Open item 4[)\]]|latest recorded decision per place' _bmad-output/planning-artifacts/prds/prd-Armoury-2026-06-11/prd.md _bmad-output/planning-artifacts/architecture.md _bmad-output/planning-artifacts/epics.md _bmad-output/planning-artifacts/ux-designs/ux-Armoury-2026-11-06/DESIGN.md _bmad-output/planning-artifacts/ux-designs/ux-Armoury-2026-11-06/EXPERIENCE.md _bmad-output/implementation-artifacts/epic-1-context.md`
   finds nothing.
3. `rg -n -i negligible` finds the new groups in the PRD, the architecture, `epics.md` and both spines;
   `rg -n "needs_attention=true"` finds the architecture and ARCH38.
4. `sprint-status.yaml` is unchanged, and the dry run reports 11 epics and 79 stories, in sync.
5. The readiness rerun closes blockers 1–8 and returns PASS, or CONCERNS that Daniel accepts.
6. `linear_reconcile.py plan --check` exits 0 after Reconcile (apart from the known Story 1.1 status
   difference).
7. `validate_story_contract.py validate --phase draft` still passes for the Story 1.1 spec.
8. Every open question in section 6 has an owner and a gate.

### Linear impact

Follow Linear Correct Course and then Linear Reconcile (`_bmad/custom/linear-workflow.md`): publish
only approved changes against existing identities, comment on each changed issue, never delete.

- **Planning issues (comment "changed: sprint-change-proposal-2026-11-07-readiness"):** `planning:prd`
  INF-7, `planning:ux` INF-8, `planning:architecture` INF-9, `planning:epics` INF-10. `planning:sprint`
  INF-11 stays In Progress until the gate passes.
- **Epic with a changed summary:** Epic 5 INF-17 (Epic List text, E24). Titles unchanged.
- **Stories whose managed blocks change (12):** 1.8 INF-30, 1.9 INF-97, 2.4 INF-34, 2.10 INF-40,
  5.1 INF-58, 5.2 INF-59, 5.3 INF-60, 5.4 INF-61, 5.6 INF-63, 5.8 INF-98, 6.2 INF-66, 6.3 INF-67.
  Bodies only; no retitle, so no identity decisions are expected.
- **New or removed issues:** none. Story 1.1 tasks (INF-101–INF-111): unchanged.
- **Commands:**
  `uv run _bmad/custom/scripts/linear_reconcile.py plan --root . --epics _bmad-output/planning-artifacts/epics.md --sprint-status _bmad-output/implementation-artifacts/sprint-status.yaml`
  → apply → baseline →
  `uv run _bmad/custom/scripts/linear_reconcile.py plan --root . --epics _bmad-output/planning-artifacts/epics.md --sprint-status _bmad-output/implementation-artifacts/sprint-status.yaml --check`.

### Contract Change Record

| Field | Value |
|---|---|
| Affected contract | STORY-1.1 — `_bmad-output/implementation-artifacts/spec-1-1-monorepo-scaffold-with-an-aggregate-local-gate-and-ci.md` |
| Approval state before | `status: 'draft'`; Revision 1; never approved; no digest |
| Change class | **Source-artifact change to an unapproved draft contract.** The spec text, ACs and VALs are not edited. No approved contract changes. |
| Old / new revision | 1 / 1 (unchanged; a revision increment applies only to an approved contract) |
| Changed AC / VAL / source IDs | ACs: none. VALs: none. Source: `architecture.md#Complete Project Directory Structure` — one comment (A9: the `ranking/` line gains "Negligible, unrated"). All other cited sources unchanged. |
| Impact on implementation | None: the scaffold creates an empty `ranking` module; the comment does not change the tree. |
| Impact on tests / evidence | None. No locked tests, no delivery evidence. |
| Evidence invalidated | None. |
| Approvals required | Daniel approves this proposal. No Test Architect reapproval (no approved validation exists). |
| Edit guard | Not involved (contract not approved or locked). |
| Validator command | `uv run _bmad/custom/scripts/validate_story_contract.py validate --phase draft _bmad-output/implementation-artifacts/spec-1-1-monorepo-scaffold-with-an-aggregate-local-gate-and-ci.md` |
| Other contracts | None: no other story has a spec. |

## 6. Open questions

Answered by Daniel on 2026-11-07 with the approval:

- **Q3:** soften the claim. Keep "calm and plain labels" in UJ-4 and Flow 4, but remove "nothing needs translating" (and "no acronyms") as a claim about the advisory sentence.
- **Q7:** when N equals M, the chip reads "Mixed" with no count; the accessible name says "All M places have their own status".

The other questions stay open and are gated by their stories.

Not decided by this proposal. Each has an owner and the gate that carries it.

| ID | Blocker | Question | Owner | Gated by |
|---|---|---|---|---|
| Q1 | B4 | Should the unknown state add "Published <date>; package data is not available yet." when the CVE List knows the ID? It does not fit the current copy: "Armoury has no data for <ID> yet" would then sit beside data Armoury has. Adding it needs a reworded first sentence. Left out for now. | UX + Daniel | Story 6.3 Build (EXPERIENCE Unknown vulnerability state) |
| Q2 | B5 | Which description is used when more than one source has one (the Grype DB record from Story 2.4; the CVE List CNA container and OSV from Story 4.4), how "first sentence" is cut, and how the source is labelled beside it. | Architect + UX | Story 2.10 Build (Grype DB only); Story 4.4 planning (precedence) |
| Q3 | B5 | UJ-4 step 3/5 and Flow 4 step 6 promise "no acronyms to decode" and "nothing needed translating"; an advisory's own first sentence can be technical. Keep the wording, or soften it? | PM + UX | None (wording only) |
| Q4 | B3 | The Negligible and Not rated yet markers are proposed in U2, U4 and U7 and are not drawn in the mock. Confirm or redraw (bar outlines at 4×11px, dashed edge legibility). | UX | Story 2.10 Build |
| Q5 | B6 | The URL value of the Needs attention filter (for example `review=needs-attention`, following `review=not-reviewed`); whether Review all N resets the type filter and search; and whether the walk follows the Issues order (Licences, Critical…, exploited first) or Home's Needs-attention order, which is still open (EXPERIENCE Open item 21). | UX | Story 5.4 Build |
| Q6 | B7 | The layout of the palette's Keyboard shortcuts view (rows and key caps, whether typing filters it, how to return to search). | UX | Story 1.8 Build (EXPERIENCE Open item 13, S2) |
| Q7 | B2 | The rule gives "Mixed · M of M" when there is no All places decision and every place has its own decision (even the same one). Confirm the chip copy for that case. | UX + Daniel | Story 5.8 Build |

Readiness concerns are unchanged and stay with the owners in `implementation-readiness.md`.

## 7. Change-analysis checklist (completed)

| Item | Status | Notes |
|---|---|---|
| 1.1 Triggering story | [x] | No story: the readiness gate FAIL (2026-11-07) after `sprint-change-proposal-2026-11-07.md`. |
| 1.2 Core problem | [x] | Gaps and contradictions in requirements, found before implementation; 8 blockers. |
| 1.3 Evidence | [x] | Section 1 (readiness table and lens findings with file:line). |
| 2.1 Current epic | [x] | Epic 1 (Story 1.1 draft). Stories 1.8 and 1.9 change; it can complete as planned. |
| 2.2 Epic-level changes | [x] | None beyond the Epic 5 summary line (E24). |
| 2.3 Remaining epics | [x] | Epics 2, 5, 6 change in story ACs; 3, 4, 7–11 checked, unchanged. |
| 2.4 Invalidated or new epics | [N/A] | None. |
| 2.5 Epic order | [x] | Unchanged. |
| 3.1 PRD | [x] | P1–P2; MVP unchanged. |
| 3.2 Architecture | [x] | A1–A11: issue read model definitions, `needs_attention` filter, two `group` values, unknown rule, issue sentence. |
| 3.3 UI/UX | [x] | U1–U38; two neutral markers with existing tokens; no new component or token. |
| 3.4 Other artifacts | [x] | `epic-1-context.md` (C1–C2); `sprint-status.yaml` unchanged; Story 1.1 spec (Contract Change Record); Linear (section 5). |
| 4.1 Direct adjustment | [x] | Viable. Effort low; risk low. |
| 4.2 Rollback | [N/A] | Nothing is built. |
| 4.3 PRD MVP review | [N/A] | No scope change. |
| 4.4 Recommended path | [x] | Direct Adjustment (section 3). |
| 5.1 Issue summary | [x] | Section 1. |
| 5.2 Epic impact and artifact needs | [x] | Section 2. |
| 5.3 Path and rationale | [x] | Section 3. |
| 5.4 MVP impact and action plan | [x] | Sections 3 and 5. |
| 5.5 Handoff plan | [x] | Section 5. |
| 6.1 Checklist complete | [x] | All applicable items addressed. |
| 6.2 Proposal accuracy | [x] | OLD quotes checked mechanically on 2026-11-07 (each found once, on the stated line). |
| 6.3 User approval | [!] | Pending: Daniel approves, edits or rejects. Status stays `draft` until then. |
| 6.4 Sprint status update | [N/A] | No epic or story added, removed or renamed. |
| 6.5 Next steps confirmed | [!] | Confirm the handoff order with Daniel; then apply, rerun the gate and reconcile Linear. |
