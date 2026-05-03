"""regime_label.py — Regime labelers (HMM / threshold / exogenous).

Per `references/shared/robustness_battery.md` § Regime-conditional Sharpe.

Three labeling approaches:
  - **HMM**: hidden Markov model on returns → discrete regime states. Uses
    hmmlearn if available; falls back to a simple GMM-based approximation.
  - **threshold**: rolling-vol terciles (or arbitrary quantile bins) on a
    user-supplied series.
  - **exogenous**: takes an exogenous regime indicator series (e.g., VIX
    bins) and aligns with the data index.

All three produce a pd.Series of integer labels {0, 1, ..., n_regimes-1}
aligned to the input data index. Use these labels in downstream code:

    regimes = label_regimes_threshold(returns, n_regimes=3)
    for r in range(3):
        sub_returns = returns[regimes == r]
        sub_sharpe = compute_sharpe(sub_returns)
"""

from __future__ import annotations

from typing import Literal

import numpy as np
import pandas as pd


def label_regimes_threshold(
    series: pd.Series,
    *,
    n_regimes: int = 3,
    rolling_window: int | None = None,
    measure: Literal["value", "rolling_std", "rolling_abs_mean"] = "rolling_std",
    method: Literal["quantile", "fixed_thresholds"] = "quantile",
    fixed_thresholds: list[float] | None = None,
) -> pd.Series:
    """Threshold-based regime labels (e.g., vol terciles).

    Args:
        series: input series (e.g., returns).
        n_regimes: number of regime bins (default 3 → low / normal / high).
        rolling_window: window for rolling measures (default: None for
            value-based labeling).
        measure: what to bin —
            "value" (raw series),
            "rolling_std" (vol regime),
            "rolling_abs_mean" (drift regime).
        method: "quantile" (equal-frequency bins) or "fixed_thresholds"
            (user-supplied).
        fixed_thresholds: required if method=="fixed_thresholds"; list of
            n_regimes-1 values.

    Returns:
        Series of integer labels in [0, n_regimes-1] aligned to series.index.
    """
    if measure == "value":
        x = series.copy()
    else:
        if rolling_window is None:
            rolling_window = max(20, len(series) // 100)
        if measure == "rolling_std":
            x = series.rolling(rolling_window).std()
        else:  # rolling_abs_mean
            x = series.rolling(rolling_window).apply(lambda v: np.abs(v).mean(), raw=True)

    if method == "quantile":
        labels = pd.qcut(x, q=n_regimes, labels=False, duplicates="drop")
    else:
        if not fixed_thresholds or len(fixed_thresholds) != n_regimes - 1:
            raise ValueError(
                f"fixed_thresholds must have length n_regimes-1 = {n_regimes-1}"
            )
        edges = [-np.inf] + sorted(fixed_thresholds) + [np.inf]
        labels = pd.cut(x, bins=edges, labels=False)

    return labels.astype("Int64").rename("regime")


def label_regimes_exogenous(
    exogenous: pd.Series,
    target_index: pd.Index,
    *,
    n_regimes: int = 3,
    method: Literal["quantile", "fixed_thresholds"] = "quantile",
    fixed_thresholds: list[float] | None = None,
) -> pd.Series:
    """Exogenous-driven regime labels (e.g., VIX bins applied to equity returns).

    Args:
        exogenous: series of the exogenous indicator (e.g., VIX daily).
        target_index: index of the series we want to label (aligned to
            exogenous via reindex + ffill).
        n_regimes: bin count.
        method: "quantile" or "fixed_thresholds".
        fixed_thresholds: required if method=="fixed_thresholds".

    Returns:
        Series of integer regime labels, aligned to target_index.
    """
    aligned = exogenous.reindex(target_index, method="ffill")
    if method == "quantile":
        labels = pd.qcut(aligned, q=n_regimes, labels=False, duplicates="drop")
    else:
        if not fixed_thresholds or len(fixed_thresholds) != n_regimes - 1:
            raise ValueError(
                f"fixed_thresholds must have length n_regimes-1 = {n_regimes-1}"
            )
        edges = [-np.inf] + sorted(fixed_thresholds) + [np.inf]
        labels = pd.cut(aligned, bins=edges, labels=False)
    return labels.astype("Int64").rename("regime")


def label_regimes_hmm(
    returns: pd.Series,
    *,
    n_regimes: int = 3,
    n_iter: int = 100,
    seed: int = 42,
) -> pd.Series:
    """HMM-based regime labels (Gaussian emissions on returns).

    Requires hmmlearn (`pip install hmmlearn`). Falls back to a
    GMM-based approximation if hmmlearn is not installed.

    Args:
        returns: 1D return series (per-period).
        n_regimes: number of hidden states.
        n_iter: training iterations.
        seed: RNG seed.

    Returns:
        Series of integer regime labels in [0, n_regimes-1].
    """
    X = returns.dropna().values.reshape(-1, 1)
    try:
        from hmmlearn.hmm import GaussianHMM

        model = GaussianHMM(
            n_components=n_regimes,
            covariance_type="diag",
            n_iter=n_iter,
            random_state=seed,
        )
        model.fit(X)
        labels = model.predict(X)
    except ImportError:
        # Fallback: GMM clustering
        try:
            from sklearn.mixture import GaussianMixture

            model = GaussianMixture(n_components=n_regimes, random_state=seed, n_init=3)
            labels = model.fit_predict(X)
        except ImportError as e:
            raise RuntimeError(
                "Neither hmmlearn nor sklearn available; install one to use HMM regime labels"
            ) from e

    out = pd.Series(index=returns.index, dtype="Int64")
    out.loc[returns.dropna().index] = labels.astype(int)
    return out.rename("regime")
