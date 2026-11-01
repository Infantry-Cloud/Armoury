# Project Context

Universal invariants for every agent. Detailed operating procedures load only when their
operation is needed, as listed below; no workflow steps or mechanical checks are removed.

## Universal ethos (methodology-agnostic)

The best work is the work never done. Lazy means efficient, not careless. Before proposing
ANY artifact — story, requirement, design, or code — stop at the first rung that holds:

1. Does this need to exist at all? Speculative need = skip it, say so in one line. (YAGNI)
2. Does something we already have cover it? Use it.
3. Can it be one line / one paragraph? Make it that.
4. Only then: the minimum that works.

Question complex requests: "Do you actually need X, or does Y cover it?" Ship the lazy
version and flag it in the same response. Default to the answer you can defend; don't stall.

## When writing code (universal hygiene only)

- Reach for the standard library / a native platform feature / an already-installed dep before new code.
- Explicit over implicit: no hidden globals, no magic; type public signatures.
- Don't abstract speculatively or add boilerplate/dependencies nobody asked for; wait for the
  third occurrence before extracting an abstraction.

### Never lazy about

Input validation at trust boundaries, error handling that prevents data loss, security,
accessibility, anything explicitly requested. Fail fast: validate at the boundary, raise at
the source — never swallow an error to keep going.

### Simplifications

Mark intentional shortcuts with a `ponytail:` comment; if the shortcut has a known ceiling
(global lock, O(n²) scan, naive heuristic), name the ceiling and the upgrade path.

### Testing

Non-trivial logic leaves ONE runnable check behind — the smallest thing that fails if the
logic breaks (assert self-check or one small test; no frameworks/fixtures unless warranted).
Trivial one-liners need no test. Never delete a test to make it pass.

## Story contracts

An approved Acceptance Contract is the source of truth. Never invent product or Test Architect
approval, alter approved intent or locked tests without Correct Course and reapproval, or claim
delivery from Build alone. Run the required validator phases and real tests; report actual evidence.

## Linear project workflow

For a new named project, agree the plan through `bmad-linear` or LP before publishing work.
Publishing, board status and task checkboxes never authorise scope, implementation or acceptance.
Use stable identities; do not invent tickets or close the Linear Project automatically.

## Version control (jj)

Use jj, never git. Agent mutations are limited to `jj new` and `jj describe` on the current change;
bookmarks, pushes, history edits and setup stay with the user. Stop on unknown work or a missing
jj workspace; never silently initialise it or fall back to Git.

## Guardrail Steward

Guardrails counter probabilistic agent failures, not just process mistakes. Never bypass a check
to finish. Code Review hands over to Vera's RV analysis; she discusses benefits, friction and blind
spots with the user. Only the user's explicit decision authorises a mechanism change.

## Methodology & structure — agreed per project

Follow the user's recorded engineering principles, environment boundary and checks in
docs/agent-readiness.md. Do not impose a methodology, CI provider or developer environment.
Keep production credentials out; never describe host-user access as sandboxed.

## Agent readiness (the environment makes the agent effective)

Mechanical feedback beats agent memory: change -> check -> diagnostic -> correction -> recheck.
A score or configured tool alone is not readiness. Honour the agreed threshold, prove applicable
critical loops and controls, and retain the full aggregate/CI backstop and independent review.
Prompts, skills and docs are soft guidance, not mechanical enforcement.

## Operating procedures — load on demand

Do not preload every manual. Read the applicable procedure completely before its operation;
stop if it is missing rather than improvising. Reuse guidance already read while unchanged.

| Before this operation | Read |
| --- | --- |
| VCS commands, stage writes or closure recommendations | `_bmad/custom/jj-vcs.md` |
| Approved implementation and its checks only | `_bmad/custom/instructions/implementation.md`; follow its stop conditions and full-manual fallback |
| Contract planning, approval, independent test design/review or revision | `_bmad/custom/story-contract.md` |
| Linear kickoff, activation, publication, status changes or reconciliation | `_bmad/custom/linear-workflow.md` |
| AR setup/reassessment, or auditing/changing the guardrail design | `_bmad/custom/project-guidance.md` |
| Running/redesigning AR itself | `_bmad/custom/agent-readiness-workflow.md` |

These are loading boundaries, not exemptions: every existing gate and lifecycle step still applies.
