# Agent Readiness: Armoury

This document is the project's feedback-loop strategy for coding agents. It records the agreed
principles, the checks that enforce them, how each check reaches the agent, and the proof that
each loop works. Owner: Daniel (decisions), Vera (mechanisms), Murat (validation design).

## Status

- Status: building
- Phase: 2 of 3 complete (design). Phase 3 (build, rehearse, assess) runs after Story 1.1 Build.
- Agreed threshold: scorer 8/10 or more AND every applicable critical loop proven (fail, then pass)
  through the channel the agent uses. A score alone never makes this document `ready`.
- Last scorer result: level 1 (Foundational), 3 of 10 level-2 criteria
  (`agent-readiness-checklist.md`, before any code). Not a phase 3 measurement.
- Linear: INF-12 (In Progress), https://linear.app/infantry-cloud/issue/INF-12/agent-readiness-ar
- Designed: 2026-11-06, Vera with Daniel.

While the status is `building`, Story 1.1 Build may run as user-authorised readiness work
(Steward Decision SD-2). No other story starts Build until the status is `ready` (PROC1).

## Methodology and principles

The primary organising principle is **Locality of Behaviour** (ARCH25): everything that changes
together lives together. Code is organised by capability, never by technical layer.

| ID | Principle | Weight | Source |
| --- | --- | --- | --- |
| P1 | Locality of Behaviour | critical | architecture.md "Implementation Patterns" |
| P2 | Security and supply chain (NFR4, NFR7, NFR11, NFR12) | critical | prd.md NFRs; architecture.md |
| P3 | Type safety | critical | architecture.md (generated types, locked enums) |
| P4 | Test confidence | important | architecture.md "Tests"; story-contract.md |
| P5 | Delivery speed | important | interview 2026-11-06 |
| P6 | Documentation | lightweight | interview 2026-11-06 |

Weights confirmed by Daniel, 2026-11-06. Critical rules get a hard block (local gate and CI)
wherever a reliable check exists. Important rules get at least a warning plus review evidence.
Lightweight rules get a context surface or a named manual check.

Resolved conflicts:

- **Delivery speed vs complete checks (P5 vs P2/P4).** The gate is split into a fast tier and a
  cluster tier. The handoff gate is always the full `mise run check`; `check:fast` is for
  iteration only.
- **LoB vs strict layering (P1).** LoB wins. The architecture caps layers at three; there is no
  `models/`/`services/`/`repositories/` split.
- **"No unwrap/expect outside startup" vs a simple lint.** Clippy denies both everywhere except
  tests. Startup code uses `?` with `anyhow`, or a reasoned `#[allow]` in `src/main.rs` only.

## Inputs and assumptions

Inputs read (Phase 0):

- `_bmad-output/planning-artifacts/architecture.md`, `epics.md` (ARCH1-37, PROC1-3),
  `prds/prd-Armoury-2026-06-11/prd.md` (NFR1-12), `sprint-change-proposal-2026-11-05.md`,
  `briefs/brief-Armoury-2026-06-11/addendum.md` (commercial model parked).
- `_bmad-output/implementation-artifacts/epic-1-context.md`, the STORY-1.1 spec and
  `_bmad-output/test-artifacts/atdd-checklist-1-1-monorepo-scaffold-with-an-aggregate-local-gate-and-ci.md`.
- `.agent-profile.yml`, `agent-readiness-checklist.md`, `.pi/extensions/`, `.mcp.json`,
  `.pi-recipe`, `mise.toml`.
- Workstation observation, 2026-11-06: macOS arm64, Pi 1.5.0, Podman 6.1.4 (machine 2 GiB),
  kubectl 1.37.2, Helm 4.3.1, Node 26, no Rust, no kind. Remote `Infantry-Cloud/Armoury`:
  private, empty, GitHub Free plan.

Inherited decisions (facts): mise pins and `mise-tasks/`; `mise run check` as the aggregate gate;
GitHub Actions running the same tasks; Skaffold dev loop (PROC3); jj with story contracts and
locked ATDD tests; `AGENTS.md` only (no `CLAUDE.md`).

Inferences (not observed): the likely agent failure modes in the register below. No historical
agent failures exist yet in this project.

Conflicts and stale planning text, resolved with Daniel:

