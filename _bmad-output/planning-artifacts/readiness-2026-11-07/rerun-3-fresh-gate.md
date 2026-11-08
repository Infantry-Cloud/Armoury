# Readiness rerun 3 — Lens 2: fresh gate pass (Epic 1; Epics 2, 4, 5, 6)

Read-only review, 2026-11-07, after `sprint-change-proposal-2026-11-07-aliases.md` was applied.
Gate question: could a developer implement these epics without inventing decisions that nothing records?
Paths: PA = `_bmad-output/planning-artifacts/`, IA = `_bmad-output/implementation-artifacts/`,
EXP / DES = `PA/ux-designs/ux-Armoury-2026-11-06/EXPERIENCE.md` / `DESIGN.md`, ACR = `PA/sprint-change-proposal-2026-11-07-aliases.md`,
RCR = `PA/sprint-change-proposal-2026-11-07-readiness.md`. I checked line numbers with `rg -n` on the current files.

Mechanical checks I ran:
- `sprint_plan.py generate --dry-run`: `in_sync: true`, 11 epics, 79 stories, 0 orphans.
- `validate_story_contract.py validate --phase draft` on the Story 1.1 spec: VALID.
- ACR success criterion 2 (the grep for stale wording) finds nothing.
- ACR success criterion 3: `--by-cve` appears at `architecture.md:257`, `:282`, ARCH7 (`epics.md:111`), ARCH38 (`:166`) and Story 2.4 (`:783`). `grype db search --vuln` appears at `architecture.md:336` and in Story 6.2 (`epics.md:1774`, `:1784`). The Q1/Q2/Q4/Q5 planning ACs are at `epics.md:926`, `:930`, `:1290`, `:1538`, `:1600` and `:1799`.
- Grype 0.120.1, installed locally (`~/.local/share/mise/installs/grype/0.120.1`), has `--by-cve`, `db search --vuln`, `db search vuln` and `db diff`. No local DB is installed, so I could not test alias behaviour.

## Verdict suggestion

**CONCERNS. Blocker 9 is closed, no new blocker was found, and Epic 1 (Stories 1.1–1.9) can start.** Story 1.1 still needs its planned Build re-plan.

Before Story 2.4 starts Build, add one-line planning ACs that carry the open alias questions ACR N1–N6 and N9 into their stories (finding 1). Without them, ACR's own success criterion 8 is not met. This is the same pattern that the last rerun's finding 14 caught.

Counts: **0 blockers · 25 concerns · 11 notes.**

### Blocker 9 (vulnerability ID aliases) is closed (verified)

- **Rule:** recorded once, at `architecture.md:257`: "Vulnerability IDs and aliases (decided 2026-11-07, readiness blocker 9): Grype runs with `--by-cve` … Each finding stores every alias … KEV matching, the enrichment joins …, Exposure queries, the unknown-vulnerability check … and ⌘K search match on any alias".
- **Grype invocation:** `architecture.md:282`.
- **Unknown rule and lookup:** `architecture.md:336`.
- **PRD glossary:** `prd.md:177`.
- **Stories:**
  - 2.4 (`epics.md:783-786`)
  - 2.10 (`:942`, the key ID)
  - 4.3 (KEV/EPSS on any alias)
  - 4.4 (CVE List/OSV on any alias)
  - 6.2 (`:1762`, `:1774`, `:1784-1785`)
  - 6.3 (alias gives the same answer; unknown state)
- **UX:** DES:719; EXP:99, `:110`, `:157`, `:226`, `:255-256`.

**The CVE-day false zero is gone.** A CVE query now matches findings keyed by GHSA through their aliases. The zero answer also needs affected-package data under the queried ID or one of its aliases.

### The cheap concerns from the last rerun are closed (verified)

