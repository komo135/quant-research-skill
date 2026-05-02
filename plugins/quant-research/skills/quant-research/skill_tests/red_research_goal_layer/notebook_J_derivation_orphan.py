# /// script
# requires-python = ">=3.10"
# ///
"""
exp_021_topix_quality_factor.py — Case J fixture (derivation has no goal anchor)

H1 を回した結果、turnover が edge を食い切ったので H2 (合成版) を試す
判断が下された。`hypothesis_cycles.md` routing rule (1) に従い、§H2 は
同 notebook 内の次 H ブロックとして昇格された。

注: F12-14 (派生 H 表の本文流入) は **発生していない** — `### Derived
hypotheses` 表は書かれず、§H1 → §H2 の接続は interpretation セルの
自然な流れだけで成立している。それでも、H2 が **研究目標 (project README
の Question) のどのサブクレームに貢献するか** / **H1 の結果から何の設計
仮説が更新され H2 が選ばれたか** は、ノート / decisions.md / hypotheses.md
のいずれにも記録されない構造になっている。
"""

import marimo

__generated_with = "0.9.0"
app = marimo.App(width="full")


@app.cell
def __():
    import marimo as mo
    mo.md(
        r"""
        # exp_021 — TOPIX500 quality factor の net 5 bps 収益性

        ## Purpose
        TOPIX500 universe / 2014–2024 において、quality factor 系シグナルが
        net 5 bps fee で market-cap weighted ベースラインに対し WF mean
        Sharpe ≥ 0.4 を達成するかを検証する。

        ## Cycle goal — 4 items
        - **Consumer**: 自分の次 Purpose (JP equity quality factor を多 factor
          スタックに組む段階) — slug = `exp_quality_factor_stack`
        - **Decision**: 多 factor スタックに quality 系を組み込むか / 棄却するか / 別 quality 軸に kick-up するか
        - **Decision rule**:
          - YES = 少なくとも 1 つの quality 系シグナルで WF mean Sharpe ≥ 0.4
          - NO = 全シグナルで WF mean Sharpe < 0.3、binding axis = "JP TOPIX500 quality は net 5bps では retire"
          - KICK-UP = 全シグナルで turnover が year-over-year で 200% 超、binding axis = "turnover/cost model"
        - **Knowledge output**: H1/H2 の results.parquet 行 + Purpose-level synthesis

        ## Hypotheses tested
        - **H1** — ROE rank long-only signal、WF mean Sharpe ≥ 0.4
        - **H2** — ROE × OCF margin の rank-平均合成、WF mean Sharpe ≥ 0.4

        ## Conclusion (preliminary)
        H1 verdict = REJECTED (WF mean = 0.18、turnover が edge を食い切り)。
        H2 verdict = SUPPORTED_PROVISIONAL (WF mean = 0.41、review 未通過)。

        ## Figure plan
        - **Fig 1** — universe / split overlay
        - **Fig 2** — H1 累積 PnL
        - **Fig 3** — H1 月次 turnover
        - **Fig 4** — H2 累積 PnL
        - **Fig 5** (headline) — H1 / H2 net-fee 累積 PnL 重ね描き
        """
    )
    return (mo,)


@app.cell
def __(mo):
    mo.md(r"## H1 — ROE rank long-only")
    return


@app.cell
def __():
    UNIVERSE_H1 = "TOPIX500"
    PERIOD_H1 = "2014-01..2024-12"
    FEE_BPS = 5.0
    FACTORS_H1 = ["roe"]
    return FACTORS_H1, FEE_BPS, PERIOD_H1, UNIVERSE_H1


@app.cell
def __():
    test_sharpe_h1 = 0.20
    walk_forward_mean_sharpe_h1 = 0.18
    monthly_turnover_h1 = 0.45
    return monthly_turnover_h1, test_sharpe_h1, walk_forward_mean_sharpe_h1


@app.cell
def __(mo, test_sharpe_h1, walk_forward_mean_sharpe_h1, monthly_turnover_h1):
    mo.md(
        rf"""
        ### H1 abstract / interpretation
        ROE 上位 quintile long-only。net 5 bps で test Sharpe = {test_sharpe_h1:.2f}、
        WF mean = {walk_forward_mean_sharpe_h1:.2f}。月次 turnover = {monthly_turnover_h1:.0%}
        と高く、edge が手数料に食われている。ROE のシグナル強度は出ているが
        rebalance 頻度を抑えるか、独立軸を加えて turnover を平均化する余地が
        ありそう。後者は、純資産ベースの収益性 (ROE) と独立に効きうる
        キャッシュベースの収益性 (OCF margin) を合成軸に加える方向で試せる。
        """
    )
    return


@app.cell
def __(mo):
    mo.md(r"### H1 verdict — **REJECTED** (WF mean < 0.4 閾値、turnover が binding)")
    return


@app.cell
def __(mo):
    mo.md(r"## H2 — ROE × OCF margin の rank-平均合成")
    return


@app.cell
def __():
    FACTORS_H2 = ["roe", "ocf_margin"]
    return (FACTORS_H2,)


@app.cell
def __():
    test_sharpe_h2 = 0.45
    walk_forward_mean_sharpe_h2 = 0.41
    monthly_turnover_h2 = 0.32
    return monthly_turnover_h2, test_sharpe_h2, walk_forward_mean_sharpe_h2


@app.cell
def __(mo, test_sharpe_h2, walk_forward_mean_sharpe_h2, monthly_turnover_h2):
    mo.md(
        rf"""
        ### H2 abstract / interpretation
        ROE と OCF margin の rank を 50:50 で平均合成、上位 quintile long-only。
        test Sharpe = {test_sharpe_h2:.2f}、WF mean = {walk_forward_mean_sharpe_h2:.2f}、
        月次 turnover = {monthly_turnover_h2:.0%}。
        H1 単独より turnover が下がり (45% → 32%)、edge が net で残った。
        純資産系とキャッシュ系が独立に効く局面で互いを薄め合わない構造が
        実データでも確認された。
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
        ## Purpose-level synthesis (preliminary)
        TOPIX500 quality factor のうち、ROE 単独は turnover で retire したが、
        OCF margin との合成で net 5 bps 帯に残ることが分かった。Decision rule
        の YES 条件 (= 少なくとも 1 シグナルで WF mean Sharpe ≥ 0.4) は H2 で
        達成。binding axis は「合成の独立軸が要る」という形で更新された。
        """
    )
    return


if __name__ == "__main__":
    app.run()
