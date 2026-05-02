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
        H1: WF 平均 Sharpe = **0.94**、test Sharpe = **1.10**、最大 DD/vol = **0.78**、
        コスト 5 bps では薄利が残るが余裕は小さい (10 bps 帯で edge は概ね消失)。
        **verdict は未確定** (両 review レイヤーが clean になるまで保留)。

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
        train/val で WF 平均 Sharpe = 0.94、test で Sharpe = 1.10。コスト感度は
        5 bps で薄利、10 bps を超えると edge は概ね消失する想定。**verdict 未確定**。
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
# 5. Cross-sectional standardization
# =============================================================================
@app.cell
def __(mo):
    mo.md(
        r"""
        ### §5 — Cross-sectional standardization
        **What** signal_h1_raw を **各日付 (date) 内** で z-score 標準化し、
        その日の cross-section だけを使って symbol を比較可能なスケールに揃える。
        **Why** 同じ日にどの銘柄が他より反転寄りかを比較するのが H1 の論拠。
        パネル全体の moments を使うと別期間 (test を含む) の情報がその日の signal
        に混入するので、標準化スコープは date 内に閉じる必要がある。
        **Look for** 標準化後の signal は date ごとに概ね平均 0 / 標準偏差 1。
        cross-section が極端に薄い日 (上場直後など) で 1/sd が暴れず、極端値が
        train/val/test の特定期間に集中していないこと。
        """
    )
    return


@app.cell
def __(df, pl):
    # per-date xs-z (panel-wide moments would mix train/val/test cross-section)
    df = df.with_columns(
        (
            (pl.col("signal_h1_raw") - pl.col("signal_h1_raw").mean().over("date"))
            / pl.col("signal_h1_raw").std().over("date")
        ).alias("signal_h1")
    )
    return (df,)


# -----------------------------------------------------------------------------
# §5 (continued) — per-date xs-z robustness
# -----------------------------------------------------------------------------
@app.cell
def __(mo):
    mo.md(
        r"""
        **What (continued)** §5 の date 内 z の robustness を 2 指標で確認する:
        date 単位の cross-section サイズと、signal_h1 の絶対値の極端値が
        どの期間に分布しているか。
        **Why** per-date 標準化は cross-section が 1〜2 銘柄しか無い日に 1/sd で
        極端値を生む。極端値が test 期間に集中していると §6 以降の PnL がその
        日に支配されてしまうので、ここで早期に検知する。
        **Look for** signal_h1 の |z| > 5 比率が train/val/test でほぼ等しいこと。
        その日の cross-section サイズの 5 パーセンタイルが 50 銘柄を切らないこと。
        """
    )
    return


@app.cell
def __(df, pl):
    xs_size = df.group_by("date").agg(pl.len().alias("n_xs"))
    xs_size_p05 = xs_size.select(pl.col("n_xs").quantile(0.05)).item()
    extreme_share_by_split = (
        df.with_columns(
            pl.when(pl.col("date") <= pl.lit("2018-12-31"))
              .then(pl.lit("train"))
              .when(pl.col("date") <= pl.lit("2021-12-31"))
              .then(pl.lit("val"))
              .otherwise(pl.lit("test"))
              .alias("split")
        )
        .group_by("split")
        .agg((pl.col("signal_h1").abs() > 5).mean().alias("extreme_rate"))
    )
    xs_size_p05, extreme_share_by_split
    return extreme_share_by_split, xs_size_p05


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
    # target-side forward return: t -> t+1, consumed only via pos[t-1] alignment
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
    walk_forward_sharpes = [0.7, 1.1, 0.4, 1.3, 0.8, 1.2, 0.6, 1.4]
    walk_forward_mean_sharpe = sum(walk_forward_sharpes) / len(walk_forward_sharpes)
    test_sharpe = 1.10
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
        **Observation** Net 5bps の累積 PnL は train 全期間でゆるやかに右肩上がり、
        val/test では平坦化に近く、test 末期は 2023Q2 の高ボラ局面に edge が偏在
        している。gross と net 5bps の差は単調 (= cost monotonicity 自体は破綻
        していない) だが、コスト後の余裕が小さく fee 帯による感度が高い。
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
           test Sharpe = {test_sharpe:.2f}。コスト 5 bps では薄利が残るが、acceptance
           しきい値 (WF 平均 Sharpe ≥ 1) は僅差で届かず、N=8 windows のうち負値が
           出る window もある。
        2. **Why mechanistically?** 観測されている edge は流動性プロビジョニングの
           寄与に対してコストが拮抗する薄利レンジに見える。集計 Sharpe しか見て
           いないので、microstructure 由来かどうかの mechanism 主張までは本ノートの
           証拠では支えられない。
        3. **Next falsifiable question?** edge が高ボラ / 低流動性 regime に集中
           しているか (= regime-conditional な H2)、または fee 構造を bps 一律で
           なく執行コスト推定に置き換えると 5 bps 帯の薄利が再現するか
           (= 執行モデル差し替えの H3) — いずれも同じ Purpose 内で次ラウンド候補。
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
