# Preregistration Policy Design

Date: 2026-05-13
Status: design approved for spec review

## Purpose

This design defines a lightweight preregistration policy for the research skill.
The policy is about preregistration itself: write the plan before the work,
conduct the research or experiment against that plan, disclose material changes,
and produce a readable outcome report.

The design deliberately does not make Pure Research, R&D, workstream labels,
promotion gates, or ledger mechanics the center of the preregistration policy.
Those systems may cite preregistration artifacts, but the preregistration
artifact is a general planning and reporting discipline.

## Source Basis

The policy is based on general preregistration practice, not a fully custom
format.

- COS preregistration guidance: preregistration is a study plan, ideally with
  an analysis plan, written before conducting the work.
- COS "plan, not prison" guidance: reasonable changes are allowed, but they
  must be transparent.
- OSF Prereg Template: the plan is structured around study information, design,
  sampling/data, variables/measures, analysis, and other notes.
- OSF Transparent Changes template: each material change should state what
  changed, why it changed, and how the change may affect study results or
  conclusions.

Local additions are limited to repository operation and report packaging. They
are not claims about what OSF itself requires:

- Markdown is the editable source.
- PDF is the provided report artifact.
- Figures, tables, and attachments live next to the report.

## Non-Goals

- Do not require external registration services.
- Do not require hashes, notarization, or anti-tamper machinery.
- Do not require external tracker run IDs.
- Do not require project-level Pure Research / R&D classification.
- Do not force every local probe into a heavy report package.
- Do not put a generic "value" or justification section in front of the plan.

## Artifact Layout

Preregistration files:

```text
prereg/
  PR_<id>_<slug>.md
```

Outcome report packages:

```text
results/reports/
  RPT_<id>_<slug>/
    report.md
    report.pdf
    figures/
    tables/
    attachments/
```

`report.md` is the editable source. `report.pdf` is the provided report.
Figures and tables included in the PDF should have source files under
`figures/` or `tables/`. Large source data and intermediate artifacts should
not be copied into the report package unless they are small and necessary for
interpretation.

Local paths may appear in `report.md` or a short provenance appendix. They
should not dominate the human-facing report. External tracker run IDs are
optional and only appear when such a tracker is actually used.

## Preregistration Type

Each preregistration declares exactly one preregistration type:

```text
preregistration_type: confirmatory | exploratory
```

This deliberately avoids the OSF term "study type", which refers to designs
such as experiment, observational study, meta-analysis, or other. The filename
format remains the same for both preregistration types. The body template
differs because confirmatory and exploratory work need different controls.

## Shared Preregistration Fields

Both confirmatory and exploratory preregistrations use these shared sections.

### Study Information

Required:

- Title
- Description
- Preregistration type

Optional:

- Authors or responsible agent
- Related prior work
- Notes needed to understand the plan

Rationale: the local OSF Prereg Template reviewed for this design separates
Title, Authors, Description, and Hypotheses under Study Information. This
repository policy keeps Title and Description required because they make the
plan identifiable and understandable. Authors or responsible agent remain
optional because Git history and ordinary project context usually cover
authorship well enough for local research. Authorship metadata may still be
useful, but it is not part of the minimal policy.

### Sampling / Data Plan

Required:

- Existing data status or data collection status
- Data source or collection procedure
- Sample size, data range, or planned observation scope
- Inclusion and exclusion rules

Optional:

- Sample size rationale
- Stopping rule
- Known data access constraints

Rationale: preregistration must make clear what evidence the plan applies to
and what data is in scope.

### Variables / Measures

This section is shared as a heading, but the required content differs by study
type.

For confirmatory work, this section fixes variables that enter the planned
analysis:

- Primary outcome or dependent variable
- Predictors or independent variables
- Covariates, if used
- Manipulated variables, if any
- Measured variables
- Indices or formulas, if any
- Measurement unit and aggregation level when relevant

For exploratory work, this section defines the variable space that may be
inspected:

- Variables or measures to inspect
- Candidate feature families or derived measures
- Allowed transformations
- Variables or measures explicitly out of scope, if any
- Selection or ranking criteria, if relevant

Rationale: both study types need to say what will be observed or generated.
Confirmatory work fixes the analysis variables; exploratory work bounds the
search space.

## Confirmatory Preregistration Template

Confirmatory preregistration is for work where the plan fixes what will be
tested and how the result will be interpreted.

Required sections:

1. Study Information
2. Hypotheses
3. Design Plan
4. Sampling / Data Plan
5. Variables / Measures
6. Analysis Plan
7. Inference / Decision Criteria
8. Data Exclusion / Missing Data Handling
9. Transparent Changes Policy

