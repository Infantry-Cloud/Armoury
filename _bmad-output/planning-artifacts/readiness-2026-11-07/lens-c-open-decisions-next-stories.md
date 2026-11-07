# Readiness review — Lens C: open decisions and the next stories

Read-only review, 2026-11-07. Paths are relative to `_bmad-output/`: PA = `planning-artifacts/`, IA = `implementation-artifacts/`, CR = `PA/sprint-change-proposal-2026-11-07.md`, EXP/DES = `PA/ux-designs/ux-Armoury-2026-11-06/EXPERIENCE.md` and `DESIGN.md`.

## Verdict suggestion

**CONCERNS.** Story 1.1 is not blocked: its draft spec is stale, but the re-plan is recorded. Two narrow Epic 1 conflicts (the `?` shortcut map in 1.8 and the lime lint in 1.9) must be fixed before those stories start Build. Several open questions that the change record says are gated are not in fact gated by any story AC (O2, O17, O20, O14/O19 only weakly). Treat the verdict as FAIL if any blocker must be closed before the readiness rerun can pass.

Counts: **2 blockers, 18 concerns, 10 notes.**

## Findings

### Blockers

**1. Blocker — the `?` shortcut map has nowhere to open. The only modal allowed is ⌘K, and nothing records where the map goes.**
- Stories affected: 1.8 (also 1.9's modal test).
- Evidence:
  - PA/epics.md:618 (Story 1.8): "…export, open the shortcut map, or close the topmost layer"
  - PA/epics.md:190 (UX-DR7): "`?` shortcut map (also listed in Settings → Personal)"
  - PA/epics.md:231 (UX-DR36): "no modal deeper than one (the ⌘K dialog is the only modal; no drawers)"
  - PA/epics.md:633 (Story 1.9): "one shared overlay component allows one modal — the ⌘K dialog — … proven by a component test"
  - EXP:510 (Open item 24): "The `?` shortcut map may belong there" (Help, which is deferred)
  - Story 1.8's pre-Build gate (PA/epics.md:619) covers only the `g` letters and `t`/`e`.
- Impact: the developer must invent what `?` does: a second dialog (which breaks 1.9), a jump to Settings → Personal, or a filtered palette.
- Fix: add "what `?` opens" to the 1.8 pre-Build gate (EXPERIENCE Open item 13/24), or state in UX-DR7 that `?` opens Settings → Personal → Shortcuts.
- Owner: bmad-ux, then bmad-correct-course (a one-line epics edit).

**2. Blocker — the Story 1.9 lime lint conflicts with lime uses that DESIGN.md requires (focus ring, sidebar ring, centre of the moved map).**
- Stories affected: 1.9 (and 1.5, 1.7 and 6.6, which would trip the lint).
- Evidence:
  - PA/epics.md:641: "fails … on lime used outside its agreed jobs (active nav, the one primary action, selected map node, Issues badge, text selection)"
  - Conflicting DESIGN.md lines:
    - DES:594: "On ink (sidebar) and on forest (selection) the ring is always lime"
    - DES:113: `focus-dark: '#C8F169'  # lime ring in dark`
    - DES:616: `--sidebar-ring` = `{colors.lime}`
    - DES:466: centre-node "6px {colors.lime} inner dot"
    - DES:26-27 / 531-533: `lime-wash` disc and `lime-ring` halo (All clear)
  - DES:568 repeats the same short exception list, so the spine is inconsistent with itself.
- Impact: the gate, implemented as written, fails as soon as Story 1.7's focus ring (or 6.6's centre node) lands. Otherwise the developer has to quietly widen the AC.
- Fix: extend the exception list in DES:568, UX-DR1 (PA/epics.md:181) and Story 1.9 to cover the focus ring on ink, forest and dark, the moved-map centre dot, and the lime-wash/lime-ring tints.
- Owner: bmad-ux, then bmad-correct-course.

### Concerns: Epic 1 (the next stories)

