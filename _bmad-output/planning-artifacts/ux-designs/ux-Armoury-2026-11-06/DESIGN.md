---
name: Armoury
description: Self-hosted software supply-chain evidence layer for SME security teams and the engineering leaders they report to. Greenhouse visual system — calm light canvas by default, one calm dark theme, black sidebar, lime for the one action that matters, forest green for selection and charts. shadcn-svelte on SvelteKit + Tailwind; this DESIGN.md specifies the brand layer over shadcn defaults.
status: final
updated: 2026-11-06
supersedes: ux-Armoury-2026-06-12
colors:
  # Semantic tokens, mapped onto shadcn CSS variables (see "Colors → shadcn
  # mapping"). Two themes share the SAME roles, layout and density:
  #   Light (default) — unsuffixed keys
  #   Dark            — keys with the -dark suffix
  # Components reference roles only, never a theme-specific hex.
  # Values lifted from mockups/greenhouse-final.html (:root and the dark remap).
  # Presentation-only tokens in the mock (stage, stage-2, stage-text-2, chrome,
  # chrome-pill, chrome-line, dot-1/2/3, frame-edge) are NOT product tokens.
  #
  # —— Light (default) ——
  ink: '#0B0F0C'            # sidebar
  ink-2: '#171D19'          # sidebar raised: search field, nav hover, badge
  ink-line: '#252C27'       # sidebar dividers (decorative)
  side-text: '#C9D0CB'      # nav labels on ink
  side-muted: '#8C968F'     # secondary text on ink
  on-ink: '#FFFFFF'         # wordmark, user name on ink
  lime: '#C8F169'           # active nav item + the one primary action per view
  lime-hover: '#B8E35A'     # primary action hover
  lime-wash: '#F1FADF'      # all-clear sprout disc
  lime-ring: '#DCEFB4'      # all-clear halo rings (decorative)
  forest: '#1F3B33'         # selection fill, active tab / segment
  forest-2: '#2C5246'       # secondary chart strokes, graph edges
  forest-3: '#3B5C50'       # user avatar gradient start (ends at forest)
  forest-wash: '#E8EFEC'    # gauge / progress / coverage track
  forest-ink: '#1F3B33'     # green text: charts, links, progress fill, Low severity
  sage: '#A9BDB5'           # secondary text on forest
  sage-hi: '#DCE7E2'        # severity / chips on forest
  on-forest: '#FFFFFF'      # text on forest
  canvas: '#FFFFFF'         # detail column, tables, dialogs
  paper: '#F5F6F3'          # list column, inputs, bands
  chip: '#ECEEEA'           # chips, grey buttons, skeleton blocks
  chip-hover: '#E3E6E1'     # grey button hover / pressed edge
  row-hover: '#EEF0EB'      # list and table row hover
  rule: '#E6E8E3'           # 1px rules (decorative)
  text: '#121814'
  text-2: '#56615B'         # secondary text
  text-3: '#5F6963'         # tertiary: versions, counts in headings, hints
  clay: '#9A4A2E'           # Critical, "Actively exploited", error icon
  clay-wash: '#F8EDE7'      # exploited pill, error band
  clay-dot: '#C9765A'       # graph vulnerability-node ring (non-text, labelled)
  amber: '#855A14'          # High, stale-source text
  amber-dot: '#D2A24C'      # stale source dot (always with a word)
  slate: '#4A5E6B'          # Medium
  slate-dot: '#8FA39A'      # neutral dots, not-deployed dashes (always with a word)
  field-border: '#737D77'   # resting edge of fields and the "Why?" textarea (≥3:1, WCAG 1.4.11)
  focus: '#1F3B33'          # focus ring on canvas / paper
  scroll-thumb: '#848E88'   # thin scrollbars, pager button hover edge
  scrim: '#0B0F0C6B'        # rgba(11,15,12,.42) behind the ⌘K dialog
  sel-chip: '#FFFFFF17'     # rgba(255,255,255,.09) chip on forest selection
  sprout-ring: '#F1FADF99'  # rgba(241,250,223,.6)
  shadow-far: '#1218142E'   # rgba(18,24,20,.18)
  shadow-near: '#12181414'  # rgba(18,24,20,.08)
  #
  # —— Print (audit report PDF, printed exports) ——
  # Print never follows the app theme: each print-*-dark pair repeats the
  # light value so theme generators see a complete pair.
  print-page: '#FFFFFF'     # page
  print-text: '#1A1A1A'     # body text, 17.4:1 on page
  print-text-2: '#555555'   # secondary text, 7.5:1
  print-rule: '#D0D0D0'     # hairline rules (decorative)
  print-critical: '#9A4A2E' # Critical (= clay), 6.2:1, word always present
  print-high: '#855A14'     # High (= amber), 6.1:1, word always present
  print-medium: '#4A5E6B'   # Medium (= slate), 6.8:1, word always present
  print-low: '#1F3B33'      # Low (= forest-ink), 12.1:1, word always present
  #
  # —— Dark ——
  ink-dark: '#070A08'
  ink-2-dark: '#151C18'
  ink-line-dark: '#242D28'
  side-text-dark: '#C9D0CB'
  side-muted-dark: '#8C968F'
  on-ink-dark: '#EEF3EF'
  lime-dark: '#C8F169'
  lime-hover-dark: '#B8E35A'
  lime-wash-dark: '#1C2618'
  lime-ring-dark: '#2C3B21'
  forest-dark: '#285443'
  forest-2-dark: '#5E9C82'
  forest-3-dark: '#33604F'
  forest-wash-dark: '#1B2B24'
  forest-ink-dark: '#8CCBAB'
  sage-dark: '#B4D2C5'
  sage-hi-dark: '#DCE9E3'
  on-forest-dark: '#EEF3EF'
  canvas-dark: '#131A16'
  paper-dark: '#0F1512'
  chip-dark: '#1F2823'
  chip-hover-dark: '#29332D'
  row-hover-dark: '#151D19'
  rule-dark: '#27312B'
  text-dark: '#E2E8E4'
  text-2-dark: '#A8B3AC'
  text-3-dark: '#8E9A93'
  clay-dark: '#EBA387'
  clay-wash-dark: '#2C1E18'
  clay-dot-dark: '#D9876A'
  amber-dark: '#E2BC72'
  amber-dot-dark: '#D8AE5E'
  slate-dark: '#A9BCC8'
  slate-dot-dark: '#7F948B'
  field-border-dark: '#748079'
  focus-dark: '#C8F169'     # lime ring in dark
  scroll-thumb-dark: '#66736B'
  scrim-dark: '#0000009E'   # rgba(0,0,0,.62)
  sel-chip-dark: '#FFFFFF14'    # rgba(255,255,255,.08)
  sprout-ring-dark: '#1C261899' # rgba(28,38,24,.6)
  shadow-far-dark: '#0000008C'  # rgba(0,0,0,.55)
  shadow-near-dark: '#00000059' # rgba(0,0,0,.35)
  print-page-dark: '#FFFFFF'    # print never follows the theme
  print-text-dark: '#1A1A1A'
  print-text-2-dark: '#555555'
  print-rule-dark: '#D0D0D0'
  print-critical-dark: '#9A4A2E'
  print-high-dark: '#855A14'
  print-medium-dark: '#4A5E6B'
  print-low-dark: '#1F3B33'
