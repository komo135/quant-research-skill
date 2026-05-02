# /// script
# requires-python = ">=3.10"
# ///
"""
exp_011_jp_eq_quality_factor_iteration.py — Case H fixture (multi-round derived-hypothesis tables accumulate)

Purpose は JP equity quality factor の net 5 bps 収益性。
H1 → H2 → H3 と 3 ラウンド進み、各 H 末尾には hypothesis_cycles.md の routing 表テンプレに従って
「### Derived hypotheses」表が常駐する。3 ラウンド分の表が並んだ時、行のライフサイクル
(消化済み / 生きている / 既に別ラウンドで吸収済み) が判別不能なまま累積する。
"""

import marimo

__generated_with = "0.9.0"
app = marimo.App(width="full")


@app.cell
def __():
    import marimo as mo
    mo.md(
        r"""
        # exp_011 — JP 個別銘柄 quality factor の net 5 bps 収益性

        ## Purpose
        TOPIX500 universe / 2014–2024 において、quality factor 系シグナル
        (ROE 単独、ROE × OCF margin 合成、regime 別) が、net 5 bps fee で
        market-cap weighted ベースラインに対し WF mean Sharpe ≥ 0.4 を
        **複数のシグナル / 条件で再現** するかを検証する。

        ## Cycle goal — 4 items
        - **Consumer**: 自分の次 Purpose (JP equity quality factor を多 factor
          スタックに組む段階) — slug = `exp_quality_factor_stack`
        - **Decision**: 多 factor スタックに ROE 系を組み込むか / 棄却するか / 別 quality 軸 (利益安定性) に kick-up するか
        - **Decision rule**:
          - YES = 少なくとも 2 つの quality 系シグナルで WF mean Sharpe ≥ 0.4
          - NO = 全シグナルで WF mean Sharpe < 0.3、binding axis = "JP TOPIX500 quality は net 5bps では retire"
          - KICK-UP = 全シグナルで turnover が year-over-year で 200% 超、binding axis = "turnover/cost model"
        - **Knowledge output**: H1/H2/H3 の results.parquet 行 + Purpose-level synthesis +
          headline = Fig 8 (signal × regime での WF Sharpe heatmap)

        ## Hypotheses tested
        - **H1** — ROE rank long-only signal、WF mean Sharpe ≥ 0.4
        - **H2** (derived from H1) — ROE × OCF margin の rank-平均合成、WF mean Sharpe ≥ 0.4
        - **H3** (derived from H2) — H2 の合成シグナルを trending regime のみに限定、WF mean Sharpe ≥ 0.5

        ## Conclusion (preliminary)
        H1 verdict = rejected (WF mean = 0.18)、H2 verdict = supported_provisional (WF mean = 0.41、未 review)、
        H3 verdict = PENDING (実装中)。

        ## Figure plan
        - **Fig 1** — universe / split overlay
        - **Fig 2** — H1 累積 PnL
        - **Fig 3** — H1 WF Sharpe 分布
        - **Fig 4** — H2 累積 PnL
        - **Fig 5** — H2 vs H1 month-by-month spread
        - **Fig 6** — H2 WF Sharpe 分布
        - **Fig 7** — H3 trending regime 限定の累積 PnL
        - **Fig 8** (headline) — signal × regime の WF Sharpe heatmap
        """
    )
    return (mo,)


@app.cell
def __(mo):
    mo.md(r"## H1 — ROE rank long-only")
    return


@app.cell
def __():
    test_sharpe_h1 = 0.20
    walk_forward_mean_sharpe_h1 = 0.18
    return test_sharpe_h1, walk_forward_mean_sharpe_h1


@app.cell
def __(mo, test_sharpe_h1, walk_forward_mean_sharpe_h1):
    mo.md(
        rf"""
        ### H1 abstract / interpretation
        ROE 上位 quintile long-only、ベンチマーク market-cap weighted。
        net 5 bps で test Sharpe = {test_sharpe_h1:.2f}、WF mean = {walk_forward_mean_sharpe_h1:.2f}。
        単独 ROE では rebalance turnover が高く net edge を食い切る。
        合成 (cash-flow を独立軸として加える) と regime 別の検証が次に要る。
        """
    )
    return


