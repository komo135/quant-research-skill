# /// script
# requires-python = ">=3.10"
# ///
"""
exp_011_jp_eq_quality_factor_iteration.py — Case H post-GREEN

After GREEN:
- 各ラウンド末尾の ### Derived hypotheses 表は無くなった (テンプレ削除済)。
- 派生 H (H4 - H9) の planning state は hypotheses.md の Status 列で
  (planned-runnow / planned-nextsession / planned-drop) として一元管理。
- ノート本文は research record としてのみ機能 — TODO ボード化が構造的に発生しない。
- H2/H3 の昇格は、hypotheses.md 行が Status: planned-runnow → in-progress → supported_provisional
  / PENDING に進む形で記録される。ノート本文では §H2 / §H3 ブロックの存在自体が "昇格済み" の
  証拠で、別記法は要らない。
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

        ## Cycle goal — 5 items
        - **Consumer**: 自分の次 Purpose (JP equity quality factor を多 factor
          スタックに組む段階) — slug = `exp_quality_factor_stack`
        - **Decision**: 多 factor スタックに ROE 系を組み込むか / 棄却するか / 別 quality 軸 (利益安定性) に kick-up するか
        - **Decision rule**:
          - YES = 少なくとも 2 つの quality 系シグナルで WF mean Sharpe ≥ 0.4
          - NO = 全シグナルで WF mean Sharpe < 0.3、binding axis = "JP TOPIX500 quality は net 5bps では retire"
          - KICK-UP = 全シグナルで turnover が year-over-year で 200% 超、binding axis = "turnover/cost model"
        - **Knowledge output**: H1/H2/H3 の results.parquet 行 + Purpose-level synthesis +
          headline = Fig 8 (signal × regime での WF Sharpe heatmap)
        - **Target sub-claim id**: Primary G1.1 (`quality factor が net 5bps で edge を持つ`)。
          Secondary: なし。

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

        ### H1 conclusion
        - Observed: test Sharpe = {test_sharpe_h1:.2f}、WF mean = {walk_forward_mean_sharpe_h1:.2f}
        - Verdict: REJECTED (WF mean < 0.4 閾値、turnover が edge を食い切り)

        ### Cannot conclude (H1)
        - 合成軸を加えた場合の挙動は H1 単独では不明
        - regime conditional は未検証
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

        ### H2 conclusion
        - Observed: test Sharpe = {test_sharpe_h2:.2f}、WF mean = {walk_forward_mean_sharpe_h2:.2f}
        - Verdict: SUPPORTED_PROVISIONAL (review 未通過、暫定)

        ### Cannot conclude (H2)
        - 全期間で trending regime / ranging regime のどちらが寄与しているかは未分解
        - 重み比 50:50 以外の sweep は未実施
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


if __name__ == "__main__":
    app.run()
