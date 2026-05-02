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
        H1 (initial run, leaky): WF 平均 Sharpe = ~~2.4~~、test Sharpe = ~~3.1~~。
        bug_review (Step 11) の high finding に従い §5 の whole-period 標準化を
        per-date cross-sectional に置換し、§6〜§8 を再計算した。
        H1 (post-fix, preliminary): WF 平均 Sharpe = **0.9**、test Sharpe = **1.1**、
        最大 DD/vol = **0.78**、コスト 5 bps で薄利。**verdict は未確定**
        (robustness battery / experiment-review を通すまで保留)。

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
        5d z-score 反転シグナル (entry |z| ≥ 1.5, hold = 1d, fee = 5bps)。
        bug_review の high finding (§5 の whole-period 標準化が look-ahead leak)
        を反映し、§5 を per-date cross-sectional 標準化に置換 → §6〜§8 を再計算。
        修正後 WF 平均 Sharpe = 0.9、test Sharpe = 1.1。コスト感度では 5 bps で
        薄利、10 bps で break-even を割る。**verdict 未確定** (robustness /
        experiment-review 待ち)。
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
# 5. Cross-sectional standardization  (per-date; previous whole-period version
#    fixed after bug_review Step 11 — high finding: look-ahead leak via
#    panel-wide mean/std crossing train/val/test boundaries)
# =============================================================================
@app.cell
def __(mo):
    mo.md(
        r"""
        ### §5 — Cross-sectional standardization (per-date)

        **What** 各 `date` 内で symbol 横断に signal_h1_raw を z-score 標準化する
        (i.e. 同日内 cross-section の mean / std を使う)。

        **Why** symbol 間の cross-section ランキングを行うのが本来の意図。
        bug_review の leakage-reviewer から **high finding** が出た:
        旧実装はパネル全体の mean / std を使っていたため、test set の moment が
        train 段階のシグナル値に混入する look-ahead leak (whole-period
        normalization に相当)。各日付内で閉じる per-date cross-section に
        修正することで、未来情報がシグナル値に流入しなくなる。
        (expanding-window で train-only fit する代替もあり得るが、本ノートの
         意図は cross-sectional ランキングなので per-date 標準化を採用。)

        **Look for** 各日付内で signal_h1 の mean ≈ 0, std ≈ 1。日次サンプル
        平均/分散をプロットして 0/1 近傍にあること。
        """
    )
    return


@app.cell
def __(df, pl):
    # Per-date cross-sectional z-score (fixed after bug_review high finding).
    # mean / std are computed within each date only; no information from other
    # dates (and therefore no information from train/val/test boundaries) leaks
    # into signal_h1.
    df = df.with_columns([
        pl.col("signal_h1_raw").mean().over("date").alias("_xs_mu"),
        pl.col("signal_h1_raw").std().over("date").alias("_xs_sd"),
    ])
    df = df.with_columns(
        ((pl.col("signal_h1_raw") - pl.col("_xs_mu")) / pl.col("_xs_sd"))
        .alias("signal_h1")
    )
    df = df.drop(["_xs_mu", "_xs_sd"])
    return (df,)


@app.cell
def __(mo):
    mo.md(
        r"""
        **Observation (sanity)** signal_h1 は構築上、各日付内で平均 ≈ 0、
        std ≈ 1 になっているはず。ここでは per-date の mean / std を eyeball で
        確認 (NaN は warm-up と当日サンプル数が少ない初期日に集中)。
        whole-period 標準化との差分は、train 期間のみのサンプルでは概ね
        order-preserving だが、レベル (mean/std の絶対値) が大きく動く点 ―
        これが旧実装で発生していた leak の正体。
        """
    )
    return


# =============================================================================
# 6. Position, PnL, turnover  (← flattened-panel cost bug lives here)
# =============================================================================
@app.cell
def __(mo):
    mo.md(
        r"""
        ### §6 — Position, PnL, turnover (recomputed after §5 fix)
        **What** signal を [-1, 1] にクリップしてポジション化、t-1 → t で発注、
        コストは 5 bps × turnover。`ret_fwd` は forward return (target-side
        `shift(-1)`、leakage では無い ― 詳細はコード内 NOTE を参照)。

        **Why** H1 の収益性そのもの。**§5 で signal_h1 の構築式が変わった**
        ため、以降の pos / pnl / turnover は **すべて再計算** が必要。

        **Look for** Fig 2 で gross と net (5bps) の差が単調。修正前 (whole-period
        標準化) では net 5bps が滑らかな増加を示していたが、leak 除去後の挙動
        を比較する。
        """
    )
    return


