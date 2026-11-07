# Lens A — Traceability & Structure (Armoury readiness, post Correct Course 2026-11-07)

Paths below are relative to `_bmad-output/planning-artifacts/` unless shown otherwise. The line numbers are from the files as read on 2026-11-07.

## Verdict suggestion

**FAIL.** Every FR and UX-DR traces, and sprint-status is in sync. But three decisions that nothing records block Stories 2.10 and 5.4, and about 17 open UX items or ordering gaps are not gated. Epic 1 is not affected by the blockers.

### Mechanical checks (passed)
- **FR → story:** all 33 FRs (FR1–FR33) are cited in story ACs. FR32 is in 4.10 and FR33 in 4.9 (a script parsed the story bodies of `epics.md`).
- **NFR → story:** all 12 NFRs are cited in story ACs.
- **UX-DR → story:** every UX-DR from 1 to 48 is cited by at least one story, except UX-DR8 and UX-DR14, which are retired (`epics.md:194`, `epics.md:200`).
- **ARCH → story:** every ARCH item from 1 to 41 is cited by at least one story.
- **Story count:** 79 stories (E1 9, E2 13, E3 6, E4 10, E5 8, E6 7, E7 4, E8 4, E9 9, E10 4, E11 5).
- **Sprint-planning dry-run:** `sprint_plan.py generate … --dry-run` returned:
  - `in_sync: true`, epics 11, stories 79.
  - Counts: backlog 90, optional 11.
  - No new, orphan or illegal entries; `changed: 0`, `upgraded_from_disk: []`.
  - Two warnings, both harmless: `unparsed Epic/Story-like heading at epics.md:16: # Armoury - Epic Breakdown` and `… epics.md:283: ## Epic List`.
- **Sprint-planning validate:** `sprint_plan.py validate` returned `valid: true` with no problems.

## Findings

### Blockers

1. **[blocker] Story 5.4 builds the review panel on multi-place issues while decisions can only cover one place until Story 5.8.**
   - **Stories affected:** 5.3, 5.4, 5.8 (7.4 inherits the problem).
   - **Evidence:**
     - Story 5.3 limits every decision to one place: "each decision in this story applies to one finding on one piece of software (one place); the "All N places" scope arrives in Story 5.8" (`epics.md:1557`).
     - In Story 5.4, the panel works on an Issues row, which covers every place (UX-DR39). Save "records the decision, updates the row's chip in place" (`epics.md:1586`). Story 5.4 never says which place or places a save covers.
     - Story 5.4's failed-save AC already keeps a "scope" value (`epics.md:1591`), but the scope control only arrives in 5.8 (`epics.md:1680–1701`).
     - The default contradicts the PRD and the architecture. PRD FR14 (`prd.md:95`) says "By default one decision covers every artifact affected by the same vulnerability". ARCH38 (`epics.md:164`) says "scope `all_places` (default…)".
   - **Impact:**
     - A developer has to invent what Save does on a 14-place issue.
     - Whatever they choose either breaks FR14's default or anticipates 5.8.
     - Story 5.4 cannot be completed on its own.
   - **Smallest fix:** move the scope AC (all_places default, per-artifact override) from 5.8 into 5.3, and the scope control into 5.4. Or re-order 5.8 before 5.4.
   - **Owner:** bmad-correct-course.

2. **[blocker] No issue group exists for Grype "Negligible" and "Unknown" severities.**
   - **Stories affected:** 2.4, 2.10, 2.11, 5.1, 5.2, 8.3 (and the 9.2 pack findings section).
   - **Evidence:**
     - ARCH38 has a closed enum: "`group` (`licence` | `critical` | `high` | `medium` | `low`)" (`architecture.md:257`; `epics.md:164`).
     - PRD FR13 lists only "Critical, High, Medium, Low" (`prd.md:94`). UX-DR11 and UX-DR14 do the same (`epics.md:197`, `epics.md:200`).
     - Story 2.4 stores Grype's "typed severity" (`epics.md:782`). Grype also emits Negligible and Unknown.
     - `rg -i negligible` over the PRD, the architecture, the UX spines and `epics.md` finds nothing.
     - Story 5.1's amendment covers "severity groups and severity-source precedence" (`epics.md:1495`). But Story 2.10 already counts Open issues by group and computes Needs attention ("Critical") (`epics.md:925–926`), three epics earlier.
   - **Impact:**
     - Unknown-severity findings are either dropped from counts or silently folded into Low. Both are NFR8 dishonesty.
     - The finding-groups API schema cannot hold them.
   - **Fix:** record a mapping in ARCH38 now (for example Negligible→Low; Unknown→its own "Unknown severity" group, or →High until known), plus how the UI shows it.
   - **Owner:** bmad-architecture, then bmad-ux for the label.

