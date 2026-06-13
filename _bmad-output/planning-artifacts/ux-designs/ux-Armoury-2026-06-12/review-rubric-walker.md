# Spine Pair Review — Armoury (rubric walker)

Finalize-time validation of `DESIGN.md` + `EXPERIENCE.md` as the contract for downstream consumers. Checked against `references/design-md-spec.md`, `.decision-log.md`, `.working/source-digest.md`, and internal cross-reference integrity. Read-only audit; severity = downstream impact.

## Overall verdict

A strong, unusually disciplined spine pair: every decision-log lock is honored in spirit, all `{path.to.token}` references resolve, three-theme semantic parity holds, the DQ hue is severity-distinct in all three themes, and the flows hit protagonist/steps/climax/failure cleanly. Two blockers stand between this and a clean finalize: untokenized Forge-only hexes that contradict the locked theme-switchability decision, and a UI-relevant FR (license policy authoring) with no home in the IA. The should-fix list is mostly the known reconcile-prd partials that finalize should now resolve rather than re-record.

## Category verdicts

- Flow coverage — **strong** (UJ-1/2/3 each: named protagonist, numbered steps, climax beat, failure path)
- Token completeness — **adequate** (all references resolve; hard-coded tint hexes are the blocker below)
- Component coverage — **strong** (one frontmatter orphan, see nits)
- State coverage — **adequate** (core honest-degradation states excellent; a few surface-level gaps)
- Visual reference coverage — **adequate** (all 8 `.working/` renders cited, spines-win stated in both; one empty import)
- Bloat & overspecification — **strong** (tight; minor editorial voice leakage in EXPERIENCE)
- Inheritance discipline — **adequate** (sources resolve, UJ names verbatim; glossary subset issue)
- Shape fit — **strong** (DESIGN canonical order exact; EXPERIENCE all required defaults present; invented sections all load-bearing)

---

## Blockers (2)

### B1 — Theme-switchability broken by hard-coded Forge hexes
**DESIGN.md** — frontmatter `components.icon-rail.background: '#151211'`; Elevation & Depth (`#181513` row hover, `#221E1A` active rail item); Components table (Findings table hover `#181513 (Forge)`).
The decision log locks "Token system must be theme-switchable (shadcn CSS variables)" and the spine's own Do's and Don'ts bans "Components referencing theme-specific hexes" — yet the rail background and the two raised-tint values are raw Forge hexes with **no semantic token and no High Signal / Gunmetal equivalents**. A downstream implementer cannot render the rail, row hover, or active-item state in two of the three day-1 themes.
*Fix:* add semantic roles (e.g. `surface-sunken`, `surface-raised`, `surface-active`) to all three theme maps in `colors`; reference them from `components.icon-rail` and the Elevation/Components prose. (`#221E1A` already equals Forge `hairline` — decide whether that aliasing is intentional or coincidental.)