- **Vendor VEX display-only:** `architecture.md:203`, `:257`; Story 5.7 `epics.md:1695-1696`; Story 11.4 `:2673` (N7 applied).
- **Lookup method:** `architecture.md:336`; `epics.md:1784`.
- **Fleet-wide Needs-attention count:** `architecture.md:257`; UX-DR38 `epics.md:235`; Story 5.2 `:1547`.
- **Stale [ASSUMPTION] removed:** Story 5.8 `:1721` and EXP:489 (Open item 9 resolved).
- **Q1, Q2, Q4 and Q5 gated:** 2.10, 4.4, 5.2, 5.4 and 6.3.

## Findings

### Concerns — fix before Story 2.4 Build (Epics 2, 4, 5, 6 data model)

**1. CONCERN (high) — The alias change record's own open questions (N1–N6, N9) are named as "gated by Story X planning", but no story AC and no architecture text carries them.** This repeats rerun-2 finding 14.

- **Stories:** 2.4 (N1, N2, N3), 4.2 (N3), 5.2 (N4, N9), 5.3 (N3), 5.6/5.7 (N6), 6.1 (N2), 6.2 (N5), 6.3 (N4).
- **What the change record promises:**
  - ACR:659-667 lists N1–N9 with gates such as "Story 2.4 planning (before Story 5.3 stores decisions)" (N3).
  - ACR:570 gives the Architect this step: "Check N1–N3 and N5 are listed for Story 2.4 and 6.2 planning".
  - ACR:591 (criterion 8): "every gate named there is carried by a story AC or by an owner's planning step".
- **What the files hold:** `rg -n "\bN[1-9]\b"` over `architecture.md`, `epics.md`, both spines and the PRD finds **nothing**. Story 2.4 (`epics.md:765-795`) has no planning AC. Neither do 4.2 (`:1223`), 5.3 (`:1560`), 6.1 (`:1733`) or 6.2 (`:1754`).
- **N3 is the risky one: key drift.** A finding keyed on a GHSA ID can gain a CVE after a DB update. Under `--by-cve` its group key then changes.
  - Story 4.2 (`epics.md:1243`) marks findings "no longer matched … resolved-by-feed" and adds new ones.
  - Story 5.3 (`:1588`) promises that a reappearing finding keeps its decisions.
  - Nothing says whether decisions attach to the key ID or to the set of aliases. A Not-impacted decision can therefore silently fall back to Not reviewed yet and re-enter Needs attention.
- **Why this is not a blocker:**
  - Story 2.4 already stores every alias (`epics.md:786`).
  - Decisions are first stored in Story 5.3.
  - So Story 2.4 or 5.3 Build planning can still settle N3 without migrating data.
- **Fix:** add one "Given open question Nx … When this story is planned … Then recorded in architecture.md and approved" AC to each story: 2.4 (N1–N3), 5.3 (N3: decisions match on any alias), 6.1 (N2), 6.2 (N5 remainder), 5.2 and 6.3 (N4, N9), and 5.6/5.7 (N6).
- **Owner:** bmad-correct-course (story ACs) + bmad-architecture.

**2. CONCERN (new) — `--by-cve` changes which vulnerability record Grype reports, and so the severity and description Armoury shows. Nobody analysed this.**

- **Stories:** 2.4, 2.10, 5.1.
- **Evidence:**
  - Grype help (0.120.1): "`--by-cve` orient results by CVE instead of the original vulnerability ID when possible".
  - Story 2.4 stores "typed severity — every level Grype reports … Unknown or no severity becomes the `unrated` group" (`epics.md:784`).
  - The issue sentence is "the record's description field" (`architecture.md:257`).
  - Needs attention depends on "severity critical" (`architecture.md:257`).
  - ACR has no severity analysis: `rg -i severity` on ACR finds only the Q4 marker lines (ACR:300-309).
  - The only severity-source precedence gate is in Story 5.1 (`epics.md:1511`), which comes after Epic 2.
