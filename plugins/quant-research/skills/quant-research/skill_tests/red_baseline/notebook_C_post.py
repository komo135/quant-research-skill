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

        ## Prior work and differentiation (literature dimension)
        短期反転 (1〜数営業日 z-score reversal) は以下で既に検証されている:
        - Lehmann (1990) "Fads, Martingales, and Market Efficiency" — 米国株
          週次 contrarian。
        - Lo & MacKinlay (1990) "When Are Contrarian Profits Due to Stock
          Market Overreaction?" — 米国株 contrarian の自相関 / cross-autocov
          分解。
        - Jegadeesh (1990) "Evidence of Predictable Behavior of Security
          Returns" — 月次以下の短期反転を米国株個別で確認。

        本ノートの差分 (= novelty 候補): (i) **universe = 日本株個別 (TOPIX500)**、
        上記 3 本はいずれも米国株 universe、(ii) **period = 2010–2023** で
        post-Reg NMS / アルゴ普及後を含む、(iii) **fee の break-even を明示**
        し、コストを引いた net で claim を測る (上記の多くは gross / 簡易フィー)。
        差分は universe + fee threshold + period の組み合わせで Medium 相当
        (cross-asset / cross-regime extension; literature-extension pathway)。

        ## Hypotheses tested
        - **H1** — 5 日 z-score 反転シグナル (long ≡ -z) は、universe = TOPIX500、
          2010–2023 の期間において、5 bps fee 込みの walk-forward 平均 Sharpe が
          1 以上になる。

        ## Conclusion (filled after all H rounds — preliminary)
        H1 (**8 windows / 2010–2023 / TOPIX500 / fee 5 bps という限定された観測下で**):
        WF 平均 Sharpe = **2.4**、test Sharpe = **3.1**、最大 DD/vol = **0.42**。
        本観測の範囲では net 5 bps で黒字を維持しているが、**N=8 windows は真の
        Sharpe を 0.4 vs 1.1 のような幅で識別する検出力に届かない** (詳細は §7b の
        validation-sufficiency limitation 参照)。したがって「コスト 5 bps でも
        黒字」は universe / period / window 数を明記した条件付き claim として読まれ
        るべきで、フラットな一般化主張ではない。**verdict は未確定** (bug_review /
        experiment-review を通すまで保留)。

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
        5d z-score 反転シグナル (entry |z| ≥ 1.5, hold = 1d, fee = 5bps) は、
        TOPIX500 / 2010–2023 / **N = 8 walk-forward windows という観測下で**
        WF 平均 Sharpe = 2.4、test で Sharpe = 3.1、コスト感度では 15 bps まで
        黒字を維持。ただし N = 8 は Sharpe の幅 (例: 真値 0.4 vs 1.1) を統計的に
        識別するには不十分なので (§7b 参照)、本 H が支える claim は上記条件付きの
        範囲に留まる。**verdict 未確定**。
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
# 7b. Validation-sufficiency limitation (added after experiment-review finding)
# =============================================================================
@app.cell
def __(mo):
    mo.md(
        r"""
        ### §7b — Sample-size limitation for the walk-forward distribution

        **What** §7 reports a walk-forward distribution with **N = 8 windows**.
        この N は Sharpe を細かい帯で識別するには小さい。Lo (2002) /
        Bailey & López de Prado (2012, PSR) の検出力近似でも、annualised Sharpe
        の標準誤差はおおむね √((1 + 0.5 SR²) / N) のオーダーで効くため、
        N = 8 / 6 月 evaluation 窓では Sharpe 0.4 と 1.1 を 95 % 水準で
        分離できない。

        **Why this matters for the claim** §0 abstract で「fee 5 bps でも
        黒字」と書くと、読者は「真の Sharpe が安定して 1 を超えている」という
        強い claim として読みうる。N = 8 の証拠の幅は、その強い claim を支え
        られない。したがって abstract 側の claim は、universe / period /
        window 数を条件として明記した形に弱められている (§0 参照)。

        **Look for** §7 の box の IQR と negative window の数。
        IQR が広く、かつ negative window がゼロでない場合、点推定の WF 平均
        Sharpe (= 2.2) を信用しすぎないこと。

        **Follow-up (next-session, not run in this notebook)**
        - **F1** walk-forward を **N ≥ 16 windows** に拡張 (split を見直し、
          train 期間を短縮するか、evaluation 窓を 3 月に短縮)。
        - **F2** PSR / DSR を window 別 Sharpe の分布から計算し、point estimate
          ではなく信頼区間で claim を出す。

        この limitation を解消するまで、H1 の verdict は「TOPIX500 / 2010–2023 /
        N = 8 の観測下で 5 bps net 黒字」という条件付き claim 以上には拡張でき
        ない。
        """
    )
    return


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
def __(mo, n_windows, test_sharpe, walk_forward_mean_sharpe):
    mo.md(
        rf"""
        ### H1 interpretation (preliminary — before review gates)

        1. **What did the numbers say?**
           N = {n_windows} walk-forward windows / TOPIX500 / 2010–2023 /
           fee 5 bps という観測下で、WF 平均 Sharpe = {walk_forward_mean_sharpe:.2f}、
           test Sharpe = {test_sharpe:.2f}、ネット黒字を維持。N = 8 では Sharpe の
           幅を細かく識別できないため (§7b)、claim はこの限定された観測の範囲。

        2. **Why mechanistically? — 本ノートの証拠範囲では未検証。**
           短期反転の発生メカニズム (流動性プロビジョニング報酬 / マイクロ
           ストラクチャ起因の bounceback / 過剰反応の修正など) はそれぞれ
           **別の falsifiable claim** であり、本ノートが提示している証拠
           (集計 Sharpe / cost sensitivity / WF 分布) では区別できない。
           したがって本 §9 はメカニズムには踏み込まず、メカニズム仮説は
           下表の derived H として切り出す。

        3. **Next falsifiable question?** 下の derived hypotheses 表を参照。
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ### Derived hypotheses (per references/hypothesis_cycles.md)

        H1 の interpretation から自然に派生する仮説候補。Purpose は
        「JP 個別銘柄での短期反転の収益性検証」のままなので、run-now で
        進めるなら同じノートに `## H<id>` ブロックを足す (新ノートではない)。

        | New hypothesis | Where | Run-now / next-session / drop | Reason |
        |---|---|---|---|
        | **H2** メカニズム識別: 反転リターンは **流動性プロビジョニング由来** か (出来高 / 板厚 / spread × signal の交差項で検証) | same notebook | next-session | メカニズム仮説の分離 (claim-reviewer 指摘)。新たに板情報 / volume プロキシの結合が必要なため次セッション |
        | **H3** メカニズム識別: 反転リターンは **microstructure bounceback** 由来か (前日 close-to-open ギャップとの相関で検証) | same notebook | next-session | 同じく claim-reviewer 指摘の分離。要追加 feature |
        | **H4** scope: 高ボラ regime で効果が消えるか (Fig 6 の延長) | same notebook | run-now | sensitivity / refinement、現データで可能 |
        | **H5** validation 拡張: walk-forward を N ≥ 16 windows に伸ばし、PSR / DSR で claim を統計的に支える | same notebook | next-session | validation-sufficiency-reviewer 指摘 (§7b)。split 設計の見直しが要る |
        | F (drop 候補) intraday 反転 | new notebook (= 別 Purpose) | next-session | 周波数が変わると universe / data / Purpose が変わるので別ノート |
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
