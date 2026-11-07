# Readiness rerun — Lens 1: blocker closure and regression (read-only, 2026-11-07)

Paths: PA = `_bmad-output/planning-artifacts/`, IA = `_bmad-output/implementation-artifacts/`,
EXP/DES = `PA/ux-designs/ux-Armoury-2026-11-06/EXPERIENCE.md` / `DESIGN.md`,
CR = `PA/sprint-change-proposal-2026-11-07-readiness.md`.

## Verdict suggestion

**CONCERNS.** All 8 previous blockers are CLOSED, and the PRD, architecture, epics (UX-DRs and stories), both spines and
`epic-1-context.md` agree on them. The 102 edits plus Q3/Q7 created no conflicts in behaviour. What is left: open questions
that the CR says are gated by a story, but whose story ACs do not carry the gate (Q2, Q4, Q5); one new count ambiguity for
the Needs attention filter option; and wording notes. No blockers.

Sprint plan dry run (`sprint_plan.py generate … --dry-run`): `"ok": true, "epics": 11, "stories": 79, "in_sync": true,
"changed": 0, "new_entries": [], "dropped_orphans": []`. The only warnings are the 2 known non-story headings (`epics.md:17`,
`:284`).

The old-wording grep (CR success criterion 2) returns no matches across all six files. The spot greps for replaced OLD
strings ("Five statuses with counts", "places that differ from the issue-wide", "any loaded feed", "Armoury has data for",
"one finding on one piece of software", "for the same finding", "`?` shortcut map") also return no matches. The only
exception is EXP:208, which keeps "scope" on purpose because it is the end-state review panel.

## Blocker closure

| # | Status | Evidence (current lines) |
|---|---|---|
| 1 Scope split 5.3/5.4 vs 5.8 | **CLOSED** | 5.3 `epics.md:1558` "every decision in this story has scope All places (`all_places`)… per-software decisions ("Only this software") arrive in Story 5.8"; 5.4 `:1587` "records the decision for All places (Story 5.3)", `:1589` "the panel has no scope control and no chip shows Mixed in this story"; failed-save AC no longer lists scope (`:1593`); 5.2 `:1525` "'Mixed · N of M' once Story 5.8 adds per-software decisions"; 5.8 `:1690-1692` adds "Only this software" on top; `:1702` failed save keeps scope. Architecture `:257` "Decisions carry scope `all_places` (default…) or `artifact`". |
| 2 Issue-wide status / Mixed N / filter / VEX | **CLOSED** | `architecture.md:257` "issue-wide `triage_status` (the status of the latest `all_places` decision…; `untriaged` when there is none), `mixed` with the number of places whose own `artifact` decision differs…" and "A place's effective status is its own `artifact` decision if present, else the issue-wide status; status filters, Needs attention and VEX… use effective statuses". The same rule appears in ARCH38 `epics.md:165`, UX-DR39 `:235`, 5.3 `:1558`, 5.6 `:1646`, 5.8 `:1703`, EXP:39, EXP:73, EXP:185, EXP:209 and DES:712. Q7 (N = M → "Mixed", no count) is identical in arch `:257`, UX-DR39, 5.8 `:1703`, EXP:39, EXP:209 and DES:712. |
| 3 Negligible / Not rated yet | **CLOSED** | PRD `prd.md:94`; arch `:257` (`negligible`, `unrated`, "both sort after `low`… hides them at 0"), `:430`, `:550`; epics FR13 `:53`, ARCH38 `:165`, UX-DR9 `:196`, UX-DR11 `:198`, UX-DR14 `:201`, UX-DR22 `:212`, Epic 5 `:305`, 2.4 `:783`, 2.10 `:926`, 5.1 `:1500`, `:1513`, 5.2 `:1525`; DES:310-311, `:578`, `:630`, `:708`, `:747`; EXP:59, `:71`, `:191`, `:205`. A grep finds no remaining four-group list in any normative section; the only one is in EXP's history section (Finding 9). |
| 4 Unknown = no Grype DB record | **CLOSED** | arch `:336` "a vulnerability ID that the vulnerability data used for matching (the active Grype DB) has no record for — even when the CVE List… already lists it"; "Only a known vulnerability — one with a record in the active Grype DB"; UX-DR40 `epics.md:236`; 6.2 `:1750`, `:1759`; 6.3 `:1782`; DES:724; EXP:110, `:255-256`, `:394`. All say Grype DB, and none says "any loaded feed". |
| 5 Issue sentence source | **CLOSED** (with an ungated detail, Finding 2) | PRD `:61` "the first sentence of the advisory's own description, as published and with its source (FR12)"; arch `:257` "Issue sentence (decided 2026-11-07)… Armoury never rewrites or generates it"; ARCH38 `:165`; UX-DR22 `:212`; 2.10 `:932`; EXP:62, `:411`. No "plain sentence of what it means" remains (grep). |
| 6 Review all N mechanism | **CLOSED** (with ungated details, Findings 1 and 3) | arch `:257` "The list also takes `needs_attention=true`… the Issues 'Needs attention' filter and Home's 'Review all N' use it"; ARCH38 `:165`; UX-DR11 `:198`, UX-DR16 `:203`, UX-DR22 `:212`, UX-DR38 `:234`; 5.2 `:1528`; 5.4 `:1597`; EXP:60, `:70`, `:207`, `:210`, `:243`, `:413`, `:484` (Open item 4 resolved). |
| 7 `?` destination | **CLOSED** | UX-DR6 `:190`, UX-DR7 `:191`, UX-DR44 `:240`; 1.8 `:619` "open the ⌘K palette on its Keyboard shortcuts view (the same dialog, no new modal)"; gate `:620` (view layout set before Build, Open item 13); DES:731; EXP:226, `:298`, `:496`, `:510`; IA/epic-1-context.md:120. |
| 8 Lime exceptions | **CLOSED** (minor list drift, Finding 7) | DES:24, `:570`, `:596`, `:702`; UX-DR1 `epics.md:182`; 1.9 `:642`; IA/epic-1-context.md:135. Each covers the focus ring (sidebar, forest selection, dark), the moved-map centre dot (DES:468) and `lime-wash`/`lime-ring` (DES:26-27, `:533-535`). |

