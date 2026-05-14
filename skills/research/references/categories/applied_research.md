# Applied Research

## When this category applies

Applied research aims at a specific practical objective by designing a method, model, or procedure. The defining feature, from the Frascati Manual (OECD 2015), is that the work is directed toward a stated objective with a measurable success criterion.

Pick applied research when:

- You have a target metric (BLEU, accuracy, energy efficiency, error rate, throughput).
- You want to propose a new method that improves on existing baselines.
- You will compare quantitatively to prior approaches.
- You expect to run ablation studies showing the contribution of each component.

This is the dominant form of method research in ML, optimization, control, signal processing, and similar fields. The Transformer paper ([Vaswani et al. 2017](https://arxiv.org/abs/1706.03762)) is a canonical example: a new architecture, BLEU as the metric, comparison to ConvS2S and prior RNN-based seq2seq, ablations isolating attention's contribution.

Do not pick applied research if the metric is not yet defined or if you are still trying to understand the phenomenon. Those are basic research first. Applied research depends on basic research having established the metric, the baselines, and the conditions of evaluation.

## Typical outputs

- A method (architecture, algorithm, training procedure) achieving the target metric
- Quantitative comparison to baselines
- Ablation results showing which components contribute
- Failure modes of the method (under what conditions it does not improve)
- Hyperparameter sensitivity characterization

## Default plan mode

`confirmatory`. Fix in advance:

- Primary metric and how it is measured
- Baseline(s) for comparison, with source/version
- Decision threshold (what improvement counts as a positive result)
- Datasets / evaluation splits
- Compute budget
- Ablations planned

Exploratory mode is acceptable for early scoping (which architectures are even feasible) but the claim-bearing phase should be confirmatory. If you do exploratory work first and then switch to confirmatory, those are two separate plans — the exploratory plan informs the confirmatory plan but does not contribute its evidence directly.

`milestone` is rarely appropriate for pure applied research — milestone implies "does it work end-to-end" while applied research asks "does it beat the baseline."

## Completion conditions

Acceptable completion shapes:

- Target metric improved over baseline by the pre-stated threshold, with claims scoped to the conditions tested
- Target metric not improved — explicit negative result with diagnosis
- Method works under specific conditions but not others — scoped claim
- Method is dominated by a simpler baseline — also a result; report it honestly

Not acceptable as completion:

- "Looks like it works" without baseline comparison
- "Probably better" without quantitative evidence
- Improvement that disappears under reasonable perturbation (different seeds, different splits, slightly different hyperparameters)
- Improvement only on the specific evaluation the agent chose; failure on the standard evaluation glossed over

## Report shape

Applied research reports follow paper-like structure, without paper formality (no LaTeX, no Related Work survey of dozens of papers, no formal abstract). Use `assets/report/applied_research_report.md.template`.

1. **Summary** — what was tried, what worked, the headline numbers
2. **Background** — what prior work this builds on (cite a handful, not dozens)
3. **Method** — substantive description of the proposed approach; enough for re-implementation
4. **Experiments** — datasets, baselines, training/evaluation protocol, hyperparameters
5. **Results** — quantitative comparison with figures and tables, including variance across seeds
6. **Ablations** — which components contribute; what happens when each is removed
7. **Limitations** — conditions not tested, failure modes, possible confounds
8. **Next action** — iteration decision, or a request to the human reader

Methods description must be substantive. "We used a Transformer" is not a methods description. The architecture choices (heads, layers, hidden dim, position encoding), training details (optimizer, schedule, regularization), and evaluation protocol (beam size, length penalty, test set) must be specific enough that another researcher could re-implement and roughly reproduce.

## Claims in applied research

The headline claim is typically: "method M achieves metric value V on benchmark B, exceeding baseline B' by Δ under conditions C." For this claim to be load-bearing:

- `evidence` must cite the specific runs and the benchmark
- `alternatives_not_excluded` must list confounders not yet ruled out (different hyperparameter budgets between method and baseline, different seed pools, lucky data splits, etc.)
- `conditions_tested` must specify which datasets, which model sizes, which compute regimes
- `conditions_not_tested` must explicitly call out generalization gaps

Ablations support claims about which components are responsible. Without ablations, "method M works because of innovation I" is weak — you cannot rule out that the improvement comes from one component you happened to also change.

Example claim record:

```yaml
- claim: Replacing the standard MHA block with the proposed sparse-attention variant reduces validation perplexity by 0.18 (relative 2.1%) on WikiText-103 at the 350M-parameter scale across 3 seeds, with stable training.
  evidence: experiments/02_sparse_attn/runs/02__008__seed{0,1,2}/eval/wikitext103.json; figures/perplexity_vs_seed.png
  alternatives_not_excluded:
    - "Improvement may come from the 1.3% increase in active FLOPs at fixed parameter count"
    - "Only 3 seeds — std 0.07; the 0.18 gap is ~2.5σ but not >3σ"
    - "Sparse-attention variant got 40 hyperparameter trials vs 20 for MHA baseline"
  conditions_tested: "WikiText-103, 350M parameters, 100k steps, AdamW lr=1e-4 cosine, batch 1024, fp16"
  conditions_not_tested:
    - "Larger scales (>1B params)"
    - "Other domains (code, dialogue)"
    - "Longer training (>100k steps)"
```

## Analysis weight

For applied research, the **claim disclosure floor from `analysis.md` is non-optional**. Without it, the claim is exploratory regardless of headline numbers. The floor:

- Leakage probe passed
- ≥3 seeds with reported variance (Bouthillier et al. 2021)
- Ablation of each claimed-novel component
- Slice / subgroup evaluation on standard axes
- Calibration check if confidence scores feed downstream
- Perturbation / robustness probe
- Error analysis on a sample of failures

Run learning curves and loss curves as standard practice — these often reveal training instabilities, overfitting, or insufficient capacity before they show up in headline metrics.

Standard ablation patterns: one component removed at a time, OR factorial design if interactions matter, with the full method and a simple baseline always in the comparison set. Single-seed ablations are not ablations — variance across seeds is part of the result.

Pearl Rung 2 (intervention via ablation) is the standard warrant for "component X is responsible for the improvement." Diagnostic plots alone (Rung 1) do not support causal claims about why the method works.

## Pitfalls

- **No baseline.** A new method without a comparator is not applied research.
- **Single-seed results.** Variance across seeds is part of the result. Always run multiple seeds for claim-bearing comparisons.
- **Hyperparameter asymmetry.** If your method got more hyperparameter tuning than the baseline, the comparison is biased. Report tuning budgets explicitly.
- **In-sample tuning.** Methods tuned on the test set are not tested. Use a validation split for tuning; test only at the end.
- **Metric shopping.** If the primary metric did not improve, do not switch to a different metric and present it as a success. If a secondary metric is more relevant, REFINE the plan before any claim is made.
- **Compute apples-vs-oranges.** Comparing a 10× larger model to a baseline tells you about scale, not about your method. Hold compute constant or report scaling curves.
- **Ablation theater.** Single-component ablations on isolated runs do not isolate causal contribution if the components interact. Report joint ablations when interactions matter.
- **Skipping the negative-result writeup.** A method that did not improve is still a result. Document it; the next agent should not re-run it.
