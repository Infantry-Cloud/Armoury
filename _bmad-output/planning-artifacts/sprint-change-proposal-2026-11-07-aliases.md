---
status: approved
approved: 2026-11-07 — Daniel approved the whole proposal ("Yes, apply it"); N5 and N7 answered
applied: 2026-11-07 — all 60 section-4 edits (P1, R1–R8, E1–E13, S1–S24, U1–U14) plus N5-a..e and N7-a..d applied; 0 failed; dry run in sync (11 epics, 79 stories)
follow-up: 2026-11-07 — three lines aligned with the N5 answer by hand (Story 6.2 zero AC, UX-DR40, EXPERIENCE "Empty answer (known vulnerability)").
date: 2026-11-07
workflow: bmad-correct-course (batch)
trigger: implementation-readiness.md second rerun 2026-11-07 FAIL (narrow) — 1 new blocker (blocker 9, vulnerability ID aliases) plus cheap concerns; evidence in readiness-2026-11-07/rerun-1-blocker-closure.md (concerns 1–5) and rerun-2-fresh-gate.md (finding 1 blocker; findings 14, 18, 20, 29)
scope: moderate — blocker 9 is closed by one data rule (Grype `--by-cve`, a key ID, every alias stored and matched) recorded in the architecture, ARCH7, ARCH38 and ten story bodies; the cheap concerns are closed by wording, one decided lookup method and four story gates. No FR, NFR, epic or story is added, removed, renumbered or renamed; no code exists. It is more than Minor because it changes the stored finding model and matching behaviour across four owner documents (PM, Architect, UX, PO/Dev) and ten Linear story bodies; it is not Major because there is no replan and no scope change.
memlog_numbering: 'memlog N = line N of ux-designs/ux-Armoury-2026-11-06/.memlog.md (125 lines). The three decisions behind this proposal are its last three lines, 123–125. Line 125 holds the four cheap-concern decisions (A3–A6).'
decisions:
  - "A1 Vulnerability ID aliases: Armoury runs Grype with `--by-cve`. The issue key (the vulnerability ID of a finding group) is the CVE ID when the vulnerability has one, else the original ID (GHSA, OSV or distro ID). Every alias of the vulnerability is stored with its finding. KEV matching, the enrichment joins (EPSS, CNA, OSV), Exposure queries, the unknown-vulnerability check and ⌘K search match on any alias, so a CVE query and a GHSA query find the same issue. The UI shows the key ID; the other aliases appear in the technical-details block (memlog 123)"
  - "A2 Vendor VEX claims (Story 5.7) are display-only: shown in the review panel with their source; they never set the issue status, counts, filters or Needs attention until a person records a decision. Emitted VEX states only people's decisions (memlog 124)"
  - "A3 Readiness-record open questions Q1, Q2, Q4 and Q5 (sprint-change-proposal-2026-11-07-readiness.md section 6) are gated in their stories by an explicit planning AC: Q1 → 6.3; Q2 → 2.10 and 4.4; Q4 → 2.10; Q5 → 5.2 and 5.4. Q5 loses its walk-order part, which the architecture already decides (memlog 125)"
  - "A4 The unknown-vulnerability check asks the Grype DB with `grype db search --vuln <ID>` (the loaded DB through the Grype CLI; Armoury never reads its SQLite schema) (memlog 125)"
  - "A5 The Needs attention count (badge, Home, the Issues filter option) ignores the Issues type filter and search; it is always the fleet-wide number (memlog 125)"
  - "A6 The rule that a later All places decision keeps per-software decisions is decided (architecture.md, Issues and review); the stale [ASSUMPTION] tags in Story 5.8, UX-DR16 and EXPERIENCE are removed and Open item 9 is closed (memlog 125)"
---

# Sprint Change Proposal — vulnerability ID aliases and the cheap readiness concerns (2026-11-07)

This proposal applies Daniel's decisions A1–A6 (frontmatter; memlog 123–125) to the PRD, the
architecture, `epics.md` and the two UX spines. It decides nothing else. Details the decisions leave
open are listed in section 6. The other readiness concerns from the second rerun stay with their owners
in `implementation-readiness.md`. Story 1.1's CI concerns ("fast tier", the Skaffold `ci` profile) are
not edited here; they go to the Story 1.1 Build re-plan (section 5).

Edit notation used in section 4:

- Each edit has an ID, a location (heading and **current** line number), `OLD` and `NEW` text, and a
  one-line rationale ("Why"). The decision it applies is in brackets after the line number.
- `OLD: ⟦…⟧` is an exact substring of the current file and is replaced by `NEW: ⟦…⟧`.
- `OLD (line starts): ⟦…⟧` means the whole line that starts with that text is replaced.
- `OLD (anchor, kept): ⟦…⟧` means the anchor stays and `NEW` is inserted directly after it (a NEW that
  starts on a new line is inserted as new lines).
- Every OLD quote was checked mechanically against the current files on 2026-11-07: each is found
  exactly once, on the stated line (checker: `/tmp/cc6/check_old.py`).
- Domain, data and API terms (`untriaged`, `all_places`, `artifact`, finding group, KEV, VEX, Grype DB,
  `--by-cve`) stay where they name data or APIs; UI words follow the EXPERIENCE glossary.
- Edit ID prefixes: P = PRD, R = architecture, E = `epics.md` front matter and requirements,
  S = `epics.md` stories, U = UX spines. "A1–A6" always means the decisions, never an edit.

## 1. Issue summary

**Problem.** The second readiness rerun after `sprint-change-proposal-2026-11-07-readiness.md` closed
blockers 1–8 but failed narrowly on 2026-11-07 with one new blocker: **blocker 9, vulnerability ID
aliases**. Issues are keyed on one vulnerability ID, but nothing says which one. Grype reports the
original ID by default (GHSA for language packages; `--by-cve` is optional), while KEV, enrichment and
Exposure use CVE IDs. Because the Grype DB holds the CVE record, the unknown rule (B4) does not fire, and
a CVE query against GHSA-keyed findings answers "No software has it" — the CVE-day false zero that FR17
and NFR8 forbid. The rerun also listed cheap concerns: ungated open questions, vendor VEX claims outside
the status rule, no recorded Grype DB lookup method, the Needs attention count versus the type filter and
search, and a stale [ASSUMPTION] in Story 5.8.

**Type.** A missing data rule and small gaps found before implementation (a readiness gate), not a change
of direction.

**How it was found.** Two independent read-only lenses (`readiness-2026-11-07/rerun-1-blocker-closure.md`,
`rerun-2-fresh-gate.md`); verdict in `implementation-readiness.md` → "Second rerun". Daniel chose: fix
blocker 9 (CVE first, keep all aliases), gate and record the cheap concerns, make vendor VEX claims
display-only, then rerun (memlog 123–125).

**Evidence (current lines).**

