# R&D Plan File Schema

## Purpose

`plans/<plan_id>_<slug>.md` is the agent's working state for one R&D investigation. It contains the plan, the actual execution narrative, the comparison, the claims, and the decision. It is the durable record across sessions.

This is **not** a write-once preregistration document. It is a live narrative. Git history is the time-anchor — the initial plan commit is the "preregistration" moment; subsequent commits show the evolution and are themselves auditable.

Why one file instead of separate prereg + plan: separate files would impose redundant maintenance with no additional discipline. Git already proves the plan existed before the result. The agent's job is to keep the document honest, not to keep two synchronized documents.

## File template

```markdown
---
plan_id: <id>
slug: <short-kebab-case-slug>
category: basic_research | applied_research | experimental_development
mode: exploratory | confirmatory | milestone
status: planned | in_progress | completed | parked | killed | replaced
created_at: YYYY-MM-DD
created_commit: <git sha — auto-filled by new_plan.py>
last_updated: YYYY-MM-DD
---

# <Plan title>

## Question / Objective
<One paragraph stating what this plan investigates or builds.>

## Plan
<Mode-specific structure — see below.>

## Actual execution
<What was done. Updated as runs accumulate.>

## Planned vs Actual
<Differences between plan and execution, with reasoning. Empty if no deviation.>

## Claims
<Load-bearing claims using the schema in claim_structure.md.>

## Decision
<One of NEXT_STEP / REFINE / ADJACENT / PARK / CLOSE — see iteration_loop.md.>

## References
- Runs: experiments/<plan_id>_<slug>/runs/...
- Related plans: <other plan IDs and their relationship>
- Related literature: <see literature/papers.md entries>
```

## Plan section by mode

### Mode: exploratory

Fix the boundaries, not the prediction. From Dirnagl (PLOS Biology 2020): exploratory work commits to the *space of investigation*, not to a point hypothesis.

```markdown
### Variable space
- <variable 1>: <range, justification>
- <variable 2>: ...

### Allowed transformations / procedures
- <list of analyses the agent may apply during exploration>
- <out-of-scope analyses, if useful to call out>

### Selection / follow-up criteria
- <what observations would trigger a deeper look>
- <what would trigger PARK or CLOSE>

### Expected output type
- <type of artifact: phenomenon description, refined question, characterized baseline, failure-mode catalog, theoretical insight>

### Out of scope
- <explicit list of things not to chase, to prevent scope creep>
```

### Mode: confirmatory

Fix the hypothesis, metric, baseline, decision threshold.

```markdown
### Hypothesis
- <one sentence statement of the prediction>

### Primary metric
- <metric name, computation, units>

### Baseline(s)
- <baseline name>: <description, source, version>
- <baseline 2>: ...

### Decision threshold
- <quantitative threshold for "hypothesis supported">
- <observation that would lead to rejection>

### Datasets / evaluation setup
- <specific datasets, splits, evaluation protocol>

### Compute / sample budget
- <budget envelope>

### Ablations planned
- <which components will be tested for individual contribution>
```

### Mode: milestone

Fix the acceptance criteria.

```markdown
### Functional milestones
- <feature 1>: <acceptance criterion>
- <feature 2>: ...

### Performance milestones
- <metric>: <threshold under stated conditions>

### Acceptance tests
- <list of scenarios the system must pass>

### Out of scope
- <explicit list of functionality not in this iteration>

### Compute / time budget
- <budget>
```

## Actual execution section

Updated after work runs:

```markdown
### Runs
- <run_id>: <one-line summary, link to runs/<run_id>/>
- <run_id>: ...

### Methodology used
<Substantive description of what was done. Methods reproducibility — enough for someone else to re-implement based on this text. NOT env locks or commit hashes — those live in the run artifacts.>

### Observations
<What was seen. Reference figures/tables in reports/<id>/figures/ if reports have been started.>
```

The Methodology subsection must be specific enough that a reader could re-implement. "We trained a Transformer" is not a methodology description. The architecture, training procedure, evaluation protocol, and data setup must be specific.

## Planned vs Actual section

If anything deviated from the plan, record it here. Deviations are not failures — undocumented deviations are.

```markdown
### Change 1: <short name>
- Description: <what changed>
- Rationale: <why>
- Effect on conclusions: <does this weaken any claim's diagnostic value? say so plainly>
```

If no deviation: `No material deviation from plan.`

Material vs immaterial deviation: a change that could affect the interpretation of results is material. Fixing a typo in a script is not. Changing the evaluation metric is. Changing the random seed is usually not material; changing it after seeing a result that depends on the seed is material.

## Claims section

Use the schema from `claim_structure.md`. Each load-bearing claim is one YAML-like record:

```yaml
- claim: ...
  evidence: ...
  alternatives_not_excluded: [...]
  conditions_tested: ...
  conditions_not_tested: [...]
```

`scripts/check_claims.py` verifies the structure. Run it before changing the plan's status from `in_progress` to anything else, and before drafting a report.

## Amendments section (for REFINE)

When the iteration loop selects `REFINE`, **do not rewrite the original Plan section**. The original Plan + its `created_commit` are the time-anchored historical record; rewriting them destroys the audit trail and is detectable in git diff.

Instead, append an Amendments section at the bottom of the plan file. The latest amendment becomes the "current" plan state; the original Plan section remains as historical context.

```markdown
## Amendments

### Amendment 1 (YYYY-MM-DD, commit <sha>)
- From question / scope: <original>
- To question / scope: <refined>
- Trigger: <evidence that prompted the refinement>
- What changes:
  - <e.g., new hypothesis>
  - <e.g., new metric / threshold>
  - <e.g., new variable range>
- Prior runs: <which carry over as evidence under the refined plan; which become exploratory only>
- Estimated cost / budget: <how much work the refined plan requires>
```

Amendments stack. If a second REFINE happens, append "Amendment 2" — do not edit Amendment 1. Each amendment is itself a time-anchored record (the commit creating it is the time-stamp).

Use the amendment pattern rather than rewriting because:
- For small refinements (a 12-run study getting a 9-run follow-up sweep), rewriting the whole Plan section is friction tax with no audit value.
- The original Plan + Amendment 1 + Amendment 2 chain reads as the evolution of the question — which is the honest research record.
- A reviewer can compare Amendment N to original Plan via git diff or by reading both sections.

When the amendment changes are large enough that "amendment" feels like a stretch (the question is fundamentally different, the category changes, the mode changes), it is no longer REFINE — it is ADJACENT (open a new plan) or CLOSE: replaced.

## Decision section

Use exactly one of:

```markdown
### NEXT_STEP
<one sentence describing the next planned step>
```

```markdown
### REFINE
- From: <original question>
- To: <refined question>
- Trigger: