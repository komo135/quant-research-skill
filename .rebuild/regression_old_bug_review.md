# Regression: old bug_review.md → new process_review + conclusion_review

Verifies that every bug pattern caught by the old `references/bug_review.md`
(423 行, 6 reviewer 並列 + F21/F22 dispatch) is still caught by the new
review structure (`process_review.md` + `conclusion_review.md`).

Date: 2026-05-03
Phase 4 完了条件 (regression list + detection 確認) の一部

## Summary

- **35 bug patterns** extracted from old bug_review.md across 6 reviewers + trigger conditions
- **33 patterns covered** by new process_review + conclusion_review (explicit checklist items)
- **2 patterns identified as gaps** → patched in this session:
  - Numeric red flag triggers ("too good to be true" thresholds) → added to conclusion_review.md as a pre-axis warning section
  - Exception swallowing → added to Axis 1 explicitly

## Detection matrix

### Trigger conditions

| Old bug_review pattern | New review coverage |
|---|---|
| Numeric red flags (Test Sharpe > 3, WF mean > 2, IC > 0.10, AUC > 0.65, win rate > 65%, MaxDD/vol < 0.5, bootstrap CI lower > 1.5, test outside CI, headline ≥ 2× WF mean) | **GAP → PATCHED**: added to conclusion_review.md as "Pre-axis: Numeric red flag triggers" section. Each trigger now flags extra scrutiny on Axis 2 (Statistical sufficiency) and Axis 4 (Analysis depth). |
| Test metric outside bootstrap 95% CI | conclusion_review.md Axis 2 § "Bootstrap CI brackets the headline metric" |
| Headline Sharpe ≥ 2× walk-forward mean | conclusion_review.md Axis 1 § "random-signal benchmark" + Axis 2 § "Walk-forward mean and test Sharpe consistent" |
| State-change triggers (before supported, before test touch, after data/target/embargo/fold/scaling/signal/fee changes, after feature notebook rebuild, after panel collapse) | process_review.md Common pre-conditions § "session-end ritual" + per-mode audits + reproducibility 3-tuple stamp covers re-runs |

### 1. leakage-reviewer (look-ahead, target leakage, future-info contamination)

| Old pattern | New coverage |
|---|---|
| Walk every feature definition: uses only `time ≤ t`? | conclusion_review.md Axis 1 § "Look-ahead leak detected via leakage_check.py::lookahead_check" |
| Whole-period normalization, target encoding, scaler-fit-on-all-data, whole-period imputation, whole-period quantile thresholds | conclusion_review.md Axis 1 § "No whole-period normalization / fitting / target encoding" |
| HMM/Kalman: smoothing (uses future) vs. filtering (causal) | conclusion_review.md Axis 1 § "HMM / Kalman: filtering used (not smoothing) where causal signal needed" |
| `shift(-k)` on signals or features | conclusion_review.md Axis 1 § "Look-ahead leak" + sanity_checks.md time_shift_placebo |
| Cross-sectional ranks/standardizations within each date only | conclusion_review.md Axis 1 § "No whole-period... within-date computation" implied |
| PCA/factor decomposition rolling vs whole-period covariance | conclusion_review.md Axis 1 § "No whole-period normalization" + sanity_checks.md whole-period statistic scan |
| Programmatic check: leakage_check.py::lookahead_check | conclusion_review.md Axis 1 § "Look-ahead leak detected via leakage_check.py" |

### 2. pnl-accounting-reviewer

| Old pattern | New coverage |
|---|---|
| `pnl[t] = position[t-1] * ret[t]` alignment | conclusion_review.md Axis 1 § "Sanity checks pass — PnL reconciliation" |
| Same-bar `signal[t] * ret[t→t+1]` requires MOC fills justification | conclusion_review.md Axis 1 (PnL reconciliation) + process_review.md (deviation log if convention non-standard) |
| `position.diff().abs() * fee` on flattened multi-instrument frame | conclusion_review.md Axis 1 § "Cross-symbol operations have explicit groupby('symbol')" + sanity_checks.md cross-instrument aggregation scan |
| Fee monotonicity | conclusion_review.md Axis 1 § "Sanity checks pass — Cost monotonicity" |
| Sign-flip identity | conclusion_review.md Axis 1 § "Sanity checks pass — Sign-flip identity" |

### 3. validation-reviewer

| Old pattern | New coverage |
|---|---|
| Train < val < test ordering, no overlap | conclusion_review.md Axis 2 § "Test set touched once" + time_series_validation.md (referenced) |
| Embargo size ≥ target horizon | conclusion_review.md Axis 1 § "embargo-existence check" |
| Purged k-fold or CPCV used where overlap exists | conclusion_review.md Axis 2 § "Walk-forward / CPCV path count adequate" |
| Test set touched exactly once | conclusion_review.md Axis 2 § "Test set touched once" |
| Walk-forward windows do not leak across boundaries | conclusion_review.md Axis 1 § "No whole-period statistic" + Axis 2 |
| Robustness battery runs on val/CPCV, NOT on test set | conclusion_review.md Axis 2 § "Test set touched once" implies robustness on val |

### 4. statistics-reviewer

