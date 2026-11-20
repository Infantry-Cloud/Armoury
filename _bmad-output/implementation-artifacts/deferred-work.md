# Deferred work

- source_spec: `_bmad-output/implementation-artifacts/spec-1-1-monorepo-scaffold-with-an-aggregate-local-gate-and-ci.md`
  summary: CodeQL does not scan script blocks in `.svelte` components, so UI surfaces bypass the SAST gate.
  evidence: An injected `eval(location.hash)` in a `.svelte` file produced no result (Decision 12); a compensating ESLint rule or a CodeQL workaround is needed before UI stories (1.5+).
- source_spec: `_bmad-output/implementation-artifacts/spec-1-1-monorepo-scaffold-with-an-aggregate-local-gate-and-ci.md`
  summary: `ci:e2e` deploys the PR preview from the branch tip, not the checked-out `GITHUB_SHA`, so a push during the run tests other code.
  evidence: `mise-tasks/ci/e2e` passes `--branch "$GITHUB_HEAD_REF"`; AC-13 specifies the branch, so a SHA-pinned deploy needs a contract change.
- source_spec: `_bmad-output/implementation-artifacts/spec-1-1-monorepo-scaffold-with-an-aggregate-local-gate-and-ci.md`
  summary: The generated rust-axum server crate (`armoury-httpapi`) is outside the workspace lints and calls `.unwrap()` on the request path.
  evidence: `control-plane/src/httpapi/server/generated/src/server/mod.rs:71,98,108`; generated code cannot be edited, so R2 needs a recorded generated-code exemption in AGENTS.md or a different generator template.
- source_spec: `_bmad-output/implementation-artifacts/spec-1-1-monorepo-scaffold-with-an-aggregate-local-gate-and-ci.md`
  summary: `check/codeql` may pass when a language database is missing, because it skips folders without `codeql-database.yml`.
  evidence: Unverified (maybe-false, medium if true); settle it by forcing one extractor to fail under `--db-cluster` and checking whether the step still prints "no results".
