# Agent readiness (AR) workflow

<!-- Shared by the AR menu item on the architect (Winston), dev (Amelia) and TEA (Murat) agents.
     Edit here only; the agent overrides load this file. -->

## Purpose — improve agentic programming through mechanical feedback

AR engineers the environment so a coding agent can detect mistakes early, understand what
failed, make a bounded correction, and verify it without relying on memory or guesswork.
The deliverable is a working correction cycle, not a tooling checklist or a high rubric score:

**change -> triggered deterministic check -> agent-visible diagnostic -> correction -> fresh recheck**

Design AND build that scaffold BEFORE product implementation begins. Interview -> design the
loops -> build -> rehearse failure and repair -> assess coverage. The intended gains are shorter
time-to-actionable-feedback, fewer blind retries, and fewer defects escaping into review/CI;
measure what is observable, never claim an unmeasured productivity improvement.
You impose NOTHING — no methodology, tool or structure. Elicit the user's priorities and design
loops WITH them. The pillars are a coverage sweep for relevant gaps, not a shopping list.
Where a capability cannot be proven until code exists, record it deferred with its trigger;
do not count a configured but unexercised mechanism as active. Follow project-context.md.

LINEAR TRACKING: read `_bmad/custom/linear-workflow.md` and follow Activation for the
agreed AR step once the project is known. If no binding/plan exists, offer Kickoff;
never invent a planning ticket or let publishing bypass readiness/contract gates.

