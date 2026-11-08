# Lens 1: blocker 9 closure and regression check (read-only)

Scope: PRD, architecture, epics, DESIGN/EXPERIENCE spines, the three 2026-11-07 change records, implementation-readiness.md and readiness-2026-11-07/. No project file was edited.
Paths: `PA` = `_bmad-output/planning-artifacts`.

## Verdict suggestion

**FAIL (narrow).** Blocker 9 is closed as written. All 60 A1–A6 edits are in place, blockers 1–8 still hold, and the dry run is in sync. But A1 makes the issue key change over time (CVE first), and nothing records what happens to findings, aliases and decisions when the key changes. The change record says this question (N3) is gated by "Story 2.4 planning", but no story AC carries that gate.

## Blocker 9 closure: verified items

| Item | Evidence | Status |
|---|---|---|
| `--by-cve` invocation | `PA/architecture.md:282`; `PA/epics.md:111` (ARCH7); `:166` (ARCH38); `:783` (Story 2.4). Local `grype 0.120.1 --help` line 41: "--by-cve orient results by CVE instead of the original vulnerability ID when possible" | closed |
| CVE-first key, every alias stored | `architecture.md:257` (Vulnerability IDs and aliases); `epics.md:166`, `:786` (2.4); `prd.md:177` (glossary) | closed |
| KEV/EPSS on any alias | `epics.md:1268`, `:1271` (4.3) | closed |
| CNA/OSV join on any alias; aliases in technical details | `epics.md:1298`, `:1306` (4.4); `:1606` (5.4); `DESIGN.md:719`; `epics.md:204` (UX-DR16) | closed |
| Exposure query / unknown check / ⌘K on any alias | `architecture.md:336`; `epics.md:1762`, `:1774`, `:1781-1785` (6.2); `:1804` (6.3); `:191` (UX-DR6), `:237` (UX-DR40); `EXPERIENCE.md:99`, `:110`, `:157`, `:226`, `:255-256` | closed |
| Known rule: `grype db search --vuln` returns affected packages (N5 answer) | `architecture.md:336`; `epics.md:1774`, `:1784-1785`, `:1812`; UX-DR40 `:237`; `EXPERIENCE.md:110`, `:256`. Local `grype db search --help`: "Search for affected packages by vulnerability ID" | closed, consistent everywhere |
| Vendor VEX display-only, including the CI policy (N7) | `architecture.md:203`, `:257`, `:518`; `epics.md:161` (ARCH36), `:166`, `:1695-1696`, `:1704` (5.7), `:2673` (11.4); `EXPERIENCE.md:243`, `:500`; `rg trustVendorVex` finds nothing | closed |
| Fleet-wide Needs attention count | `architecture.md:257`; `epics.md:166`, `:235` (UX-DR38), `:1549` (5.2); `EXPERIENCE.md:70`, `:204`, `:207` | closed |
| Q1/Q2/Q4/Q5 gates as story ACs | Q2+Q4 → 2.10 `epics.md:926-932`; Q2 → 4.4 `:1290-1292`; Q5 → 5.2 `:1538-1540`, 5.4 `:1600-1602`; Q1 → 6.3 `:1799-1801` | closed |
| Story 5.8 [ASSUMPTION] removed | `epics.md:1721` ("decided, ARCH38; EXPERIENCE Open item 9 resolved"); `EXPERIENCE.md:241`, `:489`. The success-criterion-2 stale-wording `rg` over the five artifacts finds nothing | closed |

## Blockers 1–8: no regression found

- **B1:** 5.3 is All places only (`epics.md:1577`); 5.4 has no scope control (`:1612`); scope arrives in 5.8.
- **B2:** issue-wide status is defined (`architecture.md:257`; `epics.md:1577`, `:1727`).
- **B3:** `negligible` and `unrated` groups exist (`architecture.md:257`; `epics.md:784`, `:1544`).
- **B4:** the unknown rule uses the Grype DB only, now alias-aware.
- **B5:** the issue sentence rule (`architecture.md:257`).
- **B6:** `needs_attention=true` and Review all N (`epics.md:1620`).
- **B7:** `?` opens the ⌘K Keyboard shortcuts view (`epics.md:620`).
- **B8:** the lime lint list matches DESIGN (`epics.md:643`).

**Dry run:** `{"ok": true, "epics": 11, "stories": 79, "in_sync": true, "changed": 0, "dropped_orphans": []}`. It also gives 2 benign warnings for the `# Armoury - Epic Breakdown` (`:18`) and `## Epic List` (`:285`) headings.

## Findings

1. **BLOCKER: the issue key can change, and nothing records what happens when it does. No story gates this question.**
   - **Gap:** A1 keys an issue on the CVE ID "when the vulnerability has one, else the original ID" (`architecture.md:257`; `epics.md:786`). A GHSA-only advisory that later gets a CVE (common) changes key on the next DB update.
   - **Effect on Story 4.2:** Story 4.2 then marks the old finding "resolved-by-feed" and adds a new one (`epics.md:1243`).
   - **Effect on Stories 5.3 and 5.8:** the analyst's decision stays on the old key. The issue reappears as Not reviewed yet and returns to Needs attention. This breaks Story 5.3's AC "a finding that is resolved by a feed update and later reappears … its previous decisions are still attached" (`epics.md:1588-1590`) and the decision propagation in 5.8.
   - **Effect on Exposure:** stored aliases are refreshed only on re-match, and N1 ("whether a later feed update refreshes a finding's aliases") is open. A CVE query between DB activation and the end of re-evaluation can miss GHSA-keyed findings. That window can bring back a false zero.
   - **Gating:** the change record lists N3 (and the refresh part of N1) as "Gated by Story 2.4 planning (before Story 5.3 stores decisions)" (`PA/sprint-change-proposal-2026-11-07-aliases.md`, section 6, N1/N3 rows). Its own success criterion 8 requires such gates to be carried by a story AC or a listed planning step. `rg "N1|N3|key ID (can )?change|re-?key"` over the PRD, architecture, epics and spines finds nothing. Stories 2.4 (`epics.md:765-794`), 4.2 and 5.3 have no gate AC.
   - **Stories:** 2.4, 4.2, 5.3, 5.8, 6.2 (also 9.1 history).
   - **Smallest fix:** add a planning-gate AC to Story 2.4 in the Q-gate style. It should cover N1 (alias source and refresh on DB or enrichment update) and N3 (key change and multi-CVE originals; decisions and history follow the issue across a key change). Cross-reference it from Story 5.3's "reappears" AC.
   - **Owner:** bmad-architecture + bmad-correct-course.

