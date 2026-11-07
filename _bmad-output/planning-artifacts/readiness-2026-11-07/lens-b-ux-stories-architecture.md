# Lens B — UX ↔ Stories ↔ Architecture consistency (after Correct Course 2026-11-07)

Scope: EXPERIENCE.md / DESIGN.md (ux-Armoury-2026-11-06) vs epics.md (11 epics, 79 stories) vs architecture.md vs PRD, against SCP-2026-11-07 §6.
Paths are relative to `_bmad-output/planning-artifacts/`. `EXP` = `ux-designs/ux-Armoury-2026-11-06/EXPERIENCE.md`, `DES` = `…/DESIGN.md`, `SCP` = `sprint-change-proposal-2026-11-07.md`.

Clean checks (nothing to report): no surviving Posture/drawer/ranked-table/EPSS-rating/three-theme/Inter/Forge text in epics.md or architecture.md, except retired or historical notes (rg check). IA and routes, the seven sidebar items, Light + Dark only, IBM Plex Sans + Mono, the responsive rule (1280/1024), the single-key shortcut switch, inline errors instead of toasts, licence-violation-only Needs attention, data quality kept off Home and out of list rows, stored exports in Reports → Exports, and ordered roles (admin ⊇ analyst ⊇ auditor, PRD NFR6 `prd.md:128`, Story 1.4 `epics.md:492`) all match across the UX spines, epics and architecture.

## Verdict suggestion

**FAIL.** The behaviour contracts are mostly aligned, but four gaps would make developers invent core Issues and Exposure behaviour. One is a direct UX↔architecture conflict on the CVE-day "unknown vulnerability" state. One is the undefined "issue-wide status" behind "Mixed · N of M". One is a forward dependency from Story 5.4 to Story 5.8. One is "Review all N", which rests on an ungated [ASSUMPTION] and an API filter nobody defined.

## Findings

### 1. BLOCKER — "Unknown vulnerability" is keyed to different data in UX and architecture, which brings back the CVE-day false zero
- **Stories:** 6.2, 6.3 (and Flow 2 failure path)
- **Evidence:**
  - `EXP:110`: the unknown state appears when "Armoury has no data for the queried ID … Vulnerability data updated <age> ago".
  - The glossary (`EXP:180`) defines "Vulnerability data" as the **Grype DB**.
  - The failure case is explicit (`EXP:394`): "the CVE is in the news before the vulnerability data has it → 'Armoury has no data for CVE-… yet'".
  - `architecture.md:336` defines the state as "a CVE ID that **no loaded feed** contains". Story 6.2 (`epics.md:1757`) uses "CVE not in **any loaded feed**".
  - Story 4.4 mirrors the full CVE List v5 as a loaded feed (`epics.md:1281`). A CVE that the CNA has published but Grype DB has no affected ranges for is therefore "known". Under architecture/6.2 it gets the coverage-scoped zero ("No software has it", `epics.md:1748`), which UX forbids for exactly this case.
- **Fix:** In architecture "Honest-degradation metadata" and Story 6.2, define "known" as present in the active vulnerability-match data (Grype DB) with affected-package data, not merely present in any feed. Also say which `details` (feed versions/age) the 422 carries.
- **Owner:** bmad-architecture (+ Story 6.2 AC via bmad-correct-course)

### 2. BLOCKER — "Issue-wide status" is never defined, so the Mixed chip, N, the row chip and VEX cannot be computed
- **Stories:** 2.10, 5.2, 5.3, 5.8, 5.6
- **Evidence:**
  - `architecture.md:257` makes the list return "the issue-wide `triage_status`, `mixed` with the number of places that differ from the issue-wide status".
  - `epics.md:1701` (5.8) uses "N = places that differ from the issue-wide status". `DES:710` and `EXP:209` say the same.
  - No artifact defines how the issue-wide status is derived:
    - the latest `all_places` decision, `untriaged` when there is none?
    - the majority?
    - something else when only per-artifact decisions exist (likely after Story 5.3, `epics.md:1557`, which records one place at a time)?
  - The two plausible rules give different chips and filter counts.