- **Impact:**
  - When a GHSA advisory is reported as its CVE record, the severity and description may come from the CVE record. A recent CVE that NVD has not scored yet would then land in "Not rated yet" instead of Critical. It would drop out of Needs attention in Epic 2, the CVE-day case.
  - I did not verify this mechanically (no Grype DB locally). Also check how Grype treats a GHSA ID that relates to more than one CVE. The architecture rule "the CVE ID when the vulnerability has one" may not match what the tool emits.
- **Fix:** in Story 2.4 planning, record from a fixture which record's severity and description are stored under `--by-cve`, and whether Epic 2 uses the highest severity across related records. Bring that into the Story 5.1 precedence amendment.
- **Owner:** bmad-architecture (2.4 planning).

**3. CONCERN — Parts of N5 (the unknown-vulnerability lookup) are left to Story 6.2 with no gate.**

- **Stories:** 6.2, 6.3, 6.7.
- **Evidence:**
  - Story 6.2 requires "`grype db search --vuln <ID>` returns affected packages for the queried ID or any alias of it" (`epics.md:1774`, `:1785`).
  - ACR:663 leaves these open: "whether the command resolves aliases itself, its cost per query under NFR2, and whether the same call supplies the metadata".
  - Local help shows `--vuln` filters affected-package rows. `db search vuln ID` (schema v6+) is a separate command.
- **Impact:**
  - A GHSA query whose alias exists only in the DB, not on any fleet finding, needs some way to resolve the alias. Without one, a vulnerability the DB knows comes back as "no data". The developer has to choose: `db search vuln` related IDs, or OSV/CVE List aliases from Story 4.4.
  - Nothing orders the known check against fleet matches. For example, a CPE-only record could have fleet findings yet "no affected packages".
- **Fix:** carry this in the finding 1 gate for 6.2. State that a query with fleet matches is always known.
- **Owner:** bmad-architecture (6.2 planning).

### Concerns — Epic 1

**4. CONCERN — The Story 1.1 spec is stale. Its re-plan handoff lives only in change records, and the Skaffold `ci` profile is in no Story 1.1 AC.**

- **Stories:** 1.1, 1.2.
- **Stale spec:**
  - Kind/Podman remains at IA/spec-1-1:25, `:42`, `:58`, `:70` (AC-8), `:72` (AC-10), `:74` (AC-12), `:108`, `:119` and `:134`.
  - The Code Map cites old ranges: `architecture.md:379-456` and `:282-360` "LoB rules" (now the Grype bullet), and `epics.md:310-359` (Story 1.1 is now at `:337`).
- **Gated:**
  - `status: 'draft'` (spec:5).
  - Spec change log (spec:174) requires a re-plan.
- **Not carried into the spec:**
  - The second rerun's CI items reach the re-plan only through ACR:575 (step 7) and the readiness record. The spec change log (spec:172-174) does not mention them.
  - Story 1.2 needs "the Skaffold `ci` profile from Story 1.1" (`epics.md:404`), but Story 1.1's ACs (`:337-386`) never name it; only ARCH34 does.
- **Partly closed:** the "fast tier" is now defined in `docs/agent-readiness.md:130-139` (secrets, rust, test-rust without DB, web, chart, api), but not in `epics.md` or `architecture.md`.
- **Fix:** at the re-plan, rewrite AC-8/10/12, VAL-9/11 and the Code Map from `epics.md:337-386`. Add the `ci` profile AC and cite the fast-tier table. Add a spec change-log line pointing to ACR step 7.
- **Owner:** bmad-build (1.1 re-plan).

**5. CONCERN — The sign-in page is not designed.**

- **Stories:** 1.3, 1.4.
- **Evidence:**
  - `epics.md:444` "signs in with it on the sign-in page".
  - `rg -i "sign.?in"` in EXP/DES finds only the journey text (EXP:375, `:398`) and no state or layout.
  - Undefined: the bootstrap form vs "Sign in with SSO", the generic failure copy, the copy for a user with no role, and the theme before any preference exists.
