# Agent Readiness Checklist: armoury

Maturity level: 1 (Foundational)
Next level: 2 (Guided) — 3/10 criteria passing, 7 remaining
Harnesses: pi, Claude Code (detected)

This checklist is meant to live in the repo. Every area and item keeps its guidance even once it's ticked: why it matters, what good looks like, questions to work through, and example starting points. The examples are common options, not the answer for every repo; use the questions to decide what fits this codebase, and look around before building your own (see "Find what fits this repo" at the end). A ticked box means the basics are detected, not that the question is settled: revisit when the stack, team or tools change, and regenerate with `agent-readiness --checklist` to refresh the status.

## Style & Linting (0/5, 0%)

**Why this matters:** Agents copy what they see and fix what they're told. Linters, formatters and type checkers turn the team's taste into fast, mechanical feedback, so style stops being a review topic and mistakes surface before anyone reads the diff.

**Questions for this area:**
- Which review comments are really about style or types, and could a tool make them unnecessary?
- How quickly does the agent hear about a lint or type error: the same turn, at commit, or in CI?

- [ ] **EditorConfig present** (L1, `editorconfig`)
  - Status: failing — No .editorconfig found.
  - Why it matters: EditorConfig ensures agents produce files with correct whitespace and encoding regardless of tooling
  - Goal: Create an .editorconfig file to standardize indentation, line endings, and charset across editors (effort: low, impact: low)
  - Ask yourself:
    - Do editors and agents on this team agree on indentation, line endings and final newlines, or do diffs show churn?
- [ ] **Linter configured** (L2, `linter`)
  - Status: failing — No linter configuration found.
  - Why it matters: Linters give agents instant feedback on style issues, preventing CI failures and reducing review churn
  - Goal: Add a linter like ESLint or Biome to enforce code style and catch common mistakes (effort: medium, impact: high)
  - Ask yourself:
    - Which mistakes keep coming back in review that a rule could catch automatically?
    - Is there a linter your language community treats as standard, and does one tool cover both linting and formatting here?
- [ ] **Formatter configured** (L2, `formatter`)
  - Status: failing — No formatter configuration found.
  - Why it matters: Auto-formatting removes style debates and lets agents produce consistently formatted code without guesswork
  - Goal: Configure an auto-formatter such as Prettier or Biome so code style is applied automatically (effort: medium, impact: high)
  - Ask yourself:
    - How much review time goes on whitespace, quotes and import order today?
    - Does the formatter's default style match what's already in the codebase, or would adopting it rewrite every file?
- [ ] **Type checker configured** (L3, `type-checker`)
  - Status: failing — No type checker with strict mode found.
  - Why it matters: Strict types help agents catch errors at compile time instead of at runtime, dramatically improving code reliability
  - Goal: Enable strict type checking (e.g. strict mode in tsconfig.json, mypy, or pyright) (effort: medium, impact: medium)
  - Ask yourself:
    - Where do runtime type errors actually happen in this codebase — and would stricter settings have caught them?
- [ ] **Pre-commit hooks configured** (L3, `pre-commit-hooks`)
  - Status: failing — No pre-commit hooks found.
  - Why it matters: Pre-commit hooks provide a fast feedback loop so agents discover issues before pushing code
  - Goal: Set up pre-commit hooks with Husky, Lefthook, or pre-commit to run checks before every commit (effort: medium, impact: medium)
  - Ask yourself:
    - Which checks are fast enough to run on every commit, and which belong in CI only?
- [-] **Naming conventions (AI)** (L5, `naming-conventions`)
  - Status: skipped (Requires --ai flag)
  - Why it matters: Consistent naming lets agents predict correct patterns when writing new code, reducing review friction
  - Goal: Establish and document consistent naming conventions for files, functions, and variables (effort: medium)
  - Ask yourself:
    - Could someone guess a new file's name and location from the existing ones?
    - Where do naming styles disagree today, and which one should win?

