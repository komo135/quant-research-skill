"""rolling_segment_sharpe.py — Compute a metric over CONTIGUOUS NON-OVERLAPPING
time segments of a panel.

This is a quick reach-around for variability across calendar segments. It is
NOT walk-forward — there is no per-window refit and no train/test split.
For true walk-forward (with refit per window), see `walk_forward.py`.

The previous file `walk_forward.py` (pre-rebuild) had a misleading name and
implemented this segment behavior. It has been renamed to this file; the new
`walk_forward.py` implements the actual walk-forward methodology.

Usage:
    from rolling_segment_sharpe import segment_metric_distribution

    stats, per_segment = segment_metric_distribution(
        run_metric=lambda df: vbt.Portfolio.from_signals(
            df["close"], df["entry"], df["exit"]
        ).sharpe_ratio(),
        data=panel_pd,
        segment="3MS",
        min_rows=1000,
    )
"""

from __future__ import annotations

from typing import Callable

import numpy as np
import pandas as pd


def segment_metric_distribution(
    run_metric: Callable[[pd.DataFrame], float],
    data: pd.DataFrame,
    segment: str = "3MS",
    min_rows: int = 1000,
) -> tuple[dict[str, float], pd.DataFrame]:
    """Apply run_metric to each contiguous non-overlapping segment of `data`.

    Args:
        run_metric: callable returning a scalar metric per segment.
        data: pandas DataFrame indexed by time.
        segment: pandas frequency string (e.g. "3MS" = 3-month start).
        min_rows: skip segments shorter than this.

    Returns:
        stats: dict with mean / std / p05 / p50 / p95 / pct_positive / n_segments / worst.
        per_segment: DataFrame with one row per segment.
    """
    assert isinstance(data.index, pd.DatetimeIndex), "data must be time-indexed"
    boundaries = pd.date_range(
        start=data.index.min().normalize(),
        end=data.index.max().normalize() + pd.Timedelta(days=1),
        freq=segment,
        tz=data.index.tz,
    )

    rows = []
    for s, e in zip(boundaries[:-1], boundaries[1:]):
        sub = data[(data.index >= s) & (data.index < e)]
        if len(sub) < min_rows:
            continue
        try:
            metric = float(run_metric(sub))
        except Exception as exc:  # noqa: BLE001
            metric = float("nan")
            print(f"warning: segment {s.date()} failed: {exc}")
        rows.append({"segment_start": s.date(), "n_rows": len(sub), "metric": metric})

    per_segment = pd.DataFrame(rows)
    if per_segment.empty or per_segment["metric"].isna().all():
        return {"n_segments": 0}, per_segment

    arr = per_segment["metric"].dropna().to_numpy()
    stats = {
        "n_segments":    int(len(arr)),
        "mean":          round(float(arr.mean()), 3),
        "std":           round(float(arr.std(ddof=1)) if len(arr) > 1 else 0.0, 3),
        "p05":           round(float(np.percentile(arr, 5)), 3),
        "p50":           round(float(np.percentile(arr, 50)), 3),
        "p95":           round(float(np.percentile(arr, 95)), 3),
        "pct_positive":  round(float((arr > 0).mean()), 3),
        "worst":         round(float(arr.min()), 3),
    }
    return stats, per_segment


# Backward-compatibility alias for the old name (will warn once)
def walk_forward_sharpe(*args, **kwargs):
    """DEPRECATED: this function was misnamed. It does NOT do walk-forward.
    Use segment_metric_distribution() for the same behavior, or walk_forward.py
    for actual walk-forward."""
    import warnings
    warnings.warn(
        "walk_forward_sharpe() in rolling_segment_sharpe.py is the legacy alias "
        "for segment_metric_distribution(). The function does NOT do walk-forward "
        "— use scripts/walk_forward.py for that.",
        DeprecationWarning,
        stacklevel=2,
    )
    return segment_metric_distribution(*args, **kwargs)