### B2 — FR27 license policy authoring has no surface
**EXPERIENCE.md** — Information Architecture / Settings row; Component Patterns.
FR27 (fleet-wide license allow/deny policy) is a UI-relevant FR: violations-as-findings are covered, but the admin surface where the policy is *authored* exists nowhere in the 7-surface IA. Already recorded in `reconcile-prd.md` (gap #3) — at finalize, recording is not resolving. A story-dev consumer has no home to build this into.
*Fix:* add license policy (allow/deny list management, admin role) to the Settings IA row and a behavioral note (who edits, how violations re-evaluate on policy change).

## Should-fix (10)

### S1 — Severity-band opacity contradicts the log and the spine's own prose
**DESIGN.md** — frontmatter `components.severity-band.fill-opacity: '0.55–0.80'` vs Brand & Style / Colors prose and `.decision-log.md` ("severity fills at 0.6–0.85 opacity"). *Fix:* align the token to 0.6–0.85 (or state why the band specifically runs lower).

### S2 — Locked glossary omits *Control plane* / *Cluster agent*
**EXPERIENCE.md** — Voice and Tone, locked glossary. Source glossary (digest §D) includes both; the spine's "identical across product, packs, and docs" list drops them while Foundation uses the terms freely. *Fix:* add both terms to the locked set.

### S3 — `imports/weblytics.html` is a 0-byte file cited as a lifted reference
**EXPERIENCE.md** — Inspiration & Anti-patterns, first bullet. The file is empty (Dribbble blocked the import); the inline link implies viewable content. *Fix:* delete the empty file and cite the Dribbble URL only (as the spine header already does), or note "(URL-only; import blocked)".

### S4 — FR6 uniformity is never a user-facing claim
**EXPERIENCE.md** — Posture / Settings / Flow 1. The PRD's chassis promise ("every image SBOM'd and scanned the same way") appears in no copy, stat, or surface (reconcile-prd gap #1). *Fix:* one line of posture or freshness-strip copy (e.g. "All N artifacts scanned with the same Syft/Grype config, vX") claims it.

### S5 — FR23 evidence retention setting absent
**EXPERIENCE.md** — IA, Settings row. Configurable retention with the 24-month compliance floor has no home. *Fix:* add to Settings IA purpose list.

### S6 — FR20 Prometheus endpoint discoverability unspecified
**EXPERIENCE.md** — IA / Settings. The pull-only stance is honored but where an operator finds the endpoint URL/scrape config is unstated. *Fix:* add to Settings (read-only, copyable endpoint + sample scrape config).

### S7 — NFR9 agent trust copy missing from install flow
**EXPERIENCE.md** — Flow 1 step 5 / Settings agent install. "Watch/list only, never cluster-admin" reassurance — a trust nuance the PRD leans on — never appears. *Fix:* one sentence of install-affordance copy.

### S8 — FR11 feed enumeration omits CNA records and OSV
**EXPERIENCE.md** — Honest Provenance, freshness-strip bullet ("Grype DB, KEV catalog, EPSS, SBOM index, runtime observation"). *Fix:* extend the enumerated list or mark it non-exhaustive ("every connected feed").

### S9 — Pack signature verification affordance unspecified (UJ-3/FR25)
**EXPERIENCE.md** — Flow 3 / Evidence pack generator row. Packs are "tamper-verifiable" but how Marta or the auditor verifies is never specified. *Fix:* name the mechanism (e.g. verify command / fingerprint printed on the cover sheet).

### S10 — No long-running-query state for blast radius (NFR2 worst case)
**EXPERIENCE.md** — State Patterns. NFR2 allows "under a minute worst case"; no state describes what the surface shows between Enter and answer (skeleton? progressive tiers?). *Fix:* one State Patterns row (progressive render or honest "evaluating N artifacts…" state).

## Nits (7)

1. **DESIGN.md, frontmatter + Layout** — `heading-block` has frontmatter tokens and Layout prose but no row in the Components table; extraction-by-table misses it. Add a row or fold its tokens into Layout.
2. **DESIGN.md, frontmatter** — `spacing.zone-gap-sm` (48px) is defined but never referenced; prose says "{spacing.zone-gap} (48–56px)". Reference it or drop it.
3. **DESIGN.md, Components** — Findings table headers "9.5–10px" vs the 10px `micro-label` token; KEV tag "at 0.85" alpha appears in the table but not the frontmatter token. Align table to tokens.
4. **DESIGN.md, frontmatter/prose** — `tabular-nums` for numerals lives only in prose; fine per spec, but worth a comment beside `hero-numeral` so token consumers don't miss it.
5. **EXPERIENCE.md, Inspiration & Anti-patterns** — the AmazingUI Dribbble shot that seeded the graph requirement is uncited (lineage only in `.decision-log.md`; see `reconcile-dribbble-inspiration.md`). Add the URL-only citation.
6. **EXPERIENCE.md, prose voice** — editorial flourishes ("no illustration theatre", "honest, partial, alive") leak DESIGN-style voice into EXPERIENCE; harmless but the spec assigns editorial voice to DESIGN only.
7. **EXPERIENCE.md, State Patterns** — empty Evidence trail (pre-first-decision) and artifact-detail-without-SBOM states unspecified; both are derivable from existing patterns but cheap to name.

## Mechanical notes

- All `{path.to.token}` references in both spines resolve to frontmatter tokens by exact name (including `{components.dq-badge}`, `{components.graph-node}`, `{components.graph-edge-affected}`, `{components.button-primary}`).
- Three-theme parity: all 15 semantic color roles present in Forge, High Signal, and Gunmetal maps. ✔ (Parity is broken only by the *untokenized* tints in B1.)
- No severity hue reused for data-quality in any theme (#8FAFAF / #C7AEF0 / #A493C9 are hue-distinct from all three severity ramps). ✔
- Locked Forge hexes match `.decision-log.md` values exactly, including `text-data` #D4CCC2. ✔
- `sources` frontmatter: all four paths resolve on disk. ✔
- UJ names, personas, roles, triage status set, and IA's 7 surfaces match the decision log and digest verbatim. ✔
- DESIGN body sections in canonical spec order; EXPERIENCE carries all eight required defaults plus defensible invented sections. ✔
- Spines-win-on-conflict stated once in each spine. ✔ No Mermaid present.
