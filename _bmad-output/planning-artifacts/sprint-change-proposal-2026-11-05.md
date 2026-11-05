---
status: approved
approved: 2026-11-05 — Daniel approved the whole proposal ("approve")
scope: moderate — PRD and architecture amendments, 4 new stories (1.9, 5.8, 9.8) and new Epic 11 (Stories 11.1–11.5); no approved story contract exists, so no contract revision is needed
date: 2026-11-05
applied: 2026-11-05 — all sections marked "agreed" are written into prd.md, architecture.md, EXPERIENCE.md and epics.md (Daniel: "lock it all in now")
workflow: bmad-correct-course (incremental)
trigger: _bmad-output/planning-artifacts/implementation-readiness.md (gate CONCERNS, "fix first, then rerun")
---

# Sprint Change Proposal — readiness fixes

Each gap was agreed one at a time with Daniel on 2026-11-05. Every section is now
"agreed" and applied to the planning artifacts. Linear is reconciled once, after the
final approval of this proposal.

Applied to: `prds/prd-Armoury-2026-06-11/prd.md` (FR31, NFR12, NFR6, FR10, NFR7, glossary,
roadmap) and its `.decision-log.md`; `architecture.md` (all agreed decisions);
`ux-designs/ux-Armoury-2026-06-12/DESIGN.md` (muted tokens, page header, printed report,
shadcn-svelte wording), `EXPERIENCE.md` and its `.decision-log.md`; `epics.md`
(ARCH31–ARCH36, PROC3, FR31, NFR12, story edits, new Stories 1.9, 5.8, 9.8 and new Epic 11
with Stories 11.1–11.5).

Deviations made while applying (flag for review):
- Topic 6 item 4: the `triage_status` metric label arrives in Story 8.3, after Story 5.3.
  To avoid a forward link, Story 5.3 checks the findings API and Story 8.3 checks the
  metric label.
- Topic 4 part A item 1: the muted token values were computed on 2026-11-05 to hold
  4.5:1 (text) and 3:1 (border) on `surface` and `background`: `data-quality-muted`
  Forge `#718887`, High Signal `#8A7AA6`, Gunmetal `#897BA8`; `node-inactive-border`
  Forge `#6E6660`, High Signal `#61666C`, Gunmetal `#616770`. Inactive node text uses the
  existing `text-muted` (5.4–8.1:1). Story 1.5 re-measures them.
