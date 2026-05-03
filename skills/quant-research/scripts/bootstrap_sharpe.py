"""bootstrap_sharpe.py — Block bootstrap CI for the Sharpe ratio.

Implements **stationary block bootstrap** (Politis & Romano 1994), which
draws blocks of geometrically-distributed length to preserve time-series
dependence while producing a stationary resampled series.

Also provides Künsch (1989) moving-block bootstrap (MBB) as `--method mbb`.

Block length default: Politis & White (2004) automatic selection (a rough
data-driven rule); user may override with --block-mean.

References:
- Politis & Romano (1994). The Stationary Bootstrap. *JASA* 89(428).
- Künsch (1989). The Jackknife and the Bootstrap for General Stationary
  Observations. *Annals of Statistics*.
- Politis & White (2004). Automatic Block-Length Selection for the
  Dependent Bootstrap. *Econometric Reviews*.
"""

from __future__ import annotations

from typing import Literal

import numpy as np


def _stationary_bootstrap_indices(n: int, mean_block: float, rng: np.random.Generator) -> np.ndarray:
    """Generate one resample of length n by stationary bootstrap (Politis & Romano).

    Each new index is either (prev + 1) mod n with prob (1 - 1/mean_block),
    or a fresh random index with prob 1/mean_block. Equivalent to drawing
    blocks of geometric length.
    """
    p = 1.0 / mean_block
    indices = np.empty(n, dtype=np.int64)
    indices[0] = rng.integers(0, n)
    flips = rng.random(n - 1) < p
    fresh = rng.integers(0, n, size=n - 1)
    for i in range(1, n):
        if flips[i - 1]:
            indices[i] = fresh[i - 1]
        else:
            indices[i] = (indices[i - 1] + 1) % n
    return indices


def _moving_block_bootstrap_indices(n: int, block: int, rng: np.random.Generator) -> np.ndarray:
    """Generate one resample of length n by Künsch (1989) MBB (fixed block size)."""
    n_blocks = int(np.ceil(n / block))
    starts = rng.integers(0, n - block + 1, size=n_blocks)
    out = np.empty(n_blocks * block, dtype=np.int64)
    for i, s in enumerate(starts):
        out[i * block : (i + 1) * block] = np.arange(s, s + block)
    return out[:n]


def _politis_white_block_length(returns: np.ndarray, mean: bool = True) -> float:
    """Politis & White (2004) automatic block length.

    Simplified implementation: estimates the optimal block length b_opt for
    the stationary bootstrap from the autocorrelation structure. Returns the
    mean block length for the geometric distribution (mean=True) or the
    fixed block length for MBB (mean=False).

    The PW formula uses a flat-top kernel and bandwidth chosen from the
    autocorrelation spectrum. We use a pragmatic approximation:
        b_opt ≈ (2 * sum_lag1_to_M_acf)^{2/3} * n^{1/3}
    where M is chosen as 2 * sqrt(log10(n)).
    """
    n = len(returns)
    if n < 30:
        return float(np.sqrt(n))
    centered = returns - returns.mean()
    var = (centered ** 2).sum() / n
    if var == 0:
        return float(np.sqrt(n))
    M = max(5, int(2 * np.sqrt(np.log10(n))))
    acf_sum = 0.0
    for k in range(1, M + 1):
        if k >= n:
            break
        cov_k = (centered[k:] * centered[:-k]).sum() / n
        rho_k = cov_k / var
        # Flat-top kernel: weight = 1 if |k| <= M/2, else 2(1 - |k|/M)
        if k <= M / 2:
            w = 1.0
        else:
            w = max(0.0, 2 * (1 - k / M))
        acf_sum += w * rho_k
    base = max(0.1, 2 * abs(acf_sum))
    b_opt = (base ** (2 / 3)) * (n ** (1 / 3))
    # Clip to reasonable range
    b_opt = float(max(2.0, min(b_opt, n / 4)))
    return b_opt


def bootstrap_sharpe_ci(
    returns: np.ndarray,
    *,
    n_resample: int = 10000,
    method: Literal["stationary", "mbb"] = "stationary",
    block_mean: float | None = None,
    seed: int = 42,
    ci: float = 0.95,
    ddof: int = 1,
) -> dict[str, float]:
    """Block bootstrap CI for per-period Sharpe ratio.

    Args:
        returns: 1D array of per-period returns.
        n_resample: number of bootstrap resamples.
        method: "stationary" (Politis & Romano 1994) or "mbb" (Künsch 1989).
        block_mean: mean block length for stationary OR fixed block length
            for MBB. None → Politis & White (2004) automatic selection.
        seed: RNG seed for reproducibility.
        ci: confidence level (e.g., 0.95).
        ddof: degrees of freedom for std (default 1; consistent with
            psr_dsr.py).

    Returns:
        dict with: n_samples, method, block_mean, actual, boot_mean, boot_std,
        ci_low, ci_high, prob_neg (probability that resampled SR ≤ 0).

    Notes:
        - "prob_neg" is the bootstrap probability P(SR ≤ 0 | data); this is
          NOT a frequentist p-value (which would invert the test). Use it
          as a Bayesian-flavored quick read; for formal hypothesis testing
          use a proper test.
    """
    returns = np.asarray(returns, dtype=float)
    n = len(returns)
    if n < 30:
        raise ValueError(f"need at least 30 samples, got {n}")

    if block_mean is None:
        block_mean = _politis_white_block_length(returns)

    rng = np.random.default_rng(seed)
    actual = float(returns.mean() / (returns.std(ddof=ddof) + 1e-12))

    boot_sharpes = np.empty(n_resample)
    block_int = max(2, int(round(block_mean)))
    for i in range(n_resample):
        if method == "stationary":
            idx = _stationary_bootstrap_indices(n, block_mean, rng)
        else:  # mbb
            idx = _moving_block_bootstrap_indices(n, block_int, rng)
        sample = returns[idx]
        boot_sharpes[i] = sample.mean() / (sample.std(ddof=ddof) + 1e-12)

    alpha = (1 - ci) / 2
    ci_low = float(np.percentile(boot_sharpes, alpha * 100))
    ci_high = float(np.percentile(boot_sharpes, (1 - alpha) * 100))
    prob_neg = float((boot_sharpes <= 0).mean())

    return {
        "n_samples":  n,
        "method":     method,
        "block_mean": round(float(block_mean), 2),
        "actual":     round(actual, 4),
        "boot_mean":  round(float(boot_sharpes.mean()), 4),
        "boot_std":   round(float(boot_sharpes.std(ddof=ddof)), 4),
        "ci_low":     round(ci_low, 4),
        "ci_high":    round(ci_high, 4),
        "prob_neg":   round(prob_neg, 4),
    }


def annualized(per_period_sr: float, periods_per_year: int) -> float:
    """Convert per-period Sharpe to annualized."""
    return per_period_sr * float(np.sqrt(periods_per_year))
