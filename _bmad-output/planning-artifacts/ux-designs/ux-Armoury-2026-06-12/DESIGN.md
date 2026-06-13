---
name: Armoury
description: Self-hosted software supply-chain evidence layer for SME security teams. shadcn/ui on React + Tailwind; dark-only, three user-selectable themes; this DESIGN.md specifies the full brand layer over shadcn defaults.
status: draft
updated: 2026-06-12
colors:
  # Semantic token layer mapped onto shadcn CSS variables. THREE dark themes
  # ship day 1, user-selectable: Forge (default, unsuffixed), High Signal
  # (-high-signal), Gunmetal (-gunmetal). No light mode exists or is planned.
  # Each theme remaps the SAME semantic roles; components never reference a
  # theme-specific value directly.
  #
  # —— Forge (default): warm graphite + ember amber ——
  background: '#121010'
  surface: '#1C1917'
  border: '#322C27'
  hairline: '#221E1A'
  text-primary: '#EDE7E0'
  text-data: '#D4CCC2'
  text-muted: '#9A9087'
  accent: '#D9A05B'
  severity-critical: '#D27D6E'
  severity-high: '#D2986B'
  severity-medium: '#C9B07E'
  severity-low: '#968D82'
  success: '#9DBA8C'
  warning: '#D9B36B'
  data-quality: '#8FAFAF'
  # rail-* tints: rail background sits one step below background; hover/active
  # are raised tints. High Signal / Gunmetal values are derived interpolations
  # between background and surface (mechanical derivation, same relationship
  # as the locked Forge values).
  rail-background: '#151211'
  rail-hover: '#181513'
  rail-active: '#221E1A'
  # —— High Signal: high-contrast, accessibility-leaning (AAA-targeting text) ——
  background-high-signal: '#060708'
  surface-high-signal: '#131517'
  border-high-signal: '#34383E'
  hairline-high-signal: '#2A2E33'
  text-primary-high-signal: '#F4F6F8'
  text-data-high-signal: '#DDE1E6'
  text-muted-high-signal: '#A6ADB8'
  accent-high-signal: '#93C5FD'
  severity-critical-high-signal: '#F2A0A0'
  severity-high-high-signal: '#EFB98A'
  severity-medium-high-signal: '#E3D391'
  severity-low-high-signal: '#A9B6C7'
  success-high-signal: '#A3D9B1'
  warning-high-signal: '#EFC98A'
  data-quality-high-signal: '#C7AEF0'
  rail-background-high-signal: '#0C0E10'
  rail-hover-high-signal: '#101316'
  rail-active-high-signal: '#1A1D21'
  # —— Gunmetal: near-black neutral, one restrained steel-blue accent ——
  background-gunmetal: '#0B0C0E'
  surface-gunmetal: '#15171B'
  border-gunmetal: '#262A31'
  hairline-gunmetal: '#22262C'
  text-primary-gunmetal: '#E7E9ED'
  text-data-gunmetal: '#C8CCD3'
  text-muted-gunmetal: '#878E9A'
  accent-gunmetal: '#9DB2D9'
  severity-critical-gunmetal: '#C97A7A'
  severity-high-gunmetal: '#C99A6B'
  severity-medium-gunmetal: '#C9BC85'
  severity-low-gunmetal: '#7E8A9C'
  success-gunmetal: '#8FBF9F'
  warning-gunmetal: '#C9A86B'
  data-quality-gunmetal: '#A493C9'
  rail-background-gunmetal: '#101216'
  rail-hover-gunmetal: '#14161A'
  rail-active-gunmetal: '#1C1F25'
typography:
  # Three families, hard role boundaries:
  #   Inter Display — display numerals & page titles (weights 200 / 500)
  #   Inter         — all UI text
  #   IBM Plex Mono — EVERY technical identifier: CVE IDs, package@version,
  #                   digests, cluster/namespace/workload paths, feed versions
  # Scale is deliberately asymmetric — not a modular ramp.
  hero-numeral:
    fontFamily: 'Inter Display'
    fontSize: 76px
    fontWeight: '200'
    lineHeight: '0.95'
    letterSpacing: -0.035em
  co-stat:
    fontFamily: 'Inter Display'
    fontSize: 34px
    fontWeight: '200'
    lineHeight: '1'
    letterSpacing: -0.025em
  page-title:
    fontFamily: 'Inter Display'
    fontSize: 23px
    fontWeight: '500'
    letterSpacing: -0.02em
  answer-headline:
    fontFamily: 'Inter Display'
    fontSize: 21px
    fontWeight: '300'
    letterSpacing: -0.015em
  body:
    fontFamily: 'Inter'
    fontSize: 14px
    lineHeight: '1.55'
  body-dense:
    fontFamily: 'Inter'
    fontSize: 12px
  mono-identifier:
    fontFamily: 'IBM Plex Mono'
    fontSize: 11.5px
    letterSpacing: '0'
  mono-meta:
    fontFamily: 'IBM Plex Mono'
    fontSize: 10.5px
  micro-label:
    fontFamily: 'Inter'
    fontSize: 10px
    fontWeight: '600'
    letterSpacing: 0.14em
  eyebrow:
    fontFamily: 'Inter'
    fontSize: 10px
    fontWeight: '600'
    letterSpacing: 0.16em