- **Fix:** Add one sentence to ARCH38/architecture "Issues and review". For example: "issue-wide status = the current `all_places` decision, or `untriaged` if none; `mixed` = count of places whose effective status differs".
- **Owner:** bmad-architecture

### 3. BLOCKER — Story 5.4 (review panel) depends forward on Story 5.8 (scope)
- **Stories:** 5.3, 5.4, 5.8
- **Evidence:**
  - 5.3: "each decision in this story applies to one finding on one piece of software (one place); the 'All N places' scope arrives in Story 5.8" (`epics.md:1557`).
  - 5.4 reviews an **issue** (14 places) and requires that "the chosen options, **scope** and 'Why?' text stay filled in" (`epics.md:1592`). Its Save "records the decision" with no scope available.
  - `EXP:241` makes All places the default scope.
- **Impact:** A 5.4 developer must invent which place a save writes to, or ship a panel that records 1 of 14 places. Every later chip would then be Mixed.
- **Fix:** Reorder 5.8 before 5.4, or merge the scope control into 5.4 and the scope field into 5.3. 5.4 also refers forward to the Exposure inspector Review (`epics.md:1593-1595`, Epic 6); keep that as a later-story AC.
- **Owner:** bmad-correct-course

### 4. BLOCKER — "Review all N" has no mechanism: it rests on an ungated [ASSUMPTION] and a filter neither the UX nor the API defines
- **Stories:** 5.4, 2.10, 5.2
- **Evidence:**
  - Flow 4 (`EXP:413`): "[ASSUMPTION] Review all 3 opens the three Needs-attention issues in Issues, one after another". Open item 4 (`EXP:484`).
  - Story 5.4 implements it while citing the assumption, with no "approved before Build" gate (`epics.md:1595`).
  - The Issues filters are only type, Review status and search (`EXP:70-73`; `epics.md:1527`).
  - Save and next "moves to the next issue in the **current filter**" (`EXP:243`). With the default "Not reviewed yet", that walks 312 issues, not the 3 that need attention.
  - ARCH38 (`architecture.md:257`) exposes `needs_attention` per group but no filter or query parameter for it.
- **Fix:** Decide a `needs_attention=true` Issues filter (URL plus API parameter) or an explicit review queue. Record it in EXPERIENCE and ARCH38, and gate 5.4 on it.
- **Owner:** bmad-ux + bmad-architecture

### 5. CONCERN — Architecture has no contract for the Reports → Audit trail group (D9)
- **Stories:** 5.5, 9.6, 9.9
- **Evidence:**
  - `architecture.md` has zero occurrences of "audit trail" (`rg -ci`). The SCP architecture edits (A1–A57, `SCP:356-668`) contain no D9 change.
  - Story 5.5 needs:
    - a fleet ledger listing with filters by type, subject and time window and a pager total (`epics.md:1611`);
    - subject → "plain label with its technical ID".
  - Only `GET /api/v1/evidence/verification` exists (Story 2.1, `epics.md:691-692`). It "recomputes the chain" on each call.
  - The UX wants "Chain intact — N entries, verified **4 min ago**" (`EXP:116`; `epics.md:1620`). That implies scheduled or cached verification, which nothing defines (cadence, storage, metric).
- **Fix:** In architecture, add the ledger list endpoint (filters, cursor), the subject model (type + id → label), and the verification schedule plus its stored result (and the checkpoint and anchoring read model for 9.6/9.9).
- **Owner:** bmad-architecture

