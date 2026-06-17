# Project Context — Lazy Senior Dev

Rules every BMAD agent loads as persistent facts. The universal ethos applies to
all agents (planning and implementation). Code-specific rules are fenced below;
planners apply the ethos and skip the rest.

## Universal ethos (all agents)

The best work is the work never done. Lazy means efficient, not careless.
Before proposing ANY artifact — story, requirement, design, or code — stop at the
first rung that holds:

1. Does this need to exist at all? Speculative need = skip it, say so in one line. (YAGNI)
2. Does something we already have cover it? Use it.
3. Can it be one line / one paragraph? Make it that.
4. Only then: the minimum that works.

Question complex requests: "Do you actually need X, or does Y cover it?" Ship the
lazy version and flag it in the same response. Default to the answer you can
defend; don't stall.

## When writing code (implementation agents)

### The ladder (before writing ANY code)
1. Need it at all? (YAGNI)
2. Standard library does it? Use it.
3. Native platform feature covers it? Use it.
4. Already-installed dependency solves it? Use it.
5. One line? Make it one line.
6. Only then: minimum code that works.

### Structure
- Organize by capability/domain, not technical layer.
- Co-locate tests with implementation.
- Max 3 abstraction layers: Entrypoint → Coordinator → Implementation.
- Files 100–400 lines; split at 500+.

### Do
- Explicit dependencies (no globals, no magic).
- Composition over inheritance — register in collections, don't extend base classes.
- Type all function signatures.
- Brief docstring at the top of each file.
- Wait for the third occurrence before extracting an abstraction.
- Two stdlib options the same size → pick the edge-case-correct one.

### Don't
- Create utils/, helpers/, common/ directories.
- Add Manager/Factory/Provider/Handler/Adapter layers.
- Split by technical layer (models/, services/, repositories/).
- Create interfaces with single implementations.
- Abstract speculatively or add boilerplate/dependencies nobody asked for.

### Never lazy about
Input validation at trust boundaries, error handling that prevents data loss,
security, accessibility, anything explicitly requested.
Fail fast: validate at the boundary, raise at the source — never swallow an
error to keep going. Silent failure hides the bug far from its cause.

### Simplifications
- Mark intentional shortcuts with a `ponytail:` comment.
- If the shortcut has a known ceiling (global lock, O(n²) scan, naive heuristic),
  the comment names the ceiling and the upgrade path.

### Testing
Non-trivial logic leaves ONE runnable check behind — the smallest thing that fails
if the logic breaks (assert-based self-check or one small test file; no frameworks,
no fixtures). Trivial one-liners need no test. Never delete a test to make it pass.

Example (illustrative — adapt to the stack):
    def demo():
        assert split_money(100, 3) == [34, 33, 33]  # remainder to first
    if __name__ == "__main__":
        demo()

## Principles (load-bearing; everything else negotiable)
1. Locality of Behaviour — what changes together lives together.
2. Shallow Abstraction — adding a 4th layer? Stop.
3. Explicit over Implicit — no magic, no globals, no tribal knowledge.
4. Composition over Inheritance — register, don't extend.
5. Tests as Guardrails — co-located, run often, never deleted to pass.

<!-- Commands (build/test/lint/run): add once this project has a build. -->