- **Fix:** add a sign-in state to EXP State Patterns, or record "minimal page, Light, catalogue strings" as the 1.3 default.
- **Owner:** bmad-ux.

**6. CONCERN — Global states (session expired, control plane unreachable, a forbidden deep link) are undesigned and gated nowhere.**

- **Stories:** 1.3, 1.6.
- **Evidence:**
  - EXP:517 (Open item 31).
  - `rg "Open item 31" epics.md` finds no match.
  - Story 1.3 defines only "an expired session returns 401".
- **Fix:** gate 1.6 on Open item 31, or record the interim rule: 401 → sign-in with a return URL.
- **Owner:** bmad-ux / 1.6 planning.

**7. CONCERN — The Settings → Access "users/roles view" has no data source.**

- **Story:** 1.6.
- **Evidence:**
  - `epics.md:547` "the read-only resolved auth configuration and the users/roles view".
  - The only auth stores are `sessions`, `user_preferences` and `GET /api/v1/auth/config` (IA/epic-1-context.md:58-64). Declarative OIDC has no user directory.
- **Fix:** narrow it to "role mapping (read-only)", or define a seen-users read model.
- **Owner:** bmad-architecture + bmad-ux.

**8. CONCERN — The icon-rail width is not a token, but Story 1.7 builds and tests the rail under token lints.**

- **Stories:** 1.5, 1.7.
- **Evidence:** EXP:519 (Open item 33); DES:684 gives no width; `rg "Open item 33" epics.md` finds no match.
- **Fix:** add a `spacing` token, or gate 1.7 on Open item 33.
- **Owner:** bmad-ux.

### Concerns — Epic 2

**9. CONCERN — The "Connect a registry" one-liner does not exist.**

- **Story:** 2.9.
- **Evidence:**
  - `epics.md:916` "with its copy-paste one-liner in a code block".
  - UX-DR29 (`:223`) and EXP:251 say the same.
  - Story 2.2 adds registries only through a form (`epics.md:715`), and no story builds Helm-declared connections.
- **Fix:** UX picks a button that opens Settings → Connections, or the architecture names the command.
- **Owner:** bmad-ux + bmad-architecture.

**10. CONCERN — No rule says when the summary may read "You are in good shape".**

- **Stories:** 2.9, 2.10, 4.7.
- **Evidence:**
  - EXP:57, `:140`, `:409`.
  - UX-DR22 `epics.md:213`.
  - Only the stale-feed exclusion exists (`epics.md:1377`).
- **Fix:** add threshold rules to EXP State Patterns and gate 2.9.
- **Owner:** bmad-ux.

**11. CONCERN — The order of Home's Needs attention list is "not decided" in UX, yet decided by implication elsewhere. Story 2.10 builds the list with no gate.**

- **Stories:** 2.10, 5.2, 5.4.
- **"Not decided":**
  - UX-DR22 `epics.md:213` and UX-DR38 `:235`: "The order within Home's Needs attention is not decided (EXPERIENCE Open item 21)".
  - EXP:504.
- **Decided by implication:**
  - Story 5.2 `epics.md:1554` "they use the same groups, order and counts".
  - `architecture.md:257` "`needs_attention=true` … in the same order".
  - Story 2.10 (`:936`) gives no order. It is built before `ranking` (Story 5.1) exists.
- **Fix:** close Open item 21 with "Issues order everywhere", and state the interim order in 2.10.
- **Owner:** bmad-ux.

**12. CONCERN — Open item 18 behaviours (Open-issues row click, "N more" rows) are built without a gate.**

- **Stories:** 2.10, 5.2.
- **Evidence:**
  - EXP:501.
  - `epics.md:202` (the UX-DR14 retirement note cites Open item 18).
  - Only Add software is gated (`epics.md:960`).
- **Fix:** add a "set by UX before Build (Open item 18)" clause to 2.10 and 5.2.
- **Owner:** bmad-correct-course.