| # | Gap | Evidence | Lens |
|---|---|---|---|
| 9 (blocker) | One vulnerability ID keys an issue, but the ID scheme is not recorded; Grype's default is the original ID; KEV, enrichment and Exposure use CVE IDs; with B4 a CVE query on GHSA-keyed findings gives a false zero. | `architecture.md:257`, `:282`, `:336`; `epics.md:165` (ARCH38), `:782–783` (2.4), `:932` (2.10 "CVE ID in mono"), `:1254`, `:1258` (4.3), `:1738`, `:1750` (6.2); `grype --help` (0.120.1): "`--by-cve` orient results by CVE instead of the original vulnerability ID when possible" | rerun-2 finding 1 |
| C-a | Readiness-record Q1, Q2, Q4 and Q5 name a gating story, but no story AC carries the gate; Q5 still lists the walk order that the architecture decides. | `sprint-change-proposal-2026-11-07-readiness.md:808`, `:809`, `:811`, `:812`; `epics.md:926–938`, `:1278–1295`, `:1523–1535`, `:1581–1597`, `:1773–1784`; `architecture.md:257` ("in the same order") | rerun-1 concerns 1, 2, 4, note 6; rerun-2 finding 14 |
| C-b | Vendor VEX claims are outside the effective-status rule; counts, filters, Needs attention and emitted VEX are undefined once Story 5.7 lands. | `architecture.md:203`, `:257`; `epics.md:55`, `:1670–1672`, `:1680`; `EXPERIENCE.md:500` | rerun-2 finding 18 |
| C-c | No method is recorded for asking the Grype DB whether it "has a record" for an ID. | `architecture.md:282` ("never reads the Grype SQLite schema"), `:336`; `epics.md:1759`; `grype db search --help` (0.120.1): "Search for affected packages by vulnerability ID: `grype db search --vuln …`" | rerun-2 finding 20 |
| C-d | The Needs attention filter option must show the badge's number, but nothing says whether it follows the type filter and search. | `epics.md:234` (UX-DR38), `:1528–1530`; `EXPERIENCE.md:70`, `:207`; `architecture.md:257` | rerun-1 concern 3 |
| C-e | "A later All places decision keeps per-software decisions" is decided in the architecture but still an [ASSUMPTION] in UX and stories. | `architecture.md:257`; `epics.md:203`, `:1697`; `EXPERIENCE.md:241`, `:489` | rerun-1 concern 5; rerun-2 finding 29 |

## 2. Impact analysis

### Epic impact

| Epic | Impact |
|---|---|
| 2 Inventory | Story 2.4 runs Grype with `--by-cve` and stores the key ID and every alias (A1); Story 2.10 shows the key ID (A1) and gains the Q2 and Q4 gates (A3). |
| 4 Enrichment | Story 4.3 joins KEV and EPSS on any alias (A1); Story 4.4 joins CVE List and OSV on any alias, lists aliases in technical details (A1) and gains the Q2 precedence gate (A3). |
| 5 Review | Stories 5.2 (Q5 gate, fleet-wide count — A3, A5), 5.4 (Q5 gate, aliases in technical details — A1, A3), 5.7 (display-only vendor claims — A2), 5.8 (stale [ASSUMPTION] — A6). |
| 6 Exposure | Stories 6.2 and 6.3: queries and the unknown check match any alias (A1); 6.2 records the lookup method (A4); 6.3 gains the Q1 gate (A3). |
| 1, 3, 7–11 | No change. Story 1.8 cites UX-DR6 (edited by E7), but routes vulnerability IDs only "once Story 6.3 lands"; no 1.8 AC changes. Story 11.4's use of vendor VEX in the CI verdict is not decided here (N7). |

No epic is added, removed, renumbered or reordered. No epic summary changes.

### Story impact

- **Changed acceptance criteria (10):** 2.4, 2.10, 4.3, 4.4, 5.2, 5.4, 5.7, 5.8, 6.2, 6.3.
- **Retitled, added or removed:** none. `sprint-status.yaml` needs no change (every affected key keeps its
  title).
- **Story in flight:** none. Story 1.1 has a draft spec (Revision 1, never approved).

### Artifact conflicts

| Artifact | Conflict | Edits |
|---|---|---|
| `prd.md` | The glossary's Issue entry defines issue identity ("one vulnerability … in one package version") without saying which ID identifies a vulnerability (A1). FR15 says vendor claims are "applied … with attribution", not that they set status, so it is not edited (A2 condition). FR10, FR12 and FR17 need no change. | P1 |
| `architecture.md` | Grype invocation (A1); finding-group key and alias rule (A1); vendor claims and the status rule (A2); unknown rule and lookup method (A1, A4); Needs-attention count (A5) | R1–R8 |
| `epics.md` front matter and requirements | amendments list; ARCH7, ARCH38; UX-DR6, 16, 22, 38, 40 | E1–E13 |
| `epics.md` stories | 10 stories (above) | S1–S24 |
| `DESIGN.md` | Technical-details component lists "CVE" only (A1). Frontmatter not touched. | U1 |
| `EXPERIENCE.md` | Home Overview, Issues filters, Exposure queries and unknown state, glossary (Vulnerability), Needs attention and Review status filter rows, ⌘K row, Review flow, State Patterns, Open items 9 and 17 | U2–U14 |
| `epic-1-context.md` | none (it repeats only the unchanged no-match copy, L116) | — |
| `sprint-status.yaml`, `implementation-readiness.md`, the readiness record | none (the gate rerun rewrites the readiness record; Q5 is narrowed here, in the new gates and in section 6) | — |

### Technical impact

- **Scanning (ARCH7, Story 2.4):** `grype sbom:<file> -o json --by-cve`. Each finding stores its key ID
  (CVE when one exists, else the original ID) and every alias of the vulnerability. Findings for one CVE
  reported under different original IDs now fall into one issue per package version.
- **Joins and queries:** KEV, EPSS, CNA (CVE List) and OSV joins, Exposure vulnerability queries, the
  unknown check and ⌘K search match on any alias. The Exposure zero still needs a Grype DB record, now
  under the queried ID or any alias of it.
- **Unknown check (A4):** `grype db search --vuln <ID>` through `tools` against the active DB directory.
  One more pinned-CLI call per vulnerability query; its cost under NFR2 is an open detail (N5).
- **Status:** effective statuses come only from people's decisions; vendor claims are read-only data shown
  in the review panel and are never emitted in Armoury's VEX.
- **API:** the Issues list's Needs-attention count is fleet-wide whatever the type filter and search.
- **No new tokens, components, modules, infrastructure or deployment change.** No rollback: no code
  exists. No data migration: nothing is stored yet.

### Contract status (Story 1.1)

`spec-1-1-monorepo-scaffold-with-an-aggregate-local-gate-and-ci.md`: `status: 'draft'`, Revision 1,
never approved. Its sources are `epics.md#Story 1.1`, ARCH1, ARCH12, ARCH23, ARCH25, ARCH27, ARCH34,
PROC1, PROC3 and `architecture.md#Complete Project Directory Structure`; **no edit here touches them**
(ARCH7 and ARCH38 are not sources). Its Code Map cites a stale range `architecture.md:282-360` ("LoB
rules for `AGENTS.md`"); in the current file that range holds the Grype bullet (R7) and the
honest-degradation paragraph (R8), neither of which is an LoB rule or scaffold content. **No contract
revision is needed**; see the Contract Change Record in section 5. Story 1.1's own CI concerns (fast
tier, `ci` profile) are handed to its Build re-plan, not edited here.

## 3. Recommended approach

**Direct Adjustment.** Edit the planning artifacts in place. Keep every epic, story number and title.

- **Rollback:** not applicable — nothing is built.
- **MVP review:** not needed. No FR or NFR is added or removed; P1 only says how a vulnerability is
  identified in the glossary.
- **Why this path:** blocker 9 now has Daniel's rule (memlog 123); the concerns have decisions or gates
  (memlog 124–125); each fix is a definition, a reworded AC or a planning gate; no implementation exists.
- **Effort:** low — about two hours to apply and check 60 edits, then the readiness rerun.
- **Risk:** low. Main risks: a missed copy of old wording (success criterion 2 greps for it), and the
  alias details left open in section 6 (N1–N3), which Story 2.4 planning must close before Build.
