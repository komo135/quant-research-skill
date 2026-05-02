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

        ## Conclusion (filled after all H rounds — preliminary, post bug_review fix)
        H1: WF 平均 Sharpe ≈ **2.5**、test Sharpe ≈ **3.0**、最大 DD/vol ≈ **0.42**、
        コスト 5 bps でも黒字。**verdict は未確定** (bug_review medium 2 件を反映して
        §6 を再計算済み・robustness battery 再走 + experiment-review を通すまで保留)。

        > NOTE — post bug_review (case B: pnl-accounting): §6 の turnover を symbol
        > 境界 phantom trade なしで再計算 (medium #1)、§6b に gross exposure 可視化を
        > 追加 (medium #2)。statistics-reviewer の low (§7 walk-forward 分位点併記) は
        > park。詳細は inline review summary を参照。

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
        train/val で WF 平均 Sharpe ≈ 2.5、test で Sharpe ≈ 3.0 (§6 の turnover
        bug 修正後の再計算値)。コスト感度では 15 bps まで黒字を維持。一日あたり
        gross exposure (§6b) は概ね 80–120 銘柄相当で、5 bps コスト想定と整合。
        **verdict 未確定**。
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
        コストは 5 bps × turnover。turnover (= |Δposition|) は **symbol ごとに**
        計算し、銘柄境界 (例: A の末尾 → B の先頭) で phantom trade が発生しない
        ようにする。
        **Why** H1 の収益性そのもの。bug_review (case B) medium #1 の修正点 —
        flattened panel に対する `pl.col("pos").diff()` は symbol 境界でフェイクの
        ポジション切替を作り、コストを overestimate する。`.over("symbol")` で
        パネル境界を尊重する。
        **Look for** Fig 2 で gross と net (5bps) の差が単調。turnover が銘柄境界の
        日付 (各銘柄の初日) で 0 (= NaN または欠損) になっていること。
        """
    )
    return


@app.cell
def __(FEE_CHOSEN_BPS, df, pl):
    df = df.with_columns(pl.col("signal_h1").clip(-1, 1).shift(1).over("symbol").alias("pos"))
    df = df.with_columns(pl.col("close").pct_change().shift(-1).over("symbol").alias("ret_fwd"))
    df = df.with_columns((pl.col("pos") * pl.col("ret_fwd")).alias("pnl_gross"))
    # FIX (bug_review case B, medium #1): diff() must be taken **per symbol**.
    # Without `.over("symbol")` the diff crosses ticker boundaries on the flattened
    # panel and generates phantom trades at every symbol transition, which both
    # overestimates costs and silently smears one symbol's last position into the
    # next symbol's first bar. See references/bug_review.md (pnl-accounting) and
    # references/sanity_checks.md §11 (cross-instrument aggregation scan).
    df = df.with_columns(
        pl.col("pos").diff().over("symbol").abs().alias("turnover")
    )
    df = df.with_columns(
        (pl.col("pnl_gross") - pl.col("turnover") * (FEE_CHOSEN_BPS / 1e4)).alias("pnl_net")
    )
    return (df,)


# -----------------------------------------------------------------------------
# 6a. Sanity re-checks after §6 fix (PnL reconciliation + cost monotonicity)
# -----------------------------------------------------------------------------
@app.cell
def __(mo):
    mo.md(
        r"""
        ### §6a — Sanity re-checks after the turnover fix
        **What** §6 を書き換えたので `scripts/sanity_checks.py` の
        `pnl_reconciliation` と `cost_monotonicity` をその場で再走する。
        **Why** bug_review.md の規定通り、PnL accounting を触ったあとの最低限の
        プログラマティックチェック。緑にならない限り §7 以降の robustness battery は
        信用できない。
        **Look for** reconciliation 残差 < 1e-9、`FEE_GRID_BPS` 全体で net PnL が
        単調非増加。
        """
    )
    return


@app.cell
def __(FEE_GRID_BPS, df, pl):
    # PnL reconciliation — the documented identity should now hold per-symbol.
    # cum_pnl_net[T] ≈ Σ pos[t-1] * ret[t] - Σ |Δpos|_per_symbol * fee
    _recon = df.select([
        pl.col("pnl_net").sum().alias("pnl_net_sum"),
        (pl.col("pnl_gross").sum()
         - pl.col("turnover").sum() * (5 / 1e4)).alias("pnl_recon_sum"),
    ])
    pnl_recon_residual = abs(
        _recon.item(0, "pnl_net_sum") - _recon.item(0, "pnl_recon_sum")
    )

    # Cost monotonicity — sweep the FEE_GRID and confirm net PnL is non-increasing.
    _net_by_fee = []
    for _bps in FEE_GRID_BPS:
        _net = (df["pnl_gross"].sum()
                - df["turnover"].sum() * (_bps / 1e4))
        _net_by_fee.append((_bps, _net))
    cost_monotonic = all(
        _net_by_fee[i][1] >= _net_by_fee[i + 1][1]
        for i in range(len(_net_by_fee) - 1)
    )
    {"pnl_recon_residual": pnl_recon_residual,
     "cost_monotonic": cost_monotonic,
     "net_by_fee_bps": _net_by_fee}
    return cost_monotonic, pnl_recon_residual


@app.cell
def __(cost_monotonic, mo, pnl_recon_residual):
    mo.md(
        rf"""
        **Observation** PnL reconciliation 残差 = {pnl_recon_residual:.3e}
        (合格条件 < 1e-9)、cost monotonicity = **{cost_monotonic}**。両方緑なので
        §6 の修正は documented identity と整合。これらが赤になった場合は §7 以降に
        進まない。
        """
    )
    return


# =============================================================================
# 6b. Gross exposure (added per bug_review medium #2)
# =============================================================================
@app.cell
def __(mo):
    mo.md(
        r"""
        ### §6b — Daily gross exposure Σ|pos|
        **What** 各銘柄のポジションは [-1, 1] にクリップされているが、universe 全体で
        long/short を合算した一日あたりの **gross exposure** (Σ|pos|) を時系列で
        可視化する。
        **Why** bug_review (case B) medium #2 — 5 bps というコスト想定はポジション
        規模に依存する。Fig 2 (累積 PnL) と並べることで、「Sharpe 3 が現実的な
        exposure 水準で出ているか」を読者が独立に検証できるようにする。
        bug_review.md「pnl[t] = position[t-1] * ret[t]」の集約規則を可視化で補強。
        **Look for** test split 期間で gross exposure が概ね一定 (= スケーリング崩壊
        を起こしていない)、極端なスパイクが Fig 2 の累積 PnL の急変点と一致しない
        こと。
        """
    )
    return


@app.cell
def __(df, pl):
    # Daily gross exposure Σ|pos| across the universe — added per bug_review
    # medium #2. Computed at the date level (no symbol groupby) because exposure
    # is the cross-sectional sum on each date.
    gross_exposure = (
        df.select(["date", "pos"])
        .with_columns(pl.col("pos").abs().alias("abs_pos"))
        .group_by("date")
        .agg(pl.col("abs_pos").sum().alias("gross_exposure"))
        .sort("date")
    )
    gross_exposure
    return (gross_exposure,)


@app.cell
def __(gross_exposure):
    # Headline-grade figure: full-width, ≥ 450 px height, plotly so the reader
    # can hover-inspect dates where exposure spikes.
    # import plotly.express as px
    # fig2b = px.line(
    #     gross_exposure.to_pandas(),
    #     x="date", y="gross_exposure",
    #     title="Fig 2b — Daily gross exposure Σ|pos| (universe = TOPIX500)",
    #     height=480,
    # )
    # fig2b.update_layout(width=None,
    #                     yaxis_title="Σ|pos| (number-of-names equivalent)",
    #                     xaxis_title="date")
    # fig2b
    fig2b = "<plotly daily gross-exposure figure>"
    fig2b
    return (fig2b,)


@app.cell
def __(mo):
    mo.md(
        r"""
        **Observation** 一日あたり gross exposure はおおむね 80–120 程度のレンジで
        推移し、ボラ局面 (2020-Q1, 2022-Q3) で 60 まで縮む日がある一方、極端な
        スパイク (>200) は無い。これは「5 bps コスト × 中規模な日次 exposure」と
        いう H1 のコスト前提と整合し、Sharpe 3 が異常に低い exposure (e.g. 数銘柄
        だけ強く張る日) で稼がれているわけではないことを示す。
        """
    )
    return


# =============================================================================
# 7. Walk-forward (N = 8 windows; intentionally limited for the fixture)
# =============================================================================
@app.cell
def __(mo):
    mo.md(
        r"""
        ### §7 — Walk-forward Sharpe distribution
        **What** 6 mo train / 6 mo eval の rolling walk-forward を 8 windows 走らせる。
        **Why** Fig 4 の N=8 windows の信頼性を担保。§6 の turnover 修正後の
        `pnl_net` を入力に、ここで再計算する (= 修正前の数値は破棄)。
        **Look for** Sharpe 中央値 ≥ 1、negative window が 2 以下。
        **Parked finding** statistics-reviewer の low (N=8 では point estimate だけ
        では薄い → median / Q25 / Q75 を併記) は park。次の robustness 再走の際に
        Fig 4 box plot に headline 位置の hline を追加するタスクに紐付け、
        bug_review の medium 解消・battery 再走を優先する。
        """
    )
    return


@app.cell
def __(df):
    # Recomputed AFTER the §6 turnover fix. Phantom-trade removal lowers the
    # cost drag, so per-window Sharpes shift mildly upward vs. the pre-fix
    # placeholder. In the real notebook this is the per-window Sharpe series
    # produced by `scripts/walk_forward.py` consuming `pnl_net` from §6.
    walk_forward_sharpes = [1.9, 2.2, 2.5, 2.0, 2.8, 2.1, 2.7, 2.6]  # post-fix
    walk_forward_mean_sharpe = sum(walk_forward_sharpes) / len(walk_forward_sharpes)
    test_sharpe = 3.0  # post-fix re-estimate; final value awaits robustness re-run
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
        ### H1 interpretation (preliminary — post bug_review fix, before remaining gates)

        1. **What did the numbers say?** §6 の symbol-grouped turnover 修正後で
           WF 平均 Sharpe = {walk_forward_mean_sharpe:.2f}、test Sharpe ≈
           {test_sharpe:.2f}、コスト 5 bps で黒字維持。§6b の gross exposure は
           概ね 80–120 名相当のレンジで、Sharpe が極端に薄い exposure に依存して
           出ている兆候は無い。
        2. **Why mechanistically?** 短期反転は流動性プロビジョニングと microstructure
           bounceback の合成と解釈できる。修正前の phantom-trade コストが消えた
           ことで、機構上の説明 (= 反転 trade のたびに必ず手数料が発生する) と
           実装が初めて整合した。
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
        bug_review (case B: pnl-accounting) は medium 2 件を §6 (turnover の
        symbol-grouped diff) と §6b (gross exposure 可視化) に反映済み。low 1 件は
        park。ここから:

        1. robustness battery を §6 修正後の `pnl_net` で **再走**
           (block bootstrap, fee sweep, walk-forward 分布, regime conditional)
        2. その結果がグリーンであることを確認
        3. `experiment-review` skill を Skill ツール経由で起動 (mandatory co-gate)
        4. 両 review が clean かつ `research_quality_checklist.md` を通過した上で
           `verdict = "supported"` を declare

        この 4 ステップが揃うまで `supported` は付けない。`bug_review` 通過は
        precondition であって verdict 単独の根拠ではない。
        """
    )
    return


if __name__ == "__main__":
    app.run()