**13. CONCERN — Undrawn tabs and cells, and orphaned elements.**

- **Stories:** 2.10, 2.11, 5.2, 5.5, 6.3.
- **Evidence:**
  - 2.10 "How to fix and Details wait for UX (Open item 14)" (`epics.md:942`); no later story builds them.
  - 6.3 "Home's Exposure tab (a reduced summary …)" is undrawn and ungated (`epics.md:1810`).
  - 2.11 Data quality before a score exists (Open item 32, `:966`) is gated only at 8.1.
  - The Software "Audit report" button (UX-DR25) has no story.
- **Fix:** gate or minimally define each one; assign the orphans.
- **Owner:** bmad-ux + bmad-correct-course.

**14. CONCERN — No rule classifies packages as Direct or Indirect.**

- **Stories:** 2.11, 6.4, 6.6.
- **Evidence:**
  - UX-DR25 (`epics.md:216`), 2.11 (`:966`), 6.4 "direct · in 12".
  - `rg -i indirect architecture.md` finds nothing.
- **Fix:** record how it is derived from Syft relationships, with an "unknown" fallback.
- **Owner:** bmad-architecture / 2.11 planning.

**15. CONCERN — UI read-model and API contracts are unnamed.**

- **Stories:** 2.10, 2.11, 5.1–5.4, 6.5, 6.6.
- **Gaps:**
  - The issue (finding group) ID and URL.
  - Group detail.
  - The neighbours response shape.
  - A non-unique Software route.
- **Evidence:**
  - `architecture.md:257` defines a composite key but no group ID or path.
  - Story 5.1 explains order on "`GET /api/v1/findings/{id}`" (`epics.md:1519`), but order belongs to a group.
  - `GET /api/v1/graph/neighbours` has no shape (`:1911`; `architecture.md:267`).
  - UX-DR25 routes to `/software/<name>` (`epics.md:216`).
- **Fix:** define the issue ID and URL in 2.10 planning at the latest, since 5.x and 6.x share them.
- **Owner:** bmad-architecture.

### Concerns — Epic 5

**16. CONCERN — There is no API contract for Reports → Audit trail, and O16 gates only the broken-chain state.**

- **Stories:** 5.5, 9.6, 9.9.
- **Evidence:**
  - Story 5.5 "verified 4 min ago … broken-chain state … set by UX before Build (O16)".
  - Only `GET /api/v1/evidence/verification` exists (`epics.md:693`), and it recomputes on each call.
  - No ledger list endpoint, subject model or verification cadence exists.
  - DES:740 "[ASSUMPTION, EXPERIENCE Open item 36]"; EXP:522.
- **Fix:** add the list endpoint, subject model and cadence to the architecture, and widen the gate to Open item 36.
- **Owner:** bmad-architecture + bmad-ux.

**17. CONCERN — No rule covers two people reviewing the same issue at once (Open item 30).**

- **Stories:** 5.3, 5.4, 5.8.
- **Evidence:**
  - EXP:516.
  - Story 5.3 says "it supersedes the old one".
  - `architecture.md:334` lists a 409 code but no expected-version rule; `rg "Open item 30" epics.md` finds no match.
- **Fix:** record an expected-version / 409 rule with inline copy, or explicitly accept last-writer-wins and gate it in 5.3.
- **Owner:** bmad-architecture + bmad-ux.

**18. CONCERN — Forward dependencies.**

- **Stories:** 5.4, 5.6, 6.3, 6.4.
- **Evidence:**
  - 5.4 "Review buttons on Home, the Exposure inspector and Software" (`epics.md:1618`). The inspector arrives in 6.6.
  - 6.3 "When the user chooses Review in the inspector" (`:1825`). The inspector arrives in 6.6.
  - 6.4 "the same layout as a moved map (Story 6.6 …)" (`:1846`).
  - The Mixed branch of 5.6 cannot be tested before 5.8.