## Testing (1/5, 20%)

**Why this matters:** Tests are how an agent learns whether its change worked. Without a fast, trustworthy suite it can only guess, and every guess becomes something a human has to verify by hand.

**Questions for this area:**
- If an agent changed the riskiest part of this codebase, what would tell you it broke something?
- How long does the agent wait to find out, and could the slow parts run less often?

- [ ] **Test framework configured** (L2, `test-framework`)
  - Status: failing — No test framework configuration found.
  - Why it matters: A configured test framework lets agents write and run tests to verify their changes automatically
  - Goal: Configure a test framework such as Jest, Vitest, pytest, or Go testing with a config file (effort: medium, impact: high)
  - Ask yourself:
    - How does someone know a change works today? What would make that check repeatable?
    - Is there a test runner the stack treats as standard that fits how this code is structured?
- [x] **Test files exist** (L2, `test-files-exist`)
  - Status: passing — Found 15 test file(s)
  - Why it matters: Existing tests give agents examples to follow and a safety net to validate new code against
  - Goal: Add test files alongside source code following standard naming conventions (*.test.*, *.spec.*, etc.) (effort: medium)
  - Ask yourself:
    - Which parts of the code would you be most nervous to let an agent change without tests?
    - Are there existing tests an agent could copy the pattern from?
- [ ] **Test script defined** (L2, `test-script`)
  - Status: failing — No test script or target found.
  - Why it matters: A standard test command allows agents to verify changes without guessing how to run the test suite
  - Goal: Define a 'test' script in package.json or a test target in a Makefile so tests can be run with a single command (effort: medium, impact: high)
  - Ask yourself:
    - Could a new contributor (or agent) run one test file in one command? Is that command written down?
- [ ] **Coverage configured** (L4, `coverage-config`)
  - Status: failing — No coverage configuration found.
  - Why it matters: Coverage metrics help agents understand which parts of the codebase are well-tested and which need attention
  - Goal: Set up code coverage reporting in your test framework configuration (effort: high, impact: low)
  - Ask yourself:
    - Do you want coverage as a gate, or as a map of which areas are risky to change?
    - Which untested areas get changed most often?
- [ ] **E2E / integration tests** (L4, `e2e-tests`)
  - Status: failing — No E2E or integration test setup found.
  - Why it matters: E2E tests give agents confidence that the whole application works correctly after changes, not just individual units
  - Goal: Add end-to-end or integration tests using Playwright, Cypress, or a similar framework (effort: high, impact: low)
  - Ask yourself:
    - Which user journeys would hurt most if an agent broke them silently? Start there.
- [-] **Test quality (AI)** (L5, `test-quality`)
  - Status: skipped (Requires --ai flag)
  - Why it matters: High-quality tests give agents confidence that their changes work correctly and don't break existing behavior
  - Goal: Improve test quality: add descriptive names, cover edge cases, and test behavior rather than implementation (effort: high)
  - Ask yourself:
    - Would the tests fail if the behaviour broke, or only if the implementation changed?
    - Do test names explain the behaviour well enough for an agent to tell what it's protecting?

## Documentation (0/5, 0%)

**Why this matters:** Docs carry the context code can't: why things are the way they are, how to work here, who owns what. Agents start every session with no memory, so anything that isn't written down gets rediscovered or guessed.

**Questions for this area:**
- What would a capable newcomer get wrong in their first week here?
- Which docs are out of date, and how would anyone notice?

- [ ] **README with substance** (L1, `readme`)
  - Status: failing — No README.md found.
  - Why it matters: A good README helps agents understand the project context, conventions, and how to get started quickly
  - Goal: Create a comprehensive README.md with project overview, setup instructions, and usage examples (effort: low, impact: low)
  - Ask yourself:
    - Could someone go from clone to a working change using only the README?
    - What does a newcomer (or agent) need first: purpose, setup, or how to run it?
