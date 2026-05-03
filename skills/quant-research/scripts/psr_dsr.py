"""psr_dsr.py — Probabilistic and Deflated Sharpe Ratio (per-period API).

Bailey & López de Prado (2012, 2014).

**IMPORTANT — per-period vs annualized**: The PSR/DSR formulas were derived
for the **per-period** Sharpe ratio (e.g., daily Sharpe), with T = number of
return observations. Passing an annualized SR with T = number of years (or
worse, T = number of trading days alongside an annualized SR) breaks the
formula because the variance term `1 - γ_3 × SR + ((γ_4-1)/4) × SR²`
scales with SR.

Use the high-level `from_returns(returns, ...)` API by default — it computes
per-period SR from the returns series automatically. Use `psr` / `dsr`
directly only if you have already computed per-period SR + skew + kurtosis
externally.

References:
- Bailey, D. H. & López de Prado, M. (2012). The Sharpe Ratio Efficient
  Frontier. *Journal of Risk*.
- Bailey, D. H. & López de Prado, M. (2014). The Deflated Sharpe Ratio.
  *Journal of Portfolio Management*.

See also: `references/shared/psr_dsr_formulas.md` and
`references/shared/multiple_testing.md`.
"""

from __future__ import annotations

import warnings
from typing import Literal

import numpy as np
from scipy import stats

EULER_MASCHERONI = 0.5772156649


# ---------------------------------------------------------------------------
# Low-level (per-period) functions
# ---------------------------------------------------------------------------


def psr(
    sr_obs: float,
    sr_threshold: float,
    T: int,
    skew: float,
    kurt: float,
    *,
    period: Literal["per_obs"] = "per_obs",
) -> float:
    """Probabilistic Sharpe Ratio.

    Per Bailey & López de Prado (2012):
        PSR(SR*) = Φ((SR_obs − SR*) × √(T−1) / √(1 − γ_3 × SR_obs + ((γ_4−1)/4) × SR_obs²))

    Args:
        sr_obs: observed PER-PERIOD Sharpe (e.g., daily SR, NOT annualized).
        sr_threshold: comparison Sharpe (per-period; typically 0).
        T: number of return observations.
        skew: skewness of observed returns (Fisher / unbiased).
        kurt: RAW kurtosis of observed returns (Pearson, normal=3, NOT excess).
        period: must be "per_obs" — explicit safeguard against annualized misuse.

    Returns:
        Probability in [0, 1] that the true Sharpe exceeds the threshold.

    Raises:
        ValueError: if period != "per_obs" (forces explicit acknowledgment).
    """
    if period != "per_obs":
        raise ValueError(
            "psr() requires per-period SR. Use from_returns() if you have raw "
            "returns; do NOT pass annualized SR to psr() directly."
        )
    numerator = (sr_obs - sr_threshold) * np.sqrt(T - 1)
    denominator = np.sqrt(1 - skew * sr_obs + (kurt - 1) / 4 * sr_obs**2)
    return float(stats.norm.cdf(numerator / denominator))


def expected_max_sr(n_trials: int, var_sr: float) -> float:
    """E[max SR over N trials] under the null (Bailey & López de Prado 2014).

    Args:
        n_trials: count of distinct hyperparameter / model settings tried.
        var_sr: variance of (per-period) SR across trials.
    """
    if n_trials < 2:
        return 0.0
    a = (1 - EULER_MASCHERONI) * stats.norm.ppf(1 - 1 / n_trials)
    b = EULER_MASCHERONI * stats.norm.ppf(1 - 1 / (n_trials * np.e))
    return float(np.sqrt(var_sr) * (a + b))


def dsr(
    sr_obs: float,
    T: int,
    skew: float,
    kurt: float,
    n_trials: int,
    var_sr: float,
    *,
    period: Literal["per_obs"] = "per_obs",
) -> float:
    """Deflated Sharpe Ratio: PSR with threshold = E[max SR over trials].

    All inputs must be per-period. Use from_returns() for safety.
    """
    sr_threshold = expected_max_sr(n_trials, var_sr)
    return psr(sr_obs, sr_threshold, T, skew, kurt, period=period)


# ---------------------------------------------------------------------------
# High-level (returns-driven) API — RECOMMENDED
# ---------------------------------------------------------------------------


def from_returns(
    returns: np.ndarray,
    *,
    sr_threshold_annualized: float = 0.0,
    n_trials: int = 1,
    var_sr: float | None = None,
    annualization_factor: float = 1.0,
) -> dict[str, float]:
    """Compute PSR + DSR from a return series. Recommended entry point.

    Args:
        returns: 1D array of per-period returns (e.g., daily returns).
        sr_threshold_annualized: PSR threshold as an annualized number (e.g.,
            0.5 means "test against an annualized SR of 0.5"). Internally
            converted to per-period.
        n_trials: trial count for DSR (per `references/shared/multiple_testing.md`,
            this must include EVERY hyperparameter combination tried across the
            project, not just this notebook).
        var_sr: variance of (per-period) SR across trials. None disables DSR.
        annualization_factor: √(periods per year). E.g., for daily returns
            annualization_factor = √252; for monthly, √12. Used to:
            (a) compute annualized SR for display, (b) convert
            `sr_threshold_annualized` to per-period for the formula.

    Returns:
        dict with keys: T, sr_per_period, sr_annualized, skew, kurt, psr,
        and (if var_sr provided + n_trials > 1) dsr, expected_max_sr_per_period.
    """
    returns = np.asarray(returns, dtype=float)
    T = len(returns)
    if T < 2:
        raise ValueError(f"need at least 2 observations, got {T}")

    sr_per_period = float(returns.mean() / (returns.std(ddof=1) + 1e-12))
    sr_annualized = sr_per_period * annualization_factor
    skew = float(stats.skew(returns))
    kurt = float(stats.kurtosis(returns, fisher=False))  # RAW kurtosis

    # Convert threshold to per-period for the formula
    sr_threshold_per_period = sr_threshold_annualized / annualization_factor

    psr_value = psr(sr_per_period, sr_threshold_per_period, T, skew, kurt)

    out: dict[str, float] = {
        "T":                T,
        "sr_per_period":    round(sr_per_period, 6),
        "sr_annualized":    round(sr_annualized, 4),
        "skew":             round(skew, 4),
        "kurt":             round(kurt, 4),
        "psr":              round(psr_value, 4),
        "annualization_factor": annualization_factor,
    }
    if n_trials > 1 and var_sr is not None:
        e_max = expected_max_sr(n_trials, var_sr)
        out["expected_max_sr_per_period"] = round(e_max, 6)
        out["dsr"] = round(dsr(sr_per_period, T, skew, kurt, n_trials, var_sr), 4)

    return out


# ---------------------------------------------------------------------------
# Compatibility shim for legacy callers
# ---------------------------------------------------------------------------


def _legacy_psr_with_warning(sr_obs: float, sr_threshold: float, T: int,
                              skew: float, kurt: float) -> float:
    warnings.warn(
        "Calling psr() with positional args without period='per_obs' is "
        "deprecated. Per-period SR is required; use from_returns() to be safe.",
        DeprecationWarning,
        stacklevel=2,
    )
    return psr(sr_obs, sr_threshold, T, skew, kurt, period="per_obs")