**3. Concern — the Story 1.1 spec still describes the superseded kind/Podman loop and has stale sources and line references.**
- Story affected: 1.1.
- Evidence:
  - The spec uses kind/Podman throughout:
    - IA/spec-1-1…:25 "a Skaffold `kind` dev loop"
    - :42 "local Podman machine"
    - :70 AC-8 "`skaffold dev -p kind` … local kind cluster"
    - :72 AC-10 "runs `mise run check` and `mise run e2e` against a kind deployment" (no fork-PR fast tier and no ARC runners)
    - :74 AC-12 "keep `skaffold dev -p kind` running"
  - epics.md requires the dev-cluster loop instead:
    - PA/epics.md:366-368: `mise run dev` with "no image build, database or cluster runs on the workstation"
    - :376: fast tier on GitHub-hosted runners, full gate on ARC, "a fork pull request never reaches an ARC runner"
  - Stale references in the spec:
    - Code Map cites `epics.md:310-359` (Story 1.1 is now at PA/epics.md:335-384) and `architecture.md:379-456` (the tree is now at PA/architecture.md:394-475).
    - The Sources (:49-52) omit the 2026-11-06 and 2026-11-07 proposals.
    - The Spec Change Log (:174) has no 2026-11-07 entry.
  - IA/epic-1-context.md:30,41,43 already matches epics.md.
- Gated: yes. The spec is `draft` (:5, :140), and CR step 9 / the Contract Change Record require a re-plan at CHECKPOINT 1, so this is a concern, not a blocker.
- Fix: at the re-plan, rewrite AC-8/10/12, the VALs and the Code Map from epics.md and the context, and add 2026-11-07 change-log and Sources lines.
- Owner: Story 1.1 Build planning.

