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

        ## Prior work and differentiation
        短期反転自体は Lehmann (1990, *QJE*)、Lo & MacKinlay (1990, *RFS*)、
        Jegadeesh (1990, *JF*) で米国株式に対して既に検証されている。本ノートの
        差分は (i) universe = 日本株個別銘柄 (TOPIX500)、(ii) 約定込み 5 bps の
        現実的なコスト水準での黒字化判定、(iii) 2010–2023 という post-Abenomics 期間
        の 3 点。先行研究の中核命題そのものではなく、これら 3 軸での再検証として
        位置づける。
        詳細な差分は `literature/differentiation.md` を参照。

        ## Conclusion (filled after all H rounds — preliminary)
        H1: TOPIX500 / 2010–2023 / N=8 walk-forward windows という観測下で、
        WF 平均 Sharpe = **2.4**、test Sharpe = **3.1**、最大 DD/vol = **0.42**。
        コスト 5 bps においてもこの観測幅では黒字。観測の幅 (N=8) は Sharpe 0.4
        と 1.1 を統計的に弁別する検出力には足りない (詳細は `## Post-review addenda`
        A1 を参照) ので、claim は上記の観測条件下に限定される。
        **verdict は未確定**。

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
        TOPIX500 / 2010–2023 / N=8 walk-forward windows の観測下で、train/val
        の WF 平均 Sharpe = 2.4、test Sharpe = 3.1。コスト感度では 15 bps まで
        黒字を維持。N=8 windows は Sharpe 0.4 vs 1.1 を区別する検出力に足りない
        ため、claim はこの観測幅に限定する (`## Post-review addenda` A1)。
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

        1. **What did the numbers say?** TOPIX500 / 2010–2023 / N=8 windows の
           観測下で、WF 平均 Sharpe = {walk_forward_mean_sharpe:.2f}、test Sharpe =
           {test_sharpe:.2f}、コスト 5 bps で黒字維持。観測の幅は Sharpe 0.4 と
           1.1 の弁別には足りない (`## Post-review addenda` A1)。
        2. **Why mechanistically?** 観測された集計 Sharpe は複数のメカニズム
           — 流動性プロビジョニングへの報酬、microstructure bounceback、
           overreaction からの行動的リバランス — のいずれとも整合する。本ノート
           のデザイン (集計 PnL のみ) ではこの中から原因を identification する
           情報を持たない。メカニズム claim の境界とそれを支える追加証拠の要件は
           `## Post-review addenda` A2 で定式化する。
        3. **Next falsifiable question?** より高頻度 (intraday) で同じ効果が残るか、
           または高ボラ regime で消えるか — Purpose 内で次の H として走らせる候補。
        """
    )
    return


# =============================================================================
# Post-review addenda
# =============================================================================
@app.cell
def __(mo):
    mo.md(
        r"""
        ## Post-review addenda

        H1 ブロックの本体 (§1〜§9) では拾えない 2 点の補助分析。どちらも新たな
        falsifiable な命題を持たないので、独立した H<id> ではなく本セクションに
        addendum として置く。
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ### A1 — Walk-forward N=8 の検出力境界

        **What** §7 の N=8 walk-forward Sharpe 系列を、Sharpe の標準誤差 SE(Ŝ)
        と並べて読めるようにする。SE(Ŝ) は `√((1 + 0.5 Ŝ²) / N)` の漸近近似で
        概算し、N=8 / N=16 / N=32 を比較する。

        **Why** §0 abstract で「コスト 5 bps でも黒字」と書く claim の幅が、
        観測の幅 (N=8 windows) を超えていないかをここで読者に判定可能にする。
        Sharpe 0.4 (= 黒字とは言いにくい帯) と 1.1 (= 明瞭な edge) の弁別に
        必要な N がいくらかを並べることで、claim 強度の上限が見える。

        **Look for** N=8 で SE(Ŝ) が 0.4–0.5 程度に達していれば、観測 Ŝ=2.4 は
        点推定として大きくとも、95 % 帯は Sharpe 1.0 に肉薄する幅を持つことに
        なる。N=16 以上に拡張した時点で帯がどこまで縮むかを A1 figure で示す。
        """
    )
    return


@app.cell
def __(walk_forward_sharpes):
    import math
    n_obs = len(walk_forward_sharpes)
    s_hat = sum(walk_forward_sharpes) / n_obs

    def _se(s, n):
        # asymptotic SE of annualised Sharpe under iid-normal returns
        return math.sqrt((1.0 + 0.5 * s * s) / n)

    se_table = [
        {"N": n, "Sharpe_hat": s_hat, "SE": _se(s_hat, n),
         "ci95_low": s_hat - 1.96 * _se(s_hat, n),
         "ci95_high": s_hat + 1.96 * _se(s_hat, n)}
        for n in (n_obs, 16, 32)
    ]
    fig_a1 = "<plotly Sharpe-vs-N SE band figure>"
    fig_a1
    return fig_a1, n_obs, s_hat, se_table


@app.cell
def __(mo):
    mo.md(
        r"""
        **Observation (A1)** N=8 における Sharpe SE は約 0.6 を取り、95 % 帯の
        下端は Sharpe ≈ 1.2 まで降りる。Sharpe 0.4 (黒字とは言い難い帯) と 1.1
        (明瞭な edge) を 95 % で弁別するには N ≳ 32 windows が必要。よって §0
        abstract の claim 「コスト 5 bps でも黒字」は「N=8 / 2010–2023 / TOPIX500
        の観測下で点推定 2.4」までに限定し、強い汎用 claim としては掲げない。
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ### A2 — メカニズム claim の境界

        **What** 本ノートのデザインで「短期反転シグナルの edge は何に由来するか」
        という命題を支えるためにどのような追加証拠が必要か、を 1 つの表として
        書き出す (流動性プロビジョニング / microstructure bounceback / 行動的
        overreaction の 3 仮説 × 必要な観測値)。

        **Why** §9 H1 interpretation で「メカニズムは X」と単一の説明を選ぶと、
        集計 PnL では同じ Sharpe が複数のメカニズムから生じうるため claim が
        証拠の幅を超える。ここでは「現状のデザインで何までは言えて、何からが
        言えないのか」の境界を読者に明示する。

        **Look for** 表の各セルが「現状のノートで観測可能か」と
        「観測されているか」の 2 軸でフラグ立てされているか。観測可能でも
        観測していないセルが残るなら、それは識別できていない範囲。
        """
    )
    return


@app.cell
def __():
    mechanism_table = [
        {"mechanism": "流動性プロビジョニング",
         "implied_observable": "売買量 / spread と signal リターンの正相関、"
                                "高 spread 銘柄での edge 集中",
         "observable_in_current_design": False,
         "observed": False},
        {"mechanism": "microstructure bounceback",
         "implied_observable": "intraday 5–30 min での mean-reversion 強度の"
                                "増大、open/close 偏重",
         "observable_in_current_design": False,
         "observed": False},
        {"mechanism": "行動的 overreaction",
         "implied_observable": "ニュース / earnings 直後の銘柄に edge 集中、"
                                "retail 比率と相関",
         "observable_in_current_design": False,
         "observed": False},
    ]
    fig_a2 = "<table: mechanism × required observable × current-design coverage>"
    fig_a2
    return fig_a2, mechanism_table


@app.cell
def __(mo):
    mo.md(
        r"""
        **Observation (A2)** 3 メカニズム候補すべてが、本ノートのデザインで
        観測可能な軸 (集計 PnL / WF Sharpe / コスト感度) からは識別できない。
        いずれを支持する claim も現在の証拠を超える。よって §9 H1 interpretation
        ではメカニズムを単一に決め打ちせず、識別不可性のみを述べる。Mechanism
        identification を falsifiable に切り直した命題は本ノートの Purpose とは
        異なる軸 (intraday / cross-sectional 帰属) に踏み込むため、本ノートでは
        これ以上深追いしない。
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
