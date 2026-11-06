# Validation Report — Armoury

- **DESIGN.md:** `_bmad-output/planning-artifacts/ux-designs/ux-Armoury-2026-11-06/DESIGN.md`
- **EXPERIENCE.md:** `_bmad-output/planning-artifacts/ux-designs/ux-Armoury-2026-11-06/EXPERIENCE.md`
- **Run at:** 2026-11-06

## Overall verdict

The pair is a clean, extractable contract. Every `{path.to.token}` reference resolves (357 in DESIGN.md, 25 in EXPERIENCE.md). All 42 colour roles have hex values in both Light and `-dark`. The stated contrast table matches recomputed values to ±0.05. UJ-1, UJ-2 and UJ-3 are covered verbatim, each with a protagonist, steps, a climax and a failure path. The weak spot is **state coverage**. Four high-impact gaps would have forced downstream teams to invent product behaviour. (1) An Exposure "zero" could not tell "no software has it" from "we don't know this ID yet". (2) No pattern covered a failed save of a review decision or any other mutation. (3) The unit of an "issue" was undefined when decisions differ across the places it affects. (4) The WCAG 2.2 AA claim could not hold while every viewport under 1280px was undesigned. There were no critical findings.

**Since the review:** the spines were updated after the rubric walker ran. Each finding below carries a resolution status, checked against the current DESIGN.md and EXPERIENCE.md. User decisions on 2026-11-06 resolved all 4 high findings (memlog entries 80–83), and the spines now carry them. Of the 24 findings, **16 are resolved**: 4 by decision and 12 in the spine. **8 remain as Open items** (19, 20, 27, 30, 31 ×2, 32, 33). The verdicts are the reviewer's verdicts at review time. Line references point to the spines as reviewed and may have shifted.

## Category verdicts

- Flow coverage — adequate
- Token completeness — adequate
- Component coverage — adequate
- State coverage — thin
- Visual reference coverage — strong
- Bloat & overspecification — adequate
- Inheritance discipline — strong
- Shape fit — adequate

## Resolution status

| Status | Count |
|---|---|
| Resolved (decision, memlog entries 80–83) | 4 |
| Resolved in spine | 12 |
| Open item (19, 20, 27, 30, 31, 31, 32, 33) | 8 |

## Findings by severity

### Critical (0)

None.

### High (4)

**[Component coverage]** — The unit of an "Issue" is undefined (§ EXPERIENCE.md L57, L69, L75, L86, L176, L333, L351)
An Issues or Home row was one package-version × vulnerability across the fleet ("14 places") with one status chip. The Exposure inspector and Software detail, however, show a review per piece of software, and Flow 2 records different decisions for different services. It was undefined what the single chip shows, whether a partly reviewed issue still counts as Not reviewed yet, and whether it leaves Needs attention. This blocked the data model, the per-product VEX output and the badge count.
Fix: Commit the issue unit. Then specify the aggregate chip for mixed decisions and how Needs attention and "not reviewed yet" count partial reviews.
Status: **Resolved (decision 2026-11-06, memlog entry 82)**. The spine now has The issue unit (IA), a scope control in the Review panel ("All 14 places" / "Only this software"), the Mixed · N of M status chip, and a Needs-attention rule for Mixed issues.

**[State coverage]** — Exposure "zero" cannot tell "none" from "unknown ID" (§ EXPERIENCE.md L214, L335)
The Empty answer and Flow 2's failure path could only say "No software has it". Nothing covered an ID the vulnerability data doesn't know yet, which on CVE day is exactly the likely case. The screen would show a coverage-scoped all-clear for something it never evaluated, which breaks the signature rule and FR17.
Fix: Add a distinct state ("We don't have CVE-… in our vulnerability data yet") showing the feed age and linking to Sources, plus a separate "not found" message for unknown packages and fingerprints.
Status: **Resolved (decision 2026-11-06, memlog entry 80)**. The spine has an "Unknown vulnerability" state, the Exposure IA rule and the Flow 2 failure path: "Armoury has no data for <ID> yet…" with Check again. Copy for an unknown package or fingerprint is Open item 28.

