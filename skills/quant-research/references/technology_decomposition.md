# technology_decomposition.md

R&D mode turns a large technology goal into small, testable capabilities.

## Technology map

Write this map before any implementation:

```markdown
## Target technology
[One sentence: what technical capability should exist.]

## Intended use
[Who uses it, for what decision or workflow.]

## Capability decomposition
| ID | Capability / knowledge unit | Depends on | Current maturity | Exit criteria | Blocking uncertainty | Status |
|---|---|---|---|---|---|---|
| C1 | ... | ... | TRL-1 | ... | ... | active |
```

Capability size rule: one capability should be small enough that one test can
change its maturity or split it. If a capability requires several unrelated
tests, split it before testing.

## Project-local maturity scale

This is adapted from TRL thinking, but tuned for agent-run research.

| Level | Meaning | Exit evidence |
|---|---|---|
| TRL-0 | Name only; not yet decomposed | Capability has owner, boundary, dependency list |
| TRL-1 | Principle or rationale exists | Prior work or first-principles argument supports plausibility |
| TRL-2 | Toy proof of concept | Works on synthetic / toy data for the intended property |
| TRL-3 | Critical function demonstrated | One real-data or realistic-environment test isolates the key function |
| TRL-4 | Component validated | Component works with realistic inputs and known failure modes |
| TRL-5 | Integrated prototype | Interacts with neighboring components without breaking assumptions |
| TRL-6 | Operationally relevant prototype | Demonstrated on representative workload / data / cost constraints |
| TRL-7+ | Production readiness | Outside this research skill unless the user explicitly asks for engineering handoff |

Do not skip levels by rhetoric. A strong benchmark result can move one
capability; it does not mature the entire technology.

## Test design

For each capability test, write:

- Capability ID
- Current maturity
- What success would change
- What failure would change
- Which dependency or uncertainty the test distinguishes
- Exit criteria
- Next action if success
- Next action if failure

Failure must teach something. If failure would only produce "try another
parameter", the test is too broad or poorly framed.

## State updates

After the test, update the map:

- `active`: still being worked
- `resolved`: exit criteria fired
- `blocked`: named dependency prevents progress
- `split`: capability was too broad and has been decomposed
- `merged`: duplicate of another capability
- `stale`: no longer relevant after a design change

Do not add a new capability without checking whether an existing one should be
split, merged, or retired.
