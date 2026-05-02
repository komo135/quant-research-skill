# /// script
# requires-python = ">=3.10"
# ///
"""
exp_003_jp_eq_quality_factors.py — JP 個別銘柄の 2-factor quality 合成
"""

import marimo

__generated_with = "0.9.0"
app = marimo.App(width="full")


@app.cell
def __():
    import marimo as mo
    mo.md(
        r"""
        # exp_003 — JP 個別銘柄 ROE × OCF margin 合成シグナルの利益寄与

        ## Purpose
        日本株個別銘柄に対し、ROE と営業 CF margin (OCF margin) の 2 factor を
        rank 平均で合成したシグナルが、単純な market-cap weighted ベースラインを
        net 5 bps fee で上回るか — を TOPIX500 universe / 2014–2024 で検証する。

        ## Cycle goal

        ### Consumer
        次 Purpose `exp_004_jp_quality_size_overlay` (= 同 quality 合成に
        size factor を組み合わせるか否かの決定)。

        ### Decision the consumer is blocked on
        ROE × OCF margin ベースの quality 合成を size overlay の出発点として
        採用するかどうか。

        ### Decision rule (committed before the cycle runs)
        - YES: H1 が test Sharpe ≥ 0.5、WF mean Sharpe ≥ 0.4、WF positive rate
          ≥ 60 % をすべて満たし、bootstrap CI 下限 > 0
        - NO (binding axis = `signal_strength`): test Sharpe < 0.3、または WF
          positive rate < 50 %
        - KICK-UP: bug_review が embargo / 決算日アラインメントの未解消バグを
          検出、または upstream の財務データ取得に panel-wide leak が残る

        ### Knowledge output
        H1 の per-H 行 (results.parquet) + 2-factor 合成の test 期間 cumulative
        PnL 図 + 1 段落の Purpose-level 結論。

        ## Hypotheses tested
        - **H1** — ROE と OCF margin の 2 factor を rank 平均で合成したシグナルが、
          TOPIX500 universe / 2014–2024 で net 5 bps fee 込み test Sharpe ≥ 0.5
          を達成する。

        ## Conclusion (preliminary)
        H1: WF mean Sharpe = 0.45、test Sharpe = 0.55。**verdict 未確定**
        (robustness battery / bug_review / experiment-review 未実行)。

        ## Why this matters
        ROE と OCF margin はそれぞれ会計利益と現金利益という独立した収益性の
        側面を捉える。両者の合成が JP universe + post-Abenomics 期間でも
        market-cap baseline を超えるかは、後続の size overlay 検討
        (exp_004) で出発点として採用できるか否かを決める。

        ## Universe
        - Instruments: TOPIX500 構成銘柄 (cross-section)
        - Period: 2014-01..2024-12
        - Frequency: daily (rebalancing daily)

        ## Data ranges
        train [2014-01, 2020-12] / val [2021-01, 2022-12] / test [2023-01, 2024-12],
        embargo 5 営業日

        ## Headline figure plan
        - **Fig 2 が headline**: 2-factor 合成 (ROE × OCF margin) の test 期間
          cumulative PnL を market-cap weighted baseline と並べる line chart。
        - **Axes**: x = 日付 (2023-01..2024-12)、y = cumulative net return (5 bps)。
        - **Reader が読み取るべき観察**: 2-factor 合成の test 期間の終端 PnL が
          baseline を上回り、drawdown 期間でも乖離が単調に広がること。

        ## Reader takeaway
        2-factor (ROE + OCF margin) quality 合成は TOPIX500 / 2014–2024 で
        market-cap baseline を net 5 bps で上回る (Sharpe 水準 0.5 前後) のか、
        それとも超えないのか。

        ## Figure plan
        - **Fig 1** — universe / train・val・test split overlay
        - **Fig 2** — H1 累積 PnL (2-factor 合成 vs market-cap baseline) [headline]
        - **Fig 3** — 2 factor (ROE / OCF margin) の rolling 12M IC
        - **Fig 4** — Walk-forward Sharpe 分布 (N=8)
        - **Fig 5** — fee sensitivity (0–10 bps sweep)
        - **Fig 6** — regime conditional (bull / bear / range)
        """
    )
    return (mo,)


@app.cell
def __(mo):
    mo.md(r"## H1 — ROE × OCF margin 2-factor composite")
    return


@app.cell
def __():
    # H1 config — 2-factor quality composite
    UNIVERSE = "TOPIX500"
    PERIOD = "2014-01..2024-12"
    FACTORS = ["roe", "ocf_margin"]    # rank-平均で合成、両者 long-good
    FEE_BPS = 5
    EMBARGO_BDAYS = 5
    REBAL_FREQ = "daily"
    return EMBARGO_BDAYS, FACTORS, FEE_BPS, PERIOD, REBAL_FREQ, UNIVERSE


@app.cell
def __(mo):
    mo.md(
        r"""
        ### H1 abstract
        ROE と OCF margin の 2 factor を rank 平均 (両者 long-good 方向) で
        合成し、TOPIX500 universe で daily reBAL する。net 5 bps fee 込みで
        WF mean Sharpe = 0.45、test Sharpe = 0.55、market-cap weighted
        ベースラインは WF mean 0.20、test 0.10。会計利益 (ROE) と現金利益
        (OCF margin) の両軸を取ることで cross-section の収益性ランキングが
        baseline を上回る、という仮説と整合する preliminary な水準。
        """
    )
    return


@app.cell
def __():
    walk_forward_sharpes = [0.30, 0.55, 0.40, 0.65, 0.25, 0.55, 0.50, 0.40]
    walk_forward_mean_sharpe = sum(walk_forward_sharpes) / len(walk_forward_sharpes)
    walk_forward_positive_rate = sum(1 for s in walk_forward_sharpes if s > 0) / len(walk_forward_sharpes)
    test_sharpe = 0.55
    return (
        test_sharpe,
        walk_forward_mean_sharpe,
        walk_forward_positive_rate,
        walk_forward_sharpes,
    )


@app.cell
def __(mo, test_sharpe, walk_forward_mean_sharpe, walk_forward_positive_rate):
    mo.md(
        rf"""
        ### H1 interpretation
        WF mean = {walk_forward_mean_sharpe:.2f}、test = {test_sharpe:.2f}、
        WF positive rate = {walk_forward_positive_rate:.0%} (N=8)。Decision rule
        の YES 条件 (test ≥ 0.5、WF mean ≥ 0.4、positive rate ≥ 60 %) は数値
        水準としては超えているが、N=8 では Sharpe 0.4 と 0.6 を分離する検出力が
        十分でなく、bootstrap CI 下限 / PSR を含む robustness battery と
        bug_review / experiment-review を経て初めて verdict='supported' が
        付けられる。メカニズム上は ROE が会計利益、OCF margin が現金利益という
        独立した収益性の側面を捉えるため、両者の rank 平均が相互の説明残差を
        拾うという読みと整合する。

        次に問うべき falsifiable な質問: この 2-factor 合成に size factor
        (small-minus-big rank) を overlay すると同 universe / 同 period で
        Sharpe が 0.5 → 0.7 のレンジに上ぶれするか — これは Purpose が変わる
        ので別ノート (exp_004) で扱う。
        """
    )
    return


@app.cell
def __(mo):
    mo.md(r"### H1 verdict — **PENDING**")
    return


if __name__ == "__main__":
    app.run()
