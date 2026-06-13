---
name: Armoury
status: draft
updated: 2026-06-12
sources:
  - _bmad-output/planning-artifacts/prds/prd-Armoury-2026-06-11/prd.md
  - _bmad-output/planning-artifacts/prds/prd-Armoury-2026-06-11/addendum.md
  - _bmad-output/planning-artifacts/briefs/brief-Armoury-2026-06-11/brief.md
  - _bmad-output/planning-artifacts/research/market-software-supply-chain-security-research-2026-06-11.md
---

# Armoury — Experience Spine

> Paired with `DESIGN.md` (visual identity reference — both spines inherit it). Visual references: [mockups/hybrid-posture-v2.html](mockups/hybrid-posture-v2.html) (Posture), [mockups/blast-radius-graph-v1.html](mockups/blast-radius-graph-v1.html) (Blast radius graph), [mockups/key-artifact-detail.html](mockups/key-artifact-detail.html) (Artifact detail), [mockups/key-findings-triage.html](mockups/key-findings-triage.html) (Findings + triage drawer), [mockups/key-evidence-packs.html](mockups/key-evidence-packs.html) (Evidence + packs), [mockups/key-graph-explorer.html](mockups/key-graph-explorer.html) (Graph explorer); Settings is spine-only by decision. Soft-chart inspiration: [Weblytics Dark Dashboard](https://dribbble.com/shots/15754500-Weblytics-Dark-Dashboard) (reference URL — Dribbble not importable). Spines win on conflict with renders. Render lag: hybrid-posture-v2.html predates the Graph explorer's 7th rail item (mock shows 6) — spines win.

## Foundation

Web product, desktop-first with tolerant degradation on tablet; no dedicated mobile layouts in v1. shadcn/ui + Tailwind (React) — both spines inherit; `DESIGN.md` is the visual identity reference and owns every token named here in `{path.to.token}` form. Self-hosted control plane (single instance, NFR10); read-only cluster agents report in; air-gapped deployments are first-class (NFR4, FR10). Roles: admin (configuration, connections), analyst (triage, pack generation), read-only auditor. Everything is operable by one SecOps engineer alone — zero dev-team cooperation is a product gate.

## Information Architecture

Slim left icon rail, 7 surfaces. No top nav.

| Surface | Reached from | Purpose |
|---|---|---|
| Posture | Landing state / rail / `g p` | Fleet-wide summary: artifacts, findings by priority, coverage gaps, feed freshness (FR16). What appears at minute 29. |
| Blast radius | Rail / `⌘K` query / `g b` | CVE or package+version in → affected artifacts, shipped vs running, where deployed — in seconds (FR17, NFR2). Graph and Table readings of the same answer. |
| Graph explorer | Rail / `g g` / "Explore in graph" | Open-ended traversal of the relational model (CVE → package → artifact → cluster/workload). |
| Artifacts | Rail / `g a` | List → detail: SBOM contents, findings (vulnerability and license) with triage status, evaluation provenance, running locations (FR18). |
| Findings | Rail / `g f` | Triage workbench — KEV-first, EPSS-weighted ranked list (FR13); triage drawer launches from any row. |
| Evidence | Rail / `g e` | Append-only evidence trail + evidence packs; "Generate CRA pack" lives here (FR21–25). |
| Settings | Rail (pinned bottom) | Registry connections (FR1), package feeds (FR29), agent install, feed-bundle import (FR10), license policy authoring (fleet-wide allow/deny lists, FR27), evidence retention (configurable; UI never permits below the 24-month compliance floor, FR23), Prometheus endpoint panel (read-only: endpoint URL + exported metric list with copy action — how an operator wires Grafana, FR20), theme, users/roles. |

- **Graph entry is dual:** Graph explorer has its own rail item, *and* every artifact, finding, and CVE carries a contextual "Explore in graph" action.
- **OIDC is declarative** — env vars / Helm values / config file, never a UI wizard (NFR6). Settings *displays* the resolved auth configuration read-only; first sign-in uses the bootstrap admin.
- License findings live inside Posture, Findings, and Artifact detail — embedded, never headline; there is no dedicated license dashboard (FR26–28).

## Voice and Tone

Microcopy. Calm, honest, evidence-led. Counts and verbs, no exclamation, no fear. **Definitive in tone only when the data earns it** — every definitive sentence is scoped to what was actually scanned.

| Do | Don't |
|---|---|
| "Production fleet — what we know, and what we don't yet" | "Your security at a glance!" |
| "Findings in this range are unknown, not absent." | Silence about unscanned artifacts |
| "14 affected artifacts · 9 running · 2 clusters" | "You're at risk! 14 vulnerabilities found" |
| "Populating — 671 artifacts queued for first scan." | A spinner with no account of what's missing |
| "This answer is definitive for the 14 scanned artifacts only." | "All clear" over partial coverage |
| "All 847 artifacts SBOM'd and scanned the same way — Syft v1.4 · Grype v0.92" | Fleet numbers with no account of how they were measured |
| Auditor-facing and analyst-facing: same words, same numbers | A softer story for the auditor |

**Locked glossary** (identical across product, packs, and docs): *Artifact*, *Fleet*, *Finding* (vulnerability match or license violation), *Posture* (fleet-wide, freshness-labeled state of findings and coverage), *Evidence*, *Evidence pack*, *Control plane* (the central web UI, graph, and evidence store), *Cluster agent* (read-only in-cluster reporter). Triage statuses, always lowercase, always this set: **not affected / mitigated / accepted / fix planned** (plus the derived display state *untriaged*). Never invent synonyms ("issue", "alert", "report").

## Honest Provenance

The signature pattern. **The posture must never need a caveat the UI doesn't already show.** Every answer-bearing surface carries its own sources, coverage, and freshness — inline, not in a help page:

- **Freshness strip** on Posture, Blast radius, and Artifact detail: each feed (Grype DB, KEV catalog, EPSS, CNA records, OSV, SBOM index, runtime observation) with version and age, in {typography.mono-meta}; ages colored {colors.success} (fresh) / {colors.warning} (stale).
- **Coverage gaps are first-class rows** — rendered inline in findings tables and lists as coverage-gap rows, positioned where the missing data would be, naming counts and locations ("671 artifacts not yet scanned, including 212 in `prod-eu-west`").
- **Every blast-radius answer ends with a provenance footer** and, when applicable, an explicit caveat line scoping the answer ("2 artifacts in scope have no SBOM yet and are not represented").
- **Every enrichment datum is source-attributed** (FR12) — source name + retrieval time on hover/expansion; every finding shows when it was last evaluated and against which feed versions (FR8). Feed updates re-evaluate stored SBOMs — answers are already current with no rescan, no rebuild (NFR5), and the provenance footer says so.
- **Uniformity is a visible claim** (FR6/FR21): Posture and pack covers state the single toolchain and versions — "All N artifacts SBOM'd and scanned the same way — Syft vX · Grype vY."
- **Evidence packs state their own coverage and data quality** on the cover sheet (FR24) — pack polish never outruns data integrity.
- A quiet dashboard is not the same as a safe fleet: zero-findings states always pair the zero with its coverage scope ("0 critical findings across the 82% of the fleet that is scanned").

## Theme System

Three dark themes, user-selectable, shipping day 1: **Forge** (default), **High Signal** (high-contrast option), **Gunmetal**. Behavior:

- Switcher lives in Settings, in the compact header affordance, and as a command-palette action ("Switch theme…"). Live preview on focus, applies instantly, no reload.
- Themes remap semantic tokens only (see `DESIGN.md` Colors); no layout, density, or behavior changes between themes.
- [ASSUMPTION] Theme choice persists per user server-side (so it follows the user across browsers); falls back to Forge for new users. No OS-preference detection — there is no light mode to detect into.

## Command Palette

Full Linear-grade palette on `⌘K` / `Ctrl+K` (shadcn `Command`). Keyboard-first is the philosophy: **every action in the product is invocable from the palette** — navigation, triage status changes, theme switching, pack generation, exports.

- **⌘K doubles as blast-radius query entry:** typing a CVE ID, `package@version`, or digest into the palette routes straight to a blast-radius answer. The Posture header search affordance is the same palette, pre-scoped.
- Results group: Answers (blast radius) → Navigate → Actions → Recent. `Enter` fires, `Esc` closes, results announce via `aria-live`.
- Full shortcut map, discoverable via `?` and listed in Settings. [ASSUMPTION] Vim-style two-key nav (`g` + letter, per IA table) and single-key actions in lists: `t` open triage drawer, `e` explore in graph, `x` export — exact bindings open until usability pass.

## Data-Quality Score

FR30: a second score alongside risk — SBOM depth, scan coverage, feed freshness, enrichment coverage, CVE record quality — surfaced at fleet level (Posture co-stat), artifact level (Artifact detail header), and on evidence-pack covers. The scoring model itself is an open architecture/UX decision; presentation rules that hold regardless:

- DQ always renders in {colors.data-quality} — never a severity hue. It is an instrument reading, not a threat level.
- [ASSUMPTION] Presented as 0–100 score with a letter grade (e.g. "84 B+"); compact contexts (table rows) show grade-only dq-badge. Grade banding to be fixed with the scoring model.
- DQ is always expandable to its component dimensions — the score is explainable on click, mirroring ranking explainability (FR13).
- Low DQ dims, it never alarms ({components.dq-badge}); the corrective action ("connect feed", "rescan") is offered alongside.

## Graph Views

Two surfaces, one visual language ({components.graph-node}, {components.graph-edge-affected}):

- **Blast-radius graph:** the answer rendered as a 4-tier left-to-right node-edge graph — CVE → vulnerable packages → affected artifacts → clusters/workloads. Severity hue only on the affected path; running workloads carry the ember ring; shipped-but-not-running nodes are dashed and muted. Graph/Table toggle — same evidence, two readings. Large result sets roll up ("+ 9 more artifacts") with expand-to-enumerate.
- **Graph explorer:** open-ended traversal from any starting node. Entered from the rail (search-first empty state: "Start from a CVE, package, or artifact") or via "Explore in graph" from any artifact, finding, or CVE — which opens the explorer pre-centered on that node.
- Every node is labeled with its real identifier in mono and resolves to its detail surface (click) and its evidence (context action). Hover highlights the node's direct path; selection pins it.
- Graph motion follows the global motion policy: entrance/layout transitions are subtle and disabled under `prefers-reduced-motion`.

## Component Patterns

Behavioral. Visual specs live in `DESIGN.md` Components (or shadcn defaults where inherited).

| Component | Use | Behavioral rules |
|---|---|---|
| Icon rail | Global | One item per IA surface; active state mirrors route. Tooltips on hover/focus. Settings pinned bottom. Never collapses further — 58px is the floor. |
| Command palette | Global (`⌘K`) | See Command Palette section. One palette, context-pre-scoped where launched from search affordances. |
| Findings table | Findings, Posture, Artifact detail | KEV-first then EPSS-weighted order by default (FR13); header states the sort logic in words ("KEV first, then EPSS-weighted. Severity alone does not rank."). Row click or `t` opens the triage drawer; row hover reveals "Explore in graph". Pagination, not infinite scroll, at NFR3 scale. |
| Triage drawer | Slide-over right drawer (shadcn `Sheet`) from any findings list | Contains: ranking explanation (FR13 — why this finding ranks here), VEX context with vendor attribution (FR15), full provenance (FR8/FR12), and the decision form (status + justification). Submitting records author + timestamp (FR14), updates the row in place, and keeps the user in the list — drawer advances to next finding on `⌘Enter`, closes on `Esc`. Decisions propagate to posture views and evidence packs. |
| Coverage-gap row | Any findings/artifacts list | Inline at the position the missing data would occupy. Not dismissible, not collapsible — it disappears only when the gap closes. Click-through to the gap's cause (unscanned artifacts, unreachable registry, disconnected agent). |
| Populating banner | Posture, Artifacts | Appears whenever first-scan or re-evaluation backlog exists; states queue count and estimate; progress is live (see State Patterns). Never modal, never blocking. |
| Hero stat | Posture, Blast radius answers | One per surface. Numerals animate count-up on populate (suppressed under reduced motion). |
| Severity band | Posture | Stacked distribution; segments click-filter the findings table below. Always scoped-labeled ("scanned artifacts only"). |
| DQ badge / score | Posture co-stat, Artifact detail, table rows, pack covers | Expandable to dimension breakdown. See Data-Quality Score. |
| Triage pill | Tables, drawers, packs | Displays the locked status set only. Status changes happen in the triage drawer, never inline — a recorded decision requires a justification. |
| KEV tag | Anywhere a finding renders | Always adjacent to the CVE ID; never dropped in compact views — KEV is the one mark that survives every truncation. |
| Node inspector | Graph explorer | Side panel ({components.node-inspector}); selection pins the node and shows identity, knowledge, and provenance, plus actions: open detail, view evidence, blast radius from here. `Esc` unpins. |
| License chip | Posture, Findings, Artifact detail | License findings render the neutral {components.license-chip} — never severity-hued; the severity ramp is CVE-only. Same triage drawer flow as vulnerability findings. |
| Evidence pack card | Evidence surface | Every pack card carries "Verify signature" — in-UI check showing result + signer identity — plus a copyable offline verification command (cosign; operator-key equivalent on air-gapped installs) so an external auditor can verify independently (FR25). |
| Evidence pack generator | Evidence surface, `⌘K` | Visuals inherit shadcn `Dialog` + {components.button-primary}. One-click "Generate CRA pack" with smart defaults (last audit window, whole fleet); configuration is available *after* the click (window, scope, framework — FR22 extensible), not a wizard before it. Generation is async with a progress state [ASSUMPTION: minutes-scale, progress shown as pack sections complete]; result is signed (Sigstore, or operator keys when air-gapped) with PDF + machine-readable companions (SBOMs, VEX). |
| Export | Blast radius, Posture | "Export evidence pack" / report / CSV (FR19). Export carries the same provenance footer and caveats as the on-screen answer — always. |
| Freshness strip | Posture, Blast radius, Artifact detail | Read-only; each entry click-through to the feed's Settings page. |
| Theme switcher | Header, Settings, `⌘K` | See Theme System. |

## State Patterns

| State | Surface | Treatment |
|---|---|---|
| Populating (minute-29) | Posture | Posture is live and *visibly populating*, never blocked on completeness (NFR1): populating banner with queue count + estimate; coverage co-stat marked "populating"; hero numeral counts up as artifacts index; coverage-gap rows mark the unscanned remainder. Honest, partial, alive. |
| Partial answer | Blast radius | Answer renders for scanned scope; caveat chip ("2 artifacts unscanned — not represented") + provenance footer scope the claim. Never blocks on gaps. |
| Stale feeds | Global (freshness strip) + Posture | Feed age flips to {colors.warning} past freshness threshold; posture headline gains a scoped caveat; DQ score reflects it. Air-gapped instances additionally show feed-bundle age and "import bundle" action (FR10). |
| Disconnected agent | Posture, Settings | Runtime entries in the freshness strip show last heartbeat; affected clusters' runtime data is marked stale-as-of, not removed — "last seen" honesty over silent decay. [ASSUMPTION] Heartbeat staleness threshold (warn at minutes, disconnect at an hour) pending architecture's agent-buffering design. |
| Air-gapped mode | Global | [ASSUMPTION] Instance-level flag from deployment config; UI substitutes Sigstore copy with operator-key signing copy and shows bundle-import affordances. No phone-home affordances exist anywhere (NFR4). |
| Empty (pre-setup) | Posture | First-run: heading block + the two setup actions that matter (connect registry, install agent) with copy-paste one-liners in mono. No illustration theatre. |
| Empty (no results) | Blast radius, Graph explorer | "No artifacts affected — across the N% of the fleet that is scanned." The zero is always coverage-scoped. |
| Long-running query | Blast radius | Answers stream progressively (NFR2); if not complete within seconds, partial results render with an explicit scope line ("searching — 1,204 of 3,000 artifact set evaluated"); worst case under a minute. Never an unexplained spinner. |
| Cold load | All surfaces | shadcn `Skeleton` mirroring the real layout (hero numeral block, table rows). |
| Read-only auditor | Global | Triage forms, pack-config edits, and Settings mutations are absent (not disabled-and-teasing); generation/viewing of packs and all read surfaces fully available. |
| Append-only evidence (NFR11) | Evidence, triage history | No edit or delete affordances on recorded decisions or trail entries — corrections are new entries superseding old, with both visible. The UI never offers silent rewrite. |
| Error (pack generation) | Evidence | Pack fails closed with the failing section named; partial packs are never silently delivered. Retry re-runs failed sections. |
| Palette no match | `⌘K` | "No matches. Try a CVE ID, package@version, or digest." + common actions. |

## Interaction Primitives

**Keyboard-first.** The palette is the command center; the mouse is the fallback.

- `⌘K` / `Ctrl+K` — command palette / blast-radius query (universal)
- `g` + `p / b / g / a / f / e` — go to surface [ASSUMPTION — see Command Palette]
- `t` — open triage drawer on highlighted finding; `⌘Enter` — record decision and advance; `Esc` — close topmost layer
- `e` — explore highlighted entity in graph; `x` — export current answer; `?` — shortcut map
- Graph: arrows/`Tab` traverse nodes, `Enter` opens node detail, `+`/`−` zoom

**Motion:** polished throughout — micro-interactions on hover, chart and graph entrances, smooth drawer/palette transitions — but every animation is suppressed or reduced under `prefers-reduced-motion`. Populating motion is *purposeful state communication* (counting numerals, filling coverage), never decoration; under reduced motion it degrades to stepped numeric updates, not to information loss.

**Banned everywhere:** in-product notifications, toasts-as-alerts, or badge counts for new findings — signal exits via the Prometheus endpoint only, pull-based (FR20); OIDC setup wizards (NFR6); edit/delete affordances on evidence (NFR11); infinite scroll on fleet-scale tables; modal stacks deeper than one (drawer + dialog max); hover-only affordances without keyboard/focus equivalents; celebratory animation.

## Accessibility Floor

Behavioral; contrast lives in `DESIGN.md` (High Signal theme targets AAA text and is the built-in high-contrast option).

- WCAG 2.2 AA across all surfaces; commercial B2B + compliance audience makes this contractual, not aspirational.
- `prefers-reduced-motion` honored globally (see Interaction Primitives).
- Full keyboard operability: everything reachable without a pointer; visible focus rings (shadcn `ring`) on all interactive elements; `Tab` order = reading order.
- Graph views have non-graph equivalents: the Graph/Table toggle is also the accessibility path — every graph answer is fully readable as a table; graph nodes are focusable with `aria-label`s carrying identifier + tier + state.
- Screen reader announces surface on navigation ("Posture — populating, 82% coverage") and live changes (palette results, populate progress) via polite `aria-live`.
- Severity, triage status, and running-state are never color-only: chips carry text, KEV is a text tag, running nodes have ring + pip + label.
- i18n: English-only UI in v1, but all strings externalized from day 1 — no concatenated sentences, no text baked into SVG assets.

## Responsive & Platform

| Viewport | Behavior |
|---|---|
| ≥ 1280px | Full layout: rail + 52px-gutter main column, graph canvases full-width. Primary target. |
| 1024–1279px (tablet landscape) | Tolerant degradation: same layout, tighter gutters, tables scroll horizontally before columns drop, graph canvas pans. |
| < 1024px | Best-effort read-only degradation; no dedicated mobile layouts in v1. Nothing breaks, nothing is optimized. [ASSUMPTION] Breakpoint values — sources fix only "desktop-first, tolerant tablet degradation". |

Web only; no native apps. Self-hosted means unpredictable enterprise browsers: last-2-versions evergreen baseline.

## Inspiration & Anti-patterns

- **Lifted — soft data visualization** ([Weblytics Dark Dashboard](https://dribbble.com/shots/15754500-Weblytics-Dark-Dashboard), Dribbble reference URL in decision log): rounded, muted charts and tables; no neon analytics.
- **Lifted from Linear:** keyboard-first command palette discipline — `⌘K` as the command center, full shortcut map.
- **Lifted from operator-console exploration** (.working/direction-operator-console.html — rejected as a whole, mined for parts): the slim icon rail and the dense findings table, transplanted into the calm canvas.
- **Lifted from evidence-ledger exploration** (.working/direction-evidence-ledger.html — direction rejected, character kept): the mono-accents-for-identifiers idea that became the IBM Plex Mono rule in `DESIGN.md`.
- **Rejected — command-surface direction** (.working/direction-command-surface.html): terminal-cosplay chrome; the keyboard-first idea survived as the command palette, the aesthetic did not.
- **Rejected — generic dashboard rhythm** (.working/direction-calm-canvas.html critique: "looks AI generated"): uniform KPI-card grids, centered headings, template type. Cured by the asymmetric type system in `DESIGN.md`.
- **Rejected — Anchore's setup complexity** (market research): no multi-step configuration ceremony; setup is two one-line installs and pasted read-only credentials; the <30-minute path is the product's wedge.
- **Rejected — Snyk's fragmented UI:** one rail, seven surfaces, one glossary; license findings embedded rather than a parallel product area.
- **Rejected — alert-noise fatigue** (73% of practitioners name false-positive noise top challenge): no in-product notification system at all; KEV-first ranking with stated logic instead of severity walls; metrics exit via Prometheus, the customer's own Grafana decides what alarms.
- **Out of UI scope permanently:** runtime threat detection, auto-remediation, multi-scanner orchestration UI, dedicated license dashboard, reachability claims.

## Key Flows

### Flow 1 — UJ-1: The first 30 minutes (Priya, SME SecOps engineer, alone, post-audit)

1. Priya runs the `helm install` one-liner for the control plane. Minutes later she opens the URL.
2. She signs in with the **bootstrap admin** credential from the install output — SSO is never allowed to stand between her and minute 29; OIDC can be wired up later via Helm values, never a UI wizard.
3. Empty Posture greets her with exactly two actions: connect a registry, install a cluster agent. She pastes read-only registry credentials. [ASSUMPTION inherited from PRD: single registry in the first session.]
4. The Posture surface comes alive: populating banner states the queue ("671 artifacts queued for first scan"), the artifact hero numeral counts up, coverage co-stat climbs, freshness strip shows feeds syncing.
5. She runs the second one-line `helm install` for the cluster agent; runtime entries appear in the freshness strip as the first heartbeat lands. The install affordance always states the trust posture — the agent is read-only, watch/list only, never cluster-admin — with the exact RBAC shown before install (NFR9).
6. **Climax — minute 29:** the full posture view is live and *visibly populating* — findings ranked KEV-first with the ranking logic stated in the table header, coverage gaps honestly displayed as first-class rows, feed freshness on screen. The whole fleet in one place she doesn't have to caveat — because the UI already carries every caveat itself. Full evaluation completes within 24h; the surface never pretended otherwise.

Failure: registry unreachable → connection error surfaces in Settings *and* as a coverage-gap row on Posture naming the registry; posture continues with what it has.

### Flow 2 — UJ-2: CVE day (Priya, the log4shell moment)

1. Her own Grafana alert (fed by Armoury's Prometheus endpoint — Armoury itself sent nothing) flags a new KEV entry. The news is everywhere.
2. From anywhere in Armoury: `⌘K`, types the CVE ID, Enter.
3. **Seconds later** (NFR2): the blast-radius answer — "14 affected artifacts · 9 running · 2 clusters" — rendered as the 4-tier graph: CVE → vulnerable packages → affected artifacts → clusters/namespaces/workloads. Running workloads ember-ringed; shipped-but-not-running dashed. A caveat chip scopes the claim: "2 artifacts unscanned — not represented." The provenance footer shows why the answer is already current: "Re-evaluated against Grype DB v5.61, 41 min ago — no rescan needed" — existing SBOMs were re-evaluated when the feed updated; nothing rebuilt, nothing rescanned (NFR5/FR8).
4. She toggles to Table to scan namespaces, then back to Graph.
5. **Climax:** she hits Export — the evidence-pack report, carrying the same provenance footer and unscanned caveat, goes to the CTO *before he's read the news*.
6. She works the affected list: `t` opens the triage drawer on each finding — ranking explanation, VEX context, provenance — records "fix planned" / "not affected" with justifications, `⌘Enter` advancing through the list without leaving it.
7. Every decision is already in the append-only evidence trail with author and timestamp. Nothing to write up later.

Failure: query matches nothing → "No artifacts affected — across the 82% of the fleet that is scanned"; the zero is coverage-scoped, and the unscanned remainder is one click away.

### Flow 3 — UJ-3: Audit day (Marta, compliance lead, read-only auditor)

1. Marta signs in under the read-only auditor role. The rail is the same product Priya uses — minus mutation affordances; nothing is disabled-and-teasing.
2. She opens Evidence and clicks **Generate CRA pack**. Smart defaults take the last audit window and the whole fleet — one click, no wizard. (Window, scope, and framework remain adjustable after the fact; the pack architecture is framework-extensible, FR22.)
3. Generation runs async with visible progress; she keeps browsing the evidence trail — every triage decision from CVE day is there, append-only, attributed, timestamped.
4. The pack lands: PDF + machine-readable companions (SBOMs, VEX statements), **Sigstore-signed** (operator keys on air-gapped installs), tamper-verifiable. Marta clicks "Verify signature" on the pack card — result and signer identity shown in the UI — and copies the offline verification command (cosign; operator-key equivalent on air-gapped) so the external auditor can verify independently (FR25).
5. **Climax:** the pack's cover sheet states its own coverage and data-quality score — the honest scope of the claim, in the document itself. Three weeks of spreadsheet archaeology is now a generated, signed document she hands to the auditor without a single hand-assembled appendix.

Failure: the window includes coverage gaps → the pack discloses them on its cover exactly as the UI did at the time; pack polish never outruns data integrity. Generation failure → fails closed naming the failing section; no partial pack is silently delivered.