- **Fix:** write these as "when Story 6.x / 5.8 lands".
- **Owner:** bmad-correct-course.

### Concerns — Epic 6

**19. CONCERN — Change-record questions O2 and O20 are ungated; O14 and O19 have soft gates.**

- **Stories:** 6.3, 6.5, 4.9, 7.4.
- **Evidence:**
  - `architecture.md:556` "whether files are signed. _Open — Story 6.5 planning (O1, O2)_"; Story 6.5 carries only O1 (`rg "\bO2\b" epics.md` finds no match).
  - O20 / Open item 39 ("Audit report for this answer" label, EXP:525) has no gate.
  - O14 (`epics.md:1444`) and O19 (`:2058`) say "copy to confirm" with no "before Build".
- **Fix:** add O2 and O20 to the 6.5 planning AC, and O20 to 6.3.
- **Owner:** bmad-correct-course.

**20. CONCERN — Export placement on Issues and Software, and the CSV row unit, are undefined.**

- **Story:** 6.5.
- **Evidence:**
  - UX-DR21 places Export on "Exposure, Issues and Software", and Story 6.5 requires it from all three.
  - DES places it only in the Exposure header.
  - Whether a CSV row is an issue or a place is not stated. Stored-export detail is Open item 15 (EXP:498).
- **Fix:** add the placement to EXP and the row unit to ARCH39.
- **Owner:** bmad-ux / 6.5 planning.

**21. CONCERN — There is no grammar for Exposure queries or moved-map URLs.**

- **Stories:** 6.2, 6.3, 6.6.
- **Evidence:**
  - "a package with a version range (for example `log4j-core@2.x`)" (`epics.md:1762`).
  - "the URL (`&from=` the previous step) … restores that map".
  - No grammar exists for package, vulnerability, place or roll-up centres, nor header copy for a range (or a non-key alias — N4).
- **Fix:** add the query and URL grammar to the architecture and the header copy to EXP.
- **Owner:** bmad-architecture + bmad-ux.

**22. CONCERN — The moved-map Table sits outside the Story 6.6 UX gate.**

- **Story:** 6.6.
- **Evidence:** `epics.md:1934` "the Table of a moved map is not drawn (EXPERIENCE Open item 19)". The gate (`:1919-1921`) covers only other centres and long trails.
- **Fix:** include the Table in the gate.
- **Owner:** 6.6 planning.

### Concerns — later epics (carried; they block none of Epics 1, 2, 4–6)

**23. CONCERN — FR32/FR33 follow-through is incomplete.**

- **Stories:** 4.10, 10.2, 10.3.
- **Evidence:**
  - The 4.10 amendment AC covers trusted-root delivery for air-gapped installs only (`epics.md:1469`). It does not cover connected keyless verification from `tools`/`inventory` calling Rekor/TUF against ARCH19 ("called only by `feeds`, `enrichment` and `signing`", `epics.md:132`).
  - The 10.3 endpoint check (`epics.md:2540`) omits the end-of-life source.
- **Fix:** widen the 4.10 amendment, and add end-of-life data to 10.2 and 10.3.
- **Owner:** bmad-architecture / bmad-correct-course.

**24. CONCERN — Audit-report regeneration (Open item 22) is ungated.**

- **Story:** 9.5.
- **Evidence:** EXP:505.
- **Owner:** bmad-ux + bmad-architecture.

**25. CONCERN — Turning "triage licence warnings" off leaves warnings permanently Not reviewed yet, which inflates counts.**

- **Story:** 7.4.
- **Owner:** bmad-ux / 7.4 planning.

### Notes

**26. NOTE — FR15 and the Story 5.7 statement still read as if vendor claims change findings.**
- FR15: "applying their not-affected claims … to fleet findings" (`prd.md:96`).
- Story 5.7: "apply their not-affected claims, So that upstream knowledge reduces noise" (`epics.md:1679-1680`).
- Under A2 the claims are display-only. The ACs are unambiguous, so this is N8, wording only.
- Owner: bmad-prd.