| Conflict | Resolution | Follow-up |
| --- | --- | --- |
| architecture.md says "Helm 3"; host has Helm 4.3.1 | D1: pin Helm 4 | Correct Course (OI-4) |
| PROC3, ARCH34, Stories 1.1, 1.2, 2.12 use kind on local Podman | D3-D8: dev cluster, in-cluster BuildKit, ARC runners | Correct Course + Build re-plan of 1.1 (OI-4) |
| AR default is devcontainer + Dagger | Native host with mise; mise tasks are the parity layer | Recorded below |
| CodeQL needs a licence on a private Free-plan repo | Make the repository public (after phase 3 proofs) | OI-5 |

## Decisions

| ID | Decision | Date |
| --- | --- | --- |
| D1 | mise pins Helm 4.x. The "Helm 3" text in architecture.md is out of date. Customer docs state supported Helm versions. | 2026-11-06 |
| D2 | The classic `GITHUB_TOKEN` in agent sessions is an accepted residual risk (see threat model). Expires 2027-02-06. | 2026-11-06 |
| D3 | Daniel owns the dev cluster. Every cluster command names its kube context explicitly; no task relies on the current context. | 2026-11-06 |
| D4 | Images build on a rootless, mTLS `buildkitd` in the cluster. mise pins a standalone `buildx`; Skaffold calls it explicitly. | 2026-11-06 |
| D5 | Dev images go to Harbor or Artifact Keeper (OI-2), set through `SKAFFOLD_DEFAULT_REPO`. Registry layer cache lives there too. | 2026-11-06 |
| D6 | The AGE test database is a digest-pinned Pod in the cluster. `mise run check` reaches it (port-forward locally, Service DNS on ARC). No local database. | 2026-11-06 |
| D7 | `openapi-generator` runs as a digest-pinned BuildKit stage with `--output type=local`. No local Java, no local container. | 2026-11-06 |
| D8 | CI runs on GitHub-hosted runners (fast tier) and ARC self-hosted runners in the cluster (cluster tier, e2e). kind and Podman leave the project. | 2026-11-06 |
| D9 | `mise run check` stays the one parity command. Dagger is rejected. `act` (0.2.97, pinned) is available if local workflow runs become necessary. | 2026-11-06 |
| D10 | Edit-time feedback: pi-lens plus the project readiness extension. | 2026-11-06 |
| D11 | Security set: CodeQL (CI), gitleaks, cargo-deny, `npm audit signatures`, Renovate. | 2026-11-06 |
| D12 | CI feedback for the agent: official GitHub MCP server, `actions` toolset, read-only. | 2026-11-06 |
| D13 | Fork PRs: split CI tiers plus "require approval for all outside collaborators". `pull_request_target` is banned. | 2026-11-06 |

## Environment threat model

**Boundary: unsandboxed native host with mise.** Pi runs as Daniel's macOS user and inherits all
of that user's permissions. Nothing here is sandboxed. A devcontainer was offered and declined.

| Asset | Exposure | Control |
| --- | --- | --- |
| Classic `GITHUB_TOKEN` (env) with `repo`, `workflow`, `write:packages`, `delete_repo`, `admin:org`, `admin:enterprise` | Agent can delete repos, change org settings, publish packages | **Accepted residual risk (D2), expires 2027-02-06.** jj rules forbid pushes; agents run only `jj new`/`jj describe`. Revisit: replace with a fine-grained repo token before expiry. |
| Kubeconfig (all contexts) | Agent can act on any context, including non-dev clusters | D3: tasks pass an explicit context from `ARMOURY_KUBE_CONTEXT` (set in untracked `mise.local.toml`); no task uses the current context. Daniel owns cluster RBAC. |
| BuildKit mTLS client certificate | Agent can build and push images | Stored outside the repo (for example `~/.config/armoury/buildkit/`); never committed. |
| Dev registry credentials | Push to dev repositories | Host Docker config only; never in the repo or image layers. |
| `~/.ssh`, `gh` keyring, Linear OAuth | Inherited by Pi | Not mounted anywhere new; no task reads them. |
| Production credentials | None on this host | Must stay absent from dev sessions (project-context.md). |

- Network egress: unrestricted host network. No proxy is claimed.
- CI boundary: hosted runners for untrusted code (fork PRs); ARC runners only for `push` and
  same-repo PRs, ephemeral, in a runner group limited to this repository, with a ServiceAccount
  scoped to the CI namespace.
- Merge protection: a ruleset on `main` requires the CI gate job (phase 3, applied by Daniel).
- Validation evidence: pending (phase 3): fresh-clone `mise install && mise run check`, explicit
  context use, absence of production credentials, Pi discovery of the agent surface.