**[State coverage]** — No failure pattern for any mutation (§ EXPERIENCE.md L202, L253)
No failure pattern covered Save and next, Decide later, Check again, Export, Generate audit report, Settings saves or conflicting decisions. Toasts are banned, so there was no permitted way to say "not saved". Because Save and next auto-advances, a silent failure would leave a missing audit decision that nobody notices.
Fix: Add a "Save failed" row: the panel stays on the issue, shows an inline clay-wash error and keeps "Why?". Add a generic inline-error rule and a stale-decision rule.
Status: **Resolved (decision 2026-11-06, memlog entry 81)**. The spine has a "Save failed" state, an Inline error pattern, the `{components.inline-error}` visual spec and a failure line in the Review flow. The rule for conflicting or concurrent decisions is Open item 29.

**[Shape fit]** — Viewports under 1280px are undesigned, but WCAG 2.2 AA is contractual (§ EXPERIENCE.md L267, L283)
AA includes 1.4.10 Reflow (usable at 320 CSS px) and 1.4.4 Resize text (200%). Fixed column widths of 252 + 376/500 + detail cannot meet these without a collapse model. A 1280px laptop already yields a viewport under 1280 once browser chrome is counted. This decision also shapes the routing, persistence and focus model.
Fix: Commit a collapse model now: below 1280px, list and detail stack as two routes with Back, and the sidebar becomes a rail and then a sheet.
Status: **Resolved (decision 2026-11-06, memlog entry 83)**. The Responsive & Platform table now specifies an icon rail below 1280px and one stacked column with Back below 1024px. The Accessibility Floor has a Reflow line, and DESIGN.md Layout covers narrower viewports.

### Medium (11)

**[Flow coverage]** — FR31 (Optional CI scan) has no surface or flow (§ EXPERIENCE.md Coverage table; L99)
FR31 was added to the PRD on 2026-11-05 but appears in neither the Coverage table nor any flow. The spine mentions only "CI policy" and "CI tokens" in the Settings panel list. The artifact link that every CI run prints needs a landing place. Uploaded image or package archives fit neither "Deployed" nor "Not deployed". The CI verdict and its history need a home in Software detail.
Fix: Add an FR31 row to the "Stated need" table and one line to Software saying where CI-submitted software appears, its provenance label and where the CI verdict shows. Alternatively, list FR31 in Open items as undesigned.
Status: **Open item 27**. An FR31 row is now in the Stated need table. How CI-only software is grouped and labelled, and where the verdict shows, is still open.

**[Token completeness]** — Selected-row foreground colours only partly specified (§ DESIGN.md L283, L298, L301, L403)
`exploited-text`, `kind-tag`, `licence-marker` and `table` (muted cells) had no on-selection colours, although the mock switches them to `sage-hi` / `sel-chip`. Because the spine wins, the contract read from the spine alone would put clay "Actively exploited" text on forest at 1.96:1 and text-2 on forest at 1.88:1.
Fix: Add `on-selection-foreground: '{colors.sage-hi}'` to exploited-text, licence-marker and kind-tag, plus `on-selection-background: '{colors.sel-chip}'` on kind-tag. Add `selected-foreground` and `selected-secondary` to `table`.
Status: **Resolved in spine**. exploited-text, licence-marker and kind-tag now have on-selection tokens. `table` has selected-foreground, selected-secondary and selected-chip-* tokens. The Components prose matches.

**[Token completeness]** — Composite component tokens a resolver cannot flatten (§ DESIGN.md L253, L392, L403ff)
Values such as `'1px inset {colors.ink-line}'` and `'{typography.meta}, weight 500, {colors.text-3}'` mix several properties in one string. Generating a theme from them (for example Tailwind or shadcn) needs hand-parsing, and references embedded in prose drift easily.
Fix: Split them into atomic keys (border-width, border-color, font, font-weight, color), or keep each composite as a `note:` beside atomic keys.
Status: **Open item 31**. Composite strings remain and are listed under token hygiene.

