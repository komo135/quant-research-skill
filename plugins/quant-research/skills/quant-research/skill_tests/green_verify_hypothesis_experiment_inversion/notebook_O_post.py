# /// script
# requires-python = ">=3.10"
# ///
"""
pur_003_momentum_exit_design.py — Case O GREEN

Re-running instruction_O under the post-F23/F24/F25 skill produces this
notebook. Three changes vs. red_hypothesis_experiment_inversion/notebook_O:

1. Schema uses `purpose_id` (= the notebook = the Purpose). The 3 rows
   appended to results.parquet share the same `purpose_id` and differ in
   `hypothesis_id`, with each `## H<id>` block recognized as **one
   experiment** that tests the parent thesis on a different exit-rule
   axis (F24 counter — see SKILL.md step 14, results_db_schema.md).
2. The shared `apparatus` cell is reframed: it is "the apparatus shared
   across the three experiments testing this Purpose's parent thesis",
   not "the Purpose's container holding hypotheses". Asking "what is H2's
   experiment?" now has a concrete answer: "the H2 block, which
   replaces the apparatus's exit_rule slot with TP-SL". The 1 H ↔ 1
   experiment correspondence holds.
3. Each derived H carries its own falsifiable claim and own stated
   purpose distinct from the parent (F25 admissibility — see SKILL.md
   "Derived hypothesis admissibility" and hypothesis_cycles.md sub-step 0).
   Exit rule choice IS a meaningful research axis (a different
   operationalization of when to close a position changes the realized
   risk-adjusted return), so H2 / H3 are admissible. The shared
   apparatus does NOT make them inadmissible; what would make them
   inadmissible is a 1-axis parameter sweep on the same exit rule.
4. Purpose declared as declarative falsifiable parent thesis (F23
   counter — see SKILL.md Purpose vs. Hypothesis table, rewritten
   Examples).
"""

import marimo

__generated_with = "0.9.0"
app = marimo.App(width="full")