## Aggregate gate

`mise run check` is the handoff gate, locally and on ARC. It runs these steps in order, fails fast
and prints the failing step name. Story 1.1 builds the product steps; phase 3 adds the rest.

| Tier | Step (`mise-tasks/check/...`) | Purpose |
| --- | --- | --- |
| fast | `pins` | Exact pins and lockfiles (VAL-5) |
| fast | `workflows` | `actionlint`; top-level `permissions:`; no `pull_request_target` |
| fast | `lob` | Locality of Behaviour structure rules (R1-R9) |
| fast | `secrets` | `gitleaks dir` on the working copy |
| fast | `rust` | `cargo fmt --check`, `cargo clippy --locked -- -D warnings`, `cargo deny check` |
| fast | `test-rust` | `cargo nextest run` without the database group |
| fast | `web` | `npm ci`, `npm audit signatures`, ESLint, Prettier, `svelte-check`, Vitest |
| fast | `chart` | `helm lint` |
| fast | `api` | `gen:api` into a temporary directory, then `diff -r` with committed output (no VCS) |
| cluster | `test-db` | `cargo nextest run` database group against the AGE Pod |
| both | `contracts` | Contract validator `ci --require-jj` with this run's JUnit reports |

`mise run check:fast` runs only the fast tier. It is for iteration and the fork-PR CI tier,
never for handoff. `mise run e2e` runs Playwright against the Skaffold deployment.

## Feedback Loop Register

Tiers: E = edit time, L = local gate, H = CI hosted runner, A = CI ARC runner.
Budgets are initial targets; phase 3 records the first measurements without claiming gains.

| Loop | Failure mode | Check and trigger | Diagnostic reaches agent | Expected correction | Budget | Tier | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L1 | Type or lint error while editing | pi-lens LSP (rust-analyzer, TS/Svelte) on each write | Tool result after write | Fix the reported line | < 5 s | E | deferred: Story 1.1 T2/T5 |
| L2 | File in `utils/`/`helpers/`/`common/`, edit of generated code, `CLAUDE.md` | `.pi/readiness.rules.json` + `readiness-enforce.ts` on write/edit | Tool call refused with reason | Put code in a capability module; run `gen:api` | immediate | E | deferred: phase 3 |
| L3 | Edit of approved contract or locked test | `.pi/extensions/contract-guard.ts` | Tool call refused with validator reason | Stop; Correct Course | immediate | E | active (shipped); agent-channel proof: phase 3 |
| L4 | LoB violation (globals, `anyhow` outside main, file > 500 lines, no purpose line, agent depends on control-plane) | `check/lob` | Gate output names file and rule | Restructure | < 10 s | L, H | deferred: Story 1.1 / phase 3 |
| L5 | `unwrap`/`expect`/`unsafe`, clippy warning, bad format | `check/rust` with workspace lints | Clippy file:line | Use `?`, fix lint | < 2 min warm | L, H | deferred: Story 1.1 T2-T3 |
| L6 | Broken Rust behaviour | `check/test-rust`, `check/test-db` | nextest failure output | Fix code, rerun focused test | < 3 min | L, H, A | deferred: Story 1.1 T2-T3 |
| L7 | Broken web types, lint, behaviour | `check/web` | ESLint/svelte-check/Vitest output | Fix code | < 2 min | L, H | deferred: Story 1.1 T5 |
| L8 | Invalid chart | `check/chart` | `helm lint` output | Fix template | < 10 s | L, H | deferred: Story 1.1 T6 |
| L9 | Generated code drift or hand edit | `check/api` | `diff -r` output | Run `mise run gen:api` | < 1 min | L, H | deferred: Story 1.1 T4 |
| L10 | Floating version, missing lockfile | `check/pins` (VAL-5) | Offending file named | Pin exactly | < 5 s | L, H | deferred: Story 1.1 T7 |
| L11 | Secret, vulnerable crate, bad npm signature | `check/secrets`, `cargo deny`, `npm audit signatures` | Tool output | Remove secret / bump dep | < 1 min | L, H | deferred: phase 3 |
| L12 | Unsafe workflow change | `check/workflows` | actionlint / rule output | Fix workflow | < 5 s | L, H | deferred: phase 3 |
| L13 | Weakened, skipped or missing acceptance test; contract drift | `check/contracts` (validator `ci --require-jj` + JUnit) | Validator errors with `Read:` links | Activate or fix test; Correct Course | < 10 s | L, A | deferred: phase 3 |
| L14 | Change breaks the running system | `skaffold dev` on dev cluster (PROC3) | Skaffold build/deploy output, pod logs | Fix, wait for redeploy | < 2 min redeploy | E | deferred: Story 1.1 T9 |
| L15 | UI does not load | `mise run e2e` (VAL-10) | Playwright report | Fix code | < 5 min | L, A | deferred: Story 1.1 T9 |
| L16 | CI-only failure | GitHub MCP `actions` (read-only) | Failed job logs in agent | Reproduce locally, fix | < 1 min to read | A, H | deferred: phase 3 |
| L17 | SAST finding | CodeQL on hosted runners | Code scanning alert (MCP/UI) | Fix or dismiss with reason | per push | H | deferred: repo public (OI-5) |
| L18 | Stale pins | Renovate PRs (weekly) | PR with CI result | Review and merge | weekly | H, A | deferred: phase 3 |
| L19 | Readiness coverage drift | Scorer in CI, non-blocking | CI annotation | Investigate gap | per push | H | deferred: phase 3 |