3. **[blocker] No data source is recorded for "one plain sentence of what it means".**
   - **Stories affected:** 2.10 (also UJ-4 / Flow 4).
   - **Evidence:**
     - Story 2.10: "Overview holds the title, one plain sentence of what it means" (`epics.md:931`).
     - UX-DR22: `epics.md:211`.
     - EXPERIENCE: "A vulnerability in a common logging library lets an attacker run their own code. People are using it in real attacks right now." (`ux-designs/ux-Armoury-2026-11-06/EXPERIENCE.md:62,411`).
     - PRD UJ-4 step 4: "he reads one plain sentence of what it means … No acronyms to decode" (`prd.md:61`).
     - Nothing in `architecture.md` or `epics.md` says where this sentence comes from: a CNA description (technical, and not available until Story 4.4), a template from CWE + KEV + package role, or curated text. AI remediation is roadmap only (`prd.md` Roadmap).
   - **Impact:** the developer must invent a content-generation approach. That is a product and architecture decision, not copy.
   - **Fix:** record the source and fallback (for example a template from severity, KEV, CWE class and package; the CNA description in technical details) in the architecture and UX, or reword UJ-4/UX-DR22.
   - **Owner:** bmad-architecture + bmad-ux (bmad-prd if UJ-4 changes).

### Concerns

4. **[concern] Forward dependencies inside Epic 6 (and from 5.4 and 9.9).**
   - **Stories affected:** 6.3, 6.4, 5.4, 9.9.
   - **Evidence:**
     - Story 6.3 AC: "When the user chooses Review in the inspector" (`epics.md:1793`). The inspector is built in Story 6.6 (`epics.md:1893`).
     - Story 6.4: "the same layout as a moved map (Story 6.6 …)" (`epics.md:1814`), and "show the focused node in the inspector" (`epics.md:1822`).
     - Story 5.4: "the Review buttons on Home, the Exposure inspector and Software" (`epics.md:1593`). The inspector arrives in Epic 6.
     - Story 9.9: the image is "listed in the Story 10.3 mirror image list" (`epics.md:2407`).
   - **Impact:** these ACs cannot pass when their story is built. Each story is not independently completable.
   - **Fix:** move the inspector into 6.4 (or move those ACs into 6.6). Phrase the 5.4 and 9.9 items as "when 6.6 / 10.3 lands".
   - **Owner:** bmad-correct-course.

