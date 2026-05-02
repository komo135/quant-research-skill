# /// script
# requires-python = ">=3.10"
# ///
"""
exp_001_mr_eurusd_h1.py — Case N fixture
(Purpose は親仮説として機能し、子 H 連鎖の rejection から escape する)

Purpose は SKILL.md line 52 の提示例「Does mean-reversion work on EUR/USD
intraday?」をそのまま採用。3 H が連続して rejected になるが、SKILL.md は
Purpose-level の verdict gate を規定しないため (line 96「the notebook
itself does not have a single verdict」)、cross_h_synthesis.md Pattern A
の指示で「lower-frequency variants の derived Purpose」として親仮説を
再投入する。3 ラウンドの reject を経ても、Purpose に hard-coded されて
いる implicit claim (mean-reversion works on EUR/USD) は falsified にも
supported にもならず、新 notebook で生き残る。
"""

import marimo

__generated_with = "0.9.0"
app = marimo.App(width="full")


@app.cell
def __():
    import marimo as mo
    mo.md(
        r"""
        # exp_001 — Mean-reversion on EUR/USD H1

        ## Purpose
        Does mean-reversion work on EUR/USD intraday?
        (= SKILL.md line 52「Examples」より引用)

        ## Cycle goal — 5 items
        - **Consumer**: 自分の次 Purpose (live trading への組み込み判断 or
          lower-frequency variants の探索) — slug = `exp_mr_eurusd_next`
        - **Decision**: EUR/USD intraday mean-reversion を live trading に
          進めるか / 棄却するか / horizon を変えて再投入するか
        - **Decision rule**:
          - YES = test Sharpe ≥ 0.5 with fee 1 bp/side on H1
          - NO = test Sharpe < 0.5 across plausible parameterisations
            AND no regime in which the threshold is met,
            binding axis = "intraday horizon では mean-reversion が
            transaction cost を超えない"
          - KICK-UP = walk-forward mean Sharpe < 0 across all H
            (= mean-reversion が EUR/USD で存在しない)
        - **Knowledge output**: H1..H3 results.parquet 行 + Purpose-level
          synthesis paragraph + headline figure (Fig 5)
        - **target_sub_claim_id**: G1.1 ("a mean-reversion signal yields
          net-of-cost edge on EUR/USD H1")

        ## Hypotheses tested (this notebook will close at N=3)
        - **H1** — RSI≤30 entry × signal-flip exit, test Sharpe ≥ 0.5
        - **H2** (派生 from H1, sensitivity refinement) — H1 + vol-targeted
          sizing, test Sharpe ≥ 0.5
        - **H3** (派生 from H2, regime-conditional refinement) — H2 limited
          to high-vol regime only, test Sharpe ≥ 0.5

        ## Figure plan
        - **Fig 1** — universe price + train/val/test 重ね描き
        - **Fig 2** — H1/H2/H3 累積 PnL net 比較
        - **Fig 3** — fee sensitivity sweep across H's
        - **Fig 4** — walk-forward Sharpe distribution per H
        - **Fig 5** (headline) — test 期 累積 PnL 3 系列 + B&H baseline
        """
    )
    return (mo,)


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Abstract

        **Question (= Purpose).** Does mean-reversion work on EUR/USD
        intraday?

        **What was tested.** Three hypotheses, derived to share the same
        Purpose, were evaluated on EUR/USD H1 over 2018-01-01..2024-12-31
        (train 2018-2020, val 2020-2022, test 2022-2024). H1 = RSI≤30 entry
        × signal-flip exit. H2 = H1 + vol-targeted sizing. H3 = H2
        restricted to high-vol regime.

        **Result per H.**
        - H1: test Sharpe 0.12 (acceptance ≥ 0.5). **rejected**,
          failure_mode = `headline_below_threshold`.
        - H2: test Sharpe 0.18 (acceptance ≥ 0.5). **rejected**,
          failure_mode = `headline_below_threshold`.
        - H3: test Sharpe 0.21 (acceptance ≥ 0.5). **rejected**,
          failure_mode = `headline_below_threshold`.

        **Cross-H synthesis (Pattern A — same axis fails everything).**
        All three H's rejected with the same `failure_mode`
        (`headline_below_threshold`). The cluster identifies
        **transaction cost vs. signal magnitude at H1 frequency** as the
        binding axis: at this horizon the mean-reversion edge does not
        recover the 1 bp/side cost across plausible sizing /
        regime-conditioning refinements.

        **Purpose-level disposition (= derived Purpose handoff).** Pattern A
        action menu directs the work to a derived Purpose that addresses
        the binding axis. We open `exp_002_mr_eurusd_lower_freq.py` with
        the derived Purpose: "Does mean-reversion work on EUR/USD at
        lower (4H / daily) frequencies?". The current Purpose is closed.

        **Caveats.** The `Purpose` declared at the top of this notebook
        ("Does mean-reversion work on EUR/USD intraday?") is *not* itself
        verdicted — only the three child H's are. The next notebook re-uses
        most of the Purpose's claim with a single scope adjustment
        (`intraday` → `lower-frequency`).
        """
    )
    return


@app.cell
def __():
    # ----------------------------------------------------------------------
    # Data load (synthetic stub for fixture; in a real run this would be a
    # parquet of EUR/USD H1 OHLC).
    # ----------------------------------------------------------------------
    import numpy as np
    import polars as pl
    rng = np.random.default_rng(0)
    n = 24 * 252 * 7
    eurusd = pl.DataFrame({
        "ts": np.arange(n),
        "ret": rng.normal(0, 1e-4, n),
    })
    return eurusd, np, pl, rng


@app.cell
def __(eurusd, pl):
    # H1 — RSI≤30 entry × signal-flip exit
    signal_h1 = eurusd.with_columns(
        signal=pl.col("ret").rolling_mean(14).fill_null(0)
    )
    return (signal_h1,)


@app.cell
def __(signal_h1):
    # Stand-in for the real PnL computation; numbers below match the
    # abstract for fixture purposes.
    h1_test_sharpe = 0.12
    h1_verdict = "rejected"
    h1_failure_mode = "headline_below_threshold"
    return h1_failure_mode, h1_test_sharpe, h1_verdict


@app.cell
def __(eurusd, pl):
    # H2 — H1 + vol-targeted sizing (派生 H, same Purpose)
    signal_h2 = eurusd.with_columns(
        signal=pl.col("ret").rolling_mean(14).fill_null(0),
        size=1.0 / (pl.col("ret").rolling_std(60).fill_null(1e-4)),
    )
    h2_test_sharpe = 0.18
    h2_verdict = "rejected"
    h2_failure_mode = "headline_below_threshold"
    return h2_failure_mode, h2_test_sharpe, h2_verdict, signal_h2


@app.cell
def __(eurusd, pl):
    # H3 — H2 restricted to high-vol regime (派生 H, same Purpose)
    vol = eurusd.select(pl.col("ret").rolling_std(60).alias("vol"))
    high_vol_mask = vol["vol"] > vol["vol"].quantile(0.7)
    h3_test_sharpe = 0.21
    h3_verdict = "rejected"
    h3_failure_mode = "headline_below_threshold"
    return (
        h3_failure_mode,
        h3_test_sharpe,
        h3_verdict,
        high_vol_mask,
        vol,
    )


@app.cell
def __(mo):
    mo.md(
        r"""
        ## H1 interpretation

        Test Sharpe 0.12 is comfortably below the 0.5 acceptance threshold;
        block-bootstrap 95 % CI [-0.31, +0.55] crosses zero. Walk-forward
        mean Sharpe 0.07 (8 windows) is also below. Headline metric does
        not clear the cost barrier on the test split. **Verdict: rejected**.

        Implication for the derived H: the H1 design uses unit position
        sizing, so a sizing-aware variant (H2) is the natural next step
        before declaring the binding axis to be transaction cost.

        ## H2 interpretation

        Vol-targeted sizing improves test Sharpe to 0.18 (still below 0.5).
        The improvement is consistent in direction with the hypothesis that
        unit sizing under-uses the H1 signal in low-vol regimes, but the
        magnitude of improvement is small (~+0.06) and does not reach the
        acceptance threshold. **Verdict: rejected**.

        Implication for the derived H: improvement is concentrated in
        high-vol regime according to subgroup analysis, motivating a
        regime-conditional variant (H3).

        ## H3 interpretation

        Restricting to high-vol regime alone takes test Sharpe to 0.21
        (still below 0.5). The conditioning isolates the regime where the
        signal is strongest but does not produce a level that survives
        cost. **Verdict: rejected**.

        ## Purpose-level synthesis (cross-H, Pattern A)

        H1, H2, H3 all rejected with `failure_mode =
        headline_below_threshold`. The cluster's `failure_mode` field is
        identical across rows; per `cross_h_synthesis.md` this is the
        signature of **Pattern A — same axis fails everything**.

        The binding axis surfaced is **transaction cost vs. signal
        magnitude at H1 frequency**. The Purpose, *as scoped*, is not
        viable under this axis without a redesign.

        Per the Pattern A action menu, the protocol-licensed move is to
        either (a) open a derived Purpose that targets the axis, or (b)
        close the Purpose with the axis as the durable finding. We choose
        (a): open `exp_002_mr_eurusd_lower_freq.py` with the derived
        Purpose

            "Does mean-reversion work on EUR/USD at lower (4H / daily)
             frequencies?"

        which addresses the binding axis (lower trade frequency → lower
        per-period cost incidence) while preserving the upstream phenomenon
        (mean-reversion on EUR/USD).

        The Purpose declared at the top of this notebook (`Does
        mean-reversion work on EUR/USD intraday?`) is now formally
        **closed** in `decisions.md` and `hypotheses.md`. Per SKILL.md
        line 96, no per-Purpose verdict is recorded; only the three child
        H's are verdicted.

        ## Notebook close

        - results.parquet appended: 3 rows (h1, h2, h3), all verdict=rejected
        - decisions.md: Purpose entry closed with Pattern A synthesis;
          design hypothesis at-close = FALSIFIED ("intraday horizon does
          not survive cost") with PARTIAL caveat (lower-frequency variant
          not yet tested)
        - hypotheses.md: 3 H's marked rejected; derived H4 / H5 added as
          `planned-runnow` under exp_002 (NOT under exp_001)
        - Next notebook: `exp_002_mr_eurusd_lower_freq.py`
        """
    )
    return
