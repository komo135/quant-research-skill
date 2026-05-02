# /// script
# requires-python = ">=3.10"
# ///
"""
exp_007_pca_systematic_factors.py — Case M GREEN
(per-H abstract leads with the market claim, not the implementation)

`notebook_narrative.md` 1b "Format rule — first sentence is the market
claim, not the implementation" を踏んだ post-fix notebook。per-H abstract
の lead が「最初の 3 PC が cross-sectional variance のどれだけを捕まえ、
PC1 が systematic market factor として機能したか」(= 市場 claim) で開き、
implementation 属性 (sklearn 一致 / eigenvalue 非負 / trace consistency) は
末尾の Reproducibility note にバウンドされている。verdict / interpretation
も市場 claim 軸で書かれる。

robustness battery と sanity-checks セルは別途存在するが、abstract 側で再録
しない (それぞれの cell が audit trail を担う)。
"""

import marimo

__generated_with = "0.9.0"
app = marimo.App(width="full")


@app.cell
def __():
    import marimo as mo
    mo.md(
        r"""
        # exp_007 — PCA on US large-cap daily returns 2018–2024

        ## Purpose
        US large-cap (S&P 500) cross-sectional daily returns における latent
        factor 構造を特徴づける。

        ## Cycle goal — 5 items
        - **Consumer**: 自分の次 Purpose (factor neutralization の研究) —
          slug = `exp_factor_neutralization`
        - **Decision**: cross-sectional return を market factor で
          neutralize する設計に進めるか / kick-up するか
        - **Decision rule**:
          - YES = 最初の 3 PC が ≥ 50 % variance、PC1 が ≥ 80 % names で同符号
          - NO = いずれかが満たされない
          - KICK-UP = 最初の 1 PC が < 30 % variance
        - **Knowledge output**: H1 results.parquet 行 + headline figure
        - **target_sub_claim_id**: G2.1 ("a small set of latent factors
          explains most cross-sectional co-movement of US large caps")
        """
    )
    return (mo,)


@app.cell
def __():
    # placeholder values from real PCA run
    pct_variance_pc123 = [0.34, 0.08, 0.05]
    cumulative_pc123 = sum(pct_variance_pc123)  # = 0.47
    pc1_positive_loading_share = 0.92
    return cumulative_pc123, pc1_positive_loading_share, pct_variance_pc123


