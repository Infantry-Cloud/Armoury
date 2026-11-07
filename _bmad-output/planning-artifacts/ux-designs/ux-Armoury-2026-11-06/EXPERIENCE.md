---
name: Armoury
status: final
updated: 2026-11-07
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
- **Non-technical leaders** (Tom Reid, Head of Engineering in the mock, with the **Admin** role) who need to know "are we safe, and what needs attention" quickly.

One layout and one density serve both. Plain words lead; the technical term stays, small and grey.

**Roles** (unchanged): admin (configuration, connections), analyst (review, audit report generation), read-only auditor. Tom Reid has the **Admin** role (decided 2026-11-07). [ASSUMPTION] Admin can also do everything an analyst can, which is why Tom sees Review and Review all 3. Everything is operable by one security engineer alone — zero dev-team cooperation is a product gate.

## Information Architecture

**Black sidebar ({components.sidebar}), seven items**: Home · Software · Issues · Exposure · Reports, a divider, then Settings · Help. The sidebar is headed by a "Search or jump to… ⌘K" field and ends with the signed-in user's menu ({components.user-menu}). The active item is lime ({colors.lime}). Issues carries a badge with the Needs-attention count; at 0 there is no badge.

**The issue unit.** One Issues row is **one vulnerability (or one licence) in one package version** — for example log4j-core 2.17.0 × CVE-2026-23012 — across every place it affects ("14 places"). A review applies to **all places by default**; a different status can be set for **one piece of software**. The **issue-wide status** is the latest All places decision, or Not reviewed yet when there is none. Each place's own status is its "Only this software" decision if it has one, else the issue-wide status. When any place's own decision differs from the issue-wide status, the row's status chip reads **Mixed · N of M**: N places differ, of M places ("Mixed · 3 of 14"). When N equals M the chip reads **Mixed** with no count; its accessible name "All M places have their own status". An issue counts as Not reviewed yet, and can need attention, while **any** of its places is Not reviewed yet. Counts on every surface (312 not reviewed yet, 1,094 open, the badge) count issues, not places.

**Page title = sidebar label**, with a friendly summary line under it ("Issues" + "3 need attention today. 312 not reviewed yet."; "Exposure" + "Where are we exposed to log4j-core?").

