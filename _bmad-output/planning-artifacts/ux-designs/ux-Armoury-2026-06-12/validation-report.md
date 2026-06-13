# Validation Report — Armoury

- **DESIGN.md:** `/var/home/danielbooth/projects/home/infantrycloud/armoury/_bmad-output/planning-artifacts/ux-designs/ux-Armoury-2026-06-12/DESIGN.md`
- **EXPERIENCE.md:** `/var/home/danielbooth/projects/home/infantrycloud/armoury/_bmad-output/planning-artifacts/ux-designs/ux-Armoury-2026-06-12/EXPERIENCE.md`
- **Run at:** 2026-06-12 (this run)

> **Note:** a fix pass is being applied in this same finalize run — findings B1–B2 and S1–S10 are scheduled for resolution.

## Overall verdict

A strong, unusually disciplined spine pair: every decision-log lock is honored in spirit, all `{path.to.token}` references resolve, three-theme semantic parity holds, the DQ hue is severity-distinct in all three themes, and the flows hit protagonist/steps/climax/failure cleanly. Two blockers stand between this and a clean finalize: untokenized Forge-only hexes that contradict the locked theme-switchability decision, and a UI-relevant FR (license policy authoring) with no home in the IA. The should-fix list is mostly the known reconcile-prd partials that finalize should now resolve rather than re-record.

The reconciliation lens corroborates this picture: of 44 PRD items (30 FR, 11 NFR, 3 UJ), 37 are covered, 6 are partial, 1 (NFR7, non-UI by nature) is intentionally excluded, and 0 are dropped. The 6 partials align one-to-one with the rubric walker's should-fixes (FR6 uniformity claim, FR11 feed enumeration, FR20 endpoint discoverability, FR23 retention setting, FR27 policy authoring — escalated to blocker B2 — and NFR9 agent trust copy). The inspiration audit confirms both Dribbble references landed (Weblytics strongly, AmazingUI amplified into two graph surfaces), with one cosmetic gap: the AmazingUI shot is uncited in either spine.

## Category verdicts

- Flow coverage — strong
- Token completeness — adequate
- Component coverage — strong
- State coverage — adequate
- Visual reference coverage — adequate
- Bloat & overspecification — strong
- Inheritance discipline — adequate
- Shape fit — strong

## Findings by severity

### Critical (2)

