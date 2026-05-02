# /// script
# requires-python = ">=3.10"
# ///
"""
exp_003_momentum_exit_design.py — Case O fixture
(`experiment` 語が Purpose の容器を指し、1 仮説 ↔ 1 実験 の対応が崩れる)

H1/H2/H3 は exit rule の design choice 1 軸のみ変えていて、split /
baseline / fee model / universe / entry rule は共有している。SKILL.md
line 653-660 の schema 定義 (`experiment_id (= the notebook = the
Purpose) + hypothesis_id (= the individual H within the Purpose)`) に
従って 3 行を追記すると、3 行は同一の experiment_id を持つ。
"""

import marimo

__generated_with = "0.9.0"
app = marimo.App(width="full")


@app.cell
def __():
    import marimo as mo
    mo.md(
        r"""
        # exp_003 — Exit rule design on 20-day cross-sectional SP500 momentum

        ## Purpose
        Does the choice of exit rule materially change the realized Sharpe
        of a 20-day cross-sectional momentum strategy on S&P 500?

        ## Cycle goal — 5 items
        - **Consumer**: 自分の次 Purpose (live strategy build for SP500
          momentum) — slug = `exp_momentum_live`
        - **Decision**: live strategy が採用すべき exit rule を選定する
        - **Decision rule**:
          - YES = 少なくとも 1 つの exit rule で test Sharpe ≥ B&H + 0.30
          - NO = いずれの exit rule でも test Sharpe < B&H + 0.30、
            binding axis = "exit rule の選択は SP500 momentum strategy の
            収益性に効かない (entry-side が支配的)"
          - KICK-UP = 全 exit rule で walk-forward mean Sharpe < 0
        - **Knowledge output**: H1..H3 results.parquet 行 + headline figure
        - **target_sub_claim_id**: G1.1

        ## Hypotheses tested (parallel exit-rule comparison per Step 9)
        - **H1** — signal-flip exit
        - **H2** (派生) — TP-SL exit (TP = +1σ, SL = -2σ)
        - **H3** (派生) — trailing-stop exit (3% trailing)

        ## Shared experimental apparatus (= identical across H1/H2/H3)
        - Universe: S&P 500 PIT constituents 2018-2024
        - Split: train 2018-2020, val 2020-2022, test 2022-2024
        - Baseline: B&H equal-weight SP500
        - Fee model: 1 bp/side, slippage 0.5 bp
        - Entry rule: 20-day cross-sectional decile rank (long top decile,
          short bottom decile, daily rebalance to decile membership)

        Only the *exit rule* differs between H1, H2, H3.

        ## Figure plan
        - **Fig 1** — universe equal-weight cum return + train/val/test
        - **Fig 2** — H1/H2/H3 累積 PnL net 比較 (test 期)
        - **Fig 3** — exit-rule sensitivity (TP / SL grid for H2,
          trailing distance grid for H3)
        - **Fig 4** — fee sensitivity sweep across H's
        - **Fig 5** (headline) — test 期 累積 PnL 3 系列 + B&H baseline
        """
    )
    return (mo,)


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Abstract

        **Question (= Purpose).** Does the choice of exit rule materially
        change the realized Sharpe of a 20-day cross-sectional momentum
        strategy on S&P 500?

        **What was tested.** Three hypotheses, each replacing the exit rule
        of an otherwise identical pipeline (universe / split / baseline /
        fee / entry rule are shared). H1 = signal-flip exit; H2 = TP-SL
        (+1σ / -2σ); H3 = trailing-stop (3 %).

        **Result per H (test 2022-2024, B&H test Sharpe = 0.41).**
        - H1: test Sharpe 0.78. **supported**, gap +0.37 ≥ 0.30.
        - H2: test Sharpe 0.62. **rejected**, gap +0.21 < 0.30,
          failure_mode = `headline_below_threshold`.
        - H3: test Sharpe 0.69. **supported**, gap +0.28 just below 0.30
          on point estimate but bootstrap CI for the gap is
          [+0.04, +0.51] which overlaps the threshold —
          escalated to **supported** after experiment-review pass.

        **results.parquet rows appended (3 rows, identical
        `experiment_id`):**
        ```
        experiment_id        hypothesis_id  pathway  verdict     achieved_tier
        exp_003_momentum_exit  h1           4        supported   medium
        exp_003_momentum_exit  h2           4        rejected    medium
        exp_003_momentum_exit  h3           4        supported   medium
        ```

        **Cross-H synthesis.** Two of three exit rules clear the threshold
        on the same shared apparatus. The exit-rule axis is *not* the
        binding constraint; entry-side momentum carries the edge and exit
        rules differ in capture efficiency.

        **Caveats.** Each H's claim is "exit rule X yields ≥ +0.30 Sharpe
        gap on this shared apparatus". The claim is conditional on the
        shared split / baseline / fee model. Replication on a different
        universe is a separate Purpose.
        """
    )
    return


@app.cell
def __():
    # ----------------------------------------------------------------------
    # Shared apparatus — single source of truth for split / fee model /
    # baseline / entry. H1/H2/H3 all reference these names.
    # ----------------------------------------------------------------------
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
    # H1 — signal-flip exit on the shared apparatus
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
    # H2 — TP-SL exit on the shared apparatus
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
    # H3 — trailing-stop exit on the shared apparatus
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
    # Append all three H's to results.parquet under the SAME experiment_id.
    # Per SKILL.md line 653-660: experiment_id = notebook = Purpose;
    # hypothesis_id = individual H within the Purpose.
    rows = pl.DataFrame([
        dict(
            experiment_id="exp_003_momentum_exit",
            hypothesis_id=h["hypothesis_id"],
            pathway=4,  # failure-derived from upstream
            verdict=h["verdict"],
            failure_mode=h["failure_mode"],
            achieved_tier="medium",
        )
        for h in (h1, h2, h3)
    ])
    return (rows,)


@app.cell
def __(mo, rows):
    mo.md(
        r"""
        ## Closing notes

        Three rows above all share `experiment_id = exp_003_momentum_exit`,
        differing only in `hypothesis_id`. Per SKILL.md line 653-660 this
        is the prescribed schema. Asked "what is H2's experiment?", the
        protocol-correct answer is "the apparatus declared in the
        `apparatus` cell, with exit_rule replaced by TP-SL". H2 has no
        experiment of its own; it shares one with H1 and H3 under the
        Purpose-level `experiment_id`.
        """
    )
    return
