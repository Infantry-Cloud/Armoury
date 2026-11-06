---
stepsCompleted:
  - step-01-preflight-and-context
  - step-02-generation-mode
  - step-03-test-strategy
  - step-04-generate-tests
  - step-04c-aggregate
  - step-05-validate-and-complete
lastStep: step-05-validate-and-complete
lastSaved: '2026-11-06'
storyId: '1.1'
storyKey: 1-1-monorepo-scaffold-with-an-aggregate-local-gate-and-ci
storyFile: _bmad-output/implementation-artifacts/spec-1-1-monorepo-scaffold-with-an-aggregate-local-gate-and-ci.md
atddChecklistPath: _bmad-output/test-artifacts/atdd-checklist-1-1-monorepo-scaffold-with-an-aggregate-local-gate-and-ci.md
contract: STORY-1.1
contractRevision: 1
contractStatus: draft
detectedStack: fullstack (target; no manifests exist yet)
generationMode: AI generation (no app exists to record)
executionMode: sequential (four small scaffolds; no worker split needed)
generatedTestFiles:
  - agent-proto/tests/val_2_roundtrip.rs
  - control-plane/tests/val_3_age.rs
  - mise-tasks/check/pins.test.mjs
  - web/e2e/smoke.spec.ts
  - web/src/routes/val-4.test.ts
inputDocuments:
  - _bmad-output/implementation-artifacts/spec-1-1-monorepo-scaffold-with-an-aggregate-local-gate-and-ci.md
  - _bmad-output/implementation-artifacts/epic-1-context.md
  - _bmad-output/planning-artifacts/architecture.md
  - _bmad/custom/story-contract.md
  - _bmad/custom/jj-vcs.md
  - _bmad/custom/linear-workflow.md
  - _bmad/custom/scripts/validate_story_contract.py
  - .agents/skills/bmad-testarch-atdd/resources/knowledge/test-quality.md
acceptanceCriteria:
  - { id: AC-1, idSource: supplied, text: 'Workspace, crates and SvelteKit web app build after mise install + mise run check' }
  - { id: AC-2, idSource: supplied, text: 'Every tool, crate, npm dependency, image and action is pinned; lockfiles committed; nothing floats' }
  - { id: AC-3, idSource: supplied, text: 'mise run check runs every listed step and exits 0 on a clean scaffold' }
  - { id: AC-4, idSource: supplied, text: 'Each of nine injected defects makes mise run check exit non-zero and name the step' }
  - { id: AC-5, idSource: supplied, text: 'Each crate, the web app and the chart has a real passing test or lint target' }
  - { id: AC-6, idSource: supplied, text: 'gen:api generates Rust and TS types without local Java; a second run has no diff' }
  - { id: AC-7, idSource: supplied, text: 'Digest-pinned multi-stage images with cargo-chef; agent image has no scanners' }
  - { id: AC-8, idSource: supplied, text: 'skaffold dev -p kind deploys repo:tag@digest, serves localhost:8080, redeploys with cached deps' }
  - { id: AC-9, idSource: supplied, text: 'mise run e2e Playwright smoke passes against the deployment and fails without one' }
  - { id: AC-10, idSource: supplied, text: 'ci.yml runs check and e2e with SHA-pinned mise-action and fails like local' }
  - { id: AC-11, idSource: supplied, text: 'build.yml builds images and chart; pushes to GHCR by digest only on main' }
  - { id: AC-12, idSource: supplied, text: 'AGENTS.md states ARCH25, layout and PROC3; README documents the commands' }
---

# ATDD Checklist - Epic 1, Story 1.1: Monorepo scaffold with an aggregate local gate and CI

**Contract:** STORY-1.1, Revision 1, Risk medium, Status **draft**.
**Story file:** `_bmad-output/implementation-artifacts/spec-1-1-monorepo-scaffold-with-an-aggregate-local-gate-and-ci.md`
**ATDD change:** `qnkkvwmm` — `test(story-1.1): add acceptance tests`.

The story contract is the requirements oracle. This checklist supports it and does not compete with it.

## Preflight

