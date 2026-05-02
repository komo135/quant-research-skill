# quant-research-skill

A Claude Code and Codex plugin for **agent-driven quantitative finance
research**. The `quant-research` skill now starts by choosing one of two modes:

- **R&D / technology establishment** — for establishing a technical capability.
  The skill decomposes the target technology into small capabilities, assigns a
  maturity level, and tests the smallest blocking capability with explicit exit
  criteria.
- **Pure Research** — for paper-like research and phenomenon understanding.
  The skill prioritizes prior-work review, competing explanations, failed-trial
  analysis, and research-state updates over fast conclusions.

The core rule is: **prefer a precise unresolved state over a shallow
conclusion**. Hypothesis quality management is intentionally lighter and more
stateful than the previous protocol. A trial is complete only when it updates
the research state: active / resolved / rejected / merged / stale / parked.

The separate `experiment-review` skill remains available for promotion moments:
declaring a claim `supported`, external sharing, deployment recommendation,
closing a research line, or making a major direction decision.

The skills cover both **mathematical-model research** (Ornstein–Uhlenbeck,
state-space, PCA, factor models, regression) and **machine-learning research**
(classical ML, deep learning, reinforcement learning, foundation models like
Chronos / TimesFM / Moirai) — the lifecycle and the review layers are the same;
only the modeling step differs.

> Writing a paper is not the goal of this plugin. Producing research that
> *could* be written up as a paper is.

## Who this is for

You, if all of the following are true:

- You drive a research workflow with Claude Code (or another Claude Agent SDK
  harness) rather than typing every cell yourself.
- You work on alpha factors, return prediction, regime detection, optimal
  execution, or any data → model → evaluation loop on financial time series.
- You have been burned by — or want to never be burned by — leakage,
  whole-period normalization, single-instrument generalization claims,
  test-set reuse, missing baselines, or unverified Sharpe.
- You are willing to use **marimo** as the notebook format. (See below for why.)

This plugin is **not** for:

- Pure implementation tasks (CRUD, refactors, bug fixes that have nothing to
  do with research).
- Notebook stages that have no claim to review yet (orientation, brainstorm).
  The review skill explicitly opts out at that stage.
- Projects that need a working backtest *engine* — this plugin is a research
  protocol, not a backtest engine. Pair it with whatever engine you prefer
  (your own pandas / numpy code, vectorbt, NautilusTrader, etc.).

## Why marimo, not Jupyter

marimo is a deliberate choice, not a default.

- **Notebooks are stored as `.py`.** Agents Read / Edit them as ordinary
  source files. `.ipynb` JSON + embedded outputs are noise that hurts agent
  comprehension and turns every diff into a metadata war.
- **Reactive dataflow graph.** A single global cannot be redefined across
  cells. This is mildly annoying for humans and an outright guardrail for
  agents — the notebook *cannot* enter the hidden-state regimes where most
  Jupyter-style leaks live.
- **`mo.ui` widgets.** The skill requires "the notebook must work as a
  self-contained communication artifact": prose interpretation, per-figure
  observations, at least one drill-down widget. marimo makes this natural;
  the equivalent in Jupyter (ipywidgets / voila) is heavyweight.
- **One cell = one fit / one evaluation.** This rule is enforceable in
  marimo because the dataflow graph already prevents cell-internal looping
  over models × features × targets without redefinition. The same rule in
  Jupyter is purely advisory and routinely violated.

If you want Jupyter, you will be fighting the skill, not using it.

## What you get, in one paragraph

Start a project → the skill scaffolds a folder with `research_state.md`,
`hypotheses.md`, `literature/papers.md`, `literature/differentiation.md`,
`purposes/`, `results/`, `decisions.md`, and `reproducibility/`. Work begins by
choosing R&D or Pure Research. R&D work builds a technology map and advances one
small capability at a time. Pure Research work builds a research-state map,
lists competing explanations, runs the smallest discriminating trial, and treats
misses / ambiguity as first-class evidence. Hypotheses are admitted only when
both success and failure update a named state row. Heavy review remains
available, but it is no longer the default unit of quality; ordinary quality is
managed by entry, design, interpretation, and state-update gates.

