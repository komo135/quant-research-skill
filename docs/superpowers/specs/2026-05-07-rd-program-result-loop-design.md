# R&D Program and Result Loop Design

Date: 2026-05-07
Skill: `quant-research`

## Summary

Add four named protocol concepts to `quant-research` without replacing the
existing Pure Research / R&D split:

1. **Right-Sized Rigor**: rigor increases with research state risk. Routine
   orientation and evidence collection stay lightweight; state transitions,
   handoffs, and promotion claims require stronger gates.
2. **Result-to-Question Loop**: Pure Research turns each result into updated
   questions, explanation weights, and the next discriminating step.
3. **Result-to-Capability Loop**: R&D turns each result into updated
   capability uncertainty, TRL evidence, gate decisions, or re-scope actions.
4. **Research-to-Technology Handoff**: Pure Research claims can be consumed by
   R&D as scoped assumptions, design constraints, capability requirements, or
   cross-project dependencies.

Also introduce **R&D Program** as an optional coordination layer above multiple
child projects. It is not a third research discipline. It coordinates Pure
Research and R&D projects, tracks dependencies and handoff contracts, and reads
child-project gate results. It does not own TRL, A-tier, promotion, or claim
truth.

## Motivation

The current skill correctly separates:

- **R&D**: establish a technical capability.
- **Pure Research**: understand a phenomenon or mechanism.

That split should remain. The problem is that real technical programs often
contain both. For example, a financial ML prediction effort may need:

1. Pure Research to establish where a predictive signal is real, why it exists,
   and under which market conditions it fails.
2. R&D to turn the usable part of that knowledge into a reproducible prediction
   capability.
3. R&D to integrate that capability into sizing, execution, risk, monitoring,
   or production-adjacent systems.

The current protocol can express part of this through `dependent_on_research`,
integration patterns, and maintenance plans, but it lacks a clear parent layer
that says how the child projects relate and when a research finding is ready
to be consumed by technology development.

The current skill also has the right ingredients for proportional rigor:
lightweight routine gates in the README, A0-A5 analysis depth, R&D TRL stages,
and heavy promotion reviews. But these are distributed across files. The skill
needs a named principle that prevents two opposite failures:

- treating every exploratory action like a promotion review,
- treating a state transition or handoff like ordinary exploration.

## Design Goals

- Preserve the existing discipline boundary: Pure Research and R&D remain
  separate child project types with separate ledgers.
- Make the R&D reality explicit: a large R&D effort may include Pure Research
  subprojects when unresolved empirical or causal knowledge blocks technical
  progress.
- Add proportional rigor without weakening promotion gates.
- Make result-driven iteration explicit in both modes.
- Define how Pure Research knowledge becomes R&D input without copying claims
  into the wrong ledger.
- Keep evidence artifacts neutral. Notebooks and result rows remain evidence;
  ledgers and decisions own state transitions.
- Keep the first implementation small enough to review and test.

## Non-Goals

- Do not merge Pure Research and R&D into one ledger.
- Do not create a generalized portfolio-management system.
- Do not require `program_id`, `capability_id`, `core_tech_id`, or TRL fields
  in normal trial notebooks or reusable framework APIs.
- Do not let Program re-score A-tier, TRL, or promotion status.
- Do not change the meaning of `supported`, `matured`, `established`, or
  `promoted`.
- Do not add a heavy scaffold until the markdown protocol proves useful.

## Proposed Model

### Layer 0: R&D Program

An R&D Program is an optional coordination layer for a goal that cannot be
honestly represented as one project. It contains child projects and their
dependency or handoff relationships.

Example:

```text
R&D Program: Financial ML prediction technology for decision systems

├─ Pure Research project:
│  Which predictive signals survive after leakage, regime, and cost checks?
│
├─ R&D project:
│  Establish a reproducible prediction capability from the supported signal.
│
└─ R&D project:
   Integrate predictions into sizing / execution / risk workflow.
```

The Program owns:

- child project list,
- dependency graph,
- handoff contracts,
- sequencing decisions,
- current aggregate status,
- rationale for opening, parking, or closing child projects.

The Program does not own:

- capability maturity,
- explanation support,
- A-tier or TRL reassessment,
- promotion of a child project,
- notebook-level evidence interpretation.

The Program must also avoid project-instance facts that belong in child
projects: active symbols, tuned parameters, current PnL, selected models,
candidate features, and concrete experiment conclusions. If a Program needs to
refer to those facts, it cites the child project's evidence artifact or ledger
entry instead of copying the fact into the Program map.