@app.cell
def __(FEE_CHOSEN_BPS, df, pl):
    # Position is the signal value at t-1 (one-bar entry delay) — causal.
    df = df.with_columns(pl.col("signal_h1").clip(-1, 1).shift(1).over("symbol").alias("pos"))
    # ret_fwd = forward return from t to t+1, computed per symbol.
    # NOTE (bug_review low finding): shift(-1) here is **target-side** and is
    # legal — see bug_review.md "shift(-k) on signals or features (target-only
    # shift(-k) is OK)". The signal itself (signal_h1, pos) never uses negative
    # shifts; only the return target does, by construction t→t+1.
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
        ### §7 — Walk-forward Sharpe distribution (recomputed after §5 fix)
        **What** 6 mo train / 6 mo eval の rolling walk-forward を 8 windows 走らせる。
        **Why** Fig 4 の N=8 windows の信頼性を担保。§5 の signal 修正に伴い、
        WF Sharpe も再計算した値を採用する (旧値: mean ≈ 2.4)。
        **Look for** Sharpe 中央値 ≥ 1、negative window が 2 以下。
        修正後は `(0.5, 1.4)` の範囲に分布が縮み、negative window が出現する
        想定 (whole-period leak が打ち消されるため)。
        """
    )
    return


@app.cell
def __(df):
    # Walk-forward Sharpes — RECOMPUTED after §5's per-date standardization fix.
    # Pre-fix values (kept here for audit only) were [1.8, 2.1, 2.4, 1.9, 2.7,
    # 2.0, 2.6, 2.5] with mean 2.25 and test_sharpe 3.1. Those numbers were
    # contaminated by the whole-period normalization leak flagged by
    # bug_review (Step 11, leakage-reviewer, severity=high).
    walk_forward_sharpes_pre_fix = [1.8, 2.1, 2.4, 1.9, 2.7, 2.0, 2.6, 2.5]  # audit
    walk_forward_sharpes = [0.7, 1.1, 1.4, -0.2, 1.3, 0.8, 1.2, 0.9]
    walk_forward_mean_sharpe = sum(walk_forward_sharpes) / len(walk_forward_sharpes)
    test_sharpe = 1.1
    n_windows = len(walk_forward_sharpes)
    return (n_windows, test_sharpe, walk_forward_mean_sharpe,
            walk_forward_sharpes, walk_forward_sharpes_pre_fix)


@app.cell
def __(mo, walk_forward_mean_sharpe, walk_forward_sharpes_pre_fix):
    _pre_mean = sum(walk_forward_sharpes_pre_fix) / len(walk_forward_sharpes_pre_fix)
    mo.md(
        rf"""
        **Observation (recompute audit)** WF 平均 Sharpe は
        修正前 {_pre_mean:.2f} → 修正後 {walk_forward_mean_sharpe:.2f} へ低下。
        差分の大部分は §5 の whole-period leak が test 期間の moment を
        train signal に流入させていた分。修正後は negative window (2018Q4 相当)
        が 1 個出現しており、これは bug_review の trigger
        (Headline ≥ 2 × WF mean Sharpe) を解除する方向に動いている
        (test 1.1 / WF mean 0.9 = 約 1.2x、閾値 2 を下回る)。
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
        Recomputed after §5's per-date standardization fix.
        """
    )
    return


@app.cell
def __(df):
    # placeholder figure object — recomputed against the post-fix df.
    fig2 = "<plotly cumulative PnL figure (post-fix; per-date xs-z)>"
    fig2
    return (fig2,)


@app.cell
def __(mo):
    mo.md(
        r"""
        **Observation (post-fix)** Net 5bps は train/val 区間で緩やかに上昇する
        ものの、傾きは修正前より明らかに小さい。test split (2022–2023) では
        2022Q3 の急落局面で drawdown が深まり、修正前のような滑らかな回復は
        見られない ― これは whole-period leak が test 期間の statistic を
        前借りしていたことと整合的。regime 依存性が限定的という前回の
        observation は撤回し、後段 (robustness §13 想定) の regime conditional
        で再評価する。
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
        ### H1 interpretation (preliminary — after bug_review, before robustness gate)

        **Pipeline note** §5 の whole-period 標準化を bug_review (Step 11) の
        high finding に従い per-date cross-sectional 標準化に置換。§6〜§8 は
        その修正を前提に再計算済み。以下の数値はすべて post-fix。

        1. **What did the numbers say?** WF 平均 Sharpe =
           {walk_forward_mean_sharpe:.2f}、 test Sharpe = {test_sharpe:.2f}。
           5 bps fee 込みで薄利、10 bps を越えると break-even を割る。
           修正前 (leaky) の WF 2.4 / test 3.1 は破棄。
        2. **Why mechanistically?** 短期反転自体は流動性プロビジョニング/
           microstructure bounceback で説明できるが、修正後の Sharpe レベルは
           「実質的にはコストに食われやすい弱いエッジ」として読むべき。
           leak 除去後に残った信号が真の edge の上限。
        3. **Next falsifiable question?** (a) 高ボラ regime に集中させると
           edge が回復するか (regime-conditional H2 候補)、(b) hold horizon を
           1d → 2-3d に伸ばすと turnover コストを薄められるか (H3 候補)。
           いずれも同 Purpose 内の derived H として本ノート内でテストする。
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

        Status of the four completion gates for H1:

        - **bug_review (Step 11)** — fired on `test Sharpe > 3` + state-change
          (about-to-set-supported). 1 high finding (§5 whole-period
          standardization, look-ahead leak) and 1 low finding (§6 `shift(-1)`
          comment) were returned. **High is fixed** (§5 → per-date xs-z),
          **low is fixed** (NOTE comment added to §6). §6〜§8 recomputed.
          Re-running the full bug_review pass on the post-fix code is required
          before declaring this gate clean.
        - **robustness battery (Step 12)** — **not yet run** on the post-fix
          numbers. Earlier robustness output (if any) was on the leaky pipeline
          and is invalidated.
        - **experiment-review (Step 13)** — not yet invoked.
        - **research-quality checklist + tier ≥ Medium** — pending the above.

        `supported` は 4 gates すべてを通過するまで付けない。次アクションは
        post-fix code に対する bug_review 再走 → robustness battery →
        experiment-review。
        """
    )
    return


if __name__ == "__main__":
    app.run()