## Quality management

Routine quality management is handled by four lightweight gates:

| Gate | Question |
|---|---|
| Entry | What live question, explanation, or capability does this update? |
| Design | What does success distinguish, and what does failure distinguish? |
| Interpretation | What can be said directly, and what competing explanations remain? |
| State update | What becomes active / resolved / rejected / merged / stale / parked? |

Heavy review still exists, but only for promotion moments: supported-claim
promotion, external sharing, deployment recommendation, research-line closure,
or major direction decisions.

## Repository layout

```
quant-research-skill/
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── .codex-plugin/
│   └── plugin.json
├── skills/
│   ├── quant-research/
│   │   ├── SKILL.md           # entry point — research lifecycle
│   │   ├── references/        # protocols, loaded on demand
│   │   ├── scripts/           # reusable helpers (walk-forward, PSR, …)
│   │   └── assets/            # notebook + project templates
│   └── experiment-review/
│       ├── SKILL.md           # entry point — claim-warrant review
│       ├── references/        # 8 dimensions, severity rubric, dispatch protocol
│       └── assets/            # review report template
├── README.md
└── LICENSE
```

## Installation

### Claude Code: from a Git repository

```text
/plugin marketplace add https://github.com/komo135/quant-research-skill
/plugin install quant-research@quant-research-skill
```

After installation the skills are referenced as
`/quant-research:quant-research` and `/quant-research:experiment-review`.

### Claude Code: local development

```bash
claude --plugin-dir /path/to/quant-research-skill
```

### Codex: local plugin

This repository includes a Codex manifest at `.codex-plugin/plugin.json`.
For local Codex installation, place the checkout at `~/plugins/quant-research`,
add a local marketplace root to `~/.codex/config.toml`, and enable
`quant-research@local`.

The installed Codex skills are exposed as `quant-research` and
`experiment-review`.

## Usage flow

A typical research session:

1. **Bootstrap a project.** The skill scaffolds `research_state.md`,
   `hypotheses.md`, `decisions.md`, literature files, notebooks, results, and
   reproducibility files.
2. **Choose mode.** Write R&D or Pure Research in `research_state.md`.
3. **Orient before testing.** Read prior work and the user's prior decisions.
4. **Admit only useful hypotheses.** Add a hypothesis only if success and
   failure both update a named state row.
5. **Run the smallest discriminating trial.** Keep data splits and sanity checks
   visible.
6. **Analyze misses deeply.** Failed and ambiguous results must weaken, split,
   or retire explanations rather than trigger a pile of new variants.
7. **Update state before adding work.** Update `research_state.md`,
   `hypotheses.md`, and `decisions.md`; merge or retire rows before adding new
   ones.
8. **Promote only when warranted.** Run robustness / bug-review /
   `experiment-review` when a result will become a supported claim or drive a
   high-impact decision.

## Bundled helper scripts

| script | purpose |
|---|---|
| `new_project.py` | Initialize a research project folder with the standard layout |
| `new_purpose.py` | Generate a numbered Purpose notebook (one parent thesis per file) from the template |
| `aggregate_results.py` | Append rows to `results/results.parquet` and query them |
| `walk_forward.py` | Compute Sharpe distribution over rolling windows |
| `bootstrap_sharpe.py` | Block-bootstrap CI for per-trade Sharpe |
| `psr_dsr.py` | Probabilistic / Deflated Sharpe Ratio |
| `fee_sensitivity.py` | Fee sweep with break-even fee extraction |
| `sensitivity_grid.py` | 2D threshold sensitivity grid |
| `vol_targeted_size.py` | Position sizing with size ∝ 1/volatility |
| `purged_kfold.py` | Purged k-fold CV (López de Prado) |
| `leakage_check.py` | Detect look-ahead bias and target leakage in features |
| `sanity_checks.py` | Programmatic bug-detection helpers used by the bug-review layer |

