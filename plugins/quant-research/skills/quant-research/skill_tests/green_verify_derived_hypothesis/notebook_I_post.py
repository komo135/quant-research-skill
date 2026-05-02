# /// script
# requires-python = ">=3.10"
# ///
"""
exp_013_eurusd_meanreversion_turnover_capped.py — Case I post-GREEN

After GREEN:
- ## Origin セクションは無い (= F14 の本文流入を構造的に防ぐ)。
- exp_012 由来の handoff 経緯 / Pattern A 認定 / cross_h_synthesis Pattern 名 / "派生 Purpose" /
  "binding axis として認定された" は本文に侵入していない。
- 新ノートは独立した Purpose を持つ研究文書として読める。
- exp_012 との link は (1) Cycle goal の target_sub_claim_id、(2) Figure plan の minimal な比較
  系列名 (Fig 4 で h1_old / h1_new) — どちらも research content の表明であり、handoff 経緯ではない。
- 旧ノートの synthesis や handoff 経緯は decisions.md の exp_012 Purpose entry 側にだけ残る。
"""

import marimo

__generated_with = "0.9.0"
app = marimo.App(width="full")


@app.cell
def __():
    import marimo as mo
    mo.md(
        r"""
        # exp_013 — turnover-cap 制約下の EUR/USD 5min mean-reversion

        ## Purpose
        EUR/USD 5 分足において、月次 turnover を 30%/month 以下に制約 (= 一次制約)
        した上で、RSI(14) ≤ 30 entry × signal-flip exit 構成が net 1 bp/side
        fee で test Sharpe ≥ 0.5 を達成するかを検証する。

        ## Cycle goal — 5 items
        - **Consumer**: 自分の次 Purpose (live trading 候補としての MR の総合判定)
        - **Decision**: 本構成を live trading 候補に進めるか / turnover 軸も否定して MR 棄却するか / fill model 層に kick-up するか
        - **Decision rule**:
          - YES = turnover ≤ 30%/month を保ったまま test Sharpe ≥ 0.5、WF mean Sharpe ≥ 0.4
          - NO = test Sharpe < 0.3、binding axis = "turnover 制約を入れても MR は net で生存しない"
          - KICK-UP = turnover 制約を強めると Sharpe が単調劣化する Pareto trajectory が観測 (Pattern C)
        - **Knowledge output**: H1 の results.parquet 行 + Purpose-level synthesis +
          headline = Fig 4 (turnover-cap 強度 × Sharpe の Pareto)
        - **Target sub-claim id**: Primary G2.2 (`MR が realistic な execution 制約下で生存する`)。
          Secondary: なし。

        ## Hypotheses tested
        - **H1** — RSI(14) ≤ 30 × signal-flip 構成を turnover-cap 30%/month 制約下で実装、test Sharpe ≥ 0.5

        ## Conclusion (preliminary)
        H1 verdict PENDING (実装中)。

        ## Figure plan
        - **Fig 1** — universe / split overlay
        - **Fig 2** — H1 累積 PnL (turnover-capped)
        - **Fig 3** — H1 月次 turnover 推移 (cap 線)
        - **Fig 4** (headline) — turnover-cap 強度 × Sharpe の Pareto (h1_old / h1_capped の比較系列)
        """
    )
    return (mo,)


@app.cell
def __(mo):
    mo.md(r"## H1 — turnover-cap 30%/month 制約下で RSI(14) ≤ 30 × signal-flip を検証")
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
        月次 turnover が 30%/month に達した時点で entry を停止 (一次制約) する形で
        RSI(14) ≤ 30 × signal-flip exit を実装。net 1 bp/side で test Sharpe ≥ 0.5
        を達成するかを測る。閾値は EUR/USD 5min MR の標準ベンチマークから取った。
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