typography:
  # IBM Plex Sans (variable 100–700) for everything; IBM Plex Sans Bold Italic
  # for the wordmark only; IBM Plex Mono 400 only for IDs, fingerprints,
  # commands and keys. All SIL OFL 1.1, self-hosted (no network at view time).
  # Nine sizes only: 12 · 13 · 14 · 15 · 17 · 20 · 24 · 30 · 40.
  # Single exception: the 22px wordmark (Bold Italic), nowhere else.
  # Weights: 400 body, 500 emphasis in data, 600 headings and labels.
  # Numerals: tabular-nums in every data role.
  wordmark:                 # Bold Italic; 22px is the one size outside the nine
    fontFamily: 'IBM Plex Sans'
    fontSize: 22px
    fontWeight: '700'
    lineHeight: '1'
    letterSpacing: -0.03em
  page-title:
    fontFamily: 'IBM Plex Sans'
    fontSize: 30px
    fontWeight: '600'
    lineHeight: '1.12'
    letterSpacing: -0.025em
  headline-number:
    fontFamily: 'IBM Plex Sans'
    fontSize: 30px
    fontWeight: '500'
    lineHeight: '1'
    letterSpacing: -0.025em
  group-heading:
    fontFamily: 'IBM Plex Sans'
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: -0.02em
  detail-title:
    fontFamily: 'IBM Plex Sans'
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: -0.02em
  answer:
    fontFamily: 'IBM Plex Sans'
    fontSize: 24px
    fontWeight: '400'
    lineHeight: '1.3'
    letterSpacing: -0.02em
  inspector-title:
    fontFamily: 'IBM Plex Sans'
    fontSize: 20px
    fontWeight: '600'
    lineHeight: '1.25'
    letterSpacing: -0.015em
  cell-heading:
    fontFamily: 'IBM Plex Sans'
    fontSize: 17px
    fontWeight: '600'
    lineHeight: '1.3'
    letterSpacing: -0.01em
  body:
    fontFamily: 'IBM Plex Sans'
    fontSize: 15px
    fontWeight: '400'
    lineHeight: '1.55'
  row-title:
    fontFamily: 'IBM Plex Sans'
    fontSize: 15px
    fontWeight: '600'
    lineHeight: '1.35'
    letterSpacing: -0.005em
  secondary:
    fontFamily: 'IBM Plex Sans'
    fontSize: 14px
    fontWeight: '400'
    lineHeight: '1.4'
  meta:
    fontFamily: 'IBM Plex Sans'
    fontSize: 13px
    fontWeight: '400'
    lineHeight: '1.45'
  severity-label:
    fontFamily: 'IBM Plex Sans'
    fontSize: 13px
    fontWeight: '600'
    lineHeight: '1'
  button-label:
    fontFamily: 'IBM Plex Sans'
    fontSize: 12px
    fontWeight: '600'
    letterSpacing: 0.07em
  mono-id:
    fontFamily: 'IBM Plex Mono'
    fontSize: 13px
    fontWeight: '400'
    letterSpacing: '0'
  mono-small:
    fontFamily: 'IBM Plex Mono'
    fontSize: 12px
    fontWeight: '400'
    lineHeight: '1.75'
  display-reserved:
    fontFamily: 'IBM Plex Sans'
    fontSize: 40px
    fontWeight: '500'
rounded:
  xs: 3px        # kind tag, KEV tag
  sm: 4px        # buttons, chips, fields, segments, key caps, sidebar search
  DEFAULT: 4px
  md: 6px        # segmented-control frame, palette rows
  lg: 10px       # ⌘K dialog
  pill: 999px    # "Actively exploited" pill, nav badge
  full: 9999px   # dots, radio rings, avatar, gauges
spacing:
  # Tailwind 4-based scale inherited inside components. Named layout tokens
  # from the mock's 1440px design canvas:
  sidebar-width: 252px
  list-width: 376px          # Home, Software, Exposure list
  list-width-issues: 500px   # Issues (filters + status chip column)
  list-width-reports: 420px
  list-gutter: 32px          # list column horizontal padding, row rule inset
  detail-cell-x: 34px
  detail-cell-y: 30px
  row-y: 17px                # Home / Software rows (≈78px two-line row)
  row-y-issues: 14px         # Issues rows (≈72px two-line row)
  row-y-summary: 12px        # summary and "N more" rows
  nav-item-height: 54px
  tab-height: 64px
  button-height: 42px
  button-height-sm: 32px
  button-height-wide: 54px
  field-height: 42px
  query-height: 44px
  pager-button: 32px
  table-cell-y: 12px