rounded:
  # Soft, never sharp; never pill-shaped containers.
  sm: 5px
  DEFAULT: 8px
  md: 9px
  lg: 12px
  node: 11px
  full: 9999px
spacing:
  # Tailwind 4-based scale inherited. Named tokens below are Armoury's rhythm:
  # generous BETWEEN zones, dense WITHIN data zones.
  zone-gap: 56px
  zone-gap-sm: 48px
  page-gutter: 52px
  rail-width: 58px
  data-row: 30px
  stat-gap: 44px
components:
  icon-rail:
    background: '{colors.rail-background}'
    border-right: '{colors.border}'
    width: '{spacing.rail-width}'
    item-radius: '{rounded.md}'
    active-indicator: '{colors.accent}'
  hero-stat:
    numeral: '{typography.hero-numeral}'
    label: '{typography.micro-label}'
    divider: '{colors.border}'
  severity-chip:
    radius: '{rounded.sm}'
    label: '{typography.micro-label}'
    fill-opacity: '0.13–0.16 of severity hue'
  license-chip:
    font: '{typography.mono-meta}'
    foreground: '{colors.text-muted}'
    border: '1px solid {colors.border}'
    radius: '{rounded.sm}'
  kev-tag:
    font: '{typography.mono-meta}'
    background: '{colors.severity-critical}'
    foreground: '{colors.background}'
    radius: '4px'
  triage-pill:
    radius: '{rounded.sm}'
    border: '1px solid, status hue at 0.3–0.4 alpha'
    background: 'transparent surface tint'
  dq-badge:
    font: '{typography.mono-meta}'
    foreground: '{colors.data-quality}'
  findings-table:
    row-height: '{spacing.data-row}'
    row-border: '{colors.hairline}'
    identifier-font: '{typography.mono-identifier}'
    header: '{typography.micro-label}'
  populating-banner:
    border: '{colors.warning} at 0.28 alpha'
    background: '{colors.warning} at 0.07 alpha'
    radius: '{rounded.md}'
  coverage-gap-row:
    border: '1px dashed {colors.warning} at 0.3 alpha'
    background: '{colors.warning} at 0.05 alpha'
  severity-band:
    height: 30px
    radius: '{rounded.DEFAULT}'
    segment-radius: '4px'
    fill-opacity: '0.6–0.85'
  node-inspector:
    background: '{colors.surface}'
    border-left: '{colors.border}'
    identifier: '{typography.mono-identifier}'
  graph-node:
    radius: '{rounded.node}'
    fill: '{colors.surface}'
    label: '{typography.mono-identifier}'
  graph-node-running:
    ring: '1.4px {colors.accent} at 0.55 alpha, 4px offset'
    pip: '{colors.accent}'
  graph-node-inactive:
    border: '1px dashed {colors.border}'
    opacity: '0.5–0.55'
  graph-edge-affected:
    stroke: 'severity hue, 0.3–0.55 alpha, 1.4–2px, soft bezier'
  button-primary:
    background: '{colors.accent}'
    foreground: '{colors.background}'
    radius: '{rounded.DEFAULT}'
    label: '{typography.body-dense}'
  freshness-strip:
    font: '{typography.mono-meta}'
    border-top: '{colors.border}'
  heading-block:
    eyebrow: '{typography.eyebrow}'
    title: '{typography.page-title}'
    rule: '46px × 2px {colors.accent}'
---

# Armoury — Design Spine

> Approved composition references: [mockups/hybrid-posture-v2.html](mockups/hybrid-posture-v2.html) (posture surface — typographic system, zone rhythm, dense table) and [mockups/blast-radius-graph-v1.html](mockups/blast-radius-graph-v1.html) (graph styling); further key screens in [mockups/](mockups/). Theme value maps: [.working/color-themes-1.html](.working/color-themes-1.html). This spine wins on conflict with any render.

## Brand & Style

Armoury is the workshop, not the alarm panel: warm graphite, steel, and ember light — craft over alarm. The surface is a **calm analytics canvas** — generous space between zones, dense and exact within them — interrupted only where the data earns emphasis. It is an instrument for someone working alone under pressure; nothing decorates, everything reports.

