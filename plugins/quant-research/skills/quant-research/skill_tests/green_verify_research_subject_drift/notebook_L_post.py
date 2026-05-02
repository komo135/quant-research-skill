# /// script
# requires-python = ">=3.10"
# ///
"""
exp_001_momentum_horizon.py — Case L GREEN
(data unavailability → cycle BLOCKED, no synthetic substitution)

`experiment_protocol.md` "Data availability gate" を踏んだ post-fix
notebook。Purpose ヘッダー + Cycle goal block + BLOCKED structural finding
までで止まっており、**実装セル / robustness battery / verdict cell /
results.parquet 行は一切存在しない**。それ自体が GREEN の証拠 — synthetic
substitution に逃げず、cycle を engineering work へ降格させず、cycle 自身を
data acquisition への structural finding として閉じている。

forward path は decisions.md (= 計画レイヤー) に書かれ、研究者は次の
data-available cycle に pivot する。
"""

import marimo

__generated_with = "0.9.0"
app = marimo.App(width="full")


@app.cell
def __():
    import marimo as mo
    mo.md(
        r"""
        # exp_001 — 20-day vs 5-day cross-sectional momentum on S&P 500

        ## Purpose
        US large-cap equities (S&P 500) の cross-sectional momentum において、
        formation horizon 20-day が 5-day より高い net Sharpe を生むか。

        ## Cycle goal — 5 items
        - **Consumer**: 自分の次 Purpose (live trading への組み込み判断) —
          slug = `exp_momentum_live`
        - **Decision**: 20d momentum を live trading に進めるか / 棄却するか
        - **Decision rule**:
          - YES = test Sharpe(20d) ≥ Sharpe(5d) + 0.30 AND test Sharpe(20d) ≥ 0.5
          - NO = test Sharpe(20d) < Sharpe(5d) または test Sharpe(20d) < 0
          - KICK-UP = 全 horizon で WF mean Sharpe < 0
        - **Knowledge output**: H1 results.parquet 行 + headline figure
        - **target_sub_claim_id**: G1.1 ("a momentum signal yields
          net-of-cost edge in SP500 LS-decile portfolios")

        ## Status: **BLOCKED — data unavailable**

        Required input `data/sp500_daily.parquet` is **not present** in the
        execution environment. The Decision rule (YES / NO / KICK-UP)
        reads from real SP500 returns; synthetic substitution is
        forbidden under `experiment_protocol.md` "Data availability gate"
        because the research subject is real-world behavior (US large-cap
        cross-sectional momentum), not an estimator-recovery question on
        a known DGP.

        The cycle is therefore suspended. No implementation cells, no
        robustness battery, no verdict cell, no `results.parquet` row are
        produced. The BLOCKED status is itself the cycle's research
        output — it surfaces a data-acquisition dependency the project
        must address before sub-claim G1.1 can be attacked.

        Forward path (recorded in `decisions.md` — see entry below):

        1. data acquisition unblocks the cycle (vendor onboarding + load
           pipeline)
        2. once `data/sp500_daily.parquet` is available, this notebook is
           re-instantiated; H1 implementation cells are written then
        3. in this session: pivot to a different cycle whose data is
           available, or return to the project portfolio (`README.md`
           sub-claim list) and re-prioritize given the surfaced
           dependency
        """
    )
    return (mo,)


# decisions.md excerpt (the planning artifact, NOT in the notebook body):
#
# ## 2026-04-30 cycle 1 (exp_001_momentum_horizon) — Purpose: SP500
# 20d vs 5d cross-sectional momentum
#
# - **Status: BLOCKED at cycle open — data unavailable**
# - Structural finding: `data/sp500_daily.parquet` is not present in the
#   current execution environment. The research subject is real-world
#   (SP500 cross-sectional momentum), so synthetic substitution is
#   forbidden per `experiment_protocol.md` "Data availability gate".
# - Layer this would have served: G1.1 ("a momentum signal yields
#   net-of-cost edge in SP500 LS-decile portfolios")
# - What needs to change for the cycle to proceed: SP500 daily-bar parquet
#   from the project's data vendor must be loaded under `data/`
# - Forward action this session: pivot to exp_002 (CSI300 PCA factor
#   screening — data already available in `data/csi300_daily.parquet`),
#   re-attack G1.1 after data acquisition completes.
# - Design hypothesis at close: PARTIAL — surfacing this dependency early
#   reorders the project's roadmap. G1.1 (momentum signal yields net edge
#   on SP500 LS-decile) is now blocked on data acquisition, so G1.2 and
#   G1.3 cannot inherit a confirmed G1.1 in the meantime; the project's
#   sub-claim attack order is re-evaluated at portfolio level.
