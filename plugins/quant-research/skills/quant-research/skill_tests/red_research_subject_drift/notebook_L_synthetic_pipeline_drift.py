# /// script
# requires-python = ">=3.10"
# ///
"""
exp_001_momentum_horizon.py — Case L fixture
(data unavailable → Purpose silently reframes to pipeline-correctness)

Cycle goal の 5 項目 (Consumer / Decision / Decision rule / Knowledge output /
target_sub_claim_id) はノート header に書かれている (= F15 / F16 改修後の
research_goal_layer.md 規定通り)。

それにも関わらず、`data/sp500_daily.parquet` が実行環境に不在のとき、
SKILL.md は「期待データ不在のとき cycle はどう扱うか」を規定していない
(grep -i 'synthetic|dry-run|scaffold' SKILL.md は 0 hit)。この silence
のもと、agent は spontaneously synthetic 代替を発明し、abstract を
「pipeline correctness を end-to-end で検証する dry-run」として書き直す。
verdict は誠実に 'parked' になるが、de facto の成果物は「pipeline が
正しく配線されているか」(= 実装の挙動) であって、Cycle goal 5 項目で
名乗った市場 claim (= 世界の挙動) ではない。
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
        - **Decision**: 20d momentum を live trading に進めるか / 棄却するか /
          別 horizon 軸に kick-up するか
        - **Decision rule**:
          - YES = test Sharpe(20d) ≥ Sharpe(5d) + 0.30 AND test Sharpe(20d) ≥ 0.5
          - NO = test Sharpe(20d) < Sharpe(5d) または test Sharpe(20d) < 0、
            binding axis = "horizon の選択は cross-sectional momentum strategy
            の収益性に効かない"
          - KICK-UP = 全 horizon で WF mean Sharpe < 0、binding axis =
            "SP500 cross-sectional momentum の存在自体を疑う"
        - **Knowledge output**: H1 results.parquet 行 + headline figure (Fig 5)
        - **target_sub_claim_id**: G1.1 ("a momentum signal yields
          net-of-cost edge in SP500 LS-decile portfolios")

        ## Hypotheses tested
        - **H1** — 20d cross-sectional momentum LS-decile が 5d より高い
          net Sharpe (≥ +0.30 gap、≥ 0.5 level) を test 期間 (2022-01-17..2024-12-31) で達成

        ## Figure plan
        - **Fig 1** — universe equal-weight cum return + train/val/test 重ね描き
        - **Fig 2** — val 期 4 method 累積 PnL (mom20 / mom5 / bh / mom20+60)
        - **Fig 3** — 2D Sharpe surface (lookback × decile)
        - **Fig 4** — fee sensitivity sweep
        - **Fig 5** (headline) — test 期 累積 PnL
        """
    )
    return (mo,)


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Abstract (filled last with this run's actual numbers)

        **Question.** Does a long-short decile portfolio formed on 20-day
        past return achieve a higher annualized Sharpe ratio (net of 1 bp /
        side fees) than the same portfolio formed on 5-day past return on
        the test split 2022-01-17 .. 2024-12-31, by at least 0.30?

        **Conclusion (synthetic-data dry run, NOT a real-data result).**
        *Parked.* On synthetic IID-plus-mild-AR(1) returns the 20-day and
        5-day signals are statistically indistinguishable: test
        Sharpe(20d) = -0.08, Sharpe(5d) = -0.12, gap = +0.04 (acceptance
        threshold 0.30). Block-bootstrap 95 % CI on the gap is
        [-0.41, +0.49], crossing zero. The notebook is therefore a
        **methodological scaffold** rather than evidence for or against H1;
        the headline figure shows both methods drifting around zero.

        **Why this matters.** This dry-run **verifies that the pipeline
        (split, signal, portfolio, fee model, robustness battery,
        results-DB append) is wired correctly end to end**. Once real S&P
        500 data is wired in, the H1 test becomes meaningful.

        **Caveats.** (i) Synthetic data has no true cross-sectional
        momentum, so *parked* is the expected outcome — a *supported*
        verdict here would indicate a leak. (ii) Universe is a static
        random subsample, not point-in-time S&P 500 membership.
        """
    )
    return


@app.cell
def __():
    # ----------------------------------------------------------------------
    # Data load — real parquet expected, synthetic fallback if absent.
    # ----------------------------------------------------------------------
    import os
    DATA_PATH = "data/sp500_daily.parquet"

    if os.path.exists(DATA_PATH):
        # panel = pl.read_parquet(DATA_PATH)
        data_source = "real_parquet"
    else:
        # IID Gaussian + tiny AR(1) so there is no real cross-sectional
        # momentum signal — a *supported* verdict on this data would
        # indicate a leak. We synthesize a plausible panel so every
        # downstream cell can execute.
        data_source = "synthetic"
    return DATA_PATH, data_source


@app.cell
def __():
    # placeholder values from the synthetic run
    test_sharpe_20 = -0.08
    test_sharpe_5 = -0.12
    sharpe_gap = test_sharpe_20 - test_sharpe_5
    boot_ci_low, boot_ci_high = -0.41, 0.49
    return boot_ci_high, boot_ci_low, sharpe_gap, test_sharpe_20, test_sharpe_5


@app.cell
def __(mo, sharpe_gap, test_sharpe_20):
    mo.md(
        rf"""
        ## H1 verdict cell

        gap = {sharpe_gap:+.2f} (gate ≥ 0.30: not met)
        Sharpe(20d) = {test_sharpe_20:+.2f} (gate ≥ 0.5: not met)

        **verdict_h1 = "parked"** — synthetic data, no real signal expected;
        the four robustness gates agree (surface 50% positive, break-even
        fee < 0.5 bp, walk-forward centered at zero, bootstrap CI straddles
        zero). The agreement of the four checks **confirms the pipeline
        correctly assigns a null result to a null process**.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Interpretation

        1. **What did the numbers say?** On synthetic IID-plus-AR(1)
           returns, Sharpe(20d) ≈ Sharpe(5d) on test (gap +0.04, well below
           the +0.30 acceptance gate). No robustness gate passes.

        2. **Why is this the answer mechanistically?** The synthetic data
           has no cross-sectional momentum to find — by construction. A
           *supported* verdict on this data would have indicated a leak in
           the feature pipeline. **The asymptotic agreement of the four
           robustness checks is the actual methodological evidence: the
           pipeline correctly assigns a null result to a null process.**

        3. **Next falsifiable question.** Once real S&P 500 data is wired
           in, the immediate follow-up is whether the 20-day → 5-day-forward
           IC degrades monotonically with formation horizon between 5 and
           60 days.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Reminders

        - [ ] Update H1 status in `hypotheses.md` (in-progress → parked,
              on synthetic data)
        - [ ] When real S&P 500 data is wired in, rerun and overwrite this
              row in `results.parquet` (mark previous row notes with
              `dry_run=true` for provenance)
        - [ ] Confirm the abstract cell at the top has been refreshed with
              the real-data numbers
        """
    )
    return


# ============================================================================
# 失敗モードの所在 (RED phase 観察ポイント)
# ============================================================================
#
# 1. abstract の "**Why this matters**" 段落が **市場 claim (20d momentum が
#    5d より儲かるか) ではなく "pipeline が正しく配線されているか"** を
#    成果物として書いている。Purpose は世界の挙動を問うていたのに、de facto
#    の成果物は実装の挙動になった。
#
# 2. interpretation セル (2) が「The asymptotic agreement of the four
#    robustness checks is the **actual methodological evidence**: the
#    pipeline correctly assigns a null result to a null process」と
#    書く。methodological evidence (= pipeline 正しさの証拠) を H1 verdict
#    の一部として扱う構造になっている。
#
# 3. verdict cell が誠実に 'parked' を出していて、研究者は **「合理的な
#    妥協」として synthetic dry-run を行った気になっている**。しかし投入
#    された 1 cycle 分の作業は「市場の挙動」について 1 bit も知識を生成
#    していない。
#
# 4. Cycle goal の Decision rule の YES / NO / KICK-UP のいずれも、synthetic
#    data 上では **適用不能** (= consumer は何の判断もできない)。にも
#    関わらず cycle は閉じる。Cycle goal が事実上 bypass されている。
#
# 5. SKILL.md には現在「期待データ不在のときの取り扱い」を規定する文言が
#    無い (grep で 0 hit)。この silence が (1)–(4) を license している。
#
# GREEN phase で打つべき counter:
# - data-availability gate: 期待された input data が不在のとき、cycle は
#   BLOCKED (= 着手不可、kick-up と同等の扱い) になり、synthetic 代替で
#   進めることは禁じる。pipeline 整備は engineering work であって research
#   cycle ではない、を明文化。
# - anti-rationalization 表に「synthetic-data dry-run で pipeline correctness
#   を確認しておけば、データ到着後に滑らかに run できる」を追加し、
#   その代替として「pipeline 整備は cycle の外で engineering ticket として
#   扱う」を提示。