@app.cell
def __(mo, cumulative_pc123, pc1_positive_loading_share):
    mo.md(
        rf"""
        ## H1 abstract

        **The first three PCs of SP500 daily residual returns 2018–2024
        captured {cumulative_pc123 * 100:.1f} % of cross-sectional
        variance, and PC1 loaded with the same sign on
        {pc1_positive_loading_share * 100:.0f} % of names** — consistent
        with PC1 acting as a single dominant systematic factor, but the
        50 % variance gate is missed by 3 percentage points. Verdict =
        *parked*: the loading-sign gate (≥ 80 %) is met, the variance
        gate (≥ 50 %) is on the boundary at 47 %; a longer window
        (2014–2024) is the next falsifiable variant.

        Mechanistically the gap to 50 % sits in PC2 / PC3 contributing
        less than the 16 % their slot would need to land the
        cumulative gate; this is consistent with the SP500
        cross-section being **market-factor-dominated but not
        market-factor-only** in the 2018–2023 sample. For the
        downstream Consumer (factor-neutralization design), this
        reads as: a single-factor neutralization captures most of the
        co-movement but leaves residual structure that a
        multi-factor neutralization would absorb.

        *Reproducibility note.* sklearn `PCA(n_components=10,
        svd_solver="full")` reconciles to a from-scratch
        eigendecomposition to 1.4e-12 absolute. All eigenvalues are
        non-negative and the full spectrum sums to the empirical
        covariance trace within 2.3e-15 relative. Data hash and env
        lock are recorded in `reproducibility/`.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## H1 interpretation

        1. **What did the numbers say?** Cumulative variance of the first
           three components is 47 % (gate: ≥ 50 %); PC1 positive-loading
           share is 92 % (gate: ≥ 80 %). The variance gate is on the
           boundary; the loading-sign gate is comfortably cleared.

        2. **Why is this the answer mechanistically?** The 92 % positive
           loading on PC1 says the SP500 cross-section moves with a
           single dominant systematic factor most of the time — what
           the literature calls the "market mode". The 47 % cumulative
           variance says PC2 and PC3 together add 13 percentage points
           more, short of the 16 percentage points needed to clear
           the 50 % gate. Mechanistically: SP500 has a strong market
           mode plus a small set of secondary factors (likely sector
           rotation, value/growth tilt) whose contributions in the
           2018–2023 sample sat below the threshold the cycle's
           Decision rule asked for.

        3. **Next falsifiable question.** Whether extending the window
           to 2014–2024 lifts the cumulative-variance share over 50 %.
           If 2014–2017 carried more sector dispersion (pre-COVID
           regime), the longer window may push the cumulative variance
           above 50 % and clear the YES gate. If the longer window
           confirms ~47 %, the Decision rule's threshold may have been
           too aggressive for SP500 and the binding axis is "single
           market factor frame is too tight for SP500 — multi-factor
           required" (Pattern A closure shape on the cycle).
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Robustness battery (per `references/robustness_battery.md`)

        Walk-forward (12-month rolling) PCA fits over 2018-01..2023-12;
        the PC1 positive-loading share remained ≥ 0.85 in every window
        (mean 0.91, min 0.86, max 0.94). The cumulative-variance share
        of the first three components was 0.45–0.51 across windows,
        with mean 0.47 (consistent with the headline number).
        Block-bootstrap 95 % CI on the cumulative-variance share is
        [0.43, 0.50]; the 50 % threshold is on the upper edge of the CI.

        *Observation.* The variance-share is structurally near 0.47 with
        modest dispersion across windows; the loading-sign share is
        consistently above 0.85. The walk-forward distribution
        corroborates the parked verdict — a longer window is the right
        next move, parameter sensitivity around PCA's
        `n_components=10` choice would not lift the cumulative variance
        over 50 %.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(r"## H1 verdict — **parked** (variance gate boundary, loading gate met)")
    return


# ============================================================================
# 失敗モード counter (GREEN phase 観察ポイント)
# ============================================================================
#
# 1. H1 abstract の **第 1 文** は市場 claim:
#       "The first three PCs of SP500 daily residual returns 2018–2024
#       captured 47.0 % of cross-sectional variance, and PC1 loaded
#       with the same sign on 92 % of names"
#    ノートを scroll する読者が H1 から最初に受け取るのは「世界 (SP500
#    cross-section) の挙動」であって「sklearn が正しく動いた」ではない。
#
# 2. interpretation セルの (2) は市場 mechanism (single market mode +
#    secondary factors の 2018–2023 サンプルでの寄与不足) — implementation
#    correctness の三点セットは登場しない。
#
# 3. abstract Verdict 行の主節は研究 verdict ("parked: the loading-sign
#    gate is met, the variance gate is on the boundary at 47 % vs 50 %")。
#    implementation correctness は subordinate な Reproducibility note に
#    bound されている。主従が正しい。
#
# 4. Reproducibility note (= sklearn 一致 / eigenvalue 非負 / trace
#    consistency) は abstract の **末尾 1 段落** に bound され、abstract の
#    framing を支配しない。
#
# 5. completion gate に新しい 5 番目を作る代わりに、`notebook_narrative.md`
#    1b "Format rule" + Quick checklist の対応 checkbox + experiment.py.template
#    の per-H abstract section が format-rule を agent の generation 時 と
#    template-fill 時に bite させる。verification 側は experiment-review
#    skill の `narrative` dimension がこの format rule を読むことで担保される
#    (= 既存の machinery に rule を追加する 2 層 fix、新 gate machinery 不要)。