| Item | Result |
| --- | --- |
| `validate --phase draft` before ATDD | VALID |
| `validate --phase draft` after the approved edits | VALID |
| Build status | `ready-for-dev` (Build CHECKPOINT 1) |
| Test framework configured | **No, by design.** This story creates every framework (nextest, Vitest, Playwright, node:test). This is a recorded deviation, not a halt. |
| Linear | No agreed ATDD obligation exists for story 1.1 in `_bmad/linear/projects/armoury.json`. No Linear write was made. |
| Playwright-utils | Not applicable: `@seontechnologies/playwright-utils` is not in any `package.json`. Adding it for one smoke test is not warranted; reconsider in Story 1.7. |
| Knowledge fragments | Selected by the step-01 rule (core, fullstack, traditional, backend). `test-quality.md` was read and applied (documented skips, assertions that can fail, behavioural names). The others cover data, fixtures, network, selectors and burn-in, which these scaffolds do not use. |

## Draft-contract edits (approved by Daniel in this session, 2026-11-06)

| Edit | Change | Reason |
| --- | --- | --- |
| E1 | VAL-2 moved from `agent-proto/src/lib.rs::tests::…` to `agent-proto/tests/val_2_roundtrip.rs::val_2_generated_message_roundtrip`; message `armoury.agent.v1.Heartbeat { string agent_id = 1; }` exposed as `agent_proto::v1` | A lock covers the whole file, so a lock on `lib.rs` would freeze production code. |
| E2 | VAL-4 name changed to `VAL-4 root layout disables SSR and uses the static adapter` | The old name said "prerenders", which the oracle does not check. |
| E3 | VAL-5 changed into a fixture test `mise-tasks/check/pins.test.mjs::VAL-5 pins check rejects floating references`, with lockfile and exact-pin cases | The old command ran only on a clean tree, so its negative oracle never ran. |
| E4 | VAL-12 evidence adds least-privilege `permissions:` and no `pull_request_target` | `build.yml` holds a registry write token. |
| OQ-4 | Recorded the user decision: exact pins in `Cargo.toml` (`=x.y.z`), `web/package.json` and `mise.toml`, plus committed lockfiles | AC-2 "floating version" was ambiguous for manifests. |

## Red-phase scaffolds created

| File | Test | VAL / AC | Inactive state | Activated by |
| --- | --- | --- | --- | --- |
| `agent-proto/tests/val_2_roundtrip.rs` | `val_2_generated_message_roundtrip` | VAL-2 / AC-1, AC-5 | No crate exists, so it does not compile into any target (no `#[ignore]`, see R2) | Task T2 adds `agent-proto` to the workspace |
| `control-plane/tests/val_3_age.rs` | `val_3_age_extension_is_available` | VAL-3 / AC-3, AC-5 | No crate exists (no `#[ignore]`, see R2) | Task T3 adds `control-plane` to the workspace |
| `web/src/routes/val-4.test.ts` | `VAL-4 root layout disables SSR and uses the static adapter` | VAL-4 / AC-1, AC-5 | `test.skip` | Task T5 removes `.skip` |
| `mise-tasks/check/pins.test.mjs` | `VAL-5 pins check rejects floating references` | VAL-5 / AC-2 | `test.skip` | Task T7 removes `.skip` |
| `web/e2e/smoke.spec.ts` | `loads the web app @VAL-10` | VAL-10 / AC-9 | `test.skip` | Task T9 removes `.skip` |

The test name of each scaffold carries its VAL ID (`val_2_…`, `VAL-4 …`, `@VAL-10`), as story-contract.md "CI results" requires.

### Red-phase verification (actual runs)

- `node --test mise-tasks/check/pins.test.mjs` → `skipped 1, fail 0`.
- The same file with `.skip` removed (temporary copy, then deleted) → `pass 0, fail 13`, because `mise-tasks/check/pins` does not exist. No fixture directories were left in `$TMPDIR`.
- Rust and web scaffolds cannot run yet: no toolchain, crate or `package.json` exists. They are red by construction (they do not compile, or their imports fail) until their task builds the target.
- Lock behaviour (`lock_digest` from the validator): for all five files, removing `test.skip(` gives the same digest. The validator detects the skip marker in the three TS/JS files. It does not detect a Rust marker, see R2.
- `validate_story_contract.py lock` preview lists exactly these five files. The preview was not recorded, because approval has not happened.

