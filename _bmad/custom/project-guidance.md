# Project guidance (on demand)

Full operating guidance retained from project-context.md. Read it when running or
reassessing AR, or auditing/changing guardrail design. Universal invariants stay in
project-context.md; this reference does not replace the specific workflow manuals.

## Story contracts

Every tracked BMad story has one authoritative acceptance contract: the `## Acceptance Contract`
inside its `bmad-build` spec's frozen block. Before implementation, it defines stable `AC-*`
acceptance obligations and `VAL-*` mechanical/manual validation obligations, obtains explicit
product and Test Architect (BMad TEA module) approval, and seals the normative section with a
digest. Development may append evidence but must not silently change approved intent, scope,
risk, acceptance behavior, or validation oracles; semantic changes go through Correct Course,
revision, and reapproval. QA independently consumes the same contract and traces
AC -> VAL -> evidence. Follow `_bmad/custom/story-contract.md`; prompts are soft policy, while
the contract validator, actual tests, and protected CI/repository gates provide mechanical
enforcement. During Agent Readiness, wire draft/approved/delivered validation at the appropriate
lifecycle points into the target project's aggregate local check and required CI/repository
controls; never claim the TOML hooks alone are hard gates.

## Linear project workflow

For a new named BMAD project, run `bmad-linear` (or the agent's LP menu) to agree the
planning steps, create/reuse its Linear Project, and publish those step tickets before
work starts. Follow `_bmad/custom/linear-workflow.md`: approved epics/stories and Build
execution tasks go into the same Project as they are agreed, with durable identities
under `_bmad/linear/`. Do not invent optional steps, confuse publishing with approval,
mark Build output delivered, or import tracker edits as changes to a frozen contract.

## Version control (jj)

Projects using these customisations use Jujutsu (jj), never git, for agent version-control work.
Follow `_bmad/custom/jj-vcs.md`: agents run `jj new` and `jj describe` to give each stage
(planning, ATDD, implementation, review) its own described change, and may set and push any
bookmark except `main`, forward only; `main` and history edits stay with the user. If the
workspace is not a jj workspace, stop and ask rather than falling back to git or initialising jj.
A story contract's approval is its own sealed jj change, and the validator checks the contract
against that recorded version (story-contract.md, "Approval change (jj)").

## Guardrail Steward

The guardrails above exist to make agents effective, not to slow delivery. Vera, the Guardrail
Steward (`bmad-agent-steward`), checks that they still serve that purpose. Code Review hands
every reviewed story to her: she analyses whether the guardrails helped or hindered it (her
read-only scan is one input, not the verdict) and discusses any concern with the user. The
retrospective runs the scan project-wide. When a contract, locked test, edit guard or CI check blocks legitimate
work, stop and bring in the steward instead of working around it: she diagnoses the cause with
the user, routes requirement or test problems to Correct Course or TEA, and adjusts a mechanism
only on the user's explicit decision, re-proven and recorded under `## Steward Decisions` in
`docs/agent-readiness.md`.

## Methodology & structure — established per project, NOT baked in

How this project organises code and which structural rules it enforces (e.g. Locality of
Behaviour, layered, hexagonal, DDD, feature-sliced) are decided by the AR step with the user,
not assumed here. The decisions and their enforcement live in docs/agent-readiness.md —
follow that file when it exists; if it doesn't, run AR before writing significant code.
AR first elicits and prioritises the user's engineering principles, resolves conflicts between
them, then derives methodology, tooling, tests, and CI gates from those priorities. Every enforced
rule must trace back to an agreed principle; opinionated recommendations are welcome, hidden dogma is not.
No agreed decision may be orphaned in prose. Each gets the strongest reliable enforcement justified by
its weight: a mechanical blocker, an active warning, contextual surfacing, or an explicit manual assurance
check. Soft mechanisms such as skills, MCP context, and documentation must never be mislabeled hard gates.
Every configured blocker/warning must be exercised once so the team knows it actually blocks or surfaces.
Programmatic enforcement is always preferred: agents are probabilistic and cannot be trusted to remember,
interpret, or apply a rule consistently. Agent prompts, skills, MCP context, warnings, and manual review are
defence-in-depth and visibility, not substitutes for a deterministic local check or protected CI/repository gate.
Still use those soft defences deliberately: layered reminders, timely diagnostics, relevant context, and manual
review catch ambiguity and novel failures that mechanical controls cannot express. Mechanical-first means soft
controls are accurately labelled and never the sole claimed enforcement for a critical rule—not that they are skipped.

## Agent readiness (the environment makes the agent effective)

"The agent is not broken. The environment is." AR's purpose is to improve agentic programming
by engineering mechanical correction loops, not completing a tooling checklist or maximising
a score: **change -> triggered deterministic check -> agent-visible diagnostic -> correction ->
fresh recheck**. The intended gains are earlier actionable feedback, fewer blind retries and
fewer escaped defects; don't claim an improvement without observations. Before adding a tool,
name the agreed failure mode/risk, trigger, useful diagnostic and corrective action it serves.

Treat the loop as load-bearing: when it is missing, building it IS the task. Reuse the smallest
reliable mechanism; the pillars (Style & Linting · Testing · Documentation · Dev Environment ·
CI/CD · Code Health · Security · Architecture · Context) are a coverage sweep, not a shopping list.
AR records a Feedback Loop Register in docs/agent-readiness.md and proves representative
failure -> diagnosis -> repair -> fresh pass through the actual agent-facing trigger/channel,
with latency and evidence. A configured hook or passing CLI command alone does not prove that
feedback reaches the agent. The agreed score remains necessary but is never sufficient for ready;
applicable critical loops, boundary and control validation must also pass. During programming,
consume the fastest relevant check's real result, make a bounded correction and rerun before
more speculative edits; retain the full aggregate/CI backstop and independent manual assurance.

AR is downstream of product planning, not a generic questionnaire. Before interviewing, it reads the
available BMad discovery/planning outputs and bases recommendations on the planned product, architecture,
deployment, risks, constraints, critical journeys, and delivery shape. It distinguishes explicit decisions
from inference, cites the input artifact paths, surfaces conflicts/staleness, and does not re-ask answered questions.

AR also agrees the coding environment and its trust boundary with the user, as a recorded threat model.
The recommended default is a committed, project-specific devcontainer with Pi running as a non-root user and
access limited to the workspace and explicitly approved services/secrets. A user may explicitly choose another
boundary (for example native host + a version manager such as mise); docs/agent-readiness.md then records it as
unsandboxed, with its residual risks and compensating controls. Nothing is called sandboxed if Pi inherits host-user
permissions or the container mounts the host container socket, host home, SSH agent, broad credentials/devices, or
runs privileged. Keep production credentials out of development sessions. AR documents the threat model, exceptions,
and validation evidence; Dagger or other execution engines must not silently weaken the agreed boundary.

Agent capabilities are clone-ready by default: AR inventories the active Pi runtime's supported
project resources and commits every applicable configuration and artifact beside the code, using
that runtime's native paths. This includes project settings/packages, skills, extensions/hooks,
prompts or presets, themes, and MCP configuration where selected. Prefer a root .mcp.json as the
shared cross-agent MCP source and add Pi-specific MCP config only when the chosen runtime or adapter
requires it. Never commit credentials or generated package caches, and never write user-global
configuration unless the user explicitly asks.

Automated green is necessary, not sufficient. The Test Architect independently checks delivered work
against the BMad requirements, engineering-principle matrix, architecture decisions, threat model, and
documented exceptions. It manually examines risks that linters/tests/hooks cannot reliably express and
records evidence; recurring valuable manual checks should become deterministic automation.