- **Timeline:** Epic 1 can continue. Stories 2.4 and later in the list above should not start Build before
  these edits are applied and the gate passes.

## 4. Detailed change proposals

### 4.1 PRD

<!-- file: _bmad-output/planning-artifacts/prds/prd-Armoury-2026-06-11/prd.md -->

#### prd.md

**P1 · Glossary → Issue · L177 (A1)**
OLD: ⟦one vulnerability or license-policy finding in one package version, grouping⟧
NEW: ⟦one vulnerability or license-policy finding in one package version — a vulnerability is identified by its CVE ID when it has one, else by its original advisory ID (for example a GHSA ID), and a query for any of its IDs (aliases) finds the same issue — grouping⟧
Why: A1 — the PRD defines the issue unit, so it states which ID identifies a vulnerability. FR10, FR12, FR15 and FR17 are unchanged.

### 4.2 Architecture

<!-- file: _bmad-output/planning-artifacts/architecture.md -->

#### architecture.md

**R1 · front matter · L7**
OLD: ⟦amendedAt: '2026-11-07'  # Correct Course: sprint-change-proposal-2026-11-07-readiness.md (readiness blockers B1–B8) and⟧
NEW: ⟦amendedAt: '2026-11-07'  # Correct Course: sprint-change-proposal-2026-11-07-aliases.md (readiness blocker 9, vulnerability ID aliases; A1–A6), sprint-change-proposal-2026-11-07-readiness.md (readiness blockers B1–B8) and⟧
Why: records this amendment (a YAML comment; the frontmatter still parses).

**R2 · Core Architectural Decisions → Important → Vendor VEX matching · L203 (A2)**
OLD: ⟦Each applied match records the rule that matched.⟧
NEW: ⟦Each applied match records the rule that matched. **Vendor claims are display-only (decided 2026-11-07):** a matched claim is shown in the review panel with its source (vendor, document, date); it never sets a place's status, the counts, a status-filter match or Needs attention — only a person's decision does — and emitted VEX states only people's decisions.⟧
Why: A2 — the matching rule now says what a match does.

**R3 · API & Communication Patterns → Issues and review · L257 (A1)**
OLD: ⟦keyed by vulnerability ID and package purl@version,⟧
NEW: ⟦keyed by vulnerability ID (the key ID: the CVE ID when the vulnerability has one, else the original ID — GHSA, OSV or distro ID; see Vulnerability IDs and aliases below) and package purl@version,⟧
Why: A1 — defines the finding-group key.

**R4 · API & Communication Patterns → Issues and review · L257 (A5)**
OLD: ⟦the Needs-attention count, and the total for the pager.⟧
NEW: ⟦the Needs-attention count (always fleet-wide: the type filter and search never change it), and the total for the pager.⟧
Why: A5 — the API carries the count the badge, Home and the filter option share.

**R5 · API & Communication Patterns → Issues and review · L257 (A2)**
OLD: ⟦status filters, Needs attention and VEX (one statement per product) use effective statuses.⟧
NEW: ⟦status filters, Needs attention and VEX (one statement per product) use effective statuses. Only people's decisions set a status: a vendor VEX claim (Story 5.7) is display-only and never sets a status, a count, a filter match or Needs attention (Vendor VEX matching).⟧
Why: A2 — puts vendor claims inside the status rule.

**R6 · API & Communication Patterns → Issues and review · L257 (A1)**
OLD (anchor, kept): ⟦when the record has no description, no sentence is shown.⟧
NEW: ⟦ **Vulnerability IDs and aliases (decided 2026-11-07, readiness blocker 9):** Grype runs with `--by-cve` (Substrate Integration). A finding's vulnerability ID — the key of its finding group — is the CVE ID when the vulnerability has one, else the original ID (GHSA, OSV or distro ID). Each finding stores every alias of its vulnerability. KEV matching, the enrichment joins (EPSS, CNA, OSV), Exposure queries, the unknown-vulnerability check (Format Patterns → Honest-degradation metadata) and ⌘K search match on any alias, so a CVE query and a GHSA query find the same issue. The UI shows the key ID; the other aliases appear in the technical-details block.⟧
Why: A1 — the rule blocker 9 asked for, in the read-model section that defines the key.

**R7 · Substrate Integration → Grype · L282 (A1)**
OLD: ⟦`grype sbom:<file> -o json` with `GRYPE_DB_AUTO_UPDATE=false`;⟧
NEW: ⟦`grype sbom:<file> -o json --by-cve` with `GRYPE_DB_AUTO_UPDATE=false` (`--by-cve` keys results on the CVE ID when the vulnerability has one; Issues and review → Vulnerability IDs and aliases);⟧
Why: A1 — records the scanner invocation.

**R8 · Format Patterns → Honest-degradation metadata · L336 (A1, A4)**
OLD (anchor, kept): ⟦Only a known vulnerability — one with a record in the active Grype DB — gets the coverage-scoped zero.⟧
NEW: ⟦ A vulnerability query matches every finding whose key ID or any alias equals the queried ID, and the vulnerability is known when the active Grype DB has a record for the queried ID or any alias of it. **Lookup (decided 2026-11-07):** Armoury asks the loaded DB with `grype db search --vuln <ID>` through `tools`, against the active DB directory; it never reads the Grype SQLite schema.⟧
Why: A1 makes the unknown check and the query alias-aware; A4 records how "has a record" is checked.

### 4.3 Epics — front matter, requirements, UX-DRs, Epic List

<!-- file: _bmad-output/planning-artifacts/epics.md -->

#### Front matter, FRs and ARCH

**E1 · front matter → amendments · L14**
OLD (anchor, kept): ⟦  - 2026-11-07 Correct Course — _bmad-output/planning-artifacts/sprint-change-proposal-2026-11-07-readiness.md (readiness blockers B1–B8; no story added, removed or renamed)⟧
NEW: ⟦
  - 2026-11-07 Correct Course — _bmad-output/planning-artifacts/sprint-change-proposal-2026-11-07-aliases.md (readiness blocker 9, vulnerability ID aliases, and the gated concerns; no story added, removed or renamed)⟧
Why: records this amendment.