**4. Concern — the sign-in page is not designed anywhere.**
- Stories affected: 1.3, 1.4.
- Evidence:
  - PA/epics.md:442 "signs in with it on the sign-in page".
  - `rg -i "sign.?in"` finds no hit in EXP or DES (nor in the superseded spine's DESIGN.md).
  - Undrawn as a result: the layout, the bootstrap form vs "Sign in with SSO" when OIDC is set (Story 1.4), the "generic message", the denial copy for "claims map to no role" (1.4), and the theme before any preference exists.
- Fix: add a sign-in state to EXPERIENCE "States" (or state that a minimal page uses Light + catalogue strings), before 1.3 Build.
- Owner: bmad-ux.

**5. Concern — global states (session expired, control plane unreachable, a forbidden Settings link) are silently depended on.**
- Stories affected: 1.3, 1.4, 1.6 and every surface.
- Evidence:
  - EXP:517 (Open item 31): "session expired and re-authentication; control plane unreachable …; a direct link to a Settings panel or action the role cannot use".
  - Story 1.3 returns 401 on expiry (PA/epics.md:458-461) but no story says what the SPA shows.
  - Open item 31 is cited nowhere in epics.md or architecture.md (searched with `rg "Open item 31"`).
- Fix: either gate 1.6 on Open item 31 ("set by UX before Build") or record an interim rule (for example, a 401 goes to sign-in with a return URL).
- Owner: bmad-ux / 1.6 Build planning.

**6. Concern — the "users/roles view" in Settings → Access has no data source or API.**
- Story affected: 1.6.
- Evidence:
  - PA/epics.md:545 "Settings → Access (the read-only resolved auth configuration and the users/roles view)".
  - EXP:123 "Access (users and roles, …)".
  - Architecture defines only `sessions`, `user_preferences` and `GET /api/v1/auth/config` (PA/epics.md:124 ARCH16, :497 Story 1.4). No users table or `/users` endpoint exists (`rg "/api/v1/users|users table"` finds nothing).
  - With declarative OIDC there is no user directory.
- Impact: the developer must decide whether "users" means the role-mapping config, the users seen so far, or the active sessions.
- Fix: define it, or reduce it to the role mapping shown in auth/config.
- Owner: bmad-architecture + bmad-ux, before 1.6 Build.

**7. Concern — O17 (Help placeholder copy) is cited but not gated.**
- Story affected: 1.6.
- Evidence:
  - CR:2960: "O17 … UX | Story 1.6 Build".
  - PA/epics.md:536: "Help opens a placeholder until its screen is designed (EXPERIENCE Open item 24, O17)". There is no "before Build" clause.
  - UX-DR44 (PA/epics.md:239): "copy to confirm with UX — O17".
- Fix: add "placeholder copy set by UX before Build (O17)" to Story 1.6.
- Owner: bmad-correct-course / bmad-ux.

**8. Concern — the icon-rail width (and other dimensions) are not tokenised, but Story 1.7 builds the rail and tests it at 320 CSS px.**
- Story affected: 1.7 (and 1.5's "layout tokens match DESIGN.md").
- Evidence:
  - EXP:519 (Open item 33): "some dimensions are untokenised (… 660px palette, the icon-rail width, …)".
  - DES:682 describes the rail but gives no width.
  - PA/epics.md:592 tests "1440, 1100 and 900 px wide, at 320 CSS px".
  - The `spacing` block (DES:241-262) has no rail token.
- Fix: add a `rail-width` token (and the other dimensions Open item 33 lists) to DES before 1.7 Build, or gate 1.7 on it.
- Owner: bmad-ux.

### Concerns: FR32/FR33 (Stories 4.9, 4.10) and open questions

**9. Concern — the Story 4.10 amendment does not cover connected-mode trusted-root refresh or Rekor/TUF calls, which collide with the outbound-boundary rule.**
- Story affected: 4.10.
- Evidence:
  - The amendment AC (PA/epics.md:1453) covers only "how the Sigstore trusted root reaches **air-gapped** instances". O8 (CR:2951) also asks "whether connected instances may refresh it online (a new built-in public endpoint)".
  - PA/architecture.md:205 lists it as open: "how the trusted root is delivered and refreshed (… an online refresh in connected mode as a built-in public endpoint owned by `signing`)".
  - The same architecture line says `inventory` runs `cosign verify`.
  - ARCH19 (PA/epics.md:130; PA/architecture.md:385, 486): built-in public endpoints are "called only by `feeds`, `enrichment` and `signing`".
  - By default, keyless `cosign verify` in connected mode reaches the Sigstore TUF CDN and Rekor, so `inventory` would break ARCH19 unless the amendment decides this.
- Fix: widen the AC at :1453 to cover the trusted-root source and refresh in both modes, which module makes any public call, and whether tlog lookups are online or offline.
- Owner: bmad-architecture (Story 4.10 amendment) / bmad-correct-course.

**10. Concern — O2 (are stored export files cosign-signed?) is not gated by any story.**
- Story affected: 6.5.
- Evidence:
  - CR:2945: "O2 … Architect + Daniel | Story 6.5 planning".
  - PA/architecture.md:204: "Not decided: whether stored export files are also cosign-signed (O2)".
  - Story 6.5 (PA/epics.md:1825-1863) settles only O1 (":1841 the owning module is settled when the story is planned (O1)").
  - `rg "O2\b"` finds nothing in epics.md.
- Fix: add O2 to the 6.5 planning AC.
- Owner: bmad-correct-course.

**11. Concern — O20 (the label "Audit report for this answer") is not gated, and three stories ship the label.**
- Stories affected: 6.3, 6.5, 6.6, 9.5.
- Evidence:
  - CR:2963: "O20 … UX + Daniel | Story 6.5 Build; EXPERIENCE Open item 39".
  - The label is used at PA/epics.md:1777, 1844, 1880 and 2312.
  - `rg "O20|Open item 39"` finds nothing in epics.md.
- Fix: add "label confirmed by UX + Daniel before Build (O20)" to 6.3/6.5.
- Owner: bmad-correct-course.

**12. Concern — O14 and O19 are only softly gated ("copy to confirm", "styling per U19"), not "before Build" as CR claims.**
- Stories affected: 4.9, 7.4.
- Evidence:
  - CR:2957 gates O14 at "Story 4.9 Build", but PA/epics.md:1428 says only "in plain words — copy to confirm with UX, O14".
  - CR:2962 gates O19 at "Story 7.4 Build", but PA/epics.md:2026 says "(D8; styling per U19, O19)". U19 is a proposal (EXP:523, Open item 37: "proposed: line 2 in text-2").
- Fix: reword both as "set by UX before Build".
- Owner: bmad-correct-course.

**13. Concern — O16 / Open item 36 (the Reports → Audit trail design) is only partly gated.**
- Stories affected: 5.5, 9.6, 9.9.
- Evidence:
  - CR:2959 scopes O16 as "list rows, filters, verification, checkpoint and anchoring cells, and the broken-chain state".
  - Story 5.5 gates only "the layout and wording of the broken-chain state are set by UX before Build (O16)" (PA/epics.md:1620).
  - Story 9.6 (PA/epics.md:2339) and Story 9.9 (anchoring status, ~PA/epics.md:2424) add cells with no gate.
  - EXP:522 (Open item 36): "Reports → Audit trail (D9) is not drawn".
- Fix: gate all of Open item 36 in 5.5, and the checkpoint and anchoring cells in 9.6/9.9.
- Owner: bmad-correct-course / bmad-ux.

### Concerns: later stories that depend on undecided EXPERIENCE items without a gate

**14. Concern — Story 2.10 depends on Open items 21 (order within Needs attention) and 18 (what a click on an Open-issues row does), with no gate.**
- Story affected: 2.10.
- Evidence:
  - UX-DR22 (PA/epics.md:211): "The order within Needs attention is not decided (Open item 21)".
  - UX-DR14 (PA/epics.md:200): "What a click on those rows does is not drawn (EXPERIENCE Open item 18)".
  - Story 2.10 (PA/epics.md:915-937) builds both lists and cites neither item.
- Fix: add "set by UX before Build (Open items 18, 21)" to 2.10.
- Owner: bmad-correct-course.

**15. Concern — Story 2.11 renders a Data quality row six epics before the "before a score exists" rule is decided.**
- Story affected: 2.11.
- Evidence:
  - PA/epics.md:955: "Data quality (filled by Story 8.2; what it shows before a score exists is EXPERIENCE Open item 32)".
  - The only gate is in Story 8.1 (PA/epics.md:2051).
  - In contrast, "Signed" gets an interim rule in the same AC ("until then it says the signature is not checked yet").
- Fix: add an interim rule (for example, "not scored yet") or a UX gate to 2.11.
- Owner: bmad-ux / 2.11 Build planning.

**16. Concern — the "Connect a registry" setup action needs a copy-paste one-liner, but no such command exists.**
- Stories affected: 2.9 (and 1.6's cross-reference).
- Evidence:
  - PA/epics.md:913: "the setup action 'Connect a registry' with its copy-paste one-liner in a code block".
  - UX-DR29 (PA/epics.md:221) and EXP:251 ask for "copy-paste one-liners".
  - A registry is connected through the Story 2.2 form or API (PA/epics.md:712-716).
  - No CLI or Helm one-liner for registries is defined: `rg "one-liner"` finds only the helm installs and the agent install.
- Fix: decide the command (for example `helm upgrade --set connections…` or a `curl` to the API), or change the action to a link to Settings → Connections.
- Owner: bmad-ux + bmad-architecture.

**17. Concern — Story 9.5 depends on Open item 22 (adjusting window, scope and framework after the click; regeneration semantics; the in-progress row), with no gate.**
- Story affected: 9.5.
- Evidence:
  - PA/epics.md:2278: "the user can change the window, scope and framework after the click, which regenerates the pack".
  - UX-DR20 (PA/epics.md:206): "how is not drawn — EXPERIENCE Open item 22".
  - EXP:505 (Open item 22).
- Fix: gate 9.5 on Open item 22.
- Owner: bmad-correct-course.

**18. Concern — the detail of a stored export is not drawn (Open item 15), and Story 6.5 is silent about it.**
- Story affected: 6.5.
- Evidence:
  - UX-DR27 (PA/epics.md:216): "the detail of a selected export is not drawn (EXPERIENCE Open item 15)".
  - EXP:498 (Open item 15): "detail of a stored export (… file, who, when, from which query, its audit-trail entry)".
  - Story 6.5 (PA/epics.md:1825-1863) lists exports but never says what selecting one shows. Every Reports group is master-detail (UX-DR37).
- Fix: add a UX gate, or an interim detail that reuses the record fields, to 6.5.
- Owner: bmad-correct-course.

**19. Concern — there is no rule for concurrent review decisions (Open item 30), and no story mentions it.**
- Stories affected: 5.3, 5.4, 5.8.
- Evidence:
  - EXP:516: "Conflicting decisions: two people reviewing the same issue at once (for example 'Changed by Marta at 14:05. Review again.') has no rule".
  - `rg "Open item 30|concurren|Review again"` finds only the ledger advisory lock (PA/epics.md:662).
  - Story 5.3 says only "it supersedes the old one" (PA/epics.md:1554-1556).
  - Impact: last-writer-wins with no warning conflicts with the "decide → Save and next" flow and with Mixed counts.
- Fix: gate 5.4 on Open item 30, or record last-writer-wins as an [ASSUMPTION].
- Owner: bmad-ux / bmad-correct-course.

**20. Concern — CR success criterion 9 is reported as met, but it is not.**
- Stories affected: those in findings 7 and 10-12.
- Evidence:
  - CR:2880: "Every open question in section 6 has an owner and is either answered or carried by an 'approved before implementation' AC."
  - CR:2865 marks steps 1–6 "Applied".
  - O2, O17, O20 have no AC, and O14, O19 have only soft ones (findings 7, 10-12).
- Fix: close findings 7 and 10-12 before rerunning readiness.
- Owner: bmad-correct-course.

### Notes

**21. Note — Story 4.10 does not restate the O13 answer (shown only; creates no issues; no effect on counts, CI policy or packs), although Story 4.9 does.**
- Evidence:
  - PA/epics.md:1429 (4.9): "creates no issue and does not count toward Needs attention (O13)".
  - Story 4.10 (PA/epics.md:1468-1471) says only "never shown in a severity colour".
  - CR:2935 and PA/prds/…/addendum.md:38 record the answer.
- Fix: add one AND line to 4.10.

**22. Note — Epic 1 stories build [ASSUMPTION] defaults without a gate, though each default is explicit, so nothing has to be invented.**
- Open item 3 (no OS-preference detection, Light default): Story 1.5 (PA/epics.md:520), with UX-DR4 (:184) "do not detect OS preference until it is".
- Open item 6 (Settings panel list in the list column): Story 1.6 (:543-545).
- Open item 25 (AA only, no high-contrast theme): UX-DR1 (:181) "confirm".
- Open item 2 ("Vulnerability" replaces "Weakness"): the retired-label lint in Story 1.7 bans "Weakness" (:242, :587).
- Ask UX to confirm these, or accept them, at the readiness rerun.

**23. Note — later stories also build [ASSUMPTION]s without a gate, in the same explicit style.**
- Open item 4: Review opens Issues (5.4, PA/epics.md:1595).
- Open item 9: Mixed status filter and "keep their own status" (5.2 :1529, 5.8 :1695).
- Open item 5: print face is Plex (6.5 :1857, 9.3 :2216).
- Open item 12: focus after moving the map (6.6 :1885).
- These are acceptable as stated defaults. Flag them if the strict "must gate" rule applies.

**24. Note — the PRD already partly decides O4 and O10.**
- O4: PRD FR18 (PA/prds/…/prd.md:102) says "An analyst can ask for the artifact to be checked again", so a minimum role of admin (O4, CR:2947) would contradict the PRD.
- O10: PRD FR32 (prd.md:78) limits scope to "each container image and other OCI artifact in a connected registry". Bringing feed packages or uploads into scope (O10, CR:2953) would need a PRD change.
- Note both limits in the 2.11 and 4.10 planning.

**25. Note — ARCH25 in epics.md lists `exports` without the O1 qualifier that architecture.md keeps.**
- PA/epics.md:142 lists `exports` with no qualifier. PA/architecture.md:435 says "(recommended, O1)", and PA/architecture.md:204 says "Owner: … (recommended — O1)".
- Story 1.1 writes the module layout into AGENTS.md (PA/epics.md:384), so O1 leaks into Story 1.1 even though it is gated only at 6.5.
- Fix: align the qualifier, or decide O1 now.

**26. Note — coverage and cross-references are inconsistent about who builds the setup actions and the code block.**
- Story 1.6 (PA/epics.md:540) and IA/epic-1-context.md:148 say "setup actions arrive with Stories 2.2 and 3.2", but the registry action is built in Story 2.9 (PA/epics.md:913), not 2.2.
- The Epic 1 coverage list (PA/epics.md:289) claims UX-DR42 (code block), but no Epic 1 story builds it: the first users are 2.9, 3.2 and 8.4.
- The same list claims UX-DR41 (inline error), which Epic 1 never builds even though the Settings → Personal theme save can fail (UX-DR28: "a save failure shows the inline error").

**27. Note — a stale "(open)" remains in architecture.md.**
- PA/architecture.md:73: "Agent state-recovery model (open)". ARCH9 (PA/epics.md:114) has since decided stateless re-derive.

**28. Note — two small Story 1.8 wording issues.**
- PA/epics.md:610: "a test asserts every registered keyboard shortcut also has a palette entry". Taken literally this needs palette entries for J/K/Esc/⌘↵/Backspace, so state which shortcuts are exempt.
- PA/epics.md:618: "after `G`" should be `g` (UX-DR7, :190).

**29. Note — IA/epic-1-context.md otherwise matches epics.md and architecture.md after the hand patch (C1–C17), with one small drift.**
- IA/epic-1-context.md:102 "uppercase only on button labels" omits the Graph/Table switch and zoom labels that UX-DR2 (PA/epics.md:182) allows.

**30. Note — the CR checklist still records approval as pending.**
- CR:2995 "6.3 User approval | [!] | Pending: Daniel approves…" and CR:2997 "answer O3 and O5 before the epics edit" contradict the frontmatter `status: approved` (CR:2-3) and the section 6 answers (CR:2931-2935).

## Verified as correctly gated (no finding)

- **O1:** 6.5 (PA/epics.md:1841, at planning).
- **O4:** 2.11 (:969, "chosen when the story is planned").
- **O6–O10:** 4.10 amendment, "approved by the user before implementation" (:1453). O8 is only partly covered; see finding 9.
- **O11, O12 and the O15 threshold:** 4.9 amendment (:1410).
- **O15 Home-strip placement:** "set by UX before Build" (:1437).
- **O18:** 2.9 (:909).
- **O3, O5, O13:** answered (CR:2931-2935), and reflected in 9.5 (:2313), Epic 4 and 4.9 (:1429).
- **Open items with a gate:**
  - 1: 5.1 amendment (:1495)
  - 11: 8.1 amendment (:2051)
  - 13: 1.8 (:619)
  - 16: 7.4 (:2030)
  - 17: 5.7 (:1674)
  - 18, Add software: 2.11 (:949)
  - 19 and 12, layouts: 6.6 (:1889)
  - 28: 11.2 (:2594), 11.4 (:2647)
  - 29: 6.3 (:1790)
- **Other gates:** ARCH10 (3.1, :1032), the bundle format (4.5, :1306) and VEX mapping (5.6, :1640) are all amendment-gated.
- **Stories 4.9/4.10 overall:** both put their open questions in a "recorded as an amendment to `architecture.md` and approved by the user before implementation" AC as their first criterion. The gaps are only those in findings 9, 12 (O14) and 21.
