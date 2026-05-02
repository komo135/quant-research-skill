# /// script
# requires-python = ">=3.10"
# ///
"""
exp_022_topix_quality_3factor.py — Case K fixture (Purpose B selected without research-goal review)

前ノート exp_021 (= ケース J で扱った Purpose A) は Primary YES で closing した。
Decision rule の YES 条件 = 少なくとも 1 シグナルで WF mean Sharpe ≥ 0.4 を
H2 (ROE × OCF margin 合成) が達成し、Purpose A は完了した状態。

本ノートはその次の Purpose B を扱う。Purpose B = 「TOPIX500 quality factor を
3-factor (ROE / OCF margin / accruals quality) に拡張して更に Sharpe を伸ばせるか」。

注: F14 (cross-notebook handoff の substantive な本文流入) は **発生していない**
— `## Origin` セクション、`cross_h_synthesis.md` Pattern 名 / 「派生 Purpose」/
「handoff」のような skill プロセス由来語、旧ノートの synthesis 経緯の本文化は
無い。Figure plan の Fig 4 で `1-factor (H1 of exp_021) / 2-factor (H2 of exp_021)
/ 3-factor の累積 PnL 比較` と minimal な参照はあるが、これは比較対象の系列を
名指しているだけで F14 が問題視する synthesis 経緯の流入ではない。
それでもなお、**Purpose B の選定根拠と研究目標 (project README の Question)
との紐付け** はノートからも decisions.md からも読み取れない構造になっている。
Purpose A の Primary YES が研究目標にどれだけ前進をもたらしたかの review が
無いため、Purpose B が選ばれたのは「Decision rule の YES が出たから次に進む」
という routing 由来でしかない。
"""

import marimo

__generated_with = "0.9.0"
app = marimo.App(width="full")


@app.cell
def __():
    import marimo as mo
    mo.md(
        r"""
        # exp_022 — TOPIX500 quality factor を 3-factor に拡張

        ## Purpose
        TOPIX500 universe / 2014–2024 において、ROE / OCF margin / accruals quality
        の 3-factor を rank 平均で合成した quality シグナルが、net 5 bps fee で
        market-cap weighted ベースラインに対し WF mean Sharpe ≥ 0.5 を達成するか
        を検証する。

        ## Cycle goal — 4 items
        - **Consumer**: 自分の次 Purpose (JP equity quality factor を多 factor
          スタックに組む段階の最終確認) — slug = `exp_quality_factor_stack`
        - **Decision**: 多 factor スタック組み込み時の重み比配分を決めるか / 棄却するか
        - **Decision rule**:
          - YES = 3-factor 合成で WF mean Sharpe ≥ 0.5
          - NO = 2-factor (= ROE × OCF margin) と統計的に有意差なし、binding axis = "accruals quality は JP では効かない"
          - KICK-UP = 3-factor で turnover が 40%/month を超え net edge が消失、binding axis = "fee model"
        - **Knowledge output**: H1 の results.parquet 行 + Purpose-level synthesis

        ## Hypotheses tested
        - **H1** — ROE × OCF margin × accruals quality の 3-factor 合成、WF mean Sharpe ≥ 0.5

        ## Conclusion (preliminary)
        H1 verdict = PENDING (実装中)。

        ## Figure plan
        - **Fig 1** — universe / split overlay
        - **Fig 2** — H1 累積 PnL (3-factor 版)
        - **Fig 3** — accruals quality 単独の IC 時系列
        - **Fig 4** (headline) — 1-factor (H1 of exp_021) / 2-factor (H2 of exp_021) / 3-factor の累積 PnL 比較
        """
    )
    return (mo,)


@app.cell
def __(mo):
    mo.md(r"## H1 — ROE × OCF margin × accruals quality の 3-factor 合成")
    return


@app.cell
def __():
    UNIVERSE_H1 = "TOPIX500"
    PERIOD_H1 = "2014-01..2024-12"
    FEE_BPS = 5.0
    FACTORS_H1 = ["roe", "ocf_margin", "accruals_quality"]
    WEIGHTS_H1 = [1.0 / 3, 1.0 / 3, 1.0 / 3]
    return FACTORS_H1, FEE_BPS, PERIOD_H1, UNIVERSE_H1, WEIGHTS_H1


@app.cell
def __(mo):
    mo.md(
        r"""
        ### H1 abstract
        ROE / OCF margin / accruals quality の 3-factor を等重み rank-平均で
        合成、上位 quintile long-only。net 5 bps で WF mean Sharpe ≥ 0.5 を
        目標。
        """
    )
    return


@app.cell
def __(mo):
    mo.md(r"### H1 result — IN PROGRESS (実装中)")
    return


@app.cell
def __(mo):
    mo.md(r"### H1 verdict — **PENDING**")
    return


if __name__ == "__main__":
    app.run()