**E2 · Requirements Inventory → ARCH7 · L110 (A1)**
OLD: ⟦`GRYPE_DB_AUTO_UPDATE=false`; bounded parallel worker pool.⟧
NEW: ⟦`GRYPE_DB_AUTO_UPDATE=false`; Grype runs with `--by-cve` (ARCH38); bounded parallel worker pool.⟧
Why: A1 — ARCH7 is the ARCH item that fixes the Grype configuration. ARCH6 (re-evaluation reuses `scan`'s matcher) inherits it.

**E3 · Amendments 2026-11-07 → ARCH38 · L165 (A1)**
OLD: ⟦keyed by vulnerability ID + package purl@version,⟧
NEW: ⟦keyed by vulnerability ID (the key ID: the CVE ID when the vulnerability has one, else the original ID — GHSA, OSV or distro ID) + package purl@version,⟧
Why: mirrors R3.

**E4 · ARCH38 · L165 (A5)**
OLD: ⟦per-group, per-status and Needs-attention counts and a pager total come from the server;⟧
NEW: ⟦per-group, per-status and Needs-attention counts and a pager total come from the server (the Needs-attention count is always fleet-wide; the type filter and search never change it);⟧
Why: mirrors R4.

**E5 · ARCH38 · L165 (A2)**
OLD: ⟦(used by status filters, Needs attention and VEX).⟧
NEW: ⟦(used by status filters, Needs attention and VEX); only people's decisions set a status — vendor VEX claims (Story 5.7) are display-only.⟧
Why: mirrors R5.

**E6 · ARCH38 · L165 (A1)**
OLD (anchor, kept): ⟦none when the record has no description.⟧
NEW: ⟦ Vulnerability IDs and aliases: Grype runs with `--by-cve`; each finding stores every alias of its vulnerability; KEV matching, the enrichment joins (EPSS, CNA, OSV), Exposure queries, the unknown-vulnerability check and ⌘K search match on any alias, so a CVE query and a GHSA query find the same issue; the UI shows the key ID and lists the other aliases in the technical-details block.⟧
Why: mirrors R6.

#### UX Design Requirements

**E7 · UX-DR6 · L190 (A1)**
OLD: ⟦routes to an Exposure answer (a new question on Exposure starts a new trail);⟧
NEW: ⟦routes to an Exposure answer (a new question on Exposure starts a new trail); any alias of a vulnerability (a CVE ID, a GHSA ID…) finds the same issue and the same answer (ARCH38);⟧
Why: A1 — ⌘K search matches any alias. Story 1.8 is unchanged: it routes vulnerability IDs only once Story 6.3 lands.

**E8 · UX-DR16 · L203 (A6)**
OLD: ⟦and the panel says how many keep theirs ([ASSUMPTION], EXPERIENCE Open item 9).⟧
NEW: ⟦and the panel says how many keep theirs (decided; ARCH38).⟧
Why: A6 — the rule is decided in the architecture.

**E9 · UX-DR16 · L203 (A1)**
OLD: ⟦The panel ends with the technical-details block (CVE, KEV, CVSS, raw EPSS, source, check time).⟧
NEW: ⟦The panel ends with the technical-details block (the vulnerability ID and its other aliases, KEV, CVSS, raw EPSS, source, check time).⟧
Why: A1 — other aliases appear in the technical-details block.

**E10 · UX-DR16 · L203 (A2)**
OLD (anchor, kept): ⟦Agree both with UX before the stories that build them.⟧
NEW: ⟦ Vendor VEX claims are display-only (decided 2026-11-07): shown in the panel with their source, they never set a status, a count, a filter match or Needs attention until a person records a decision, and emitted VEX states only people's decisions (ARCH38).⟧
Why: A2.

**E11 · UX-DR22 · L212 (A1)**
OLD: ⟦Vulnerability (CVE ID), Found in⟧
NEW: ⟦Vulnerability (the key ID: the CVE ID, else the original ID such as a GHSA ID; ARCH38), Found in⟧
Why: A1 — the UI shows the key ID.

**E12 · UX-DR38 · L234 (A5)**
OLD: ⟦(`nav-badge`, lime count on `ink-2`); no badge at 0.⟧
NEW: ⟦(`nav-badge`, lime count on `ink-2`); no badge at 0. The number is always fleet-wide: the Issues type filter and search never change it, including on the filter option.⟧
Why: A5.

**E13 · UX-DR40 · L236 (A1)**
OLD: ⟦has no record for the queried ID, even if the CVE List or another source already lists it):⟧
NEW: ⟦has no record for the queried ID or any alias of it, even if the CVE List or another source already lists it):⟧
Why: A1 — the unknown check matches any alias.

### 4.4 Epics — stories

<!-- file: _bmad-output/planning-artifacts/epics.md -->

#### Stories (same file)

**S1 · Story 2.4: Uniform vulnerability scanning → scan AC · L782 (A1)**
OLD: ⟦**When** the scan job runs `grype sbom:<file> -o json` with the single fleet-wide config⟧
NEW: ⟦**When** the scan job runs `grype sbom:<file> -o json --by-cve` with the single fleet-wide config⟧
Why: A1 — the scanner invocation.

**S2 · Story 2.4 → scan AC · L784 (A1)**
OLD (anchor, kept): ⟦**And** an evidence entry records the scan, inputs and versions.⟧
NEW: ⟦
**And** each finding stores its vulnerability ID — the CVE ID when the vulnerability has one, else the original ID (GHSA, OSV or distro ID) — and every alias of the vulnerability; the finding group (issue) is keyed on that ID (ARCH38).⟧
Why: A1 — findings are stored with their aliases.

**S3 · Story 2.10: Home — Needs attention and open issues by severity → first AC · L924 (A3)**
OLD: ⟦**Given** scanned findings
**When** Home renders⟧
NEW: ⟦**Given** the open question Q2 (how the issue sentence is cut from the Grype DB description and how its source is labelled beside it; sprint-change-proposal-2026-11-07-readiness.md)
**When** this story is planned
**Then** the decision is recorded in `architecture.md` (Issues and review → Issue sentence) and EXPERIENCE.md (Home → Overview) and approved by the user before implementation.

**Given** the open question Q4 (the Negligible and Not rated yet severity markers, proposed in DESIGN.md but not drawn in the mock: confirm or redraw; sprint-change-proposal-2026-11-07-readiness.md)
**When** this story is planned
**Then** the decision is recorded in DESIGN.md (Components → Severity) and approved by the user before implementation.

**Given** scanned findings
**When** Home renders⟧
Why: A3 — Q2 (cut and label) and Q4 are gated in the story that first shows the sentence and the markers.

**S4 · Story 2.10 → detail AC · L932 (A1)**
OLD: ⟦Vulnerability (CVE ID in mono)⟧
NEW: ⟦Vulnerability (the key ID in mono: the CVE ID when the vulnerability has one, else the original ID such as a GHSA ID; ARCH38)⟧
Why: A1 — the UI shows the key ID.

**S5 · Story 4.3: KEV and EPSS enrichment → re-join AC · L1258 (A1)**
OLD: ⟦**Then** findings are re-joined to the new enrichment without re-matching SBOMs,⟧
NEW: ⟦**Then** findings are re-joined to the new enrichment without re-matching SBOMs, matching KEV entries and EPSS scores on any alias of the finding's vulnerability (ARCH38),⟧
Why: A1 — KEV and EPSS are CVE-keyed; findings may be keyed on another ID.

**S6 · Story 4.3 → UI AC · L1261 (A1)**
OLD: ⟦**When** it is KEV-listed⟧
NEW: ⟦**When** it is KEV-listed (the KEV catalogue lists any alias of its vulnerability, ARCH38)⟧
Why: A1 — KEV matching on any alias.

**S7 · Story 4.4: OSV and CNA record enrichment → first AC · L1280 (A3)**
OLD: ⟦**Given** connected mode
**When** the enrichment schedule fires (default every 6 h, Helm value, PROC2)
**Then** the full CVE List v5⟧
NEW: ⟦**Given** the open question Q2 (which description the issue sentence uses when more than one source has one — the Grype DB record, the CVE List CNA container or OSV; sprint-change-proposal-2026-11-07-readiness.md)
**When** this story is planned
**Then** the decision is recorded in `architecture.md` (Issues and review → Issue sentence) and approved by the user before implementation.

**Given** connected mode
**When** the enrichment schedule fires (default every 6 h, Helm value, PROC2)
**Then** the full CVE List v5⟧
Why: A3 — Q2's precedence part is gated where the second and third descriptions arrive.

**S8 · Story 4.4 → OSV AC · L1283 (A1)**
OLD (anchor, kept): ⟦(all OSV, ~2.7 GB), set via Helm values.⟧
NEW: ⟦
**And** CVE List and OSV records join to a finding on any alias of its vulnerability (ARCH38).⟧
Why: A1 — the CNA and OSV enrichment joins.