### Oracle notes per scaffold

- **VAL-2:** encodes a `Heartbeat` with `..Default::default()`, so additive proto fields in Epic 3 do not break it. A rename of `Heartbeat` or `agent_id` needs Correct Course on STORY-1.1.
- **VAL-3:** `#[sqlx::test(migrations = false)]` keeps this check independent of the Story 1.2 migrations. It runs `CREATE EXTENSION IF NOT EXISTS age` and then asserts `extversion = '1.8.0'`.
- **VAL-4:** uses dynamic imports so that the skipped file loads before `+layout.ts` and `svelte.config.js` exist. It asserts `ssr === false` first, then the adapter name `@sveltejs/adapter-static`.
- **VAL-5:** runs `mise-tasks/check/pins <root>` as a process, so the checker can be in any language. The expected interface is: exit 0 when clean, and exit 1 with the offending file path in stdout or stderr. There are ten defect fixtures, one clean fixture and the real repository.
- **VAL-10:** the first assertion is HTTP 200 at `/`, then the page title matches `/Armoury/` (the product name). There is no `webServer`, so an unreachable deployment fails the test.

## AC → VAL → artifact map

| AC | VAL | Method | Artifact or procedure | Owner |
| --- | --- | --- | --- | --- |
| AC-1 | VAL-1, VAL-2, VAL-4 | mechanical | fresh-copy `mise run check` log; `agent-proto/tests/val_2_roundtrip.rs`; `web/src/routes/val-4.test.ts` | Dev |
| AC-2 | VAL-5 | mechanical | `mise-tasks/check/pins.test.mjs` | Dev |
| AC-3 | VAL-1, VAL-3 | mechanical | fresh-copy log; `control-plane/tests/val_3_age.rs` | Dev |
| AC-4 | VAL-6 | manual | nine-defect observation record | Dev |
| AC-5 | VAL-1, VAL-2, VAL-3, VAL-4 | mechanical | as above | Dev |
| AC-6 | VAL-7 | mechanical (command) | `mise run gen:api` twice + `jj diff --stat` | Dev |
| AC-7 | VAL-8 | manual | image inspection record | Test Architect |
| AC-8 | VAL-9 | manual | Skaffold dev-loop observation record | Test Architect |
| AC-9 | VAL-10 | mechanical | `web/e2e/smoke.spec.ts` + saved negative run | Dev |
| AC-10 | VAL-11 | manual | two CI run URLs with commit IDs | Test Architect |
| AC-11 | VAL-12 | manual | build run URLs, digests, permissions read | Test Architect |
| AC-12 | VAL-13 | manual | documentation inspection, fresh-checkout walk-through | Test Architect |

Evidence location for all records: `_bmad-output/implementation-artifacts/evidence/1-1/`.

### Manual obligations (verified: procedure, oracle, evidence, owner, reason)

VAL-6, VAL-8, VAL-9, VAL-11, VAL-12 and VAL-13 each have an exact procedure, an observable expected result, a saved-record evidence type, an owner and a manual reason. VAL-6 belongs to Dev, but Code Review must repeat at least one defect independently.

## Test Architect review: risks and blockers

### Approval blockers

- **B1. CI cannot verify the mechanical checks (sent to Vera by the user).** The scope sends JUnit contract wiring, `validate_story_contract.py ci` and `docs/agent-readiness.md` to Agent Readiness (INF-12). The team policy "CI NAMING CHECK" calls this an approval blocker. VAL-1 and VAL-7 are commands only, so no JUnit result can ever match them without a converter. The circular dependency is: AR needs this scaffold, and the policy wants AR wiring before approval. The user chose to discuss it with the Guardrail Steward (Vera) before approval.

### Residual risks for Dev (no contract change)

