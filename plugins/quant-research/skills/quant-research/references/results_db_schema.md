# results_db_schema.md

Common schema for appending interpreted trial results to
`results/results.parquet`.

## When to read

- A trial result should be queryable across notebooks.
- A claim is being considered for promotion and needs an audit trail.
- Prior results are being compared by state row, mode, method, market, or
  failure mode.

Do not append rows just because a notebook ran. Append when the result has an
interpretation and updates a named research-state row.

## Principle

One row is one interpreted trial outcome. The row does not replace
`research_state.md`; it is a queryable index of evidence that points back to
the notebook and the state row it changed.

The `purpose_id` field is kept for compatibility with the existing generated
notebook names (`pur_001_*`). Treat it as the trial / notebook identifier, not
as a large parent-thesis verdict.

## Required Fields

```python
{
    # Identification
    "project": str,
    "purpose_id": str,      # trial / notebook id, e.g. pur_005_signal_flip
    "hypothesis_id": str,   # H1, H2, ...
    "run_timestamp": datetime,  # UTC

    # Research state
    "mode": str,            # r_and_d | pure_research
    "state_row_id": str,    # Q1 / E2 / C3 / CL4 from research_state.md
    "state_transition": str | None,  # e.g. active->resolved, active->split

    # Universe / data
    "instrument": str,
    "timeframe": str,
    "data_start": date | None,
    "data_end": date | None,
    "split": str | None,    # train / val / test / full / walk_forward

    # Method
    "method": str,
    "model_type": str,      # math / classical_ml / dl / rl / foundation / hybrid
    "entry_rule": str | None,
    "exit_rule": str | None,
    "sizing": str | None,

    # Cost
    "fee_bp_per_side": float,
    "slippage_model": str | None,

    # Primary metrics
    "n_trades": int,
    "win_rate": float | None,
    "total_return": float | None,
    "sharpe": float,
    "max_drawdown": float | None,
    "ret_per_trade_bp": float | None,

    # Optional prediction-model metrics
    "auc": float | None,
    "ic_spearman": float | None,
    "ir": float | None,
    "calibration_ece": float | None,

    # Optional robustness metrics
    "wf_mean_sharpe": float | None,
    "wf_pct_positive": float | None,
    "bootstrap_ci_low": float | None,
    "bootstrap_ci_high": float | None,
    "bootstrap_p": float | None,
    "psr": float | None,
    "dsr": float | None,

    # Interpretation
    "verdict": str,         # supported_candidate / supported / rejected / partial / parked
    "failure_mode": str | None,
    "competing_explanations_changed": str | None,
    "scope_condition": str | None,

    # Meta
    "n_hyperparams_tried": int | None,
    "notebook_path": str,
    "notes": str,
}
```

`scripts/aggregate_results.py` validates only the minimal required subset so
projects can add optional metrics without editing the helper.

## Failure Mode Vocabulary

Use one primary value when `verdict` is `rejected`, `partial`, or `parked`:

| Value | Meaning |
|---|---|
| `leakage` | Look-ahead, target leak, scaling leak, or timestamp error |
| `regime_mismatch` | Works only in a regime narrower than the claim |
| `fee_model` | Gross edge exists but realistic costs consume it |
| `wrong_horizon` | Holding period does not match the signal information horizon |
| `wrong_universe` | Result is specific to a narrower universe than claimed |
| `wrong_baseline` | Beats a weak baseline but not the relevant baseline |
| `threshold_brittleness` | Result depends on a narrow parameter optimum |
| `capacity_constraint` | Degrades materially with plausible notional / turnover |
| `signal_weakness` | No interpretable edge after checks |
| `mechanism_misspecification` | Proposed mechanism does not explain the observation |
| `power_insufficient` | Test cannot distinguish the explanations yet |
| `implementation_bug` | Correctness review invalidated the result |
| `other` | Requires a concrete explanation in `notes` |

Generic labels such as `noise`, `bad data`, or `market regime` are not valid
terminal explanations unless decomposed in `notes`.

## Append Example

```python
from datetime import datetime, timezone
from aggregate_results import append_result

append_result(
    "results/results.parquet",
    {
        "project": "pca_factor_screening",
        "purpose_id": "pur_005_signal_flip",
        "hypothesis_id": "H3",
        "run_timestamp": datetime.now(timezone.utc),
        "mode": "pure_research",
        "state_row_id": "Q1",
        "state_transition": "active->split",
        "instrument": "SPY",
        "timeframe": "D1",
        "data_start": None,
        "data_end": None,
        "split": "test",
        "method": "pca_factor_screening",
        "model_type": "math",
        "entry_rule": None,
        "exit_rule": None,
        "sizing": None,
        "fee_bp_per_side": 1.0,
        "slippage_model": "scalar",
        "n_trades": 223,
        "win_rate": None,
        "total_return": None,
        "sharpe": -1.74,
        "max_drawdown": None,
        "ret_per_trade_bp": None,
        "verdict": "rejected",
        "failure_mode": "regime_mismatch",
        "competing_explanations_changed": "E1 weakened; E2 still active",
        "scope_condition": "fails outside low-volatility regime",
        "n_hyperparams_tried": 20,
        "notebook_path": "purposes/pur_005_signal_flip.py",
        "notes": "Failure split Q1 into regime-conditioned subquestions.",
    },
)
```

## Query Examples

```python
import polars as pl

db = pl.read_parquet("results/results.parquet")

# What evidence changed Q1?
db.filter(pl.col("state_row_id") == "Q1").select(
    ["purpose_id", "hypothesis_id", "verdict", "failure_mode", "notes"]
)

# Failure modes by research mode
db.group_by(["mode", "failure_mode"]).len().sort(["mode", "len"])

# Supported candidates that still need promotion review
db.filter(pl.col("verdict") == "supported_candidate").select(
    ["purpose_id", "hypothesis_id", "state_row_id", "sharpe", "notebook_path"]
)
```

## Extension Rules

- Add project-specific metrics with the prefix `extra_<name>`.
- Do not change the type or meaning of common-schema columns.
- Older rows may leave new optional columns null.
- Keep the state transition in `research_state.md`; this table only indexes
  the evidence.