### 6. CONCERN — Issue identity, deep links and several UI-needed endpoints are unnamed
- **Stories:** 2.10, 2.11, 5.1–5.4, 5.8, 6.5, 6.6, 9.5
- **Evidence:**
  - ARCH38 gives the group key (vuln ID + purl@version), but defines no group ID, list or detail path, or decisions path (`architecture.md:257`). Story 2.10 only says "the findings API returns finding groups" (`epics.md:932`).
  - Story 5.1 puts the order explanation on `GET /api/v1/findings/{id}` (`epics.md:1503`). A finding is a **place**, while ordering is per group (issue).
  - Cross-surface Review must "open the issue in Issues on its Review tab" (`EXP:210`; `epics.md:1595`), but there is no URL for a selected issue or tab (`EXP:49` gives only `/issues?review=not-reviewed`).
  - `/software/<name>` (`EXP:48`) is not unique against artifact UUIDs (`GET /api/v1/artifacts/{id}`, `architecture.md:205`).
  - Missing endpoints: export create/download (only the `GET /api/v1/exports` list exists, `architecture.md:204`); pack list, detail and in-product signature verification (9.5); the neighbours API shape and node-ID scheme (`architecture.md:267, 436` say only "the graph neighbours API"; 6.6 names the path only, `epics.md:1879`).
- **Fix:** Add a short "UI read models" subsection to architecture: issue ID and URL, group detail, decisions, exports POST/download, packs, neighbours query and node IDs.
- **Owner:** bmad-architecture

### 7. CONCERN — Severities outside Critical/High/Medium/Low have no group, and Epic 2 groups before the severity rule exists
- **Stories:** 2.4, 2.10, 5.1
- **Evidence:**
  - Story 2.4 stores Grype's "typed severity" (`epics.md:782`); Grype also emits Negligible and Unknown.
  - The UX has only "Licences, then Critical · High · Medium · Low" (`EXP:71`; `DES:576`).
  - Story 2.10 (Epic 2) already computes "Critical" for Needs attention and the Open-issues groups (`epics.md:925`).
  - Severity-source precedence is decided only by the Story 5.1 amendment (`epics.md:1495`). That amendment covers "issues without enrichment" (`epics.md:1512`), not Negligible/Unknown.
- **Fix:** Before Story 2.10, decide the mapping of Negligible/Unknown and the interim severity source, so Needs-attention counts do not change meaning at 5.1.
- **Owner:** bmad-architecture (pull the 5.1 rule forward)

### 8. CONCERN — The "plain sentence of what it means" has no source
- **Story:** 2.10
- **Evidence:**
  - Home Overview requires "one plain sentence of what it means ('…lets an attacker run their own code. People are using it in real attacks right now.')" (`EXP:62`; `epics.md:931`).
  - Feeds supply technical CVE/CNA descriptions (Story 4.4). No artifact says how a plain sentence is produced: a template from CWE/impact plus KEV, the CNA text verbatim, or none.
- **Fix:** Record the content rule (and its fallback) in UX and the Story 2.10 AC.
- **Owner:** bmad-ux

### 9. CONCERN — No rule for when Home may say "You are in good shape"
- **Stories:** 2.9, 2.10, 4.7
- **Evidence:**
  - Home leads with "You are in good shape. 3 things need attention today." (`EXP:57, 379, 409`).
  - Story 2.9 asks only for "one plain summary line" (`epics.md:899`). Only the stale-feed caveat (4.7) and All clear (`epics.md:937`) have rules.
  - Nothing says when "good shape" is withheld, for example at 40 needs-attention items or 20 % coverage. Voice requires reassurance "only when the data earns it" (`EXP:136`).
- **Fix:** Add the summary-line rules to EXPERIENCE State Patterns and gate 2.9.
- **Owner:** bmad-ux

### 10. CONCERN — Home Needs-attention order is an open item that Story 2.10 silently depends on
- **Story:** 2.10
- **Evidence:** "Home Needs attention order … not decided" (`EXP:504`, Open item 21; UX-DR22 `epics.md:211`). Story 2.10 lists the rows with no order and no gate (`epics.md:925`).
- **Fix:** Decide it (for example, the Issues order) or add "set by UX before Build".
- **Owner:** bmad-ux / Story 2.10 planning

### 11. CONCERN — Undrawn detail tabs and cells are built without gates (Open items 14, 15)
- **Stories:** 2.10, 2.11, 4.9, 5.5, 6.3, 6.5, 9.5
- **Evidence:**
  - `EXP:497-498`: the Home Exposure tab, Issues Exposure and History, Software's Issues/Packages/Audit trail tabs, Reports' Files/Audit trail tabs, and the stored-export detail are "not drawn".
  - These stories build them with only "not drawn" notes and no "set by UX before Build" gate:
    - 6.3 delivers "Home's Exposure tab (a reduced summary …)" (`epics.md:1778`);
    - 5.5 builds the History and Audit trail tabs (`epics.md:1623`);
    - 2.11 builds the Packages and Issues tabs;
    - 4.9 adds per-package end-of-life to the Packages tab (`epics.md:1428`);
    - 6.5 lists exports, but no story defines the export detail column.
  - The drawn Home Overview Exposure cell (All / Deployed / Not deployed, first places, `EXP:62`) is in no story's AC (2.10's Overview list, `epics.md:931`).
- **Fix:** Add a UX gate per story or draw the tabs. Give the Overview Exposure cell an owner.
- **Owner:** bmad-ux + bmad-correct-course

### 12. CONCERN — Reports → Audit trail is gated only for the broken-chain state
- **Stories:** 5.5, 9.6, 9.9
- **Evidence:**
  - Open item 36 (`EXP:116`, "Not drawn yet") and SCP O16 (`SCP:2959`) cover the list rows, filters, verification, checkpoint and anchoring cells and the broken-chain state, "gated by Story 5.5 Build".
  - Story 5.5 gates only "the layout and wording of the broken-chain state" (`epics.md:1620`).
  - The `DES` Audit trail row is itself an [ASSUMPTION] (`DES:738`).
- **Fix:** Widen the 5.5 gate to all of O16.
- **Owner:** Story 5.5 planning / bmad-ux

### 13. CONCERN — Regenerating an audit report is undefined (Open item 22)
- **Story:** 9.5
- **Evidence:**
  - "the user can change the window, scope and framework after the click, **which regenerates the pack**" (`epics.md:2278`).
  - `EXP:505` (Open item 22): "how window, scope and framework are adjusted after the click … and re-generation semantics" and the in-progress row are open. UX-DR20 also says "how is not drawn" (`epics.md:206`).
  - With signed, append-only packs, the story must invent whether the first pack is kept, superseded or cancelled. No gate.
- **Fix:** Decide in UX plus architecture and gate 9.5.
- **Owner:** bmad-ux + bmad-architecture

### 14. CONCERN — Export placement on Issues and Software, the JSON choice and the row unit are undefined
- **Story:** 6.5
- **Evidence:**
  - Export exists on "Exposure, Issues, Software" (`EXP:218`). Only Exposure places it (header, `DES:722`).
  - The Issues and Software sections (`EXP:67-90`) have no Export control.
  - Story 6.5 and `DES:716` put the failure in "the Export row", which no surface defines (`epics.md:1849`).
  - The "JSON as an option" UI is undefined (`epics.md:1835`).
  - Whether an Issues CSV has one row per issue or per place (the screen counts issues; architecture metrics count places, `architecture.md:202`) is undefined.
- **Fix:** Add Export placement and the format choice to EXPERIENCE; state the CSV row unit in ARCH39.
- **Owner:** bmad-ux / Story 6.5 planning

### 15. CONCERN — SCP open questions O2 and O20 are not carried by Story 6.5
- **Story:** 6.5
- **Evidence:**
  - SCP gates O2 ("are stored export files also cosign-signed") and O20 (label confirmation) on Story 6.5 (`SCP:2945, 2963`). Architecture repeats O2 (`architecture.md:204, 556`).
  - Story 6.5 gates only O1 ("the owning module is settled when the story is planned", `epics.md:1841`).
  - SCP success criterion 9 requires every open question to be carried by an AC (`SCP:2880`).
- **Fix:** Add both to the 6.5 planning gate.
- **Owner:** bmad-correct-course

### 16. CONCERN — "N more" rows and Home Open-issues row clicks are built on an open item
- **Stories:** 5.2, 2.10
- **Evidence:**
  - Open item 18 (`EXP:501`): "'N more' rows with the pager, Home Open issues row click behaviour" are not drawn.
  - Story 5.2 builds "'N more High' rows for long groups" (`epics.md:1524`) with no gate. Story 2.10 builds the Open-issues summary rows with no click behaviour.