@app.cell
def __(mo):
    mo.md(r"### H1 verdict — **REJECTED** (WF mean < 0.4 閾値、turnover が edge を食い切り)")
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ### Derived hypotheses (next rounds inside THIS notebook, or candidates for new notebooks)
        | New hypothesis | Where | Run-now / next-session / drop | Reason |
        |---|---|---|---|
        | H2: ROE × OCF margin の rank-平均合成、WF mean Sharpe ≥ 0.4              | same notebook | run-now      | 同 Purpose、cash-flow を独立軸として加える refinement |
        | H4: sector-neutral 版で ROE を再評価                                    | same notebook | next-session | 同 Purpose、別レンズ。sector exposure データの整備が要る |
        | H5: long-short 化して market-neutral にした版                           | same notebook | next-session | 同 Purpose、portfolio construction 層の specialization |
        | (drop) earnings revision 系 factor の追加                              | drop          | —            | papers.md で JP universe の弱さが既知 |
        """
    )
    return


@app.cell
def __(mo):
    mo.md(r"## H2 — ROE × OCF margin rank-平均合成")
    return


@app.cell
def __():
    test_sharpe_h2 = 0.45
    walk_forward_mean_sharpe_h2 = 0.41
    return test_sharpe_h2, walk_forward_mean_sharpe_h2


@app.cell
def __(mo, test_sharpe_h2, walk_forward_mean_sharpe_h2):
    mo.md(
        rf"""
        ### H2 abstract / interpretation
        ROE と OCF margin の rank を 50:50 で平均合成、上位 quintile long-only。
        test Sharpe = {test_sharpe_h2:.2f}、WF mean = {walk_forward_mean_sharpe_h2:.2f}。
        合成は H1 単独の turnover 問題を緩和し、純資産系とキャッシュ系が
        独立に効く局面で互いを薄め合わない。
        """
    )
    return


@app.cell
def __(mo):
    mo.md(r"### H2 verdict — **SUPPORTED_PROVISIONAL** (review 未通過、暫定)")
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ### Derived hypotheses (next rounds inside THIS notebook, or candidates for new notebooks)
        | New hypothesis | Where | Run-now / next-session / drop | Reason |
        |---|---|---|---|
        | H3: H2 を trending regime のみに限定、WF mean Sharpe ≥ 0.5              | same notebook | run-now      | 同 Purpose、regime specialization |
        | H6: H2 を turnover-cap 30%/month で制約した版                           | same notebook | next-session | 同 Purpose、portfolio construction 層 |
        | H7: H2 の重み比を 70:30 / 30:70 で sweep                                | same notebook | next-session | 同 Purpose、parameter sensitivity |
        """
    )
    return


@app.cell
def __(mo):
    mo.md(r"## H3 — H2 を trending regime のみに限定")
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ### H3 abstract
        H2 の合成シグナルを、TOPIX 200日移動平均上向き × 200日リターン > 0 の
        日のみ active にし、それ以外は flat にする。WF mean Sharpe ≥ 0.5 を目標。
        """
    )
    return


@app.cell
def __(mo):
    mo.md(r"### H3 result — IN PROGRESS (実装中、評価セル未生成)")
    return


@app.cell
def __(mo):
    mo.md(r"### H3 verdict — **PENDING**")
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ### Derived hypotheses (next rounds inside THIS notebook, or candidates for new notebooks)
        | New hypothesis | Where | Run-now / next-session / drop | Reason |
        |---|---|---|---|
        | H8: H3 を sector-neutral × regime の 2 軸 cross で評価               | same notebook | next-session | 同 Purpose、H4 と H3 の合流 |
        | H9: H3 を US large-cap (S&P500) に移植                                | new notebook  | next-session | new Purpose: cross-asset |
        """
    )
    return


if __name__ == "__main__":
    app.run()
