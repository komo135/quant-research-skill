# /// script
# requires-python = ">=3.10"
# ///
"""
exp_022_topix_quality_3factor.py — Case K post-GREEN

After GREEN:
- Cycle goal の 5 項目目に target_sub_claim_id (Primary G1.3) を明示。
  本 Purpose は G1.1 (= exp_021 で confirmed 済) ではなく、G1.3 (`signal stacks with
  other quality factors without canceling`) を attack する。
- なぜ G1.3 を次に選んだか の根拠は decisions.md の exp_021 entry 末尾 (= "Design
  hypothesis at close" + "Research-goal sub-claim progress update" + "Derived Purposes")
  に記録される。新ノート本文は handoff 経緯を抱えない (= F14 解消継続)。
- "Sharpe を更に伸ばせるか" だけでなく、研究目標 G1.3 の sub-claim を attack することが
  Cycle goal で固定されている。次 Purpose 選定根拠が研究目標との距離で説明される
  (= F16 解消)。
"""

import marimo

__generated_with = "0.9.0"
app = marimo.App(width="full")


@app.cell
def __():
    import marimo as mo
    mo.md(
        r"""
        # exp_022 — TOPIX500 quality factor を 3-factor に拡張 (= G1.3 attack)

        ## Purpose
        TOPIX500 universe / 2014–2024 において、ROE / OCF margin / accruals quality
        の 3-factor を rank 平均で合成した quality シグナルが、net 5 bps fee で
        market-cap weighted ベースラインに対し WF mean Sharpe ≥ 0.5 を達成し、
        かつ 1-factor / 2-factor 構成と比べて factor 同士が **打ち消し合わない**
        (合成 Sharpe ≥ 2-factor 単独 Sharpe) ことを検証する。

        ## Cycle goal — 5 items
        - **Consumer**: 自分の次 Purpose (JP equity quality factor を多 factor
          スタックに組む段階の最終確認) — slug = `exp_quality_factor_stack`
        - **Decision**: 多 factor スタック組み込み時の重み比配分を決めるか / 棄却するか
        - **Decision rule**:
          - YES = 3-factor 合成で WF mean Sharpe ≥ 0.5、かつ 2-factor の Sharpe を有意に下回らない
          - NO = 3-factor が 2-factor と統計的に有意差なし、binding axis = "accruals quality は JP では効かない"
          - KICK-UP = 3-factor で turnover が 40%/month を超え net edge が消失、binding axis = "fee model"
        - **Knowledge output**: H1 の results.parquet 行 + Purpose-level synthesis +
          headline = Fig 4 (1-factor / 2-factor / 3-factor の累積 PnL 比較)
        - **Target sub-claim id**: Primary G1.3 (`signal stacks with other quality
          factors without canceling`)。Secondary: 触れない。G1.1 は別 Purpose で
          既に状態が確定している (README サブクレーム status を参照)。

        ## Hypotheses tested
        - **H1** — ROE × OCF margin × accruals quality の 3-factor 等重み合成、
          WF mean Sharpe ≥ 0.5 かつ 2-factor の Sharpe と Diebold-Mariano 検定で
          下回らない (有意水準 5%)

        ## Conclusion (preliminary)
        H1 verdict = PENDING (実装中)。

        ## Figure plan
        - **Fig 1** — universe / split overlay
        - **Fig 2** — H1 累積 PnL (3-factor 版)
        - **Fig 3** — accruals quality 単独の IC 時系列
        - **Fig 4** (headline) — 1-factor / 2-factor / 3-factor の累積 PnL 比較
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
        合成、上位 quintile long-only。net 5 bps で WF mean Sharpe ≥ 0.5 かつ
        2-factor 構成 (= 既に G1.1 を confirmed にした exp_021 の H2 構成) との
        差が DM 検定で有意に正である、を満たすかを測る。
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
