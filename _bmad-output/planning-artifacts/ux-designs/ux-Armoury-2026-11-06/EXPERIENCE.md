---
name: Armoury
status: final
updated: 2026-11-06
supersedes: ux-Armoury-2026-06-12
sources:
  - _bmad-output/planning-artifacts/prds/prd-Armoury-2026-06-11/prd.md
  - _bmad-output/planning-artifacts/prds/prd-Armoury-2026-06-11/addendum.md
  - _bmad-output/planning-artifacts/briefs/brief-Armoury-2026-06-11/brief.md
  - _bmad-output/planning-artifacts/research/market-software-supply-chain-security-research-2026-06-11.md
  - _bmad-output/planning-artifacts/ux-designs/ux-Armoury-2026-11-06/.memlog.md
  - _bmad-output/planning-artifacts/ux-designs/ux-Armoury-2026-11-06/mockups/greenhouse-final.html
  - _bmad-output/planning-artifacts/ux-designs/ux-Armoury-2026-11-06/imports/inspo-shost-server-dashboard.png
---

# Armoury — Experience Spine

> Paired with `DESIGN.md`, which owns every token named here in curly-brace reference form (for example {colors.lime} or {components.status-chip}). Approved composition reference: [mockups/greenhouse-final.html](mockups/greenhouse-final.html). **The spines win on conflict with any mock.** Supersedes `ux-Armoury-2026-06-12`: its product behaviour, flows and primitives carry over except where the decision log ([.memlog.md](.memlog.md)) changes them; every change is listed in [Changes from ux-Armoury-2026-06-12](#changes-from-ux-armoury-2026-06-12). Mock numbers (1,094 open issues, 3,847 pieces of software, 82% checked) are example data used consistently across screens and flows.

## Foundation

Web product, desktop-first. shadcn-svelte + Tailwind on SvelteKit; `DESIGN.md` is the visual reference. Self-hosted control plane (single instance, NFR10); read-only cluster agents report in; air-gapped deployments are first-class (NFR4, FR10), which is one reason the fonts are self-hosted.

**North star: approachable first.** Security is stressful; the product must feel calm and serene, never intimidating or exhausting. Calm comes from the light canvas, plain words, spacing and restrained colour, not from hiding data: tables, filters, grouping, pagination and keyboard paths stay.

**Two primary users, equal weight:**

- **Security engineers** (Priya, the PRD's SME SecOps engineer) who need precision and the fastest route to information.
- **Non-technical leaders** (Tom Reid, Head of Engineering in the mock) who need to know "are we safe, and what needs attention" quickly.

One layout and one density serve both. Plain words lead; the technical term stays, small and grey.

**Roles** (unchanged): admin (configuration, connections), analyst (review, audit report generation), read-only auditor. Everything is operable by one security engineer alone — zero dev-team cooperation is a product gate.

## Information Architecture

**Black sidebar ({components.sidebar}), seven items**: Home · Software · Issues · Exposure · Reports, a divider, then Settings · Help. The sidebar is headed by a "Search or jump to… ⌘K" field and ends with the signed-in user's menu ({components.user-menu}). The active item is lime ({colors.lime}). Issues carries a badge with the Needs-attention count; at 0 there is no badge.

**The issue unit.** One Issues row is **one vulnerability (or one licence) in one package version** — for example log4j-core 2.17.0 × CVE-2026-23012 — across every place it affects ("14 places"). A review applies to **all places by default**; a different status can be set for **one piece of software**. When places differ, the row's status chip reads **Mixed** with the count of places that differ from the issue-wide status ("Mixed · 3 of 14"). An issue counts as Not reviewed yet, and can need attention, while **any** of its places is Not reviewed yet. Counts on every surface (312 not reviewed yet, 1,094 open, the badge) count issues, not places.

**Page title = sidebar label**, with a friendly summary line under it ("Issues" + "3 need attention today. 312 not reviewed yet."; "Exposure" + "Where are we exposed to log4j-core?").

**Three-column master-detail** on every surface: sidebar · list column (title, summary, filters, grouped list with counts, pager, the view's one primary action, {components.button-primary}) · tabbed detail column. Detail tabs ({components.tabs}) end with the position and keys ("1 of 3 · J K").

| Surface | URL (as drawn) | Purpose | Primary action |
|---|---|---|---|
| Home | `/` | Landing. "Are we safe, and what needs attention?" Fleet summary, coverage, freshness (FR16). | Review all 3 |
| Software | `/software/<name>` | The real fleet, grouped Deployed / Not deployed, with what we haven't checked said plainly (FR18). | Add software |
| Issues | `/issues?review=not-reviewed` | Every open issue — vulnerabilities and licences — grouped by severity; review without leaving the list (FR13, FR14, FR27). | Save and next |
| Exposure | `/exposure?q=log4j-core@2.17.0[&view=table]` | Ask about a vulnerability, a package or a fingerprint; one answer as a map or a table (FR17, FR19). Absorbs the prior Blast radius and Graph explorer. | Review (in the inspector) |
| Reports | `/reports/<id>` | Audit reports and exports, nothing else (FR19, FR21–25). | Generate audit report |
| Settings | `/settings/<panel>` | Connections, sources, policy, access, signals, personal. | — |
| Help | — | Not designed (see Open items). | — |

### Home

- **List column:** "Home" + "You are in good shape. 3 things need attention today." + "Last checked 38 min ago".
  - **Needs attention N** — the issues that need someone today. Rule: *An issue needs attention when it is Not reviewed yet (in any place) AND it is Actively exploited OR Critical. Every licence issue that is Not reviewed yet also needs attention.* Rows use the standard row shape; right column is places ("14 places").
  - **Open issues N** — summary rows: **Licences** first (hidden at 0), then Critical (with "1 actively exploited"), High, Medium, Low, each with its count.
  - "312 not reviewed yet · 782 reviewed · See all" (See all opens Issues), then the lime **Review all 3**.
- **Detail column** (the selected issue): tabs **Overview · Exposure · How to fix · Details**.
  - Overview: title, one plain sentence of what it means ("…lets an attacker run their own code. People are using it in real attacks right now."), severity, Actively exploited pill + KEV tag; Vulnerability (CVE ID), Found in, The fix, Review status; grey Review and See exposure; an Exposure cell (All / Deployed / Not deployed) listing the first places and "See all 14 on the map".
  - **Exposure tab:** a reduced summary of the Exposure page so people can scan it quickly, with a button that opens the full Exposure page for that query.
- **"Across all software" band** under the issue, clearly separate from it: Checked (82% gauge, "671 are waiting their turn"), Open issues (last 30 days, sparkline, "247 fewer"), Audit report (last 12 months, signed, coverage, Download / Preview).
- **Freshness strip** at the bottom.

### Issues

- **Filters:** a type segmented control **All · Vulnerabilities · Licences** with counts (licence problems are not vulnerabilities; "Licences 0" stays visible in the filter); a **Review status** filter listing all five statuses with counts, **default Not reviewed yet**; a search field ("Find a package or vulnerability", `/`); the ordering stated in words: "Actively exploited sorts first in each group".
- **Grouping:** **Licences** at the top (hidden when 0 — licence issues are rare and each needs a decision), then **Critical · High · Medium · Low**. Within each group, Actively exploited items first; [ASSUMPTION] then ordered by the raw EPSS value, which is never shown as a rating. Long groups end with an "N more High" row.
- **Rows:** standard row shape, one row per issue (see The issue unit); right column is the review-status chip, or **Mixed · N of M** when places differ.
- [ASSUMPTION] The **Review status** filter matches an issue when any of its places has that status, so a Mixed issue can appear under more than one status; counts are issues.
- **Pager:** "1–25 of 312 · page 1 of 13". Never infinite scroll.
- **Detail tabs: Review · Exposure · History.** Review holds the summary (title, severity, pill, KEV), Exposure count with "See the map", What to do, Review status, the **review panel** and the technical-details block. Exposure and History are not drawn (see Open items).

### Software

- "Software" + "3,847 pieces of software. 1,126 deployed, 2,721 not deployed." The **real fleet**, grouped **Deployed N** (row line 2: "prod-eu-west · 4 copies") and **Not deployed N** (line 2: "Last deployed 12 days ago" or "Never deployed"; hint "Not seen running in any connected cluster."). Right column: issue count ("2 issues").
- **Not checked yet 671** — the coverage-gap row, in place: "Counted above, but we haven't looked inside them yet, including 212 in prod-eu-west. Their issues are unknown, not absent."
- Pager "1–25 of 3,847 · page 1 of 154"; lime **Add software**.
- **Detail tabs: Overview · Issues · Packages · Audit trail**, with "Deployed" status at the bar's end. Overview: Name, Fingerprint (mono, copy), Runs in, Copies, Built, Last checked, Signed; grey Check again and Audit report; cells for Issues (with Review), Packages ("214 packages · SBOM", Direct 37 / Indirect 177, licence and end-of-life lines), Where it runs (each copy with zone), Latest in the audit trail ("Entries are never edited or removed"), and an issues trend.

### Exposure

- Header across the list and map: "Exposure" + the question ("Where are we exposed to log4j-core?"); the query button showing the subject (opens ⌘K to change the question); **Graph · Table** switch; grey Export and "Audit report for this answer".
- **The answer first, in words:** "14 pieces of software have it. 9 are deployed, 5 are not deployed." Meta: Actively exploited pill, KEV, Critical, CVSS 9.8, "Answered 38 min ago"; deployed/not-deployed split.
- **List column:** Deployed N, Not deployed N, then the "Not checked yet" gap row ("…so we can't say either way. They're not on the map. Next check in about 20 min.").
- **Graph:** four tiers — Vulnerability · Package · Software · Where it runs. Deployed solid, Not deployed dashed below a labelled rule. Legend, zoom (+ / − / Fit), and a caveat line under the map.
- **Inspector** under the map for the selected node: identity, How it got it, What to do (fix, review status), lime Review, grey Open software, "How we know".
- **Table:** the same answer, same order (deployed first), sortable sentence-case headers; selection carries across Graph and Table; "2 not checked yet, not listed".
- Queries accept a vulnerability ID, `package@version` or a fingerprint. A fingerprint query centres on that piece of software (prior digest layout).
- **No query** (`/exposure` from the sidebar): the answer slot asks "Ask about a vulnerability, a package or a fingerprint." with examples ("CVE-2026-23012 · log4j-core@2.17.0 · sha256:…"); the query button opens ⌘K.
- **Unknown vulnerability:** when Armoury has no data for the queried ID, the answer reads "Armoury has no data for <ID> yet. Vulnerability data updated <age> ago." with **Check again**. It never says "No software has it" for an ID it doesn't know. A **known** vulnerability with no matches gets the coverage-scoped zero (State Patterns).

### Reports

- **Audit reports N** and **Exports N**, nothing else. New report types (for example a management summary) are new scope and need Correct Course first.
- Export rows say what and where from ("Exposure: log4j-core 2.17.0 · CSV · 14 rows · from Exposure"). "Exports are kept for 24 months, like audit reports. Make a new one from Exposure, Issues or Software with Export."
- Lime **Generate audit report**.
- **Detail tabs: Overview · Files · Audit trail**, with "Generated today, 08:31, by …" at the bar's end. Overview: coverage when it was made, Signature ({components.signature-status}: verified in product, plus the copyable `cosign verify-blob` command in a {components.code-block}: "Auditors can run this themselves, without Armoury."; when it does not verify, see State Patterns), Files (pack.pdf, sboms.tar.gz "Package lists … SBOM", vex.json "review decisions … VEX"), What it says.

### Settings

Spine-only (no mock), carried from the prior spine. An in-page panel list (in the list column) with one route per panel, `/settings/<panel>`, so links (for example "Sources" on the freshness strip, "Open connection settings" on an error) open a panel directly. Panels: **Connections** (registries FR1, package feeds FR29, agent install) · **Sources** (feed status and history, bundle import FR10) · **Policy** (licence policy FR27, CI policy, retention — never below the 24-month floor, FR23) · **Access** (users and roles, resolved auth configuration read-only, CI tokens) · **Signals** (Prometheus endpoint, read-only with copy, FR20; signing key) · **Personal** (theme, keyboard shortcuts including the switch that turns single-key shortcuts off). Edit controls are absent for roles without write access. OIDC is declarative (env vars / Helm values), never a UI wizard (NFR6).

### Help

In the sidebar of the approved design; content not specified by any source (see Open items).

### Rules across surfaces

- No dedicated licence dashboard: licences live in Issues (Licences group and type filter), Home (Open issues) and a software's Packages and Issues (FR26–28).
- Contextual entry to Exposure replaces "Explore in graph": See exposure, See the map, See all 14 on the map, and Exposure results in ⌘K.

## Voice and Tone

Calm, plain and honest. Counts and verbs; no exclamation marks, no fear, no jargon in primary labels. Definitive only when the data earns it: every reassuring sentence is scoped to what was checked. Analyst, leader and auditor see the same words and the same numbers.

| Do | Don't |
|---|---|
| "You are in good shape. 3 things need attention today." | "Your security at a glance!" |
| "14 pieces of software have it. 9 are deployed, 5 are not deployed." | "You're at risk! 14 vulnerabilities found" |
| "Nothing needs you today. … That covers the 3,176 pieces of software we've checked; 671 are still waiting their turn." | "All clear" over partial coverage |
| "Their issues are unknown, not absent." | Silence about unchecked software |
| "We can't reach registry.acme.internal. … Nothing has been removed." | "Sync failed (502)" |
| "Checking 671 more pieces of software… about 2 h left" | A spinner with no account of what is missing |
| "Saved with your name in the audit trail." | "Success!" |
| "Decide later" | "Skip" |

### Glossary: plain label → technical term

This **replaces the prior "locked glossary"**. Rule: **plain label first; the technical term small and grey beside it, never removed.** Exports and audit reports keep the technical terms (VEX statuses, SBOM, CVE) so machines and auditors get standard vocabulary.

| Plain label (UI) | Technical term | Where the technical term appears |
|---|---|---|
| Home | Posture | Docs and PRD only |
| Issues / issue | Finding (vulnerability match or licence-policy violation) | Docs; exports |
| Vulnerability [ASSUMPTION: replaces "Weakness"] | CVE | The ID, small and mono: detail ("Vulnerability CVE-2026-23012"), technical details, Exposure query, palette |
| Actively exploited | KEV (CISA Known Exploited Vulnerabilities) | Grey "KEV" tag in detail views and the Exposure answer; technical details; freshness strip ("Exploited list KEV") |
| Licence | Licence-policy violation (SPDX ID as the name, e.g. AGPL-3.0) | Kind tag "Licence"; audit report licence section |
| Exposure | Blast radius | Docs only |
| Reports | Evidence packs and exports | Docs; file names (`pack.pdf`) |
| Audit report | Evidence pack (CRA pack) | File names and the verification command |
| Audit trail / History | Evidence trail (append-only) | Docs |
| Software / piece of software | Artifact | Docs and API |
| Places | Affected software | — (the detail says "Found in 14 pieces of software") |
| Packages | SBOM components | "SBOM" small and grey beside "214 packages"; Reports file list |
| Direct / Indirect | Direct / transitive dependency | "transitive" in technical detail |
| Deployed / Not deployed | Running / shipped, not running | Hint on Not deployed: "Not seen running in any connected cluster." Exposure table column "Deployed?" uses Yes / No |
| Copies | Running replicas | — |
| Where it runs | Cluster / namespace / workload | Shown as a path ("prod-eu-west/payments") |
| Fingerprint | Image digest | The `sha256:` value in mono |
| Checked / Not checked yet | Scanned / unscanned (coverage gap) | — |
| Check again | Rescan | — (on Exposure's "no data yet" answer, Check again re-asks the question against the latest vulnerability data; no rescan) |
| Vulnerability data · Exploited list · Packages · Sources | Vulnerability feed (Grype DB) · KEV catalog · SBOM index · feeds | Freshness strip (small term) and "How we know: Syft v… · Grype DB v…" |
| Review / Review status | Triage / triage status | Docs |
| Not reviewed yet | untriaged | Exports, audit report, VEX |
| Needs a decision | Licence-policy violation, untriaged | Second line of a licence row that is Not reviewed yet ("AGPL-3.0 — Licence · Needs a decision · report-render") |
| Mixed · N of M | Per-product triage status differs | Status chip on an issue whose places have different statuses; VEX states each product's own status |
| Not impacted | not affected | VEX (vex.json), audit report |
| Fix planned | fix planned | VEX, audit report |
| Mitigated | mitigated | VEX, audit report |
| Risk accepted | accepted | VEX, audit report |
| Why? | Justification | VEX, audit report |
| Severity: Critical / High / Medium / Low | CVSS severity | "CVSS 9.8" in the answer meta and technical details |
| (not shown) | EPSS | Raw value only in the grey technical-details block. Never a rating, tag or column. |

UI copy is British English ("Licences"). **Retired labels** (must not appear): Posture, Findings, Blast radius, Graph explorer, Artifacts, Evidence, triage, Things to look at, Where it's affected, Weakness, ingredients, What's inside, Chosen by your team, Came along with them, Running, Shipped not running, Undeployed, Being attacked in the wild, chance of attack, Doesn't affect us, Fixed for now, Workaround in place, Mark reviewed, Plan the fix, Skip.

## Component Patterns

Behavioural. Visual specs live in `DESIGN.md` Components.

| Component | Use | Behavioural rules |
|---|---|---|
| Sidebar | Global | One item per surface; active state mirrors the route. The search field opens ⌘K. Issues badge = Needs-attention count; no badge at 0. It is a count of what needs a decision, not a new-findings notification. |
| Grouped list (List row, Group heading, Pager) | Home, Issues, Software, Exposure, Reports | {components.list-row} under {components.group-heading}; {components.pager}. Groups with counts; one row shape (name + version · severity · actively exploited · where · one right column). Click or `J`/`K` selects and fills the detail column; the list keeps its place. Groups too long for the page end in an "N more …" row. Pagination at 25 per page, never infinite scroll (NFR3 scale). |
| Needs attention | Home, Issues summary, sidebar badge | An issue needs attention when it is Not reviewed yet (in any place) AND it is Actively exploited OR Critical. Every licence issue that is Not reviewed yet also needs attention. A Mixed issue stays in Needs attention until none of its places is Not reviewed yet. The same number everywhere it appears. |
| Severity groups | Issues, Home "Open issues" | Licences group first and hidden at 0; then Critical, High, Medium, Low; Actively exploited first within each. The sort is stated in words above the list (explainable ordering, FR13). |
| Actively exploited marker | Rows, detail, Exposure, palette | **Text in lists, pill in detail**: quiet clay text with icon ({components.exploited-text}) in list rows and palette results; filled pill ({components.exploited-pill}) in detail panels and the Exposure answer; {components.kev-tag} only in detail views. Never dropped when a row truncates. |
| Review status filter | Issues | Five statuses with counts; default Not reviewed yet. Never mixed with the severity groups. |
| Review panel | Issues detail (Review tab) | Options are {components.review-option} rows; the reason is a {components.review-note-field}. A **scope** control sits above the questions: **"All 14 places"** (default) or **"Only this software"**, which asks which piece of software (pre-filled when Review was opened from a piece of software). Replaces the prior slide-over triage drawer; the list stays visible. See [Review flow](#review-flow). Status changes happen only here, never inline, because a decision needs its reason. **Save failure:** an {components.inline-error} line in the panel names the problem and offers **Try again**; Save and next does not advance; the chosen options, scope and "Why?" text stay filled in. |
| Status chip | Every row and detail that shows a decision | {components.status-chip}. Five statuses, each with its icon and word, plus **Mixed · N of M** (own icon, neutral) when an issue's places have different statuses; N is the places that differ from the issue-wide status. Accessible name in full ("Mixed: 3 of 14 places have a different status"). Reflects the latest recorded decision per place. |
| Review action | Home, Exposure inspector, Software Issues cell | One "Review" action replaces "Plan the fix" and "Mark reviewed". [ASSUMPTION] Outside Issues it opens that issue in Issues on its Review tab. |
| Coverage-gap row | Software, Exposure (list and table), Home band | {components.coverage-gap-row}. Sits where the missing data would be, names the count and where ("including 212 in prod-eu-west"), says "unknown, not absent". Not dismissible, not collapsible; it disappears only when the gap closes. Click-through to the cause (unchecked software, unreachable registry, disconnected agent). |
| Exposure answer | Exposure | Answer in words first, then the map or table. Every answer carries its caveat line for unchecked software and "Answered N min ago" / "How we know". Feed updates re-evaluate stored package lists; answers are current with no rescan (NFR5). |
| Exposure graph | Exposure | {components.exposure-graph} with {components.inspector} and {components.table}. Graph and Table are two readings of one answer; selection carries across. Hover highlights a node's direct path; click selects and pins it (inspector updates); `Esc` unpins. Roll-up nodes ("8 more") expand. Nodes resolve to their detail (Open software). |
| Home Exposure tab | Home detail | Reduced summary of the Exposure page for the selected issue; a button opens the full Exposure page for that query. |
| Export | Exposure, Issues, Software | CSV of the current view; lands in Reports → Exports; kept 24 months. Carries the same caveats and provenance as the screen ("The 2 not checked yet travel with the CSV and the audit report"). |
| Audit report generator | Reports, ⌘K | One click on Generate audit report with smart defaults (last 12 months, whole fleet); window, scope and framework adjustable after the click, not a wizard (FR22). Asynchronous with progress. Signed with cosign using the operator key by default; keyless only when enabled, never when air-gapped. PDF + package lists (SBOM) + review decisions (VEX). |
| Signature status | Reports | {components.signature-status}. "Signature verified" with the signer key in the product, plus the copyable offline command (FR25). When it does not verify: see State Patterns. |
| Code block | Empty Home setup, agent install, Reports, Settings → Signals, Software fingerprint | {components.code-block}. **Copy** copies the whole command, never a truncated one; the label changes to "Copied" for 2 s and is announced politely (`aria-live`). Copy is keyboard reachable; the command text is selectable. |
| Inline error | Review panel, Export, Generate audit report, Settings panels | {components.inline-error}. A failed save or start shows one line where the action was taken, naming the problem in plain words, with **Try again**. Nothing advances or closes; every entered value stays. Announced with `role="alert"`. Not a toast. Clears on a successful retry. |
| User menu | Sidebar foot | {components.user-menu}. Shows the signed-in name and role; opens a menu with **Personal settings** (Settings → Personal) and **Sign out**. Keyboard: `Enter`/`Space` opens, arrows move, `Esc` closes and returns focus. |
| Freshness strip | Home | {components.freshness-strip}. Each source and its age; stale turns amber with the age in words. "Sources" opens Settings → Sources. Exposure and Software detail carry provenance inline ("Answered 38 min ago", "How we know", "Last checked"). |
| Tabs | Detail column | Counts in tabs ("Exposure 14", "Packages 214"). Position and keys at the bar's end. |
| ⌘K palette | Global | {components.command-palette}. Search or jump: results grouped Issues · Software · Exposure · Actions; the first result is the best match; `↵` opens; the dialog traps focus, dims the page, never navigates on its own, and returns focus on `Esc`. Typing a CVE ID, `package@version` or fingerprint routes to an Exposure answer. Every action is invocable here (Review, Export, Generate audit report, Switch theme). |
| Theme switch | Settings → Personal, ⌘K | See [Theme](#theme). |

### Review flow

Two questions, in the review panel, copy as approved:

1. **"Does this vulnerability impact us?"**
   - **No, not impacted** — "Our software doesn't use the vulnerable code." → *Not impacted*
   - **Yes** → reveals question 2.
2. **"What will we do?"**
   - **Fix it** — "Update log4j-core to 2.17.2." → *Fix planned*
   - **Reduce the risk** — "Lower the risk without updating the package, for example with a config change or a firewall rule." → *Mitigated*
   - **Accept the risk** — "Leave it as it is, for a reason we record." → *Risk accepted*

**Scope** comes first: **All 14 places** (default) records the decision for every place the issue affects; **Only this software** records it for one piece of software, which then keeps its own status. [ASSUMPTION] A later "All places" decision does not overwrite places that have their own status; the panel says how many keep theirs ("2 places keep their own status").

Each option shows the status chip it produces. **"Why? (shown in the audit report)"** is required for Not impacted, Mitigated and Risk accepted, optional for Fix planned. **Save and next ⌘↵** (lime) is disabled until a question is answered; it records the decision with author, timestamp and scope (FR14), updates the row's chip in place (Mixed when places now differ) and moves to the next issue in the current filter. If the save fails, the panel stays on the issue with the inline error and Try again; nothing is lost. **Decide later** moves on without recording. Hint under the actions: **"Saved with your name in the audit trail."** Decisions propagate to Home counts, Exposure, Software, exports and audit reports.

## State Patterns

The signature rule carries over: **the screen must never need a caveat it doesn't already show.** Every reassuring number is scoped to what was checked.

| State | Surface | Treatment |
|---|---|---|
| Empty (pre-setup) | Home | Title + the two setup actions that matter (connect a registry, install a cluster agent) with copy-paste one-liners in mono. No illustration. |
| Checking (first check or backlog) | Software, Home | {components.checking-band} with determinate progress ("3,176 of 3,847 checked (82%)") and an estimate in words; "You can keep working: numbers update as each one finishes." Names appear at once; counts fill in; skeletons only where data is missing; per-row step text ("Reading packages · step 2 of 3", "Waiting its turn"). Never blocks, never a spinner, never modal. |
| Cold load | All | shadcn `Skeleton` mirroring the real layout. |
| Partial answer | Exposure | Answer for what is checked, caveat line naming the unchecked ("2 pieces of software haven't been checked yet and aren't on the map. This answer covers the 3,176 we have checked."). |
| Empty answer (known vulnerability) | Exposure | Coverage-scoped zero, only for a vulnerability Armoury has data for: "No software has it — across the 3,176 pieces of software we've checked (82%)", with the unchecked remainder one click away. |
| Unknown vulnerability | Exposure | Armoury has no data for the queried ID: "Armoury has no data for <ID> yet. Vulnerability data updated <age> ago." with **Check again** (the view's lime action). No map, no zero, never "No software has it". |
| No query | Exposure (from the sidebar) | "Ask about a vulnerability, a package or a fingerprint." with examples ("CVE-2026-23012 · log4j-core@2.17.0 · sha256:…"); the query button opens ⌘K. |
| Nothing to review | Issues (filter at 0) | "No issues are waiting for review." plus the coverage scope ("That covers the 3,176 pieces of software we've checked; 671 are still waiting their turn.") and grey **Show all statuses**. |
| Search no match | Issues and list searches | "No issues match “<text>” with these filters." with grey **Clear search**; the filters stay as set. |
| Nothing yet | Reports | "No audit reports yet" with the lime **Generate audit report**; Exports: "No exports yet. Make one from Exposure, Issues or Software with Export." |
| Save failed | Review panel, Export, Generate audit report, Settings | {components.inline-error} in the panel names the problem and offers **Try again**. Save and next does not advance; the choices, scope and "Why?" text stay filled in. No toast. |
| Signature does not verify | Reports | {components.error-band} (clay-wash) in place of "Signature verified", naming the file and the reason ("The signature on pack.pdf does not verify: the file has changed since it was signed."). No download is hidden; a link opens the audit trail entry for the signing. |
| All clear | Home | "Nothing needs you today." with the scope sentence, stats (0 Need attention · 1,094 Open, all reviewed · 82% Checked), the severity line, grey See open issues, lime Audit report. No Issues badge. |
| Licences 0 | Issues, Home | Licences group hidden; the type filter still shows "Licences 0". |
| Stale source | Freshness strip, Home | The source's age turns amber with the age in words; the Home summary gains a scoped caveat. Air-gapped instances also show bundle age and an import-bundle action (FR10). |
| Registry unreachable | Software (and gap rows elsewhere) | {components.error-band}: what failed, since when, what it affects, what still works, likely cause. Lime **Try again** is the one lime action; **Add software** turns grey (secondary) while the band shows. Grey **Open connection settings**. Affected rows say "As of 14:02 · registry" in amber with a clock; nothing is removed. |
| Disconnected agent | Freshness strip, Software | "N clusters reporting"; that cluster's runtime data marked "as of", not removed. Heartbeat 30 s; stale after 5 min; disconnected after 60 min (Helm values). |
| Air-gapped mode | Global | [ASSUMPTION] Instance-level flag from deployment config; operator-key signing copy only; bundle-import affordances; no phone-home anywhere (NFR4). |
| Read-only auditor | Global | Review, Add software, Generate audit report and Settings mutations are absent, not disabled. Viewing, downloading and verifying audit reports fully available. Generation appears for auditors only when an admin enables `rbac.auditorCanGeneratePacks` (default off; NFR6). |
| Append-only history | Audit trail, History | No edit or delete on recorded decisions or trail entries; a correction is a new entry superseding the old, both visible (NFR11). "Entries are never edited or removed." |
| Audit report failure | Reports | Fails closed, naming the failing section; no partial report is delivered silently. Retry re-runs failed sections. |
| Palette no match | ⌘K | "No matches. Try a CVE ID, package@version or fingerprint." plus common actions. |
| Disabled | Buttons, pager | 0.45 opacity, not-allowed cursor; Save and next until a question is answered. |

## Long-running operations

Never an unexplained spinner, never modal, never blocking.

- **First check and backlogs** (minute 29, new registry): the Checking band (above). Progress is announced politely to screen readers.
- **Exposure queries** answer in seconds (NFR2). If a query is still running after 2 s, partial results render with a scope line ("Checking — 1,204 of 3,000 pieces of software so far"); worst case under a minute.
- **Check again** on a piece of software: the row and detail show step text until done.
- **Audit report generation** is asynchronous with visible progress. [ASSUMPTION] Minutes-scale; progress shown as report sections complete. The user can keep working; the report appears in Reports → Audit reports when signed.
- **Feed updates** re-evaluate stored package lists; no rescans, no rebuilds (NFR5). "Answered N min ago" and "How we know" say so.

## Interaction Primitives

**Keyboard-first, mouse as fallback, and still calm for people who never touch a shortcut.** Keys are shown, never required.

- `⌘K` / `Ctrl+K` — search or jump (universal). Also the sidebar field and the Exposure query button.
- `g` + letter — go to a surface; the letters show next to each nav item after pressing `G`. Letters for the renamed surfaces are open (see Open items).
- `J` / `K` — next / previous item in the list (shown at the end of the tab bar).
- `/` — focus the list search.
- `⌘↵` — Save and next in the review panel.
- `Esc` — close the topmost layer (palette); unpin the graph selection.
- Palette: `↑` `↓` move, `↵` open, `esc` close.
- From the prior spine: `x` export current view, `?` shortcut map. `t` (open triage drawer) and `e` (explore in graph) need new meanings (see Open items).
- **Single-key shortcuts** (`J`, `K`, `/`, `x`, `?`, `g` + letter) are active only when focus is not in a text field, and **can be turned off in Settings → Personal** (WCAG 2.1.4). Modified shortcuts (`⌘K`, `⌘↵`) stay on.
- Graph: arrows / `Tab` traverse nodes, `↵` opens detail, `+` / `−` zoom, Fit.

**Motion:** quiet. 0.16 s colour, background and shadow transitions on rows, tabs, nav, segments, buttons and fields; skeleton pulse. All motion is off under `prefers-reduced-motion`; progress then updates in steps with no information lost.

**Banned everywhere:** in-product notifications or toasts-as-alerts (signal leaves via the Prometheus endpoint only, FR20); badge counts for *new* findings; OIDC setup wizards (NFR6); edit/delete on evidence (NFR11); infinite scroll; modal stacks deeper than one (the ⌘K dialog is the only modal); hover-only affordances without a keyboard or focus equivalent; celebratory animation; a second lime action in a view.

## Theme

- **Light is the default; Dark is a second theme** ({colors.canvas} / {colors.canvas-dark} and every other `-dark` pair) with the same semantic roles, layout and density (`DESIGN.md` `-dark` tokens). Ink stays darkest in both; lime is unchanged; the focus ring is lime in dark.
- [ASSUMPTION] The switch lives in Settings → Personal and as a ⌘K action ("Switch theme…"). The prior spine's header switcher is gone with the header. The mock's top-right Light / Dark switch (no-JS radio pair) belongs to the presentation page, not the product.
- Applies instantly, no reload. Choice persists per user server-side (`user_preferences`, `GET`/`PUT /api/v1/me/preferences`, from the prior spine), so it follows the user across browsers.
- [ASSUMPTION] New users get Light regardless of OS setting; whether to follow `prefers-color-scheme` is not decided.
- The printed report never follows the app theme.

## Accessibility Floor

Contrast lives in `DESIGN.md` (both themes hold AA; lowest text pair 4.9:1).

- WCAG 2.2 AA across all surfaces, both themes — contractual for a B2B compliance audience. There is no separate high-contrast theme any more (the prior High Signal role).
- **Reflow and resize** (1.4.10, 1.4.4): below 1280px the sidebar becomes an icon rail; below 1024px list and detail stack in one column with a Back link, so 400% zoom (320 CSS px) and 200% text keep every function without horizontal scrolling. The Exposure map and wide tables may scroll in two directions as 2D content; their header, answer and inspector reflow.
- **Single-key shortcuts** are active only outside text fields and can be turned off in Settings → Personal (2.1.4).
- **Field edges** meet 3:1 at rest ({colors.field-border}, 1.4.11).
- Full keyboard operability; `Tab` order = reading order; visible focus ring on every interactive element ({colors.focus}; lime on the sidebar and on forest selection). Selected rows use `aria-current`; segmented controls use `aria-pressed`.
- **Never colour alone:** severity has its word and level marker; Actively exploited has its word and icon; review status has its word and icon; deployed vs not deployed has solid vs dashed **and** a label; stale has amber **and** a clock **and** the time in words; the selection changes text colour as well as fill.
- The graph has a full table equivalent (Graph/Table switch). The map has an `aria-label` summarising the answer; nodes are focusable with labels carrying name, tier and state.
- Hover hints ("Not seen running in any connected cluster.") are also reachable on focus.
- The ⌘K palette is a real modal dialog: focus trapped, returned on `Esc`; results announced via polite `aria-live`. Checking progress is a polite `role="status"`.
- Screen readers announce the surface on navigation using title + summary ("Issues — 3 need attention today").
- `prefers-reduced-motion` honoured globally.
- English-only UI in v1 with every string externalised from day 1; no concatenated sentences; no text baked into static SVG assets.

## Responsive & Platform

| Viewport | Behaviour |
|---|---|
| ≥ 1440px | The designed layout: 252px sidebar + list column + detail column. |
| 1280–1439px | Same three columns; the detail column absorbs the loss. |
| 1024–1279px | The sidebar becomes an **icon rail**: icons only, labels as tooltips and accessible names (tooltips also on focus), the search field as a ⌘K icon button, the user menu as the avatar. List and detail stay side by side. |
| < 1024px | Icon rail, and the list and detail **stack in one column**: the list fills the width; opening an item shows its detail with a **Back** link that returns to the list at the same place and selection. The URL is the same in both layouts. This is what 400% zoom at 1280px (320 CSS px) and 200% text resize reach. |

Web only; no native apps. Self-hosted means unpredictable enterprise browsers: last-2-versions evergreen baseline. Fonts are self-hosted (no network at view time).

## Printed report

Visual spec: `DESIGN.md` → Printed report (print-only light palette). Behaviour:

- Produced by Generate audit report (and printable exports); Preview in the product before download.
- The cover sheet comes first and states coverage at generation time ("3,176 of 3,847 checked (82%)"), listing the not-checked software rather than leaving it out — exactly as the product showed it that day.
- Plain labels with the technical term beside them; companions keep technical names (SBOM, VEX).
- Every page footer carries report ID, window, generation time and page number.
- No mock: one sample PDF is produced for review (prior spine: Story 9.3).

## Inspiration & Anti-patterns

- **Lifted — s.host server dashboard** ([imports/inspo-shost-server-dashboard.png](imports/inspo-shost-server-dashboard.png)), adopted whole: light canvas, black sidebar, one lime accent, deep green selection and charts, three-column master-detail, calm sparse cells, uppercase buttons.
- **Lifted — the prior final design's function:** the fastest way to find information. ⌘K, g-keys, pagination, coverage-gap rows, feed freshness, Exposure graph and table, graph inspector, review that keeps you in the list.
- **Lifted from Linear:** keyboard-first palette discipline.
- **Chosen — Greenhouse** out of eight directions (greenhouse, still-water, field-notes, calm-instruments, sumi, aurora-night, hybrid-forge-greenhouse, calm-console), finished in an Impeccable pass (greenhouse-final).
- **Rejected — hybrid "Greenhouse Instruments":** friendly but too much eye candy, and it lost the prior design's function.
- **Rejected — Compact density** ("horrible"). One density only.
- **Rejected — a quantified "chance of attack" (EPSS) rating:** users found it misleading. Actively exploited stays a yes/no.
- **Rejected — mixing severity, likelihood and review status in one list** (the "Fine 1,091" breakdown was confusing).
- **Rejected — jargon as primary labels** (KEV, EPSS, SBOM, blast radius, triage); **alarm red**; eyebrows and kickers; an undeclared system font.
- **Rejected — "ingredients"** (unprofessional), **"Undeployed"** (implies removal), **"Workaround in place"** (tacky).
- **Kept from the prior spine:** no Anchore-style setup ceremony; no Snyk-style fragmentation (one sidebar, one vocabulary, licences embedded); no alert-noise (no in-product notifications; signal exits via Prometheus).
- **Out of UI scope permanently:** runtime threat detection, auto-remediation, multi-scanner orchestration UI, a dedicated licence dashboard, reachability claims.

## Key Flows

### Flow 1 — UJ-1: The first 30 minutes (Priya, the only dedicated security engineer, post-audit)

1. Priya runs the `helm install` one-liner for the control plane and opens the URL.
2. She signs in with the **bootstrap admin** from her Helm values. SSO is never allowed to stand between her and minute 29; OIDC comes later via Helm values, never a UI wizard.
3. Empty **Home** offers exactly two actions: connect a registry, install a cluster agent. She pastes read-only registry credentials. [ASSUMPTION inherited from PRD: a single primary registry in the first session.]
4. **Software** fills: "3,847 pieces of software found. We're checking what's inside them." The Checking band shows "Checking 671 more pieces of software… about 2 h left"; names appear at once and counts fill in. She keeps working.
5. She runs the second one-line `helm install` for the cluster agent. The install affordance shows the exact RBAC first — read-only, watch/list, never cluster-admin (NFR9). "2 clusters reporting" appears on the freshness strip; software splits into Deployed and Not deployed.
6. **Climax — minute 29:** Home reads "You are in good shape. 3 things need attention today." Needs attention lists them; Open issues groups the rest by severity with Licences on top; "Checked 82% — 671 are waiting their turn" and the freshness strip sit on the same screen. The whole fleet in one place she doesn't have to caveat, because the screen already carries every caveat. Full checking completes within 24 h; the screen never pretended otherwise.

Failure: registry unreachable → Software shows the clay-wash band "We can't reach registry.acme.internal" with Try again and **Open connection settings**, which lands on **Settings → Connections**; affected rows read "As of 14:02"; Home carries a gap row naming the registry; nothing is removed.

### Flow 2 — UJ-2: CVE day (Priya, the logging-library CVE)

1. Her own Grafana alert, built on Armoury's Prometheus metrics, pings her; Armoury itself sent nothing.
2. From anywhere: `⌘K`, types the CVE ID (or "log4j"); the Exposure result "Where are we exposed to log4j-core?" is in the list; `↵`.
3. **Seconds later** (NFR2), **Exposure** answers: "14 pieces of software have it. 9 are deployed, 5 are not deployed." Actively exploited pill, KEV, Critical, CVSS 9.8, "Answered 38 min ago". The map draws Vulnerability → Package → Software → Where it runs, deployed solid and not deployed dashed. The caveat line scopes the claim: "2 pieces of software haven't been checked yet and aren't on the map." Feeds updated overnight and stored package lists were re-evaluated: no rescan, no rebuild (NFR5).
4. She switches to **Table** to scan where it runs, sorts by Deployed?, and back to Graph; payments-api stays selected. **Open software** shows its copies and audit trail in **Software**.
5. **Climax:** she presses **Export**. The CSV — carrying the same caveat and provenance — goes to the CTO before he's read the news, and is filed in **Reports → Exports**.
6. She reviews from the inspector (**Review**) into **Issues**: "Does this vulnerability impact us?" With **All 14 places** she records **Fix it** → Fix planned; then, for each of the two services that don't use the vulnerable code, **Only this software** → **Not impacted** with a reason. The row's chip reads **Mixed · 2 of 14**, and the issue leaves Needs attention because no place is Not reviewed yet. `⌘↵` saves and moves on; the list stays in view. If a save fails, the panel stays put with "Try again" and her answers intact.
7. Every decision is already in the audit trail with her name and time ("Saved with your name in the audit trail."). Nothing to write up later.

Failure: the CVE is in the news before the vulnerability data has it → "Armoury has no data for CVE-2026-23012 yet. Vulnerability data updated 41 min ago." with **Check again**; never "No software has it" for an ID Armoury doesn't know. A known vulnerability with nothing matching → the coverage-scoped zero ("No software has it — across the 3,176 pieces of software we've checked (82%)"), with the unchecked remainder one click away.

### Flow 3 — UJ-3: Audit day (Marta, compliance lead, read-only auditor)

1. Marta signs in with the read-only auditor role. Same sidebar, same words, same numbers; Review, Add software and Generate actions are simply absent.
2. Priya opens **Reports** and presses **Generate audit report**. Smart defaults take the last 12 months and the whole fleet; window, scope and framework stay adjustable afterwards (FR22). If an admin has enabled auditor generation, Marta can press it herself.
3. Generation runs in the background with progress. Marta reads the audit trail meanwhile (a software's Audit trail tab, an issue's History): every decision from CVE day is there, attributed, timestamped, never edited.
4. The report lands under **Audit reports**: "Production fleet · 12 Nov 2025 → 6 Nov 2026 · Signed". Overview shows "Signature verified", the signer key, and the `cosign verify-blob` command with Copy — "Auditors can run this themselves, without Armoury." Files: pack.pdf, package lists (SBOM), review decisions (VEX).
5. **Climax:** the report's first fact is its own coverage — "3,176 of 3,847 checked (82%)", with the 671 not checked listed, not left out. Three weeks of spreadsheet archaeology is now a signed document she downloads and hands over without a single hand-assembled appendix.

Failure: the window includes coverage gaps → the report discloses them exactly as the product showed them. Generation failure → fails closed naming the failing section; no partial report is delivered silently.

### Flow 4 — Tom Reid, Head of Engineering: the Monday one-minute check

1. Monday morning, Tom opens Armoury. It lands on **Home**; the sidebar shows **Issues 3**.
2. The line under the title answers the only question he came with: "You are in good shape. 3 things need attention today." "Last checked 38 min ago."
3. **Needs attention 3:** log4j-core 2.17.0 — Critical · Actively exploited · 14 places; AGPL-3.0 — Licence · Needs a decision · report-render; jackson-databind 2.15.2 — Critical · 3 places. No acronyms to decode.
4. The first item is open in the detail column: one plain sentence ("A vulnerability in a common logging library lets an attacker run their own code. People are using it in real attacks right now."), the fix ("Update to 2.17.2"), Review status "Not reviewed yet". The **Exposure** tab shows the short version — 14 pieces of software, 9 deployed — and its button opens the full **Exposure** page if he wants the map.
5. Below, **Across all software**: 82% checked, open issues down 247 in 30 days, the audit report signed and covering 82%. The freshness strip shows every source current.
6. **Climax — under a minute:** Tom knows we are in good shape, which three things need a decision, that the numbers are fresh and scoped to what was checked, and that the audit report is ready if anyone asks. Nothing on the screen alarmed him or needed translating. He presses **Review all 3** to work through them, or leaves them for Priya. [ASSUMPTION] Review all 3 opens the three Needs-attention issues in Issues, one after another.

Variation: on a quiet Monday Home reads "Nothing needs you today." with its scope sentence; the one lime action is the Audit report.
Failure: a source is stale → its age turns amber on the strip and the summary line carries a scoped caveat, so "good shape" is never claimed on old data.

### Coverage

| Surface | Flows that land there |
|---|---|
| Home | Flow 1 (climax), Flow 4 |
| Software | Flow 1 (steps 4–5), Flow 2 (step 4), Flow 3 (step 3) |
| Issues | Flow 2 (step 6), Flow 3 (step 3), Flow 4 (step 6) |
| Exposure | Flow 2, Flow 4 (step 4) |
| Reports | Flow 2 (step 5, Exports), Flow 3 |
| Settings | Flow 1 failure (Connections) |
| Help | None — no source defines Help (Open items) |

| Stated need (source) | Surface |
|---|---|
| "Are we safe, and what needs attention?" (memlog, Tom) | Home |
| Fastest way to find information (memlog, prior spine) | ⌘K, Exposure, Issues filters |
| Fleet posture at minute 29 (UJ-1, FR16) | Home, Software |
| Blast-radius answer in seconds, export to the CTO (UJ-2, FR17, FR19) | Exposure, Reports → Exports |
| Triage with justification, author, timestamp (UJ-2, FR14) | Issues review panel, audit trail |
| Signed audit pack, verifiable (UJ-3, FR21–25) | Reports |
| Artifact detail: SBOM, findings, provenance, running locations (FR18) | Software detail |
| Licence policy and findings (FR26–28) | Settings → Policy, Issues Licences group |
| Prometheus endpoint (FR20) | Settings → Signals |
| Optional CI scan: a pipeline submits a built artifact; the server scans it and decides pass or fail with the fleet CI policy; the step prints the verdict and a link to the artifact in Armoury; a known artifact is linked, not duplicated (FR31, NFR12) | Settings → Policy (CI policy), Settings → Access (CI tokens); the printed link lands on the piece of software in **Software**. How CI-submitted software is grouped and labelled, and where the verdict shows, is **open** (Open items) |
| VEX ingestion with vendor attribution (FR15) | **Gap** — no drawn surface (Open items) |
| Data-quality score (FR30) | **Gap** — no surface or token (Open items) |

## Changes from ux-Armoury-2026-06-12

For the downstream Correct Course.

- **Theme:** three dark-only themes (Forge default, High Signal, Gunmetal; "no light mode planned") → **Light default + one calm Dark theme** with the same roles, layout and density. High Signal's role as the built-in high-contrast option is gone (both themes hold AA). The header theme switcher is gone with the header; switching stays in Settings → Personal and ⌘K. Persistence in `user_preferences` is unchanged; the default for new users becomes Light.
- **Visual identity:** warm graphite + ember "workshop" → Greenhouse: black sidebar, light canvas, lime for the active nav item and the one primary action, forest for selection and charts. The ember accent, data-quality hue and success/warning roles are replaced by the token set in `DESIGN.md`.
- **Typography:** Inter Display + Inter + IBM Plex Mono for every identifier (76px hero numeral, 10px tracked micro-labels, eyebrows) → **IBM Plex Sans** for everything, Plex Mono only for IDs, fingerprints, commands and keys; nine sizes (12–40); no hero numeral, eyebrows or tracked-caps labels; sentence-case table headers; fonts embedded/self-hosted (OFL).
- **Navigation:** 58px icon rail with seven surfaces (Posture, Blast radius, Graph explorer, Artifacts, Findings, Evidence, Settings) plus a page header (breadcrumb, search, theme switcher) → a 252px labelled black **sidebar**: Home, Software, Issues, Exposure, Reports, Settings, **Help** (new). Graph explorer merges into Exposure; Evidence becomes Reports (audit reports + exports only); the page header becomes the sidebar search field. Page title equals the sidebar label plus a friendly summary line.
- **Layout:** rail + single full-width main column with full-width tables → **three-column master-detail** (sidebar · grouped list · tabbed detail).
- **Terminology:** the "locked glossary" (Artifact, Finding, Posture, Evidence pack, blast radius, triage; lowercase statuses; "never 'issue' or 'report'") → **plain labels first with the technical term small and grey** (glossary above). Statuses: **Not reviewed yet · Not impacted · Fix planned · Mitigated · Risk accepted**. KEV is shown as **"Actively exploited"**. Exports and audit reports keep the technical (VEX) terms. "Evidence pack" → "Audit report" in the UI. UI copy in British English ("Licences").
- **Ranking:** a single KEV-first, EPSS-weighted ranked list with the logic stated in the header (FR13) → **severity groups** Critical / High / Medium / Low with Actively exploited first in each group, and a **Licences group at the top, hidden at 0**. EPSS is **not shown as a rating** anywhere (raw value only in technical details). The PRD's FR13 wording ("KEV first, then EPSS-weighted severity") needs reconciling.
- **Severity and KEV visuals:** tinted uppercase severity chips and soft-opacity severity fills; KEV as a solid critical-hued tag ("nothing outranks it") → severity as **word + 4-step level marker**, no fills, no red; "Actively exploited" as **quiet text in lists, a pill in detail**; KEV as a small grey tag in detail views only.
- **Review:** slide-over triage drawer (`Sheet`, `t` to open) with status, justification and scope → **review panel in the Issues detail column** with **two plain questions**, "Why? (shown in the audit report)" required except for Fix planned, **Save and next ⌘↵**, **Decide later**, and a scope control (**All 14 places** by default, or **Only this software**). One "Review" action everywhere replaces separate status actions. Status chips: status-hued outlined pills → **neutral chips with drawn icons**, plus a neutral **Mixed · N of M** chip when places differ.
- **Responsive:** tolerant tablet degradation and best-effort read-only below 1024px → an **icon rail below 1280px** and **one stacked column with a Back link below 1024px**, fully operable (reflow at 400% zoom).
- **Density:** "dense within data zones", 30px table rows → **one comfortable density** (≈72–78px two-line rows). Compact was explored and rejected.
- **Home (was Posture):** hero numeral, co-stat band, severity band → page summary line, Needs attention, Open issues summary rows, an "Across all software" band (gauge, sparkline, audit report) and the freshness strip. **Needs attention** is new (rule agreed 2026-11-06). An **Issues nav badge** with the Needs-attention count is new; the prior ban on badge counts now applies to new-finding counts only.
- **Software (was Artifacts):** grouped **Deployed / Not deployed** (was running / shipped, not running) with pagination over the real fleet; detail tabs Overview · Issues · Packages · Audit trail.
- **Exposure (was Blast radius + Graph explorer):** answer in words first; graph restyled from ember-ringed, severity-hued rounded-rect nodes to a **hairline graph**: circular nodes, four sentence-case tiers, **deployed solid / not deployed dashed**, clay only on the vulnerability node. "Explore in graph" becomes See exposure / See the map. The digest layout becomes a fingerprint query.
- **Honesty states:** warning-tinted dashed coverage-gap rows and populating banner → plain "Not checked yet" rows and a paper **Checking band** with determinate progress; errors in a **clay-wash band**, never red; freshness strip in plain words (source names, technical term small, stale in amber) instead of mono feed versions in success/warning colours.
- **⌘K palette:** groups Answers → Navigate → Actions → Recent → **Issues · Software · Exposure · Actions**. `g`-key letters must change with the surface names; `t` and `e` need new meanings; `J`/`K` and `/` are added.
- **Opacity:** "no opacity dimming on any element with text" is kept, with one exception drawn in the approved mock: **disabled controls at 0.45**.
- **Shapes and depth:** 5–12px soft radii → 3–6px quiet radii (10px for the ⌘K dialog), pill only for the exploited pill; shadows only on the ⌘K dialog (no drawer).
- **Data-quality score (FR30):** the DQ badge, hue and Posture co-stat are **not carried into the approved design**; open (see below).
- **Primary users:** Priya and Marta, plus **Tom Reid, Head of Engineering**, as an equal-weight non-technical protagonist.

## Open items

Remaining assumptions:

1. [ASSUMPTION] The raw **EPSS** value lives only in the technical-details block and orders items within a severity group after the Actively exploited ones.
2. [ASSUMPTION] **"Vulnerability"** replaces "Weakness" in rows and detail (the decision log calls it easy to revert).
3. [ASSUMPTION] **Theme** switch placement (Settings → Personal and ⌘K) and **OS preference** (new users get Light; `prefers-color-scheme` not followed). Not decided.
4. [ASSUMPTION] **Review buttons outside Issues** (Home, Exposure inspector, Software) and **Review all 3** open the issue(s) in Issues on the Review tab.
5. [ASSUMPTION] **Print face** IBM Plex Sans (prior: Inter).
6. [ASSUMPTION] Settings' panel list sits in the list column.
7. [ASSUMPTION, inherited] Air-gapped mode is an instance-level flag; audit report generation is minutes-scale with section progress; UJ-1 has a single primary registry (PRD).
8. [ASSUMPTION, from the decision log] Surfaces for new scope (servers, live estate, K8s policy) are deferred and need Correct Course.
9. [ASSUMPTION] **Review scope details:** a later "All places" decision does not overwrite places that have their own status; the **Review status** filter matches an issue when any of its places has that status.

Not drawn in the final mock:

10. **Keyboard focus and g-key frame** (not drawn; no frame in the final mock shows it); the **g-key letters** for the new surfaces and new meanings for `t` / `e`.
11. **Home detail Exposure tab** (only the Overview's Exposure cell is drawn), **How to fix** and **Details** tabs.
12. **Issues detail Exposure and History tabs**; Software's Issues, Packages and Audit trail tabs (only Overview cells); Reports' Files and Audit trail tabs.
13. **Licence review:** the two questions are worded for vulnerabilities; the licence decision copy is not drawn.
14. **Vendor VEX claims with attribution** plus "the decision that applies now and its source" (FR15) — not in the review panel. (Review scope is decided: see The issue unit and Review flow.)
15. **"N more" rows** with the pager, Home **Open issues** row click behaviour, and the destination of **Add software**.
16. **Graph explorer traversal** beyond the query (re-centring on any node) and whether the full **freshness strip** also appears on Exposure and Software detail, as in the prior spine.
17. **⌘K "Recent"** group (prior) not drawn.
18. **Home Needs attention order** (drawn: exploited, licence, Critical) — not decided; the Licences-at-top rule covers the Issues list and the Open issues summary only.
19. **Audit report generation in progress:** the in-progress row in Audit reports, how window, scope and framework are adjusted after the click (FR22), and re-generation semantics.
20. **Behavioural rows not yet written** for the segmented control (URL, keyboard), table (sort keys, keyboard sort, default order), pager (does `J`/`K` cross pages), search fields (clear), technical details (always open or collapsible) and gauges and charts (text alternative); until then shadcn defaults apply.

Unresolved product questions and gaps:

21. **Data-quality score (FR30):** no surface, token or presentation in the new design.
22. **Help:** stays in the sidebar; the Help screen is deferred to a later UX update (decided 2026-11-06). The `?` shortcut map may belong there.
23. **Tom Reid's role** (analyst, admin or read-only) — the mock shows him with Review actions — and whether he is the PRD's CTO.
24. **High-contrast option:** with High Signal gone, confirm AA-only is acceptable.
25. **PRD FR13** wording (KEV first, then EPSS-weighted) vs severity grouping; PRD glossary terms vs plain labels.
26. **Mock housekeeping:** the stale header notes and the High 40 count were fixed in the mock on 2026-11-06. A few stylesheet contrast ratios differ slightly from computed values; the spine values win. The mock's lime avatar initials are not carried (DESIGN.md user menu).
27. **Optional CI scan (FR31) landing:** the PRD fixes only that the CI step prints the verdict and a link to the artifact in Armoury, and that a known artifact is linked, not duplicated. Not decided: how CI-submitted software that is in no connected registry (an uploaded image or package archive) is grouped in Software (it fits neither "Deployed" nor "Not deployed · Last deployed …"), the label that says where it came from, and where the CI verdict and its history show in Software detail.
28. **Unknown package or fingerprint:** the "no data yet" state covers vulnerability IDs; the copy for a `package@version` or fingerprint Armoury has never seen is not written.
29. **Conflicting decisions:** two people reviewing the same issue at once (for example "Changed by Marta at 14:05. Review again.") has no rule.
30. **Global states:** session expired and re-authentication; control plane unreachable (single instance, NFR10); a direct link to a Settings panel or action the role cannot use.
31. **Token hygiene for code generation:** several component tokens are composite strings (for example `'1px {colors.rule}'`) rather than atomic keys; some dimensions are untokenised (26px tab padding, 128px term column, 120px gauge, 56px sparkline, 84px disc, 660px palette, the icon-rail width); `button-label`, `mono-id` and `display-reserved` have no line height; `display-reserved` and `rounded.DEFAULT` are unreferenced.
32. **Printed report** content (cover sheet, footer, plain labels) is restated in both spines; visual rules should live in `DESIGN.md` and the content contract here, cross-linked.
33. **Retired label "Running":** the ban should read "Running as a group or status label", since the hint "Not seen running…" and the glossary's "Running replicas" use the word.