## A note on tone

The skill files use language like "MANDATORY", "protocol violation",
"downgrades to preliminary screening". This is intentional and applies
*within* the protocol — the layers exist precisely because the typical
failure mode is skipping them. You, the user, are always free to override
any of it: superpowers / project conventions take precedence over the
plugin. The strong tone is a guardrail for the agent, not a verdict on
your taste.

## References

The skill leans on a small number of well-known references:

- López de Prado, *Advances in Financial Machine Learning* (2018) — purged
  k-fold, embargo, CPCV, backtest overfitting.
- Bailey & López de Prado, *The Probabilistic Sharpe Ratio* (2012) and
  *The Deflated Sharpe Ratio* (2014).
- Bailey, Borwein, López de Prado, Zhu, *Pseudo-Mathematics and Financial
  Charlatanism* (2014).
- Politis & Romano, *Block Bootstrap* (1994).
- Avellaneda & Lee, *Statistical Arbitrage in the U.S. Equities Market*
  (Quantitative Finance, 2010) — reference example for math-driven
  research.
- Song, *Cross-Context Review: Improving LLM Output Quality by Separating
  Production and Review Sessions* (arxiv:2603.12123, 2026) — empirical
  basis for the adversarial reviewer's deliberately minimum context
  bundle. Reports +4.7 F1 for code-review specifically (CCR 40.7 % vs
  same-session self-review 36.0 %, Table 5).

## Status

- Version 0.16.0
- Two skills, two review layers, both required as co-gate.
- Notebook unit is one Purpose (open-ended investigation); per-Hypothesis
  verdict gates and result rows.
- R-side R&D protocol: Stage 0 (pre-hypothesis exploration), Step 1.5
  (hypothesis generation pathways), why-why result-analysis gate before
  every per-H verdict (rooted in observed result pattern; every level
  observation-pinned to a cited table / value and assigned a diagnostic
  role; prose plausibility ladders are rejected and the chain stops at
  the first uncomputable level), cross-H synthesis, exhaustion trigger,
  novelty / knowledge-advance gate.
- Adversarial-reviewer mechanism backed by Song (2026); see *References*.

### Changelog

**0.17.0** — Major research-state redesign. This is a structural rewrite of
`quant-research`, not a small protocol patch.

- **Two research modes.** The skill now starts by choosing either R&D / technology
  establishment or Pure Research. R&D decomposes a target technology into small
  capabilities with maturity levels, dependencies, and exit criteria. Pure
  Research treats the deliverable as a research-state update: prior work,
  competing explanations, failed-trial analysis, and the next discriminating
  question.
- **Research state as the central artifact.** New projects now include
  `research_state.md`, a compact map of active questions, explanations, R&D
  capabilities, claims, and retired / merged / stale rows. A trial is not
  complete until it changes this state.
- **Hypothesis quality rebuilt around pruning.** Routine hypothesis management
  now uses four lightweight gates: entry, design, interpretation, and state
  update. Hypotheses must name what state row changes under both success and
  failure. Parameter tweaks, threshold variants, lower-fee reruns, and
  same-family signal variants default to `merged` / robustness work, not new H
  rows.
- **Pure Research conclusion discipline.** First-session Pure Research cannot
  end with `supported` unless it is a bounded replication / verification task
  with all evidence already present and promotion gates run. Same-day conclusion
  pressure is explicitly reframed as a research-state update, not weaker evidence
  standards.
- **Failure analysis strengthened.** `failure_analysis.md` now requires generic
  labels such as noise, regime, cost, sample size, overfitting, or data quality
  to be decomposed into observable sub-claims. Cost-sensitive alpha failures get
  explicit gross-edge, turnover, holding-period, break-even fee, slippage, and
  regime-dependence checks before any lower-fee or narrower-regime follow-up.