components:
  sidebar:
    background: '{colors.ink}'
    width: '{spacing.sidebar-width}'
    label: '{colors.side-text}'
    muted: '{colors.side-muted}'
    divider: '{colors.ink-line}'
  nav-item:
    height: '{spacing.nav-item-height}'
    font: '{typography.body}'
    hover-background: '{colors.ink-2}'
    active-background: '{colors.lime}'
    active-foreground: '{colors.ink}'
  nav-badge:
    background: '{colors.ink-2}'
    foreground: '{colors.lime}'
    radius: '{rounded.pill}'
  sidebar-search:
    background: '{colors.ink-2}'
    border: '1px inset {colors.ink-line}'
    foreground: '{colors.side-muted}'
    radius: '{rounded.sm}'
  list-column:
    background: '{colors.paper}'
    border-right: '{colors.rule}'
    width: '{spacing.list-width}'
  list-row:
    padding-y: '{spacing.row-y}'
    padding-x: '{spacing.list-gutter}'
    title: '{typography.row-title}'
    version: '{colors.text-3}'
    second-line: '{typography.secondary}'
    second-line-color: '{colors.text-2}'
    right-column: '{typography.meta}'
    rule: '1px {colors.rule}, inset {spacing.list-gutter}'
    hover-background: '{colors.row-hover}'
    selected-background: '{colors.forest}'
    selected-foreground: '{colors.on-forest}'
    selected-secondary: '{colors.sage}'
  group-heading:
    font: '{typography.group-heading}'
    count: '{colors.text-3}'
  severity-marker:
    critical: '{colors.clay}'
    high: '{colors.amber}'
    medium: '{colors.slate}'
    low: '{colors.forest-ink}'
    label: '{typography.severity-label}'
    bars: '4 bars, 4×11px, 2px gap, radius 1px; unlit bars at 0.22 (5×15px in group headings)'
  exploited-text:
    foreground: '{colors.clay}'
    on-selection-foreground: '{colors.sage-hi}'
    icon: 'pulse, 13px'
    font: '{typography.meta}, weight 500'
  exploited-pill:
    background: '{colors.clay-wash}'
    foreground: '{colors.clay}'
    radius: '{rounded.pill}'
    icon: 'pulse, 14px'
    font: '{typography.severity-label}'
  kev-tag:
    font: '{typography.mono-small}'
    background: '{colors.chip}'
    foreground: '{colors.text-2}'
    radius: '{rounded.xs}'
  licence-marker:
    foreground: '{colors.text-2}'
    on-selection-foreground: '{colors.sage-hi}'
    icon: 'scale'
  kind-tag:
    background: '{colors.chip}'
    foreground: '{colors.text-2}'
    on-selection-background: '{colors.sel-chip}'
    on-selection-foreground: '{colors.sage-hi}'
    radius: '{rounded.xs}'
  status-chip:
    background: '{colors.chip}'
    foreground: '{colors.text-2}'
    radius: '{rounded.sm}'
    icon: '12px drawn icon per status'
    mixed-icon: 'layers (two offset outlines), 12px'
    on-selection-background: '{colors.sel-chip}'
    on-selection-foreground: '{colors.sage-hi}'
  segmented-control:
    frame: '1px {colors.rule}, 3px inset, {rounded.md}'
    background: '{colors.canvas}'
    segment-radius: '{rounded.sm}'
    active-background: '{colors.forest}'
    active-foreground: '{colors.on-forest}'
  tabs:
    height: '{spacing.tab-height}'
    rule: '1px {colors.rule} bottom'
    active-background: '{colors.forest}'
    active-foreground: '{colors.on-forest}'
    count: '{colors.text-3}'
  detail-column:
    background: '{colors.canvas}'
    cell-padding: '{spacing.detail-cell-y} {spacing.detail-cell-x}'
    cell-rule: '{colors.rule}'
  review-option:
    border: '1px {colors.rule}'
    checked-border: '1.5px {colors.forest-ink}'
    radio-ring: '{colors.text-3}'
    radio-checked: '{colors.forest-ink}'
    radius: '{rounded.sm}'
  review-note-field:
    background: '{colors.paper}'
    border: '1px {colors.field-border}'
    hover-border: '1px {colors.text-3}'
    focus-border: '1.5px {colors.focus}'
    radius: '{rounded.sm}'
  inline-error:
    background: '{colors.clay-wash}'
    icon: '{colors.clay}'
    foreground: '{colors.text}'
    secondary: '{colors.text-2}'
    font: '{typography.secondary}'
    radius: '{rounded.sm}'
    action-height: '{spacing.button-height-sm}'
  technical-details:
    font: '{typography.mono-small}'
    foreground: '{colors.text-2}'
    rule: '{colors.rule}'
  button:
    height: '{spacing.button-height}'
    label: '{typography.button-label}'
    case: uppercase
    background: '{colors.chip}'
    hover-background: '{colors.chip-hover}'
    foreground: '{colors.text}'
    radius: '{rounded.sm}'
  button-primary:
    background: '{colors.lime}'
    hover-background: '{colors.lime-hover}'
    foreground: '{colors.ink}'
    radius: '{rounded.sm}'
  field:
    min-height: '{spacing.field-height}'
    background: '{colors.canvas}'
    border: '1px {colors.field-border}'
    hover-border: '1px {colors.text-3}'
    focus-border: '1.5px {colors.focus}'
    radius: '{rounded.sm}'
  code-block:
    background: '{colors.paper}'
    border: '1px {colors.rule}'
    font: '{typography.mono-small}'
    foreground: '{colors.text-2}'
    radius: '{rounded.sm}'
    copy-button-height: '{spacing.button-height-sm}'
  signature-status:
    verified-disc: '{colors.forest-wash}'
    verified-icon: '{colors.forest-ink}'
    title: '{typography.body}'
    detail: '{typography.meta}'
    detail-color: '{colors.text-2}'
    failed-band: '{colors.clay-wash}'
    failed-icon: '{colors.clay}'
  user-menu:
    avatar-start: '{colors.forest-3}'
    avatar-end: '{colors.forest}'
    avatar-initials: '{colors.on-forest}'
    avatar-radius: '{rounded.full}'
    name: '{colors.on-ink}'
    role: '{colors.side-muted}'
    menu-background: '{colors.canvas}'
  kbd:
    font: '{typography.mono-small}'
    foreground: '{colors.text-2}'
    background: '{colors.canvas}'
    border: '1px {colors.rule}'
    radius: '{rounded.sm}'
  pager:
    rule: '1px {colors.rule} top'
    button: '{spacing.pager-button} square, {colors.canvas}, 1px {colors.rule}, {rounded.sm}'
  coverage-gap-row:
    title: '{typography.row-title}'
    count: '{colors.text-3}'
    body: '{typography.secondary}'
    body-color: '{colors.text-2}'
  freshness-strip:
    background: '{colors.paper}'
    rule: '1px {colors.rule} top'
    font: '{typography.meta}'
    foreground: '{colors.text-2}'
    stale: '{colors.amber} text + {colors.amber-dot} dot'
  checking-band:
    background: '{colors.paper}'
    track: '{colors.forest-wash}'
    fill: '{colors.forest-ink}'
  error-band:
    background: '{colors.clay-wash}'
    icon: '{colors.clay}'
    title: '{colors.text}'
    body: '{colors.text-2}'
  exposure-graph:
    tier-label: '{typography.meta}, weight 500, {colors.text-3}'
    edge: '1.2px {colors.forest-2}'
    edge-not-deployed: '1.2px dashed 3 4 {colors.slate-dot}'
    edge-selected: '2.4px {colors.forest-ink}'
    node: 'circle, {colors.canvas} fill, 1.5px {colors.forest-ink} or {colors.forest-2} ring'
    node-vulnerability: '{colors.clay-wash} fill, 1.5px {colors.clay-dot} ring, pulse icon in {colors.clay} when actively exploited'
    rule: '1px {colors.rule}; dashed rule above the Not deployed band'
  inspector:
    title: '{typography.inspector-title}'
    background: '{colors.canvas}'
    rule: '1px {colors.rule} top'
  table:
    header: '{typography.meta}, weight 500, {colors.text-2} on {colors.paper}'
    cell-padding-y: '{spacing.table-cell-y}'
    rule: '{colors.rule}'
    hover-background: '{colors.row-hover}'
    selected-background: '{colors.forest}'
    selected-foreground: '{colors.on-forest}'
    selected-secondary: '{colors.sage}'
    selected-chip-background: '{colors.sel-chip}'
    selected-chip-foreground: '{colors.sage-hi}'
  command-palette:
    width: 660px
    background: '{colors.canvas}'
    radius: '{rounded.lg}'
    scrim: '{colors.scrim}'
    shadow: '0 30px 70px -20px {colors.shadow-far}, 0 4px 12px {colors.shadow-near}'
    active-row-background: '{colors.forest}'
    active-row-foreground: '{colors.on-forest}'
    footer-background: '{colors.paper}'
  all-clear:
    disc: '{colors.lime-wash}'
    disc-ring: '{colors.sprout-ring}'
    halo: '{colors.lime-ring}'
    icon: '{colors.forest-ink}'
  focus-ring:
    default: '2px {colors.focus}, 2px offset'
    on-ink-or-forest: '2px {colors.lime}'