**S9 · Story 4.4 → technical-details AC · L1291 (A1)**
OLD: ⟦its technical-details block lists every source used with retrieval time (CVE, KEV, CVSS, EPSS, source, check time)⟧
NEW: ⟦its technical-details block lists every source used with retrieval time (the vulnerability ID and its other aliases, KEV, CVSS, EPSS, source, check time)⟧
Why: A1 — aliases in the technical-details block.

**S10 · Story 5.2: Issues list → first AC · L1523 (A3)**
OLD: ⟦**Given** the Issues surface
**When** it loads⟧
NEW: ⟦**Given** the open question Q5 (the URL value of the Needs attention filter option, and whether Review all N clears the type filter and search; the walk order is already decided — `needs_attention=true` keeps the Issues order, architecture.md → Issues and review; sprint-change-proposal-2026-11-07-readiness.md)
**When** this story is planned
**Then** the decision is recorded in EXPERIENCE.md (Issues → Filters) and approved by the user before implementation.

**Given** the Issues surface
**When** it loads⟧
Why: A3 — 5.2 builds the filter and its URL; Q5 loses its decided walk-order part (rerun-1 concern 1).

**S11 · Story 5.2 → filters AC · L1530 (A5)**
OLD: ⟦counts count issues, not places⟧
NEW: ⟦counts count issues, not places; the Needs attention option's count is always the fleet-wide Needs-attention number, whatever the type filter and search (UX-DR38)⟧
Why: A5.

**S12 · Story 5.4: Review panel → first AC · L1581 (A3)**
OLD: ⟦**Given** the Issues list
**When** an issue is selected⟧
NEW: ⟦**Given** the open question Q5 (the URL value of the Needs attention filter option, and whether Review all N clears the type filter and search; the walk order is already decided — `needs_attention=true` keeps the Issues order, architecture.md → Issues and review; sprint-change-proposal-2026-11-07-readiness.md)
**When** this story is planned
**Then** the decision is recorded in EXPERIENCE.md (Issues → Filters) and approved by the user before implementation.

**Given** the Issues list
**When** an issue is selected⟧
Why: A3 — 5.4 builds Review all N.