- **Heavy review moved to promotion moments.** Full bug-review, robustness, and
  `experiment-review` are no longer the default for every exploratory trial.
  They are mandatory for supported-claim promotion, external sharing, deployment
  decisions, research-line closure, or major direction changes. Good headline
  metrics make a claim eligible for review; they do not establish `supported`.
- **R&D shortcuts blocked.** A whole technology cannot be marked `supported`
  because one integrated backtest looks good. For financial ML / return
  prediction, the capability map must separate task definition, point-in-time
  data, feature / embedding generation, leakage controls, baselines, validation,
  economic integration, and promotion gates.
- **Templates rebuilt.** `README.md.template`, `research_state.md.template`,
  `hypotheses.md.template`, `decisions.md.template`, and `purpose.py.template`
  now reflect the state-led workflow. `new_project.py` creates
  `research_state.md` and points the user to fill it before adding hypotheses.
- **Pressure-tested with five adversarial scenarios.** Multi-agent read-only
  pressure tests covered R&D big-backtest pressure, Pure Research same-day
  conclusion pressure, fee/regime failure analysis, RSI threshold hypothesis
  proliferation, and premature `supported` promotion from good metrics. The
  resulting hardening patches are included in this release.

**0.16.0** — Made the why-why chain a pre-verdict result-analysis gate rather
than a post-verdict explanation. The chain had to start from the observed result
pattern, state the diagnostic role of each observation, and be able to downgrade,
qualify, or block an apparent verdict before final wording.

**0.15.0** — Added observation grounding to why-why analysis. Each chain level
had to cite a computed cell / value / distribution / correlation instead of
stacking plausible prose. If the required analysis was unavailable, the protocol
had to stop and surface the gap rather than admit a derived hypothesis.

**0.14.0** — Removed the duplicate "cycle" abstraction and attached decision
rules, stop conditions, and Purpose closure directly to the Purpose layer. Also
introduced the depth gate for derived hypotheses: a derived H needed a
mechanism-level why-why terminal, not just a parent verdict or `failure_mode`
label.

**0.13.0** — Repaired the Purpose / Hypothesis / Experiment vocabulary. A
Purpose became the notebook-level parent thesis; each `## H<id>` block became
one experiment testing one child claim. Parameter sweeps and threshold variants
were moved out of the hypothesis log and into robustness / implementation
analysis.

**0.12.0** — Added the research-goal layer so Purpose selection had to be tied
back to project-level sub-claims and close with explicit progress updates rather
than drifting from notebook to notebook.

**0.11.0** — Added review-dispatch efficiency rules so expensive multi-agent
reviews run only from clear triggers and with bounded context.

**0.10.0** — Added subject-drift protection: notebooks must keep the research
claim about the market / mechanism / technique, not silently turn into library,
implementation, or process documentation.

**0.9.0** — Added notebook narrative and post-review reconciliation rules so
review fixes do not leave stale figures, contradictory prose, edit-history
language, or reviewer vocabulary inside the research artifact.

**0.8.0** — Introduced downstream-consumer framing: Purpose headers name the
consumer, blocked decision, decision rule, and knowledge output before H design.

**0.7.0** — Added the original R-side research protocol: pre-hypothesis
exploration, hypothesis-generation pathways, novelty / differentiation checks,
cross-H synthesis, and exhaustion triggers.

**0.6.0** — Added notebook readability conventions: self-explanatory figures,
per-figure observations, helper-function docstrings, and centralized config
cells.

**0.5.0** — Reframed the notebook unit from one hypothesis to one Purpose with
multiple H rounds inside it.

**0.4.0** — Initial public release with `quant-research` and
`experiment-review`: falsifiable design, time-series validation, robustness,
bug-review, and claim-warrant review.

## License

MIT. See [LICENSE](./LICENSE).