**[Token completeness]** — Input boundaries miss non-text contrast (WCAG 1.4.11) (§ DESIGN.md L334, L522, L586; EXPERIENCE.md L267)
The "Why?" textarea was a paper fill with a 1px rule on canvas: 1.08:1 for the fill and 1.23:1 for the border in light, 1.31:1 in dark. An empty required field was effectively invisible at rest, yet the spine claims AA in both themes.
Fix: Give the resting border of `field` and `review-note-field` a token of at least 3:1, or justify the exemption. Add the pair to the non-text contrast line.
Status: **Resolved in spine**. New `{colors.field-border}` (#737D77 / dark #748079) is used on field and review-note-field. It is listed in the non-text contrast line and in the Accessibility Floor ("Field edges meet 3:1 at rest").

**[Token completeness]** — Print palette is raw hex with no tokens (§ DESIGN.md L605, L610)
The print palette existed only as hex values in prose (`#1A1A1A`, `#555555`, `#D0D0D0`), and the print severity colours were never named. Whoever writes the Typst template for the UJ-3 audit report would have to guess.
Fix: Add `print-*` tokens (text, text-2, rule and four severities, with contrast on white), or map print severity to the light-theme tokens.
Status: **Resolved in spine**. The frontmatter now has `print-page`, `print-text`, `print-text-2`, `print-rule` and `print-critical/high/medium/low`, with contrast on white. Printed report references them.

**[Component coverage]** — The Needs-attention rule can be read two ways (§ EXPERIENCE.md L57, L172)
The rule read "Not reviewed yet AND (Actively exploited OR Critical), plus licence decisions". With 9 open licences, 1 of them not reviewed yet, "plus licence decisions" reads as 9, but the mock and Flow 4 show 1. The spine requires the same number everywhere.
Fix: Rewrite it as "Not reviewed yet AND (Actively exploited OR Critical OR Licence)".
Status: **Resolved in spine**. Home and Component Patterns now read "Every licence issue that is Not reviewed yet also needs attention."

**[Component coverage]** — Components used in flows have no spec (code block, signature, report generation) (§ EXPERIENCE.md L183, L184, L210)
Several components that carry the trust moments of UJ-1 and UJ-3 had no spec: the copyable command block with Copy, the "Signature verified" block, the in-progress audit-report row and the control that adjusts window, scope and framework after the click.
Fix: Add `code-block` and `signature-status` rows to DESIGN.md Components. Add a Component Patterns row for report generation covering the in-progress row, adjustment after the click and re-generation.
Status: **Open item 19**. Code block and Signature status now have rows in both spines. The in-progress row, adjustment after the click and re-generation semantics remain open.

**[State coverage]** — First-visit and zero states missing (§ EXPERIENCE.md State Patterns)
Four zero states had no copy: Issues with the "Not reviewed yet" filter at 0, an Issues search with no match, Exposure opened from the sidebar with no query, and Reports with no audit reports or exports yet.
Fix: Add three State Patterns rows with copy.
Status: **Resolved in spine**. State Patterns now has Nothing to review, Search no match, No query and Nothing yet (Reports), each with copy.

**[State coverage]** — No state for a signature that fails to verify (§ EXPERIENCE.md L184; Flow 3 step 4)
Only "Signature verified" was specified. A failed verification, a missing key and a key mismatch had no state, although verification is central to FR25 and to the auditor's trust in UJ-3.
Fix: Add a "Signature does not verify" state: a clay-wash band naming the file and the key, with no download hidden.
Status: **Resolved in spine**. State Patterns has "Signature does not verify" (error band naming the file and the reason, no download hidden, link to the trail entry), and DESIGN.md has a Signature status row. The failure output of the offline command is not written separately.

**[State coverage]** — Registry-unreachable state puts two lime actions in one view (§ EXPERIENCE.md L77, L218, L253)
The lime Try again appeared alongside the lime Add software. Two lime actions in one view is banned.
Fix: While an error band shows, its recovery action takes the view's lime and the list's primary action turns grey.
Status: **Resolved in spine**. The registry-unreachable row now says "Add software turns grey (secondary) while the band shows".

**[Shape fit]** — Single-key shortcuts need an off switch (WCAG 2.1.4) (§ EXPERIENCE.md L99, L243–248)
`J`, `K`, `/`, `x`, `?` and `g`+letter must be possible to turn off or remap, unless they are active only on focus. Settings → Personal listed "keyboard shortcuts" but committed to neither.
Fix: State that single-key shortcuts can be turned off in Settings → Personal.
Status: **Resolved in spine**. Interaction Primitives, the Accessibility Floor and Settings → Personal now state: active only outside text fields, and can be turned off.

### Low (9)

**[Token completeness]** — 22px wordmark breaks the nine-size rule (§ DESIGN.md L108, L111, L528)
The 22px wordmark broke the "Nine sizes only" rule and the "Intermediate sizes" Don't. The token also could not express Bold Italic.
Fix: State "22 — wordmark only" as an exception and add an italic note to the token.
Status: **Resolved in spine**. The single exception is stated in the frontmatter, in Typography and in the Do's and Don'ts. Bold Italic is a YAML comment on the token, not a `note:` key.

**[Token completeness]** — Orphan tokens: amber-wash and forest-3 (§ DESIGN.md L30, L49)
`amber-wash` was described as the background of an amber tag, but no such component existed. `forest-3` was described as the start of an avatar gradient, but there was no avatar component.
Fix: Either specify the avatar and the amber tag, or remove the tokens.
Status: **Resolved in spine**. `amber-wash` was removed. `forest-3` is now `user-menu.avatar-start`.

**[Component coverage]** — DESIGN.md components with no behavioural row (§ EXPERIENCE.md Component Patterns)
Six components have a visual spec but no behaviour: Segmented control (URL and keyboard), Table (sort keys and default order), Pager (whether `J`/`K` cross pages), Fields/search (clearing), Technical details (always open or collapsible) and Gauges & charts (text alternative).
Fix: Add one row each, or one line saying "Inherited shadcn behaviour unless stated".
Status: **Open item 20**. These rows are listed as not yet written. Until they are, shadcn defaults apply.

**[Component coverage]** — Signed-in user at the sidebar foot has no behaviour (§ EXPERIENCE.md Component Patterns)
The account menu and sign out were not specified, and there was no avatar component.
Fix: Add one Component Patterns row.
Status: **Resolved in spine**. User menu now has a row in both spines (`{components.user-menu}`), covering Personal settings, Sign out and the keyboard model.

**[State coverage]** — Global states missing (§ EXPERIENCE.md State Patterns)
Three global states were missing: session expired and re-authentication, control plane unreachable (single instance, NFR10), and a direct link to a panel or action the role cannot use.
Fix: Add one row each.
Status: **Open item 30**. Listed as an unresolved gap.

**[Bloat & overspecification]** — Components table restates token values as literal pixels (§ DESIGN.md L581, L585)
Rows such as "Tabs … 64px" and "Buttons … 42px … 32px … 54px" repeated token values as literal pixels. Other dimensions had no token at all: 26px tab padding, 128px term column, 120px gauge, 56px sparkline, 84px disc and 660px palette. Each duplicate can drift from its token.
Fix: Reference the tokens, tokenise recurring dimensions, and mark the rest as component-internal.
Status: **Open item 31**. Buttons now cite `{spacing.button-height*}`. The Tabs row still says 64px, and the untokenised dimensions are listed under token hygiene.

**[Bloat & overspecification]** — Printed report content restated in both spines (§ DESIGN.md L601–612; EXPERIENCE.md L287–295)
The cover sheet with its coverage statement, the page footer and the plain labels appear in both spines.
Fix: Keep the visual rules in DESIGN.md and the content contract in EXPERIENCE.md, and cross-link them.
Status: **Open item 32**. Listed as open.

**[Inheritance discipline]** — Component names drift between files (§ EXPERIENCE.md L185; DESIGN.md L594)
Several components had different names in each file: "Freshness strip" vs "Data-source freshness strip", "Key cap" vs `kbd`, "Actively exploited marker" vs "Actively exploited — text / pill", and "Grouped list" vs "List row" + "Group heading".
Fix: Use one name per component in both spines, matching the token key.
Status: **Resolved in spine**. "Freshness strip" is now used in both files. Rows now cite their component token: Key cap cites `{components.kbd}`, the marker is now "Actively exploited marker — text / pill", and Grouped list names List row, Group heading and Pager. "Key cap" still differs from the key `kbd`.

**[Inheritance discipline]** — "Needs a decision" is undefined, and the "Running" ban is too broad (§ EXPERIENCE.md L351)
Flow 4 used "Needs a decision", which was not in the glossary. The retired-label list bans "Running", yet the hint says "Not seen running…" and the glossary says "Running replicas".
Fix: Add "Needs a decision" to the glossary, and narrow the ban to "Running as a group or label".
Status: **Open item 33**. "Needs a decision" is now in the glossary. The wording of the "Running" ban is still open.

## Mechanical notes

- No references were unresolved. The literal placeholder `{path.to.token}` at EXPERIENCE.md L18 would trip an automated resolver. *Now fixed: the line reads "curly-brace reference form".*
- Colours: 42/42 light↔dark pairs, and every value is valid hex. The mock CSS matches the spine exactly, and the spine contrast table checks out.
- Typography tokens without `lineHeight`: `button-label`, `mono-id`, `display-reserved`. *Still open: Open item 31.*
- Open item 10 had a garbled fragment (a stray quote and parenthesis). *Now fixed.*
- In-page anchors resolve. There is no Mermaid. Frontmatter is complete in both files. At review time the Open items were numbered 1–24; they are now numbered 1–33.

## Reviewer files

- `review-rubric.md`