**27. NOTE — The Story 4.5 scope manifest lists "CVE IDs and package coordinates only".**
- Source: `epics.md:1331`.
- Under A1, a GHSA-keyed finding has no CVE. Say "vulnerability IDs and aliases".
- Owner: 4.5 planning.

**28. NOTE — The O17 Help placeholder copy has no gate.**
- Source: `epics.md:538`.
- This is copy only.

**29. NOTE — Epic 1 builds stated [ASSUMPTION] defaults without a gate.**
- Defaults: Open items 3, 6 and 25.
- Evidence: `epics.md:186`, `:219`, `:522`.
- They are stated, not invented. Accept them, or have UX confirm.

**30. NOTE — Story 1.8 wording.**
- "every registered keyboard shortcut also has a palette entry" (`epics.md:612`) should list the exempt keys (J/K/Esc/⌘↵/Backspace).
- `epics.md:620` uses "`G`" where `:619` uses `g`.

**31. NOTE — The Story 1.9 lime list omits two DESIGN.md exceptions.**
- Missing: the "Selected on the map" marker (DES:570) and `sprout-ring` (DES:57, `:534`).
- IA/epic-1-context.md:119 also gates only the `g` letters, not the Keyboard shortcuts view layout (`epics.md:621`).

**32. NOTE — Epic 1 coverage and Epic List drift.**
- The Epic List says Epic 1's Home offers "the two setup actions" (`epics.md:290`).
- Story 1.6 says they "arrive with Stories 2.2 and 3.2" (`:542`), but the registry action is built in 2.9 (`:916`).

**33. NOTE — Three change records still mark "6.3 User approval: Pending" although their frontmatter says approved and applied.**
- Locations: ACR:698, RCR:845, `sprint-change-proposal-2026-11-07.md:2995`.
- The `implementation-readiness.md` frontmatter history does not yet list the aliases change record. This gate rerun updates it.

**34. NOTE — architecture.md drift.**
- `architecture.md:73` still says "Agent state-recovery model (open)", although ARCH9 decided it.
- `:282` requires "Grype pinned, ≥ v0.121.1" for `grype db diff`, but 0.120.1 already ships `db diff` (local `grype db --help`).
- Harmless, but the version floor should be confirmed when Story 2.4 or 4.2 pins Grype.

**35. NOTE — Auditor access to "Audit report for this answer" is not stated.**
- Story 6.5's auditor AC (`epics.md:1893`) covers only export.

**36. NOTE — Dev-cluster prerequisites are external but recorded.**
- Stories 1.1 and 1.2 need in-cluster BuildKit, the dev registry, ARC runners, the AGE Pod, and a CNI that enforces NetworkPolicy.
- These are Daniel's (OI-3, `docs/agent-readiness.md:379`; `PA/sprint-change-proposal-2026-11-06.md:67-71`).
- Confirm they are in place before 1.1 VAL-9/11/12 run.

## Regrading of the second rerun's findings

- **Closed by ACR:**
  - rerun-2 finding 1 (blocker 9)
  - finding 14 (Q-gates)
  - finding 18 (vendor VEX)
  - finding 20 (lookup method; its remainder is concern 3)
  - finding 29 (stale [ASSUMPTION])
  - rerun-1 concerns 1–5
- **Partly closed:** rerun-2 finding 2. The fast tier is now defined in `docs/agent-readiness.md`; the stale spec and the `ci` profile remain (concern 4).
- **Still concerns, unchanged:** rerun-2 findings 3–13, 15–17, 19, 21–26. They are concerns 5–25 here.
- **New in this pass:** concerns 1, 2 and 3 (from the alias change itself), and notes 26, 27 and 34.
- **No actionable blocker remains.** Every open item above can be settled by its story's Build planning or by a one-line gate.