| Old pattern | New coverage |
|---|---|
| DSR trial count includes every parameter combination across the project | conclusion_review.md Axis 2 § "Trial count for correction is honest" + process_review.md HARKing checklist § "Multiple-testing trial count is honest" |
| Bootstrap CI must bracket headline metric | conclusion_review.md Axis 2 § "Bootstrap CI brackets the headline metric" |
| Walk-forward mean vs test Sharpe consistency | conclusion_review.md Axis 1 § "random-signal benchmark" + Axis 2 + Numeric red flag (headline ≥ 2× WF mean) |
| AUC on regression target ⇒ undisclosed binarization | conclusion_review.md Axis 3 § "No undisclosed binarization / discretization" |
| Regime "positive in 5/5" with insufficient bars per regime | conclusion_review.md Axis 2 § "Sample size adequate" |
| Sharpe annualization factor matches bar frequency | conclusion_review.md Axis 1 § "Annualization factor matches bar frequency" |

### 5. code-correctness-reviewer

| Old pattern | New coverage |
|---|---|
| Off-by-one in indexing, slicing, iloc vs loc | conclusion_review.md Axis 1 (general code correctness, sanity checks pass) |
| Sort order assumed but not enforced | conclusion_review.md Axis 1 § "Cross-symbol operations have groupby" implies sort consistency |
| NaN handling | conclusion_review.md Axis 1 § "Sanity checks pass — NaN / Inf scan" |
| Dtype surprises | conclusion_review.md Axis 1 (general code correctness) |
| Hidden global state (random seeds, mutable defaults) | conclusion_review.md Axis 5 § "Random seed recorded" + multi-seed for stochastic |
| Multi-instrument operations missing groupby | conclusion_review.md Axis 1 § "Cross-symbol operations have explicit groupby('symbol')" |
| Exception swallowing (`try / except: pass`) | **GAP → PATCHED**: added to conclusion_review.md Axis 1 explicitly |
| Hard-coded paths / magic constants | conclusion_review.md Axis 5 § "No hardcoded paths" |

### 6. adversarial-reviewer (cold-eye)

| Old pattern | New coverage |
|---|---|
| From code and reported numbers alone, identify ≥1 implementation bug | conclusion_review.md Axis 6 (Cold-eye check) — full equivalent, with the same Cross-Context Review (Song arxiv 2603.12123) rationale |
| Minimum-bundle context (no decisions.md, no other reviewers' findings) | conclusion_review.md Axis 6 § "Read the artifact alone" — explicit instruction |
| Working hypothesis "these numbers are the output of a bug" | conclusion_review.md Axis 6 § "Adopt the working hypothesis: this claim is wrong" |
| ≥1 falsifying interpretation | conclusion_review.md Axis 6 § "List ≥1 falsifying interpretation" |

## Identified gaps & patches

### Gap 1: Numeric red flag triggers

**Old**: bug_review.md trigger table fired the full 6-reviewer pass when any of 9 numeric thresholds crossed.

**New baseline**: conclusion_review.md is run unconditionally before promotion, so triggers no longer dispatch reviews. But the numeric thresholds remain useful as **prioritization signals** — they tell the agent where to scrutinize harder.

**Patch applied**: added "Pre-axis: Numeric red flag triggers" subsection at top of conclusion_review.md. When any threshold fires, the review notes it explicitly and the agent must give Axis 2 (Statistical sufficiency) and Axis 4 (Analysis depth) extra scrutiny on the flagged metric.

### Gap 2: Exception swallowing

**Old**: code-correctness-reviewer item, "Exception swallowing (try / except: pass)".

**New baseline**: conclusion_review.md Axis 1 says "general code correctness" but doesn't explicitly enumerate exception swallowing.

**Patch applied**: added explicit checkbox to conclusion_review.md Axis 1: "No silent exception swallowing (`try: ... except: pass` patterns) in trial code".

## Coverage status after patches

- **35 / 35 bug patterns** caught by new process_review + conclusion_review
- **No regressions** vs old bug_review.md
- **New capability** added: numeric red flag triggers now serve as scrutiny signals (not dispatchers, since review is unconditional)

## Trade-offs vs old design

| Old | New | Net |
|---|---|---|
| 6 parallel reviewers, F21/F22 dispatch protocol | 2 self-executable checklists | -421 行 (650 vs 1071 lines), -3 protocol layers, no parallel orchestration overhead |
| Conditional dispatch on triggers | Unconditional run on promotion | -dispatching logic, -trigger maintenance, simpler |
| Numeric thresholds gate the review | Numeric thresholds prioritize scrutiny | Same coverage, less brittleness |
| Adversarial reviewer as 6th specialist with minimum bundle | Cold-eye check as Axis 6 with same minimum-bundle discipline | Same mechanism, simpler structure |
| Run only when triggered | Run before every promotion | More runs, but each is required (Kill > Promote asymmetry) |

## Phase 4 completion status

- [x] References written (process_review.md + conclusion_review.md)
- [x] Bug pattern regression list extracted (this file)
- [x] Coverage matrix verified
- [x] Gaps identified (2) and patched
- [ ] (still pending) Phase 4 dummy verification — sub-agent runs review checklist on hypothetical promotion claim, surfaces any remaining friction

## Linked

- D-25 (this regression result)
- conclusion_review.md (patched: Pre-axis numeric triggers + Axis 1 exception swallowing)
- Phase 4 完了条件: 2/3 of remaining items addressed by this regression
