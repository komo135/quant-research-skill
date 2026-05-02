# /// script
# requires-python = ">=3.10"
# ///
"""
exp_001_jp_eq_short_term_reversion.py

This is a fixture used by skills/quant-research/skill_tests/. It mimics the
state of an experiment notebook *just before* a triggered review fires —
H1 is run, headline numbers are in the abstract, but verdict is not yet
declared and bug_review / experiment-review have not yet returned findings.

It follows references/notebook_narrative.md (purpose abstract, figure plan,
per-section what&why, per-figure observation, per-H interpretation, config
cell at the top of the H block, named constants).
"""

import marimo

__generated_with = "0.9.0"
app = marimo.App(width="full")


# =============================================================================
# 0. Title & Purpose-level abstract
# =============================================================================
@app.cell
def __():
    import marimo as mo
    mo.md(
        r"""
        # exp_001 — JP 個別銘柄 短期反転 (1〜3 営業日 reversion) の収益性

        ## Purpose
        日本株個別銘柄に対する 1〜3 営業日の短期反転シグナルが、現実的な手数料
        (約定込み 5 bps) を引いてもプラスの期待値を持つかを検証する。

        ## Hypotheses tested
        - **H1** — 5 日 z-score 反転シグナル (long ≡ -z) は、universe = TOPIX500、
          2010–2023 の期間において、5 bps fee 込みの walk-forward 平均 Sharpe が
          1 以上になる。

        ## Conclusion (filled after all H rounds — preliminary)
        H1: WF 平均 Sharpe = **2.4**、test Sharpe = **3.1**、最大 DD/vol = **0.42**、
        コスト 5 bps でも黒字。**verdict は未確定** (bug_review / experiment-review
        を通すまで保留)。

        ## Why this matters
        個人投資家・小規模ファンドが現実的にアクセスできる universe / コスト水準で
        短期反転が黒字化するなら、数日サイクルのオーバーレイとして使える。
        逆に黒字化しないなら、この universe では中期戦略にスイッチする根拠になる。

        ## Figure plan (decided up-front, before running H1)
        - **Fig 1** — Universe + train/val/test split overlay
        - **Fig 2** — H1 累積 PnL (gross / net 5bps) を 3 splits 縦線つきで
        - **Fig 3** — コスト感度 (0/3/5/10/15 bps) と headline marker
        - **Fig 4** — Walk-forward window 別 Sharpe 分布 (box, N=8 windows)
        - **Fig 5** — Bootstrap Sharpe 分布 (block bootstrap, B=2000)
        - **Fig 6** — Regime conditional (trending/ranging × high/low vol)
        """
    )
    return (mo,)


# =============================================================================
# 1. Imports & data load
# =============================================================================
@app.cell
def __(mo):
    mo.md(
        r"""
        ## §1 — Data load

        **What** TOPIX500 個別銘柄の日次 OHLCV を読み込む。
        **Why** universe 固定が figure plan §1 (split overlay) と H1 の前提。
        **Look for** symbol × date のユニーク制約と、日付範囲が 2010-01-04 〜
        2023-12-29 になっていること。
        """
    )
    return


@app.cell
def __():
    import polars as pl
    import numpy as np
    raw = pl.read_parquet("data/jp_eq_topix500.parquet").sort(["symbol", "date"])
    return np, pl, raw


# =============================================================================
# 2. H1 config cell (top of H1 block, named constants only)
# =============================================================================
@app.cell
def __(mo):
    mo.md(r"## H1 — 5d z-score reversion")
    return


@app.cell
def __():
    # H1 config — sweep ranges and chosen point (no raw literals downstream)
    Z_WINDOW = 5                         # rolling window for z-score
    Z_TAU_GRID = [1.0, 1.5, 2.0, 2.5]    # entry threshold sweep (|z| ≥ TAU)
    Z_TAU_CHOSEN = 1.5                   # H1 reported configuration
    HOLD_GRID = [1, 2, 3]                # bars
    HOLD_CHOSEN = 1
    FEE_GRID_BPS = [0, 3, 5, 10, 15]
    FEE_CHOSEN_BPS = 5
    UNIVERSE = "TOPIX500"
    SPLIT = {"train": "2010-01-04..2018-12-31",
             "val":   "2019-01-01..2021-12-31",
             "test":  "2022-01-01..2023-12-29"}
    return (FEE_CHOSEN_BPS, FEE_GRID_BPS, HOLD_CHOSEN, HOLD_GRID,
            SPLIT, UNIVERSE, Z_TAU_CHOSEN, Z_TAU_GRID, Z_WINDOW)


# =============================================================================
# 3. H1 per-H abstract
# =============================================================================
@app.cell
def __(mo):
    mo.md(
        r"""
        ### H1 abstract
        5d z-score 反転シグナル (entry |z| ≥ 1.5, hold = 1d, fee = 5bps) は
        train/val で WF 平均 Sharpe = 2.4、test で Sharpe = 3.1。コスト感度では
        15 bps まで黒字を維持。**verdict 未確定**。
        """
    )
    return


# =============================================================================
# 4. Feature: 5d z-score and signal
# =============================================================================
@app.cell
def __(mo):
    mo.md(
        r"""
        ### §4 — Signal construction
        **What** 5 日 rolling z-score を符号反転して反転シグナルとする。
        **Why** H1 の central claim そのもの。
        **Look for** symbol ごとに rolling window が分離していること。
        """
    )
    return