Representative failure and repair rehearsal (phase 3): at least L2, L4, L5, L9, L10 and L13,
plus one CI failure read through L16, each recorded with elapsed time and evidence.

## Engineering principles traceability matrix

Enforcement levels: hard, warning, context, manual. "Trigger" lists the agent-facing trigger first.

| Rule | Principle | Rule text | Level | Mechanism and path | Trigger | CI gate | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| R1 | P1 | No `utils/`, `helpers/`, `common/` | hard | `.pi/readiness.rules.json`; `check/lob` | write/edit; gate | H | deferred phase 3 |
| R2 | P1 | No `unwrap`/`expect` outside tests and startup | hard | `[workspace.lints.clippy] unwrap_used, expect_used = "deny"`; `clippy.toml` allow in tests; `check/lob` fails on `#[allow(clippy::unwrap_used\|expect_used)]` outside `src/main.rs` | pi-lens; gate | H | deferred 1.1 |
| R3 | P1 | No `unsafe` | hard | `[workspace.lints.rust] unsafe_code = "forbid"` | pi-lens; gate | H | deferred 1.1 |
| R4 | P1 | No globals or singletons | hard | `check/lob`: `static mut`, `static` with `Mutex`/`RwLock`/`OnceLock`/`LazyLock`, `lazy_static`, `once_cell` | gate | H | deferred phase 3 |
| R5 | P1 | Wiring only in `main.rs`; max 3 layers; traits at third use | manual | Test Architect review (M1); context in `AGENTS.md` | review | - | active from 1.1 |
| R6 | P1 | `anyhow` only in `main.rs`; one `thiserror` enum per capability | hard (anyhow) / manual (enum) | `check/lob`; review | gate | H | deferred phase 3 |
| R7 | P1/P6 | File opens with a purpose line; split at 500+ lines | hard (> 500, purpose); warning (> 400) | `check/lob` | gate | H | deferred phase 3 |
| R8 | P1 | `agent` crate depends on nothing in `control-plane` | hard | `check/lob` via `cargo metadata` | gate | H | deferred phase 3 |
| R9 | P2 | Exact pins (mise, Cargo `=`, npm exact, image `@sha256`, action SHA); lockfiles committed | hard | `check/pins` (VAL-5) | gate | H | deferred 1.1 |
| R10 | P2 | No secrets in repo or history | hard | `check/secrets` (gitleaks dir); CI gitleaks full history; GitHub secret scanning + push protection once public | gate; CI | H | deferred phase 3 |
| R11 | P2 | No known-vulnerable or disallowed dependency | hard | `cargo deny check` (`deny.toml`); `npm audit signatures`; Renovate; Dependabot alerts once public | gate; weekly | H | deferred phase 3 |
| R12 | P2 | SAST clean or reasoned dismissal | hard | CodeQL (Rust, JS/TS, Actions) required check | CI | H | deferred OI-5 |
| R13 | P2 | Workflows least privilege; no `pull_request_target`; fork code never on ARC | hard | `check/workflows`; job `if:` conditions; `ci-gate` job fails when the ARC tier was skipped | gate; CI | H | deferred phase 3 |
| R14 | P2 | Agent image has no scanners (NFR12) | manual now | VAL-8 (STORY-1.1); mechanical in Story 10.1 (release SBOM) | review | - | active 1.1 |
| R15 | P2 | Outbound only from owning modules; off in air-gap (NFR4) | hard later | Story 10.3 check | gate | H | deferred: Story 10.3 |
| R16 | P2 | Evidence append-only (NFR11) | hard later | DB grant test (no UPDATE/DELETE for `armoury_app`) | gate | A | deferred: Story 1.2 / 2.1 |
| R17 | P2 | Every operation declares `x-armoury-role` | hard later | Spec test | gate | H | deferred: Story 1.4 |
| R18 | P2 | Credentials never logged | manual now | Review (M2); redaction test | review | - | deferred test: Story 1.3 |
| R19 | P3 | No warnings; strict types | hard | `clippy -D warnings`; `svelte-check` with strict `tsconfig` | pi-lens; gate | H | deferred 1.1 |
| R20 | P3 | Generated code never hand-edited | hard | `check/api` drift; R1 block list includes generated paths | write/edit; gate | H | deferred 1.1 / phase 3 |
| R21 | P3 | Locked enums and glossary, never free strings | manual now | Review (M6); typed enums in OpenAPI/Rust/TS | review | - | deferred check: first triage-status story (Epic 5) |
| R22 | P4 | Aggregate gate passes before handoff and in CI | hard | `mise run check`; Build and Code Review hooks; ruleset on `main` | handoff; CI | H, A | deferred phase 3 |
| R23 | P4 | Acceptance tests run, pass and stay unweakened | hard | Locked tests; `check/contracts` with JUnit; edit guard | gate; CI | A | deferred phase 3 |
| R24 | P4 | Coverage measured | - | not adopted now | - | - | deferred: trigger = a review finds untested logic twice |
| R25 | P5 | Feedback within budget | warning | Budgets in register; phase 3 measures; slow steps get routed, not removed | phase 3 | - | deferred phase 3 |
| R26 | P6 | `AGENTS.md` states LoB rules, layout, PROC3; README commands work | manual | VAL-13 (STORY-1.1); M7 | review | - | active 1.1 |
| R27 | P6 | `LICENSE`, `SECURITY.md`, `CODEOWNERS` present | context | Files at repo root | - | - | deferred: LICENSE OI-1; SECURITY.md + CODEOWNERS phase 3 |
| R28 | process | `skaffold dev` runs during development (PROC3) | context + manual | `AGENTS.md`; review asks for redeploy evidence (M5) | - | - | deferred 1.1 |

