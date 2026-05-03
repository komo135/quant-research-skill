"""walk_forward.py — Anchored / sliding walk-forward validation with refit.

True walk-forward methodology: train the model on a window, test on the
following window, slide forward, repeat. Per `references/shared/time_series_validation.md`.

Two modes:
- **anchored**: train window starts at t0 and grows ([t0, t_train_end])
- **sliding**: train window has fixed length, sliding through time

Each iteration:
    train: data[train_start : train_end]
    embargo: drop H bars between train_end and test_start (per AFML)
    test:  data[train_end + H : test_end]

Per-iteration: refit the model on train, evaluate on test, record the
metric. The output is a per-iteration metric series + summary statistics.

This differs from `rolling_segment_sharpe.py` which simply evaluates a
fixed strategy over contiguous segments (no train/test split, no refit).

Usage:
    from walk_forward import walk_forward

    results = walk_forward(
        fit_predict=lambda train_df, test_df: ...,  # returns metric per fold
        data=panel_pd,
        train_size=252,        # 1 year of daily bars
        test_size=63,          # 3 months
        step=21,               # advance by 1 month each iteration
        embargo=12,            # 12-bar embargo between train end and test start
        mode="sliding",
    )
"""

from __future__ import annotations

from typing import Callable, Literal

import numpy as np
import pandas as pd


def walk_forward(
    fit_predict: Callable[[pd.DataFrame, pd.DataFrame], float],
    data: pd.DataFrame,
    *,
    train_size: int,
    test_size: int,
    step: int,
    embargo: int = 0,
    mode: Literal["anchored", "sliding"] = "sliding",
    min_train: int | None = None,
) -> dict[str, object]:
    """Run walk-forward validation.

    Args:
        fit_predict: callable (train_df, test_df) -> metric (scalar). Should
            internally fit the model on train_df, evaluate on test_df.
        data: pandas DataFrame indexed by integer position OR DatetimeIndex.
        train_size: training window size in rows. For anchored mode this is
            the INITIAL train size; the window grows.
        test_size: test window size in rows.
        step: how many rows to advance between iterations (typically equal to
            test_size for non-overlapping test windows).
        embargo: bars dropped between train end and test start. Per AFML, set
            to ≥ target horizon to prevent label leakage.
        mode: "anchored" (train window grows from t0) or "sliding" (fixed
            train window).
        min_train: minimum train size to actually fit (default: train_size).

    Returns:
        dict with:
            iterations: list of dicts {iter, train_start, train_end, test_start, test_end, metric}
            stats: dict with mean / std / p05 / p50 / p95 / pct_positive / n_iters / worst
    """
    n = len(data)
    if min_train is None:
        min_train = train_size

    iterations: list[dict] = []
    iter_num = 0

    # First iteration: train spans rows [0, train_size), test spans [train_size + embargo, ...)
    train_start = 0
    train_end = train_size
    while True:
        test_start = train_end + embargo
        test_end = test_start + test_size
        if test_end > n:
            break
        if (train_end - train_start) < min_train:
            # Advance and try again
            train_start = train_start + step if mode == "sliding" else train_start
            train_end += step
            continue

        train_df = data.iloc[train_start:train_end]
        test_df = data.iloc[test_start:test_end]
        try:
            metric = float(fit_predict(train_df, test_df))
        except Exception as exc:  # noqa: BLE001
            metric = float("nan")
            print(f"warning: iteration {iter_num} failed: {exc}")

        iterations.append({
            "iter": iter_num,
            "train_start": train_start,
            "train_end": train_end,
            "test_start": test_start,
            "test_end": test_end,
            "n_train": train_end - train_start,
            "n_test": test_end - test_start,
            "metric": metric,
        })

        iter_num += 1
        # Advance windows
        if mode == "sliding":
            train_start += step
        train_end += step

    if not iterations:
        return {"iterations": [], "stats": {"n_iters": 0}}

    arr = np.array([it["metric"] for it in iterations if not np.isnan(it["metric"])])
    stats = {
        "n_iters":      len(arr),
        "mean":         round(float(arr.mean()), 4) if len(arr) else float("nan"),
        "std":          round(float(arr.std(ddof=1)), 4) if len(arr) > 1 else 0.0,
        "p05":          round(float(np.percentile(arr, 5)), 4) if len(arr) else float("nan"),
        "p50":          round(float(np.percentile(arr, 50)), 4) if len(arr) else float("nan"),
        "p95":          round(float(np.percentile(arr, 95)), 4) if len(arr) else float("nan"),
        "pct_positive": round(float((arr > 0).mean()), 4) if len(arr) else float("nan"),
        "worst":        round(float(arr.min()), 4) if len(arr) else float("nan"),
    }
    return {"iterations": iterations, "stats": stats}