Optional sections:

- Randomization
- Blinding
- Sample Size Rationale
- Stopping Rule
- Secondary Analyses
- Other Notes

The analysis plan should be specific enough that another reviewer can tell
whether the reported analysis followed the plan. If multiple tests or model
variants are planned, the plan must say how they will be interpreted.

## Exploratory Preregistration Template

Exploratory preregistration is for planned exploration. It does not need to
pretend that hypotheses, model choices, or patterns are fixed in advance.
Instead, it defines the search area, allowable operations, and expected outputs.

Required sections:

1. Study Information
2. Exploratory Objective
3. Exploration Scope
4. Sampling / Data Plan
5. Variables / Measures
6. Allowed Transformations / Procedures
7. Selection or Follow-Up Criteria
8. Expected Outputs
9. Transparent Changes Policy

Optional sections:

- Hypotheses or Expectations
- Constraints / Risks
- Trigger for Future Confirmatory Preregistration
- Other Notes

The expected outputs section is not a reporting plan. It states what kind of
artifact the exploration is expected to produce: a diagnostic map, candidate
explanations, ranked patterns, failure analysis, narrowed question, or a future
confirmatory plan.

## Transparent Changes Policy

Every report package includes a `Transparent Changes` section.

If no material changes occurred, the section may be one sentence:

```text
No material changes from the preregistration.
```

If material changes occurred, each change uses this structure:

```text
### Change <n>: <short name>

- Description of change:
- Rationale:
- Effect on study results or conclusions:
```

The effect statement should be honest about uncertainty. If the change was made
with knowledge of how it would affect the outcome, the report must state that
the affected result has weaker diagnostic value.

Changes are not automatically failures. The policy requires transparent
disclosure, not rigid punishment. When a change makes the original plan no
longer answer the intended question, the report should say so plainly.

## Outcome Report Template

All preregistered work that produces a report uses the same package shape, with
slightly different emphasis by study type.

Required sections:

1. Preregistration Reference
2. Summary
3. Plan-to-Result Table
4. Key Figures / Tables
5. Transparent Changes
6. Scope / Limitations

Optional section:

- Follow-up or next decision, if the report asks the reader to choose one

Confirmatory reports emphasize hypotheses, decision criteria, and whether each
planned analysis was completed.

Exploratory reports emphasize exploration scope, patterns found, diagnostics,
and follow-up decisions.

The plan-to-result table is the main accountability device. It maps each
planned item to its execution status, result, and evidence location.

Suggested columns:

```text
planned_item | executed_as_planned | result_summary | evidence | notes
```

The `evidence` column should point to a figure, table, appendix, or local source
artifact. It should not require readers to understand internal tracker run IDs.

## Report PDF

`report.pdf` is the provided report artifact. It should include the key figures
and tables needed to understand the result without opening raw notebooks or
tracker exports.

The PDF does not need to include every internal path. It may include a short
provenance appendix:

```text
Preregistration: prereg/PR_<id>_<slug>.md
Report source: results/reports/RPT_<id>_<slug>/report.md
Figures: results/reports/RPT_<id>_<slug>/figures/
Tables: results/reports/RPT_<id>_<slug>/tables/
Source data or artifact: <path or citation>
```

External tracker run IDs are omitted unless an external tracker is used and the
ID helps resolve the evidence.

## Implementation Impact

The likely implementation should update only protocol references, templates,
and tests that currently describe preregistration too narrowly.

Expected affected areas:

- `skills/research/references/pure_research/preregistration.md`
- `skills/research/assets/pure_research/preregistration.md.template`
- `skills/research/references/pure_research/pr_workflow.md`
- `skills/research/SKILL.md`
- report-related templates or references, if present
- boundary tests that assert preregistration is confirmatory-only

The implementation should avoid introducing a new state system. The
preregistration policy defines planning and reporting artifacts; other research
state remains owned by existing ledgers and decision logs.

## Test Strategy

Tests should verify the policy shape without over-constraining wording.

Expected checks:

- The corpus no longer says preregistration is confirmatory-only.
- Confirmatory and exploratory preregistration templates exist or are described.
- Transparent Changes requires description, rationale, and effect on results or
  conclusions.
- Report package structure includes `report.md`, `report.pdf`, `figures/`,
  `tables/`, and `attachments/`.
- External tracker run ID is optional, not required.
- The spec does not reintroduce project-level Pure Research / R&D locking.

## Open Design Decisions

No open decisions remain for this spec. Implementation may still choose exact
file names for shared templates if the existing repository structure makes one
location cleaner than another.