### Layer 1: Child Projects

Child projects remain one of the two existing disciplines:

- Pure Research child projects use `prfaq.md`, `prereg/`, and
  `explanation_ledger.md`.
- R&D child projects use `charter.md` and `capability_map.md`.

Child projects continue to be promoted, killed, parked, or pivoted under their
own discipline-specific rules.

### Layer 2: Evidence Artifacts

Trial notebooks, result rows, configs, generated reports, scripts, and tracker
runs remain neutral evidence artifacts. They can be cited by a child ledger or
by a Program handoff note, but they never decide state transitions on their own.

## Right-Sized Rigor

Add a named principle to the main skill:

> Rigor is sized to the research state being changed. Exploration can be light;
> state transitions, cross-project handoffs, and promotion claims require
> explicit evidence and review.

### Rigor Levels

| Situation | Required rigor | Reason |
|---|---|---|
| Orientation, scaffold, environment setup | Lightweight notes | No research state changes. |
| Exploratory analysis not cited for a claim | Lightweight run note | Useful context, not promotion evidence. |
| First load-bearing trial design | Medium-high | Design choices may shape future state transitions. |
| Trial interpretation | Analysis tier explicit | Results without analysis remain A0. |
| Pure Research ledger update | Ledger movement + next discriminating step | The question state changed. |
| R&D capability gate decision | Stage-appropriate evidence + gate decision | The capability can advance, hold, recycle, or die. |
| Research-to-Technology handoff | Handoff contract + cited child gate | Another project will depend on the claim or capability. |
| `supported`, `matured`, `established`, `promoted` | Highest rigor | Durable claims and downstream dependency decisions. |

This does not lower existing promotion requirements. It prevents promotion
discipline from leaking backward into all low-risk work.

The following are never relaxed by Right-Sized Rigor:

- A4+ for `supported`, `matured`, `established`, or `promoted`.
- Frozen pre-registration requirements for promotion-cited Pure Research
  trials.
- Frozen charter and kill criteria as R&D decision anchors.
- Reproducibility records for promotion-cited or handoff-cited evidence.
- Process review and conclusion review before durable promotion claims.
- Maintenance plan requirements for `継続改善型` R&D core technologies.

## Result-to-Question Loop

Pure Research already has this loop implicitly in `pr_workflow.md`. The design
renames and clarifies it.

Loop:

1. Observe the result with numerical precision and uncertainty.
2. Decompose candidate explanations.
3. Ask what new or sharper question the result created.
4. Decide whether existing data can answer it through deeper analysis.
5. If existing data cannot answer it, design the next discriminating trial.
6. Update `explanation_ledger.md`:
   - explanation evidence summary,
   - explanation status,
   - question status,
   - `next_discriminating_step`,
   - supported claim only when promotion gates pass.

The key rule remains: push analysis depth on the current trial before opening a
new trial.

## Result-to-Capability Loop

R&D needs the corresponding named loop. It should live in `rd_stages.md`
near the gate decision protocol.

Loop:

1. Observe the result with numerical precision and uncertainty.
2. Ask what technical uncertainty the result changed.
3. Decide whether the result affects:
   - `blocking_uncertainty`,
   - `exit_criteria`,
   - `kill_criteria`,
   - `current_TRL`,
   - capability `Status`,
   - parent K status,
   - dependency or integration path.
4. Decide the stage outcome:
   - Go,
   - Hold,
   - Recycle,
   - Re-scope,
   - Split / merge,
   - Kill.
5. If the result raises a new research question, decide whether it is:
   - a sub-question inside the same capability,
   - a new capability,
   - a new core technology,
   - a Pure Research child project under a Program.
6. Record the transition in `capability_map.md` and `decisions.md`.

R&D uses questions instrumentally. The purpose is not to publish the question's
answer; it is to determine whether the technical capability can be trusted,
modified, integrated, maintained, or killed.

The loop must not permit goalpost shifting. If a result shows that an exit
criterion, kill criterion, threshold, data source, or test design was wrong,
the fix is a dated deviation entry and a prospective re-scope. The old result
is not silently reinterpreted under the new criterion.

When an R&D result creates a Pure Research question, the R&D project does not
update a Pure Research ledger directly. The valid paths are:

- open a secondary Pure Research child project under the Program,
- cite the R&D observation as prior work or motivating evidence,
- pre-register the Pure Research trial before using that observation to support
  a claim.

