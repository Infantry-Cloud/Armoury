# Readiness rerun — Lens 2: fresh gate pass (Epic 1 next stories; Epics 2, 5, 6)

Read-only review, 2026-11-07. I ignored the earlier verdict. Gate question: could a developer implement these epics without inventing decisions that nothing records?
Paths: PA = `_bmad-output/planning-artifacts/`, IA = `_bmad-output/implementation-artifacts/`, EXP/DES = `PA/ux-designs/ux-Armoury-2026-11-06/EXPERIENCE.md` / `DESIGN.md`, RCR = `PA/sprint-change-proposal-2026-11-07-readiness.md`, CR7 = `PA/sprint-change-proposal-2026-11-07.md`. Line numbers were checked with `rg -n` on the current files.

## Verdict suggestion

**FAIL (narrow).** Epic 1 (Stories 1.1–1.9) can start. All eight earlier blockers are closed in the files. One cross-epic data-model decision is still unrecorded: how vulnerability IDs are made canonical (Grype's original GHSA/OSV ID versus the CVE). Story 2.4 persists that ID. It is the key for issue grouping (2.10), the KEV join (4.3) and the CVE query (6.2), and with the new B4 rule it brings back the CVE-day false zero. Close it before Story 2.4 starts Build. Everything else is a story-local concern or a note.

Counts: **1 blocker · 25 concerns · 9 notes.**

### The eight earlier blockers are closed (verified)
- B1 scope split: `PA/epics.md:1558` "every decision in this story has scope All places"; `:1589` "the panel has no scope control and no chip shows Mixed in this story".
- B2 issue-wide status: `PA/architecture.md:257` "the issue-wide `triage_status` (the status of the latest `all_places` decision on the group; `untriaged` when there is none)"; VEX at `PA/epics.md:1646`.
- B3 Negligible and Not rated yet: `PA/epics.md:783` "every level Grype reports, Negligible and Unknown included".
- B4 unknown means no Grype DB record: `PA/architecture.md:336`; `PA/epics.md:1759`.
- B5 advisory sentence: `PA/epics.md:932`; `PA/architecture.md:257` "Issue sentence (decided 2026-11-07)".
- B6 Needs attention filter: `PA/epics.md:1528`, `:1597`; `PA/architecture.md:257` "`needs_attention=true`".
- B7 `?` key: `PA/epics.md:191`, `:619-620`.
- B8 lime exceptions: `PA/epics.md:642`; `DES:570`, `DES:596`, `DES:702`. The lists now match.

## Findings

### Blocker

**1. BLOCKER — No rule for vulnerability-ID aliases or a canonical issue ID. Lens A 5 graded this a concern; I regrade it a blocker because B4 now depends on it.**
- **Stories:** 2.4 (persists the ID), 2.10, 4.3, 5.1–5.3, 5.6, 6.2, 6.3.
- **Evidence:**
  - Issues are keyed on a single ID: `PA/architecture.md:257` "keyed by vulnerability ID and package purl@version"; `PA/epics.md:165` (ARCH38) "keyed by vulnerability ID + package purl@version".
  - Story 2.4 stores whatever Grype reports: `PA/epics.md:783` "vulnerability findings are stored with typed severity … and the locked `Finding` vocabulary".
  - Grype's default is the original advisory ID. Local Grype 0.120.1 `grype --help` prints: "--by-cve  orient results by CVE instead of the original vulnerability ID when possible". Language-ecosystem matches come back as GHSA IDs unless that flag (or `relatedVulnerabilities`) is used. No artifact says which.
  - KEV is a CVE list joined onto findings: `PA/epics.md:1254` "fetches the CISA KEV catalogue", `:1258` "findings are re-joined to the new enrichment".
  - Exposure is queried by CVE ID: `PA/epics.md:1738` "`POST /api/v1/blast-radius-queries` with a CVE ID".
  - B4 makes the zero decision depend on the Grype DB alone: `PA/epics.md:1750` "only for a vulnerability that has a record in the vulnerability data used for matching (Grype DB)". The NVD CVE record exists in the Grype DB, so a CVE query against GHSA-keyed findings is "known" and gets "No software has it". That is the CVE-day false zero that FR17 and NFR8 forbid (`PA/prds/prd-Armoury-2026-06-11/prd.md` FR17: "an unknown CVE ID is answered as unknown … never as zero").
  - Detail shows "Vulnerability (CVE ID in mono)" (`PA/epics.md:932`), which is undefined when the primary ID is a GHSA.
  - `rg -i "alias|GHSA|relatedVulnerab"` over the PRD, the architecture, `epics.md` and the spines finds only the OSV fetch scope ("the CVEs/aliases in fleet findings", `PA/epics.md:1283`).
- **Impact:**
  - The Story 2.4 developer has to invent the stored ID scheme.
  - That choice changes issue counts (one CVE can split into two issues), Needs attention (a missed KEV join means "Actively exploited" never lights) and Exposure answers.
  - Changing the scheme after Epic 2 means migrating stored findings and history.
- **Smallest fix:** add one rule to the ARCH38 / "Issues and review" text and to the Story 2.4 and 6.2 ACs. For example: run Grype with `--by-cve` (or store `relatedVulnerabilities`), key the issue on the CVE where one exists, else on the original ID, keep every alias on the finding, and join KEV and Exposure queries on any alias; the Grype DB lookup (finding 20) also resolves aliases.
- **Owner:** bmad-architecture (amendment), then bmad-correct-course (2.4, 4.3, 6.2 ACs).

### Concerns — Epic 1 (next stories)

**2. CONCERN — The Story 1.1 spec is stale, and the current Story 1.1 ACs leave two CI and dev-loop details undefined (the second part is new).**
- **Stories:** 1.1, 1.2.
- **Stale spec:**
  - It still uses kind and Podman: `IA/spec-1-1-…md:25` "a Skaffold `kind` dev loop"; `:42` "local Podman machine"; `:70` AC-8 "`skaffold dev -p kind`"; `:72` AC-10 "against a kind deployment"; `:74` AC-12.
  - Its Code Map cites old line ranges: `architecture.md:379-456` (the tree is now at `PA/architecture.md:394`) and `epics.md:310-359` (Story 1.1 is now at `PA/epics.md:336`).
  - This is gated: the spec is `status: 'draft'` (`:5`), and its change log (`:174`) requires a re-plan at CHECKPOINT 1. RCR:830 says the planned re-plan picks up A9.
- **New:**
  - The "fast tier" is never defined. `PA/epics.md:377` says "runs the fast tier on GitHub-hosted runners for every event"; `PA/architecture.md:201` and ARCH23 (`PA/epics.md:138`) name it but list no checks.
  - Story 1.2 depends on "the Skaffold `ci` profile from Story 1.1" (`PA/epics.md:403`), and "CI runs the same task" (e2e, `:373`) needs a deployment in CI. But no Story 1.1 AC requires the `ci` profile; only ARCH34 does (`PA/epics.md:158` "A `ci` profile deploys to a temporary namespace from ARC runners").
- **Fix:** in the 1.1 re-plan, rewrite AC-8/10/12, the VALs and the Code Map from `PA/epics.md:336-384`. Name the fast-tier steps (for example fmt, clippy, unit tests without `#[sqlx::test]`, web lint/svelte-check/Vitest, gen drift) and add the `ci` profile and its CI e2e use to the ACs.
- **Owner:** Story 1.1 Build planning (bmad-build).

**3. CONCERN — The sign-in page is not designed.**
- **Stories:** 1.3, 1.4.
- **Evidence:**
  - `PA/epics.md:443` "signs in with it on the sign-in page".
  - `rg -i "sign.?in"` finds no sign-in state in EXP or DES (only EXP:262 and EXP:270, which are unrelated).
  - Undefined: the layout; bootstrap form vs "Sign in with SSO" (1.4); the "generic message"; the no-role denial copy (1.4); the theme before any preference exists.
- **Fix:** add a sign-in state to EXP State Patterns, or record "minimal page, Light, catalogue strings" as the 1.3 default.
- **Owner:** bmad-ux, before 1.3 Build.

**4. CONCERN — Global states (session expired, control plane unreachable, a forbidden deep link) are not designed, and no story gates on them.**
- **Stories:** 1.3, 1.6 (and every surface).
- **Evidence:**
  - EXP:517 (Open item 31) "session expired and re-authentication; control plane unreachable …; a direct link to a Settings panel or action the role cannot use".
  - Story 1.3 defines only the API: "an expired session returns 401" (`PA/epics.md` Story 1.3 session AC).
  - No story cites Open item 31.
- **Fix:** gate 1.6 on Open item 31, or record an interim rule (401 → sign-in with a return URL).
- **Owner:** bmad-ux / 1.6 Build planning.

**5. CONCERN — Settings → Access "users/roles view" has no data source.**
- **Story:** 1.6.
- **Evidence:**
  - `PA/epics.md:546` "Settings → Access (the read-only resolved auth configuration and the users/roles view)".
  - EXP:123 "Access (users and roles …)".
  - The only auth stores are `sessions`, `user_preferences` and `GET /api/v1/auth/config` (ARCH16, `PA/epics.md` ARCH16). Declarative OIDC has no user directory.
- **Fix:** reduce it to "role mapping (read-only)" from auth/config, or define a seen-users read model.
- **Owner:** bmad-architecture + bmad-ux, before 1.6 Build.

**6. CONCERN — The icon-rail width is not a token, but lints enforce tokens and Story 1.7 builds and tests the rail.**
- **Stories:** 1.5, 1.7.
- **Evidence:**
  - EXP:519 (Open item 33): "some dimensions are untokenised (… the icon-rail width …)".
  - `PA/epics.md:517` requires the layout tokens to match DESIGN.md; `:592` builds the icon rail.
  - DES:684 describes the rail with no width.
- **Fix:** add `spacing.icon-rail-width` to DES, or gate 1.7 on Open item 33.
- **Owner:** bmad-ux.

### Concerns — Epic 2

**7. CONCERN — The "Connect a registry" copy-paste one-liner does not exist, and the artifacts disagree on whether connections are declarative.**
- **Stories:** 2.9, 2.2.
- **Evidence:**
  - `PA/epics.md:914` "the setup action "Connect a registry" with its copy-paste one-liner in a code block with Copy"; EXP:251 "copy-paste one-liners in mono".
  - Story 2.2 adds a registry only through a form: `PA/epics.md:714` "an admin adds a registry (URL, auth type, read-only credentials) and runs "Test connection"".
  - Yet ARCH22 (`PA/epics.md:137`) and `PA/architecture.md:473` say chart values cover "connections", and no story builds Helm-declared connections.
- **Impact:** the developer must invent the command (a curl to the API, or a Helm `--set`, which would mean building declarative connections) or drop it.
- **Fix:** UX picks "button to Settings → Connections", or architecture names the command and a story builds it.
- **Owner:** bmad-ux + bmad-architecture, before 2.9 Build.

**8. CONCERN — No rule for when the Home summary may say "You are in good shape".**
- **Stories:** 2.9, 2.10, 4.7.
- **Evidence:**
  - EXP:57, EXP:140 and EXP:409 use "You are in good shape. 3 things need attention today."
  - EXP:136 "Definitive only when the data earns it".
  - `PA/epics.md:900` asks only for "one plain summary line". Only the stale caveat and All clear have rules.
- **Fix:** add the summary-line rules (thresholds on coverage and needs-attention) to EXP State Patterns and gate 2.9.
- **Owner:** bmad-ux.

**9. CONCERN — The order of Home's Needs attention list is undecided (Open item 21), and the other artifacts imply a different order.**
- **Stories:** 2.10, 5.2, 5.4.
- **Evidence:**
  - EXP:504 "Home Needs attention order (drawn: exploited, licence, Critical) — not decided; the Licences-at-top rule covers the Issues list … only".
  - Story 2.10 renders the list with no order and no gate (`PA/epics.md:926`).
  - Story 5.2 says Home "use[s] the same groups, order and counts" (`PA/epics.md:1535`), and `PA/architecture.md:257` says `needs_attention=true` returns groups "in the same order" (the Issues order, Licences first).
  - RCR:812 (Q5) leaves open whether Save and next follows the Issues order or Home's.
- **Fix:** decide the order (simplest: the Issues order everywhere) and state it in 2.10.
- **Owner:** bmad-ux.

**10. CONCERN — Open item 18 behaviours are built without a gate (Open-issues row click, "N more" rows with the pager).**
- **Stories:** 2.10, 2.11, 5.2.
- **Evidence:**
  - EXP:501.
  - UX-DR14 (`PA/epics.md:201`) "What a click on those rows does is not drawn (EXPERIENCE Open item 18)".
  - Story 5.2 builds "N more High" rows (`PA/epics.md:1525`). Only the Add software destination is gated (`:950`).
- **Fix:** add a "set by UX before Build" gate (Open item 18) to 2.10 and 5.2.
- **Owner:** bmad-correct-course / bmad-ux.

**11. CONCERN — Undrawn or orphaned detail tabs and cells (Open items 14, 15, 32), with no gates or owners.**
- **Stories:** 2.10, 2.11, 5.2, 5.5, 6.3, 6.5, 9.5.
- **Evidence:**
  - EXP:497-498 and EXP:518.
  - 2.10's "How to fix and Details wait for UX (EXPERIENCE Open item 14)" (`PA/epics.md:932`); no later story builds them.
  - 6.3's "Home's Exposure tab (a reduced summary …)" is undrawn and ungated (`PA/epics.md:1780`).
  - 2.11's Data quality "what it shows before a score exists is EXPERIENCE Open item 32" (`PA/epics.md:956`); the only gate is Story 8.1.
  - UX-DR22's Overview Exposure cell (`PA/epics.md:212`) and UX-DR25's Software "Audit report" button (`PA/epics.md:215`) have no story.
- **Fix:** gate each AC, or state minimal content; assign or defer the orphans explicitly.
- **Owner:** bmad-ux + bmad-correct-course.

**12. CONCERN — No rule for classifying packages as Direct or Indirect.**
- **Stories:** 2.11, 6.4, 6.6.
- **Evidence:**
  - UX-DR25 "Direct / Indirect" (`PA/epics.md:215`).
  - 6.4 edge labels "direct · in 12"; 6.6 "How it got it".
  - The architecture has no derivation from Syft relationships.
- **Fix:** record the derivation and an "unknown" fallback in the architecture.
- **Owner:** bmad-architecture / 2.11 planning.

**13. CONCERN — UI read-model and API contracts are unnamed: issue ID and URL, group detail, the decisions path, exports POST/download, packs, the neighbours shape and node IDs, and a non-unique Software route.**
- **Stories:** 2.10, 2.11, 5.1–5.4, 5.8, 6.5, 6.6, 9.5.
- **Evidence:**
  - `PA/architecture.md:257` gives a composite key but no group ID or path.
  - `PA/epics.md:1504` puts the order explanation on "`GET /api/v1/findings/{id}`". A finding is a place, but order is per group.
  - `PA/epics.md:1881` names `GET /api/v1/graph/neighbours` with no shape; `PA/architecture.md:267` says "the `graph` neighbours API".
  - UX-DR25 routes `/software/<name>` (`PA/epics.md:215`), which is not unique per digest or version.
- **Fix:** add a short "UI read models" subsection to the architecture. Under OpenAPI-first each story could also define its own, but the issue ID and URL are shared by 2.10, 5.x and 6.x, so fix those in 2.10 planning at the latest.
- **Owner:** bmad-architecture.

**14. CONCERN (new) — The readiness change record says its open questions are "gated by their stories", but no story AC carries Q1, Q2, Q4 or Q5. Its success criterion 8 is not met.**
- **Stories:** 2.10 (Q2, Q4), 5.4 (Q5), 6.3 (Q1).
- **Evidence:**
  - RCR:758 "8. Every open question in section 6 has an owner and a gate."
  - The gates exist only in the table:
    - RCR:808 (Q1) → "Story 6.3 Build"
    - RCR:809 (Q2) → "Story 2.10 Build (Grype DB only); Story 4.4 planning"
    - RCR:811 (Q4) → "Story 2.10 Build"
    - RCR:812 (Q5) → "Story 5.4 Build"
  - `rg -n "Q[1-7]\b" PA/epics.md` finds no match. Stories 2.10 (`:926-938`), 4.4 (`:1278-1296`), 5.4 (`:1581-1601`) and 6.3 (`:1782-1784`) carry no such gate.
  - Only Q6 is carried (`PA/epics.md:620`). Q3 and Q7 are answered (RCR:800).
  - This is the same pattern that sank criterion 9 last time (lens C 20).
- **Fix:** add "set by UX before Build (Q4; Q2 cut and label)" to 2.10, Q2 precedence to 4.4, Q5 to 5.4 and Q1 to 6.3.
- **Owner:** bmad-correct-course.

### Concerns — Epic 5

**15. CONCERN — Earlier change-record questions are still ungated or only softly gated: O2 and O20 are ungated, and O14 and O19 are soft.**
- **Stories:** 6.3, 6.5, 4.9, 7.4.
- **Evidence:**
  - O2: `PA/architecture.md:556` "whether files are signed. _Open — Story 6.5 planning (O1, O2)_"; Story 6.5 carries only O1 (`PA/epics.md:1843`).
  - O20: the label "Audit report for this answer" is used at `PA/epics.md:1779`, `:1846`, `:1882` and `:2314` with no gate (`rg "O20|Open item 39"` finds none).
  - O14: "copy to confirm with UX, O14" (`PA/epics.md:1429`).
  - O19: "styling per U19, O19" (`PA/epics.md:2028`). Neither has a "before Build" clause.
- **Fix:** add O2 and O20 to the 6.5 planning AC (and O20 to 6.3), and reword O14 and O19 as "set by UX before Build".
- **Owner:** bmad-correct-course.

**16. CONCERN — The Reports → Audit trail architecture contract is missing, and O16 is gated only for the broken-chain state.**
- **Stories:** 5.5, 9.6, 9.9.
- **Evidence:**
  - `PA/epics.md:1622` "verified 4 min ago … the layout and wording of the broken-chain state are set by UX before Build (O16)".
  - Only `GET /api/v1/evidence/verification` exists, and it recomputes on call (Story 2.1). There is no list endpoint, no subject→label model and no verification schedule.
  - DES:740 "[ASSUMPTION, EXPERIENCE Open item 36]".
- **Fix:** add the ledger list endpoint, the subject model and the verification cadence to the architecture; widen the 5.5 gate to all of Open item 36 and gate 9.6 and 9.9.
- **Owner:** bmad-architecture + bmad-ux.

**17. CONCERN — No rule for concurrent review decisions (Open item 30).**
- **Stories:** 5.3, 5.4, 5.8.
- **Evidence:**
  - EXP:516 "two people reviewing the same issue at once … has no rule".
  - `PA/epics.md:1557` "it supersedes the old one". No expected-version or 409 rule exists, so the last writer silently wins on evidence-grade data.
- **Fix:** record a 409 / expected-version rule and its inline copy, or accept last-writer-wins explicitly as an [ASSUMPTION] gated in 5.3.
- **Owner:** bmad-architecture + bmad-ux.

**18. CONCERN (new) — Vendor VEX claims are left out of the new effective-status rule, so counts, Needs attention, filters and emitted VEX are undefined once Story 5.7 lands.**
- **Stories:** 5.7 (and 5.2, 5.6, 2.10).
- **Evidence:**
  - B2 defines effective status from team decisions only: `PA/architecture.md:257` "A place's effective status is its own `artifact` decision if present, else the issue-wide status; status filters, Needs attention and VEX … use effective statuses".
  - 5.7 "applies" vendor claims: `PA/epics.md:1672` "the finding shows a vendor-attributed status ("Not impacted — per <vendor> VEX, <date>") … the team can still record their own decision, which takes precedence".
  - FR15 says the claims are "applied … to fleet findings" (`PA/epics.md:55`).
  - Not stated: whether a vendor not-affected place still counts as Not reviewed yet or Needs attention, matches which status filter, counts toward Mixed N, or is re-emitted in our VEX.
  - The 5.7 gate covers only the presentation ("designed before this story starts Build", `PA/epics.md:1676`).
- **Fix:** extend the ARCH38 effective-status sentence with the vendor-claim rule in the 5.7 planning gate.
- **Owner:** bmad-architecture / 5.7 planning.

**19. CONCERN — Forward dependencies: several ACs reference UI that later stories build.**
- **Stories:** 5.4, 6.3, 6.4, 9.9.
- **Evidence:**
  - 5.4: "the Review buttons on Home, the Exposure inspector and Software" (`PA/epics.md:1595`) and "the places count with "See the map"" (`:1583`). Exposure arrives in Epic 6.
  - 6.3: "When the user chooses Review in the inspector" (`PA/epics.md:1795`). The inspector arrives in 6.6.
  - 6.4: "the same layout as a moved map (Story 6.6 …)" (`PA/epics.md:1816`).
- **Fix:** phrase these as "when Story 6.x lands", or move the inspector into 6.4.
- **Owner:** bmad-correct-course.

### Concerns — Epic 6

**20. CONCERN (new) — How Armoury asks the Grype DB whether it "has a record" for an ID (and reads its metadata) is not recorded, although B4 makes that check decide unknown versus zero.**
- **Stories:** 6.2, 6.3.
- **Evidence:**
  - `PA/architecture.md:336` "Only a known vulnerability — one with a record in the active Grype DB — gets the coverage-scoped zero".
  - `PA/epics.md:1761-1763` "a CVE that matches no fleet package … still includes the CVE's metadata from the Grype DB".
  - `PA/architecture.md:282` "Armoury never reads the Grype SQLite schema itself". Scan JSON contains only matched vulnerabilities.
  - A CLI path exists: local Grype 0.120.1 `grype db search --help` shows "Search for affected packages by vulnerability ID: $ grype db search --vuln …".
- **Fix:** in 6.2 planning, record `grype db search --vuln <id> -o json` through `tools` against the active DB directory (alias-aware, see finding 1), and its cost under NFR2.
- **Owner:** bmad-architecture / 6.2 planning.

**21. CONCERN — Export is placed only on Exposure. Its placement on Issues and Software, the JSON choice, the CSV row unit (issue or place) and the stored-export detail (Open item 15) are not defined.**
- **Story:** 6.5.
- **Evidence:**
  - UX-DR21 (`PA/epics.md:208`) puts Export on "Exposure, Issues and Software".
  - DES places it only in the Exposure header (DES:724).
  - Open item 15 covers the export detail (EXP:498).
  - Story 6.5 lists "the Export row" for errors.
- **Fix:** add the placement and format choice to EXP, and the CSV row unit to ARCH39.
- **Owner:** bmad-ux / 6.5 planning.

**22. CONCERN — The Exposure query grammar is undefined for version ranges and for moved centres in the URL.**
- **Stories:** 6.2, 6.3, 6.6.
- **Evidence:**
  - `PA/epics.md:1738` "a package with a version range (for example `log4j-core@2.x`)".
  - `:1882` "the URL (`&from=` the previous step) … restores that map".
  - No grammar exists for package, vulnerability or place centres, and there is no header copy for a range.
- **Fix:** add the query and URL grammar to the architecture and the header copy to EXP.
- **Owner:** bmad-architecture + bmad-ux.

**23. CONCERN — The moved-map Table sits outside the Story 6.6 UX gate.**
- **Story:** 6.6.
- **Evidence:** `PA/epics.md:1904` "the Table of a moved map is not drawn (EXPERIENCE Open item 19)". The gate covers only other centres and long trails.
- **Fix:** include the Table in the 6.6 gate.
- **Owner:** 6.6 planning.

### Concerns — later epics (carried and regraded; none blocks Epics 1, 2, 5 or 6)

**24. CONCERN — FR32/FR33 follow-through is incomplete.**
- **Stories:** 4.10, 10.2, 10.3.
- **Evidence:**
  - The 4.10 amendment covers only "how the Sigstore trusted root reaches air-gapped instances" (`PA/epics.md:1454`). It does not cover connected-mode refresh, or a keyless `cosign verify` in `inventory` calling the TUF CDN and Rekor, which conflicts with ARCH19 ("called only by `feeds`, `enrichment` and `signing`").
  - Story 10.2 bundle variants omit end-of-life data (`PA/epics.md:2480`).
  - The 10.3 endpoint list omits the end-of-life source (`PA/epics.md:2510`).
  - Story 4.10 does not restate O13; Story 4.9 does (`:1430`).
- **Fix:** widen the 4.10 amendment AC, and add end-of-life data to 10.2 and 10.3.
- **Owner:** bmad-correct-course / bmad-architecture.

**25. CONCERN — Audit-report regeneration (Open item 22) is ungated, and the Software "Audit report" action is undefined.**
- **Story:** 9.5.
- **Evidence:**
  - `PA/epics.md:2280` "which regenerates the pack".
  - EXP:505.
  - It is not decided whether the first signed pack is kept, superseded or cancelled.
- **Fix:** add a UX + architecture gate to 9.5.
- **Owner:** bmad-ux + bmad-architecture.

**26. CONCERN — Turning "triage licence warnings" off breaks counts.**
- **Story:** 7.4.
- **Evidence:** `PA/epics.md:2023` "warnings stay visible but have no review panel". They stay Not reviewed yet forever, which inflates the default Issues filter and "N not reviewed yet". Their effective status (B2) is undefined.
- **Fix:** define the count and status treatment in ARCH38/UX, or drop the setting.
- **Owner:** bmad-ux / 7.4 planning.

### Notes

**27. NOTE — The O17 Help placeholder copy has no gate.** Downgraded from a concern: it is copy only. Evidence: `PA/epics.md:537` "Help opens a placeholder until its screen is designed (EXPERIENCE Open item 24, O17)"; `:240` "copy to confirm with UX — O17". A neutral placeholder string in the catalogue is enough. Owner: bmad-ux.

**28. NOTE — Epic 1 builds explicit [ASSUMPTION] defaults without a gate.**
- The defaults: Open item 3 (no OS-preference detection), Open item 6 (Settings panel list), Open item 25 (AA only) and Open item 2.
- Each default is stated, so nothing has to be invented. Evidence: `PA/epics.md:189` (UX-DR4), `:218` (UX-DR28), UX-DR1. Later stories do the same (Open items 5 and 12).
- Accept them at this gate, or have UX confirm them. Owner: bmad-ux.

**29. NOTE — A stale [ASSUMPTION] tag remains on a decided rule.**
- UX-DR16 (`PA/epics.md:203`) "A later all-places decision does not overwrite … ([ASSUMPTION], EXPERIENCE Open item 9)" and Story 5.8 (`:1697`) still tag the survival rule.
- ARCH38 decides it: `PA/architecture.md:257` "a later `all_places` decision leaves per-artifact decisions in place".
- Owner: bmad-ux.

**30. NOTE — Two small Story 1.8 wording issues.**
- `PA/epics.md:611` "a test asserts every registered keyboard shortcut also has a palette entry". Taken literally, J/K/Esc/⌘↵/Backspace need palette entries; state which shortcuts are exempt.
- `:619` "after `G`" should be `g` (`:191`).
- Owner: 1.8 planning.

**31. NOTE — Epic 1 coverage claims and context drift.**
- Epic 1 claims UX-DR29 and UX-DR41–44 (`PA/epics.md:290`), but no Epic 1 story builds the code block (UX-DR42) or the setup actions.
- `PA/epics.md:541` "setup actions arrive with Stories 2.2 and 3.2", but the registry action is built in 2.9 (`:914`).
- `IA/epic-1-context.md:102` "uppercase only on button labels" omits the Graph/Table switch and zoom labels that UX-DR2 allows.
- Owner: bmad-correct-course (editorial).

**32. NOTE — Both change records still record approval as pending, although their frontmatter says approved and applied.**
- RCR:845 "6.3 User approval | [!] | Pending … Status stays `draft`" vs RCR:2 `status: approved` and RCR:4 `applied: 2026-11-07`.
- CR7:2995 has the same issue.
- Owner: bmad-correct-course (editorial).

**33. NOTE — A stale "(open)" remains in architecture.md.**
- `PA/architecture.md:73` "Agent state-recovery model (open)".
- ARCH9 has since decided stateless re-derive.
- Owner: bmad-architecture.

**34. NOTE — Auditor access to "Audit report for this answer" is not stated.**
- Story 6.5's auditor AC covers only "export".
- The answer report shares the "Audit report" label, and Generate audit report is absent for auditors (UX-DR31, `PA/epics.md:224`).
- Owner: 6.5 planning.

**35. NOTE — The dev-cluster prerequisites are external but recorded.**
- Stories 1.1 and 1.2 assume the dev cluster: in-cluster BuildKit, the dev registry, ARC runners, the AGE Pod, and a CNI that enforces NetworkPolicy egress.
- These are Daniel's dependency under Agent Readiness OI-3 (`PA/sprint-change-proposal-2026-11-06.md:67-71`).
- Not a planning gap. Confirm they are in place before 1.1 VAL-9/11/12 run.

## Regrading of the earlier ~45 concerns (lenses A, B and C)

- **Upgraded to blocker:** lens A 5 (the alias rule), now finding 1, because B4 made the Grype DB the sole judge of "known".
- **Closed by RCR:** lens A 16 (Open items 4 and 9 for the filter), lens B 7 and 8, lens C 1 and 2.
- **Downgraded to note:** lens C 7 (O17), now finding 27.
- **Still concerns** (story-local; each story's planning or a UX gate can resolve them):
  - lens A 4, 6–13, 15, 17–20;
  - lens B 5, 6, 9–18, 20–25;
  - lens C 3–6, 8–19.
  - They are merged above as findings 2–13, 15–17, 19 and 21–26.
- **New in this pass:** findings 14, 18 and 20, plus the parts of finding 2 about the fast tier and the `ci` profile.
