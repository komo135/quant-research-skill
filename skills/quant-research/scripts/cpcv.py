"""cpcv.py — Combinatorial Purged Cross Validation (López de Prado, AFML chap 7).

CPCV generates K_choose_test_K combinatorial splits from N folds, where
test_K folds are tested at a time. Combined with purging (drop train samples
whose label horizon overlaps a test fold) and embargo (drop train samples
within a window after a test fold), this produces multiple OOS paths from
the same data — used to estimate backtest overfitting (PBO via CSCV) and
provide more robust OOS estimates than single-path walk-forward.

References:
- López de Prado, M. (2018). *Advances in Financial Machine Learning*,
  Chapter 7 (cross-validation in finance).
- See also `references/shared/time_series_validation.md` and
  `scripts/pbo.py`.

Usage:
    from cpcv import CPCV

    cv = CPCV(n_splits=10, n_test_splits=2, embargo=12, label_horizon=12)
    paths = cv.split(X, target_times=target_end_times)
    for train_idx, test_idx in paths:
        model.fit(X[train_idx], y[train_idx])
        score = model.score(X[test_idx], y[test_idx])
"""

from __future__ import annotations

from itertools import combinations
from typing import Iterator

import numpy as np
import pandas as pd


class CPCV:
    """Combinatorial Purged k-fold CV.

    Args:
        n_splits: total number of folds N (typical: 6-10).
        n_test_splits: number of folds used as test in each path K (typical: 2).
        embargo: number of samples to drop on each side of each test fold.
        label_horizon: max horizon (in samples) of the target.
    """

    def __init__(
        self,
        n_splits: int = 10,
        n_test_splits: int = 2,
        embargo: int = 0,
        label_horizon: int = 0,
    ):
        if n_splits < 2:
            raise ValueError("n_splits must be >= 2")
        if not (1 <= n_test_splits < n_splits):
            raise ValueError("n_test_splits must be in [1, n_splits)")
        self.n_splits = n_splits
        self.n_test_splits = n_test_splits
        self.embargo = max(0, int(embargo))
        self.label_horizon = max(0, int(label_horizon))

    def n_paths(self) -> int:
        """Number of distinct (train, test) paths produced.

        For each combination of n_test_splits folds out of n_splits folds,
        we generate one path. Total = C(n_splits, n_test_splits).
        """
        from math import comb
        return comb(self.n_splits, self.n_test_splits)

    def split(
        self,
        X: pd.DataFrame | np.ndarray,
        target_times: pd.Series | None = None,
    ) -> Iterator[tuple[np.ndarray, np.ndarray]]:
        """Yield (train_idx, test_idx) tuples for each combinatorial path.

        Args:
            X: features (DataFrame or ndarray), time-ordered.
            target_times: optional pd.Series mapping each row to the time at
                which its target ends. If provided, train samples whose target
                window overlaps any test fold are purged. If None, only
                embargo + label_horizon-based purging is applied.

        Yields:
            (train_idx, test_idx): np.ndarray pairs. Each test_idx is the
            concatenation of n_test_splits non-overlapping fold ranges.
        """
        n = len(X)
        indices = np.arange(n)
        fold_size = n // self.n_splits

        # Build fold boundaries [start, end)
        folds: list[tuple[int, int]] = []
        for k in range(self.n_splits):
            start = k * fold_size
            end = (k + 1) * fold_size if k < self.n_splits - 1 else n
            folds.append((start, end))

        if target_times is not None:
            target_times = pd.Series(target_times).reset_index(drop=True)

        # For each combination of n_test_splits folds, yield a (train, test) split
        for test_fold_set in combinations(range(self.n_splits), self.n_test_splits):
            train_mask = np.ones(n, dtype=bool)
            test_idx_list: list[np.ndarray] = []

            for k in test_fold_set:
                start, end = folds[k]
                test_idx_list.append(indices[start:end])
                train_mask[start:end] = False

                # Embargo
                emb_lo = max(0, start - self.embargo)
                emb_hi = min(n, end + self.embargo)
                train_mask[emb_lo:start] = False
                train_mask[end:emb_hi] = False

                # label_horizon purge (left side: train samples whose target
                # would reach into this test fold)
                if self.label_horizon > 0:
                    hz_lo = max(0, start - self.label_horizon)
                    train_mask[hz_lo:start] = False

                # target_times-based purge (precise overlap detection)
                if target_times is not None:
                    if start < len(target_times) and end - 1 < len(target_times):
                        test_time_min = target_times.iloc[start]
                        test_time_max = target_times.iloc[end - 1]
                        if pd.notna(test_time_min) and pd.notna(test_time_max):
                            overlap = (
                                (target_times >= test_time_min) &
                                (target_times <= test_time_max)
                            )
                            train_mask &= ~overlap.values

            test_idx = np.concatenate(test_idx_list)
            yield indices[train_mask], np.sort(test_idx)