## Research-to-Technology Handoff

Add a handoff concept that explains how Pure Research outputs become R&D
inputs.

### Handoff Source

A Pure Research child project can hand off only a bounded claim whose status is
clear:

- `supported` claim with A4+ evidence, or
- `rejected` / null finding with A4+ analysis when the negative result is the
  useful input.

The claim must include:

- claim phrasing no stronger than evidence,
- scope conditions,
- failure conditions or untested regions,
- cited trials and reproducibility records,
- promotion or review status.

### Handoff Target

An R&D project consumes the handoff as one or more of:

- design assumption,
- capability requirement,
- `dependent_on_research` entry,
- scope condition,
- risk / kill criterion,
- validation benchmark,
- maintenance trigger.

The R&D project must not copy the Pure Research claim into its own ledger as if
it established the claim. It cites the source project and states how the claim
constrains the technology work.

### Handoff Contract

Each handoff records:

```markdown
## Handoff: <source project> -> <target project>

- Source claim / capability: <id + short phrase>
- Source gate status: <supported / rejected finding / matured / promoted>
- Consumed as: <assumption / requirement / dependency / scope / benchmark>
- Scope imported: <conditions under which the input is valid>
- What is not imported: <untested regions or non-claims>
- Target ledger update: <capability row / charter item / decision entry>
- Revalidation trigger: <when the target must revisit this input>
```

## Program Map

Add a new reference file:

`skills/quant-research/references/program/program_map.md`

The first implementation can define a markdown table, not a script-heavy
system.

Suggested sections:

```markdown
# Program Map - <program name>

## Program Goal

## Child Projects
| project_id | discipline | deliverable | required_gate | status | owner role |
|---|---|---|---|---|---|

## Dependencies
| from_project | to_project | dependency_type | required_gate | handoff_contract | status |
|---|---|---|---|---|---|

## Integration / Handoff Log
| date | source | target | consumed_as | decision | evidence |
|---|---|---|---|---|---|

## Program Decisions
Chronological decisions that affect child sequencing, handoff, parking,
or closure.
```

Allowed `dependency_type` values:

- `research_to_rd`: Pure Research claim consumed by R&D.
- `rd_to_rd`: one R&D capability or project consumed by another R&D project.
- `rd_to_research`: R&D result opens a Pure Research question.
- `shared_infra`: shared code or data infrastructure dependency.
- `integration`: downstream system integration dependency.

Program status should be descriptive, not a new truth claim:

- `active`,
- `blocked`,
- `parked`,
- `handoff-ready`,
- `integration-ready`,
- `closed`.

Program statuses must not reuse `supported`, `matured`, `established`, or
`promoted`. Those terms remain child-ledger and child-project terms only.

## File Impact

### Main Entry

- `skills/quant-research/SKILL.md`
  - Add R&D Program as a coordination layer, not a discipline.
  - Add Right-Sized Rigor after Analysis Depth or near Review.
  - Add a short shared result-loop principle.
  - Link to program reference.

### Shared Reference

- `skills/quant-research/references/shared/result_analysis.md`
  - Clarify that the next discriminating test returns to different state
    objects depending on discipline:
    - Pure Research: Q/E state and `next_discriminating_step`.
    - R&D: capability stage, blocker, TRL, or gate decision.

### Pure Research

- `skills/quant-research/references/pure_research/pr_workflow.md`
  - Rename or annotate the discriminating trial loop as the
    Result-to-Question Loop.
  - Explicitly state that a new R&D handoff is allowed only after the source
    claim's scope and status are clear.

### R&D

- `skills/quant-research/references/rd/rd_stages.md`
  - Add Result-to-Capability Loop near the gate decision protocol.
  - Explain how results update `blocking_uncertainty`, TRL, status, scope, or
    dependency path.

- `skills/quant-research/references/rd/capability_map_schema.md`
  - Expand cross-project dependency language beyond Pure-only dependencies,
    while preserving the rule that Program does not own child state.

### Program

- New: `skills/quant-research/references/program/program_map.md`
  - Define Program purpose, schema, handoff contracts, dependency types,
    lifecycle, and anti-patterns.

### Review

- `skills/quant-research/references/review/process_review.md`
- `skills/quant-research/references/review/conclusion_review.md`

No direct change is required in the first implementation. The existing review
layers continue to review child project process and conclusions. Program
coordination may cite those review outcomes, but it does not replace them.

### README