**Three-column master-detail** on every surface: sidebar · list column (title, summary, filters, grouped list with counts, pager, the view's one primary action, {components.button-primary}) · tabbed detail column. Detail tabs ({components.tabs}) end with the position and keys ("1 of 3 · J K").

| Surface | URL (as drawn) | Purpose | Primary action |
|---|---|---|---|
| Home | `/` | Landing. "Are we safe, and what needs attention?" Fleet summary, coverage, freshness (FR16). | Review all 3 |
| Software | `/software/<name>` | The real fleet, grouped Deployed / Not deployed, with what we haven't checked said plainly (FR18). | Add software |
| Issues | `/issues?review=not-reviewed` | Every open issue — vulnerabilities and licences — grouped by severity; review without leaving the list (FR13, FR14, FR27). | Save and next |
| Exposure | `/exposure?q=log4j-core@2.17.0[&view=table]`; after a move `/exposure?q=software:acme/payments-api@sha256:9f2c41…&from=log4j-core@2.17.0` | Ask about a vulnerability, a package or a fingerprint; one answer as a map or a table (FR17, FR19). Absorbs the prior Blast radius and Graph explorer, including moving the map to any node. | Review (in the inspector); Open software when the map is centred on a piece of software |
| Reports | `/reports/<id>` | Audit reports, exports (both kept as evidence) and the fleet-wide audit trail, nothing else (FR19, FR21–25, NFR11). | Generate audit report |
| Settings | `/settings/<panel>` | Connections, sources, policy, access, signals, personal. | — |
| Help | — | Not designed (see Open items). | — |

### Home

- **List column:** "Home" + "You are in good shape. 3 things need attention today." + "Last checked 38 min ago".
  - **Needs attention N** — the issues that need someone today. Rule: *An issue needs attention when it is Not reviewed yet (in any place) AND it is Actively exploited OR Critical. Every licence violation that is Not reviewed yet also needs attention; licence warnings never do.* Rows use the standard row shape; right column is places ("14 places").
  - **Open issues N** — summary rows: **Licences** first (hidden at 0), then Critical (with "1 actively exploited"), High, Medium, Low, Negligible and Not rated yet (the last two hidden at 0), each with its count.
  - "312 not reviewed yet · 782 reviewed · See all" (See all opens Issues), then the lime **Review all 3**, which opens Issues with the Review status filter set to **Needs attention**; Save and next walks that set.
- **Detail column** (the selected issue): tabs **Overview · Exposure · How to fix · Details**.
  - Overview: title, the first sentence of the advisory description, as is, with its source (FR12) — no plain-language rewrite, and no sentence when there is no description (the mock's sentence is placeholder copy; the mock is not changed), severity, Actively exploited pill + KEV tag; Vulnerability (CVE ID), Found in, The fix, Review status; grey Review and See exposure; an Exposure cell (All / Deployed / Not deployed) listing the first places and "See all 14 on the map".
  - **Exposure tab:** a reduced summary of the Exposure page so people can scan it quickly, with a button that opens the full Exposure page for that query.
- **"Across all software" band** under the issue, clearly separate from it: Checked (82% gauge, "671 are waiting their turn"), Open issues (last 30 days, sparkline, "247 fewer"), Audit report (last 12 months, signed, coverage, Download / Preview).
- **No data-quality reading on Home** (decided 2026-11-07). The fleet-wide reading and its five parts live in Reports. It may be added to the Home Details tab later (Open items).
- **Freshness strip** at the bottom.

### Issues

- **Filters:** a type segmented control **All · Vulnerabilities · Licences** with counts (licence problems are not vulnerabilities; "Licences 0" stays visible in the filter); a **Review status** filter listing **Needs attention** (its count is the Needs-attention number) above all five statuses with counts, **default Not reviewed yet**; a search field ("Find a package or vulnerability", `/`); the ordering stated in words: "Actively exploited sorts first in each group".
- **Grouping:** **Licences** at the top (hidden when 0 — licence issues are rare and each needs a decision); the group holds licence violations and licence warnings, and a warning row says "Warning" on line 2 ("Licence · Warning · <where>") and never needs attention; then **Critical · High · Medium · Low**, then **Negligible** and **Not rated yet** (no severity in the vulnerability data), each hidden at 0. Within each group, Actively exploited items first; [ASSUMPTION] then ordered by the raw EPSS value, which is never shown as a rating. Long groups end with an "N more High" row.
- **Rows:** standard row shape, one row per issue (see The issue unit); right column is the review-status chip, or **Mixed · N of M** when places differ from the issue-wide status (see The issue unit).
- The **Review status** filter matches an issue when any of its places has that status (decided 2026-11-07), so a Mixed issue can appear under more than one status; counts are issues.
- **Pager:** "1–25 of 312 · page 1 of 13". Never infinite scroll.
- **Detail tabs: Review · Exposure · History.** Review holds the summary (title, severity, pill, KEV), Exposure count with "See the map", What to do, Review status, the **review panel** and the technical-details block. Exposure and History are not drawn (see Open items).

### Software

- "Software" + "3,847 pieces of software. 1,126 deployed, 2,721 not deployed." The **real fleet**, grouped **Deployed N** (row line 2: "prod-eu-west · 4 copies") and **Not deployed N** (line 2: "Last deployed 12 days ago" or "Never deployed"; hint "Not seen running in any connected cluster."). Right column: issue count ("2 issues").
- **Not checked yet 671** — the coverage-gap row, in place: "Counted above, but we haven't looked inside them yet, including 212 in prod-eu-west. Their issues are unknown, not absent."
- Pager "1–25 of 3,847 · page 1 of 154"; lime **Add software**.
- **Detail tabs: Overview · Issues · Packages · Audit trail**, with "Deployed" status at the bar's end. **Overview, in this order:**
  1. **Info** (left, tall): Name, Fingerprint (mono, copy), Runs in, Copies, Built, Last checked, **Data quality "91 A−"** ({components.dq-value}), Signed; grey Check again and Audit report. Beside it on the right, **Packages** ("214 packages · SBOM", Direct 37 / Indirect 177, licence and end-of-life lines) over **Where it runs** (each copy with zone).
  2. **Issues** full width ("2 open"): the issues side by side, Review under them.
  3. **Issues trend** chart ("Issues in payments-api · Last 30 days · from 9 to 2").
  4. **Data quality** ("How much you can trust these numbers"): the {components.quality-meter} with the weakest part and its one reason ("Package lists 82 — version missing for 6 indirect packages, so their issues can't be matched yet. See them") and the technical terms on one grey line.
  5. **Latest in the audit trail** at the bottom ("Entries are never edited or removed").
- **No grade in Software list rows:** a row has one right column (issues), and a grade would add a third subject to every row. Data quality lives in the detail.
- **Low grade** (legacy-ftp, "58 D"): see State Patterns.

### Exposure

- Header across the list and map: "Exposure" + the question ("Where are we exposed to log4j-core?"); the query button showing the subject (opens ⌘K to change the question); **Graph · Table** switch; grey Export and "Audit report for this answer".
- **The answer first, in words:** "14 pieces of software have it. 9 are deployed, 5 are not deployed." Meta: Actively exploited pill, KEV, Critical, CVSS 9.8, "Answered 38 min ago"; deployed/not-deployed split.
- **List column:** Deployed N, Not deployed N, then the "Not checked yet" gap row ("…so we can't say either way. They're not on the map. Next check in about 20 min.").
- **Graph:** four tiers — Vulnerability · Package · Software · Where it runs. Deployed solid, Not deployed dashed below a labelled rule. Legend, zoom (+ / − / Fit), and a caveat line under the map.
- **Inspector** under the map for the selected node: identity, How it got it, What to do (fix, review status), lime Review, grey Open software, "How we know".
- **Table:** the same answer, same order (deployed first), sortable sentence-case headers; selection carries across Graph and Table; "2 not checked yet, not listed".
- Queries accept a vulnerability ID, `package@version` or a fingerprint. A fingerprint query centres on that piece of software (prior digest layout).
- **Moving around the map** (the prior Graph explorer's traversal, kept inside Exposure). One rule for every node: **click or `Enter` on a node moves the map to that node** and adds a step to the trail.
  - **Ego view:** the new centre sits in the true centre of the map. What it contains is on the left (its packages and their vulnerabilities); where it runs and its copies are on the right. The node you came from carries a "Came from here" marker. Packages with no known issues roll up into one node ("212 more packages · No known issues"; caveat: "Showing the 2 packages with issues. The other 212 have none and sit in one group; Packages in Software lists them all.").
  - **Trail** directly above the map once it has moved: Back, the previous steps as link chips, the current step in bold, and the key hints "↵ Move the map · ⌫ Back". Back, `Backspace`, any step in the trail or the browser's Back button returns to that map with its selection.
  - **The centre drives everything:** the question ("What is in payments-api 3.4.1, and where does it run?"), the query field, the answer line ("payments-api 3.4.1 has 2 open issues. It runs in 1 place, with 4 copies."), Export, "Audit report for this answer" and the URL (`/exposure?q=software:acme/payments-api@sha256:9f2c41…&from=log4j-core@2.17.0`) all follow the current centre, so the view can be shared and reloaded.
  - **List column** follows the centre too: Issues 2, Where it runs 1, Packages 214.
  - Asking a new question with **⌘K starts a new trail**.
  - **Table** lists the centre's neighbours: its issues, the packages they come from and where it runs. The selection carries across Graph and Table.
  - **Inspector** for a software centre adds Issues ("2 open: 1 Critical, 1 Low"); the one lime action is **Open software**; **Show only this** stays grey; hint "Click any node to move the map to it. Enter does the same from the keyboard."
  - [ASSUMPTION] The ego view is drawn for a piece of software only; for a package, vulnerability or place centre the same rule applies (contents on the left, where it is used and runs on the right), but those layouts are not drawn (Open items).
- **No query** (`/exposure` from the sidebar): the answer slot asks "Ask about a vulnerability, a package or a fingerprint." with examples ("CVE-2026-23012 · log4j-core@2.17.0 · sha256:…"); the query button opens ⌘K.
- **Unknown vulnerability:** when the vulnerability data (Grype DB, the database Armoury matches against) has no record for the queried ID — even if the CVE List or another source already lists it — the answer reads "Armoury has no data for <ID> yet. Vulnerability data updated <age> ago." with **Check again**. It never says "No software has it" for an ID it doesn't know. A **known** vulnerability with no matches gets the coverage-scoped zero (State Patterns).

### Reports

- **Audit reports N**, **Exports N** and **Audit trail**, nothing else (Audit trail added 2026-11-07, Correct Course D9). New report types (for example a management summary) are new scope and need Correct Course first.
- **Exports are stored as evidence** (decided 2026-11-07): every CSV made with Export in **Exposure, Issues or Software** is stored in Reports with an **audit-trail entry** (who, when, from which view and query) and the **same retention as audit reports** (24 months, never below the floor, FR23). They are listed under **Reports → Exports**, newest first. Export rows say what and where from ("Exposure: log4j-core 2.17.0 · CSV · 14 rows · from Exposure · 6 Nov"). "Exports are kept for 24 months, like audit reports. Make a new one from Exposure, Issues or Software with Export." Like audit reports, stored exports are never edited or removed by hand.
- **Audit trail** (fleet-wide, decided 2026-11-07): every ledger entry, newest first — type, subject (plain label with its technical ID small), actor, time, tool and feed versions — with filters by type, subject and time window and the pager. Its detail column shows the chain verification ("Chain intact — N entries, verified 4 min ago", or the first broken entry), the latest signed checkpoint, and the anchoring status (mode, latest anchored checkpoint, pending anchors). Per-item trails stay as tabs (a software's Audit trail, an issue's History, a report's Audit trail), each linking to this group filtered to that subject. Not drawn yet (Open item 36).
- Lime **Generate audit report**.
- **Detail tabs: Overview · Files · Audit trail**, with "Generated today, 08:31, by …" at the bar's end. Overview: title, lead and Download all / Preview; **row 1: Coverage when it was made | Signature** ({components.signature-status}: verified in product, plus the copyable `cosign verify-blob` command in a {components.code-block}: "Auditors can run this themselves, without Armoury."; when it does not verify, see State Patterns); **row 2: Data quality, full width** ("Data quality 84 B+ when it was made": the fleet-wide {components.quality-meter}, the weakest part with its reason — "Extra sources 78 — one of three extra sources had no answer for 412 packages; those use the main vulnerability data only." — and the technical terms on one grey line); then Files (pack.pdf, sboms.tar.gz "Package lists … SBOM", vex.json "review decisions … VEX") and What it says. This is the only place the fleet-wide five-part breakdown appears in the product.
- The **printed cover page** carries the same reading (see Printed report).

### Settings

Spine-only (no mock), carried from the prior spine. An in-page panel list (in the list column) with one route per panel, `/settings/<panel>`, so links (for example "Sources" on the freshness strip, "Open connection settings" on an error) open a panel directly. Panels: **Connections** (registries FR1, package feeds FR29, agent install) · **Sources** (feed status and history, bundle import FR10, end-of-life data FR33) · **Policy** (licence policy FR27, signature policy — trusted keys and keyless signer identities FR32, CI policy, retention — never below the 24-month floor, FR23) · **Access** (users and roles, resolved auth configuration read-only, CI tokens) · **Signals** (Prometheus endpoint, read-only with copy, FR20; signing key) · **Personal** (theme, keyboard shortcuts including the switch that turns single-key shortcuts off). Edit controls are absent for roles without write access. OIDC is declarative (env vars / Helm values), never a UI wizard (NFR6).

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
| Reports | Evidence packs, exports and the evidence trail | Docs; file names (`pack.pdf`) |
| Audit report | Evidence pack (CRA pack) | File names and the verification command. Exception: "Audit report for this answer" (Exposure) is the PDF answer report, not an evidence pack; it is stored under Reports → Exports (Correct Course D3) |
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
| Data quality | Data-quality score (FR30) | Docs, PRD; the score and letter ("91 A−") need no technical term |
| Package lists (data-quality part) | SBOM depth | Grey "In technical terms" line under the meter; `title` attribute; small beside the name on the printed cover page |
| Coverage (data-quality part) | Scan coverage | Same as above |
| Freshness (data-quality part) | Feed freshness | Same as above |
| Extra sources (data-quality part) | Enrichment | Same as above |
| Vulnerability records (data-quality part) | CVE record quality | Same as above |
| Check again | Rescan | — (on Exposure's "no data yet" answer, Check again re-asks the question against the latest vulnerability data; no rescan) |
| Vulnerability data · Exploited list · Packages · Sources | Vulnerability feed (Grype DB) · KEV catalog · SBOM index · feeds | Freshness strip (small term) and "How we know: Syft v… · Grype DB v…" |
| Review / Review status | Triage / triage status | Docs |
| Not reviewed yet | untriaged | Exports, audit report, VEX |
| Needs a decision | Licence-policy violation, untriaged | Second line of a licence row that is Not reviewed yet ("AGPL-3.0 — Licence · Needs a decision · report-render") |
| Warning | Licence-policy warning (`license_warning`; the policy marks the licence "warning", including unknown licences by default) | Second line of a licence warning row ("<licence> — Licence · Warning · <where>"); never counts toward Needs attention |
| Mixed · N of M | Per-product triage status differs | Status chip on an issue where N places have their own decision that differs from the issue-wide status; VEX states each product's own status (its own decision, else the All places decision) |
| Not impacted | not affected | VEX (vex.json), audit report |
| Fix planned | fix planned | VEX, audit report |
| Mitigated | mitigated | VEX, audit report |
| Risk accepted | accepted | VEX, audit report |
| Why? | Justification | VEX, audit report |
| Severity: Critical / High / Medium / Low / Negligible / Not rated yet | CVSS severity (Not rated yet: Grype "Unknown", no severity) | "CVSS 9.8" in the answer meta and technical details |
| (not shown) | EPSS | Raw value only in the grey technical-details block. Never a rating, tag or column. |

UI copy is British English ("Licences"). **Retired labels** (must not appear): Posture, Findings, Blast radius, Graph explorer, Artifacts, Evidence, triage, Things to look at, Where it's affected, Weakness, ingredients, What's inside, Chosen by your team, Came along with them, Running, Shipped not running, Undeployed, Being attacked in the wild, chance of attack, Doesn't affect us, Fixed for now, Workaround in place, Mark reviewed, Plan the fix, Skip.

## Component Patterns

Behavioural. Visual specs live in `DESIGN.md` Components.

| Component | Use | Behavioural rules |
|---|---|---|
| Sidebar | Global | One item per surface; active state mirrors the route. The search field opens ⌘K. Issues badge = Needs-attention count; no badge at 0. It is a count of what needs a decision, not a new-findings notification. |
| Grouped list (List row, Group heading, Pager) | Home, Issues, Software, Exposure, Reports | {components.list-row} under {components.group-heading}; {components.pager}. Groups with counts; one row shape (name + version · severity · actively exploited · where · one right column). Click or `J`/`K` selects and fills the detail column; the list keeps its place. Groups too long for the page end in an "N more …" row. Pagination at 25 per page, never infinite scroll (NFR3 scale). |
| Needs attention | Home, Issues summary, sidebar badge | An issue needs attention when it is Not reviewed yet (in any place) AND it is Actively exploited OR Critical. Every licence violation that is Not reviewed yet also needs attention; licence warnings never do. A Mixed issue stays in Needs attention until none of its places is Not reviewed yet. The same number everywhere it appears. |
| Severity groups | Issues, Home "Open issues" | Licences group first and hidden at 0; then Critical, High, Medium, Low, Negligible, Not rated yet (the last two hidden at 0); Actively exploited first within each. The sort is stated in words above the list (explainable ordering, FR13). |
| Actively exploited marker | Rows, detail, Exposure, palette | **Text in lists, pill in detail**: quiet clay text with icon ({components.exploited-text}) in list rows and palette results; filled pill ({components.exploited-pill}) in detail panels and the Exposure answer; {components.kev-tag} only in detail views. Never dropped when a row truncates. |
| Review status filter | Issues | **Needs attention** (with the Needs-attention count, the same number as Home and the badge) above the five statuses with counts; default Not reviewed yet. An issue matches a status when any of its places has it. Home's Review all N opens this filter on Needs attention. Never mixed with the severity groups. |
| Review panel | Issues detail (Review tab) | Options are {components.review-option} rows; the reason is a {components.review-note-field}. A **scope** control sits above the questions: **"All 14 places"** (default) or **"Only this software"**, which asks which piece of software (pre-filled when Review was opened from a piece of software). Replaces the prior slide-over triage drawer; the list stays visible. See [Review flow](#review-flow). Status changes happen only here, never inline, because a decision needs its reason. **Save failure:** an {components.inline-error} line in the panel names the problem and offers **Try again**; Save and next does not advance; the chosen options, scope and "Why?" text stay filled in. |
| Status chip | Every row and detail that shows a decision | {components.status-chip}. Five statuses, each with its icon and word, plus **Mixed · N of M** (own icon, neutral) when any place's own decision differs from the issue-wide status (the latest All places decision, or Not reviewed yet when there is none); N is the number of those places, M the number of places. Accessible name in full ("Mixed: 3 of 14 places have a different status"). When N equals M the chip reads **Mixed** with no count, accessible name "All M places have their own status". Reflects each place's own status: its "Only this software" decision if it has one, else the All places decision. |
| Review action | Home, Exposure inspector, Software Issues cell | One "Review" action replaces "Plan the fix" and "Mark reviewed". Outside Issues it opens that issue in Issues on its Review tab (decided 2026-11-07). Home's **Review all N** opens Issues with the Needs attention filter. |
| Coverage-gap row | Software, Exposure (list and table), Home band | {components.coverage-gap-row}. Sits where the missing data would be, names the count and where ("including 212 in prod-eu-west"), says "unknown, not absent". Not dismissible, not collapsible; it disappears only when the gap closes. Click-through to the cause (unchecked software, unreachable registry, disconnected agent). |
| Exposure answer | Exposure | Answer in words first, then the map or table. Every answer carries its caveat line for unchecked software and "Answered N min ago" / "How we know". Feed updates re-evaluate stored package lists; answers are current with no rescan (NFR5). |
| Exposure graph | Exposure | {components.exposure-graph} with {components.inspector} and {components.table}. Graph and Table are two readings of one answer; selection carries across. Hover, arrows or `Tab` highlight a node's direct path and show it in the inspector; `Esc` unpins. **Click or `Enter` on any node moves the map to that node** (ego view: the centre in the true centre, what it contains on the left, where it runs and its copies on the right; the node you came from marked "Came from here") and adds a step to the trail. Roll-up nodes ("8 more", "212 more packages") expand. Nodes resolve to their detail through the inspector (Open software). |
| Exposure trail | Exposure (after the first move) | {components.exposure-trail}. Records each move as a step. **Back**, `Backspace` (outside text fields) or the browser's Back button goes back one step; any earlier step goes back to that map with its selection. The query field, answer line, Export, "Audit report for this answer" and the URL always follow the current centre; each move updates the URL (`&from=` the previous step), so a trail can be shared and reloaded. Asking a new question with ⌘K starts a new trail. Table lists the centre's neighbours. The trail is a `nav` named "How you got here"; the current step has `aria-current="location"`. |
| Data-quality value | Software detail Info list, Reports detail heading, printed cover page | {components.dq-value}. One reading per subject: the score out of 100 and its letter ("91 A−"). Software shows its own; Reports and the cover page show the fleet's at generation time ("84 B+ when it was made"). **Not on Home and not in list rows.** [ASSUMPTION] Grade bands (which scores earn which letter, and that D and below counts as low) are a placeholder until the scoring model exists. |
| Quality meter | Software detail (Data quality cell), Reports detail (Data quality row) | {components.quality-meter}. Five parts, each out of 100: Package lists, Coverage, Freshness, Extra sources, Vulnerability records. Only the weakest part is emphasised and explained in one sentence, with a link when there is a way to act ("See them"); at a low grade the weakest parts (at most two) each get a sentence and a grey **Check again** appears. Technical terms appear once, on the grey line, and in each name's `title` attribute; the list has an accessible name ("Data quality 91, grade A−, in five parts, each out of 100"). The fleet-wide breakdown appears only in Reports. |
| Home Exposure tab | Home detail | Reduced summary of the Exposure page for the selected issue; a button opens the full Exposure page for that query. |
| Export | Exposure, Issues, Software | CSV of the current view (on a moved Exposure map, of the current centre). **Stored as evidence:** lands in Reports → Exports with an audit-trail entry (who, when, from which view and query) and the same retention as audit reports (24 months). Carries the same caveats and provenance as the screen ("The 2 not checked yet travel with the CSV and the audit report"). A failed export shows the inline error with Try again. |
| Audit report generator | Reports, ⌘K | One click on Generate audit report with smart defaults (last 12 months, whole fleet); window, scope and framework adjustable after the click, not a wizard (FR22). Asynchronous with progress. Signed with cosign using the operator key by default; keyless only when enabled, never when air-gapped. PDF + package lists (SBOM) + review decisions (VEX). |
| Signature status | Reports | {components.signature-status}. "Signature verified" with the signer key in the product, plus the copyable offline command (FR25). When it does not verify: see State Patterns. |
| Code block | Empty Home setup, agent install, Reports, Settings → Signals, Software fingerprint | {components.code-block}. **Copy** copies the whole command, never a truncated one; the label changes to "Copied" for 2 s and is announced politely (`aria-live`). Copy is keyboard reachable; the command text is selectable. |
| Inline error | Review panel, Export, Generate audit report, Settings panels | {components.inline-error}. A failed save or start shows one line where the action was taken, naming the problem in plain words, with **Try again**. Nothing advances or closes; every entered value stays. Announced with `role="alert"`. Not a toast. Clears on a successful retry. |
| User menu | Sidebar foot | {components.user-menu}. Shows the signed-in name and role; opens a menu with **Personal settings** (Settings → Personal) and **Sign out**. Keyboard: `Enter`/`Space` opens, arrows move, `Esc` closes and returns focus. |
| Freshness strip | Home | {components.freshness-strip}. Each source and its age; stale turns amber with the age in words. "Sources" opens Settings → Sources. Exposure and Software detail carry provenance inline ("Answered 38 min ago", "How we know", "Last checked"). |
| Tabs | Detail column | Counts in tabs ("Exposure 14", "Packages 214"). Position and keys at the bar's end. |
| ⌘K palette | Global | {components.command-palette}. Search or jump: results grouped Issues · Software · Exposure · Actions; the first result is the best match; `↵` opens; the dialog traps focus, dims the page, never navigates on its own, and returns focus on `Esc`. Typing a CVE ID, `package@version` or fingerprint routes to an Exposure answer. Every action is invocable here (Review, Export, Generate audit report, Switch theme). `?` opens the palette on a **Keyboard shortcuts** view listing every shortcut (no other dialog). |
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

Each option shows the status chip it produces. **"Why? (shown in the audit report)"** is required for Not impacted, Mitigated and Risk accepted, optional for Fix planned. **Save and next ⌘↵** (lime) is disabled until a question is answered; it records the decision with author, timestamp and scope (FR14), updates the row's chip in place (Mixed when places now differ) and moves to the next issue in the current filter (after Review all N, the next issue that needs attention). If the save fails, the panel stays on the issue with the inline error and Try again; nothing is lost. **Decide later** moves on without recording. Hint under the actions: **"Saved with your name in the audit trail."** Decisions propagate to Home counts, Exposure, Software, exports and audit reports.

## State Patterns

The signature rule carries over: **the screen must never need a caveat it doesn't already show.** Every reassuring number is scoped to what was checked.

| State | Surface | Treatment |
|---|---|---|
| Empty (pre-setup) | Home | Title + the two setup actions that matter (connect a registry, install a cluster agent) with copy-paste one-liners in mono. No illustration. |
| Checking (first check or backlog) | Software, Home | {components.checking-band} with determinate progress ("3,176 of 3,847 checked (82%)") and an estimate in words; "You can keep working: numbers update as each one finishes." Names appear at once; counts fill in; skeletons only where data is missing; per-row step text ("Reading packages · step 2 of 3", "Waiting its turn"). Never blocks, never a spinner, never modal. |
| Cold load | All | shadcn `Skeleton` mirroring the real layout. |
| Partial answer | Exposure | Answer for what is checked, caveat line naming the unchecked ("2 pieces of software haven't been checked yet and aren't on the map. This answer covers the 3,176 we have checked."). |
| Empty answer (known vulnerability) | Exposure | Coverage-scoped zero, only for a vulnerability the vulnerability data (Grype DB) has a record for: "No software has it — across the 3,176 pieces of software we've checked (82%)", with the unchecked remainder one click away. |
| Unknown vulnerability | Exposure | The vulnerability data (Grype DB) has no record for the queried ID, even if the CVE List or another source lists it: "Armoury has no data for <ID> yet. Vulnerability data updated <age> ago." with **Check again** (the view's lime action). No map, no zero, never "No software has it". |
| No query | Exposure (from the sidebar) | "Ask about a vulnerability, a package or a fingerprint." with examples ("CVE-2026-23012 · log4j-core@2.17.0 · sha256:…"); the query button opens ⌘K. |
| Nothing to review | Issues (filter at 0) | "No issues are waiting for review." plus the coverage scope ("That covers the 3,176 pieces of software we've checked; 671 are still waiting their turn.") and grey **Show all statuses**. |
| Search no match | Issues and list searches | "No issues match “<text>” with these filters." with grey **Clear search**; the filters stay as set. |
| Nothing yet | Reports | "No audit reports yet" with the lime **Generate audit report**; Exports: "No exports yet. Make one from Exposure, Issues or Software with Export." |
| Save failed | Review panel, Export, Generate audit report, Settings | {components.inline-error} in the panel names the problem and offers **Try again**. Save and next does not advance; the choices, scope and "Why?" text stay filled in. No toast. |
| Signature does not verify | Reports | {components.error-band} (clay-wash) in place of "Signature verified", naming the file and the reason ("The signature on pack.pdf does not verify: the file has changed since it was signed."). No download is hidden; a link opens the audit trail entry for the signing. |
| All clear | Home | "Nothing needs you today." with the scope sentence, stats (0 Need attention · 1,094 Open, all reviewed · 82% Checked), the severity line, grey See open issues, lime Audit report. No Issues badge. |
| Licences 0 | Issues, Home | Licences group hidden; the type filter still shows "Licences 0". |
| Low data-quality grade | Software detail, Reports detail, cover page | [ASSUMPTION: D and below, placeholder bands] The score and letter turn quieter in {colors.dq-muted} ("58 D"), keep their number and letter, and never turn clay, amber or red: a reading, not a threat. The meter names the two weakest parts, each with what it means ("Package lists 24 — this image was built without package details, so 41 files couldn't be matched to a package. Their issues are unknown, not absent."), and offers a grey **Check again** — a low grade is not the view's main job, so it takes no lime. |
| Moved map | Exposure | The map is centred on the node that was clicked or entered; the trail shows how you got there; header, answer, list, Export, audit report and URL describe the centre. Packages with no known issues roll up with a caveat line saying so. |
| Stale source | Freshness strip, Home | The source's age turns amber with the age in words; the Home summary gains a scoped caveat. Air-gapped instances also show bundle age and an import-bundle action (FR10). |
| Registry unreachable | Software (and gap rows elsewhere) | {components.error-band}: what failed, since when, what it affects, what still works, likely cause. Lime **Try again** is the one lime action; **Add software** turns grey (secondary) while the band shows. Grey **Open connection settings**. Affected rows say "As of 14:02 · registry" in amber with a clock; nothing is removed. |
| Disconnected agent | Freshness strip, Software | "N clusters reporting"; that cluster's runtime data marked "as of", not removed. Heartbeat 30 s; stale after 5 min; disconnected after 60 min (Helm values). |
| Air-gapped mode | Global | [ASSUMPTION] Instance-level flag from deployment config; operator-key signing copy only; bundle-import affordances; no phone-home anywhere (NFR4). |
| Read-only auditor | Global | Review, Add software, Generate audit report and Settings mutations are absent, not disabled. Viewing, downloading and verifying audit reports fully available. Generation appears for auditors only when an admin enables `rbac.auditorCanGeneratePacks` (default off; NFR6). |
| Append-only history | Audit trail, History, Reports | No edit or delete on recorded decisions, trail entries, audit reports or stored exports; a correction is a new entry superseding the old, both visible (NFR11). "Entries are never edited or removed." |
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

- `⌘K` / `Ctrl+K` — search or jump (universal). Also the sidebar field and the Exposure query button. On Exposure, a new question starts a new trail.
- `g` + letter — go to a surface; the letters show next to each nav item after pressing `G`. Letters for the renamed surfaces are open (see Open items).
- `J` / `K` — next / previous item in the list (shown at the end of the tab bar).
- `/` — focus the list search.
- `⌘↵` — Save and next in the review panel.
- `Esc` — close the topmost layer (palette); unpin the graph selection.
- Palette: `↑` `↓` move, `↵` open, `esc` close.
- From the prior spine: `x` export current view. `?` opens the ⌘K palette on its **Keyboard shortcuts** view (no new modal); Settings → Personal lists the same map. `t` (open triage drawer) and `e` (explore in graph) need new meanings (see Open items).
- **Single-key shortcuts** (`J`, `K`, `/`, `x`, `?`, `g` + letter, `Backspace` on the Exposure map) are active only when focus is not in a text field, and **can be turned off in Settings → Personal** (WCAG 2.1.4). Modified shortcuts (`⌘K`, `⌘↵`) stay on.
- Graph: arrows / `Tab` move between nodes first; **click or `↵` on a node moves the map to it** (and adds a step to the trail); `Backspace` or the trail's Back goes back one step, as does the browser's Back button; `+` / `−` zoom, Fit; `Esc` unpins. The node's detail opens from the inspector (Open software). Key hints sit at the right end of the trail: "↵ Move the map · ⌫ Back".

**Motion:** quiet. 0.16 s colour, background and shadow transitions on rows, tabs, nav, segments, buttons and fields; skeleton pulse. **One authored moment:** when the Exposure map moves, the centre node's outer ring scales in once (0.62 → 1, 200 ms ease-out); nothing else animates on a move. All motion is off under `prefers-reduced-motion` (the ring is simply drawn); progress then updates in steps with no information lost.

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
- The graph has a full table equivalent (Graph/Table switch). The map has an `aria-label` summarising the answer (after a move, the centre and what sits on each side, including the node you came from); nodes are focusable with labels carrying name, tier and state. The trail is a `nav` ("How you got here") with the current step marked `aria-current="location"`; [ASSUMPTION] moving the map puts focus on the new centre and announces the new answer politely.
- **Data quality** never relies on colour: the score and letter are always printed, the weakest part is named in words with its reason, the meter list has an accessible name, and each part's technical term is on a visible grey line as well as in its `title` attribute. Low grades use {colors.dq-muted} at ≥ 4.9:1.
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
- **Data quality** comes second on the cover sheet, before Signature and before any finding: "84 B+", the same five parts with plain names and the technical term small beside each, and "Lowest part: Extra sources (78). …" — the same reading as Reports detail at generation time. Coverage, then data quality: what was checked, then how much to trust it.
- The cover sheet ends with Signature (the operator key and the `cosign verify-blob` line anyone can run) and a sign-off line (name and role, date).
- Plain labels with the technical term beside them; companions keep technical names (SBOM, VEX).
- Every page footer carries report ID, window, generation time and page number.
- The cover page is drawn (Audit report — cover page frame); the remaining pages are not: one sample PDF is produced for review (prior spine: Story 9.3).

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
5. **Following the map:** back on Exposure she clicks payments-api (or presses `Enter` on it). The map moves: payments-api sits in the centre, its two vulnerable packages and their vulnerabilities on the left (log4j-core marked "Came from here"), prod-eu-west/payments and its 4 copies on the right. The header now asks "What is in payments-api 3.4.1, and where does it run?" and answers "payments-api 3.4.1 has 2 open issues. It runs in 1 place, with 4 copies."; the URL follows. The trail above the map reads Back · log4j-core 2.17.0 › **payments-api 3.4.1**; `Backspace` or the log4j-core step takes her back to the CVE answer with payments-api still selected.
6. **Climax:** she presses **Export** on the log4j-core answer. The CSV — carrying the same caveat and provenance — goes to the CTO before he's read the news, and is stored in **Reports → Exports** as evidence, with an audit-trail entry under her name.
7. She reviews from the inspector (**Review**) into **Issues**: "Does this vulnerability impact us?" With **All 14 places** she records **Fix it** → Fix planned; then, for each of the two services that don't use the vulnerable code, **Only this software** → **Not impacted** with a reason. The row's chip reads **Mixed · 2 of 14**, and the issue leaves Needs attention because no place is Not reviewed yet. `⌘↵` saves and moves on; the list stays in view. If a save fails, the panel stays put with "Try again" and her answers intact.
8. Every decision is already in the audit trail with her name and time ("Saved with your name in the audit trail."). Nothing to write up later.

Failure: the CVE is in the news before the vulnerability data has it → "Armoury has no data for CVE-2026-23012 yet. Vulnerability data updated 41 min ago." with **Check again**; never "No software has it" for an ID Armoury doesn't know. A known vulnerability with nothing matching → the coverage-scoped zero ("No software has it — across the 3,176 pieces of software we've checked (82%)"), with the unchecked remainder one click away.

### Flow 3 — UJ-3: Audit day (Marta, compliance lead, read-only auditor)

1. Marta signs in with the read-only auditor role. Same sidebar, same words, same numbers; Review, Add software and Generate actions are simply absent.
2. Priya opens **Reports** and presses **Generate audit report**. Smart defaults take the last 12 months and the whole fleet; window, scope and framework stay adjustable afterwards (FR22). If an admin has enabled auditor generation, Marta can press it herself.
3. Generation runs in the background with progress. Marta reads the audit trail meanwhile (Reports → Audit trail for the whole fleet, or a software's Audit trail tab, an issue's History): every decision from CVE day is there, attributed, timestamped, never edited.
4. The report lands under **Audit reports**: "Production fleet · 12 Nov 2025 → 6 Nov 2026 · Signed". Overview shows "Signature verified", the signer key, and the `cosign verify-blob` command with Copy — "Auditors can run this themselves, without Armoury." Files: pack.pdf, package lists (SBOM), review decisions (VEX).
5. **Climax:** the report's first fact is its own coverage — "3,176 of 3,847 checked (82%)", with the 671 not checked listed, not left out — and its second is how much to trust it: "Data quality 84 B+", five parts, the lowest one explained, on the screen and on the printed cover page alike. Three weeks of spreadsheet archaeology is now a signed document she downloads and hands over without a single hand-assembled appendix.

Failure: the window includes coverage gaps → the report discloses them exactly as the product showed them. Generation failure → fails closed naming the failing section; no partial report is delivered silently.

### Flow 4 — Tom Reid, Head of Engineering: the Monday one-minute check

1. Monday morning, Tom opens Armoury, signed in with the **Admin** role. It lands on **Home**; the sidebar shows **Issues 3**.
2. The line under the title answers the only question he came with: "You are in good shape. 3 things need attention today." "Last checked 38 min ago."
3. **Needs attention 3:** log4j-core 2.17.0 — Critical · Actively exploited · 14 places; AGPL-3.0 — Licence · Needs a decision · report-render; jackson-databind 2.15.2 — Critical · 3 places. The labels are plain.
4. The first item is open in the detail column: the first sentence of the advisory description, as published, with its source, the fix ("Update to 2.17.2"), Review status "Not reviewed yet". The **Exposure** tab shows the short version — 14 pieces of software, 9 deployed — and its button opens the full **Exposure** page if he wants the map.
5. Below, **Across all software**: 82% checked, open issues down 247 in 30 days, the audit report signed and covering 82%. The freshness strip shows every source current.
6. **Climax — under a minute:** Tom knows we are in good shape, which three things need a decision, that the numbers are fresh and scoped to what was checked, and that the audit report is ready if anyone asks. Nothing on the screen alarmed him, and the labels were plain. As an Admin he can press **Review all 3** to work through them, or leave them for Priya. Review all 3 opens Issues filtered to Needs attention, and Save and next walks those three.

Variation: on a quiet Monday Home reads "Nothing needs you today." with its scope sentence; the one lime action is the Audit report.
Failure: a source is stale → its age turns amber on the strip and the summary line carries a scoped caveat, so "good shape" is never claimed on old data.

### Coverage

| Surface | Flows that land there |
|---|---|
| Home | Flow 1 (climax), Flow 4 |
| Software | Flow 1 (steps 4–5), Flow 2 (step 4), Flow 3 (step 3) |
| Issues | Flow 2 (step 7), Flow 3 (step 3), Flow 4 (step 6) |
| Exposure | Flow 2 (moving the map: step 5), Flow 4 (step 4) |
| Reports | Flow 2 (step 6, Exports), Flow 3 (step 3, Audit trail; data quality: step 5) |
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
| Artifact signature verification (FR32) | Software detail Info "Signed"; Settings → Policy (signature policy). Words for each signature state not written (Open item 38) |
| End-of-life data for packages (FR33) | Software detail Packages cell and tab; Settings → Sources. End-of-life lines other than "No package is past its end of life." not written (Open item 38) |
| Prometheus endpoint (FR20) | Settings → Signals |
| Optional CI scan: a pipeline submits a built artifact; the server scans it and decides pass or fail with the fleet CI policy; the step prints the verdict and a link to the artifact in Armoury; a known artifact is linked, not duplicated (FR31, NFR12) | Settings → Policy (CI policy), Settings → Access (CI tokens); the printed link lands on the piece of software in **Software**. How CI-submitted software is grouped and labelled, and where the verdict shows, is **open** (Open items) |
| VEX ingestion with vendor attribution (FR15) | **Gap** — no drawn surface (Open items) |
| Data-quality score (FR30) | Software detail (Info list and Data quality cell), Reports detail (Data quality row), printed cover page. Not on Home (may join the Home Details tab later, Open items); not in list rows |
| Follow the graph from any node (prior Graph explorer) | Exposure (moving the map, trail, Back) |
| Exports kept as evidence (FR19) | Reports → Exports (audit-trail entry, audit-report retention) |

## Changes from ux-Armoury-2026-06-12

For the downstream Correct Course.

- **Theme:** three dark-only themes (Forge default, High Signal, Gunmetal; "no light mode planned") → **Light default + one calm Dark theme** with the same roles, layout and density. High Signal's role as the built-in high-contrast option is gone (both themes hold AA). The header theme switcher is gone with the header; switching stays in Settings → Personal and ⌘K. Persistence in `user_preferences` is unchanged; the default for new users becomes Light.
- **Visual identity:** warm graphite + ember "workshop" → Greenhouse: black sidebar, light canvas, lime for the active nav item and the one primary action, forest for selection and charts. The ember accent and success/warning roles are replaced by the token set in `DESIGN.md`; the data-quality hue becomes the blue-violet {colors.dq} with {colors.dq-muted} for low grades and {colors.print-dq} in print.
- **Typography:** Inter Display + Inter + IBM Plex Mono for every identifier (76px hero numeral, 10px tracked micro-labels, eyebrows) → **IBM Plex Sans** for everything, Plex Mono only for IDs, fingerprints, commands and keys; nine sizes (12–40); no hero numeral, eyebrows or tracked-caps labels; sentence-case table headers; fonts embedded/self-hosted (OFL).
- **Navigation:** 58px icon rail with seven surfaces (Posture, Blast radius, Graph explorer, Artifacts, Findings, Evidence, Settings) plus a page header (breadcrumb, search, theme switcher) → a 252px labelled black **sidebar**: Home, Software, Issues, Exposure, Reports, Settings, **Help** (new). Graph explorer merges into Exposure, with its traversal kept (moving the map to any node); Evidence becomes Reports (audit reports, exports and, from 2026-11-07, the fleet-wide audit trail); the page header becomes the sidebar search field. Page title equals the sidebar label plus a friendly summary line.
- **Layout:** rail + single full-width main column with full-width tables → **three-column master-detail** (sidebar · grouped list · tabbed detail).
- **Terminology:** the "locked glossary" (Artifact, Finding, Posture, Evidence pack, blast radius, triage; lowercase statuses; "never 'issue' or 'report'") → **plain labels first with the technical term small and grey** (glossary above). Statuses: **Not reviewed yet · Not impacted · Fix planned · Mitigated · Risk accepted**. KEV is shown as **"Actively exploited"**. Exports and audit reports keep the technical (VEX) terms. "Evidence pack" → "Audit report" in the UI. UI copy in British English ("Licences").
- **Ranking:** a single KEV-first, EPSS-weighted ranked list with the logic stated in the header (FR13) → **severity groups** Critical / High / Medium / Low with Actively exploited first in each group, and a **Licences group at the top, hidden at 0**. EPSS is **not shown as a rating** anywhere (raw value only in technical details). The PRD's FR13 wording ("KEV first, then EPSS-weighted severity") needs reconciling.
- **Severity and KEV visuals:** tinted uppercase severity chips and soft-opacity severity fills; KEV as a solid critical-hued tag ("nothing outranks it") → severity as **word + 4-step level marker**, no fills, no red; "Actively exploited" as **quiet text in lists, a pill in detail**; KEV as a small grey tag in detail views only.
- **Review:** slide-over triage drawer (`Sheet`, `t` to open) with status, justification and scope → **review panel in the Issues detail column** with **two plain questions**, "Why? (shown in the audit report)" required except for Fix planned, **Save and next ⌘↵**, **Decide later**, and a scope control (**All 14 places** by default, or **Only this software**). One "Review" action everywhere replaces separate status actions. Status chips: status-hued outlined pills → **neutral chips with drawn icons**, plus a neutral **Mixed · N of M** chip when places differ.
- **Responsive:** tolerant tablet degradation and best-effort read-only below 1024px → an **icon rail below 1280px** and **one stacked column with a Back link below 1024px**, fully operable (reflow at 400% zoom).
- **Density:** "dense within data zones", 30px table rows → **one comfortable density** (≈72–78px two-line rows). Compact was explored and rejected.
- **Home (was Posture):** hero numeral, co-stat band, severity band → page summary line, Needs attention, Open issues summary rows, an "Across all software" band (gauge, sparkline, audit report) and the freshness strip. **Needs attention** is new (rule agreed 2026-11-06). An **Issues nav badge** with the Needs-attention count is new; the prior ban on badge counts now applies to new-finding counts only.
- **Software (was Artifacts):** grouped **Deployed / Not deployed** (was running / shipped, not running) with pagination over the real fleet; detail tabs Overview · Issues · Packages · Audit trail.
- **Exposure (was Blast radius + Graph explorer):** answer in words first; graph restyled from ember-ringed, severity-hued rounded-rect nodes to a **hairline graph**: circular nodes, four sentence-case tiers, **deployed solid / not deployed dashed**, clay only on the vulnerability node. "Explore in graph" becomes See exposure / See the map. The digest layout becomes a fingerprint query. The Graph explorer's **traversal is kept inside Exposure**: click or Enter on any node moves the map there (ego view), with a trail, Back and a URL that follow the centre; ⌘K starts a new trail.
- **Honesty states:** warning-tinted dashed coverage-gap rows and populating banner → plain "Not checked yet" rows and a paper **Checking band** with determinate progress; errors in a **clay-wash band**, never red; freshness strip in plain words (source names, technical term small, stale in amber) instead of mono feed versions in success/warning colours.
- **⌘K palette:** groups Answers → Navigate → Actions → Recent → **Issues · Software · Exposure · Actions**. `g`-key letters must change with the surface names; `t` and `e` need new meanings; `J`/`K` and `/` are added.
- **Opacity:** "no opacity dimming on any element with text" is kept, with one exception drawn in the approved mock: **disabled controls at 0.45**.
- **Shapes and depth:** 5–12px soft radii → 3–6px quiet radii (10px for the ⌘K dialog), pill only for the exploited pill; shadows only on the ⌘K dialog (no drawer).
- **Data-quality score (FR30): carried over, with a new presentation.** The DQ badge, hue and Posture co-stat are gone; instead a small violet reading (score + letter, "91 A−") in the Software detail Info list, a five-part **quality meter** (Software detail, Reports detail) with only the weakest part emphasised and explained, a data-quality block on the printed cover page, and a quieter muted violet for low grades, never red. **Not on Home** and not in list rows.
- **Exports (FR19):** exports are **stored in Reports as evidence** — CSV from Exposure, Issues and Software, each with an audit-trail entry and the same retention as audit reports. FR19 needs rewording to match.
- **Software detail:** Overview reordered: Info beside Packages over Where it runs; Issues full width; Issues trend; Data quality; Latest in the audit trail last. **Reports detail:** Coverage beside Signature, then Data quality full width.
- **Primary users:** Priya and Marta, plus **Tom Reid, Head of Engineering** (Admin role), as an equal-weight non-technical protagonist.
- **Correct Course 2026-11-07 (sprint-change-proposal-2026-11-07.md):** licence warnings show in the Licences group with the word "Warning" and never count toward Needs attention (D8); Reports gains the fleet-wide Audit trail group (D9); "Signed" and end-of-life data are v1 scope as PRD FR32 and FR33, with their settings in Policy and Sources (D10); "Audit report for this answer" is the PDF answer report, stored under Exports (D3).

## Open items

Remaining assumptions:

1. [ASSUMPTION] The raw **EPSS** value lives only in the technical-details block and orders items within a severity group after the Actively exploited ones.
2. [ASSUMPTION] **"Vulnerability"** replaces "Weakness" in rows and detail (the decision log calls it easy to revert).
3. [ASSUMPTION] **Theme** switch placement (Settings → Personal and ⌘K) and **OS preference** (new users get Light; `prefers-color-scheme` not followed). Not decided.
4. **Resolved 2026-11-07** (readiness blocker 6): Review buttons outside Issues (Home, Exposure inspector, Software) open the issue in Issues on its Review tab; **Review all 3** opens Issues with the Review status filter on **Needs attention**, and Save and next walks that set.
5. [ASSUMPTION] **Print face** IBM Plex Sans (prior: Inter).
6. [ASSUMPTION] Settings' panel list sits in the list column.
7. [ASSUMPTION, inherited] Air-gapped mode is an instance-level flag; audit report generation is minutes-scale with section progress; UJ-1 has a single primary registry (PRD).
8. [ASSUMPTION, from the decision log] Surfaces for new scope (servers, live estate, K8s policy) are deferred and need Correct Course.
9. [ASSUMPTION] **Review scope details:** a later "All places" decision does not overwrite places that have their own status. (Decided 2026-11-07: the **Review status** filter matches an issue when any of its places has that status.)
10. **Resolved 2026-11-07:** admin includes the analyst's actions (PRD NFR6, roles are ordered; architecture: each operation declares a minimum role), which is why Tom Reid (Admin) sees Review and Review all 3.
11. [ASSUMPTION] **Data-quality grade bands** (which score earns which letter, and that D and below counts as a low grade shown in {colors.dq-muted}) are a placeholder until the scoring model exists. The five parts and their plain names are fixed; their weights are not.
12. [ASSUMPTION] **Moving the Exposure map:** focus goes to the new centre and the new answer is announced politely; the ego layout for a package, vulnerability or place centre follows the drawn software rule (contents left, where it is used and runs right).

Not drawn in the final mock:

13. **Keyboard focus and g-key frame** (not drawn; no frame in the final mock shows it); the **g-key letters** for the new surfaces and new meanings for `t` / `e`; the layout of the ⌘K palette's **Keyboard shortcuts** view (opened with `?`).
14. **Home detail Exposure tab** (only the Overview's Exposure cell is drawn), **How to fix** and **Details** tabs. **Data quality on Home** is decided against for now (2026-11-07); it may be added to the Home **Details** tab later, which needs its own UX update.
15. **Issues detail Exposure and History tabs**; Software's Issues, Packages and Audit trail tabs (only Overview cells); Reports' Files and Audit trail tabs, and the **detail of a stored export** (Reports → Exports row selected: file, who, when, from which query, its audit-trail entry).
16. **Licence review:** the two questions are worded for vulnerabilities; the licence decision copy is not drawn.
17. **Vendor VEX claims with attribution** plus "the decision that applies now and its source" (FR15) — not in the review panel. (Review scope is decided: see The issue unit and Review flow.)
18. **"N more" rows** with the pager, Home **Open issues** row click behaviour, and the destination of **Add software**.
19. **Moved Exposure map for other centres:** only a software centre is drawn ("Exposure — moved to payments-api"); centres on a package, a vulnerability other than the query, a place or a roll-up node, a long trail (how many steps show before they collapse), and the Table view of a moved map are not drawn. Whether the full **freshness strip** also appears on Exposure and Software detail, as in the prior spine, is also open.
20. **⌘K "Recent"** group (prior) not drawn.
21. **Home Needs attention order** (drawn: exploited, licence, Critical) — not decided; the Licences-at-top rule covers the Issues list and the Open issues summary only.
22. **Audit report generation in progress:** the in-progress row in Audit reports, how window, scope and framework are adjusted after the click (FR22), and re-generation semantics.
23. **Behavioural rows not yet written** for the segmented control (URL, keyboard), table (sort keys, keyboard sort, default order), pager (does `J`/`K` cross pages), search fields (clear), technical details (always open or collapsible) and gauges and charts (text alternative); until then shadcn defaults apply.

Unresolved product questions and gaps:

24. **Help:** stays in the sidebar; the Help screen is deferred to a later UX update (decided 2026-11-06). `?` opens the ⌘K palette's Keyboard shortcuts view, not Help (decided 2026-11-07).
25. **High-contrast option:** with High Signal gone, confirm AA-only is acceptable.
26. **Resolved 2026-11-07** (Correct Course): PRD FR13 now describes the severity groups; the PRD glossary gains UI labels; FR19 says exports are stored as evidence with evidence-pack retention.
27. **Mock housekeeping:** the stale header notes and the High 40 count were fixed in the mock on 2026-11-06. A few stylesheet contrast ratios differ slightly from computed values; the spine values win. The mock's lime avatar initials are not carried (DESIGN.md user menu). The mock's graph labels use 11.5, 12.5 and 13.5px SVG text; product graph labels use the nine sizes.
28. **Optional CI scan (FR31) landing:** the PRD fixes only that the CI step prints the verdict and a link to the artifact in Armoury, and that a known artifact is linked, not duplicated. Not decided: how CI-submitted software that is in no connected registry (an uploaded image or package archive) is grouped in Software (it fits neither "Deployed" nor "Not deployed · Last deployed …"), the label that says where it came from, and where the CI verdict and its history show in Software detail.
29. **Unknown package or fingerprint:** the "no data yet" state covers vulnerability IDs; the copy for a `package@version` or fingerprint Armoury has never seen is not written.
30. **Conflicting decisions:** two people reviewing the same issue at once (for example "Changed by Marta at 14:05. Review again.") has no rule.
31. **Global states:** session expired and re-authentication; control plane unreachable (single instance, NFR10); a direct link to a Settings panel or action the role cannot use.
32. **Data quality before a score exists:** what Software detail shows for a piece of software that is Not checked yet or still checking (no score yet), and how a score is explained when the scoring model changes.
33. **Token hygiene for code generation:** several component tokens are composite strings (for example `'1px {colors.rule}'`) rather than atomic keys; some dimensions are untokenised (26px tab padding, 128px term column, 120px gauge, 56px sparkline, 84px disc, 660px palette, the icon-rail width, the 164px meter name column); `button-label`, `mono-id` and `display-reserved` have no line height; `display-reserved`, `rounded.DEFAULT` and `colors.dq-wash` are unreferenced by any component.
34. **Printed report** content (cover sheet, footer, plain labels) is restated in both spines; visual rules should live in `DESIGN.md` and the content contract here, cross-linked.
35. **Retired label "Running":** the ban should read "Running as a group or status label", since the hint "Not seen running…" and the glossary's "Running replicas" use the word.
36. **Reports → Audit trail** (D9) is not drawn: the list rows, the filters, the verification cell, the checkpoint and anchoring cells, and the broken-chain state.
37. **Licence warning row** (D8): the "Warning" word's exact placement and style (proposed: line 2 in {colors.text-2}, never amber or clay); and the review-panel copy for warnings (with Open item 16).
38. **Signed and end-of-life words** (FR32, FR33): the words for each signature state other than "Yes" (not signed, signed by an untrusted signer, check failed, not checked for this type, no signature policy); end-of-life lines other than "No package is past its end of life."; the Signature policy panel and the end-of-life source in Settings.
39. **"Audit report for this answer"** (D3): confirm the label, since "Audit report" otherwise means an evidence pack.