## Findings

1. **Concern — the Needs attention filter's URL value and the reset of other filters are open (CR Q5), and no story AC gates them. The architecture already fixes the walk order that Q5 still lists as open.**
   - Stories: 5.2 (builds the filter), 5.4 (Review all N).
   - Evidence:
     - CR Q5 (§6): "The URL value of the Needs attention filter (for example `review=needs-attention`…); whether Review all N resets the type filter and search; and whether the walk follows the Issues order… or Home's Needs-attention order… Gated by: Story 5.4 Build".
     - Neither 5.2 (`epics.md:1528`) nor 5.4 (`:1597`) has a "set before Build" clause. The filter's URL is built in 5.2, not 5.4.
     - `architecture.md:257` already says `needs_attention=true` "returns only groups with `needs_attention`, in the same order", which is the Issues order. Q5's third part is therefore already answered in the architecture, but Q5 still treats it as open.
   - Fix: add to 5.2 (or 5.4) "the URL value of the Needs attention option and whether Review all N clears the type filter and search are set in EXPERIENCE before Build (CR Q5)". Close Q5's order part by citing arch `:257`.
   - Owner: bmad-ux (+ bmad-correct-course, one-line AC).

2. **Concern — how the first sentence is cut, how its source is labelled, and which description wins between sources (CR Q2) are not gated in Story 2.10 or 4.4.**
   - Stories: 2.10, 4.4.
   - Evidence:
     - CR Q2: "how 'first sentence' is cut, and how the source is labelled beside it … Gated by: Story 2.10 Build (Grype DB only); Story 4.4 planning (precedence)".
     - 2.10 `epics.md:932` only says "the first sentence of the advisory description from the vulnerability record, unchanged, with its source", with no gate.
     - 4.4 (`:1272-1297`) has no description-precedence AC. It mirrors CNA "descriptions" (`:1282`) and says "each value is shown with its own source label" (`:1287`), which could mean two sentences.
   - Fix: add a pre-Build clause to 2.10 (sentence boundary rule and source label copy) and a planning gate to 4.4 (description precedence for the issue sentence).
   - Owner: bmad-architecture + bmad-ux.

3. **Concern — the Needs attention filter option's count is required to equal the badge, but nothing says whether the status-filter counts follow the active type filter and search.**
   - Stories: 5.2.
   - Evidence:
     - UX-DR38 `epics.md:234`: "The same number appears on Home…, in the Issues summary, as the count of the Issues 'Needs attention' filter option (UX-DR11) and as the Issues nav badge". EXP:207 says the same: "(with the Needs-attention count, the same number as Home and the badge)".
     - 5.2 `:1528-1530` lists the type filter, the Review status filter "with counts" and the search together, and says "they narrow the list server-side".
     - `architecture.md:257` says "the page carries counts per group and per triage status… the Needs-attention count" and does not say whether these are fleet-wide or scoped to the active type and search.
   - Impact: with type = Licences or a search active, a scoped option count would differ from the badge. That breaks UX-DR38, which this CR edit (E19) introduced.
   - Fix: state in ARCH38/5.2 that the Needs-attention count (and, if intended, every status count) is fleet-wide and ignores the type filter and search, or exempt the option from the same-number rule.
   - Owner: bmad-architecture + bmad-ux.

4. **Concern — CR Q4 (confirm or redraw the Negligible and Not rated yet markers) names Story 2.10 Build as its gate, but 2.10 does not carry the gate.**
   - Stories: 2.10 (and every list that renders severity).
   - Evidence:
     - CR Q4: "proposed… not drawn in the mock. Confirm or redraw… Gated by: Story 2.10 Build".
     - 2.10 `epics.md:932` says only "severity as a word + 4-step marker (UX-DR9)".
     - The spec itself is buildable: DES:310-311, `:578` and `:708`.
   - Fix: add "UX confirms the Negligible / Not rated yet markers before Build (CR Q4)" to 2.10, or record the confirmation in DES and close Q4.
   - Owner: bmad-ux.

