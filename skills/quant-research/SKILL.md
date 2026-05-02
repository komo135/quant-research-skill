---
name: quant-research
description: Use for quantitative-finance, algorithmic-trading, or financial time-series research. Supports two modes: R&D for establishing a technology by decomposing it into small technical capabilities with explicit maturity/exit criteria, and Pure Research for slow, literature-grounded research that prioritizes research-state updates, failure analysis, competing explanations, and reproducibility over fast conclusions. Use for alpha factors, backtests, return prediction, regime detection, execution, portfolio construction, and financial ML.
---

# Quant Research

A protocol skill for agent-driven technical research in quantitative finance.
The primary job is not to produce quick answers. The job is to keep the
research state clean, make uncertainty explicit, and move the investigation
forward by the smallest defensible step.

## Prime Directive

Prefer a precise unresolved state over a shallow conclusion.

No experiment is complete until it changes the research state. A result may
change the state by confirming, weakening, splitting, merging, parking, or
deleting a question / hypothesis / explanation. Merely appending another
verdict or another decision log entry is not progress.

## First Decision: Research Mode

Before designing any Purpose, notebook, hypothesis, model, or backtest, choose
one mode and follow its reference:

| Mode | Use when | Required reference |
|---|---|---|
| **R&D / technology establishment** | The goal is to establish a technology, capability, pipeline, model class, validation method, or deployable research technique | `references/research_modes.md` and `references/technology_decomposition.md` |
| **Pure Research** | The goal is to understand a phenomenon, answer a research question, or produce knowledge in a paper-like sense | `references/research_modes.md` and `references/pure_research_protocol.md` |

If the request mixes both, split it. R&D can consume Pure Research findings,
and Pure Research can study a technical artifact, but one active work unit must
have one dominant mode.

## R&D Mode

R&D mode exists to establish a technology. Do not start by inventing a large
hypothesis about the whole target. Decompose the target into small technical
capabilities and knowledge prerequisites first.

Required sequence:

1. Write the target technology in one sentence.
2. Decompose it into sub-capabilities, knowledge gaps, dependencies, and
   interfaces.
3. Assign a maturity level to each sub-capability using the project-local TRL
   scale in `references/technology_decomposition.md`.
4. Select the smallest blocking capability.
5. Design one test whose success and failure both teach something about that
   capability.
6. After the test, update the technology map: maturity changed / dependency
   changed / capability split / capability merged / blocked.

Do not promote a whole technology because one component worked. Do not keep
testing a component after its exit criteria have fired.

## Pure Research Mode

Pure Research mode exists to reduce ignorance, not to answer quickly.
The first session usually should not end with a supported conclusion.
It should end with a better research state.

Required sequence:

1. Survey prior work, including the user's own prior notebooks and decisions.
2. Define the research question and what is currently unknown.
3. Record competing explanations before running a test.
4. Run the smallest discriminating trial.
5. Analyze why the result landed where it did, especially when the hypothesis
   failed.
6. Update the research state ledger before proposing the next step.

The normal outcome of a failed hypothesis is a better explanation set, not a
new hypothesis pile. Read `references/pure_research_protocol.md` before
starting, and `references/failure_analysis.md` before interpreting a miss.

## Lightweight Hypothesis Quality Management

Hypothesis management is a pruning system, not an accumulation system. Read
`references/hypothesis_quality.md` before adding or running any hypothesis.

Every hypothesis / experiment passes four lightweight gates:

1. **Entry gate** — What live question, capability, or explanation does this
   test update? If none, do not run it.
2. **Design gate** — What does success distinguish, and what does failure
   distinguish? If failure teaches nothing, redesign.
3. **Interpretation gate** — What can be said directly from the result, what
   remains ambiguous, and which competing explanations became weaker?
4. **State update gate** — Which ledger rows become active, resolved, rejected,
   merged, stale, or parked?

Heavy review is reserved for promotion moments:

- declaring a claim `supported`
- external sharing, paper writing, or deployment recommendation
- closing a research line
- making a large project-direction decision

At those moments, run the relevant bug-review / robustness /
`experiment-review` gates. During ordinary exploration, do not bury the
research under review bureaucracy that does not change the state.

## Required Ledgers

Use the project templates, but treat them as active state surfaces:

- `research_state.md` — questions, explanations, capabilities, and claims by
  status (`active`, `resolved`, `rejected`, `merged`, `stale`, `parked`)
- `hypotheses.md` — only hypotheses that pass the entry gate; rows may be
  downgraded, merged, or marked stale
- `decisions.md` — only durable decisions and state transitions, not every
  thought the agent had
- `literature/papers.md` and `literature/differentiation.md` — prior work,
  including the user's own earlier research

Before adding a row, check whether an existing row should instead be updated,
merged, or retired.

## Guardrails Against Agent Failure Modes

- Do not write "the result suggests..." unless the observation and at least one
  competing explanation are named.
- Do not use generic explanations such as "noise", "data quality", "sample
  size", or "market regime" as terminal causes. Treat them as labels to
  decompose.
- Do not turn an implementation artifact into the research claim. If masking
  library / model / process names leaves no claim about the world or technique,
  the work is engineering, not research.
- Do not keep a hypothesis alive because work has already been spent on it.
  Mark it `rejected`, `merged`, `stale`, or `parked` when the state warrants it.
- Do not continue after the consumer can decide, the capability exit criteria
  fired, or the next discriminating test belongs to a different question.

## References

Read only what applies:

- `references/research_modes.md` — choosing R&D vs Pure Research
- `references/technology_decomposition.md` — R&D capability map, maturity, exit criteria
- `references/pure_research_protocol.md` — slow research workflow and conclusion discipline
- `references/failure_analysis.md` — deep analysis of failed or ambiguous trials
- `references/hypothesis_quality.md` — lightweight gates and ledger pruning
- `references/research_state.md` — state ledger schema and allowed transitions
- `references/literature_review.md` — prior-work review and differentiation
- `references/time_series_validation.md` — time-series validation when a quantitative test runs
- `references/robustness_battery.md` — robustness checks for promotion gates
- `references/bug_review.md` — correctness review for promotion gates
- `references/modeling_approach.md` — model selection guidance

## Bundled Helper Scripts

| script | purpose |
|---|---|
| `new_project.py` | Initialize a research project folder with the standard layout |
| `new_purpose.py` | Generate a numbered Purpose notebook from the template |
| `aggregate_results.py` | Append rows to `results/results.parquet` and query them |
| `walk_forward.py` | Compute Sharpe distribution over rolling windows |
| `bootstrap_sharpe.py` | Block-bootstrap CI for per-trade Sharpe |
| `psr_dsr.py` | Probabilistic / Deflated Sharpe Ratio |
| `fee_sensitivity.py` | Fee sweep with break-even fee extraction |
| `sensitivity_grid.py` | 2D threshold sensitivity grid |
| `vol_targeted_size.py` | Position sizing with size proportional to inverse volatility |
| `purged_kfold.py` | Purged k-fold CV |
| `leakage_check.py` | Detect look-ahead bias and target leakage |
| `sanity_checks.py` | Programmatic sanity checks used before promotion |