- **Fix:** Decide (for example, "N more" applies the group filter) or gate.
- **Owner:** bmad-ux

### 17. CONCERN — No rule for concurrent review decisions (Open item 30)
- **Stories:** 5.3, 5.4, 5.8
- **Evidence:**
  - "two people reviewing the same issue at once … has no rule" (`EXP:516`).
  - 5.3 makes a new decision supersede the old one (`epics.md:1556`). Without a version check, the last write silently wins on evidence-grade data.
  - Architecture defines no optimistic-concurrency rule (409 exists in the envelope list, `architecture.md:334`).
- **Fix:** Record expected-version or a 409 conflict, plus the inline copy.
- **Owner:** bmad-architecture + bmad-ux

### 18. CONCERN — Global session, offline and forbidden-link states (Open item 31)
- **Stories:** 1.3, 1.6
- **Evidence:**
  - Open item 31 (`EXP:517`) covers session expiry and re-authentication, an unreachable control plane, and a direct link to a forbidden Settings panel.
  - Story 1.3 defines only the API 401 (`epics.md:452, 461`). Story 1.6 has no UI rule. The review panel's "nothing is lost" promise depends on re-auth behaviour.
- **Fix:** UX decision plus a gate on 1.6.
- **Owner:** bmad-ux

### 19. CONCERN — The `?` shortcut map has no surface
- **Story:** 1.8
- **Evidence:**
  - Story 1.8 must make `?` "open the shortcut map" (`epics.md:618`).
  - The ⌘K dialog is the only allowed modal and a test enforces it (`epics.md:633`; `EXP:304`).
  - Help is deferred, and "the `?` shortcut map may belong there" (`EXP:510`). Nothing says where `?` goes; Settings → Personal holds a list.