- `README.md`
  - Add a short explanation that large efforts may use Program coordination
    while child projects remain R&D or Pure Research.
  - Clarify routine gates vs heavy promotion gates under Right-Sized Rigor.

### Assets and Scripts

Initial implementation should not add a script-heavy Program scaffold unless
the markdown protocol feels insufficient. A later follow-up may add:

- `assets/program/program_map.md.template`,
- `scripts/new_program.py`, or
- `scripts/new_project.py --mode program`.

This keeps the first change focused and lowers the risk of overbuilding.

### Not Changed

- Trial templates should not gain mandatory Program metadata.
- Project-instance framework code should not gain Program, TRL, K, or C
  arguments.
- `experiment-review` internals do not need to change in the first slice.
- Existing helper scripts do not need to support `--mode program` in the first
  slice.

## Validation Strategy

### Static Checks

Extend or add tests that protect existing boundaries:

- Protocol docs may mention program and handoff.
- Trial templates must not require `program_id`, `capability_id`,
  `core_tech_id`, TRL, or Program fields.
- Framework code must not require Program metadata.
- Program reference must say it reads child gate results, not re-scores them.

### Documentation Checks

Search for prohibited placeholders in new docs: unfinished-work markers,
repeated question marks, and unreplaced template braces.

Check for terminology consistency:

- `supported` remains Pure Research claim status.
- `matured` remains capability status.
- `established` remains core technology status.
- `promoted` remains R&D project status.
- Program statuses must not replace these terms.

Run the existing project-boundary tests and extend them if needed:

- `pytest tests/test_project_boundaries.py`

Expected preserved behavior:

- protocol references can define Program and handoff rules,
- evidence artifacts remain neutral,
- framework code and templates do not require protocol-state IDs.

### Scenario Tests

Use three documentation scenarios during review:

1. **Financial ML prediction program**
   - Pure Research establishes scoped signal validity.
   - R&D consumes the claim to build prediction capability.
   - R&D integrates prediction into sizing/risk workflow.

2. **R&D result opens a Pure Research question**
   - A capability fails in a way that cannot be resolved inside the capability.
   - Program opens a Pure Research child project.
   - Original R&D capability is blocked or re-scoped.

3. **No Program needed**
   - A narrow R&D project with no child research dependency continues to use
     only charter and capability map.
   - The new Program layer stays optional.

## Risks and Mitigations

### Risk: Program becomes a hidden mega-ledger

Mitigation: Program may coordinate dependencies and handoffs only. Child
ledgers remain authoritative for claims and capability state.

### Risk: R&D becomes too research-paper-like

Mitigation: Right-Sized Rigor explicitly permits lightweight exploration and
stage-appropriate evidence. Maximum rigor is reserved for transitions,
handoffs, and promotion.

### Risk: Pure Research claims are over-consumed by R&D

Mitigation: Handoff contracts require imported scope and "what is not
imported". R&D must cite the source claim and state how it constrains the
technology, not restate it as an R&D finding.

### Risk: Program metadata leaks into notebooks and APIs

Mitigation: Boundary tests enforce that evidence artifacts and framework code
do not require Program or capability metadata.

### Risk: Too much scaffold too early

Mitigation: First implementation adds references and documentation. Program
templates or scripts are deferred until the markdown protocol proves useful.

## Recommended Implementation Slice

Implement in two small passes.

### Pass 1: Protocol Concepts

- Add Right-Sized Rigor and Program layer language to `SKILL.md`.
- Add Result-to-Question wording to Pure Research workflow.
- Add Result-to-Capability wording to R&D stages.
- Add shared result-analysis routing language.
- Add README summary.

This pass should be mostly documentation and should not touch scripts.

### Pass 2: Program Reference and Boundary Tests

- Add `references/program/program_map.md`.
- Add or extend boundary tests that prevent Program metadata from becoming
  required in notebooks or framework APIs.
- Lightly update cross-project dependency language in
  `capability_map_schema.md`.

No scaffold script is required in this slice.

## Implementation Defaults

These decisions are fixed for the first implementation slice:

- `program_map.md` starts as a reference-only protocol document.
- No `new_program.py` script is added in the first slice.
- No `new_project.py --mode program` scaffold is added in the first slice.
- Existing `dependent_on_research` language is clarified, but no new required
  schema field is introduced in the first slice.
- Program metadata remains optional and external to trial artifacts.

Future work may add a template or script only after the reference protocol is
used in at least one dry-run scenario and the missing automation is concrete.