- [ ] **Contributing guide** (L2, `contributing`)
  - Status: failing — No contributing guide found.
  - Why it matters: Contributing guidelines teach agents the team's workflow so their PRs match expectations from the start
  - Goal: Add a CONTRIBUTING.md with development workflow, coding standards, and PR guidelines (effort: low, impact: high)
  - Ask yourself:
    - What does a change need before it's mergeable here (tests, changelog, commit style, review)? Is that written down?
    - Which workflow mistakes keep coming up in pull requests?
- [ ] **API documentation** (L3, `api-docs`)
  - Status: failing — No API documentation found.
  - Why it matters: API docs let agents understand available endpoints, data shapes, and contracts without reading every source file
  - Goal: Add API documentation using OpenAPI/Swagger specs, JSDoc, TypeDoc, or a dedicated docs folder (effort: medium, impact: medium)
  - Ask yourself:
    - Which interfaces do other code, teams or agents depend on, and where is their contract described?
    - Would generated docs from the code be enough, or is the contract the source of truth?
- [ ] **CODEOWNERS defined** (L3, `codeowners`)
  - Status: failing — No CODEOWNERS file found.
  - Why it matters: CODEOWNERS helps agents understand who to tag for reviews and which areas have strict oversight
  - Goal: Create a CODEOWNERS file to define ownership for different parts of the codebase (effort: low, impact: medium)
  - Ask yourself:
    - Which areas need a specific reviewer, and how would an agent (or newcomer) find out who?
- [ ] **Architecture documentation** (L4, `architecture-docs`)
  - Status: failing — No architecture documentation found.
  - Why it matters: Architecture docs help agents make design choices consistent with the existing system instead of guessing
  - Goal: Create architecture documentation (ARCHITECTURE.md or docs/adr/) describing system design and decisions (effort: high, impact: low)
  - Ask yourself:
    - Which design decisions would someone reverse without knowing why they were made?
    - Where do the main components meet, and is that boundary written down anywhere?
- [-] **README quality (AI)** (L5, `readme-quality`)
  - Status: skipped (Requires --ai flag)
  - Why it matters: A high-quality README gives agents rich context about the project beyond just file presence
  - Goal: Improve your README content: add clear sections for installation, usage, architecture, and contributing (effort: high)
  - Ask yourself:
    - Which questions about this project keep coming up that the README doesn't answer?
- [-] **Documentation agent-friendliness (AI)** (L5, `docs-agent-friendliness`)
  - Status: skipped (Requires --ai flag)
  - Why it matters: Agent-friendly docs help autonomous coding agents make correct changes without constant human guidance
  - Goal: Improve documentation to be more AI-agent-friendly: explain project structure, coding conventions, and testing patterns (effort: high)
  - Ask yourself:
    - If an agent read only the docs, which wrong assumption would it most likely make?
    - Are the commands and paths in the docs still correct?

## Developer Environment (1/5, 20%)

**Why this matters:** An agent can only verify its work in an environment that installs and runs reliably. Every 'works on my machine' gap becomes a failed check the agent can't explain.

**Questions for this area:**
- How long from a fresh clone to green tests, and which steps rely on someone remembering them?
- What does this project need beyond the code (services, secrets, tool versions), and is that written down or automated?

- [ ] **Lock file present** (L1, `lock-file`)
  - Status: failing — No dependency lock file found.
  - Why it matters: Lock files ensure agents install the exact same dependency versions, preventing 'works on my machine' issues
  - Goal: Commit a dependency lock file (package-lock.json, pnpm-lock.yaml, yarn.lock, poetry.lock, etc.) (effort: low, impact: low)
  - Ask yourself:
    - Would a fresh install today give the same dependency versions as yesterday's CI run?