---

# Armoury — Design Spine

> Approved composition reference: [mockups/greenhouse-final.html](mockups/greenhouse-final.html) (Light / Dark switch top right; screens: Home, Issues, Software, Exposure graph, Exposure table, Reports, ⌘K palette, Checking, Registry unreachable, All clear, Palette and type). Inspiration: [imports/inspo-shost-server-dashboard.png](imports/inspo-shost-server-dashboard.png). Decision log: [.memlog.md](.memlog.md). **This spine wins on conflict with any mock.** Supersedes `ux-Armoury-2026-06-12`.

## Brand & Style

Armoury is a calm room for stressful work. Security is stressful; the product should not add to it. The surface is **calm, approachable and serene**: a light canvas, a black sidebar, plain words, generous white space, thin rules and a few quiet charts. Calm must not mean bland: the lime accent, the forest selection, the hairline Exposure map, gauges and sparklines keep it alive. The visuals serve the task and never replace tables, filters or lists.

Two audiences, equal weight: security engineers who need precision and speed, and non-technical leaders who need to know "are we safe, and what needs attention" in a minute. One layout and one density serve both. Plain words come first; the technical term is kept, small and grey, so the engineer loses nothing.

Inspiration is the s.host server dashboard ([imports/inspo-shost-server-dashboard.png](imports/inspo-shost-server-dashboard.png)), adopted as a whole: light main canvas with a black sidebar; one lime accent for the primary action and the active nav item; deep green for selection and charts; three-column master-detail (nav · grouped list with counts · tabbed detail); calm, sparse cells with few numbers, large plain labels and simple sparklines; uppercase button labels.

**Why the three dark themes went.** The prior spine shipped three dark themes — Forge (warm graphite, ember), High Signal (high contrast) and Gunmetal (near-black) — and planned no light mode. Users found that UI intimidating, dense and exhausting, and the visual style wrong for half the audience. The new north star is approachable first, so the default is a light canvas. Dark stays as **one** calm second theme with the same semantic roles, layout and density, instead of three dark value maps to maintain and test.

shadcn-svelte + Tailwind (SvelteKit) remains the UI system. These tokens map onto shadcn CSS variables; unlisted shadcn tokens inherit.

## Colors

Every component references a **role**; Light and Dark are value maps over the same roles (frontmatter, `-dark` suffix). Light values are quoted below.

### Shell

- **{colors.ink}** — the sidebar, darkest surface in both themes. {colors.ink-2} raises the sidebar search field, nav hover and badge; {colors.ink-line} divides. Text on ink: {colors.side-text} (labels), {colors.side-muted} (secondary), {colors.on-ink} (wordmark, user name).
- **{colors.canvas} / {colors.paper} / {colors.chip} / {colors.rule}** — the light stack. Canvas holds the detail column, tables and dialogs; paper holds the list column, inputs, bands and strips; chip holds chips, grey buttons and skeleton blocks; rule is every 1px line (decorative). {colors.row-hover} is the hover tint for rows.
- **{colors.text} / {colors.text-2} / {colors.text-3}** — primary, secondary, tertiary text. text-3 marks versions, counts beside headings and hints; it was darkened to pass on chip.

### Accent and selection

- **{colors.lime}** — two main jobs: the **active nav item** and the **single primary action per view**. Agreed exceptions: the **selected graph node** and its "Selected on the map" marker, the **Issues nav badge** count, and **text selection**. Ink text on lime (14.9:1). Never a chip, never a list marker, never text on the light canvas (1.3:1). Hover {colors.lime-hover}. Tints {colors.lime-wash} and {colors.lime-ring} appear only in the all-clear illustration.
- **{colors.forest}** — selection: the selected list row, table row and palette result; the active tab; the active segment. Text on it is {colors.on-forest}, secondary {colors.sage}, chips and severity {colors.sage-hi}. In dark the forest fill is only 2.1:1 against canvas, so selection never relies on the fill alone: the text colour changes with it.
- **{colors.forest-ink}** — green as text and line: charts, sparklines, progress and coverage fill, links ("See all 14 on the map"), checked radio dots, and the Low severity colour. {colors.forest-2} draws secondary chart strokes and graph edges; {colors.forest-wash} is the track under gauges and progress.

### Risk