- Topic 4 part B item 2: the print palette values (#1A1A1A body, #555555 secondary,
  #D0D0D0 rules, 9.5 pt body, 8.5 pt tables) were chosen while writing DESIGN.md.
- Independent review (2026-11-05, two read-only reviewers) found leftover text against
  agreed decisions. Fixed without a new decision: "Sigstore-signed" wording (PRD UJ-3,
  EXPERIENCE pack generator and air-gapped rows, UX-DR30); "stream progressively"
  (EXPERIENCE long-running query row → polling, 2 s); "air-gap axis/funnel" wording →
  two-class outbound boundary; FR31 → `ciscan` in the requirements table; long-operation
  pointer in Format Patterns; "no custom key bindings" in UX-DR7 and Story 1.8; Story 1.1
  dev-loop cache line and `ponytail:` note; KEV tag 0.85 is background alpha, not element
  opacity; history coverage test covers every application schema, and Story 2.1 marks
  `sessions` and `user_preferences` "not evidence" (removes a forward reference from
  Story 1.3); Story 3.1 serves enrollment, renewal and revocation on the agent port
  (Story 1.2 now says the listener arrives in 3.1); Story 5.8 states that the findings API
  and VEX export use the fleet-wide-aware status; Story 5.7 cites the architecture.
- Correction: Epic 11 does not depend only on Epic 2. Its verdict uses KEV (Epic 4),
  triage decisions (Epic 5) and license results (Epic 7). Epic 11 text and the
  architecture sequence now say "builds on Epics 2, 4, 5 and 7".

Decisions added while writing Epic 11 (flag for review): Story 11.4 lets current
`not_affected` and `mitigated` triage decisions exempt a finding from the CI verdict;
upload size limit default 2 GiB; CLI timeout default 10 minutes; Story 9.5 owns the
auditor pack-route RBAC test (Story 1.4 has no pack route yet); Story 4.5 bundles are
signed with the operator key only (Story 4.6 verifies against trusted public keys).

## Governing principle — all scanning on the server

Status: agreed (Daniel, 2026-11-05). This principle overrides any item below that
conflicts with it.

Syft, Grype, Grant, licence policy and every other check run only on the Armoury server,
with the single fleet tool versions and configuration. A CI runner, a cluster agent or
any other client only identifies an artifact or supplies its bytes. The server never
uses an SBOM, a finding, a licence result or a verdict that a client computes.

Reasons: one toolchain gives consistent results (FR2, FR6), and a changed runner cannot
remove packages or findings to get a clean result.

Where it applies: central registry and feed scanning (Epic 2), CI scanning (Epic 11),
licence evaluation (Epic 7), and the agent, which reports running digests only (Epic 3).

## Gap 1 — Container images, chart build and the dev loop

Status: agreed (Daniel, 2026-11-05)

Problem: no story builds a container image before Story 10.1, but Story 1.2 needs one
for `helm install` (`epics.md:296-345, 1994`; `architecture.md:340`).

Decision (Daniel):
- A GitHub pipeline builds the official images and the Helm chart from Story 1.1 on.
- Skaffold is the development loop. It runs and deploys continuously while code is written.
- Customers still install with one `helm install` of the published chart (NFR1).

Proposed edits:

1. Story 1.1 (scaffold)
   - Add multi-stage Dockerfiles for `control-plane` (`armoury` binary + SPA build) and
     `agent` (`armoury-agent` only), base images pinned by digest.
   - Add `.github/workflows/build.yml`: on each push, build both images and package the
     chart; on `main`, push them to GHCR (`ghcr.io`) by digest.
   - Add `skaffold.yaml` (pinned Skaffold version) with the same Dockerfiles, the Helm
     deployer (`setValueTemplates` with `repo:tag@digest`) and a `kind` profile that loads
     images into a local kind cluster, with `portForward` for UI and API.
   - New AC: `skaffold dev -p kind` builds both images, deploys the chart to kind and
     redeploys after a code change.
   - `AGENTS.md` states PROC3.
   - `ponytail:` note: Rust rebuilds are slow; use a debug profile for dev and a
     cached dependency layer (for example `cargo-chef`). Upgrade path: a remote build cache.
2. New process rule PROC3 in `epics.md`: every development step starts with
   `skaffold dev -p kind` running and deploying continuously; changes are checked against
   that live deployment as well as by `mise run check`; an unhealthy loop is fixed before code
   is written. Applies to every story after 1.1.
3. Story 1.2 (install): install and durability checks run against the Skaffold-deployed
   kind cluster; the customer `helm install` AC stays.
4. Story 2.12 (minute 29): deploy with the Skaffold `kind` profile, then time the customer
   steps (sign in, connect registry, Posture).
5. Story 10.1 and ARCH23: `release.yml` reuses the build pipeline and adds release tags,
   cosign signing, SLSA provenance and SBOM attestations for the built digests. The agent
   image carries no scanner tools.
6. `architecture.md`: ARCH1/scaffold section, Testing/Dev (replace the Vite-proxy hot
   reload with the Skaffold loop), directory tree (`skaffold.yaml`, `build.yml`,
   `agent/Dockerfile`).
7. Agent Readiness (INF-12): record the Skaffold loop as a proven correction loop.

Confirmed by Daniel:
- Registry: GHCR.
- Scanner tools enter the control-plane image in the story that first uses them:
  Syft 2.3, Grype 2.4, cosign 4.5, Grant 7.1 (each pinned and checksum-verified).
- PROC3 is one shared rule, not a preface copied into each story.

## Gap 2 — Evidence history that can rebuild the past

Status: agreed (Daniel, 2026-11-05)

Problem: ledger entries store only a payload digest (`epics.md:540`). Operational tables
are overwritten, so Story 9.1 cannot rebuild the state at a past time (FR23), and the
history written in Epics 2–8 is lost before Epic 9 exists (`epics.md:1803`).

Decision (Daniel): versioned history tables ("way 2"), not event replay from the ledger.
Reasons: a past-time question is one indexed query, not a replay that grows with history;
history tables follow normal migrations, so no old event formats must stay readable;
state logic exists once.

Proposed edits:

1. Story 2.1 and `architecture.md` (Data Architecture, ARCH2, ARCH5):
   - Each evidence-bearing table has a current table (live rows only) and a history table
     (every closed version, with `valid_from` and `valid_to`).
   - A database trigger copies the old version to the history table on each update or
     delete, so application code cannot skip it.
   - History tables are insert-only: the application role has no UPDATE or DELETE grant.
   - History tables are partitioned by month, so ARCH30 archiving applies to them.
   - Each change appends a ledger entry with the digest of the new version. Events that
     are themselves the fact (for example a triage decision) keep their full content in
     the ledger entry. Large content (SBOMs, scan output) stays in the object store,
     content-addressed and never overwritten inside retention.
   - Record PostgreSQL 18 as the database version (`WITHOUT OVERLAPS` temporal
     constraints; Apache AGE has PG18 builds, `PG18/v1.8.0-rc0`, 2026-07-09).
   - Rule: ledger entries and history rows never contain credentials or secrets; a test
     checks this for every connection type.
2. Rule 1 — version only on content change. A row that is checked but not changed writes
   no history version. A re-evaluation records one run entry ("fleet evaluated against
   Grype DB vX") instead. Story 4.2 changes: unaffected findings get no new version; their
   provenance reads the run entry.
3. Rule 2 — history coverage test (Story 2.1). A test lists every table in the inventory,
   findings and triage schemas. Each table must have a history table or an explicit
   "not evidence" marker, so a new table cannot silently lose its history.
4. Story 2.1: replace the "reserved quota/tablespace" AC (not buildable in Postgres) with
   health-endpoint reporting of ledger and history size and database volume headroom,
   with a warning threshold (default 80 % used).
5. Story 2.1: new AC — a reconstruction test changes current rows after recorded events,
   then rebuilds an earlier state from the history tables and checks it.
6. Story 9.1: answer past-time questions from the history tables (and from verified
   archive segments for archived windows).
7. ARCH30: archive history-table partitions with the ledger partitions.
8. Out of scope: the AGE graph shows current state only; a time-travel graph stays on
   the roadmap.

## Gap 3 — Feed-delta computation

Status: agreed (Daniel, 2026-11-05)

Problem: Story 4.2 needs the delta between two Grype DB versions, but nothing records how
to compute it (`epics.md:1032`; `architecture.md:61, 427`). The Grype DB is a SQLite file
with a Grype-owned internal schema.

Decision (Daniel): way A, `grype db diff`, with a full re-check as a measured fallback.
Do not read the Grype SQLite schema directly (way B).

Proposed edits:

1. `architecture.md` (Substrate Integration, ARCH6, ARCH7): `reeval` computes the delta
   with `grype db diff -o json <previous-db> <current-db>` through `tools` (Grype pinned,
   ≥ v0.121.1; checked 2026-11-05). The changed packages select the stored SBOMs that
   contain them, through the package index; `scan` re-matches that subset. Armoury never
   reads the Grype SQLite schema. `feeds` keeps each activated DB in its own directory
   (`<feeds-dir>/grype/<db-version>/`), at least the current and the previous version.
2. Story 4.2, AC 1: compute the delta with `grype db diff -o json` through `tools`
   (packages with changed matches; added, changed and withdrawn vulnerability records).
   The existing equivalence test (delta result = full re-check result) stays.
3. Story 4.1: replace "validates its checksum/signature and schema" with "validates its
   checksum from the Grype DB listing and its schema version" (Anchore publishes
   checksums, not signatures).
4. Story 4.8: measure both the diff path and a full re-check of every stored SBOM at the
   scale anchor; record both in the performance record. If the diff misses NFR5, or the
   full re-check meets it with margin, choose by the measurement (fallback recorded in
   the architecture).
5. Story 4.8: new AC — an enrichment-only update (KEV, EPSS, OSV or CNA re-join) also
   completes within one hour.

## Gap 4 — Runtime signing of packs and checkpoints

Status: agreed (Daniel, 2026-11-05)

Problem: packs (Story 9.4) and ledger checkpoints (Story 9.6, ARCH30) are "keyless when
connected", but public Fulcio trusts Kubernetes service-account tokens only from EKS, GKE
and AKS issuers (Fulcio `config/identity/config.yaml`, checked 2026-11-05). Self-managed
clusters have no accepted identity. Also, keyless signing writes the signer identity
(cluster issuer URL, which can name the project, region or cluster) to the public Rekor
log; daily checkpoints would publish this for every customer by default.

Decision (Daniel): way 2 — operator key by default at runtime; keyless is opt-in.
FR25 needs no change ("Connected deployments may use Sigstore keyless signing").

Proposed edits:

1. `architecture.md` (Signing bullet, Substrate Integration cosign line, Data Flow
   "Signing — two distinct roles") and ARCH18:
   - Runtime signing setting `signing.mode`: `key` (default) or `keyless` (PROC2).
   - `key`: cosign signs with the operator key. If the operator supplies no key, the
     control plane generates one on first start and stores it in a named Secret in its
     own namespace; its RBAC covers only that Secret. Settings shows the public key.
   - Each public key in use is appended to the ledger, so old packs and checkpoints stay
     verifiable after a key rotation.
   - `keyless`: projected service-account token (audience `sigstore`) to public Fulcio
     (EKS, GKE or AKS issuers only) or a configured private Fulcio, with Rekor. If the
     issuer is not accepted, startup fails with a clear message, not pack generation.
   - Air-gapped mode always uses `key`.
   - The mode and signer identity are recorded on each signature.
   - Build-time keyless signing of Armoury's own releases in CI (NFR7) is unchanged.
   - `ponytail:` a key in a Kubernetes Secret is only as safe as the cluster; a cluster
     admin can read it. Upgrade path: a cosign KMS key reference (cloud KMS or Vault)
     in place of the Secret.
2. Story 9.4: AC 1 becomes "signs the pack manifest in the configured signing mode (`key`
   by default)"; keyless is an admin opt-in with the startup check above. The air-gapped,
   fail-closed, tamper and offline-verification ACs stay.