- [ ] **Environment variables documented** (L2, `env-documentation`)
  - Status: failing — No environment variable documentation found.
  - Why it matters: Environment variable documentation lets agents understand required configuration without accessing secrets
  - Goal: Create a .env.example or .env.template documenting all required environment variables (effort: low, impact: high)
  - Ask yourself:
    - Which environment variables must be set for the app or tests to run, and where would someone find them?
    - Which ones are secrets that should never appear in a committed file?
- [ ] **Setup script or dev command** (L2, `setup-script`)
  - Status: failing — No setup script or dev command found.
  - Why it matters: A one-command setup lets agents bootstrap the project quickly and correctly every time
  - Goal: Add a setup script (Makefile, mise task, scripts/setup.sh, or npm run setup) to automate development environment setup (effort: medium, impact: high)
  - Ask yourself:
    - How long does a fresh clone take to get to green tests, and which steps are tribal knowledge?
- [x] **Runtime version pinned** (L2, `version-pinned`)
  - Status: passing — Version pinning found: mise.toml
  - Why it matters: Pinned runtime versions prevent agents from hitting version incompatibilities during execution
  - Goal: Pin the runtime version with .nvmrc, .node-version, .python-version, .tool-versions, mise.toml, or .mise.toml (effort: low)
  - Ask yourself:
    - Which runtime and tool versions does this repo actually depend on, and what breaks on the wrong one?
- [ ] **Containerization** (L3, `containerization`)
  - Status: failing — No container configuration found.
  - Why it matters: Containerization gives agents a fully reproducible environment, eliminating setup discrepancies
  - Goal: Add a Dockerfile, docker-compose.yml, or .devcontainer configuration for reproducible environments (effort: high, impact: medium)
  - Ask yourself:
    - What does running this project need beyond the language runtime (databases, queues, system libraries)?
    - Is a container the simplest way to make that reproducible here, or would a toolchain manager be enough?

## CI/CD (0/6, 0%)

**Why this matters:** CI is the backstop that holds every change to the same bar, however it was written. For agent-written changes it is often the first independent check, so it should cover what you actually care about.

**Questions for this area:**
- Which problems has CI missed that reached review or production?
- Which checks run locally but not in CI, or the other way round?

- [ ] **CI configuration present** (L2, `ci-config`)
  - Status: failing — No CI configuration found.
  - Why it matters: CI pipelines give agents automated feedback on whether their changes pass all quality gates
  - Goal: Set up a CI pipeline configuration (GitHub Actions, GitLab CI, CircleCI, or similar) (effort: medium, impact: high)
  - Ask yourself:
    - What should be true of every change before it merges, and who or what checks that today?
- [ ] **CI runs tests** (L3, `ci-runs-tests`)
  - Status: failing — No CI configuration found to check for test execution.
  - Why it matters: Running tests in CI means agents get immediate feedback if their changes break existing functionality
  - Goal: Ensure your CI pipeline runs the test suite on every push and pull request (effort: medium, impact: medium)
  - Ask yourself:
    - Do the tests that pass locally also run on every pull request, in the same way?
- [ ] **CI runs linters** (L3, `ci-runs-linters`)
  - Status: failing — No CI configuration found to check for linter execution.
  - Why it matters: CI lint checks catch style issues agents may miss locally, keeping the codebase consistent
  - Goal: Add linting and formatting checks to your CI pipeline (effort: medium, impact: medium)
  - Ask yourself:
    - Which checks pass locally but are skipped in CI, or the other way round?
- [ ] **Build automated** (L3, `build-automated`)
  - Status: failing — No automated build process found.
  - Why it matters: An automated build step verifies that agents' changes compile and bundle correctly before merging
  - Goal: Add an automated build step to your CI pipeline or package.json scripts (effort: medium, impact: medium)
  - Ask yourself:
    - Could a change pass tests but still fail to build or bundle? Where would that show up?
