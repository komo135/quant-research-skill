# /// script
# requires-python = ">=3.10"
# ///
"""
pur_001_mr_eurusd_h1.py — Case N GREEN

Re-running instruction_N under the post-F23/F24/F25 skill produces this
notebook. Three changes vs. red_hypothesis_experiment_inversion/notebook_N:

1. Purpose is declarative falsifiable (= the parent research thesis),
   verdicted at notebook closure (F23 counter — see SKILL.md
   "Purpose-level closure gate" and the rewritten Purpose vs. Hypothesis
   table).
2. Schema uses `purpose_id` (= the notebook = the Purpose); each `## H<id>`
   block IS one experiment (F24 counter — see results_db_schema.md and
   SKILL.md step 14).
3. Only H1 enters the hypothesis log. The original "vol-targeted sizing
   variant" and "high-vol regime restriction" fail derived-H admissibility
   (F25 counter — see SKILL.md "Derived hypothesis admissibility" and
   hypothesis_cycles.md routing sub-step 0). They are moved into H1's
   robustness section as 2D sensitivity grids.
4. Pattern A carry-forward is only invoked AFTER the parent thesis is
   verdicted refuted at notebook closure (F23 counter — see
   cross_h_synthesis.md Pattern A action menu and Handoff section
   precondition 0). The derived Purpose tests a thesis distinct from
   the closed one, not a near-paraphrase.
"""

import marimo

__generated_with = "0.9.0"
app = marimo.App(width="full")