2. **CONCERN: alias storage and indexing, and the graph `Cve` vertex (N2), are not gated.**
   - **Gap:** N2 says "Story 2.4 planning (storage); Story 6.1 planning (graph)". Story 6.1 still names only a `Cve` vertex (`epics.md:1743`), and neither story has a gate AC.
   - **Why a concern:** local data-model detail that Build planning can settle, but the gate is missing.
   - **Stories:** 2.4, 6.1.
   - **Fix:** fold it into the Story 2.4 gate from finding 1, and add one line to Story 6.1.
   - **Owner:** bmad-architecture.

3. **CONCERN: the rest of N5 is not gated in Story 6.2.**
   - **Gap:** still open are the output format, whether `grype db search --vuln` resolves aliases itself, how Armoury finds "any alias of" a queried ID that matches no fleet finding, the per-query cost under NFR2, and whether the same call supplies the metadata for "a CVE that matches no fleet package" (`epics.md:1787-1789`).
   - **Gating:** the change record says "Story 6.2 planning". Story 6.2 (`epics.md:1754-1789`) has no gate AC.
   - **Risk:** if this is left undecided, a query degrades to "unknown", not to a false zero, so the risk is local.
   - **Stories:** 6.2 (and the 6.7 load test).
   - **Fix:** add a planning-gate AC to 6.2.
   - **Owner:** bmad-architecture.

4. **CONCERN: N4 is not gated.**
   - **Gap 1:** Story 5.2's Issues search field ("Find a package or vulnerability", `epics.md:1547`) may or may not match any alias. A1 names ⌘K only.
   - **Gap 2:** no story builds vulnerability-ID results in the ⌘K Issues group. Story 1.8 (`epics.md:608`) only routes to Exposure.
   - **Gap 3:** the Exposure header and query button do not say whether a non-key alias query shows the typed ID, the key ID or both (6.3 `epics.md:1809`).
   - **Gating:** the change record says "Story 6.3 / 5.2 planning". Those stories' gate ACs cover only Q1 and Q5.
   - **Stories:** 5.2, 6.3, 1.8.
   - **Fix:** widen the 5.2 Q5 gate and the 6.3 Q1 gate to include N4.
   - **Owner:** bmad-ux + PO.

5. **CONCERN: N6 is not gated.**
   - **Gap:** Story 5.7 matches a vendor statement on "product and vulnerability" (`epics.md:1693`) but does not say whether that matches on any alias. Story 5.6 does not say which ID and aliases emitted VEX states (for example OpenVEX `aliases`).
   - **Gating:** Story 5.6 has a status-mapping gate (`epics.md:1663-1665`) that does not cover aliases. Story 5.7 has no gate.
   - **Stories:** 5.6, 5.7.
   - **Fix:** extend the 5.6 mapping gate and add a 5.7 planning gate.
   - **Owner:** bmad-architecture.

6. **CONCERN: N9 is not gated.**
   - **Gap:** it is open whether the per-status and per-group counts follow the type filter and search. A5 fixes only the Needs attention count.
   - **Gating:** Story 5.2's Q5 gate (`epics.md:1538`) does not include N9.
   - **Stories:** 5.2.
   - **Fix:** add N9 to the 5.2 gate.
   - **Owner:** bmad-ux + bmad-architecture.

7. **NOTE: FR15 wording still says vendor claims are "applied" (N8, not gated by design).**
   - **Evidence:** PRD FR15 says "applying their not-affected claims (with attribution) to fleet findings" (`prd.md:96`; `epics.md:56`). Story 5.7's statement says "apply their not-affected claims … reduces noise" (`epics.md:1679-1680`).
   - **Impact:** a reader could take this as status-setting. The ACs and architecture are unambiguous, so there is no build impact.
   - **Owner:** bmad-prd.

8. **NOTE: Story 4.5's air-gapped scope manifest lists only CVE IDs.**
   - **Evidence:** the manifest lists "CVE IDs and package coordinates only" (`epics.md:1331`). Story 4.4's fleet-scoped OSV mode uses "the CVEs/aliases in fleet findings" (`:1297`).
   - **Impact:** advisories for GHSA-keyed findings are still reached through package coordinates. The impact is low, and Story 4.5 already has a bundle-format gate (`:1320-1322`).
   - **Fix:** say "vulnerability IDs and aliases" there.
   - **Owner:** bmad-correct-course.

9. **NOTE: the aliases change record still says approval is pending.**
   - **Evidence:** checklist item 6.3 reads "[!] Pending: Daniel approves … Status stays `draft`" (`PA/sprint-change-proposal-2026-11-07-aliases.md:698`). Its frontmatter says `status: approved`, `applied: 2026-11-07`.
   - **Impact:** bookkeeping only.
   - **Owner:** bmad-correct-course.

No other contradiction from the aliases change was found across the PRD, architecture, epics or spines.