- [ ] **Deploy pipeline** (L4, `deploy-pipeline`)
  - Status: failing — No deploy pipeline found.
  - Why it matters: Automated deployments let agents' changes reach production safely through a controlled pipeline
  - Goal: Configure a deploy pipeline or stage in your CI/CD system for automated deployments (effort: high, impact: low)
  - Ask yourself:
    - How does a merged change reach users today, and which steps are manual?
    - Where should a human stay in the loop?
- [ ] **Branch protection awareness** (L4, `branch-protection`)
  - Status: failing — No branch protection rules documented or configured.
  - Why it matters: Branch protection ensures agents' PRs go through proper review and validation before reaching main
  - Goal: Document or configure branch protection rules requiring reviews and passing checks before merging (effort: medium, impact: low)
  - Ask yourself:
    - Can anything (or any agent) push straight to the main branch today?
    - Which checks must pass before a merge, and are they enforced or just expected?

## Code Health (0/2, 0%)

**Why this matters:** Agents extend whatever they find. Stale dependencies, dead code and bloated bundles get copied and built on unless something makes them visible.

**Questions for this area:**
- Which parts of the codebase would you rather an agent didn't learn from?
- How would you notice the codebase getting worse over time?

- [-] **Dependencies recently updated** (L3, `no-outdated-deps`)
  - Status: skipped (No recognized project manifest found; skipping dependency freshness check.)
  - Why it matters: Current dependencies reduce compatibility issues agents encounter and ensure security patches are applied
  - Goal: Update critically outdated dependencies to their latest stable versions (effort: medium)
  - Ask yourself:
    - Which dependencies are far enough behind that their docs no longer match how this repo uses them?
    - Who notices when an update is overdue?
- [ ] **Dead code detection configured** (L4, `dead-code-detection`)
  - Status: failing — No dead code detection tool found.
  - Why it matters: Dead code detection helps agents avoid modifying unused code and keeps the codebase lean
  - Goal: Configure dead code detection using Knip, ts-unused-exports, vulture, or a similar tool (effort: medium, impact: low)
  - Ask yourself:
    - How much code here is no longer called, and would an agent know not to extend it?
- [ ] **Bundle analysis configured** (L5, `bundle-analysis`)
  - Status: failing — No bundle analysis configuration found.
  - Why it matters: Bundle analysis helps agents understand the impact of adding dependencies on application size
  - Goal: Set up bundle analysis with webpack-bundle-analyzer, @next/bundle-analyzer, or a similar tool (effort: high, impact: low)
  - Ask yourself:
    - Does bundle size matter for this project's users? Who would notice a dependency that doubles it?

## Security (0/5, 0%)

**Why this matters:** Agents work fast and in bulk, which makes it easy to slip in a vulnerable dependency, a leaked secret or an unsafe pattern. Automated checks catch these at a volume people can't review by eye.

**Questions for this area:**
- What's the most damaging thing that could leak or be introduced through a change here?
- Which security checks would you trust to run unattended on agent-written changes?

- [ ] **License file present** (L1, `license`)
  - Status: failing — No license file found.
  - Why it matters: A clear license file helps agents understand what code and dependencies they can use
  - Goal: Add a LICENSE file specifying the project's open-source or proprietary license (effort: low, impact: low)
  - Ask yourself:
    - Under what terms can this code, and code an agent pulls in, be used and shared?
- [ ] **Security policy** (L3, `security-policy`)
  - Status: failing — No security policy found.
  - Why it matters: A security policy gives agents guidance on handling security-sensitive changes appropriately
  - Goal: Create a SECURITY.md file describing how to report vulnerabilities (effort: low, impact: medium)
  - Ask yourself:
    - If someone finds a vulnerability, how should they report it, and who responds?
- [ ] **Dependency update automation** (L3, `dep-update-automation`)
  - Status: failing — No dependency update automation found.
  - Why it matters: Automated dependency updates keep the project current so agents work with well-maintained libraries
  - Goal: Configure automated dependency updates with Dependabot or Renovate (effort: medium, impact: medium)
  - Ask yourself:
    - How are dependency updates handled today, and who notices when one is overdue?