- **R1.** `KIND_EXPERIMENTAL_PROVIDER=podman` in `mise.toml` `[env]` also applies in CI, and mise `[env]` overrides workflow `env:`. Use a mise environment profile (for example `MISE_ENV=ci`) or a template condition, so that CI uses Docker. VAL-11 shows the effect.
- **R2.** The validator neither strips nor detects Rust `#[ignore]`. Rust scaffolds therefore have no marker. Adding `#[ignore]` later changes the lock digest, so the lock still blocks it. The delivery skip check does not see `#[ignore]` on unlocked Rust tests. **Raise with Vera** as a validator gap.
- **R3.** With Podman only, a `docker` CLI may not exist on the workstation (`docker run` for openapi-generator, the Skaffold docker builder). Document a `docker` shim or socket in `README.md`, or detect `podman` in the tasks.
- **R4.** The drift check inside `mise run check` must not use jj or git. CI has a Git checkout and no jj workspace, and VAL-1 runs in a copy with no VCS. Generate into a temporary directory and `diff -r` it against the committed output.
- **R5.** `mise-tasks/check` cannot be both a file and a directory. Use `mise-tasks/check/_default` for the aggregate gate and `mise-tasks/check/pins` for the checker. Checked with mise 2026.11.0: a non-executable `pins.test.mjs` is not listed as a task.
- **R6.** Exact pins (OQ-4): `sv create` and `npm install` write `^` ranges. Add `save-exact=true` to `web/.npmrc` and rewrite the generated ranges. Use `cargo … --locked` and `npm ci` in the gate.
- **R7.** Before the `ci` step goes live, Agent Readiness must give testcases a `contract` property and a full test identity: nextest JUnit, Vitest `--reporter=junit`, Playwright `PLAYWRIGHT_JUNIT_OUTPUT_FILE` and node `--test-reporter=junit`. This depends on the B1 decision.

## Implementation checklist (per task)

- [ ] T1: pin the toolchain exactly (OQ-4). VAL-5 activates in T7.
- [ ] T2: workspace + `proto/agent/v1/agent.proto` (`package armoury.agent.v1; message Heartbeat { string agent_id = 1; }`), `agent_proto::v1` module. Then run `cargo nextest run -p agent-proto` and confirm that VAL-2 goes from red to green.
- [ ] T3: `control-plane` crate; `mise run check` starts the digest-pinned AGE container and sets `DATABASE_URL`. Run VAL-3 from red to green.
- [ ] T4: `gen:api` + VCS-free drift check (R4). VAL-7.
- [ ] T5: web app. Remove `.skip` from VAL-4, show red, then green.
- [ ] T6: chart + `helm lint`.
- [ ] T7: `check/_default` + `check/pins` (R5). Remove `.skip` from VAL-5, show red (13 failures), then green. Run the VAL-6 demonstration.
- [ ] T8: Dockerfiles. VAL-8 is for the reviewer.
- [ ] T9: Skaffold + `playwright.config.ts` (`baseURL` `http://localhost:8080`, no `webServer`). Remove `.skip` from VAL-10. Save the run without a deployment as negative evidence.
- [ ] T10: workflows with least-privilege `permissions:` (E4) and the R1 environment override.
- [ ] T11: `AGENTS.md`, `README.md` (R3 Podman notes).

After approval, the only allowed edit to a locked scaffold is removing its skip marker.

## Running the tests

```sh
node --test mise-tasks/check/pins.test.mjs        # VAL-5
cargo nextest run -p agent-proto -p control-plane  # VAL-2, VAL-3 (needs DATABASE_URL)
npm --prefix web run test -- --run src/routes/val-4.test.ts  # VAL-4
mise run e2e                                       # VAL-10 against skaffold dev -p kind
mise run check                                     # aggregate gate
```

## Status and next step

The contract stays **draft**. Approval needs:
1. a decision on B1 with Vera, and
2. Daniel's explicit product approval of intent, scope, ACs, risk, oracles and the residual manual checks.

After that, the separate JJ APPROVAL change records the approvers, the digest and the `### Locked Tests` table.