5. **Concern — the rule that a later All places decision keeps per-software decisions is "decided" in the architecture but an [ASSUMPTION] in UX and Story 5.8, and 5.8 has no gate.**
   - Stories: 5.8.
   - Evidence:
     - `architecture.md:257`: "a later `all_places` decision leaves per-artifact decisions in place (Story 5.8)"; ARCH38 `epics.md:165` "per-artifact decisions override and survive a later `all_places` decision".
     - 5.8 `:1697`: "…the panel says how many keep theirs ("2 places keep their own status"; [ASSUMPTION], EXPERIENCE Open item 9)".
     - UX-DR16 `:203` "([ASSUMPTION], EXPERIENCE Open item 9)"; EXP:241 "[ASSUMPTION] A later 'All places' decision does not overwrite…"; EXP:489 Open item 9 is still [ASSUMPTION].
     - This was not created by the CR, which deliberately left "the other half of item 9" open (CR U36). It is still an ungated [ASSUMPTION].
   - Fix: mark Open item 9 decided (as the architecture already does), or add "confirmed by UX before Build" to 5.8.
   - Owner: bmad-ux.

6. **Note — CR Q1 (add "Published <date>; package data is not available yet") names Story 6.3 Build as its gate, but 6.3 does not carry it.**
   - Story: 6.3.
   - Evidence: 6.3 `epics.md:1782-1784` has the complete current copy. CR Q1 says "Left out for now".
   - Impact: none. The story is buildable as written, and Q1 is an optional enhancement.
   - Owner: bmad-ux.

7. **Note — the Story 1.9 lint and epic-1-context lime lists are a little shorter than DESIGN.md.**
   - Story: 1.9.
   - Evidence:
     - DES:570 and UX-DR1 `epics.md:182` include the "Selected on the map" marker. 1.9 `:642` and IA/epic-1-context.md:135 say only "selected map node including the centre dot". 1.9 does cite "DESIGN.md → Accent and selection".
     - The all-clear `disc-ring` uses `sprout-ring` (`#F1FADF99`, a translucent `lime-wash`: DES:57, `:534`, `:736`), which is not named in any of the lists.
   - Impact: a lint keyed on hex or hue could flag either one.
   - Fix: add "and its 'Selected on the map' marker" and `sprout-ring` to 1.9 and epic-1-context.
   - Owner: bmad-correct-course.

8. **Note — "when places differ / have different statuses" wording no longer matches the Q7 rule.**
   - Evidence: DES:581 "the Mixed chip shown when places differ"; DES:712 "when the places an issue affects have different statuses"; EXP:461; UX-DR16 `epics.md:203` "('Mixed' when places now differ)".
   - Under the decided rule (arch `:257`, EXP:39), "Mixed" also shows when every place has the same per-software decision and there is no All places decision (N = M).
   - Impact: none on behaviour. Each line points to the rule, but the phrasing can mislead.
   - Owner: bmad-ux.

9. **Note — the EXPERIENCE "what changed" history still lists four severity groups and says FR13 "needs reconciling".**
   - Evidence: EXP:459 "severity groups Critical / High / Medium / Low… The PRD's FR13 wording… needs reconciling". This contradicts EXP:71, `:205` and Open item 26 (`:512`, resolved).
   - Impact: history section only, so not normative.
   - Owner: bmad-ux.

10. **Note — epic-1-context does not carry the Story 1.8 gate for the Keyboard shortcuts view layout.**
    - Evidence: IA/epic-1-context.md:119 gates only the `g` letters; 1.8 `epics.md:620` also gates "the layout of the palette's Keyboard shortcuts view"; EXP:496.
    - Fix: append it to epic-1-context.md:119-120.
    - Owner: bmad-correct-course (or regenerate with compile-epic-context).

11. **Note — the architecture defines `unrated` as Grype Unknown, while Story 5.1 still decides severity-source precedence.**
    - Evidence:
      - `architecture.md:257` "`unrated` is Grype's Unknown or no severity"; ARCH38 `epics.md:165`.
      - 5.1 `:1496` gates "severity groups and severity-source precedence" in an amendment before implementation.
    - Impact: the gate is valid. If precedence lets CNA or OSV severity win, issues can move out of Not rated yet, or into Critical, and Needs-attention counts change. The 5.1 amendment must also update ARCH38's group definitions.
    - Owner: bmad-architecture (at Story 5.1 planning).

12. **Note — Story 5.6 specifies Mixed and effective-status VEX before Story 5.8 creates per-software decisions.**
    - Evidence: 5.6 `epics.md:1646` "when an issue is Mixed, each product's statement carries its own effective status"; 5.8 `:1703` "the findings API and VEX export (Story 5.6) use the resulting current status per place".
    - Impact: the Mixed branch in 5.6 is untestable until 5.8. This is not new: the CR only reworded the existing sentence.
    - Fix: say in 5.6 that the per-software case is tested in 5.8.
    - Owner: bmad-correct-course.

**Counts:** 0 blockers · 5 concerns (1–5) · 7 notes (6–12).
**No actionable blocker findings remain.** The ~45 earlier readiness concerns that the CR left open are outside this lens.
