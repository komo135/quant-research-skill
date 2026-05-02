# /// script
# requires-python = ">=3.10"
# ///
"""
exp_007_eurusd_intraday_meanreversion.py — Case G fixture (run-now derived H promoted to next ## H<id> block)

H1 (RSI≤30 entry × signal-flip exit) was tested; verdict is PENDING (robustness 未通過).
H1 round の末尾で同 Purpose に属する run-now 派生 H が 1 件提案され、
hypothesis_cycles.md の routing rule に従って same-notebook で次の ## H2 ブロックに昇格された。
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

        ## Cycle goal — 4 items
        - **Consumer**: 同チーム execution 班。EUR/USD 5min の MR 帯を
          live trading 候補に引き上げるか否かの判断者。
        - **Decision**: live paper-trade フェーズに進めるか / 別 universe に kick-up するか / 棚上げするか
        - **Decision rule**:
          - YES = test Sharpe ≥ 0.5 かつ WF mean Sharpe ≥ 0.4 を **複数の
            entry signal で再現** (single-signal で偶然に乗っただけではない、を担保)
          - NO = 全 signal の test Sharpe < 0.3、binding axis = "EUR/USD 5min は MR 帯ではない"
          - KICK-UP = 全 signal で fee model を緩める (1 bp → 0.5 bp) と急変、binding axis = "fee model"
        - **Knowledge output**: 各 H の results.parquet 行 + Purpose-level synthesis 1 段落 +
          headline = Fig 6 (signal 別 net-fee 累積 PnL 重ね描き)

        ## Hypotheses tested
        - **H1** — RSI(14) ≤ 30 entry × signal-flip exit、net 1 bp/side で test Sharpe ≥ 0.5
        - **H2** (derived from H1) — Bollinger band (20, 2.0σ) lower-touch entry × signal-flip exit、
          同条件で test Sharpe ≥ 0.5 (= 同じ MR Purpose を別レンズで再検証)

        ## Conclusion (preliminary)
        H1 verdict PENDING (robustness 未通過 / WF mean = 0.42、test = 0.55)。
        H2 verdict PENDING (実装中、結果セル未生成)。

        ## Why this matters
        EUR/USD 5min の MR が単一 entry signal の偶然でなく **複数 signal で再現**
        するかは、Decision rule の YES 条件 (= 「複数 entry で再現」) に直接対応する。

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
        閾値 0.5 は test 単独では達成しているが WF 平均は届かず、verdict は
        PENDING (robustness gates 未通過)。
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
        ### H1 interpretation
        test = {test_sharpe_h1:.2f}、WF mean = {walk_forward_mean_sharpe_h1:.2f}。
        EUR/USD 5min は短期的な MR を見せるが、RSI 単独では entry 後 ~30 分の
        ノイズで signal-flip 判定がぶれる。次に試したいのは **同じ MR Purpose を
        別レンズで再検証** すること — 具体的には Bollinger band の lower-touch
        を entry にした場合、複数 signal で再現するかが Decision rule の YES 条件
        に直接対応する。
        """
    )
    return


@app.cell
def __(mo):
    mo.md(r"### H1 verdict — **PENDING** (robustness 未通過)")
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ### Cannot conclude (H1)
        - 別 entry signal (Bollinger / Keltner) でも MR が出るかは H1 単独では不明
        - regime conditional は未検証

        ### Derived hypotheses (next rounds inside THIS notebook, or candidates for new notebooks)
        | New hypothesis | Where | Run-now / next-session / drop | Reason |
        |---|---|---|---|
        | H2: Bollinger(20, 2.0σ) lower-touch entry × signal-flip exit、test Sharpe ≥ 0.5 | same notebook | run-now      | 同 Purpose、別レンズで MR 再検証 (alternative formulation) |
        | H3: regime conditional (trending / ranging) で H1 を分解        | same notebook | next-session | 同 Purpose、specialization。WF re-run が要る |
        | H4: USD/JPY 5min に RSI signal を移植                            | new notebook  | next-session | new Purpose: cross-asset |
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