### Enforcement coverage

- Every agreed principle (P1-P6) maps to at least one rule above. Every rule has an active or a
  deferred mechanism with a trigger. **Orphans: none.**
- Critical rules without a reliable hard block today: R5 (layers, wiring, traits), R14, R18, R21.
  Each has an approval-blocking manual check (M1-M3, M6) until its mechanical check exists.
- Story-specific guards from planning stay with their stories: message catalogue (1.7), banned
  patterns (1.9), RBAC spec test (1.4), outbound check (10.3).

## Contract CI Wiring

Every mechanical VAL-* is planned as `path::test name` and carries its VAL ID in the test name or
a reporter tag. JUnit reports go outside the workspace (`$RUNNER_TEMP` in CI,
`$TMPDIR/armoury-check/` locally). The local gate runs the same contract step as a preview.

| Suite | Test command | JUnit report | VAL ID convention | Contract and test identity | Runs in |
| --- | --- | --- | --- | --- | --- |
| Rust (nextest) | `cargo nextest run --profile ci` with `CARGO_TARGET_DIR` outside the workspace | `<target>/nextest/ci/junit.xml` (`.config/nextest.toml`) | test fn name `val_<n>_...` | Adapter adds `contract` and `test-file` (binary id -> `<crate>/tests/<stem>.rs` or source file) | ARC `cluster` job; local gate |
| Web unit (Vitest) | `vitest run --reporter=junit --outputFile=<dir>/web-unit.xml` | `web-unit.xml` | test name `VAL-<n> ...` | Adapter adds `contract`; normalises `classname` to `web/...` path | ARC; local gate |
| E2E (Playwright) | `PLAYWRIGHT_JUNIT_OUTPUT_FILE=<dir>/e2e.xml playwright test --reporter=junit` | `e2e.xml` | tag `@VAL-<n>` (keep `omitTags` off) | Adapter adds `contract`; normalises spec path to `web/e2e/...` | ARC `e2e` job; `mise run e2e` |
| Task tests (node:test) | `node --test --test-reporter=junit --test-reporter-destination=<dir>/tasks.xml mise-tasks/` | `tasks.xml` | test name `VAL-<n> ...` | Adapter adds `contract` and `test-file` | ARC; local gate |