@app.cell
def __(Z_WINDOW, pl, raw):
    df = raw.with_columns(pl.col("close").pct_change().over("symbol").alias("ret_1d"))
    df = df.with_columns([
        pl.col("ret_1d").rolling_mean(Z_WINDOW).over("symbol").alias("mu5"),
        pl.col("ret_1d").rolling_std(Z_WINDOW).over("symbol").alias("sd5"),
    ])
    df = df.with_columns(((pl.col("ret_1d") - pl.col("mu5")) / pl.col("sd5")).alias("z5"))
    df = df.with_columns((-pl.col("z5")).alias("signal_h1_raw"))
    return (df,)


# =============================================================================
# 5. Cross-sectional standardization  (← look-ahead leak lives here)
# =============================================================================
@app.cell
def __(mo):
    mo.md(
        r"""
        ### §5 — Cross-sectional standardization
        **What** signal_h1_raw をパネル全体で z-score 標準化する。
        **Why** symbol 間の cross-section ランキングを行うため。
        **Look for** 標準化後の signal が概ね N(0, 1)。
        """
    )
    return


@app.cell
def __(df, pl):
    # WHOLE-PERIOD standardization (intentionally leaky for the fixture)
    mu = df.select(pl.col("signal_h1_raw").mean()).item()
    sd = df.select(pl.col("signal_h1_raw").std()).item()
    df = df.with_columns(((pl.col("signal_h1_raw") - mu) / sd).alias("signal_h1"))
    return (df,)


# =============================================================================
# 6. Position, PnL, turnover  (← flattened-panel cost bug lives here)
# =============================================================================
@app.cell
def __(mo):
    mo.md(
        r"""
        ### §6 — Position, PnL, turnover
        **What** signal を [-1, 1] にクリップしてポジション化、t-1 → t で発注、
        コストは 5 bps × turnover。
        **Why** H1 の収益性そのもの。
        **Look for** Fig 2 で gross と net (5bps) の差が単調。
        """
    )
    return


@app.cell
def __(FEE_CHOSEN_BPS, df, pl):
    df = df.with_columns(pl.col("signal_h1").clip(-1, 1).shift(1).over("symbol").alias("pos"))
    df = df.with_columns(pl.col("close").pct_change().shift(-1).over("symbol").alias("ret_fwd"))
    df = df.with_columns((pl.col("pos") * pl.col("ret_fwd")).alias("pnl_gross"))
    # NOTE: diff() over the flattened panel introduces phantom trades at
    # ticker boundaries (intentional bug in this fixture).
    df = df.with_columns(pl.col("pos").diff().abs().alias("turnover"))
    df = df.with_columns(
        (pl.col("pnl_gross") - pl.col("turnover") * (FEE_CHOSEN_BPS / 1e4)).alias("pnl_net")
    )
    return (df,)


# =============================================================================
# 7. Walk-forward (N = 8 windows; intentionally limited for the fixture)
# =============================================================================
@app.cell
def __(mo):
    mo.md(
        r"""
        ### §7 — Walk-forward Sharpe distribution
        **What** 6 mo train / 6 mo eval の rolling walk-forward を 8 windows 走らせる。
        **Why** Fig 4 の N=8 windows の信頼性を担保。
        **Look for** Sharpe 中央値 ≥ 1、negative window が 2 以下。
        """
    )
    return


@app.cell
def __(df):
    # placeholder: in the real notebook this returns the per-window Sharpe series
    walk_forward_sharpes = [1.8, 2.1, 2.4, 1.9, 2.7, 2.0, 2.6, 2.5]
    walk_forward_mean_sharpe = sum(walk_forward_sharpes) / len(walk_forward_sharpes)
    test_sharpe = 3.1
    n_windows = len(walk_forward_sharpes)
    return n_windows, test_sharpe, walk_forward_mean_sharpe, walk_forward_sharpes


# =============================================================================
# 8. Headline figure (Fig 2 — cumulative PnL)
# =============================================================================
@app.cell
def __(mo):
    mo.md(
        r"""
        ### Fig 2 — H1 cumulative PnL (gross vs net 5bps), 3 splits overlay
        """
    )
    return


@app.cell
def __(df):
    # placeholder figure object
    fig2 = "<plotly cumulative PnL figure>"
    fig2
    return (fig2,)


@app.cell
def __(mo):
    mo.md(
        r"""
        **Observation** Net 5bps は全 3 splits でほぼ単調増加。test split (2022–2023)
        では 2022Q3 の急落局面でも回復しており、regime 依存性は限定的に見える。
        """
    )
    return


# =============================================================================
# 9. Per-H interpretation (before any verdict)
# =============================================================================
@app.cell
def __(mo, test_sharpe, walk_forward_mean_sharpe):
    mo.md(
        rf"""
        ### H1 interpretation (preliminary — before review gates)

        1. **What did the numbers say?** WF 平均 Sharpe = {walk_forward_mean_sharpe:.2f}、
           test Sharpe = {test_sharpe:.2f}、コスト 5 bps で黒字維持。
        2. **Why mechanistically?** 短期反転は流動性プロビジョニングと microstructure
           bounceback の合成と解釈できる。
        3. **Next falsifiable question?** より高頻度 (intraday) で同じ効果が残るか、
           または高ボラ regime で消えるか — derived H 候補。
        """
    )
    return


# =============================================================================
# 10. Verdict (NOT YET SET — bug_review / experiment-review pending)
# =============================================================================
@app.cell
def __(mo):
    mo.md(
        r"""
        ### H1 verdict — **PENDING**
        bug_review / experiment-review を通過するまで `supported` は付けない。
        """
    )
    return


if __name__ == "__main__":
    app.run()