@app.cell
def __():
    import marimo as mo
    mo.md(
        r"""
        # pur_001 — Mean-reversion on EUR/USD H1

        ## Purpose (parent research thesis — verdicted at notebook closure)
        Mean-reversion at H1 frequency on EUR/USD generates risk-adjusted
        edge net of cost (≥ 0.5 test Sharpe with 1 bp/side fees, on the
        2022-01-17..2024-12-31 test split, against B&H baseline).

        ## Cycle goal — 5 items
        - **Consumer**: 自分の次 Purpose (live trading への組み込み判断 or
          a derived Purpose with a different parent thesis if H1 frequency
          is refuted) — slug = `pur_mr_eurusd_next`
        - **Decision**: EUR/USD H1 mean-reversion を live trading に進めるか
          / 棄却するか / 別の thesis (lower frequency, different mechanism) で
          再検討するか
        - **Decision rule**:
          - YES = test Sharpe ≥ 0.5 with fee 1 bp/side on H1
          - NO = test Sharpe < 0.5 across plausible parameterisations
            AND no regime in which the threshold is met,
            binding axis = "intraday horizon では mean-reversion が
            transaction cost を超えない"
          - KICK-UP = walk-forward mean Sharpe < 0 across all H
        - **Knowledge output**: H1 results.parquet 行 + Purpose-level
          verdict + headline figure (Fig 5)
        - **target_sub_claim_id**: G1.1

        ## Hypothesis tested (this notebook closes at N=1)
        - **H1** — RSI≤30 entry × signal-flip exit, test Sharpe ≥ 0.5
          with fee 1 bp/side on EUR/USD H1, 2022-2024 test split

        ## What is NOT a separate hypothesis here (per derived-H admissibility)
        - "vol-targeted sizing variant of H1" — would be a sizing-axis
          parameter sweep without an independent falsifiable claim or
          stated purpose distinct from H1; reported as 2D robustness
          grid inside H1, not as H2
        - "high-vol regime restriction of the sizing variant" — would be a
          regime-axis sweep without an independent claim; reported as a
          regime-conditional row in H1's robustness table, not as H3

        ## Figure plan
        - **Fig 1** — universe price + train/val/test 重ね描き
        - **Fig 2** — H1 累積 PnL net vs. B&H baseline (test 期)
        - **Fig 3** — fee sensitivity sweep (H1 robustness)
        - **Fig 4** — sizing × regime 2D sensitivity grid (H1 robustness;
          NOT separate H's)
        - **Fig 5** (headline) — test 期 累積 PnL with bootstrap CI

        ## Reader takeaway (one sentence)
        Whether mean-reversion at H1 frequency on EUR/USD survives
        transaction cost, with the binding axis named when refuted.
        """
    )
    return (mo,)


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Abstract

        **Parent thesis (= Purpose).** Mean-reversion at H1 frequency on
        EUR/USD generates risk-adjusted edge net of cost (≥ 0.5 test Sharpe
        with 1 bp/side fees, 2022-2024 test split).

        **What was tested.** One hypothesis (H1) testing the parent
        thesis on EUR/USD H1, with sizing and regime sensitivity as
        robustness inside H1.

        **Per-H result.** H1: test Sharpe 0.12, B&H test Sharpe 0.07,
        gap +0.05 (acceptance ≥ 0.5). **rejected**, failure_mode =
        `headline_below_threshold`.

        **Robustness inside H1 (not separate H's).**
        - Sizing sweep (unit / vol-targeted / Kelly-cap): max test Sharpe
          0.18 at vol-targeted; still below 0.5.
        - Regime conditioning (low-vol / mid-vol / high-vol subsamples):
          max test Sharpe 0.21 in high-vol regime; still below 0.5.
        - Fee sensitivity (0.5 / 1 / 2 bp/side): break-even fee 0.4 bp,
          below the realistic 1 bp/side floor.

        **Purpose-level verdict.** **refuted.** The parent thesis is
        rejected on the test split: at H1 frequency on EUR/USD,
        mean-reversion does not generate ≥ 0.5 test Sharpe net of
        1 bp/side fees, even under the most favorable sizing and regime
        conditioning observed in robustness analysis.

        **Binding axis.** transaction cost vs. signal magnitude at H1
        frequency. The signal does carry mild predictive information
        (positive but small Sharpe across robustness configurations);
        it does not carry enough to clear realistic fees.

        **Carry-forward.** This notebook closes here. A derived Purpose
        is opened separately (`pur_002_mr_eurusd_lower_freq.py`) with a
        **different parent thesis**: "Mean-reversion at lower frequencies
        (4H / daily) on EUR/USD generates risk-adjusted edge net of
        cost". Per cross_h_synthesis.md Pattern A handoff precondition 0,
        the closing notebook records the verdict on the *current* parent
        thesis (refuted) before any derived Purpose may open.
        """
    )
    return


@app.cell
def __():
    # ---- Data load (synthetic stub for fixture) -------------------------
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
    # ---- H1 — RSI≤30 entry × signal-flip exit ---------------------------
    signal_h1 = eurusd.with_columns(
        signal=pl.col("ret").rolling_mean(14).fill_null(0)
    )
    h1_test_sharpe = 0.12
    h1_bh_test_sharpe = 0.07
    h1_verdict = "rejected"
    h1_failure_mode = "headline_below_threshold"
    return (
        h1_bh_test_sharpe,
        h1_failure_mode,
        h1_test_sharpe,
        h1_verdict,
        signal_h1,
    )


@app.cell
def __(mo):
    mo.md(
        r"""
        ## H1 robustness (sizing × regime grid, fee sweep)

        Sizing sweep, regime conditioning, and fee sensitivity are
        reported here as **robustness inside H1**, not as separate H's.
        Per `references/robustness_battery.md` and the derived-H
        admissibility rule (`SKILL.md` Derived hypothesis admissibility),
        a 1-axis sweep over sizing or regime is not a new hypothesis —
        it's robustness for the parent H.

        ### Sizing × regime grid
        | sizing \ regime | low-vol | mid-vol | high-vol |
        |---|---|---|---|
        | unit          | 0.04 | 0.10 | 0.18 |
        | vol-targeted  | 0.06 | 0.14 | 0.21 |
        | Kelly-cap     | 0.05 | 0.12 | 0.19 |

        Maximum cell: 0.21 (vol-targeted × high-vol). Still well below
        0.5 acceptance threshold. The signal exists; the magnitude does
        not.

        ### Fee sensitivity
        | fee bp/side | test Sharpe |
        |---|---|
        | 0.0 | 0.41 |
        | 0.5 | 0.27 |
        | 1.0 | 0.12 (= headline) |
        | 2.0 | -0.18 |

        Break-even fee ≈ 0.4 bp/side. Realistic floor (institutional
        EUR/USD spread + slippage) is ≥ 1 bp/side. The headline
        configuration sits below break-even on a realistic fee.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## H1 interpretation

        Test Sharpe 0.12 is below the 0.5 acceptance threshold;
        block-bootstrap 95 % CI [-0.31, +0.55] crosses zero. Walk-forward
        mean Sharpe 0.07 (8 windows) is also below. The signal carries
        mild but positive predictive information across the robustness
        grid (0.04 to 0.21 across 9 sizing × regime cells), but no
        configuration clears the cost barrier on the test split.

        **Verdict (per-H): rejected**, failure_mode =
        `headline_below_threshold`. The H1 verdict is the per-H
        verdict; the parent thesis verdict is below.

        ## Purpose-level closure (parent thesis verdict)

        **Parent thesis verdict: refuted.**

        The parent thesis ("Mean-reversion at H1 frequency on EUR/USD
        generates risk-adjusted edge net of cost") is rejected on the
        test split. Even under the most favorable sizing × regime
        configuration observed in H1 robustness (vol-targeted ×
        high-vol regime, test Sharpe 0.21), the parent thesis's
        threshold (≥ 0.5 test Sharpe) is not met.

        **Binding axis (per cross_h_synthesis.md Pattern A):**
        transaction cost vs. signal magnitude at H1 frequency. The
        H1-frequency signal has positive expected value (point estimate
        +0.04 to +0.21 across robustness configurations) but the
        magnitude does not survive the realistic fee floor (≥ 1
        bp/side); break-even fee is approximately 0.4 bp/side.

        **What this Purpose closes for the project (= G1.1 transition).**
        G1.1 ("a mean-reversion signal yields net-of-cost edge on EUR/USD
        H1") is moved to `falsified` for the H1-frequency operationalization.
        Whether mean-reversion at lower frequencies (4H / daily) survives
        is a separate question and a separate parent thesis, attacked in
        the derived Purpose `pur_002_mr_eurusd_lower_freq.py` with the
        thesis "Mean-reversion at lower frequencies on EUR/USD generates
        risk-adjusted edge net of cost". That derived Purpose is NOT a
        rebranding of the current Purpose — it tests a different
        parent thesis on the same instrument.

        ## Notebook close

        - results.parquet appended: 1 row (h1, verdict=rejected,
          purpose_id=pur_001_mr_eurusd_h1)
        - decisions.md: Purpose entry closed with Pattern A binding-axis;
          design hypothesis at-close = FALSIFIED on G1.1 for H1-frequency
          operationalization
        - hypotheses.md: H1 marked rejected; no further H's added under
          this `purpose_id`
        - Next notebook: `pur_002_mr_eurusd_lower_freq.py` (different
          parent thesis, opened only after the above verdict is in
          writing per cross_h_synthesis.md Handoff precondition 0)
        """
    )
    return