- **Adapter:** `mise-tasks/ci/junit-contract` (phase 3). It reads every spec's planned
  `path::test` checks and adds `contract` and `test-file` testcase properties only to a testcase
  whose reported file and test name match that planned check exactly. It never invents results,
  changes statuses or matches on a VAL ID alone.
- **Contract step:** after all suites, the ARC job runs
  `uv run _bmad/custom/scripts/validate_story_contract.py ci --require-jj --junit "$RUNNER_TEMP/rust.xml" --junit "$RUNNER_TEMP/web-unit.xml" --junit "$RUNNER_TEMP/e2e.xml" --junit "$RUNNER_TEMP/tasks.xml"`.
  It records the run ID (`$GITHUB_RUN_ID`) and commit in the job summary.
- **jj in CI:** `actions/checkout` with `fetch-depth: 0`, then `jj git init --colocate` (jj from
  mise) so `--require-jj` can find the sealed approval changes. CI only; agents never run git.
- **Fork PRs** cannot reach the contract step (no ARC). The `ci-gate` job then fails, and a
  maintainer re-runs the change from a same-repo branch.
- **Proof (phase 3):** a temporary VAL-tagged test that fails must fail the contract step naming
  the VAL ID, then pass after repair; a report without the test must fail with "CI did not run
  it". Then remove the probe.
- **Command-only checks** cannot be verified from CI results. STORY-1.1 VAL-1 and VAL-7 are being
  changed by TEA (SD-3).

## CI design

| Workflow | Job | Runner | Events | Runs |
| --- | --- | --- | --- | --- |
| `ci.yml` | `fast` | `ubuntu-24.04` (hosted) | push, all PRs | `mise run check:fast`; gitleaks full history |
| `ci.yml` | `cluster` | ARC scale set | push; same-repo PRs | `mise run check` (all tiers) + contract step |
| `ci.yml` | `e2e` | ARC scale set | push; same-repo PRs | `skaffold run` to the CI namespace; `mise run e2e` |
| `ci.yml` | `ci-gate` | hosted | always | Fails unless `fast`, `cluster` and `e2e` all succeeded (skipped counts as failure) |
| `codeql.yml` | `analyze` | hosted | push, PRs, weekly | CodeQL for Rust, JS/TS and Actions |
| `build.yml` | `images` | ARC | push | Build images and chart; push by digest only on `main` |

All workflows set top-level `permissions: contents: read`. Only the `main` image push job gets
`packages: write`. Actions are pinned by 40-character SHA. The `main` ruleset requires `ci-gate`
and `analyze`.

## Project agent surface

| Capability | Path or reference | Status | Fresh-clone discovery check (phase 3) |
| --- | --- | --- | --- |
| Context file | `AGENTS.md` | deferred: Story 1.1 T11 | Pi loads it at session start |
| Project context | `project-context.md` | active | Loaded by BMAD agents |
| Pi extensions | `.pi/extensions/contract-guard.ts`, `.pi/extensions/readiness-enforce.ts` | active (guard); readiness rules deferred | Blocked write shows the reason |
| Readiness rules | `.pi/readiness.rules.json` | deferred: phase 3 | L2 rehearsal |
| Pi packages | `npm:pi-lens`, `npm:@upstash/context7-pi`, `npm:@gotgenes/pi-anthropic-auth` (in `.pi-recipe`) | active on this host; project declaration to verify | Fresh clone starts Pi with pi-lens |
| MCP | `.mcp.json`, `.pi/mcp.json`: `linear` | active | Linear tools listed |
| MCP | GitHub MCP, `actions` toolset, read-only | deferred: phase 3 (verify endpoint, headers and token use against primary docs) | Agent reads a failed job log |
| Skills | `.agents/skills/` (BMAD, TEA, steward) | active | Skills listed |
| TEA module | `bmad-tea`, `bmad-testarch-*` | active | - |
| Prompts, presets, themes | - | not-needed: no requirement | - |
| Local overrides | `mise.local.toml` (untracked: kube context, BuildKit endpoint, registry) | deferred: Story 1.1 / phase 3 | `.gitignore` covers it; `mise.local.toml.example` committed |

## Pillar coverage

