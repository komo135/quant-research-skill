# /// script
# requires-python = ">=3.10"
# ///
"""
exp_007_eurusd_intraday_meanreversion.py — Case G post-GREEN

After GREEN-phase changes:
- ### Derived hypotheses 表テンプレ (hypothesis_cycles.md L120-128) は削除されたので、
  §H1 末尾は ### H<id> conclusion + ### Cannot conclude のみ。
- 派生 H (H2) の planning state は hypotheses.md の Status 列で管理 (planned-runnow → in-progress)、
  ノート本文には現れない。
- §H2 ブロックは hypothesis_cycles.md routing rule (1) に従って同 notebook の次 H として作られた。
- 二重登録 (= F12 の症状) は構造的に発生しない。
"""

import marimo

__generated_with = "0.9.0"
app = marimo.App(width="full")


@app.cell
def __():
    import marimo as mo
    mo.md(
        r"""
        # exp_007 — EUR/USD 5min intraday mean-reversion の net-fee 収益性

        ## Purpose
        EUR/USD 5 分足において、短期的な over-extension の事後リバースを
        net 1 bp/side fee で取りに行く mean-reversion 系シグナルが、
        single-instrument B&H ベースラインを test Sharpe ≥ 0.5 で上回るかを検証する。

        ## Cycle goal — 5 items
        - **Consumer**: 同チーム execution 班。EUR/USD 5min の MR 帯を
          live trading 候補に引き上げるか否かの判断者。
        - **Decision**: live paper-trade フェーズに進めるか / 別 universe に kick-up するか / 棚上げするか
        - **Decision rule**:
          - YES = test Sharpe ≥ 0.5 かつ WF mean Sharpe ≥ 0.4 を **複数の
            entry signal で再現**
          - NO = 全 signal の test Sharpe < 0.3、binding axis = "EUR/USD 5min は MR 帯ではない"
          - KICK-UP = 全 signal で fee model を緩める (1 bp → 0.5 bp) と急変、binding axis = "fee model"
        - **Knowledge output**: 各 H の results.parquet 行 + Purpose-level synthesis +
          headline = Fig 6 (signal 別 net-fee 累積 PnL 重ね描き)
        - **Target sub-claim id**: Primary G2.1 (`EUR/USD 5min に net-fee 帯で MR が存在する`)。
          Secondary: なし。

        ## Hypotheses tested
        - **H1** — RSI(14) ≤ 30 entry × signal-flip exit
        - **H2** — Bollinger(20, 2.0σ) lower-touch entry × signal-flip exit
          (= 同 Purpose 内で MR を別レンズで再検証)

        ## Conclusion (preliminary)
        H1 verdict PENDING (robustness 未通過)、H2 verdict PENDING (実装途中)。

        ## Figure plan
        - **Fig 1** — universe / split overlay
        - **Fig 2** — H1 累積 PnL (net fee) vs B&H
        - **Fig 3** — H1 RSI 分布 / entry trigger 密度
        - **Fig 4** — H1 walk-forward Sharpe 分布 (N=8)
        - **Fig 5** — H2 累積 PnL vs B&H
        - **Fig 6** (headline) — H1 / H2 net-fee 累積 PnL 重ね描き
        """
    )
    return (mo,)


@app.cell
def __(mo):
    mo.md(r"## H1 — RSI(14) ≤ 30 entry × signal-flip exit")
    return


@app.cell
def __():
    UNIVERSE_H1 = "EURUSD 5min"
    PERIOD_H1 = "2018-01..2024-12"
    FEE_BPS_PER_SIDE = 1.0
    RSI_WINDOW_H1 = 14
    RSI_THRESHOLD_H1 = 30
    return FEE_BPS_PER_SIDE, PERIOD_H1, RSI_THRESHOLD_H1, RSI_WINDOW_H1, UNIVERSE_H1


@app.cell
def __(mo):
    mo.md(
        r"""
        ### H1 abstract
        RSI(14) ≤ 30 で long エントリ、RSI(14) > 50 へ反転で exit。
        net 1 bp/side で test Sharpe = 0.55、WF mean Sharpe = 0.42。
        閾値 0.5 は test 単独では達成しているが WF 平均は届かず、
        verdict は PENDING (robustness gates 未通過)。
        """
    )
    return


@app.cell
def __():
    test_sharpe_h1 = 0.55
    walk_forward_sharpes_h1 = [0.40, 0.55, 0.30, 0.45, 0.35, 0.50, 0.45, 0.40]
    walk_forward_mean_sharpe_h1 = sum(walk_forward_sharpes_h1) / len(walk_forward_sharpes_h1)
    return test_sharpe_h1, walk_forward_mean_sharpe_h1, walk_forward_sharpes_h1


@app.cell
def __(mo, test_sharpe_h1, walk_forward_mean_sharpe_h1):
    mo.md(
        rf"""
        ### H1 conclusion
        - Observed: test Sharpe = {test_sharpe_h1:.2f}、WF mean = {walk_forward_mean_sharpe_h1:.2f}
        - Verdict: PENDING (robustness 未通過)

        ### H1 interpretation
        EUR/USD 5min は短期的な MR を見せるが、RSI 単独では entry 後 ~30 分の
        ノイズで signal-flip 判定がぶれる。Bollinger band の lower-touch を
        entry にした構造で MR が再現するかが、Decision rule の YES 条件
        (= 複数 entry signal での再現) を満たすかを直接決める。

        ### Cannot conclude (H1)
        - 別 entry signal (Bollinger / Keltner) でも MR が出るかは H1 単独では不明
        - regime conditional は未検証
        """
    )
    return


@app.cell
def __(mo):
    mo.md(r"## H2 — Bollinger(20, 2.0σ) lower-touch entry × signal-flip exit")
    return


@app.cell
def __():
    UNIVERSE_H2 = "EURUSD 5min"
    PERIOD_H2 = "2018-01..2024-12"
    BB_WINDOW_H2 = 20
    BB_K_H2 = 2.0
    return BB_K_H2, BB_WINDOW_H2, PERIOD_H2, UNIVERSE_H2


@app.cell
def __(mo):
    mo.md(
        r"""
        ### H2 abstract
        Bollinger lower band (20, 2.0σ) タッチで long エントリ、ミドルバンド回帰で exit。
        net 1 bp/side で test Sharpe ≥ 0.5 を目標。H1 と同 universe / 同 split / 同 fee。
        """
    )
    return


@app.cell
def __(mo):
    mo.md(r"### H2 result — IN PROGRESS (実装中、評価セル未生成)")
    return


@app.cell
def __(mo):
    mo.md(r"### H2 verdict — **PENDING** (実装未完了)")
    return


if __name__ == "__main__":
    app.run()