**[Token completeness]** — B1: Theme-switchability broken by hard-coded Forge hexes (DESIGN.md — `components.icon-rail.background`; Elevation & Depth; Components table)
The decision log locks "Token system must be theme-switchable (shadcn CSS variables)" and the spine's own Do's and Don'ts bans "Components referencing theme-specific hexes" — yet the rail background (#151211) and the two raised-tint values (#181513 row hover, #221E1A active rail item) are raw Forge hexes with no semantic token and no High Signal / Gunmetal equivalents. A downstream implementer cannot render the rail, row hover, or active-item state in two of the three day-1 themes.
Fix: add semantic roles (e.g. `surface-sunken`, `surface-raised`, `surface-active`) to all three theme maps in `colors`; reference them from `components.icon-rail` and the Elevation/Components prose. (#221E1A already equals Forge `hairline` — decide whether that aliasing is intentional or coincidental.)

**[Inheritance discipline]** — B2: FR27 license policy authoring has no surface (EXPERIENCE.md — Information Architecture / Settings row; Component Patterns)
FR27 (fleet-wide license allow/deny policy) is a UI-relevant FR: violations-as-findings are covered, but the admin surface where the policy is *authored* exists nowhere in the 7-surface IA. Already recorded in `reconcile-prd.md` (gap #3) — at finalize, recording is not resolving. A story-dev consumer has no home to build this into.
Fix: add license policy (allow/deny list management, admin role) to the Settings IA row and a behavioral note (who edits, how violations re-evaluate on policy change).

### High (4)

**[Token completeness]** — S1: Severity-band opacity contradicts the log and the spine's own prose (DESIGN.md — `components.severity-band.fill-opacity`)
Frontmatter token says '0.55–0.80' vs Brand & Style / Colors prose and `.decision-log.md` ("severity fills at 0.6–0.85 opacity") — an implementer gets conflicting values for the soft-chart signature.
Fix: align the token to 0.6–0.85 (or state why the band specifically runs lower).

**[Inheritance discipline]** — S4: FR6 uniformity is never a user-facing claim (EXPERIENCE.md — Posture / Settings / Flow 1)
The PRD's chassis promise ("every image SBOM'd and scanned the same way") appears in no copy, stat, or surface (reconcile-prd gap #1) — the product's core promise is invisible.
Fix: one line of posture or freshness-strip copy (e.g. "All N artifacts scanned with the same Syft/Grype config, vX") claims it.

**[Inheritance discipline]** — S5: FR23 evidence retention setting absent (EXPERIENCE.md — IA, Settings row)
Configurable retention with the 24-month compliance floor has no home.
Fix: add to Settings IA purpose list.

**[Flow coverage]** — S9: Pack signature verification affordance unspecified (UJ-3/FR25) (EXPERIENCE.md — Flow 3 / Evidence pack generator row)
Packs are "tamper-verifiable" but how Marta or the auditor verifies is never specified — a story-dev consumer has no mechanism to build.
Fix: name the mechanism (e.g. verify command / fingerprint printed on the cover sheet).

### Medium (6)

**[Inheritance discipline]** — S2: Locked glossary omits *Control plane* / *Cluster agent* (EXPERIENCE.md — Voice and Tone, locked glossary)
Source glossary (digest §D) includes both; the spine's "identical across product, packs, and docs" list drops them while Foundation uses the terms freely.
Fix: add both terms to the locked set.

**[Visual reference coverage]** — S3: `imports/weblytics.html` is a 0-byte file cited as a lifted reference (EXPERIENCE.md — Inspiration & Anti-patterns, first bullet)
The file is empty (Dribbble blocked the import); the inline link implies viewable content.
Fix: delete the empty file and cite the Dribbble URL only (as the spine header already does), or note "(URL-only; import blocked)".

**[Inheritance discipline]** — S6: FR20 Prometheus endpoint discoverability unspecified (EXPERIENCE.md — IA / Settings)
The pull-only stance is honored but where an operator finds the endpoint URL/scrape config is unstated.
Fix: add to Settings (read-only, copyable endpoint + sample scrape config).

**[Flow coverage]** — S7: NFR9 agent trust copy missing from install flow (EXPERIENCE.md — Flow 1 step 5 / Settings agent install)
"Watch/list only, never cluster-admin" reassurance — a trust nuance the PRD leans on — never appears.
Fix: one sentence of install-affordance copy.

**[Inheritance discipline]** — S8: FR11 feed enumeration omits CNA records and OSV (EXPERIENCE.md — Honest Provenance, freshness-strip bullet)
The strip enumerates "Grype DB, KEV catalog, EPSS, SBOM index, runtime observation"; CNA records and OSV are absent from any named UI list.
Fix: extend the enumerated list or mark it non-exhaustive ("every connected feed").

**[State coverage]** — S10: No long-running-query state for blast radius (NFR2 worst case) (EXPERIENCE.md — State Patterns)
NFR2 allows "under a minute worst case"; no state describes what the surface shows between Enter and answer (skeleton? progressive tiers?).
Fix: one State Patterns row (progressive render or honest "evaluating N artifacts…" state).

### Low (7)

**[Component coverage]** — Nit 1: `heading-block` missing from Components table (DESIGN.md — frontmatter + Layout)
Frontmatter tokens and Layout prose exist but no Components-table row; extraction-by-table misses it.
Fix: add a row or fold its tokens into Layout.

**[Token completeness]** — Nit 2: `spacing.zone-gap-sm` defined but never referenced (DESIGN.md — frontmatter)
48px token is unused; prose says "{spacing.zone-gap} (48–56px)".
Fix: reference it or drop it.

**[Token completeness]** — Nit 3: Findings table values drift from tokens (DESIGN.md — Components)
Headers "9.5–10px" vs the 10px `micro-label` token; KEV tag "at 0.85" alpha appears in the table but not the frontmatter token.
Fix: align table to tokens.

**[Token completeness]** — Nit 4: `tabular-nums` lives only in prose (DESIGN.md — frontmatter/prose)
Fine per spec, but token consumers may miss it.
Fix: add a comment beside `hero-numeral`.

**[Visual reference coverage]** — Nit 5: AmazingUI Dribbble shot uncited (EXPERIENCE.md — Inspiration & Anti-patterns)
The shot that seeded the graph requirement is uncited (lineage only in `.decision-log.md`; see `reconcile-dribbble-inspiration.md`).
Fix: add the URL-only citation.

**[Bloat & overspecification]** — Nit 6: Editorial voice leaks into EXPERIENCE (EXPERIENCE.md — prose voice)
Flourishes ("no illustration theatre", "honest, partial, alive") leak DESIGN-style voice into EXPERIENCE; harmless but the spec assigns editorial voice to DESIGN only.
Fix: neutralize or relocate the flourishes.

**[State coverage]** — Nit 7: Two derivable-but-unnamed states (EXPERIENCE.md — State Patterns)
Empty Evidence trail (pre-first-decision) and artifact-detail-without-SBOM states unspecified; both derivable from existing patterns but cheap to name.
Fix: name both states.

## Reconciliation lens

**PRD reconciliation** (`reconcile-prd.md`): 44 PRD items (30 FR + 11 NFR + 3 UJ) — Covered 37 · Partial 6 · Excluded 1 (NFR7, non-UI by nature) · Dropped 0. The six partials (FR6, FR11, FR20, FR23, FR27, NFR9) map one-to-one to the walker's should-fixes, with FR27 escalated to blocker B2. Qualitative at-risk item beyond the table: UJ-2's "no rescans, no rebuilds" quiet-magic moment isn't narrated in Flow 2 (only FR8 provenance carries it indirectly).

**Inspiration reconciliation** (`reconcile-dribbble-inspiration.md`): Weblytics landed strongly (soft-data posture, dark themes exceeded; soft tables became a deliberate operator-console fusion). AmazingUI landed amplified (two graph surfaces + full graph token set) but is never credited in either spine — carried as nit 5.

## Mechanical notes

- All `{path.to.token}` references in both spines resolve to frontmatter tokens by exact name (including `{components.dq-badge}`, `{components.graph-node}`, `{components.graph-edge-affected}`, `{components.button-primary}`).
- Three-theme parity: all 15 semantic color roles present in Forge, High Signal, and Gunmetal maps. (Parity is broken only by the untokenized tints in B1.)
- No severity hue reused for data-quality in any theme (#8FAFAF / #C7AEF0 / #A493C9 are hue-distinct from all three severity ramps).
- Locked Forge hexes match `.decision-log.md` values exactly, including `text-data` #D4CCC2.
- `sources` frontmatter: all four paths resolve on disk.
- UJ names, personas, roles, triage status set, and IA's 7 surfaces match the decision log and digest verbatim.
- DESIGN body sections in canonical spec order; EXPERIENCE carries all eight required defaults plus defensible invented sections.
- Spines-win-on-conflict stated once in each spine. No Mermaid present.

## Reviewer files

- `review-rubric-walker.md`
- `reconcile-prd.md`
- `reconcile-dribbble-inspiration.md`