5. **[concern] The rule for vulnerability ID aliases (GHSA/OSV ↔ CVE) is undecided.**
   - **Stories affected:** 2.4, 4.3, 5.1, 6.2, 6.3; the ARCH38 group key.
   - **Evidence:**
     - Issue identity is "keyed by vulnerability ID and package purl@version" (`architecture.md:257`).
     - KEV is keyed by CVE (Story 4.3, `epics.md:1253`).
     - Exposure is queried by CVE ID (Story 6.2, `epics.md:1736`).
     - `rg -i "alias|GHSA|relatedVulnerabilities"` finds only an OSV fetch-scope mention (`epics.md:1282`).
   - **Impact:**
     - Grype reports GHSA IDs for many language-ecosystem matches. A CVE query or KEV join keyed on the primary ID can miss them, giving a false "no software has it" on CVE day (FR17, NFR8).
     - One CVE can also split into two issues.
   - **Fix:** record an alias rule: group on a canonical ID (CVE where one exists, using Grype's related vulnerabilities) and join on all aliases.
   - **Owner:** bmad-architecture.

6. **[concern] The registry setup action needs a "copy-paste one-liner" that nothing defines.**
   - **Stories affected:** 2.9, 2.2.
   - **Evidence:**
     - Story 2.9: "the setup action "Connect a registry" with its copy-paste one-liner in a code block with Copy" (`epics.md:913`). UX-DR29 says the same (`epics.md:221`), as does `EXPERIENCE.md:251`.
     - Story 2.2 connects a registry through a form ("adds a registry (URL, auth type, read-only credentials) and runs "Test connection"", `epics.md:712–714`).
     - EXPERIENCE Flow 1 says "She pastes read-only registry credentials" (`EXPERIENCE.md:376`).
     - No CLI or Helm-values command for adding a registry is specified.
   - **Impact:** the developer must invent the command, or drop the one-liner.
   - **Fix:** UX states whether the registry action is a button to the form or a command, and the architecture names the command if there is one.
   - **Owner:** bmad-ux (+ bmad-architecture).

7. **[concern] The order of Home's Needs attention list is undecided, and Story 5.2 implies an order that conflicts with the drawn one.**
   - **Stories affected:** 2.10, 5.2.
   - **Evidence:**
     - UX-DR38: "The order within Home's Needs attention is not decided (EXPERIENCE Open item 21)" (`epics.md:233`).
     - EXPERIENCE: "drawn: exploited, licence, Critical — not decided; the Licences-at-top rule covers the Issues list and the Open issues summary only" (`EXPERIENCE.md:504`).
     - Story 5.2: "Home's Open issues summary and Needs attention … use the same groups, order and counts" (`epics.md:1534`).
     - Story 2.10 renders the list without stating any order or a gate (`epics.md:925`).
   - **Impact:** a silent dependency on an open item. The draft (exploited first) and 5.2's wording (Licences first) conflict.
   - **Fix:** decide the order, or add "set by UX before Build" to 2.10, and narrow 5.2's wording.
   - **Owner:** bmad-ux.

8. **[concern] How the audit-report window, scope and framework are changed after the click is undrawn and not gated.**
   - **Stories affected:** 9.5.
   - **Evidence:**
     - Story 9.5: "the user can change the window, scope and framework after the click, which regenerates the pack" (`epics.md:2278`).
     - UX-DR20: "(FR22; how is not drawn — EXPERIENCE Open item 22)" (`epics.md:206`).
     - Open item 22 also leaves the in-progress row and re-generation semantics open (`EXPERIENCE.md:505`).
   - **Fix:** add a "designed before Build" gate to 9.5.
   - **Owner:** bmad-ux / 9.5 Build planning.

9. **[concern] Undrawn detail tabs are built without a gate (Open item 15).**
   - **Stories affected:** 2.11, 4.9, 5.2, 5.4, 5.5, 6.5, 9.5.
   - **Evidence:**
     - Story 2.11 builds "tabs Overview · Issues · Packages · Audit trail" (`epics.md:955`), but only Overview is drawn.
     - Story 5.2 builds "tabs Review · Exposure · History … not drawn" (`epics.md:1538`).
     - Story 5.5 builds the Issues History tab "(not drawn — EXPERIENCE Open item 15)" (`epics.md:1623`).
     - Stories 6.5 and 9.5 list exports and a Files tab whose detail is undrawn (`EXPERIENCE.md:498`).
     - Open item 15 itself: `EXPERIENCE.md:498`.
   - **Impact:** the content and layout of seven tabs are invented, or the tabs ship empty.
   - **Fix:** gate each AC ("designed before Build") or state minimal content (for example the Packages tab is the SBOM package table).
   - **Owner:** bmad-ux.

10. **[concern] Several behaviours from Open item 18 are undecided but depended on.**
    - **Stories affected:** 2.10, 2.11, 5.2.
    - **Evidence:**
      - UX-DR14: "What a click on those rows does is not drawn (EXPERIENCE Open item 18)" (`epics.md:200`).
      - Story 2.10 builds the Open issues rows (`epics.md:925`).
      - The "N more High" rows work together with the pager (Stories 5.2 `epics.md:1524` and 2.11). Open item 18 says ""N more" rows with the pager … not drawn" (`EXPERIENCE.md:501`).
      - Only the Add software destination is gated (`epics.md:949`).
    - **Fix:** gate these items or decide them.
    - **Owner:** bmad-ux.

11. **[concern] What the Data quality field in Software detail shows from Epic 2 until Epic 8 is undecided.**
    - **Stories affected:** 2.11.
    - **Evidence:**
      - Story 2.11 Info: "Data quality (filled by Story 8.2; what it shows before a score exists is EXPERIENCE Open item 32)" (`epics.md:955`).
      - Only Story 8.1's amendment answers Open item 32 (`epics.md:2051`), five epics later.
    - **Fix:** decide the interim display (for example omit the field, or "Not scored yet") in 2.11, or gate it.
    - **Owner:** bmad-ux / 2.11 Build planning.

12. **[concern] The Home Exposure, How to fix and Details tabs are built undrawn or orphaned (Open item 14).**
    - **Stories affected:** 2.10, 6.3.
    - **Evidence:**
      - Story 6.3: "Home's Exposure tab (a reduced summary with a button to the full page)" (`epics.md:1778`). It is not drawn (UX-DR22 `epics.md:211`; `EXPERIENCE.md:497`) and has no gate.
      - Story 2.10: "How to fix and Details wait for UX (EXPERIENCE Open item 14)" (`epics.md:931`). No later story builds them once they are drawn.
    - **Fix:** gate 6.3's Home tab, and assign How to fix and Details to a story or remove the tabs.
    - **Owner:** bmad-ux + bmad-correct-course.

13. **[concern] Global and conflict states are unowned (Open items 30, 31).**
    - **Stories affected:** 1.3, 1.6, 5.4.
    - **Evidence:**
      - Open item 30: "two people reviewing the same issue at once … has no rule" (`EXPERIENCE.md:516`).
      - Open item 31: "session expired and re-authentication; control plane unreachable; a direct link to a Settings panel or action the role cannot use" (`EXPERIENCE.md:517`).
      - Story 1.3 only says "an expired session returns 401" (`epics.md:461`). No story owns the UI behaviour.
    - **Fix:** assign each state to a story, with a UX gate.
    - **Owner:** bmad-ux + bmad-correct-course.

14. **[concern] Open questions O2 and O20 are not gated where the change record says they are.**
    - **Stories affected:** 6.5, 6.3.
    - **Evidence:**
      - The change record gates O2 ("Are stored export files also cosign-signed") at Story 6.5 planning (`sprint-change-proposal-2026-11-07.md` §6 table; `architecture.md:556` "Open — Story 6.5 planning (O1, O2)"). Story 6.5 cites only O1: "the owning module is settled when the story is planned (O1)" (`epics.md:1841`).
      - O20, confirming the label "Audit report for this answer" (EXPERIENCE Open item 39, `EXPERIENCE.md:525`), is gated at Story 6.5 Build. Neither 6.3 (`epics.md:1777`) nor 6.5 (`epics.md:1844`) mentions it.
    - **Fix:** add O2 and O20 to 6.5's planning AC (and to 6.3, which renders the label).
    - **Owner:** bmad-correct-course.

15. **[concern] Stories 10.2 and 10.3 were not updated for FR33 (and the FR32 trusted root).**
    - **Stories affected:** 10.2, 10.3, 10.4.
    - **Evidence:**
      - Story 10.2's published bundle variants list "core (Grype DB, KEV, EPSS and the full CVE List v5 snapshot …) or full (core plus the full OSV mirror)" (`epics.md:2478`), with no end-of-life dataset.
      - FR33 requires that end-of-life data is "carried in the signed offline bundle (FR10)" (`prd.md:93`). FR10 says "Armoury also publishes signed bundles" (`prd.md:87`).
      - Story 10.3's boundary check lists built-in endpoints "(Grype DB, KEV, EPSS, OSV, CVE List, public Fulcio, public Rekor)" (`epics.md:2508`). It omits "the end-of-life data source (FR33)", which ARCH19 includes (`epics.md:130`; `architecture.md:486`), and any trusted-root refresh endpoint (O8).
    - **Impact:** air-gapped users of the published bundles never get end-of-life data, and the egress check misses an endpoint.
    - **Fix:** add end-of-life data (and the trusted root if O8 chooses it) to 10.2's variants and to 10.3's list.
    - **Owner:** bmad-correct-course.

16. **[concern] [ASSUMPTION] items are used as decided behaviour without a gate.**
    - **Stories affected:** 1.5, 5.2, 5.4, 5.8, 6.6.
    - **Evidence:**
      - Story 5.2: "a Mixed issue matches every status any of its places has ([ASSUMPTION], EXPERIENCE Open item 9)" (`epics.md:1529`).
      - Story 5.4: "open the issue in Issues on its Review tab ([ASSUMPTION], EXPERIENCE Open item 4)" (`epics.md:1595`).
      - Story 6.6: "focus goes to the new centre … ([ASSUMPTION], EXPERIENCE Open item 12)" (`epics.md:1885`).
      - Story 1.5: no OS-preference detection "([ASSUMPTION], EXPERIENCE Open item 3)" (`epics.md:520`).
    - The [ASSUMPTION] in 5.8 at `epics.md:1695` is largely resolved by PRD FR14 and ARCH38. Open item 5 (print face) is decided by ARCH35.
    - **Impact:** the task's rule allows an [ASSUMPTION] only with a gate. Each of these needs an explicit "accepted" or "approved before Build".
    - **Owner:** bmad-ux (accept or decide) / each story's Build planning.

17. **[concern] No rule is recorded for classifying packages as direct or indirect.**
    - **Stories affected:** 2.11, 6.4, 6.6.
    - **Evidence:**
      - UX-DR25: "Packages ("214 packages · SBOM", Direct / Indirect …)" (`epics.md:214`). Story 2.11 includes "Direct / Indirect" (`epics.md:955`).
      - Story 6.4 edge labels: "direct · in 12" (`epics.md:1810`). Story 6.6: "How it got it" (`epics.md:1893`).
      - `architecture.md` has no rule (`rg -i direct` finds no dependency-depth rule). Syft's relationship data differs by ecosystem.
    - **Fix:** the architecture records the derivation and an "unknown" fallback.
    - **Owner:** bmad-architecture.

18. **[concern] Some UX elements are not built by any story.**
    - **Stories affected:** 2.11, 2.10.
    - **Evidence:**
      - UX-DR25 and EXPERIENCE put "grey Check again and Audit report" in the Software Info cell (`epics.md:214`; `EXPERIENCE.md:83`). Story 2.11 builds Check again only (`epics.md:966–970`). No story defines what Audit report does there; packs are fleet-scoped by default (`epics.md:2277`).
      - UX-DR22's Overview "Exposure cell (All / Deployed / Not deployed) with "See all N on the map"" (`epics.md:211`) is missing from 2.10's Overview list (`epics.md:931`). Story 6.3 only wires the link.
    - **Fix:** assign each element to a story and define the Audit report action.
    - **Owner:** bmad-correct-course + bmad-ux.

19. **[concern] Settings → Access shows a "users/roles view", but no user store exists.**
    - **Stories affected:** 1.6.
    - **Evidence:**
      - Story 1.6: "Settings → Access (the read-only resolved auth configuration and the users/roles view)" (`epics.md:545`).
      - The architecture has only `sessions` and `user_preferences` (`architecture.md` Auth bullet). Roles come from OIDC claims at sign-in (`epics.md:477`).
    - **Impact:** a list of "users" has no data source. Is it derived from sessions, from preferences, or is it just the role-mapping config?
    - **Fix:** define it, or reduce it to "role mapping (read-only)".
    - **Owner:** bmad-architecture / 1.6 Build planning.

20. **[concern] The Reports → Audit trail design (O16 / Open item 36) is only partly gated.**
    - **Stories affected:** 5.5, 9.6, 9.9.
    - **Evidence:**
      - Story 5.5 gates only "the layout and wording of the broken-chain state are set by UX before Build (O16)" (`epics.md:1620`).
      - O16 covers "list rows, filters, verification, checkpoint and anchoring cells" (change record §6; `EXPERIENCE.md:522`).
      - Stories 9.6 (`epics.md:2339`) and 9.9 (`epics.md:2424`) add checkpoint and anchoring cells with no gate.
    - **Fix:** widen 5.5's gate and add one to 9.6 and 9.9.
    - **Owner:** bmad-ux.

### Notes

21. **[note] "Copy to confirm with UX" has no owner or gate.**
    - Occurrences: `epics.md:882` (2.8), `:955` (2.11 Built), `:1176` (3.6), `:1290` (4.4), `:1361` (4.7), `:1428` (4.9, O14), `:1470` (4.10, O7), `:1699` (5.8), and the Help placeholder (1.6; O17, `epics.md:239`).
    - Low risk (copy only), but story completion should state whether UX sign-off is required.
    - **Owner:** bmad-ux.

22. **[note] Story 5.2 adds coverage-gap rows to Issues, which UX-DR12 does not place there.**
    - Story 5.2: "and coverage-gap rows in place" (`epics.md:1524`).
    - UX-DR12 places gap rows only in "Software, Exposure list and table, Home band" (`epics.md:198`).
    - **Owner:** bmad-ux / 5.2 planning.

23. **[note] The FR coverage map and NFR placement are stale.**
    - "FR16: … extended by Epics 5, 8" (`epics.md:262`). Epic 8 explicitly adds nothing to Home (8.2, `epics.md:2085`), while Stories 3.6, 4.7, 6.3 and 9.5 do extend Home.
    - "FR18: … extended by Epics 3, 4, 5, 7, 8" (`epics.md:264`) omits Epic 6 (6.6 cites FR18) and Epic 11 (11.3 source records).
    - The NFR placement line (`epics.md:281`) omits NFR1 in E10 (10.4) and NFR6 in E11.
    - **Owner:** bmad-correct-course (editorial).

24. **[note] The Story 1.1 contract is stale, and sprint-status does not see it.**
    - The spec still uses kind and local Podman: `implementation-artifacts/spec-1-1-…md:25,42,70,72,74` ("Skaffold `kind` dev loop", "local Podman machine", "`skaffold dev -p kind`"). The current Story 1.1 ACs use `mise run dev` on the dev cluster and ARC runners (`epics.md:362–378`).
    - This is acknowledged and gated by the Build re-plan at CHECKPOINT 1 (change record §5, step 9). Recorded here so it is not lost.
    - `sprint-status.yaml:39` has `1-1-…: backlog`, while the draft spec exists. The `spec-` prefix is not picked up by the dry-run (`upgraded_from_disk: []`).
    - **Owner:** Story 1.1 Build planning.

25. **[note] The Software route uses a name that may not be unique.**
    - UX-DR5 and UX-DR25 route to `/software/<name>` (`epics.md:188`, `:214`).
    - Artifacts are identified by digest and UUIDv7 (ARCH13, ARCH36), and one name has many versions and digests.
    - The URL key is undecided.
    - **Owner:** bmad-architecture / 2.11 planning.

26. **[note] The change record and the readiness record are internally stale.**
    - `sprint-change-proposal-2026-11-07.md:2995–2997` still marks the checklist items "6.3 User approval [!] Pending", "6.4 … applied only after approval" and "6.5 … answer O3 and O5". Its frontmatter says "approved … applied".
    - `implementation-readiness.md:21` says "Current verdict: PASS … stale", which this rerun replaces.
    - **Owner:** bmad-correct-course (editorial).

No other actionable Lens-A findings: there are no orphan stories, and every epic delivers user value (Epics 1 and 10 are NFR-only by design and are stated as such).