**S13 · Story 5.4 → Review tab AC · L1583 (A1)**
OLD: ⟦the technical-details block (CVE, KEV, CVSS, EPSS, source and check time,⟧
NEW: ⟦the technical-details block (the vulnerability ID and its other aliases, KEV, CVSS, EPSS, source and check time,⟧
Why: A1.

**S14 · Story 5.7: Ingest vendor VEX → claim AC · L1672 (A2)**
OLD: ⟦**Then** the finding shows a vendor-attributed status ("Not impacted — per <vendor> VEX, <date>") distinct from the team's own decisions, and the team can still record their own decision, which takes precedence and is shown alongside.⟧
NEW: ⟦**Then** the review panel shows the vendor claim with its source ("Not impacted — per <vendor> VEX, <date>"), distinct from the team's own decisions; the claim is display-only — it never sets the issue's status, its counts, a Review status filter match or Needs attention, and the place stays Not reviewed yet until a person records a decision (ARCH38)
**And** VEX export (Story 5.6) states only people's decisions; a vendor claim is never emitted as Armoury's statement.⟧
Why: A2 — a claim is shown, not applied as a status.

**S15 · Story 5.7 → withdrawal AC · L1680 (A2)**
OLD: ⟦**Then** the change supersedes the earlier claim, and affected findings return to their prior status with history kept.⟧
NEW: ⟦**Then** the change supersedes the earlier claim, the review panel shows the current claim, and history is kept; no status changes, because a claim never set one.⟧
Why: A2 — "return to their prior status" assumed claims set status.

**S16 · Story 5.8: Review scope → override AC · L1697 (A6)**
OLD: ⟦("2 places keep their own status"; [ASSUMPTION], EXPERIENCE Open item 9).⟧
NEW: ⟦("2 places keep their own status"; decided, ARCH38; EXPERIENCE Open item 9 resolved).⟧
Why: A6 — removes the stale [ASSUMPTION].

**S17 · Story 6.2: Blast-radius query API → query AC · L1738 (A1)**
OLD: ⟦with a CVE ID, a `package@version`,⟧
NEW: ⟦with a vulnerability ID (a CVE ID or any other alias, such as a GHSA ID; it matches every finding whose key ID or any alias equals it, ARCH38), a `package@version`,⟧
Why: A1 — closes the CVE-day false zero for GHSA-keyed findings.

**S18 · Story 6.2 → zero AC · L1750 (A1)**
OLD: ⟦used for matching (Grype DB), never a bare empty list.⟧
NEW: ⟦used for matching (Grype DB) under the queried ID or any alias of it, never a bare empty list.⟧
Why: A1.

**S19 · Story 6.2 → unknown AC · L1757 (A1)**
OLD: ⟦**Given** an unknown CVE ID or malformed query⟧
NEW: ⟦**Given** an unknown vulnerability ID (a CVE ID or any other alias) or malformed query⟧
Why: A1.

**S20 · Story 6.2 → unknown AC · L1759 (A1, A4)**
OLD: ⟦the active Grype DB has no record for the ID, even when the CVE List (Story 4.4) or another enrichment feed knows it — (with feed versions and their age); the UI never turns the second into "No software has it" (Story 6.3).⟧
NEW: ⟦the active Grype DB has no record for the ID or any alias of it, even when the CVE List (Story 4.4) or another enrichment feed knows it — (with feed versions and their age); the UI never turns the second into "No software has it" (Story 6.3)
**And** the record check runs `grype db search --vuln <ID>` through `tools` against the active DB directory; Armoury never reads the Grype SQLite schema (architecture.md → Honest-degradation metadata).⟧
Why: A1 makes the check alias-aware; A4 records the lookup method.

**S21 · Story 6.3: Exposure surface → first AC · L1773 (A3)**
OLD: ⟦**Given** the palette⟧
NEW: ⟦**Given** the open question Q1 (whether the unknown-vulnerability state adds "Published <date>; package data is not available yet." when the CVE List knows the ID, with a reworded first sentence; sprint-change-proposal-2026-11-07-readiness.md)
**When** this story is planned
**Then** the decision is recorded in EXPERIENCE.md (State Patterns → Unknown vulnerability) and approved by the user before implementation.

**Given** the palette⟧
Why: A3 — Q1 is gated by the story that builds the unknown state.

**S22 · Story 6.3 → palette AC · L1774 (A1)**
OLD: ⟦**When** the user types a CVE ID or `package@version`⟧
NEW: ⟦**When** the user types a vulnerability ID (a CVE ID or any other alias, such as a GHSA ID) or `package@version`⟧
Why: A1 — ⌘K matches any alias.

**S23 · Story 6.3 → palette AC · L1775 (A1)**
OLD: ⟦routes to Exposure with that query;⟧
NEW: ⟦routes to Exposure with that query, and any alias of the same vulnerability gives the same answer (ARCH38);⟧
Why: A1.

**S24 · Story 6.3 → unknown AC · L1782 (A1)**
OLD: ⟦**Given** Exposure with a CVE ID Armoury has no data for (the Story 6.2 "no record in the vulnerability data" error: Grype DB has no record for it, even if the CVE List already lists it)⟧
NEW: ⟦**Given** Exposure with a vulnerability ID Armoury has no data for (the Story 6.2 "no record in the vulnerability data" error: Grype DB has no record for it or any alias of it, even if the CVE List already lists it)⟧
Why: A1.

### 4.5 UX spines

<!-- file: _bmad-output/planning-artifacts/ux-designs/ux-Armoury-2026-11-06/DESIGN.md -->

#### DESIGN.md

No token, frontmatter or component is added. Only the technical-details content list changes.

**U1 · Components → Technical details · L719 (A1)**
OLD: ⟦Holds CVE, KEV, CVSS, EPSS, source and check time.⟧
NEW: ⟦Holds the vulnerability ID (the CVE ID when there is one, else the original ID) and its other aliases (for example a GHSA ID), KEV, CVSS, EPSS, source and check time.⟧
Why: A1 — the other aliases appear in the technical-details block.

<!-- file: _bmad-output/planning-artifacts/ux-designs/ux-Armoury-2026-11-06/EXPERIENCE.md -->

#### EXPERIENCE.md

**U2 · Home → detail column → Overview · L62 (A1)**
OLD: ⟦Vulnerability (CVE ID), Found in⟧
NEW: ⟦Vulnerability (the key ID: the CVE ID, else the original ID such as a GHSA ID), Found in⟧
Why: A1 — the UI shows the key ID.

**U3 · Issues → Filters · L70 (A5)**
OLD: ⟦(its count is the Needs-attention number)⟧
NEW: ⟦(its count is the fleet-wide Needs-attention number; the type filter and search never change it)⟧
Why: A5.

**U4 · Exposure → queries · L99 (A1)**
OLD: ⟦- Queries accept a vulnerability ID, `package@version` or a fingerprint.⟧
NEW: ⟦- Queries accept a vulnerability ID, `package@version` or a fingerprint. A vulnerability query matches any alias: a CVE ID and a GHSA ID for the same vulnerability give the same answer (decided 2026-11-07).⟧
Why: A1 — Exposure queries match any alias.

**U5 · Exposure → Unknown vulnerability · L110 (A1)**
OLD: ⟦has no record for the queried ID — even if the CVE List⟧
NEW: ⟦has no record for the queried ID or any alias of it — even if the CVE List⟧
Why: A1.

**U6 · Glossary → Vulnerability · L157 (A1)**
OLD (line starts): ⟦| Vulnerability [ASSUMPTION: replaces "Weakness"] | CVE |⟧
NEW: ⟦| Vulnerability [ASSUMPTION: replaces "Weakness"] | CVE ID, or the original ID (GHSA, OSV or distro ID) when there is no CVE | The key ID, small and mono: detail ("Vulnerability CVE-2026-23012"), Exposure query, palette. The technical details list it with its other aliases (for example a GHSA ID); a query for any alias finds the same issue |⟧
Why: A1 — the glossary line about the CVE ID.

**U7 · Component Patterns → Needs attention · L204 (A5)**
OLD: ⟦The same number everywhere it appears. |⟧
NEW: ⟦The same number everywhere it appears: always fleet-wide, never narrowed by the Issues type filter or search. |⟧
Why: A5.

**U8 · Component Patterns → Review status filter · L207 (A5)**
OLD: ⟦**Needs attention** (with the Needs-attention count, the same number as Home and the badge)⟧
NEW: ⟦**Needs attention** (with the Needs-attention count, the same number as Home and the badge; it is always fleet-wide — the type filter and search never change it)⟧
Why: A5.

**U9 · Component Patterns → ⌘K palette · L226 (A1)**
OLD: ⟦Typing a CVE ID, `package@version` or fingerprint routes to an Exposure answer.⟧
NEW: ⟦Typing a CVE ID, `package@version` or fingerprint routes to an Exposure answer; any alias of a vulnerability (a CVE ID, a GHSA ID…) finds the same issue and the same answer.⟧
Why: A1 — ⌘K search matches any alias.

**U10 · Review flow → Scope · L241 (A6)**
OLD: ⟦[ASSUMPTION] A later "All places" decision does not overwrite places that have their own status;⟧
NEW: ⟦A later "All places" decision does not overwrite places that have their own status (decided; architecture → Issues and review);⟧
Why: A6.

**U11 · Review flow · L243 (A2)**
OLD (anchor, kept): ⟦Decisions propagate to Home counts, Exposure, Software, exports and audit reports.⟧
NEW: ⟦ **Vendor VEX claims** (Story 5.7) are shown in the panel with their source but are not decisions: they never set the status, the counts, the filters or Needs attention, and Armoury's VEX never states them; the place stays Not reviewed yet until a person decides (decided 2026-11-07; layout Open item 17).⟧
Why: A2 — the review panel rule.

**U12 · State Patterns → Unknown vulnerability · L256 (A1)**
OLD: ⟦The vulnerability data (Grype DB) has no record for the queried ID, even if⟧
NEW: ⟦The vulnerability data (Grype DB) has no record for the queried ID or any alias of it, even if⟧
Why: A1.

**U13 · Open items → 9 · L489 (A6)**
OLD (line starts): ⟦9. [ASSUMPTION] **Review scope details:**⟧
NEW: ⟦9. **Resolved 2026-11-07** (readiness concern): a later "All places" decision does not overwrite places that have their own status (architecture → Issues and review); the **Review status** filter matches an issue when any of its places has that status.⟧
Why: A6 — closes the open item.

**U14 · Open items → 17 · L500 (A2)**
OLD: ⟦— not in the review panel. (Review scope is decided: see The issue unit and Review flow.)⟧
NEW: ⟦— not drawn in the review panel; the layout is set before Story 5.7 Build. Decided 2026-11-07: the claims are display-only — shown in the review panel with their source, never setting status, counts, filters or Needs attention until a person decides, and never emitted in Armoury's VEX. (Review scope is decided: see The issue unit and Review flow.)⟧
Why: A2 — the rule is decided; only the layout stays open.

### 4.6 Epic 1 context

No edit. `epic-1-context.md` repeats only the palette no-match copy (L116), which does not change.

### 4.7 Edits by decision

| Decision | Edit IDs |
|---|---|
| A1 vulnerability ID aliases (`--by-cve`, key ID, aliases matched everywhere) | P1, R3, R6, R7, R8, E2, E3, E6, E7, E9, E11, E13, S1, S2, S4, S5, S6, S8, S9, S13, S17, S18, S19, S20, S22, S23, S24, U1, U2, U4, U5, U6, U9, U12 |
| A2 vendor VEX claims display-only | R2, R5, E5, E10, S14, S15, U11, U14 |
| A3 gates for Q1, Q2, Q4, Q5 | S3 (Q2, Q4 → 2.10), S7 (Q2 → 4.4), S10 (Q5 → 5.2), S12 (Q5 → 5.4), S21 (Q1 → 6.3) |
| A4 `grype db search --vuln <ID>` | R8, S20 |
| A5 fleet-wide Needs attention count | R4, E4, E12, S11, U3, U7, U8 |
| A6 stale [ASSUMPTION] on later All places decisions | E8, S16, U10, U13 |
| Bookkeeping | R1, E1 |

R8 and S20 serve A1 and A4. Not changed, checked: PRD FR15 (says vendor claims are "applied … with
attribution", not that they set a status — the A2 condition is not met), FR10, FR12, FR17 ("a CVE ID …
answered as unknown" still holds with aliases); epics FR15 (L55) and FR17 (L60), mirrors of the PRD;
UX-DR33 (L229, the vocabulary pair "Vulnerability (CVE)"); Story 1.8 palette ACs (L607, L615); Story 5.1
(it orders groups but does not key them); Story 5.6 (it emits effective statuses, which now come only
from decisions; R5); Story 6.2's vendor VEX line (L1742: claims are included in the answer as data);
Story 6.1 `Cve` vertex (N2); DESIGN.md Exposure header (L724: the rule lives in EXPERIENCE); EXPERIENCE
L255 (known-vulnerability zero) and Flow 2 (L386, L394); `epic-1-context.md`; `sprint-status.yaml`; the
mock.

## 5. Implementation handoff

### Scope classification

**Moderate.** The fixes are one data rule, definitions, reworded ACs and planning gates, but they change
the stored finding model and matching behaviour in four owner documents (PRD glossary, architecture, UX
spines, epics) and ten Linear story bodies, so PO/Dev applies them with the PM, Architect and UX owners
checking their own documents. No replan: no FR, NFR, epic or story is added, removed, renamed or
reordered, and no code exists.

### Who applies what, in this order

| Step | Owner (skill) | Applies | Notes |
|---|---|---|---|
| 1 | PM — `bmad-prd` (update) | P1 | `updated` is already 2026-11-07. |
| 2 | Architect — `bmad-architecture` (update) | R1–R8 | Check N1–N3 and N5 are listed for Story 2.4 and 6.2 planning. |
| 3 | UX designer — `bmad-ux` (update) | U1–U14 | Add a memlog event "Readiness blocker 9 and cheap concerns applied (sprint-change-proposal-2026-11-07-aliases.md)". |
| 4 | PO/Dev — Developer agent | E1–E13, S1–S24 | Keep every story number and title. |
| 5 | Test Architect / PO — `bmad-sprint-planning` | readiness gate rerun (INF-11) | Expect `sprint_plan.py generate --dry-run` unchanged: 11 epics, 79 stories, in sync. |
| 6 | PO — Linear Reconcile | see "Linear impact" | Only after Daniel approves this proposal. |
| 7 | Story 1.1 owner — `bmad-build` | nothing from section 4 | The planned Story 1.1 re-plan also takes the second rerun's CI concerns: define the "fast tier" steps (`epics.md:377`; ARCH23) and add the Skaffold `ci` profile and its CI e2e use to the Story 1.1 ACs (ARCH34; Story 1.2 depends on it, `epics.md:403`) — rerun-2 finding 2. |

### Success criteria

1. Every edit in section 4 is applied; each OLD quote no longer appears where it was replaced.
2. `rg -n 'grype sbom:<file> -o json`? with|Vulnerability \(CVE ID|user types a CVE ID or|unknown CVE ID or malformed|\(CVE, KEV|Holds CVE, KEV|keep theirs \(\[ASSUMPTION\]|\[ASSUMPTION\], EXPERIENCE Open item 9|\[ASSUMPTION\] A later "All places"|9\. \[ASSUMPTION\]|return to their prior status|vendor-attributed status' _bmad-output/planning-artifacts/prds/prd-Armoury-2026-06-11/prd.md _bmad-output/planning-artifacts/architecture.md _bmad-output/planning-artifacts/epics.md _bmad-output/planning-artifacts/ux-designs/ux-Armoury-2026-11-06/DESIGN.md _bmad-output/planning-artifacts/ux-designs/ux-Armoury-2026-11-06/EXPERIENCE.md`
   finds nothing.
3. `rg -n -- '--by-cve'` finds the architecture (Grype bullet, Issues and review), ARCH7, ARCH38 and
   Story 2.4; `rg -n 'grype db search --vuln'` finds the architecture and Story 6.2;
   `rg -n 'open question Q[1245] '` finds Stories 2.10 (Q2, Q4), 4.4 (Q2), 5.2 (Q5), 5.4 (Q5) and 6.3 (Q1).
4. `sprint-status.yaml` is unchanged, and the dry run reports 11 epics and 79 stories, in sync.
5. The readiness gate is rerun: blocker 9 is closed, Q1, Q2, Q4 and Q5 are gated by story ACs, and the
   verdict is PASS, or CONCERNS that Daniel accepts.
6. `linear_reconcile.py plan --check` exits 0 after Reconcile (apart from the known Story 1.1 status
   difference).
7. `validate_story_contract.py validate --phase draft` still passes for the Story 1.1 spec.
8. Every open question in section 6 has an owner and a gate, and every gate named there is carried by a
   story AC or by an owner's planning step listed in this section.

### Linear impact

Follow Linear Correct Course and then Linear Reconcile (`_bmad/custom/linear-workflow.md`): publish
only approved changes against existing identities, comment on each changed issue, never delete.

- **Planning issues (comment "changed: sprint-change-proposal-2026-11-07-aliases"):** `planning:prd`
  INF-7, `planning:ux` INF-8, `planning:architecture` INF-9, `planning:epics` INF-10. `planning:sprint`
  INF-11 stays In Progress until the gate passes.
- **Epics:** no summary or title changes (Epic 2 INF-14, Epic 4 INF-16, Epic 5 INF-17, Epic 6 INF-18 only
  contain changed stories).
- **Stories whose managed blocks change (10):** 2.4 INF-34, 2.10 INF-40, 4.3 INF-52, 4.4 INF-53,
  5.2 INF-59, 5.4 INF-61, 5.7 INF-64, 5.8 INF-98, 6.2 INF-66, 6.3 INF-67. Bodies only; no retitle, so no
  identity decisions are expected.
- **Unchanged, checked:** 1.8 INF-30 (UX-DR6 text changes, its ACs do not), 5.1 INF-58, 5.6 INF-63,
  11.4 (vendor VEX in the CI verdict stays as written; N7).
- **New or removed issues:** none. Story 1.1 tasks (INF-101–INF-111): unchanged.
- **Commands:**
  `uv run _bmad/custom/scripts/linear_reconcile.py plan --root . --epics _bmad-output/planning-artifacts/epics.md --sprint-status _bmad-output/implementation-artifacts/sprint-status.yaml`
  → apply → baseline →
  `uv run _bmad/custom/scripts/linear_reconcile.py plan --root . --epics _bmad-output/planning-artifacts/epics.md --sprint-status _bmad-output/implementation-artifacts/sprint-status.yaml --check`.

### Contract Change Record

| Field | Value |
|---|---|
| Affected contract | STORY-1.1 — `_bmad-output/implementation-artifacts/spec-1-1-monorepo-scaffold-with-an-aggregate-local-gate-and-ci.md` (checked; not changed) |
| Approval state before | `status: 'draft'`; Revision 1; never approved; no digest |
| Change class | **None.** No cited source changes: `epics.md#Story 1.1`, ARCH1, ARCH12, ARCH23, ARCH25, ARCH27, ARCH34 and `architecture.md#Complete Project Directory Structure` are untouched. The stale Code Map range `architecture.md:282-360` now covers R7 and R8, which are not LoB rules or scaffold content. No approved contract changes. |
| Old / new revision | 1 / 1 (unchanged) |
| Changed AC / VAL / source IDs | ACs: none. VALs: none. Sources: none. |
| Impact on implementation | None. The CI concerns for Story 1.1 (fast tier, `ci` profile) go to its Build re-plan (step 7), outside this proposal. |
| Impact on tests / evidence | None. No locked tests, no delivery evidence. |
| Evidence invalidated | None. |
| Approvals required | Daniel approves this proposal. No Test Architect reapproval (no approved validation exists). |
| Edit guard | Not involved (contract not approved or locked). |
| Validator command | `uv run _bmad/custom/scripts/validate_story_contract.py validate --phase draft _bmad-output/implementation-artifacts/spec-1-1-monorepo-scaffold-with-an-aggregate-local-gate-and-ci.md` |
| Other contracts | None: no other story has a spec. |

## 6. Open questions

Answered by Daniel on 2026-11-07 with the approval:

- **N5:** an ID is known only when `grype db search --vuln <ID>` returns affected packages. A record with no package data shows "Armoury has no data for <ID> yet".
- **N7:** vendor claims never pass the CI policy. Only a human decision changes a CI policy result; Story 11.4 changes to match.

The other questions stay open and are gated by their stories.

Not decided by this proposal. Each has an owner and the gate that carries it.

**Carried from the readiness record** (`sprint-change-proposal-2026-11-07-readiness.md` section 6), now
gated by story ACs (A3):

| ID | Question (as narrowed) | Owner | Gated by |
|---|---|---|---|
| Q1 | Whether the unknown state adds "Published <date>; package data is not available yet." when the CVE List knows the ID, with a reworded first sentence. | UX + Daniel | Story 6.3 planning AC (S21) |
| Q2 | How the first sentence is cut and how its source is labelled (Grype DB description); which description wins when the CVE List or OSV also has one. | Architect + UX | Story 2.10 planning AC (S3, cut and label); Story 4.4 planning AC (S7, precedence) |
| Q4 | Confirm or redraw the Negligible and Not rated yet markers. | UX | Story 2.10 planning AC (S3) |
| Q5 | The URL value of the Needs attention filter option, and whether Review all N clears the type filter and search. **Narrowed:** the walk order is no longer open — `architecture.md:257` says `needs_attention=true` returns groups "in the same order" (the Issues order), and Save and next walks the current filter. Note: with the count fleet-wide (A5), clearing the type filter and search would keep "Review all N" and the walked set the same size; that choice is still Q5's. | UX | Story 5.2 and Story 5.4 planning ACs (S10, S12) |

Q6 (Story 1.8) is already gated; Q3 and Q7 were answered.

**New, raised by A1–A6:**

| ID | Decision | Question | Owner | Gated by |
|---|---|---|---|---|
| N1 | A1 | Where the aliases come from: only Grype's related vulnerabilities in the `--by-cve` output, or also OSV `aliases` and CVE List data (Story 4.4); and whether a later feed or enrichment update refreshes a finding's aliases. | Architect | Story 2.4 planning |
| N2 | A1 | How aliases are stored and indexed for alias lookups (column or table), and how the AGE `Cve` vertex (Story 6.1) holds them (the key ID with alias properties, or one vertex per alias). | Architect | Story 2.4 planning (storage); Story 6.1 planning (graph) |
| N3 | A1 | The key ID can change: a GHSA-keyed finding gets a CVE after a DB update, or one original ID relates to more than one CVE. Which key wins, and how decisions and history recorded on the old key stay attached to the issue. | Architect + Daniel | Story 2.4 planning (before Story 5.3 stores decisions) |
| N4 | A1 | Exposure header and query button when the query is a non-key alias (show the typed ID, the key ID, or both); whether the Issues search field ("Find a package or vulnerability") also matches any alias (A1 names ⌘K only); and which story builds vulnerability-ID results in the ⌘K Issues group. | UX + PO | Story 6.3 planning (Exposure); Story 5.2 planning (search, palette Issues group) |
| N5 | A4 | `grype db search --vuln <ID>` searches affected packages; Grype 0.120.1 also has `grype db search vuln <ID>` (vulnerability records, DB schema v6+). Confirm that an ID with a vulnerability record but no affected-package rows counts as known or unknown under the decided command; the output format (`-o json`), whether the command resolves aliases itself, its cost per query under NFR2, and whether the same call supplies the metadata for "a CVE that matches no fleet package" (`epics.md:1761–1763`). | Architect | Story 6.2 planning |
| N6 | A1, A2 | Whether vendor VEX statements match a finding's vulnerability on any alias (Story 5.7), and which ID and aliases Armoury's emitted VEX states (Story 5.6, for example OpenVEX `aliases`). | Architect | Story 5.6 and 5.7 planning |
| N7 | A2 | Story 11.4 (`epics.md:2643`) lets a matching vendor VEX `not_affected` statement keep a finding from failing the CI policy by default (`ciPolicy.trustVendorVex`). A2 covers status, counts, filters and Needs attention, not the CI verdict. Keep, or make vendor claims display-only there too? | Daniel + Architect | Story 11.4 planning |
| N8 | A2 | Wording only: FR15 ("applying their not-affected claims") and Story 5.7's story statement ("apply their not-affected claims", "reduces noise") read as if claims change findings. Reword to match display-only? | PM | None (wording only) |
| N9 | A5 | Whether the other Review status counts and the group counts follow the type filter and search (A5 fixes only the Needs attention count). | UX + Architect | Story 5.2 planning |

Other readiness concerns are unchanged and stay with the owners in `implementation-readiness.md`.

## 7. Change-analysis checklist (completed)

| Item | Status | Notes |
|---|---|---|
| 1.1 Triggering story | [x] | No story: the readiness gate's second rerun (2026-11-07, FAIL narrow) after `sprint-change-proposal-2026-11-07-readiness.md`. |
| 1.2 Core problem | [x] | A missing data rule (vulnerability ID aliases, blocker 9) and five cheap concerns, found before implementation. |
| 1.3 Evidence | [x] | Section 1 (rerun lenses with file:line; local Grype 0.120.1 help output). |
| 2.1 Current epic | [x] | Epic 1 (Story 1.1 draft). Not affected; it can complete as planned. |
| 2.2 Epic-level changes | [x] | None. |
| 2.3 Remaining epics | [x] | Epics 2, 4, 5, 6 change in story ACs; 1, 3, 7–11 checked, unchanged (Story 11.4 → N7). |
| 2.4 Invalidated or new epics | [N/A] | None. |
| 2.5 Epic order | [x] | Unchanged. |
| 3.1 PRD | [x] | P1 (glossary); FR15 checked, unchanged; MVP unchanged. |
| 3.2 Architecture | [x] | R1–R8: `--by-cve`, key ID and aliases, vendor claims display-only, unknown rule and lookup, fleet-wide count. |
| 3.3 UI/UX | [x] | U1–U14; no new component or token. |
| 3.4 Other artifacts | [x] | `epic-1-context.md` checked, unchanged; `sprint-status.yaml` unchanged; Story 1.1 spec (Contract Change Record); Linear (section 5). |
| 4.1 Direct adjustment | [x] | Viable. Effort low; risk low. |
| 4.2 Rollback | [N/A] | Nothing is built. |
| 4.3 PRD MVP review | [N/A] | No scope change. |
| 4.4 Recommended path | [x] | Direct Adjustment (section 3). |
| 5.1 Issue summary | [x] | Section 1. |
| 5.2 Epic impact and artifact needs | [x] | Section 2. |
| 5.3 Path and rationale | [x] | Section 3. |
| 5.4 MVP impact and action plan | [x] | Sections 3 and 5. |
| 5.5 Handoff plan | [x] | Section 5. |
| 6.1 Checklist complete | [x] | All applicable items addressed. |
| 6.2 Proposal accuracy | [x] | OLD quotes checked mechanically on 2026-11-07 (each found once, on the stated line; no overlaps; simulated application keeps the `epics.md`, `architecture.md` and `DESIGN.md` frontmatter parsing). |
| 6.3 User approval | [!] | Pending: Daniel approves, edits or rejects. Status stays `draft` until then. |
| 6.4 Sprint status update | [N/A] | No epic or story added, removed or renamed. |
| 6.5 Next steps confirmed | [!] | Confirm the handoff order with Daniel; then apply, rerun the gate and reconcile Linear. |