3. Story 9.6 and ARCH30: checkpoints are signed "in the configured signing mode
   (Story 9.4)", replacing "keyless + Rekor when connected, operator key when air-gapped".
4. Story 9.5, UX-DR19, `EXPERIENCE.md` (Evidence pack card row, Flow 3 step 4): the
   verification command is the operator-key command by default, or the keyless command
   when keyless is enabled; "Sigstore-signed" becomes "signed with cosign".

## Gap 5 — Live updates and partial results in the browser

Status: agreed (Daniel, 2026-11-05)

Problem: Story 2.9 (populating banner "updating live"), Story 6.3 (partial blast-radius
results "stream in" with a scope line) and Story 9.5 (per-section pack progress) need
changing results in the browser. The architecture has only single request/response REST,
and Story 6.2 defines blast radius as one `GET` (`epics.md:739, 1427, 1474`;
`architecture.md:175, 301`).

Decision (Daniel): way A, polling. No Server-Sent Events in v1.

Proposed edits:

1. `architecture.md` (API & Communication Patterns, Format Patterns) and ARCH13: new
   "long operation" pattern.
   - `POST /api/v1/<operations>` creates the operation and returns it at once with `id`,
     `status` (`running` / `completed` / `failed`), `progress` (done and total counts),
     partial results so far, `provenance`, and a cursor for result pages.
   - `GET /api/v1/<operations>/{id}` returns the same shape. If the first response is
     already `completed`, the client sends no second request.
   - The SPA polls with svelte-query `refetchInterval`: about 1 s for long operations,
     about 10 s for the Posture summary, and only while work is queued or running.
   - `ponytail:` partial blast-radius results are held in control-plane memory for about
     10 minutes (single instance, NFR10); a restart loses them and the user runs the query
     again. Upgrade path: store them in PostgreSQL if Armoury runs more than one control
     plane. SSE stays a later option if polling delay is measured as too slow.
2. Story 6.2: `GET /api/v1/blast-radius` becomes `POST /api/v1/blast-radius-queries` and
   `GET /api/v1/blast-radius-queries/{id}` with the pattern above. All other ACs (provenance,
   coverage-scoped zero, digest query, 422 cases, no-match CVE metadata) stay.
3. Story 6.3: partial results and the scope line come from `progress` and partial results
   on each poll; "a few seconds" becomes a number (operation still `running` after 2 s
   shows the scope line).
4. Story 2.9: the populating banner refreshes by polling the Posture summary while backlog
   exists.
5. Story 9.5: pack generation uses the long-operation pattern; per-section progress comes
   from `progress`.

## Gap 6 — Auditor and pack generation

Status: agreed (Daniel, 2026-11-05)

Problem: PRD NFR6 makes the auditor read-only and gives pack generation to the analyst
(`prd.md:48, 113`). `EXPERIENCE.md` (`:142`, Flow 3 `:221-224`) and Story 9.5
(`epics.md:1917`) let the auditor generate packs by default. Pack generation writes a
ledger entry and uses the signing key, so it is not a pure read.

Decision (Daniel): follow the PRD. By default, only admins and analysts generate packs.
A setting lets auditors generate packs too. The PRD stays unchanged.

Proposed edits:

1. Story 9.5: replace the auditor AC. By default, an auditor can view, download and
   verify packs, and the generate controls are absent (UX-DR31). When the setting
   `rbac.auditorCanGeneratePacks` is `true` (default `false`, PROC2), an auditor can also
   generate packs. Auditors can never change triage, policy or Settings.
2. The setting is a Helm value, like the rest of the role configuration (NFR6: declarative,
   no UI wizard). Settings shows its value read-only in the resolved auth configuration.
3. Story 1.4: the RBAC route test covers the pack-generation route for the auditor in
   both setting values (403 when `false`, allowed when `true`).
4. `EXPERIENCE.md`: the Read-only auditor row (`:142`) says pack viewing, download and
   verification are available, and generation only when an admin enables it. Flow 3
   step 2: Priya (analyst) generates the pack for the audit window; Marta (auditor) opens
   it, verifies it and hands it over. A note says an admin can let auditors generate packs.
5. UX-DR31 in `epics.md`: same wording as the `EXPERIENCE.md` auditor row.

## Gap 7 — Decisions recorded only in `epics.md`

Status: agreed (Daniel, 2026-11-05)

Problem: `architecture.md` claims to be the single reference (`:486`), but still lists VEX
formats and retention as open (`:462-463`), omits the ARCH30 maintenance role from its
data boundary (`:399`), and does not mention PROC2. Story 5.6 cites a VEX status-mapping
amendment that does not exist (`epics.md:1368`).

Decision (Daniel): recommendation items 1 and 2.

Proposed edits:

1. `architecture.md` becomes complete again:
   - Add ARCH29 (VEX formats: OpenVEX and CycloneDX VEX; CSAF deferred) and ARCH30
     (signed checkpoints, monthly partitions, archive, purge option); mark both closed in
     the Gap Analysis.
   - Data boundary: add the separate maintenance role that exports and drops archived
     partitions; the application role keeps no UPDATE or DELETE grant.
   - Add every architecture decision from gaps 1–6 of this proposal.
   - Point to PROC1, PROC2 and PROC3 in `epics.md`; they stay there as process rules.
2. Story 5.6: the VEX status mapping (locked statuses to OpenVEX and CycloneDX VEX states
   and justifications, including `accepted` and `fix_planned`) is recorded as an amendment
   to `architecture.md` and approved by the user before implementation, like the ranking
   formula (5.1) and the DQ model (8.1). Replace "the documented one from the amendment"
   with a reference to that amendment.

## Decision — task runner: mise file tasks

Status: agreed (Daniel, 2026-11-05)

Problem: `architecture.md:108` names a `Taskfile`, and `:147` says "Taskfile/Make". No
recorded user decision chose Taskfile. The repository already pins tools with `mise.toml`
(`jj`, `skaffold`).

Decision (Daniel): use mise for tool versions and for tasks. No Taskfile. Tasks are mise
file tasks in the `mise-tasks/` folder (executable scripts with `#MISE` comments; for
example `mise-tasks/check` runs as `mise run check`, `mise-tasks/gen/api` as `gen:api`).