- [ ] **Security scanning in CI** (L4, `security-scanning`)
  - Status: failing — No security scanning configured in CI.
  - Why it matters: Security scanning catches vulnerabilities agents might introduce before they reach production
  - Goal: Configure security scanning with CodeQL, Snyk, Trivy, or Semgrep in your CI pipeline (effort: high, impact: low)
  - Ask yourself:
    - Which kinds of vulnerability matter most here (dependencies, injection, infrastructure misconfiguration), and what scans for them today?
- [ ] **Secrets detection configured** (L4, `secrets-detection`)
  - Status: failing — No secrets detection tool configured.
  - Why it matters: Secrets detection prevents agents from accidentally committing API keys, tokens, or credentials
  - Goal: Set up secrets detection using Gitleaks, detect-secrets, or GitGuardian (effort: medium, impact: low)
  - Ask yourself:
    - Which secrets could plausibly end up in a commit here (API keys, .env files, cloud credentials, test fixtures)?

## Architecture & Methodology (0/3, 0%)

**Why this matters:** Without a declared and enforced structure, each agent session invents its own, and the codebase drifts. Writing the methodology down and checking it mechanically keeps new code where it belongs.

**Questions for this area:**
- If an agent added a feature tomorrow, how would it decide where the code goes?
- Which structural rules are only enforced by someone noticing in review?

- [ ] **Methodology documented** (L2, `methodology-documented`)
  - Status: failing — No methodology/architecture doc found.
  - Why it matters: A declared methodology tells agents where new code belongs instead of letting each session invent a structure
  - Goal: Declare how code is organised (layered, hexagonal, DDD, feature-sliced, LoB, …) in ARCHITECTURE.md, docs/agent-readiness.md, or docs/adr/ (effort: low, impact: high)
  - Ask yourself:
    - When a new feature lands, how does a contributor decide which folder and layer it belongs in? Is that written anywhere?
    - Which structural mistakes do you correct most often in review?
- [ ] **Architecture boundaries enforced** (L3, `boundary-enforcement`)
  - Status: failing — No architecture/boundary enforcement found.
  - Why it matters: Boundary linters turn the documented architecture into a failing check, so agent drift is caught automatically
  - Goal: Enforce module boundaries mechanically: dependency-cruiser or eslint-plugin-boundaries (JS/TS), import-linter (Python), go-arch-lint/depguard (Go), ArchUnit (JVM) (effort: medium, impact: medium)
  - Ask yourself:
    - Which imports would you reject in review (UI → DB, domain → framework, package A → package B internals)?
    - Does your language already have a boundary tool your team uses, or could a few lint rules express the same rules?
- [ ] **Agent harness enforcement rules** (L3, `agent-harness-rules`)
  - Status: failing — No agent harness enforcement rules found.
  - Why it matters: Agents get feedback on rule violations while they edit instead of only after CI fails or review catches it
  - Goal: Give agents your project rules as an enforced rules file, judged on every edit rather than only read once (effort: low, impact: medium)
  - Ask yourself:
    - Which rules do you find yourself repeating to the agent, or fixing after it?
    - Which of those can a linter express, and which need judgement (naming, error handling, where code belongs)? The judgement ones are what a rules file is for.
    - Do some rules apply only to part of the tree (API handlers, migrations, generated code)?
  - Starting points (examples, not the only options):
    - pi: Install pi-warden (`pi install -l npm:pi-warden`), run `/warden init` to write pi-warden.md, and move AGENTS.md "never/don't" gotchas into `#` rules (optionally scoped with `paths:`). Rule judging needs a TypeSafe key (`/warden enable`); `/warden improve` tunes rules from session history
    - Claude Code: Reuse the same pi-warden.md for Claude Code edits: `pi-warden init claude --project` (writes .claude/settings.json hooks)

