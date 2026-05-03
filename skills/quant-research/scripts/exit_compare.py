"""exit_compare.py — Parallel comparison of exit strategy types.

Per `references/shared/exit_strategy_design.md`: every strategy backtest
must compare ≥3 exit types in parallel (signal-flip / TP-SL / trailing /
time-stop / etc.) before selecting one.

This helper takes a callable `run_backtest(exit_kwargs)` and a list of
exit configurations, runs them in parallel (sequential here; the caller
can wrap in joblib if desired), and produces a comparison table.

Usage:
    from exit_compare import compare_exits

    results = compare_exits(
        run_backtest=lambda kw: my_backtest(close, entries, **kw),
        exit_configs={
            "signal_flip": {"exits": signal_flip_exits},
            "atr_tp_sl":   {"sl_stop": 0.02, "tp_stop": 0.05},
            "atr_trail":   {"sl_stop": 0.03, "sl_trail": True},
            "time_stop":   {"max_hold": 96},
        },
        metrics=["sharpe", "win_rate", "avg_hold", "max_drawdown"],
    )
"""

from __future__ import annotations

from typing import Any, Callable

import numpy as np
import pandas as pd


def compare_exits(
    run_backtest: Callable[[dict], dict[str, float]],
    exit_configs: dict[str, dict[str, Any]],
    *,
    metrics: list[str] | None = None,
) -> pd.DataFrame:
    """Run a backtest with each exit configuration; tabulate results.

    Args:
        run_backtest: callable taking exit_kwargs dict, returning a dict of
            metrics. Example return: {"sharpe": 1.2, "max_drawdown": -0.15}.
        exit_configs: dict mapping exit name → kwargs passed to run_backtest.
        metrics: optional list of metric names to include in the output. If
            None, all metrics returned by run_backtest are included.

    Returns:
        pandas DataFrame indexed by exit name, with metrics as columns.
        Includes a `comparison_rank` column ranking exits by sharpe (or
        first metric if sharpe absent).
    """
    if len(exit_configs) < 3:
        print(
            f"warning: comparing only {len(exit_configs)} exit type(s). "
            "Per references/shared/exit_strategy_design.md, ≥3 exit types "
            "are required for a complete comparison."
        )

    rows = {}
    for name, kwargs in exit_configs.items():
        try:
            metrics_dict = run_backtest(kwargs)
        except Exception as exc:  # noqa: BLE001
            print(f"warning: exit '{name}' failed: {exc}")
            metrics_dict = {}
        if metrics is not None:
            metrics_dict = {k: metrics_dict.get(k, float("nan")) for k in metrics}
        rows[name] = metrics_dict

    df = pd.DataFrame(rows).T

    # Add a comparison rank by sharpe (descending) if available, else first column
    rank_col = "sharpe" if "sharpe" in df.columns else (df.columns[0] if not df.empty else None)
    if rank_col and len(df) > 1:
        df["comparison_rank"] = df[rank_col].rank(ascending=False, method="dense").astype(int)

    return df


def time_stop_safety_net(
    primary_exits: pd.Series,
    entries: pd.Series,
    max_hold: int,
) -> pd.Series:
    """Combine a primary exit (e.g., signal-flip) with a time-stop safety net.

    Per `references/shared/exit_strategy_design.md`: time-stop alone is NOT
    a valid exit. It is acceptable as a safety net combined with a primary
    exit.

    Args:
        primary_exits: boolean Series, True where primary exit fires.
        entries: boolean Series, True where entries fire.
        max_hold: max bars to hold before forced exit.

    Returns:
        Combined exit Series (primary OR time-stop).
    """
    safety = entries.shift(max_hold).fillna(False).astype(bool)
    return primary_exits | safety
