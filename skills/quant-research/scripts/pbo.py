"""pbo.py — Probability of Backtest Overfitting (Bailey, Borwein, López de Prado, Zhu).

Implements Combinatorially Symmetric Cross-Validation (CSCV) per:
  Bailey, D. H., Borwein, J. M., López de Prado, M., & Zhu, Q. J. (2017).
  "The Probability of Backtest Overfitting." *Journal of Computational Finance*.

The PBO estimates the probability that the backtest configuration
selected as best on in-sample data will UNDER-perform the median on
out-of-sample data. Model-free, non-parametric.

Inputs:
    A matrix M of shape (T, N) where:
      - rows = T time observations (e.g., daily returns)
      - cols = N strategy configurations (e.g., hyperparameter grid)
    M[t, n] is the per-period return of configuration n at time t.

CSCV procedure:
    1. Partition T rows into S equal blocks (S typically = 16).
    2. For each combination C(S, S/2) of S/2 blocks (the "training set"):
       - Compute IS rank of each configuration on training rows
       - Compute OOS rank of each configuration on the complementary rows
       - Record: did the IS-best configuration place above or below
         the OOS median?
    3. PBO = fraction of combinations where the IS-best was below the
       OOS median (equivalently, "logit < 0").

Pass condition: PBO ≤ 0.5 (random selection would have PBO ≈ 0.5; useful
strategies should be substantially below).

References:
- See `references/shared/multiple_testing.md` § PBO.
"""

from __future__ import annotations

from itertools import combinations

import numpy as np


def cscv_pbo(
    returns_matrix: np.ndarray,
    *,
    n_blocks: int = 16,
    metric: str = "sharpe",
) -> dict[str, float]:
    """Compute PBO via CSCV.

    Args:
        returns_matrix: shape (T, N). T = time observations, N = config trials.
        n_blocks: number of CSCV blocks S (must be even, typical 16).
        metric: "sharpe" (mean / std, ddof=1) or "mean".

    Returns:
        dict with:
            n_blocks, n_combinations, pbo, mean_logit, mean_rank_loss,
            n_configs, n_obs.

    Notes:
        - n_blocks must be even (CSCV requires symmetric partitioning).
        - Computational cost: C(n_blocks, n_blocks/2) combinations.
          For n_blocks=16 → 12,870 combinations.
        - For very large N (configurations), this is dominated by the
          per-combination metric computation; consider down-sampling
          configurations.
    """
    if n_blocks % 2 != 0:
        raise ValueError(f"n_blocks must be even, got {n_blocks}")
    M = np.asarray(returns_matrix, dtype=float)
    if M.ndim != 2:
        raise ValueError(f"returns_matrix must be 2D, got shape {M.shape}")
    T, N = M.shape
    if T < n_blocks:
        raise ValueError(f"T={T} < n_blocks={n_blocks}; not enough observations")
    if N < 2:
        raise ValueError(f"N={N} configurations; CSCV requires ≥ 2")

    # Partition rows into n_blocks equal-ish chunks
    block_size = T // n_blocks
    blocks: list[np.ndarray] = []
    for b in range(n_blocks):
        start = b * block_size
        end = (b + 1) * block_size if b < n_blocks - 1 else T
        blocks.append(np.arange(start, end))

    half = n_blocks // 2
    block_indices = list(range(n_blocks))

    logits: list[float] = []
    rank_losses: list[float] = []

    for train_block_set in combinations(block_indices, half):
        test_block_set = [b for b in block_indices if b not in train_block_set]

        train_rows = np.concatenate([blocks[b] for b in train_block_set])
        test_rows = np.concatenate([blocks[b] for b in test_block_set])

        train_metric = _compute_metric(M[train_rows], metric)
        test_metric = _compute_metric(M[test_rows], metric)

        # IS-best configuration
        best_is = int(np.argmax(train_metric))

        # OOS rank of the IS-best (1 = worst, N = best)
        oos_ranks = np.argsort(np.argsort(test_metric)) + 1  # ranks in [1, N]
        oos_rank_of_best = int(oos_ranks[best_is])

        # Relative rank loss in [0, 1]: 0 = best in OOS, 1 = worst
        rank_loss = 1 - (oos_rank_of_best - 1) / (N - 1) if N > 1 else 0.0
        rank_losses.append(rank_loss)

        # Logit transform: ln(rank_loss / (1 - rank_loss)).
        # Negative logit = OOS performance below median = overfit indicator.
        # Use percentile-rank style: relative rank in (0, 1)
        pr = oos_rank_of_best / (N + 1)  # avoid 0 / N+1 boundary
        if 0 < pr < 1:
            logit = np.log(pr / (1 - pr))
        else:
            logit = 0.0
        logits.append(logit)

    logits_arr = np.array(logits)
    pbo = float((logits_arr < 0).mean())  # fraction where IS-best ended below OOS median
    return {
        "n_blocks":         n_blocks,
        "n_combinations":   len(logits_arr),
        "pbo":              round(pbo, 4),
        "mean_logit":       round(float(logits_arr.mean()), 4),
        "mean_rank_loss":   round(float(np.mean(rank_losses)), 4),
        "n_configs":        N,
        "n_obs":            T,
    }


def _compute_metric(returns: np.ndarray, metric: str) -> np.ndarray:
    """Compute per-config metric over a subset of rows."""
    if metric == "sharpe":
        means = returns.mean(axis=0)
        stds = returns.std(axis=0, ddof=1)
        return means / (stds + 1e-12)
    if metric == "mean":
        return returns.mean(axis=0)
    raise ValueError(f"unknown metric: {metric!r} (use 'sharpe' or 'mean')")