## Agent Context & Capabilities (4/5, 80%)

**Why this matters:** This is the agent's view of the repo: what it's told, what it can reach, what it's allowed to do, and how quickly it hears about mistakes. It changes faster than any other area as the team's tools and workflows evolve, so revisit it regularly.

**Questions for this area:**
- What do you still do by hand for the agent that a context file, tool, guardrail or feedback loop could do instead?
- What has changed in how the team works with agents since you last looked at this setup?

- [x] **AI context file present** (L2, `ai-context-file`)
  - Status: passing — AI context file found: project-context.md
  - Why it matters: AI context files give agents tailored instructions about architecture decisions, patterns to follow, and pitfalls to avoid
  - Goal: Add an agent context file (AGENTS.md is read by most harnesses) with commands, architecture, conventions, and gotchas (effort: low)
  - Ask yourself:
    - What do you re-explain to the agent at the start of most sessions?
    - Which commands, conventions and gotchas would a new teammate need on day one?
    - Which harnesses does your team actually use — can one shared file (AGENTS.md) serve all of them?
  - Starting points (examples, not the only options):
    - pi: Add AGENTS.md at the repo root (pi loads AGENTS.md / CLAUDE.md from the working directory and its ancestors); add nested AGENTS.md per package in monorepos
    - Claude Code: Add CLAUDE.md, or a one-line CLAUDE.md that imports @AGENTS.md to share one source
- [x] **MCP servers / connectors configured** (L3, `mcp-servers`)
  - Status: passing — MCP configuration found: .pi/mcp.json
  - Why it matters: Committed MCP config gives every agent session the same external context instead of each user wiring it up
  - Goal: Declare the MCP servers the codebase needs (databases, APIs, observability, domain tools) in a committed config (effort: medium)
  - Ask yourself:
    - Which systems does a typical change touch outside the repo (database, cloud, tickets, docs, observability, design files)?
    - Where does the agent currently guess or ask you to paste context in?
    - Does an official server already exist for those systems (search an MCP registry), and should it be read-only for agents?
  - Starting points (examples, not the only options):
    - pi: Declare project servers under `mcpServers` in .pi/mcp.json and validate with `pi mcp list` (loads after project trust)
    - Claude Code: Add servers to .mcp.json at the repo root