PHASE 0 — SYNTHESISE THE PLANNED PROJECT (before interviewing): discover the configured BMad output
locations and read every relevant existing artifact, including available product brief/research, PRD,
UX, architecture/NFR/data/API/deployment decisions, epics/stories, technical specs, and test design.
Also inspect stack manifests such as mise.toml/package.json/pyproject/go.mod/*.tf. Extract the planned
product shape, critical user journeys, stack, scale, trust boundaries/data sensitivity, integrations,
deployment target, risks, constraints, and already-made decisions. Cite exact input paths, distinguish
facts from inference, surface conflicting/stale artifacts, and ask only what the outputs do not answer.
Give the user a concise synthesis to correct before recommending anything. If planning outputs do not
exist yet, say so explicitly and proceed using the evidence available; never invent a planned architecture.

From that synthesis, identify the project's likely agent failure modes and missing feedback:
what could the agent get wrong, what currently detects it, and how late would it learn?
Distinguish observed problems from risk-based hypotheses; do not invent historical failures.

PHASE 1 — PROJECT-SPECIFIC DESIGN (interview; tailor options to Phase 0, offer an opinionated lazy
default per item with reasons, then ask and record — ask, don't monologue):
  0. Engineering principles, methodology & patterns — first elicit the principles the user values,
     including simplicity, type safety, test confidence, security, performance, architectural isolation,
     delivery speed, and documentation. Discuss relevant schools such as Clean Code, Locality of Behaviour
     (LoB), SOLID, DRY, YAGNI, functional core/imperative shell, layered, hexagonal/ports-adapters, DDD,
     and feature-sliced design as trade-offs, not doctrine. Mark each selected principle critical,
     important, or lightweight. Surface and explicitly resolve conflicts (for example delivery speed vs
     exhaustive testing, LoB vs strict layering, or simplicity vs abstraction). Then agree how the repo is
     organised and translate the priorities into concrete, enforceable rules. Do NOT silently assume one.
  1. Style & Linting — recommend an opinionated linter, formatter, type/strict checks, .editorconfig,
     and pre-commit approach derived from the principle priorities; explain the mapping and alternatives.
  2. Testing — recommend an opinionated framework, test convention/location, one test command, coverage,
     and E2E scope derived from the weighted risks and principles; avoid tests that do not buy confidence.
  3. Documentation — README, CONTRIBUTING, CODEOWNERS, AGENTS.md/CLAUDE.md, ARCHITECTURE/ADR, API docs.
  4. Dev Environment & agent boundary — threat-model the coding environment with the user. Recommend by
     default a committed Dev Container Specification setup tailored to the planned stack:
     .devcontainer/devcontainer.json plus the smallest Dockerfile/Compose files needed, runtime/tool pins,
     lockfiles, .env.example, one-command setup, and the selected Pi distribution. Default to non-root Pi
     with no runtime sudo, no privileged mode, no host container socket/home/SSH agent/cloud credential
     mounts, no unnecessary capabilities/devices/ports, no secrets baked into image/repo, and only the
     workspace plus explicit named volumes/services mounted. Drop capabilities and enable no-new-privileges
     where the runtime permits; discuss network/egress needs and document any unrestricted boundary.
     The user may explicitly choose another boundary instead (for example native host + a version manager
     such as mise). Then record it as unsandboxed: Pi inherits host-user permissions; list protected host
     assets, keep production credentials out of development, state the real network/egress posture
     (proxy variables or config are not proof), and agree compensating controls. Never describe an
     unsandboxed choice as sandboxed. If Dagger needs a container engine, explicitly choose a remote
     engine, isolated rootless/nested engine, CI-only execution, or a user-accepted weaker boundary—never
     silently mount /var/run/docker.sock or call a privileged container sandboxed.
  5. CI/CD — recommend Dagger first as the portable local-and-CI execution layer, explain its container
     runtime/setup cost, then let the user choose Dagger or provider-native CI. Choose the hosting provider,
     jobs (lint+types+test+architecture+security+build), deploy flow, and which checks BLOCK merge. Establish
     one local/CI parity command (`dagger check` by default) and require automated tests on pull requests.
     Contract CI wiring: for each test suite agree its runner command, JUnit reporter, where the report
     is written (outside the workspace, e.g. $RUNNER_TEMP) and how tests carry their VAL ID (in the test
     name or tag, or a testcase `val` property). Checks that are not tests (scans, contract verification)
     emit JUnit through a small converter or stay manual. The stack is the project's choice; the fixed
     interface is story-contract.md 'CI results'. The CI provider (Dagger, GitHub Actions, GitLab CI…)
     is chosen per project in this step; do not impose one, and do not assume merge protection.
     Reuse bmad-testarch-framework and bmad-testarch-ci to build it.
  6. Code Health — dead-code detection, dependency freshness + update automation.
  7. Security — LICENSE, SECURITY.md, secrets detection, dependency + SAST scanning in CI.
  8. Agent context & capabilities — AI context files (CLAUDE.md/AGENTS.md). Detect the installed Pi
     runtime/distribution and version, then inventory every project-local capability it supports:
     settings and packages/plugins, skills, extensions/hooks, prompts or presets, themes, MCP/LSP,
     system-prompt files, and runtime-specific resources. Confirm the BMad TEA module (bmad-tea,
     bmad-testarch-*) is installed: the story-contract lifecycle requires it; if absent, recommend
     installing it and record the blocker. Discover the best agent CI-feedback integration
     for the CI provider and stack chosen in item 5: prefer an official provider MCP, then an audited and
     user-approved third-party MCP, then a least-privilege provider CLI/API or structured CI log/artifact
     adapter when no suitable MCP exists. Dagger MCP and GitHub MCP's `actions` toolset are examples, not a
     closed list. The integration must let agents inspect check status and actionable failure logs; default
     to read-only, minimum scopes/toolsets, and no committed credentials. Search primary docs, relevant stack/domain
     capabilities, and pi.dev/packages; suggest the smallest useful set and record the user's picks.
     Default to clone-ready committed project config. Use ~/.pi/agent, ~/.omp/agent, ~/.config/mcp,
     or another user-global path only when the user explicitly requests it.
  9. Acceptance threshold — agree observable loop outcomes and feedback budgets appropriate to
     this project, then propose a readiness score of 8/10 as a secondary coverage threshold and
     ask the user to confirm it or explicitly choose another. Both proven applicable loops and
     the agreed score are required; a numeric pass alone cannot establish readiness.
Item 0 drives the enforceable structure rules — translate their chosen methodology into concrete
checks (import boundaries, dependency direction, path rules, …). After agreeing those priorities,
organise the decisions around the highest-value failure modes and correction loops, not pillar order.
For every proposed tool/artifact ask: which agreed risk or programming failure does it address,
when will it run, what useful signal reaches the agent, and what should the agent do next?
A justified compliance/safety obligation also earns its place; not every control is a speed optimisation.
Reuse an existing loop when it covers the need. Review every applicable pillar, but do not install
something for every pillar; record not-needed/deferred choices with reasons and activation triggers.
Stay lazy: the smallest reliable feedback loop, not the most tools.

ENFORCEMENT LADDER — apply this to EVERY agreed principle, architecture/tooling/security/testing decision;
no decision may remain orphaned prose. Choose the strongest reliable level justified by its priority and
record why weaker/stronger levels were rejected:
  A. HARD BLOCK — deterministic Pi extension/hook, compiler/type/lint/architecture rule, test/security scan,
     Dagger check, pre-commit gate, or required CI check that prevents the prohibited outcome.
  B. ACTIVE WARNING — non-blocking Pi hook/plugin, linter warning, advisory check, editor diagnostic, CI
     annotation, or MCP/CLI feedback that puts the issue in front of the agent/user at the point of work.
  C. CONTEXT SURFACE — AGENTS.md/context, skill, prompt/preset, MCP resource, generated report/dashboard,
     checklist, or documentation that makes a non-mechanical decision visible when relevant.
  D. MANUAL ASSURANCE — a concrete Test Architect code-review check with required evidence when automation
     would be unreliable or disproportionate.
Default mapping: critical decisions require a hard blocker wherever technically reliable, preferably a fast
local control plus a required CI backstop; if no reliable blocker exists, make the manual check approval-
blocking and visibly warn. Important decisions require at least an active warning plus review evidence, and
block when cheap/reliable. Lightweight decisions require contextual surfacing or a named manual check. Skills,
MCP, docs, prompts, and reports are soft unless an actual intercepting hook/check enforces them. Every rule
needs an owner, trigger, evidence location, exception/expiry path, and deferred activation trigger.

Explain the trust model during this discussion: programmatic enforcement is always better because agents are
probabilistic and cannot be trusted to remember or consistently enforce rules. Prompts, skills, MCP context,
reports, warnings, and QA-agent review improve visibility and defence-in-depth but are never equivalent to a
compiler/linter/test/policy/hook or protected CI/repository gate. If a critical decision cannot be enforced
programmatically, record it as explicit residual risk, make its manual review approval-blocking, and obtain
the user's acceptance; do not mark it mechanically enforced.
Still layer useful soft defences around mechanical controls: put concise context where the agent sees it, emit
warnings close to the edit, expose actionable evidence through MCP/reports, supply focused skills/prompts, and
give QA explicit residual checks. Mechanical-first means soft controls are labelled honestly and are not the
sole claimed enforcement for a critical decision; it does not mean omitting them.

Potential considerations to discuss when the project's risk/scale earns them (not automatic dependencies):
  - A small machine-readable decision registry that generates/validates Pi rules, Dagger/CI checks, QA
    checklists, evidence links, exceptions and expiry, preventing the Markdown matrix from drifting.
  - Policy-as-code plus repository-host controls (for example structured config/IaC policies, CODEOWNERS,
    protected required checks and merge rules) so important controls cannot be bypassed from an agent session.

Explore further tooling WITH the user based on actual Phase 0 requirements and uncovered enforcement gaps.
Search current primary documentation and the relevant ecosystem for suitable compiler/linter rules, architecture
fitness tools, policy-as-code, contract/schema checks, test-strength tools, security/supply-chain scanners,
devcontainer controls, Dagger modules, CI capabilities, Pi packages/extensions/hooks, MCP servers, skills,
prompts and observability/runtime feedback. Present at most 2–3 credible options per real gap, recommend one
(including "build nothing/use the existing tool"), and compare enforcement strength, feedback latency,
false-positive risk, maintenance, security/trust, permissions, portability, licence/cost and agent context overhead.
The user chooses; record accepted/rejected/deferred options and rationale. Never install or grant access merely
because a tool exists—reuse the stack first and obtain explicit approval for dependencies, services or credentials.

PHASE 2 — ARTIFACT: write docs/agent-readiness.md as a living risk/principle-led feedback-loop
strategy. Make the Feedback Loop Register the primary delivery plan, with exact commands,
triggers and enforcement. Add a short pillar coverage summary with each relevant choice's
reason and status (active | deferred + trigger | not-needed + reason). Not-needed means genuinely
inapplicable, never a waiver of an agreed obligation or critical control. Record the chosen
methodology and its enforcement rules up top.
Add an Inputs & Assumptions section citing the BMad artifacts used, decisions inherited, inferences,
conflicts/staleness resolved with the user, and project risks that shaped the scaffold. Record an overall
status (designing | building | ready); ready requires proven applicable correction loops, the
agreed score, and successful validation of the agreed environment boundary and critical controls.
Add a Feedback Loop Register linked to the principle/risk IDs, with: failure mode, check and
normal-work trigger, where the diagnostic reaches the agent, expected correction, measured
feedback latency/budget, local-vs-CI tier, reproducible failure/repair evidence, owner and status.
For example, a wrong interface might use a type check; wrong behaviour a focused test; an
illegal dependency a boundary check. These are illustrations, not mandatory tool choices.
Prefer immediate focused feedback plus the full aggregate/CI backstop; slow/noisy checks need
an explicit routing strategy, not silently weaker gates. Record baseline observations when
available; in a new project record the initial measurement without claiming an improvement.
Add a Project Agent Surface manifest covering every capability category from item 8: its exact
repo-local path or package reference, active/not-needed/deferred status, and a fresh-clone discovery check.
Add an Engineering Principles Traceability Matrix with: principle, priority, resolved conflicts,
decision/rule ID, selected tool, enforcement level (hard | warning | context | manual), config/code path,
local command/trigger, agent hook/plugin/skill/MCP feedback, CI check/gate, evidence location, owner,
exception/expiry process, status, and deferred activation trigger. Add an Enforcement Coverage summary proving
every agreed decision has at least one active/deferred mechanism and explicitly listing any orphan as a blocker.
Add a short Potential Enforcement Considerations section recording whether the decision registry and policy-as-
code/repository-host controls were adopted, rejected, or deferred, with the project-specific reason and trigger.
Add a Tooling Exploration Log linking each explored tool to a concrete requirement/gap, recommendation and
trade-offs, user decision, approval/access needs, selected version/source, and revisit trigger. No gap means no tool.
Add an Environment Threat Model naming the agreed boundary (devcontainer, or an explicitly accepted
unsandboxed alternative), protected host assets, permitted mounts/network/secrets, credential exclusions,
selected Dagger engine boundary, accepted exceptions, exact start/exec/setup commands, and validation evidence.
Add a Contract CI Wiring table: suite, test command, JUnit report path, VAL ID convention (name/tag or
`val` property), testcase `contract` identity and full `test-file`/`test-id` export (or native file/name),
the CI provider and job it runs in, and the step that runs
`validate_story_contract.py ci --require-jj --junit ...` after the tests, with the run identity it records. Story planning and ATDD follow this convention.
Add a Residual Manual Assurance Plan mapping every requirement/principle/risk not fully covered by automation
to a concrete manual check, evidence expected, frequency/trigger, and Test Architect ownership. Include a
rule for promoting repeated valuable findings into the smallest deterministic test/lint/architecture/CI gate.

PHASE 3 — BUILD + REHEARSE + ASSESS (after approval): create every artifact buildable now, designed from the
user's decisions — no canned templates. Encode the methodology rules as real enforcement (linter,
CI gates, .pi/readiness.rules.json, and a compatible project-local readiness extension).

Build and validate the agreed environment BEFORE implementation: install the pinned application toolchain,
Pi, project-local agent resources, readiness commands, and Dagger client when selected. For a devcontainer,
run Pi and normal dev commands as the non-root container user; keep credentials in runtime secret/env
injection, never image layers; validate with the Dev Container CLI (or the user's compatible implementation):
build/up the container, execute the stack setup and aggregate checks inside it, confirm the user is non-root,
confirm forbidden host sockets/paths are absent, start Pi inside it, and confirm Pi discovers the committed
context, skills, extensions, prompts/presets, packages and MCP configuration. For an explicitly accepted
unsandboxed boundary, prove one-command setup from a fresh clone without user-global changes, confirm
production credentials are absent, record the actual egress posture, and confirm the same Pi discovery.
Record commands/results and known network/container-engine exceptions. Do not mark ready if validation fails,
or if a privileged/host-socket/host-user exception is mislabeled sandboxed.

Build the
lint, format, type, unit/integration/E2E, architecture, security, and build checks selected by the
traceability matrix. Recommend and, when approved, initialise Dagger in the project's primary language,
implement those validations as focused Dagger checks, and make `dagger check` the green local parity gate.
Create the chosen CI provider workflow as a thin automated wrapper that installs Dagger and runs the same
checks for pull requests and protected branches. If the user declines Dagger, implement equivalent gates
with their chosen CI and retain one reproducible local aggregate command. Critical principles should block;
important/lightweight principles get the enforcement level explicitly agreed in the matrix.

Wire `_bmad/custom/scripts/validate_story_contract.py` (draft/approved/delivered phases, see
_bmad/custom/story-contract.md) into the aggregate local gate and required CI at the story lifecycle points
project-context.md describes.
In jj projects, run the CI validation with `--require-jj` so a missing, ambiguous or mismatched approval
change fails the gate (see story-contract.md 'Approval change (jj)').
Have the project's CI (whichever provider was chosen) write JUnit XML outside the
workspace and run `validate_story_contract.py ci --junit <report>` (every approved contract, any stack)
after its test steps, so mechanical checks pass only on real test results (story-contract.md 'CI results').
Prove the wiring once: a temporary VAL-tagged test that fails must fail the contract step naming the VAL ID,
then pass after repair; a report without the test must fail with 'CI did not run it'. Remove the probe.
Keep `.pi/extensions/contract-guard.ts` installed (sync.sh ships it): its edit guard refuses agent edits to approved
contracts and locked tests (story-contract.md 'Edit guard (Pi)').

Implement every active enforcement mapping, not just the underlying tool installation. Wire hard controls into
the fastest appropriate local/Pi feedback point and a required CI gate where warranted; wire warnings into a
place the agent/user will actually see; install/contextualise selected skills, MCP resources, prompts, reports,
and hooks; and add every residual item to the Test Architect plan. Mechanically validate the enforcement itself:
for each hard blocker, use a safe temporary/fixture violation or tool-native config test to prove a non-zero/
blocked result; for each warning/context surface, prove the intended diagnostic/context is emitted or discovered;
then remove temporary violations. Record evidence. Do not claim a rule active merely because its config file
exists. Any unimplemented or unproven mechanism remains deferred/not-ready and cannot satisfy a critical rule.

PROVE THE LOOP FROM THE AGENT'S POINT OF VIEW, inside the agreed environment boundary:
rehearse at least one representative coding failure and correction end-to-end, in addition to
exercising every configured blocker/warning as required above. Use a harmless temporary fixture
or tool-native self-test; never production resources, secrets or an altered approved contract.
Start with a passing baseline, introduce a known fault, exercise the normal edit/check trigger,
then observe the actual failing result and diagnostic in the channel the coding agent uses.
Record elapsed time, source/rule/expected-vs-actual detail, and the bounded correction taken.
Repair the fault without weakening the oracle or disabling a gate, rerun the same check freshly,
and confirm it passes; restore temporary probes and run the aggregate gate. Do not remove a
real assertion just to make it green. A direct CLI test alone does not prove an automatic hook
or diagnostic delivery. If the agent cannot see or act on the result, the loop is not proven.
If an integration is unavailable, flaky, excessively noisy or slower than its agreed budget,
record the gap and fix or explicitly defer it; applicable critical gaps still prevent ready.
Configuration presence, a screenshot of green CI, and agent assurances do not replace this evidence.

Configure the selected CI feedback integration in the committed, secret-free agent surface. Use whatever
official MCP the chosen CI provider offers; otherwise use an audited user-approved MCP, or a narrow CLI/API/
artifact adapter when no MCP fits. Expose the Dagger module through MCP when useful and compatible. Configure
only workflow/check/log capabilities with read-only minimum scopes by default. Validate from inside the
agreed environment that the agent discovers the integration and retrieves actionable failed-check diagnostics.
This feedback integration enriches the loop but never replaces deterministic local checks or CI merge gates.

Build the
clone-ready Project Agent Surface using the detected runtime's documented conventions. For upstream Pi,
use committed .pi/settings.json and real artifacts in applicable .pi/extensions/, .pi/skills/<name>/SKILL.md,
.pi/prompts/, and .pi/themes/ paths, plus .pi/SYSTEM.md or .pi/APPEND_SYSTEM.md when selected. For
runtime/package features such as presets, create their documented
project files (for example .pi/presets.json and .pi/presets/). Put packages/plugins in project settings and
use local-scope installation (for example `pi install -l`) only with approval; commit declarations/locks,
not caches. For MCP, create a secret-free root .mcp.json as the shared cross-agent source plus .pi/mcp.json
when required by the chosen Pi runtime/adapter; document one canonical server list, use environment-variable
placeholders, and update .env.example. Do not invent unsupported plugin folders or empty cargo-cult directories.
Install the toolchain only with the user's go-ahead (mise use); reuse bmad-testarch-framework/ci where they
fit. Validate from a fresh-clone perspective that Pi discovers every active skill, extension, prompt/preset,
package/plugin, and MCP server before scoring.
Then ASSESS COVERAGE: run the readiness scorer exactly as
`pnpm dlx @danielboothcloud/agent-readiness . --format json`. Treat the score as a coverage
diagnostic, not the objective. Inspect each gap against the agreed risks, real correction loops
and explicit obligations; improve the capability it exposes, not just the rubric's file count.
Never add irrelevant tooling solely to raise the score or claim runtime performance from it.
Rerun after meaningful fixes. Do not declare ready below the agreed threshold (8/10 by default)
or with an unproven applicable critical loop, boundary or control—even if the score is high.
If the rubric and a justified project choice conflict, record the conflict and ask the user to
resolve it explicitly; do not silently lower the threshold or waive a required control.
Record remaining deferred items/triggers, add the scorer to CI for coverage tracking, and keep
its result separate from the failure/repair evidence in docs/agent-readiness.md.
Implementation then uses the proven loops: make a bounded change, consume the fastest relevant
check's actual result, correct the reported failure, and rerun before further speculative edits.
Run the full aggregate gate at the required handoff. These instructions are soft policy; the
project must implement and exercise its selected triggers/checks and protected gates.

Finally follow Linear Planning completion for AR using the actual readiness document,
score, proven failure/repair loops, agreed boundary/control validation and acceptance evidence.
Only a ready scaffold
meeting its agreed obligations closes the ticket; a design, failed check or interrupted
run remains In Progress/pending. Report the Linear URL or publication blocker.