Proposed edits:

1. `architecture.md` (`:108`, `:147`, directory tree `:325`) and ARCH1: replace Taskfile
   with mise. `mise.toml` pins every tool (Rust, Node, Helm, kind, Skaffold, Playwright
   and the others); `mise-tasks/` holds the tasks.
2. Everywhere in `epics.md` (ARCH1, ARCH23, Stories 1.1, 1.7, 2.12, 2.13, 4.8, 6.7,
   10.3, 10.4 and PROC3): `task check` becomes `mise run check`; `Taskfile.yaml` becomes
   `mise.toml` plus `mise-tasks/`; "its own task outside `task check`" becomes "its own
   mise task outside `mise run check`".
3. CI (`ci.yml`, `build.yml`, `release.yml`) installs mise with the official
   `jdx/mise-action` (v5.2.6 checked 2026-11-05, pinned by commit) and runs the same
   mise tasks as local.

## Topic 1 — Story 1.1 toolchain gaps

Status: agreed (Daniel, 2026-11-05; items 2–4 "do your recommendations", AGE image
confirmed)

1. OpenAPI generation (agreed): Story 1.1 owns generation and the CI drift check
   (ARCH12). Rust server via `openapi-generator` run from its pinned container image (no
   local Java). TypeScript via `openapi-typescript` plus `openapi-fetch`. Task
   `mise run gen:api`; `mise run check` fails if generated code differs from committed code.
2. PostgreSQL 18 with AGE (`apache/age:release_PG18_1.8.0`, pinned by digest) for
   `#[sqlx::test]` in `mise run check`, as a CI service container, and as the bundled
   chart database. Closes `architecture.md:189`.
3. Playwright in Story 1.1 with one smoke test against the Skaffold deployment, as a
   separate `mise run e2e` task that runs in CI.
4. `riverqueue`: architecture updated to `=0.5.0` (crates.io, 2026-11-02) with `sqlx` 0.9
   and `jiff`; Story 1.2 runs River migrations before `sqlx` migrations and adds a test
   that enqueues a job in a transaction and checks that a worker runs it. If the test
   fails, switch to `graphile_worker` in Story 1.2.

## Topic 2 — Forward and missing links between stories

Status: agreed (Daniel, 2026-11-05)

1. Story 4.4: remove the "blast-radius or detail lookup on a CVE" AC (`epics.md:1093`);
   Story 6.2 already keeps it (`:1449-1451`).
2. Story 4.5 creates the `signing` module (key signing and verification for bundles).
   Story 9.4 extends it to packs and adds the signing mode from gap 4.
3. Story 5.7: remove "or point to one in an air-gapped bundle" (`epics.md:1379`); upload
   through the UI or API covers air-gapped instances. No bundle change.
4. Story 2.6: new AC — each package connector re-enumerates periodically, and a new
   package version is SBOM'd and scanned within one hour (FR9), with one integration test
   per connector type. Story 2.7 connectors inherit the AC and test.
5. Story 10.2: the publishing workflow attaches SLSA provenance to each published bundle,
   and import verifies it (NFR7). Operator-built bundles keep the signature only.
6. Story 7.1: new AC — on deployment, a one-time job evaluates every stored SBOM; its
   backlog shows in the populating banner.
7. Story 1.5 tests the theme preference through the API; Story 1.6 tests the picker.
   Story 3.1 marks the cluster revoked; Story 3.2 adds the AC that marks runtime data of
   a revoked cluster stale. Story 5.3 says "the decision API"; Story 5.4 owns the form.

## Topic 3 — Technical details with no decision

Already closed by earlier decisions: tools in the agent image (gap 1), ledger tablespace
quota (gap 2), Grype DB "signature" (gap 3), Postgres-AGE image, `openapi-generator`
Java and the TS client (Topic 1).

### Part A — registries, packages and PDFs

Status: agreed (Daniel, 2026-11-05)

1. Registry discovery (Story 2.2): use the `oci-client` crate (0.18.0, checked
   2026-11-05). Discovery modes (PROC2): **catalog** (default for generic registries),
   **provider API** for ECR, Artifact Registry and Docker Hub (same read-only
   credentials), and **repository list** (names or a prefix, works everywhere).
   "Test connection" states when the catalog endpoint is missing and which mode to use.
2. Package SBOMs (Stories 2.6, 2.7): the connector downloads the archive, checks its
   checksum against the feed, unpacks it into a temporary folder (rejects path traversal
   and links outside the folder), and runs `syft dir:<path>`; JAR files use
   `syft file:<path>`. Known limit, recorded in the architecture and shown as a caveat on
   package artifacts: archives without a lock file give the package itself, not exact
   dependency versions. Story 2.6 confirms the Syft output per ecosystem (not run here).
3. PDF renderer (Stories 6.5, 9.3): Typst (0.15.1, checked 2026-11-05), a pinned static
   binary run through `tools`, no network access. Templates live in the module that owns
   the report; the bundled Inter and IBM Plex Mono fonts are passed to Typst. PDF visual
   design is a Topic 4 item.

### Part A addendum — CI scanning in v1 (scope change)

Status: agreed (Daniel, 2026-11-05). Revised the same day: all scanning runs on the
server (see "Governing principle — all scanning on the server").

Decision (Daniel): add an optional CI scan in v1, as a new epic. Central scanning stays
the default and needs no CI change (FR1). The CI runner only identifies the artifact; the
server does all scanning, matching and policy work with the fleet tools and configuration.

Design:

- Command `armoury scan`, a subcommand of the existing `armoury` binary (like
  `armoury bundle create`), plus a GitHub Action that runs it. The CLI contains no Syft,
  Grype or Grant.
- **Digest mode (default).** The image is already pushed to a connected registry. The CLI
  sends the image digest and the build details. The server pulls the image by digest with
  the connection credentials, then runs Syft, Grype, Grant and the CI policy.
- **Upload mode (fallback).** The image or package is not in a connected registry. The CLI
  uploads the built artifact (OCI image archive or package archive), never source code.
  The server computes the digest or checksum itself, stores the upload in the object
  store, then does the same work. The upload has a configurable size limit.
- The server never uses an SBOM, a finding or a verdict that the runner computes.
- Build details (repository, commit, pipeline run URL) are stored and shown as "declared
  by CI", because the server cannot verify them.
- CI scans use their own job queue priority, so a CI scan does not wait behind the
  initial fleet scan.
