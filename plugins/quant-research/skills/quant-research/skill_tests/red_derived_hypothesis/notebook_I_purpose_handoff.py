# /// script
# requires-python = ">=3.10"
# ///
"""
exp_013_eurusd_meanreversion_turnover_capped.py — Case I fixture (new-Purpose handoff carries old-notebook synthesis)

このノートは exp_012 (EUR/USD 5min mean-reversion の網羅検証) で
H1-H4 が `failure_mode='turnover'` を共有して emergency-stop (N=5 advisory) に
ヒットし、cross_h_synthesis.md の Pattern A (binding axis = turnover) が
出た結果として開かれた、派生 Purpose のうちの 1 本。

派生 Purpose の handoff 経緯と前提が、Purpose ヘッダー / Cycle goal /
H1 abstract に **本文化** されており、新ノート単独で Purpose を読むと
研究内容より handoff メタ情報が先に来る。
"""

import marimo

__generated_with = "0.9.0"
app = marimo.App(width="full")


@app.cell
def __():
    import marimo as mo
    mo.md(
        r"""
        # exp_013 — EUR/USD 5min MR を turnover-cap 制約下で再検証

        ## Origin (handoff from exp_012)
        本ノートは exp_012 の Purpose-level synthesis (Pattern A:
        `failure_mode='turnover'` が H1-H4 全件で共通) から派生した
        2 つの候補 Purpose のうち、P_X (turnover-controlled re-test) を扱う。
        もう一方の派生 Purpose P_Y (signal-flip の代わりに TP/SL exit) は
        exp_014 で別途開く予定。exp_012 で binding axis として特定された
        turnover を一次制約として固定した上で、MR が edge を保つかを
        改めて測るのが本ノートの主旨。

        ## Purpose
        exp_012 で binding axis として特定された turnover を 30%/month
        以下に制約 (= 強い一次制約) した上で、RSI(14) ≤ 30 entry × signal-flip
        exit が EUR/USD 5min / net 1 bp/side で test Sharpe ≥ 0.5 を達成するか。
        exp_012 の H1-H4 では turnover 制約なしで Sharpe ≈ 0.55 だが
        net-fee で edge が消えていた。本ノートはこの "Pattern A 解消" 仮説の
        直接検証になる。

        ## Cycle goal — 4 items
        - **Consumer**: 自分の次 Purpose (exp_012 cluster の inheritance を
          解決した上で次に進める意思決定者)
        - **Decision**: exp_012 由来の MR 帯を live trading 候補に再昇格させるか /
          turnover 制約も無効と確認して棄却するか / 別 binding axis (slippage model)
          に kick-up するか
        - **Decision rule** (exp_012 synthesis を引き継いだ上で再定義):
          - YES = turnover ≤ 30%/month を保ったまま test Sharpe ≥ 0.5、WF mean Sharpe ≥ 0.4
          - NO = turnover 制約有り版でも test Sharpe < 0.3、binding axis は
            turnover ではなく slippage / fill model の側、と読み替える
          - KICK-UP = turnover 制約を強めると Sharpe が単調に劣化し、turnover-edge の
            Pareto trajectory が見えた場合 (Pattern C 形状)、layer を変える
        - **Knowledge output**: H1 の results.parquet 行 + Purpose 単一 H で
          十分なら synthesis 不要、複数 H に展開すれば exp_012 と同形式の synthesis +
          headline = Fig 4 (turnover 制約 sweep × Sharpe Pareto)

        ## Hypotheses tested
        - **H1** — exp_012 の RSI(14) ≤ 30 × signal-flip 構成を turnover-cap 30%/month
          制約下で再検証、test Sharpe ≥ 0.5

        ## Conclusion (preliminary)
        H1 verdict PENDING (実装中)。

        ## Why this matters
        exp_012 の cluster synthesis (`failure_mode='turnover'` の Pattern A)
        が正しい binding axis 認定だったかは、本ノートの H1 の verdict で
        決まる。supported なら axis 認定が正、rejected なら axis を slippage 側に
        付け替える必要があり、exp_014 (P_Y = exit を TP/SL に変更) の前提も
        揺らぐ。

        ## Figure plan
        - **Fig 1** — universe / split overlay
        - **Fig 2** — H1 累積 PnL (turnover-capped)
        - **Fig 3** — H1 月次 turnover 推移 (cap 線)
        - **Fig 4** (headline) — turnover-cap 強度 × Sharpe の Pareto
        """
    )
    return (mo,)


@app.cell
def __(mo):
    mo.md(r"## H1 — turnover-cap 30%/month 制約下で RSI(14) ≤ 30 × signal-flip を再検証")
    return


@app.cell
def __():
    UNIVERSE_H1 = "EURUSD 5min"
    PERIOD_H1 = "2018-01..2024-12"
    FEE_BPS_PER_SIDE = 1.0
    RSI_THRESHOLD_H1 = 30
    TURNOVER_CAP_MONTHLY = 0.30
    return (
        FEE_BPS_PER_SIDE,
        PERIOD_H1,
        RSI_THRESHOLD_H1,
        TURNOVER_CAP_MONTHLY,
        UNIVERSE_H1,
    )


@app.cell
def __(mo):
    mo.md(
        r"""
        ### H1 abstract
        exp_012 で binding axis と認定された turnover を 30%/month に制約した上で、
        RSI(14) ≤ 30 entry × signal-flip exit を再検証する。entry シグナル発火後、
        その月の累積 turnover が cap に達した時点で以降のエントリを停止する。
        net 1 bp/side で test Sharpe ≥ 0.5 を目標。閾値は exp_012 の H1 と同じ
        (= synthesis を承けて変更しない)。
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