| Pillar | Choice | Status |
| --- | --- | --- |
| Style and linting | rustfmt, clippy, ESLint, Prettier; no pre-commit (jj has no git hooks; Pi edit feedback instead) | deferred: 1.1 |
| Testing | nextest + `#[sqlx::test]`, Vitest, Playwright, node:test for tasks; coverage not adopted | deferred: 1.1; coverage deferred (R24) |
| Documentation | `AGENTS.md`, `README.md`, `SECURITY.md`, `CODEOWNERS`; `LICENSE` open | deferred: 1.1, phase 3, OI-1 |
| Dev environment | Native host + mise (unsandboxed); dev cluster; `mise.local.toml` | building |
| CI/CD | GitHub Actions: hosted + ARC tiers; ruleset on `main` | deferred: 1.1, phase 3 |
| Code health | Renovate; dead code via clippy `dead_code` (deny via `-D warnings`) and ESLint | deferred: phase 3 |
| Security | CodeQL, gitleaks, cargo-deny, npm audit signatures, secret scanning | deferred: phase 3, OI-5 |
| Architecture | `check/lob`, crate dependency rule, story guards | deferred: phase 3 and stories |
| Agent context | `AGENTS.md`, pi-lens, readiness extension, contract guard, MCP | building |

## Tooling exploration log

| Tool | Gap | Decision | Reason | Revisit |
| --- | --- | --- | --- | --- |
| Dagger | Local/CI parity | rejected | mise tasks already give parity; Dagger needs an engine and a second task layer | If tasks diverge between local and CI |
| nektos `act` 0.2.97 | Run workflows locally | accepted, pinned, unused | Cheap insurance for workflow debugging | When a workflow fails only in CI twice |
| devcontainer | Agent boundary | rejected by Daniel | Native host chosen; residual risk recorded | D2 expiry |
| kind on Podman | Local cluster | rejected | 2 GiB machine; Daniel provides a dev cluster | - |
| BuildKit (rootless, mTLS) vs Buildah vs kaniko | In-cluster image builds | BuildKit | Native buildx path, registry cache, `--output type=local` for codegen; Buildah needs custom scripts and does not cover codegen | If Skaffold buildx support regresses |
| ARC runners vs hosted + kubeconfig | CI access to cluster | ARC | API server stays private; no kubeconfig in GitHub | - |
| CodeQL vs opengrep | SAST in CI | CodeQL (needs public repo) | User choice; free on public repos | OI-5 |
| gitleaks | Secret detection | accepted | Free, works without git locally (`dir` mode) | - |
| cargo-deny | Rust advisories, licences, sources | accepted | Standard, offline-capable after DB fetch | - |
| `npm audit signatures` | npm provenance | accepted | Built into npm | - |
| Renovate vs Dependabot | Stale exact pins | Renovate | Handles mise, Cargo `=`, npm, image digests, action SHAs | - |
| GitHub MCP vs `gh` CLI | CI feedback for agent | GitHub MCP, `actions`, read-only | Structured results | If the server or toolset changes |
| Coverage tools | Test depth | deferred | No evidence of need yet | R24 trigger |

## Potential enforcement considerations

- Machine-readable decision registry: **rejected**. One maintainer and one document; the
  traceability matrix is enough. Revisit if the matrix and checks drift twice.
- Repository-host controls: **adopted** (phase 3): ruleset on `main` with required `ci-gate` and
  CodeQL, fork-PR approval, ARC runner group limited to this repository, `CODEOWNERS`.

## Residual manual assurance plan

Owner for all: Test Architect, at Test Review or Code Review of each story.

| ID | Check | Evidence | Trigger |
| --- | --- | --- | --- |
| M1 | Wiring only in `main.rs`; at most 3 layers; traits only at third use or real second implementation | Review note naming files checked | Every Rust story |
| M2 | No credentials or full SBOMs in logs | Review note; log sample from the dev deployment | Every story touching auth, connectors or logging, until R18 test exists |
| M3 | Agent image has no scanners; control-plane image contents | Image listing record (VAL-8) | Story 1.1; any Dockerfile change until Story 10.1 |
| M4 | ARC runner group, namespace RBAC and fork approval settings | Settings screenshots or `gh api` output | Phase 3; any ARC or repo-settings change |
| M5 | `skaffold dev` was running and healthy during the story (PROC3) | Redeploy log excerpt in Implementation Notes | Every story after 1.1 |
| M6 | Locked enums and glossary used, no synonyms | Review note | Every API or UI story until R21 check exists |
| M7 | `AGENTS.md` and `README.md` are correct and commands work | VAL-13 record | Story 1.1; docs changes |

Promotion rule: when a manual check finds the same defect twice, Vera proposes the smallest
deterministic check for it at the next RV.