- **Fix:** Decide (for example, `?` opens Settings → Personal#shortcuts) and add it to the existing Open item 13 gate.
- **Owner:** bmad-ux

### 20. CONCERN — The "Connect a registry" one-liner contradicts the credential form
- **Stories:** 2.2, 2.9
- **Evidence:**
  - Story 2.9's empty Home shows "Connect a registry with its copy-paste one-liner in a code block" (`epics.md:913`; `EXP:251`).
  - Story 2.2 adds a registry from the empty Home page with a form (URL, auth type, credentials, Test connection, `epics.md:712-713`). UJ-1 says "She pastes read-only registry credentials" (`EXP:376`).
  - No artifact defines what the registry one-liner is.
- **Fix:** UX states either a form or a one-liner (and which command).
- **Owner:** bmad-ux

### 21. CONCERN — Software detail "Audit report" button has no story and no behaviour
- **Story:** 2.11 / 9.5
- **Evidence:**
  - `EXP:83` and UX-DR25 (`epics.md:214`): "grey Check again **and Audit report**" in the Info cell.
  - Story 2.11's Info list and actions omit it (`epics.md:955`).
  - Nothing defines whether it generates a pack scoped to this software (which would need the generate role) or opens Reports.
- **Fix:** Define it in UX and assign it to 9.5.
- **Owner:** bmad-ux / bmad-correct-course

### 22. CONCERN — The "triage license warnings = off" setting is not in the spines and breaks counts
- **Story:** 7.4
- **Evidence:**
  - "when an admin turns it off, warnings stay visible but have no review panel" (`epics.md:2018-2021`).
  - Unreviewable warnings would stay "Not reviewed yet" forever. That inflates "312 not reviewed yet", the default Issues filter (`EXP:70`) and the Home line (`EXP:60`). Their chip is undefined.
- **Fix:** Define the status and count treatment in UX/ARCH38, or drop the setting.
- **Owner:** bmad-ux + Story 7.4 planning

### 23. CONCERN — The moved-map Table is undrawn and outside the 6.6 gate
- **Story:** 6.6
- **Evidence:**
  - The 6.6 gate covers other centres and long trails (`epics.md:1889`).
  - The Table of a moved map is only noted "not drawn (EXPERIENCE Open item 19)" (`epics.md:1902`). Its columns differ from the answer table (issues, packages, places versus `DES` table columns Software … Review).
- **Fix:** Include the Table in the 6.6 UX gate.
- **Owner:** Story 6.6 planning

### 24. CONCERN — The Exposure query grammar for moved centres and version ranges is undefined
- **Stories:** 6.2, 6.3, 6.6
- **Evidence:**
  - The moved-map URL uses `q=software:acme/payments-api@sha256:…` (`EXP:49, 103`). Queries accept only a vulnerability ID, `package@version` or a fingerprint (`EXP:99`).
  - No grammar exists for package, vulnerability or place centres; the URL must "restore that map" (`epics.md:1880`).
  - Story 6.2 and PRD FR17 accept version ranges ("log4j-core@2.x", `epics.md:1736`; `prd.md:101`), but UX has no header or question copy for a range.
- **Fix:** Add the query/URL grammar to architecture and the UX header copy.
- **Owner:** bmad-architecture + bmad-ux

### 25. CONCERN — The icon-rail width is untokenised while lints enforce tokens (Open item 33)
- **Stories:** 1.5, 1.7
- **Evidence:**
  - `EXP:519` lists untokenised dimensions, "the icon-rail width" among them.
  - Story 1.5 requires layout tokens to "match DESIGN.md" (`epics.md:516`), and Story 1.7 builds the icon rail (`epics.md:591`).
- **Fix:** Add `spacing.icon-rail-width` (and the other listed dimensions) to `DES`.
- **Owner:** bmad-ux

### 26. NOTE — Stale [ASSUMPTION] tags on decisions the architecture or PRD already made
- **Stories:** 1.5, 1.6, 5.2, 5.8, 6.5, 9.3
- **Evidence:**
  - `EXP:33` still reads "[ASSUMPTION] Admin can also do everything an analyst can", while `EXP:490` marks it resolved and `prd.md:128` decides it.
  - Open item 9 (`EXP:73, 489`) is decided in `architecture.md:257`, but Stories 5.2 and 5.8 still cite it as an [ASSUMPTION] (`epics.md:1529, 1695`).
  - Open items 3 and 5 (theme default, print face) are fixed by `architecture.md:182, 264-265, 285`, but Stories 1.5, 6.5 and 9.3 cite them as [ASSUMPTION] with no gate (`epics.md:520, 1857, 2216`).
- **Fix:** Retag them as decided.
- **Owner:** bmad-ux

### 27. NOTE — The surface list for inline errors differs
- **Evidence:** `EXP:222` lists Review panel, Export, Generate audit report and Settings. UX-DR41 (`epics.md:236`) and the architecture SPA pattern add Check again. The Exposure "Check again" (re-ask) is a different action with the same label (`EXP:179`).
- **Fix:** Align `EXP:222`.
- **Owner:** bmad-ux

### 28. NOTE — Issues' primary action sits outside the list column
- **Evidence:** The IA table gives Issues the primary "Save and next" (`EXP:49`). Layout puts "the view's one primary action" at the end of the list column (`DES:677`; UX-DR37 `epics.md:232`). Save and next lives in the detail-column review panel (`DES:715`).
- **Fix:** State the exception in `DES` Layout.
- **Owner:** bmad-ux

### 29. NOTE — Some drawn tabs have no owning story
- **Evidence:** No story delivers the Home tabs "How to fix" and "Details" (`epics.md:931` says they "wait for UX") or the Issues "Exposure" tab (`epics.md:1538`).
- **Fix:** Record them as deferred in epics.md so they are not orphaned.
- **Owner:** bmad-correct-course

### 30. NOTE — Auditor access to "Audit report for this answer" is ambiguous
- **Evidence:** Auditors may export (`epics.md:1863`; `architecture.md:204`), but "Generate audit report" is absent for them (`EXP:271`). The answer report shares the "Audit report" label and is generated by Typst. Story 6.5's auditor AC mentions only "export".
- **Fix:** State it explicitly in 6.5.
- **Owner:** Story 6.5 planning