Three axes, never mixed: severity (how bad), actively exploited (yes/no), review status (the team's decision).

- **Severity** is always a **word plus a 4-step level marker**, in text colour only: Critical {colors.clay}, High {colors.amber}, Medium {colors.slate}, Low {colors.forest-ink}. No fills, and **no red anywhere**.
- **Actively exploited** (KEV) uses {colors.clay}: quiet clay text with a pulse icon in list rows; a {colors.clay-wash} pill in detail panels and the Exposure answer. {colors.clay-dot} rings the vulnerability node on the map.
- **Licences** have no severity: neutral {colors.text-2} with a scale icon.
- **Review status** chips are neutral ({colors.chip} / {colors.text-2}) with a drawn icon. Status never carries a colour, including the **Mixed** chip shown when places differ.
- **Honesty states**: stale sources use {colors.amber} text with the age in words and an {colors.amber-dot}; errors use a {colors.clay-wash} band with a {colors.clay} icon. {colors.slate-dot} marks neutral dots and not-deployed dashes.

### Interaction

- **{colors.focus}** — 2px focus ring, 2px offset: forest on light, lime on dark. On ink (sidebar) and on forest (selection) the ring is always lime.
- **Text selection** (`::selection`) is lime with ink text (an agreed lime exception).
- **{colors.field-border}** — the resting edge of every field and the "Why?" textarea, at ≥3:1 against the field fill and the surface around it (WCAG 1.4.11), so an empty required field is visible at rest. Hover darkens the edge to {colors.text-3}; focus is the 1.5px {colors.focus} edge plus the ring.
- {colors.scroll-thumb} for thin scrollbars and the pager button hover edge; {colors.scrim} behind the ⌘K dialog.

### shadcn mapping

| shadcn variable | Armoury role |
|---|---|
| `--background`, `--card`, `--popover` | {colors.canvas} |
| `--foreground`, `--card-foreground`, `--popover-foreground` | {colors.text} |
| `--primary` / `--primary-foreground` | {colors.lime} / {colors.ink} |
| `--secondary` / `--secondary-foreground` | {colors.chip} / {colors.text} |
| `--muted` / `--muted-foreground` | {colors.chip} / {colors.text-2} |
| `--accent` / `--accent-foreground` | {colors.row-hover} / {colors.text} |
| `--destructive` | {colors.clay} |
| `--border` | {colors.rule} |
| `--input` | {colors.field-border} |
| `--ring` | {colors.focus} |
| `--chart-1` … `--chart-3` | {colors.forest-ink}, {colors.forest-2}, {colors.slate-dot} |
| `--sidebar` / `--sidebar-foreground` | {colors.ink} / {colors.side-text} |
| `--sidebar-primary` / `--sidebar-primary-foreground` | {colors.lime} / {colors.ink} |
| `--sidebar-accent` / `--sidebar-border` / `--sidebar-ring` | {colors.ink-2} / {colors.ink-line} / {colors.lime} |

Dark sets the same variables from the `-dark` tokens. Paper ({colors.paper}) has no shadcn equivalent; add it as `--paper`. The `print-*` tokens are not shadcn variables; they feed the Typst template only (see Printed report).

### Contrast (WCAG 2.x)

Computed from the token hexes (the mock's stylesheet comments agree to ±0.2 except where noted). Floor: 4.5:1 for all text. Lowest text pair in either theme: **4.9:1** (text-3 on chip, light).

| Text pair | Light | Dark |
|---|---|---|
| text on canvas / paper / chip / row-hover | 18.0 / 16.6 / 15.4 / 15.7 | 14.2 / 14.9 / 12.2 / 13.8 |
| text-2 on canvas / paper / chip / row-hover | 6.4 / 5.9 / 5.5 / 5.6 | 8.2 / 8.5 / 7.0 / 7.9 |
| text-3 on canvas / paper / chip / row-hover | 5.7 / 5.3 / 4.9 / 5.0 | 6.1 / 6.3 / 5.2 / 5.9 |
| clay (Critical, exploited) on canvas / paper / row-hover | 6.2 / 5.7 / 5.4 | 8.5 / 8.9 / 8.3 |
| clay on clay-wash (exploited pill) | 5.4 | 7.7 |
| text / text-2 on clay-wash (error band, inline error, signature failed) | 15.7 / 5.6 | 12.9 / 7.4 |
| text-2 on paper (code block) | 5.9 | 8.5 |
| amber (High, stale) on canvas / paper / row-hover | 6.1 / 5.6 / 5.3 | 9.8 / 10.3 / 9.6 |
| slate (Medium) on canvas / paper / row-hover | 6.8 / 6.2 / 5.9 | 9.0 / 9.4 / 8.8 |
| forest-ink (Low, links, charts) on canvas / paper / forest-wash | 12.1 / 11.2 / 10.4 | 9.5 / 9.9 / 7.9 |
| on-forest on forest (selection) | 12.1 | 7.7 |
| sage on forest (secondary on selection) | 6.1 | 5.3 |
| sage-hi on forest / on sel-chip | 9.6 / 7.2 | 6.9 / 5.6 |
| On selection (forest fill): exploited text, licence marker, severity in sage-hi; kind tag and status chip (incl. Mixed) sage-hi on sel-chip; table secondary cells in sage | 9.6 / 7.2 / 6.1 | 6.9 / 5.6 / 5.3 |
| ink on lime / lime-hover (primary action, active nav) | 14.9 / 13.0 | 15.4 / 13.4 |
| side-text on ink / ink-2 | 12.3 / 10.9 | 12.7 / 11.0 |
| side-muted on ink / ink-2 | 6.3 / 5.6 | 6.5 / 5.7 |
| on-ink on ink | 19.3 | 17.7 |
| lime on ink-2 (nav badge) | 13.2 | 13.4 |
| text / text-2 on lime-wash (all clear) | 16.7 / 6.0 | 12.6 / 7.2 |

Non-text: focus ring 12.1 / 11.2:1 (light, canvas / paper), 13.7 / 14.3:1 (dark); lime ring on forest 9.4 / 6.7:1; scroll thumb on paper 3.1 / 3.7:1; **field border** on canvas / paper / chip 4.3 / 3.9 / 3.7:1 (light) and 4.3 / 4.5 / 3.7:1 (dark). Without selection colours, clay on forest would be 2.0:1 (light) and text-2 on forest 1.9:1, which is why every foreground on a selected row or table row switches as listed above. The mock comment gives side-text on ink as 12.9:1 (light); computed is 12.3:1. Markers below 3:1 — {colors.amber-dot} (2.1–2.3:1 light), {colors.slate-dot} (2.5–2.7:1 light) and the dark forest selection fill (2.1:1) — **never carry meaning alone**: each sits beside a word ("As of 14:02", "Not deployed") or a text-colour change.

## Typography

**IBM Plex Sans** for everything; **IBM Plex Sans Bold Italic** only for the wordmark ({typography.wordmark}); **IBM Plex Mono** only for IDs, fingerprints, commands and keys ({typography.mono-id}, {typography.mono-small}). All three are SIL OFL 1.1 and self-hosted, so air-gapped installs render the same face (no network at view time). Glyphs outside Latin (⌘ ↵ ↑ ↓) fall back to the system stack.

Nine sizes, no others. The **single exception** is the 22px wordmark ({typography.wordmark}, Bold Italic), used only in the sidebar head:

| px | Role |
|---|---|
| 40 | Reserved (gauge at large sizes); not used in product UI |
| 30 | Page title {typography.page-title}; headline numbers {typography.headline-number} |
| 24 | List group headings {typography.group-heading}; detail titles {typography.detail-title}; the Exposure answer {typography.answer} |
| 20 | Inspector titles {typography.inspector-title}; small-number stats |
| 17 | Cell headings {typography.cell-heading}; palette input |
| 15 | Body {typography.body}, row titles {typography.row-title}, definition lists, nav items |
| 14 | Secondary lines {typography.secondary}, fields, tables |
| 13 | Meta, chips, hints, captions {typography.meta}; severity and exploited labels {typography.severity-label}; mono IDs |
| 12 | Key caps, technical-details block, uppercase button labels {typography.button-label}, KEV tag |

Weights: 400 body, 500 emphasis in data, 600 headings and labels. Numerals are `tabular-nums` in every data role. Sentence case everywhere, including table headers and graph tiers; uppercase only on button labels, the Graph/Table switch and zoom labels. No eyebrows, kickers or tracked-caps labels above headings. Versions sit beside names in {colors.text-3} at weight 400 ("log4j-core 2.17.0").

## Layout & Spacing

**Three-column master-detail** on a 1440px design canvas:

1. **Sidebar** ({spacing.sidebar-width}, {colors.ink}) — wordmark, "Search or jump to… ⌘K" field, nav (Home · Software · Issues · Exposure · Reports, a divider, Settings · Help), user at the bottom.
2. **List column** ({colors.paper}, {spacing.list-width}; {spacing.list-width-issues} on Issues for the filters and status column; {spacing.list-width-reports} on Reports) — page title, summary line, filters, grouped list, pager, then the view's one primary action.
3. **Detail column** ({colors.canvas}, the rest) — tab bar ({spacing.tab-height}), then a grid of cells separated by 1px rules, never cards.

Exposure is the exception: a full-width header (title, query, Graph/Table switch, actions, answer) spans columns 2–3; below it, the list column and the map with its inspector.

**Narrower viewports** (behaviour in `EXPERIENCE.md` → Responsive & Platform): below 1280px the sidebar becomes an **icon rail** — the same 20px nav icons on {colors.ink}, active item lime, labels moved to tooltips and accessible names, the search field reduced to a ⌘K icon button and the user to the avatar alone. Below 1024px the list and detail columns **stack in one column**: the list fills the width, and opening an item shows its detail with a **Back** link at the top in {colors.forest-ink}. No other breakpoints.

Rhythm: list gutters {spacing.list-gutter}; detail cells {spacing.detail-cell-y} × {spacing.detail-cell-x}; rows {spacing.row-y} vertical padding (≈78px two-line row), {spacing.row-y-issues} on Issues (≈72px), {spacing.row-y-summary} for summary and "N more" rows. **One density only** — there is no Compact mode. Tailwind's 4-based scale applies inside components.

## Elevation & Depth

Flat and tonal. Separation comes from tone (ink → paper → canvas → chip) and 1px {colors.rule} lines, never from shadows on in-page elements and never from nested cards. Selection is a forest fill, hover a {colors.row-hover} tint. The only shadow in the product is the ⌘K dialog: {colors.scrim} behind it, and `0 30px 70px -20px {colors.shadow-far}, 0 4px 12px {colors.shadow-near}` on the dialog. Banners (Checking, error) run edge to edge of the content column, not as floating cards.

## Shapes

Small, quiet radii: {rounded.xs} for the kind and KEV tags; {rounded.sm} for buttons, chips, fields, segments, key caps and the sidebar search; {rounded.md} for the segmented-control frame and palette rows; {rounded.lg} for the ⌘K dialog. {rounded.pill} only for the "Actively exploited" pill and the nav badge; {rounded.full} for dots, radio rings, the avatar and gauges. Level-marker bars round at 1px. Graph nodes are circles; graph edges are soft beziers.

## Components

shadcn-svelte components used with Armoury tokens: `Button`, `Tabs`, `ToggleGroup` (segmented control), `Select` / `DropdownMenu` (review-status filter), `RadioGroup` (review questions), `Textarea`, `Command` + `Dialog` (⌘K), `Tooltip`, `Skeleton`, `Table`, `Pagination`, `Sidebar`. Brand-layer specifics:

| Component | Visual spec |
|---|---|
| Sidebar & nav | {components.sidebar}. Nav items {spacing.nav-item-height} tall, 20px icon + label. Active item: {colors.lime} fill, {colors.ink} text, weight 600 — the only lime in the sidebar besides the badge count. Hover {colors.ink-2}. Issues carries a {components.nav-badge} with the Needs-attention count; no badge at 0. The search field heads the nav with a `⌘K` key cap. Below 1280px it collapses to the icon rail (Layout & Spacing). |
| User menu | {components.user-menu}: at the foot of the sidebar, a 40px round avatar (gradient {colors.forest-3} → {colors.forest}, initials in {colors.on-forest}, 7.4:1 light / 6.4:1 dark; the mock's lime initials are not carried, lime keeps its agreed jobs), name in {colors.on-ink} 15px 500, role in {colors.side-muted} 13px, chevron in {colors.side-muted}. Opens a shadcn `DropdownMenu` on {colors.canvas}: the name and role, Personal settings, Sign out. On the icon rail only the avatar shows. |
| Page title + summary | {typography.page-title} equal to the sidebar label, then one {typography.body} summary line in {colors.text-2} with key numbers in {colors.text} 600 ("3 need attention today. 312 not reviewed yet."). Home adds "Last checked 38 min ago" in {typography.meta}. |
| List row | **One shape in every list.** Line 1: name + version ({typography.row-title}, version in {colors.text-3}). Line 2: severity · actively exploited · where ({typography.secondary}, `·` separators in {colors.text-3}). Right: **one** column — the thing this list is about (places, issues, copies or review status) in {typography.meta}. Rules inset by {spacing.list-gutter}; hover {colors.row-hover}; selected {colors.forest} fill with {colors.on-forest} title and {colors.sage} secondary, rules hidden around it. Licence rows carry a small {components.kind-tag} "Licence". |
| Group heading | {typography.group-heading} with the count beside it in {colors.text-3} weight 400 ("Critical 2"). Severity groups lead with the level marker at 5×15px; the Licences group with the scale icon. |
| "N more" / summary rows | {spacing.row-y-summary} padding, 14px weight 500 in {colors.text-2}, chevron ("38 more High", "Show all 169 Low"). |
| Severity | Word + {components.severity-marker} (4 bars, filled by level: Critical 4, High 3, Medium 2, Low 1). Colour per level; on selection {colors.sage-hi}. |
| Actively exploited marker — text | {components.exploited-text}: clay text, pulse icon, no fill; {colors.sage-hi} on a selected row. Used in **list rows** (Home, Issues, a software's Issues tab) and palette results. |
| Actively exploited marker — pill | {components.exploited-pill}: clay on clay-wash, pill radius, pulse icon. Used in **detail panels and the Exposure answer** only. |
| KEV tag | {components.kev-tag}: mono 12px grey "KEV" beside the pill, in detail views and the technical-details block only. |
| Status chip | {components.status-chip} with a drawn icon: Not reviewed yet (open circle), Not impacted (tick), Fix planned (arrow), Mitigated (half-filled circle), Risk accepted (flag). **Mixed** (layers icon) when the places an issue affects have different statuses, with the count of places that differ from the issue-wide status ("Mixed · 3 of 14"). Neutral grey in every status, Mixed included; text always present. On a selected row: {colors.sel-chip} fill, {colors.sage-hi} text. |
| Licence marker and kind tag | {components.licence-marker}: scale icon + word in {colors.text-2}. {components.kind-tag}: "Licence" on {colors.chip}. On a selected row both switch to {colors.sage-hi} (the kind tag on {colors.sel-chip}). |
| Segmented control | {components.segmented-control}: one style everywhere (Issues type filter, Exposure card All/Deployed/Not deployed, Graph/Table, theme). 3px inset frame, forest pill for the active segment, label colour changes too. Graph/Table labels are uppercase {typography.button-label}. |
| Tabs | {components.tabs}: 64px, 26px side padding, counts in {colors.text-3}; active tab is a forest block. The right end of the bar carries position and keys ("1 of 3 · J K") or context ("Generated today, 08:31, by …"). |
| Detail cells | Grid of {spacing.detail-cell-y}/{spacing.detail-cell-x} cells divided by rules. {typography.detail-title} for the subject, {typography.body} lead in {colors.text-2} (max 58ch), tags row, then a definition list (128px term column, terms {colors.text-2}). Cell headings {typography.cell-heading} with meta or a segmented control on the same baseline. Home adds a {colors.paper} band "Across all software" for fleet readings, separate from the selected issue. |
| Review panel | In the Issues detail column (Review tab). Two fieldsets with {typography.row-title}-weight legends; options are {components.review-option} rows: 18px radio ring, bold option, {typography.meta} hint, and the resulting status chip at the right. The second question indents under "Yes" with a 1px rule. "Why?" {components.review-note-field} (min 66px). Above the questions, a **scope** {components.segmented-control}: "All 14 places" (default) · "Only this software"; choosing the second reveals a shadcn `Select` of the places, in {components.field} style. Actions: lime "Save and next ⌘↵" (disabled at 0.45 until a question is answered), grey "Decide later", hint "Saved with your name in the audit trail." in {colors.text-3}. A failed save shows the {components.inline-error} line directly above the actions. Ends with the {components.technical-details} block. |
| Inline error | {components.inline-error}: one line in the panel where the action was taken (review panel, Export or Generate row, Settings panel), full width of that panel: {colors.clay-wash} fill, {rounded.sm}, 10px × 14px padding, 16px {colors.clay} alert icon, {typography.secondary} message in {colors.text} naming the problem ("Your decision wasn't saved: Armoury can't reach its database."), optional detail in {colors.text-2}, and a grey small **Try again** button ({spacing.button-height-sm}) at the right. No border, no shadow, no red. |
| Technical details | Mono 12px, line-height 1.75, {colors.text-2}, under a rule with a sans 13px 600 heading. Holds CVE, KEV, CVSS, EPSS, source and check time. |
| Buttons | {components.button}: {spacing.button-height}, uppercase 12px 600 +0.07em labels, {rounded.sm}, grey {colors.chip} with a 1px bottom edge; pressed edge flips to top. Small {spacing.button-height-sm}; wide {spacing.button-height-wide} at 13px for the list column's primary action; icon-only {spacing.button-height} square. **Primary** {components.button-primary}: lime fill, ink text — one per view. Disabled: 0.45 opacity, `not-allowed` cursor. |
| Fields | {components.field}: canvas, 1px {colors.field-border} edge (≥3:1), hover {colors.text-3} edge, focus 1.5px focus colour. The "Why?" textarea ({components.review-note-field}) uses the same edges on paper. Filter fields show label + bold value + count ("Review status: **Not reviewed yet** 312"). Search fields show a `/` key cap. |
| Pager | {components.pager}: "1–25 of 312 · page 1 of 13" in {typography.meta} with bold numbers; previous/next 32px square buttons; disabled at 0.45. |
| Coverage-gap row | {components.coverage-gap-row}: sits in the list where the missing rows would be. Title "Not checked yet" + count in {colors.text-3}; one {typography.secondary} sentence ("Counted above, but we haven't looked inside them yet, including 212 in prod-eu-west. Their issues are unknown, not absent."). No tint, no dashes, not dismissible. |
| Exposure header | With no query (opened from the sidebar), the answer slot holds a prompt in {typography.answer} and three example queries in {typography.mono-id}; with an ID Armoury has no data for, it holds that sentence in {typography.answer}, the data age in {typography.meta} and a lime Check again — no map, no zero. Otherwise: page title + summary question; the query as a {spacing.query-height} paper button showing the subject ("log4j-core 2.17.0 · Vulnerability CVE-2026-23012", ⌘K cap); Graph/Table switch; grey Export and "Audit report for this answer". Answer in {typography.answer} with bold numbers, a meta line (exploited pill, KEV tag, severity, CVSS, "Answered 38 min ago"), and a right-hand split of deployed/not-deployed copy bars. |
| Exposure graph | {components.exposure-graph}. Hairline, left to right, **four tiers** labelled in sentence case: Vulnerability · Package · Software · Where it runs (with counts). **Deployed edges solid** {colors.forest-2}; **not-deployed edges dashed** {colors.slate-dot}; the selected path heavier {colors.forest-ink}. Not-deployed software sits below a dashed rule labelled "Not deployed". Only the vulnerability node takes clay (pulse icon when actively exploited). Roll-ups as text nodes ("8 more", "5 more places"); edge labels ("direct · in 12", "bundles it · in 2"). Legend and zoom (+ / − / Fit) in a footer; a caveat line under it ("2 pieces of software haven't been checked yet and aren't on the map…"). |
| Inspector | Under the map, two cells: identity (title {typography.inspector-title} with version and "Selected on the map" marker; Name, Fingerprint in mono, Runs in, Copies, How it got it) and "What to do" (The fix, Review status chip, actions). Ends with "How we know: Syft v… · Grype DB v… · checked 38 min ago" in {colors.text-3}. |
| Table | {components.table}: sentence-case sortable headers with a sort arrow, 14px cells, numbers right-aligned; selected row forest with {colors.on-forest} text, secondary (muted) cells in {colors.sage}, chips {colors.sage-hi} on {colors.sel-chip}, severity {colors.sage-hi}. Exposure table columns: Software, Version, Deployed? (Yes/No), Where it runs, Copies, Severity, Review. |
| ⌘K palette | {components.command-palette}: 660px dialog, input row at 17px with search icon and `esc` cap; results grouped (Issues · Software · Exposure · Actions) under 13px 600 headings with counts; rows 15px with matched text underlined; active row forest; footer on paper with ↑ ↓ move · ↵ open · esc close and "Also finds CVE IDs, package@version and fingerprints". |
| Freshness strip | {components.freshness-strip}: one row on paper under a rule at the bottom of the detail column. Each source and its age ("Vulnerability data 41 min ago · Exploited list KEV 6 Nov · Packages 38 min ago · 2 clusters reporting"), technical term small in {colors.text-3}; a stale source turns {colors.amber} with its age in words and an amber dot. "Sources" link at the end in {colors.forest-ink}. |
| Checking band | {components.checking-band}: edge-to-edge paper band, title "Checking 671 more pieces of software…" with an estimate ("about 2 h left"), an 8px determinate bar (forest-ink on forest-wash), and one line of what it means. Rows below show per-item step text; {colors.chip} skeleton blocks only where data is missing. |
| Error band | {components.error-band}: edge-to-edge clay-wash band, clay icon, 15px 600 title naming the failure ("We can't reach registry.acme.internal"), 14px body (since when, what it affects, what still works, likely cause), then actions. While the band shows, its recovery action (Try again) is the view's one lime button and the list column's primary action (for example Add software) turns grey. Stale rows say "As of 14:02" in amber with a clock icon. |
| Gauges & charts | Ring gauge (120px) in forest-ink on forest-wash with the value inside; sparklines 56px tall in forest-ink with start/end values; copy bars (5×13px) in forest-ink, off bars in rule; coverage bar 8px. Deltas as a forest-wash chip ("247 fewer"). |
| All clear | Centered in the detail area: 84px {colors.lime-wash} disc with a forest-ink sprout and a {colors.sprout-ring}, faint {colors.lime-ring} halo; 30px title, one scoped paragraph, three stats between rules, severity line, then actions. |
| Key cap | {components.kbd}: mono 12px, canvas, 1px rule with a bottom edge. Inside buttons it inherits the button colour. |
| Code block | {components.code-block}: copyable command or one-liner (setup `helm install`, `cosign verify-blob`, Prometheus endpoint). {colors.paper} fill, 1px {colors.rule} inset edge, {rounded.sm}, {typography.mono-small} in {colors.text-2}, 6px × 14px padding; a grey small **Copy** button ({spacing.button-height-sm}, sans label) at the right end. Long commands scroll horizontally; text is never cut off. |
| Signature status | {components.signature-status}. **Verified:** 34px round {colors.forest-wash} disc with a {colors.forest-ink} tick, then "Signature verified" in {typography.body} and the signer key below in {typography.meta} {colors.text-2}; the {components.code-block} with the offline command follows. **Does not verify:** an {components.error-band} in place of the disc and line — clay icon, title naming the file, body giving the reason, a link to the audit trail entry in {colors.forest-ink}; the download buttons stay. |

### Printed report

Audit reports (PDF, rendered with Typst) and printed exports use a **print-only light palette**, independent of the app theme:

- {colors.print-page} page, {colors.print-text} body text (17.4:1), {colors.print-text-2} secondary (7.5:1), hairline rules in {colors.print-rule} (decorative).
- Severity colours: Critical {colors.print-critical} (6.2:1), High {colors.print-high} (6.1:1), Medium {colors.print-medium} (6.8:1), Low {colors.print-low} (12.1:1), each on white and each with the level word and the 4-step marker beside it.
- IBM Plex Mono for every ID, fingerprint and command. [ASSUMPTION] Text face is IBM Plex Sans, replacing the prior spine's Inter so print matches the app. Body 9.5pt, tables 8.5pt.
- A4 by default; US Letter as an option.
- The cover sheet comes first and carries the coverage statement ("Covers 3,176 of 3,847 (82%)", with the not-checked software listed, not left out).
- Every page has a footer with the report ID, the time window, the generation time and the page number.
- Severity always has its word as well as its colour, so a black-and-white print stays readable; no red.
- Long tables repeat their header row on each page.
- The report uses plain labels with the technical term beside them; machine-readable companions keep technical names (SBOM, VEX).

## Do's and Don'ts

| Do | Don't |
|---|---|
| **Pills in detail, text in lists**: "Actively exploited" as clay text in rows, a clay-wash pill in detail panels and the Exposure answer | Pills, chips or fills for exploited, places or counts in list rows |
| **One lime action per view**, plus the active nav item | Two lime buttons on a screen; lime chips, lime list markers, lime text on the light canvas |
| Severity as word + 4-step marker in text colour | Red, red fills, or severity-coloured backgrounds anywhere |
| Plain label first, technical term small and grey beside it | Dropping the technical term, or leading with it |
| Headings that lead their own block | Eyebrows, kickers, tracked-caps labels above headings |
| Review status as a neutral chip with icon and word | Status-coloured chips |
| Severity, actively exploited and review status as separate axes | A combined "risk" or "chance of attack" rating; EPSS shown as a score, tag or column |
| One density for everyone | A Compact density or density toggle |
| Cells divided by 1px rules on a flat canvas | Nested cards, shadows on in-page elements |
| IBM Plex Sans for text; Plex Mono only for IDs, fingerprints, commands, keys | Mono for labels, headers or prose; a third family |
| Nine type sizes, plus the 22px wordmark as the single exception | Intermediate sizes (14.5, 15.5 …) |
| Coverage gaps as plain rows where the data would be | Hiding unchecked software in a footnote or tooltip |
| Semantic tokens; themes only remap values | Components referencing a theme-specific hex |
| Markers under 3:1 always beside a word | Meaning carried by a dot or dash colour alone |