Dark only. There is no light mode and none is planned. Three dark themes ship day 1, user-selectable: **Forge** (default — the warm workshop), **High Signal** (high-contrast for long triage sessions; AAA-targeting text, fills kept pastel-soft so contrast never turns shrill), **Gunmetal** (near-black neutral — the quietest room in the building; the data is the only color that matters).

Two hard postures define the character:

1. **Asymmetric composition.** No uniform KPI-card grids, no centered cards, no template rhythm. One dominant hero numeral with co-stats in a hairline-divided band; strong left-aligned heading blocks with a short ember rule. The generic dashboard look is an explicit reject.
2. **Soft data.** Charts, bands, and graph edges are rounded and muted — severity fills at 0.6–0.85 opacity, no neon, no glow. Severity is heat, but the room stays cool.

shadcn/ui + Tailwind is the UI system. These tokens extend shadcn defaults via its CSS-variable layer; unlisted shadcn tokens inherit, restated only when a theme remaps them.

## Colors

All components reference **semantic roles**; the three themes are value maps over the same roles (see frontmatter). Forge values below; High Signal and Gunmetal substitute their suffixed equivalents.

- **{colors.background} / {colors.surface} / {colors.border} / {colors.hairline}** — the tonal stack. Surfaces separate by tone and 1px borders, not shadow. {colors.hairline} is for in-table row rules only.
- **{colors.accent} (ember amber, Forge)** — restrained, never decorative floods. Means exactly: *primary action, active nav, running-now emphasis* (graph ring/pip), and the heading rule. Never severity, never large fills.
- **Severity ramp** {colors.severity-critical} → {colors.severity-low} — fills always at reduced opacity (0.6–0.85 in bands/bars, 0.13–0.16 behind chip text). In graph views, severity hue appears **only on the CVE → affected path** — never on chrome, never on unaffected nodes.
- **{colors.data-quality}** — Forge: cool slate-teal; reads "instrument, not heat." The data-quality hue is **always hue-distinct from the severity ramp** in every theme (High Signal: soft lavender; Gunmetal: muted violet). DQ is a measurement, not a threat level, and must never be mistaken for one.
- **{colors.warning}** — owns honesty states: populating banners, coverage-gap rows, stale-feed flags, unscanned caveats. **{colors.success}** — fresh feeds, healthy agents, verified signatures.
- **{colors.text-data}** — table/data text, one step quieter than {colors.text-primary}; {colors.text-muted} for labels and secondary copy.

Contrast: Forge and Gunmetal hold WCAG AA for all text roles on their surfaces; High Signal targets AAA for {colors.text-primary-high-signal} (≈17:1 on surface) and ≥7:1 for muted text — it doubles as the product's high-contrast accessibility option.

## Typography

Three families, hard boundaries:

- **IBM Plex Mono** — *every* technical identifier, no exceptions: CVE IDs, `package@version`, digests, cluster/namespace/workload paths, feed names and versions, registry URLs. If it could be pasted into a terminal, it is mono. ({typography.mono-identifier}, {typography.mono-meta})
- **Inter Display** — display numerals and titles only, weights 200 and 500. The {typography.hero-numeral} (76px, weight 200, −0.035em, tabular-nums) is the loudest element on any surface and appears at most once per surface. {typography.co-stat} for the supporting band; {typography.page-title} / {typography.answer-headline} for headings.
- **Inter** — everything else. {typography.body} for prose, {typography.body-dense} for dense UI, {typography.micro-label} (10px, uppercase, +0.14em) for stat labels and table headers, {typography.eyebrow} (accent-colored, +0.16em) above page titles.

The scale is asymmetric by design — a deliberate jump from 76px numerals to 10px micro-labels with little middle ground. Numerals are always `tabular-nums`. No font size between 14px and 21px exists except {typography.page-title}; resist inventing intermediate sizes.

## Layout & Spacing

Rhythm rule: **generous between zones, dense within data zones.** Zones separate by {spacing.zone-gap} (48–56px) and a 1px {colors.border} rule with a {typography.micro-label}-style zone header. Inside a data zone, rows run at {spacing.data-row} (30px) with {colors.hairline} rules.

- App shell: slim left icon rail ({spacing.rail-width}, background {colors.rail-background} one step below surface) + single main column at {spacing.page-gutter} horizontal padding. No top nav bar.
- Heading blocks are strong and left-aligned: eyebrow → title → muted subtitle (max-width ~620px) → 46×2px ember rule. Never centered.
- Stat zone: one hero numeral, then co-stats divided by 1px {colors.border} hairlines at {spacing.stat-gap} padding — a band, not a card grid.
- Tables run full-width of the main column; designed for the NFR3 scale anchor (hundreds of repos, thousands of images, ≤10 clusters) — density and pagination over virtualized infinite walls.
- Tailwind's 4-based spacing scale inherits for everything inside components.

## Elevation & Depth