- Verdict: the server decides pass or fail with the fleet CI policy (for example "fail on
  high and above", "fail on KEV", "fail on licence violation"). The policy has versions,
  and each version is appended to the ledger. The CLI has no flag that changes the
  verdict. It exits with the server verdict and prints the policy version. Default
  policy: report only, so a new install breaks no pipeline.
- Exit codes: `0` pass, `1` policy failure, `2` no verdict (server unreachable, scan
  timeout or scan error). Code `2` fails the job in most CI systems. On a timeout the CLI
  still prints the URL, and the scan continues on the server.
- Report: the CLI polls for the result (gap 5 long-operation pattern) and prints the
  artifact, findings by severity, KEV findings, licence violations, duplicate status,
  verdict, policy version and the Armoury URL of the artifact. It always prints the URL.
- Duplicates: an artifact is identified by image digest, or by package coordinates plus
  archive checksum. A known artifact gets the CI scan as a new source record, not a new
  artifact; the report says "already known — also in registry `X`". An unknown artifact
  is created; later registry discovery links to it. The server produces one SBOM per
  artifact digest, so identical content is never scanned twice for the same tool
  versions.
- Access: an admin creates a scoped CI token in Settings. It can only submit scans and
  read their results; it is not a user and has no UI role.
- Accepted limit: a pipeline can skip `armoury scan` or ignore its exit code. Central
  registry discovery still scans every artifact in a connected registry.
- Not added now: lock files uploaded as extra input ("declared by CI, not verified") to
  improve package dependency detail. Upgrade path if package SBOM depth is too low.

Artifact changes:

1. PRD: new FR31 (optional CI scan: the runner identifies the artifact; the server runs
   Syft, Grype, Grant and the fleet CI policy; duplicate linking; result URL); NFR6
   mentions scoped CI tokens; "Build-time integration" in Roadmap (`prd.md:136`) is
   narrowed to what stays post-v1 (build provenance, Sigstore attestation at build).
2. `architecture.md`: the governing principle; the CI ingestion path (digest and upload
   modes); artifact identity and source records; CI policy and verdict; CI token; CI job
   queue priority; remove "build-time CI SBOM ingestion" from the roadmap (`:185, :481`).
3. `epics.md`: new Epic 11 "Scan in CI and see the result in Armoury", depending only on
   Epic 2. Draft stories: 11.1 `armoury scan` digest mode and the scoped CI token;
   11.2 upload mode; 11.3 artifact identity, source records and duplicate linking;
   11.4 fleet CI policy, server verdict, exit codes and the CI report with URL;
   11.5 GitHub Action. Numbered 11, not inserted after Epic 2, so the published Linear
   keys and sprint keys of Epics 3–10 stay stable.
4. Linear: after approval, publish Epic 11, its milestone and its stories.

### Part B — agent connection, outbound calls and sessions

Status: agreed (Daniel, 2026-11-05)

1. Agent connection (Stories 1.2, 3.2, 3.4; ARCH8): the agent uses its own control-plane
   port, separate from the UI and API port. That port serves gRPC and the HTTPS long-poll
   fallback. The control plane ends mTLS itself with `rustls`; nothing in between ends TLS.
   The chart exposes the port as a `LoadBalancer` or `NodePort` Service, or through an
   ingress with TLS passthrough. An ingress that ends TLS is not supported for this port,
   and the chart documentation says so.
2. Outbound calls (ARCH19, `architecture.md:400`, Story 10.3): two endpoint classes.
   - Admin-configured endpoints: registries, package feeds, the OIDC issuer, a private
     Fulcio and proxies. The module that owns the connection calls its configured URL.
     A default public URL that the admin accepts when saving a connection (for example
     the public npm registry) is stored in the connection record and counts as
     admin-configured.
   - Built-in public endpoints: Grype DB, KEV, EPSS, OSV, CVE List, public Fulcio and
     Rekor. Only `feeds`, `enrichment` and `signing` call them. Air-gapped mode turns
     this class off completely.
   The Story 10.3 check enforces both classes.
3. Sessions (Stories 1.3, 1.4; ARCH16): a PostgreSQL `sessions` table. The cookie holds a
   random session ID; the table stores only its hash. Sessions survive a restart; sign-out
   deletes the row. Idle timeout and maximum lifetime are Helm values (PROC2), defaults
   8 h idle and 24 h maximum. Sessions are operational data, marked "not evidence" for
   the gap 2 history coverage test.

### Part C — metrics, credential encryption, route roles and VEX matching

Status: agreed (Daniel, 2026-11-05)

1. "New critical/KEV" metrics (Story 8.3, FR20): Armoury does not define "new".
   - Counter `armoury_findings_created_total{severity, kev}` increases when a finding
     appears, and when an existing finding becomes KEV-listed.
   - Gauge `armoury_findings_open{severity, kev, triage_status}` gives the open count.
   - The example `PrometheusRule` alerts use `increase(...[1h]) > 0` and
     `armoury_findings_open{kev="true", triage_status="untriaged"} > 0`.
2. Credential encryption (ARCH17, Stories 2.2, 2.6): AES-256-GCM with `aws-lc-rs` (already
   used by `rustls`). Each credential has its own random data key; the master key from the
   Kubernetes Secret encrypts the data keys. Each record stores a key ID for rotation: add
   a new master key, re-encrypt the data keys with a job, then remove the old key. The
   record ID is AAD (associated data), so an encrypted value cannot move to another
   record. With no master key in the chart, the control plane generates one at first
   start and stores it in a Secret (same pattern as the gap 4 signing key).
3. Route roles (Story 1.4, ARCH12): every OpenAPI operation has
   `x-armoury-role: admin | analyst | auditor`. A spec test fails on an operation with no
   role. A route test calls each route with each role and expects `403` below the
   required role and no `403` at or above it. The middleware reads the same value. The
   pack-generation route also has `x-armoury-role-setting: rbac.auditorCanGeneratePacks`
   (gap 6).
4. Vendor VEX matching (Story 5.7): exact identifiers only, in this order: image digest;
   purl with version; purl without version. No fuzzy name or CPE matching. A statement
   with no fleet match is stored and shown as "no fleet match". Each applied match
   records the rule that matched, and the triage drawer shows it.

## Topic 4 — UX gaps

### Part A — shell and shared design

Status: agreed (Daniel, 2026-11-05)

1. Dimmed elements and contrast (Stories 1.5, 1.7, 6.4, 8.2; `DESIGN.md:206, 293, 300`):
   no opacity on elements that contain text. Each theme gets muted colour tokens (for
   example `data-quality-muted`, `node-inactive-text`), checked at 4.5:1 or more by the
   Story 1.5 contrast test. The low-grade DQ badge uses the muted token and keeps its
   grade letter. The "not running" graph node keeps its dashed border and its label
   "shipped, not running"; its text uses the muted token; only border and fill may be
   lighter, at 3:1 or more for non-text elements. Intent stays: quieter, never red.
   The review estimates (about 3.9:1, 3.5:1 and 2.4:1) are not measured; Story 1.5
   measures them.
2. Theme storage (Story 1.5, UX-DR4; `EXPERIENCE.md:76`): table `user_preferences`, keyed
   by a stable user ID (OIDC issuer + `sub`; fixed ID for the bootstrap admin).
   `GET` and `PUT /api/v1/me/preferences`; every role can change its own theme. Not
   evidence (gap 2, rule 2). Close the `EXPERIENCE.md` assumption.
3. Page header (Stories 1.6, 1.8, 6.3; `mockups/hybrid-posture-v2.html:368-379`): Story 1.6
   builds the header on every surface (breadcrumb, search field, compact theme control).
   Story 1.8 connects the search field to the palette, pre-scoped to blast radius. Before
   Epic 6 the field opens the normal palette; Story 6.3 adds the answer route.
   `EXPERIENCE.md` gets a "Page header" row in its component table.
4. Settings layout (Stories 1.6, 2.2, 3.2, 7.3, 8.4, 9.7, Epic 11; `EXPERIENCE.md:16, 36`,
   UX-DR28): an in-page left list of panels; each panel has its own route
   `/settings/<panel>`. Groups: Connections (registries, package feeds, agents); Feeds
   (feed status and history, bundle import); Policy (licence policy, CI policy,
   retention); Access (users and roles, resolved auth configuration, CI tokens); Signals
   (metrics, signing key); Personal (theme, keyboard shortcuts). Panels use the existing
   heading block and components; no new mockup. Edit controls are absent for roles
   without write access (UX-DR31).

### Part B — answer layouts, print, triage scope and cleanup

Status: agreed (Daniel, 2026-11-05; "rest recommended"; Svelte confirmed for B5)

1. Digest blast-radius layout (Stories 6.2, 6.3, 6.4; UX-DR23): same surface and
   components, centred on the artifact. Headline: "12 CVEs · 7 vulnerable packages ·
   runs in 3 workloads". Graph tiers left to right: CVEs → packages → artifact →
   clusters/workloads. Table: one row per finding in ranked order (KEV first), with
   triage status.
2. Printed report (Stories 6.5, 9.3): new "Printed report" section in `DESIGN.md`. Light
   print palette (white page, dark text; print only, the app keeps no light mode); Inter
   and IBM Plex Mono; A4 by default, US Letter as an option (PROC2); cover sheet first
   with the coverage and DQ statement; footer on each page with pack ID, window,
   generation time and page number; severity as a text label and a colour; long tables
   repeat their header row. No mockup; Story 9.3 produces one sample PDF for review.
3. Triage scope in the drawer (Stories 5.3, 5.4; UX-DR16): the decision form has two
   scope options, "This artifact" (default) and "Fleet-wide — every artifact with
   `CVE-x` in `package`", with the count of artifacts it changes now. Above the form, the
   drawer shows the decision that applies now and its source (for example "fleet-wide
   decision by Priya, 3 Nov" or "this artifact — overrides the fleet-wide decision").
   The table triage pill does not change.
4. Key bindings (Story 1.8, UX-DR7; `EXPERIENCE.md:84`): the current bindings are the v1
   bindings; close the assumption. A later usability test changes them through Correct
   Course. No custom key bindings.
5. `DESIGN.md:238`: "shadcn/ui + Tailwind" (the old React name) becomes
   "shadcn-svelte + Tailwind (SvelteKit)". The framework stays Svelte.

## Topic 5 — Story size and acceptance criteria without numbers

Status: agreed (Daniel, 2026-11-05; licence policy "unopinionated by default with
configurable settings")

### Part 1 — splits (new stories take the next free number in their epic, so published
Linear keys and sprint keys stay stable)

1. Story 1.7 keeps the axe gate, keyboard and focus, `aria-live`, reduced motion, the
   message catalogue and the responsive layouts. New **Story 1.9 "Banned-pattern
   guards"**: the frontend guide, the overlay limit (drawer + one dialog), the toast rule,
   the one-primary-button lint and the celebratory-animation lint.
2. Story 5.3 keeps per-artifact decisions, superseding, the auditor 403, propagation and
   reappearance. New **Story 5.8 "Fleet-wide triage decisions"**: the fleet-wide scope,
   the override rule, and the drawer parts from Topic 4 part B item 3. Story 7.4 uses
   the scope choice; Epic 7 comes after Epic 5, so no forward link.
3. Story 9.7 keeps the retention setting, the archive job for ledger and history
   partitions, reads from archived windows and verification. New **Story 9.8 "SBOM
   compaction and archive purge"**: SBOM blob compaction and the optional purge.

### Part 2 — approval-then-build stories (3.1, 4.5, 5.1, 8.1)

No separate spike stories. The first AC of each story already requires user approval of
the amendment before implementation, at Build CHECKPOINT 1. Story 3.1 is not split,
because Story 3.2 uses its revocation (Topic 2).

### Part 3 — numbers for vague acceptance criteria (configurable where a setting makes
sense, PROC2)

- 2.13 latency: p95 ≤ 500 ms for the posture, findings page (50 rows) and artifact list
  endpoints at the scale anchor, while the initial evaluation runs.
- 2.13 estimate: when 10 % of the backlog is done, the banner estimate is within ±25 % of
  the actual completion time.
- 3.3 reconnect: during the ten-agent reconnect test, API p95 stays below 1 s.
- 3.3 heartbeat: every 30 s; `stale` after 5 min; `disconnected` after 60 min (Helm
  values). Closes the `EXPERIENCE.md:136` assumption.
- 4.7 freshness: connected mode, each daily feed (Grype DB, KEV, EPSS, CVE List, OSV) is
  stale after 48 h; air-gapped mode, the bundle is stale after 7 days.
- 6.7 latency: p50 ≤ 5 s, p95 ≤ 30 s, every query < 60 s (NFR2).
- 1.7 responsive: Playwright checks each shell route at 1440, 1100 and 900 px; no page
  horizontal scroll (only tables and graphs scroll); every control visible and reachable
  by keyboard.
- 7.3 licence policy default: unopinionated. Empty allow list and empty deny list;
  licences on neither list are `ignore`; unknown licences are `warning`. No violations
  until the admin sets a policy. Every treatment is configurable.

## Topic 6 — Minor items

Status: agreed (Daniel, 2026-11-05)

1. Artifact types (`prd.md:160` glossary, Story 2.11): four types, `image`, `package`,
   `oci_artifact` and `filesystem`. A CI upload (Epic 11) is a source of an artifact, not
   a type: an uploaded image is an `image`, an uploaded package is a `package`.
2. PRD basis for Stories 10.1 and 10.2: FR10 adds "Armoury also publishes signed bundles,
   so an operator does not need a connected build machine." NFR7 adds "Each release
   publishes Armoury's own scan result."
3. NFR1 initial-scan projection (Story 2.13): measure throughput for at least 1 hour after
   a 10-minute warm-up; the projected completion must be 18 hours or less (25 % margin to
   the 24-hour limit).
4. FR14 "team consumption": the findings API, VEX export (Story 5.6) and the
   `triage_status` metric label (Topic 3 part C item 1). Story 5.3 adds one AC: a recorded
   decision appears in the findings API and in the metric label.
5. `architecture.md`: line 451 `control-plane/internal` becomes "the `control-plane`
   crate"; line 455 is replaced by the two-class outbound rule (Topic 3 part B item 2).

## Review decisions (after the independent review)

### Decision R1 — CI client publication

Status: agreed (Daniel, 2026-11-05)

Problem: Story 11.5 downloaded an `armoury` CLI "from GHCR", but no story built or
published a standalone CLI, and the GitHub Action had no home.

Decision: publish a standalone CLI binary; Story 11.5 owns it.

1. Story 11.5: the release workflow builds the `armoury` CLI for Linux and macOS
   (x86-64, arm64) and publishes each binary as a GitHub Release file with a checksum,
   a cosign signature and SLSA provenance (NFR7). The CLI contains no scanners (NFR12).
2. The GitHub Action lives in `action/` in this repository, with the same version tags as
   the CLI. It verifies the checksum and signature before it runs `armoury scan`; a failed
   check fails the step. A separate Marketplace repository can come later.
3. `architecture.md`: CI client bullet, `action/` in the directory tree.

### Decision R2 — CI token access to the API

Status: agreed (Daniel, 2026-11-05)

Problem: every route declares `x-armoury-role: admin | analyst | auditor`, but a CI token
is not a user and has no role, so the middleware and the route test had no rule for it.

Decision: a separate route marker, not a fourth role.

1. CI routes declare `x-armoury-ci-token: true` as well as their user role. CI tokens use
   `Authorization: Bearer <token>`; a session cookie never counts as a CI token. The
   middleware accepts a CI token only on marked routes and returns 403 elsewhere. NFR6
   keeps three user roles.
2. Story 1.4 builds the marker support and proves it with a test-only marked route; the
   route test adds a "CI token" caller.
3. Story 11.1 adds the real CI routes with the marker; the Story 1.4 route test then
   covers them.
4. `architecture.md` (route roles) and ARCH12 record the rule.

### Decision R3 — Signing key for Armoury-published feed bundles

Status: agreed (Daniel, 2026-11-05: "the safe approach that stays out of the user's way")

Problem: releases are signed keyless, but Story 10.2 signs bundles with a "release signing
key", ships its public key and plans a rotation. Nothing said where the private key lives.
Only air-gapped instances import published bundles.

Decision: option 1.

1. Story 10.2: a long-lived bundle signing key in a cloud KMS that cosign supports; the
   provider is chosen in Story 10.2. The private key never leaves the KMS; the workflow
   authenticates with GitHub OIDC, so the repository stores no long-lived secret.
2. The chart ships the public key in the Story 4.6 trusted-key list; users configure
   nothing.
3. Rotation: the chart ships the old and new public keys together for 12 months; the
   release notes state each rotation.
4. `architecture.md` signing section records the exception to keyless release signing.

### Decision R4 — Defaults for the remaining ACs without numbers

Status: agreed (Daniel, 2026-11-05). Every value is a Helm value with this default (PROC2).

- 1.3 sign-in rate limit: 5 failures per username in 15 min block that username for
  15 min; 20 attempts per source IP in 15 min.
- 2.2 retry: exponential backoff, 1 min first wait, doubled, at most 1 h, no retry limit;
  Settings shows the next retry time.
- 2.3 worker pool: the CPU limit of the control-plane pod, at least 2.
- 2.5 and 2.6 re-enumeration: every 15 min.
- 4.1, 4.3, 4.4 feed schedules: every 6 h (fits the 48 h staleness limit in Story 4.7).
- 6.1 graph consistency check: once a day.
- 6.4 graph display limit: 25 nodes per tier.
- 7.2 filesystem upload limit: 2 GiB.
- 9.8 SBOM snapshot archive: 90 days after a newer snapshot replaces it.
- 11.1 CI queue priority: a CI scan starts within 60 s of submission.
- 10.2 key overlap: 12 months (Decision R3).

## Readiness gate rerun (2026-11-05, after approval)

Independent reviewer verdict: CONCERNS — no blockers; all items from the earlier review
resolved. Fixed without a new decision (text corrections only):

- Epic 11 dependency list: builds on Epics 2, 4, 5, 6, 7 and 10 (long-operation pattern
  from Story 6.2; release workflow from Story 10.1). Linear relations updated (INF-91 blocked by INF-14, INF-16, INF-17, INF-18, INF-19, INF-22).
- Story 3.2: only reporting connections need a client certificate; enrollment (Story 3.1)
  uses the enrollment token.
- Story 1.4 builds `x-armoury-role-setting` support (Story 9.5 relies on it).
- River queue tables (Story 2.1 list) and AGE graph tables (Story 6.1) marked
  "not evidence".
- `architecture.md`: Grant is not re-run on a policy change; GUAC lines marked historical
  or superseded; implementation sequence marked indicative; scheduled `bundles.yml` for
  Story 10.2.
- Story 2.11 source list includes "CI upload"; FR10 and NFR7 summaries in `epics.md`
  match the PRD; Story 10.1 states how the release scans its own images.

Open for decision: published bundle base snapshot (concern A), offline provenance
verification for published bundles (concern B), and three small defaults.

### Decision R5 — Published bundles are complete (concern A)

Status: agreed (Daniel, 2026-11-05: option 1)

Problem: the published "core" bundle carried only a daily CVE List v5 delta, so a fresh
air-gapped instance, or one that skipped days, could not import it.

Decision: every Armoury-published bundle is complete. The core bundle carries the full
CVE List v5 snapshot (about 0.8 GB, measured 2026-11-04). Any published bundle imports
into any instance. Operator-built bundles (Story 4.5) can still carry deltas. Story 10.2
adds a test that imports a bundle 7 days newer than the active bundle. A weekly base plus
daily update bundles stays a later option if size becomes a problem.

### Decision R6 — Offline provenance check for published bundles (concern B)

Status: agreed (Daniel, 2026-11-05: option 1)

Problem: GitHub SLSA provenance is signed keyless, and an air-gapped instance has no
Sigstore trust root to verify it offline.

Decision: `bundles.yml` signs the SLSA provenance of each published bundle with the same
KMS bundle key (`cosign attest --key`). The import verifies the bundle signature and the
provenance offline with the one public key that the chart ships. No trust root is needed,
and users configure nothing.

### Decision R7 — Last three values

Status: agreed (Daniel, 2026-11-05: "recommended")

1. Story 4.8: choose the full re-check only if it completes in 45 minutes or less (25 %
   margin to the one-hour bound); otherwise keep `grype db diff`.
2. Story 2.1: external Postgres has no default budget. With no budget set, the health
   endpoint reports ledger and history size only, with "no budget set — headroom
   unknown" and no warning. With a budget set, the warning starts at 80 % used.
3. Story 11.4: by default a vendor VEX `not_affected` statement that matches the artifact
   exactly (Story 5.7 rules) keeps the finding from failing the CI policy. A team
   decision always wins; the CI report names the vendor statement; an admin can turn this
   off with `ciPolicy.trustVendorVex` (default `true`).

## Readiness gate rerun 2 (2026-11-05)

Independent reviewer verdict: CONCERNS — all earlier concerns resolved; no blockers.
Text fixes applied without a new decision: Story 2.1 "not evidence" list adds
`_sqlx_migrations` and the AGE graph tables from Story 1.2; feed-bundle signing stated
consistently (operator-built bundles: operator key; published bundles: KMS key in
`bundles.yml`; `release.yml` signs images, chart and CLI keyless) in ARCH18, ARCH23 and
`architecture.md`; Story 4.8 states the R7 rule in full; ARCH5 and `architecture.md`
state the external-Postgres no-budget case; Story 11.3 has the server derive package
coordinates (NFR12); Story 10.2 size wording (whole core bundle about 0.8 GB); DESIGN.md
High Signal contrast targets clarified and checked in Story 1.5. Story 10.2 KMS provider
needs Daniel's cloud account — raise when the story starts.

Open for decision: the database role and table-ownership model (NFR11 depends on it).

### Decision R8 — Database role and table ownership

Status: agreed (Daniel, 2026-11-05: option 1)

Problem: Story 1.2 ran migrations in the control plane, so the application login owned
the tables. A PostgreSQL owner always has full rights, so the "no UPDATE or DELETE grant"
test proved nothing, and NFR11 depended only on code.

Decision: two logins.

1. `armoury_owner` owns every schema and table. Only the migration Job (`armoury migrate`,
   Helm pre-install/pre-upgrade hook; also creates monthly partitions 3 months ahead) and
   the maintenance CronJob (future partitions, archive and drop) use it.
2. `armoury_app` owns nothing and is the only login of the control-plane pod. It can insert
   into ledger and history tables, but not update or delete. Story 2.1 tests run as
   `armoury_app` and also prove that it owns no table.
3. Two Secrets; the control-plane pod cannot read the owner Secret.
4. Bundled database: the chart creates both logins and the AGE extension; the user
   configures nothing. External database: the user supplies both logins; the owner login
   can create schemas; a database administrator installs AGE once. Story 1.2 confirms and
   documents the exact rights, and the migration Job fails with a clear message when one
   is missing.
5. Applied to Stories 1.2, 2.1, 9.7, ARCH5, ARCH30 and `architecture.md` (Data boundary,
   Retention).

## Readiness gate rerun 3 (2026-11-05)

Verdict: CONCERNS — all earlier items resolved, no blockers. Wording fixed: Story 4.8 R7
rule; Story 1.5 contrast check covers the muted and border tokens in all themes; ARCH5
cites "risks R5, R9". Open for decision: migration Job timing on a fresh bundled install,
owner of future monthly partitions, overlap enforcement on partitioned history tables,
source of the bundled Postgres volume free space.

### Decision R9 — Database operations details

Status: agreed (Daniel, 2026-11-05: "recommended")

1. The migration Job runs as a Helm `post-install` and `pre-upgrade` hook. The control
   plane reports not ready until the schema version matches its expected version. A fresh
   `helm install` stays one command (Story 1.2).
2. Story 2.1 adds the daily maintenance CronJob (as `armoury_owner`). It keeps partitions
   3 months ahead and warns on the health endpoint and in metrics when less than 1 month
   remains; a test proves it. Story 9.7 later adds archive and drop to the same CronJob.
3. `WITHOUT OVERLAPS` is removed. Only the trigger writes history, and each version closes
   when the next starts. A test changes rows across a month boundary and checks that no
   versions overlap. PostgreSQL 18 stays (AGE image).
4. Bundled database headroom = PVC size (read access to that one PVC) minus
   `pg_database_size`. `ponytail:` ignores WAL and file-system overhead; upgrade path is a
   sidecar in the database pod.

### Decision R10 — Optional Rekor anchoring of ledger checkpoints

Status: agreed (Daniel, 2026-11-05: "default is disabled, with option 1 or 2 available,
include it in the helm chart, comments recommend external Rekor")

Rekor is not a ledger replacement: Rekor v2 stores only a digest, a signature and a
public key per entry (`hashedrekord`), has no search, and the public instance needs
internet. It is useful as an external witness for signed checkpoints.

1. New Story 9.9 and ARCH37. Setting `rekor.anchoring.mode`: `disabled` (default),
   `external` (public `rekor.sigstore.dev` or a Rekor that another team runs) or
   `bundled` (`rekor-tiles`, POSIX backend, own volume, log key in a Secret created once).
2. A witness is not required (`--witness-policy-path` is optional in `rekor-tiles`); an
   optional witness policy is a chart value.
3. Chart comments recommend `external`: a bundled Rekor shows accidental damage, but an
   administrator of the same cluster can rebuild it.
4. Each entry sends only the checkpoint digest, signature and public key. The public key
   links the entries of one installation. Air-gapped mode refuses the public Rekor.
5. Failures leave the anchor pending and never block the ledger.
6. Known limit (found while writing the story): Rekor v2 returns no signed timestamp. A
   full rebuild that is anchored again is found only by comparing with an earlier receipt
   (evidence packs carry the latest anchored checkpoint) or by monitoring the log. An
   RFC 3161 timestamp authority is the upgrade path.
7. PRD NFR11 gets one sentence; Story 10.3 lists the `rekor-tiles` image; the
   admin-configured endpoint class includes a configured Rekor.

Gate text fixes applied at the same time: Story 2.1 warns on the health endpoint and
Story 8.3 adds the partition runway metric; Story 1.2 documents no `--wait`/`--atomic`,
the Job retries the database connection for up to 10 minutes, readiness is "schema at
least the expected version", partitions start with Story 2.1; ledger appends are
serialized with a PostgreSQL advisory lock (Story 9.7, architecture Retention item 7).

### Decision R11 — History partition key

Status: agreed (Daniel, 2026-11-05)

History tables are partitioned by month on `valid_to` (the close time); the ledger by
entry time. A closed version always goes into the current month, so a row that was
unchanged for more than the retention period can still change. "Wholly older than
retention" (Story 9.7) uses that column. Story 2.1 adds a test that closes a version whose
`valid_from` is in an archived month. Applied to ARCH30, ARCH32, Story 2.1 and
`architecture.md`.

## Readiness gate rerun 4 (2026-11-05)

Verdict: CONCERNS — no blockers, no new decision needed. Text fixes applied: ARCH19 and
Story 10.3 list a configured Rekor as admin-configured and "public Rekor" as built-in;
Story 2.1 serializes ledger appends with an advisory lock and tests concurrent appends;
ARCH30 names the partition keys; the NFR11 summary in `epics.md` matches the PRD; Story
8.3 metric covers ledger and history partition runway; the Story 2.1 R11 test drops the
partition itself.