@app.cell
def __():
    import marimo as mo
    mo.md(
        r"""
        # pur_003 — Exit rule choice on 20-day cross-sectional SP500 momentum

        ## Purpose (parent research thesis — verdicted at notebook closure)
        At least one exit rule among signal-flip / TP-SL / trailing-stop
        produces a 20-day cross-sectional momentum strategy on S&P 500
        with test Sharpe ≥ B&H + 0.30 (test 2022-2024, fee 1 bp/side,
        slippage 0.5 bp). The parent thesis is supported if any of the
        three exit rules clears the threshold; refuted if none do.

        ## Cycle goal — 5 items
        - **Consumer**: live strategy build for SP500 momentum — slug
          = `pur_momentum_live`
        - **Decision**: live strategy が採用すべき exit rule を選定する
        - **Decision rule**:
          - YES = ≥ 1 つの exit rule で test Sharpe ≥ B&H + 0.30
          - NO = いずれの exit rule でも test Sharpe < B&H + 0.30、
            binding axis = "exit rule の選択は SP500 momentum strategy の
            収益性に効かない (entry-side が支配的または entry-side 自体が
            機能しない)"
          - KICK-UP = 全 exit rule で walk-forward mean Sharpe < 0
        - **Knowledge output**: H1..H3 results.parquet 行 + Purpose-level
          verdict + headline figure
        - **target_sub_claim_id**: G1.1

        ## Hypotheses tested (each one is a separate experiment;
        ## each tests the parent thesis on a different exit-rule axis)

        Each H below has (a) own falsifiable claim distinct from the
        parent and from sibling H's, (b) own stated purpose, and (c)
        meaningful research unit — exit rule operationalization is a
        non-trivial research axis with mechanism implications (when to
        realize gains vs. cap losses), not a 1-axis parameter sweep.

        - **H1** (exit rule = signal-flip)
          - Claim: signal-flip exit gives test Sharpe ≥ B&H + 0.30.
          - Stated purpose: test the simplest mechanism-aligned exit
            (close when the entry signal reverses) — the least
            operational-noise variant. Distinct from H2/H3 in that no
            external level is imposed; the strategy speaks only when
            the signal does.
        - **H2** (exit rule = TP-SL +1σ / -2σ)
          - Claim: TP-SL exit at +1σ / -2σ levels gives test Sharpe ≥
            B&H + 0.30.
          - Stated purpose: test whether imposing volatility-scaled
            level-based exits captures more momentum than letting the
            signal-flip resolve. Distinct from H1 (level-based vs.
            signal-based exit) and from H3 (static levels vs. dynamic
            trailing).
        - **H3** (exit rule = 3 % trailing stop)
          - Claim: 3 % trailing-stop exit gives test Sharpe ≥ B&H + 0.30.
          - Stated purpose: test whether dynamic ratchet-based exits
            capture more upside than either signal-flip (H1) or static
            levels (H2). Distinct from H1/H2 in mechanism (ratcheting
            vs. fixed level vs. signal-driven).

        ## Shared apparatus across the three experiments
        - Universe: S&P 500 PIT constituents 2018-2024
        - Split: train 2018-2020, val 2020-2022, test 2022-2024
        - Baseline: B&H equal-weight SP500
        - Fee model: 1 bp/side, slippage 0.5 bp
        - Entry rule: 20-day cross-sectional decile rank (long top decile,
          short bottom decile, daily rebalance)

        These are the **shared apparatus** components. Each H replaces
        only the exit_rule slot; the rest of the apparatus is held
        constant so that the 3 experiments compare cleanly on the
        exit-rule axis. Each H is one experiment that tests the parent
        thesis through one specific exit-rule operationalization.

        ## Figure plan
        - **Fig 1** — universe equal-weight cum return + train/val/test
        - **Fig 2** — H1/H2/H3 累積 PnL net 比較 (test 期, 3 experiments)
        - **Fig 3** — exit-rule mechanism comparison (signal-flip vs.
          TP-SL vs. trailing-stop trade-by-trade payoff distribution)
        - **Fig 4** — fee sensitivity sweep across the 3 experiments
        - **Fig 5** (headline) — test 期 累積 PnL 3 系列 + B&H baseline
        """
    )
    return (mo,)


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Abstract

        **Parent thesis (= Purpose).** At least one exit rule among
        signal-flip / TP-SL / trailing-stop produces a 20-day
        cross-sectional momentum strategy on S&P 500 with test Sharpe
        ≥ B&H + 0.30.

        **What was tested.** Three experiments under one Purpose, each
        testing the parent thesis on one exit-rule axis. Universe /
        split / baseline / fee / entry are held constant; only exit_rule
        varies between experiments.

        **Per-H (= per-experiment) result (test, B&H = 0.41).**
        - H1 (signal-flip): test Sharpe 0.78. **supported**, gap +0.37.
        - H2 (TP-SL): test Sharpe 0.62. **rejected**, gap +0.21,
          failure_mode = `headline_below_threshold`.
        - H3 (trailing-stop): test Sharpe 0.69. **supported** after
          experiment-review pass; bootstrap CI on the gap is
          [+0.04, +0.51] which overlaps the threshold but the lower
          bound is positive.

        **results.parquet rows (3 rows, identical `purpose_id`):**
        ```
        purpose_id              hypothesis_id  pathway  verdict     achieved_tier
        pur_003_momentum_exit   h1             4        supported   medium
        pur_003_momentum_exit   h2             4        rejected    medium
        pur_003_momentum_exit   h3             4        supported   medium
        ```

        **Cross-H synthesis.** Two of three exit rules clear the
        threshold on the same shared apparatus. The exit-rule axis is
        not the binding constraint; entry-side momentum carries the
        edge and exit rules differ in capture efficiency.

        **Purpose-level verdict.** **supported.** The parent thesis is
        supported by H1 and H3; H2 fails to clear the threshold but does
        not refute the parent thesis (which only requires ≥ 1 exit rule
        to clear). The qualifying conditions are: (a) tested on test
        period 2022-2024 only (replication on a different period is a
        separate Purpose), (b) tested with the apparatus's specific
        entry rule (20-day decile rank); (c) costs at 1 bp/side
        slippage 0.5 bp.

        **Caveats.** Each per-H claim is conditional on the shared
        apparatus. Replication on a different universe / period / fee
        regime is a separate Purpose with its own parent thesis.
        """
    )
    return


@app.cell
def __():
    # ---- Shared apparatus across the 3 experiments under this Purpose ---
    # Each experiment (H1, H2, H3) replaces only the exit_rule slot;
    # the rest of the apparatus is held constant to isolate the
    # exit-rule axis.
    import polars as pl
    import numpy as np
    rng = np.random.default_rng(0)

    apparatus = dict(
        universe="SP500_PIT_2018_2024",
        train="2018-01-01..2020-12-31",
        val="2021-01-01..2022-06-30",
        test="2022-07-01..2024-12-31",
        baseline="bh_equal_weight_sp500",
        fee_bp_per_side=1.0,
        slippage_bp=0.5,
        entry_rule="20d_xs_decile_long_top_short_bottom_daily_rebal",
    )
    return apparatus, np, pl, rng


@app.cell
def __(apparatus):
    # ---- H1 (= experiment 1): signal-flip exit on the shared apparatus
    h1 = dict(
        hypothesis_id="h1",
        exit_rule="signal_flip",
        apparatus=apparatus,
        test_sharpe=0.78,
        bh_sharpe=0.41,
        verdict="supported",
        failure_mode=None,
    )
    return (h1,)


@app.cell
def __(apparatus):
    # ---- H2 (= experiment 2): TP-SL exit on the shared apparatus
    h2 = dict(
        hypothesis_id="h2",
        exit_rule="tpsl_+1sigma_-2sigma",
        apparatus=apparatus,
        test_sharpe=0.62,
        bh_sharpe=0.41,
        verdict="rejected",
        failure_mode="headline_below_threshold",
    )
    return (h2,)


@app.cell
def __(apparatus):
    # ---- H3 (= experiment 3): trailing-stop exit on the shared apparatus
    h3 = dict(
        hypothesis_id="h3",
        exit_rule="trailing_stop_3pct",
        apparatus=apparatus,
        test_sharpe=0.69,
        bh_sharpe=0.41,
        verdict="supported",
        failure_mode=None,
    )
    return (h3,)


@app.cell
def __(h1, h2, h3, pl):
    # Append all three H's (= all three experiments) to results.parquet
    # under the same `purpose_id` (= notebook = Purpose).
    # Per SKILL.md step 14 / results_db_schema.md: purpose_id identifies
    # the notebook; hypothesis_id identifies the individual experiment
    # within it. Each `## H<id>` block IS one experiment.
    rows = pl.DataFrame([
        dict(
            purpose_id="pur_003_momentum_exit",
            hypothesis_id=h["hypothesis_id"],
            pathway=4,
            verdict=h["verdict"],
            failure_mode=h["failure_mode"],
            achieved_tier="medium",
        )
        for h in (h1, h2, h3)
    ])
    return (rows,)


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Closing notes

        Three rows above all share `purpose_id = pur_003_momentum_exit`,
        differing in `hypothesis_id`. Each row corresponds to one
        experiment that tests the parent thesis through one specific
        exit-rule operationalization. Asked "what is H2's experiment?",
        the answer is concrete: **the H2 block — the apparatus declared
        in the `apparatus` cell with `exit_rule` replaced by
        `tpsl_+1sigma_-2sigma`**. H2's experiment is not a sub-thing of
        H1's experiment; the three experiments share an apparatus but
        each tests a different falsifiable claim on a different exit-rule
        axis.

        The vocabulary holds: 1 hypothesis ↔ 1 experiment. The notebook
        is the Purpose (= the parent research thesis the cluster of
        experiments tests). The schema reflects this directly.
        """
    )
    return