## Steward Decisions

### SD-1: Rust `#[ignore]` is a skip marker (2026-11-06)

- Trigger and evidence: STORY-1.1 ATDD (R2). `lock_digest` and skip detection ignored Rust
  `#[ignore]`, so removing it changed a lock and an ignored test passed delivery checks.
- Concern: agents can silently skip unlocked Rust acceptance tests.
- Options: fix the validator and raise upstream; rely on CI JUnit only; raise upstream only.
- Decision (Daniel): fix the validator and raise upstream.
- What changed: `_bmad/custom/scripts/validate_story_contract.py`, new `RustIgnoreTests`,
  `story-contract.md` limits text, regenerated `instructions/implementation.md`. jj change `orzznppm`.
- Re-proof: new tests failed (5 subtest failures), then passed; full suite `OK (skipped=28)`;
  STORY-1.1 lock digests unchanged; a probe `#[ignore]` on VAL-2/VAL-3 is detected and keeps the lock.
- Gives up: nothing (adds coverage).
- Revisit: when `bmad-customisations` syncs; confirm the fix is upstream or reapply it.

### SD-2: AR design before STORY-1.1 approval (2026-11-06)

- Trigger and evidence: ATDD blocker B1. ATDD's CI NAMING CHECK needs the Contract CI Wiring
  convention before approval, but PROC1 runs AR after Story 1.1.
- Options: AR design now and build after 1.1; a narrow exception for 1.1; pull JUnit wiring into 1.1.
- Decision (Daniel): AR phases 0-2 now (this document, status `building`); STORY-1.1 Build runs as
  user-authorised readiness work; AR phase 3 builds and proves the wiring; Code Review of 1.1 uses
  real CI results.
- What changed: this document. No check was relaxed.
- Expiry: AR must reach `ready` before Story 1.2 Build. Build and Code Review readiness gates
  enforce this.

### SD-3: STORY-1.1 VAL-1 and VAL-7 (2026-11-06)

- Trigger: `steward_scan` concern `ci-unverifiable` (command-only planned checks).
- Decision (Daniel): VAL-7 becomes a node:test test (`mise-tasks/gen/api.test.mjs`); VAL-1 becomes
  a manual demonstration. Routed to TEA (ATDD Edit). Pending.

### SD-4: Classic GitHub token in agent sessions (2026-11-06)

- Decision (Daniel): keep it; accepted residual risk (D2).
- Gives up: least privilege for the agent session.
- Expiry: 2027-02-06. At expiry, replace it with a fine-grained repo token or renew this decision.

## Open items

| ID | Item | Owner | Needed before |
| --- | --- | --- | --- |
| OI-1 | Licence choice (no `LICENSE` means all rights reserved) | Daniel | Public announcement or outside contributions |
| OI-2 | Dev registry: Harbor or Artifact Keeper; repository paths | Daniel | Story 1.1 T9 |
| OI-3 | Kube context names, CI namespace, BuildKit endpoint and mTLS client files, AGE Pod location | Daniel | Story 1.1 T3/T4/T9 |
| OI-4 | Correct Course for PROC3, ARCH34, Stories 1.2 and 2.12 (kind/Podman to cluster, Helm 4); Build re-plan of STORY-1.1; ATDD Edit (VAL-1, VAL-7, VAL-9, VAL-11) | PM, Build, TEA | STORY-1.1 approval |
| OI-5 | Make the repository public | Daniel | After phase 3 proves the runner split and a clean gitleaks full-history scan |

## Phase 3 build list

1. Fast-tier checks: `check/lob`, `check/workflows`, `check/secrets`, `deny.toml`, workspace lints, `.pi/readiness.rules.json`.
2. JUnit adapter `mise-tasks/ci/junit-contract` and `check/contracts`.
3. ARC scale set, runner group, CI namespace RBAC; `ci.yml` tiers and `ci-gate`; `codeql.yml`.
4. GitHub MCP (`actions`, read-only) in `.mcp.json` and `.pi/mcp.json`.
5. Renovate config; `SECURITY.md`; `CODEOWNERS`; `mise.local.toml.example`.
6. Rehearse L2, L4, L5, L9, L10, L13 and L16; prove the contract step; fresh-clone and Pi discovery checks.
7. Run the scorer (`pnpm dlx @danielboothcloud/agent-readiness . --format json`); fix real gaps; add it to CI.
8. Set Status `ready` only when the threshold and all applicable critical loops are proven.