Tonal layering, not shadows. Depth = background → surface → raised tints ({colors.rail-hover} row hover, {colors.rail-active} active rail item). Borders do the separating; shadows appear only on true overlays (slide-over drawer, command palette, popovers) as soft, large-radius, low-alpha black — never colored glows. Nothing on the canvas floats.

## Shapes

Soft and rounded, never sharp, never pill containers: {rounded.sm} chips and tags, {rounded.DEFAULT} inputs and buttons, {rounded.md} rail items and banners, {rounded.lg} cards and canvases, {rounded.node} graph nodes. {rounded.full} only for status pips and dots. Severity band segments round at 4px — the "soft chart" signature. SVG graph edges are soft beziers, never straight elbows.

## Components

shadcn components inherited as-is unless listed: `Dialog`, `Sheet`, `Popover`, `DropdownMenu`, `Tabs`, `Command`, `Tooltip`, `Skeleton`, `Toast`. Brand-layer components (token detail in frontmatter `components`):

| Component | Visual spec |
|---|---|
| Icon rail | 58px, icon-only items 40×40 {rounded.md}; active = raised tint + 2px {colors.accent} left indicator; tooltip flyout right. Settings pinned bottom. |
| Hero stat | {typography.hero-numeral} + {typography.micro-label} label; co-stats in hairline band. Critical count may take {colors.severity-critical}; DQ grade takes {colors.data-quality}. |
| Severity chip | Uppercase micro label on 0.13–0.16-alpha severity tint, {rounded.sm}. |
| KEV tag | Mono, dark text on {colors.severity-critical} at 0.85 — the single highest-urgency mark in the system; nothing outranks it visually. |
| License chip | Neutral policy/license-type chip for license findings: {typography.mono-meta} text in {colors.text-muted}, 1px {colors.border}, {rounded.sm}. Never a severity hue — the severity ramp is CVE-only. |
| Triage pill | Outlined, status-hued text: fix planned = {colors.accent}, mitigated = {colors.success}, accepted = {colors.severity-medium}, not affected = {colors.text-muted}, untriaged = {colors.warning}. |
| DQ badge | Mono grade + 6px pip, always {colors.data-quality}. Dims (0.65 opacity) for lower grades — never turns red. |
| Findings table | 30px rows, 9.5–10px uppercase headers, identifiers in mono, hover = {colors.rail-hover}. Coverage-gap rows sit inline (see below). |
| Coverage-gap row | Full-width inline table row: dashed {colors.warning} rules, warning pip, bold warning lead-in. Gaps are first-class rows, not footnotes. |
| Populating banner | Warning-tinted {rounded.md} band with pip; sits under the heading block. |
| Severity band | 30px stacked distribution, 3px gaps, per-segment 4px radius, soft-opacity fills. |
| Graph node | {rounded.node} surface-filled rect, mono identifier + muted 9px meta line. Affected nodes carry severity-hued 0.35–0.45-alpha border. |
| Graph node — running | Outer {colors.accent} ring (1.4px, 0.55 alpha, 4px offset) + ember pip. Ring, never glow. |
| Graph node — not running | 0.5 opacity, dashed border, muted text ("shipped, not running"). |
| Graph edges | Soft beziers; severity hue at 0.3–0.55 alpha only on the affected path; artifact→workload edges in {colors.accent} (running) or dashed muted (not). |
| Node inspector | Side panel anchored right within Graph explorer: {colors.surface} background, 1px {colors.border} left rule, identifiers in {typography.mono-identifier}. |
| Primary button | {colors.accent} fill, {colors.background} text — at most one per surface (e.g. "Export evidence pack"). |
| Freshness strip | Mono micro-text row at page end: feed name bold, age in {colors.success}/{colors.warning}. |
| Theme switcher | Compact affordance: 9px swatch + theme name; full picker lives in Settings and command palette. |

## Do's and Don'ts

| Do | Don't |
|---|---|
| One hero numeral per surface; co-stats in a hairline band | Four identical KPI cards in a grid |
| Severity fills at 0.6–0.85 opacity, rounded | Neon, glows, saturated full-opacity heat |
| {colors.data-quality} for DQ everywhere, all themes | Reuse any severity hue for data quality |
| IBM Plex Mono for every identifier | Identifiers in Inter, or mono for prose |
| Severity hue only on the affected graph path | Coloring whole graphs by severity |
| Ember = action / active / running-now | Ember floods, ember severity, decorative ember |
| Surface coverage gaps as warning-tinted first-class rows | Hiding gaps in tooltips or footers |
| Tonal layering + 1px borders | Drop shadows on in-canvas cards |
| Strong left-aligned heading blocks with ember rule | Centered headings, centered empty states |
| Semantic tokens; themes only remap values | Components referencing theme-specific hexes |