- [x] **Agent skills & packages available** (L3, `agent-skills`)
  - Status: passing — Agent skills/packages found: .pi/extensions/contract-guard.ts
  - Why it matters: Repo-scoped skills and packages encode how THIS codebase is built, tested and released, so agents stop rediscovering it
  - Goal: Commit codebase-specific agent capabilities (skills, prompt templates, extensions, packages) so recurring workflows are reusable (effort: medium)
  - Ask yourself:
    - Which multi-step tasks do you walk the agent through repeatedly (release, migration, adding an endpoint, regenerating clients)?
    - Which tools, scripts or internal services does this repo need that the agent can't call yet?
    - Has someone already packaged this? Search before you build; if nothing fits, a small project prompt, skill or extension is cheap to write.
    - Would other repos on the same stack benefit? Then it's worth publishing as a shared package.
  - Starting points (examples, not the only options):
    - pi: Share packages with `pi install -l npm:<pkg>` (written to .pi/settings.json); add prompt templates in .pi/prompts/*.md, skills in .agents/skills/<name>/SKILL.md, or a custom extension in .pi/extensions/. See Considerations for stack-specific package ideas
    - Claude Code: Add .claude/skills/<name>/SKILL.md, .claude/commands/*.md, or .claude/agents/*.md
- [x] **Agent guardrails (hooks / permissions) configured** (L3, `agent-guardrails`)
  - Status: passing — Agent guardrails found: .pi/extensions/contract-guard.ts, .pi/extensions/readiness-enforce.ts
  - Why it matters: Repo-scoped guardrails protect every agent session, not just machines that happen to have user-level guards installed
  - Goal: Commit repo-scoped guardrails (hooks / permission rules) that block or hold destructive and off-policy agent actions (effort: medium)
  - Ask yourself:
    - What is the worst thing an agent could run in this repo (publish, deploy, drop a database, force-push, delete files)?
    - Which of those should be blocked outright, and which just need a human to confirm?
    - Are any secrets, credentials or production configs reachable from the working tree?
  - Starting points (examples, not the only options):
    - pi: `pi install -l npm:pi-warden` — its offline guards hold irreversible commands (no key needed); commit .pi/pi-warden.json for project settings, and add repo-specific bans to .pi/aio-blocklist.json or .pi/hook/hooks.yaml
    - Claude Code: Add `permissions.deny`/`ask` rules and PreToolUse hooks to .claude/settings.json
- [ ] **In-edit code feedback for agents** (L3, `agent-edit-feedback`)
  - Status: failing — No in-edit code feedback for agents found.
  - Why it matters: Per-edit diagnostics let agents fix mistakes in the same turn instead of compounding them until CI fails
  - Goal: Feed lint, type and structural diagnostics back to the agent right after each edit, not only in CI (effort: low, impact: medium)
  - Ask yourself:
    - How long after an agent writes a bug do you find out — the same turn, at CI, or in review?
    - Which linters, type checkers or LSPs does this stack already have that could run on every edit?
    - Which codebase-specific patterns (banned APIs, required wrappers, naming) could become a structural rule?
  - Starting points (examples, not the only options):
    - pi: `pi install -l npm:pi-lens` (LSP, linters, ast-grep and tree-sitter diagnostics after every write); commit a .pi-lens.json for project toggles and codebase rules under rules/ast-grep-rules/rules/ (the pi-lens-write-ast-grep-rule skill scaffolds them)
    - Claude Code: Add a PostToolUse hook (matcher Edit|Write) to .claude/settings.json that runs lint/typecheck on the changed file

## Find what fits this repo

The tools named above are examples. The best setup depends on your stack and how your team works with agents. Work through these questions; each "yes" points to a kind of capability worth looking for.

- [ ] What do you re-explain to the agent in most sessions?
  - Look for: context file content, or a skill that loads when relevant
- [ ] Which review comments keep recurring on agent-written changes?
  - Look for: a lint/structural rule, or an enforced rules-file entry
- [ ] Which systems outside the repo does a typical change touch (DB, cloud, tickets, docs, observability, design)?
  - Look for: an MCP server or a tool extension for that system
- [ ] Which multi-step workflows do you walk the agent through by hand?
  - Look for: a prompt template, skill, or custom extension
- [ ] Which commands or files would be costly if an agent got them wrong?
  - Look for: a guardrail: block, or require confirmation
- [ ] Where does the agent burn the most turns (finding code, running tests, reading huge output, waiting on slow checks)?
  - Look for: a navigation/search, test-runner, or output-compression extension

**Where to look** (adopt before you build):
- pi: Browse the pi package gallery (https://pi.dev/packages) or `npm search keywords:pi-package` — search for your stack, tools and pain points, not just the names in this checklist
- pi: Trial a package project-scoped with `pi install -l <source>`; trim what it loads with `pi config -l`; remove it if it doesn't earn its context
- pi: Nothing fits? Start with a .pi/prompts/*.md or a small .pi/extensions/*.ts; if it's useful beyond this repo, publish it with the `pi-package` keyword
- Claude Code: Browse plugin marketplaces with `/plugin` and the skills/commands other teams on your stack share
- Any harness: For external systems, check the official MCP registry (https://registry.modelcontextprotocol.io) and the vendor's own docs for an official server
- Ask your agent: describe the pain point and your stack, and have it search for existing packages, skills or MCP servers before proposing to build one

Legend: [x] detected as passing (still worth revisiting), [ ] failing / to decide, [-] skipped
