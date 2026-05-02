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

## First-session R&D output

In the first session of an R&D request, before any implementation or benchmark,
record:

- explicit mode choice
- target technology in one sentence
- intended use
- capability map
- maturity level for every capability
- smallest blocking capability
- one test design for that capability
- ledger rows that mark whole-technology benchmarks as blocked until upstream
  exits fire

The first session must not run an integrated benchmark, large backtest, or
whole-technology promotion unless this map already exists and shows the
benchmark capability is unblocked.

For financial ML / return-prediction R&D, do not accept a capability map unless
it separates at least:

- prediction task definition
- data availability and point-in-time alignment
- feature or embedding generation
- leakage controls
- baseline model
- validation protocol
- economic / backtest integration
- robustness / promotion gate

A row such as "use model X to predict returns" is too large and must be split.

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
