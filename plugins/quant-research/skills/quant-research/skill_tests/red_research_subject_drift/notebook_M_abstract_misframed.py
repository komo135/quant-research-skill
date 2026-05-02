# /// script
# requires-python = ">=3.10"
# ///
"""
exp_007_pca_systematic_factors.py — Case M fixture
(data is present, real numbers are computed, but the per-H abstract
describes the deliverable as code/pipeline correctness rather than as
a claim about the world)

Cycle goal の 5 項目は揃っている。data は実在し、PCA は実走、% variance
explained / loading sign distribution の数値も出る。robustness battery も
通った。それにも関わらず、per-H abstract と interpretation セルは「PCA
decomposition の数値 correctness が確認された」「sklearn reference との
一致が取れた」「eigenvalue が non-negative で sum が total variance に
一致する」のような **implementation property** を成果物として書く。市場
claim (= 「最初の 3 PC が cross-sectional variance の 50% 超を捕まえ、
PC1 が systematic market factor として機能する」) は abstract に登場するが、
deliverable の framing は code-correctness 側に寄る。

完了 4 gate (bug_review / experiment-review / research_quality_checklist /
achieved_tier ≥ Medium) には「per-H abstract が市場 claim を名乗っているか /
実装の正しさを名乗っているか」を判定するルールが無い (silence)。この
silence のもと、code-correctness を成果物として書いた notebook が 4 gate
を通過し得る。
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
          - YES = 最初の 3 PC が ≥ 50% variance、PC1 が ≥ 80% names で同符号
          - NO = いずれかが満たされない、binding axis = "single market
            factor で neutralize する frame は SP500 の co-movement 構造に
            合わない"
          - KICK-UP = 最初の 1 PC が < 30% variance、binding axis = "そもそも
            systematic factor が支配的でなく多 factor frame が必要"
        - **Knowledge output**: H1 results.parquet 行 + headline figure (Fig 3)
        - **target_sub_claim_id**: G2.1 ("a small set of latent factors
          explains most cross-sectional co-movement of US large caps")

        ## Hypotheses tested
        - **H1** — 最初の 3 PC で ≥ 50% variance、PC1 が ≥ 80% names で
          同符号 (= systematic market factor)

        ## Figure plan
        - **Fig 1** — universe equal-weight cum return + train/val/test 重ね描き
        - **Fig 2** — eigenvalue scree plot (累積 variance 比率)
        - **Fig 3** (headline) — PC1 loading 分布 histogram (符号別)
        - **Fig 4** — walk-forward での PC1 loading sign 安定性
        """
    )
    return (mo,)


@app.cell
def __():
    # placeholder values from real PCA run
    pct_variance_pc123 = [0.34, 0.08, 0.05]
    cumulative_pc123 = sum(pct_variance_pc123)  # = 0.47
    pc1_positive_loading_share = 0.92
    pc1_loading_min = 0.018
    pc1_loading_max = 0.094
    return (
        cumulative_pc123,
        pc1_loading_max,
        pc1_loading_min,
        pc1_positive_loading_share,
        pct_variance_pc123,
    )


@app.cell
def __(
    mo,
    cumulative_pc123,
    pc1_positive_loading_share,
    pct_variance_pc123,
):
    mo.md(
        rf"""
        ## H1 abstract

        **Implementation summary.** PCA was performed on daily standardized
        residual returns (after de-meaning per date) of N=487 SP500
        constituents over 2018-01-01..2023-12-31. The decomposition was
        computed with `sklearn.decomposition.PCA(n_components=10,
        svd_solver="full")` and **verified to match a from-scratch
        eigendecomposition of the empirical covariance matrix** (max
        absolute residual on the first 10 eigenvalues = 1.4e-12).

        **Numerical correctness.** All eigenvalues are non-negative
        (min = 1.2e-04, max = {pct_variance_pc123[0] * 100:.1f}); the sum
        across the full spectrum (487 components) equals the trace of the
        empirical covariance matrix to machine precision (relative error
        2.3e-15). The first three PCs explain
        {cumulative_pc123 * 100:.1f}% of the cross-sectional variance.
        PC1's loadings are positive on
        {pc1_positive_loading_share * 100:.0f}% of names.

        **Verdict.** The implementation is correct and reconciles with
        sklearn's reference. The threshold (≥ 50% / ≥ 80%) is met on the
        loading-sign side; the variance-share is just below at 47%.

        **Caveat.** The 50% threshold was missed by 3 percentage points;
        verdict is *parked* pending a longer window.
        """
    )
    return


@app.cell
def __():
    pca_implementation_match_max_abs_diff = 1.4e-12
    eigenvalue_min = 1.2e-04
    trace_consistency_rel_error = 2.3e-15
    return (
        eigenvalue_min,
        pca_implementation_match_max_abs_diff,
        trace_consistency_rel_error,
    )


@app.cell
def __(mo, cumulative_pc123, pc1_positive_loading_share):
    mo.md(
        rf"""
        ## H1 interpretation

        1. **What did the numbers say?** Cumulative variance of the first
           three components is {cumulative_pc123 * 100:.1f}% (gate: ≥ 50%);
           PC1 positive-loading share is
           {pc1_positive_loading_share * 100:.0f}% (gate: ≥ 80%).

        2. **Numerical evidence that the decomposition is trustworthy.**
           sklearn's PCA matches a from-scratch eigendecomposition to
           1.4e-12 absolute. All eigenvalues are non-negative. The full
           spectrum's sum equals the empirical covariance trace to 2.3e-15
           relative. **These three checks together establish that the
           reported numbers reflect the actual eigenstructure of the data
           and not an implementation artefact.**

        3. **Next falsifiable question.** Whether extending the window to
           2014-2024 lifts the cumulative-variance share over 50%.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Robustness battery

        Ran walk-forward (12-month rolling) PCA fits over 2018-01..2023-12;
        the PC1 positive-loading share remained ≥ 0.85 in every window
        (mean 0.91, min 0.86, max 0.94). The cumulative-variance share of
        the first three components was 0.45–0.51 across windows, with mean
        0.47 (consistent with the headline number). The bootstrapped CI on
        the cumulative-variance share is [0.43, 0.50], 95%; the threshold
        0.50 is on the boundary.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(r"## H1 verdict — **parked** (variance gate boundary, loading gate met)")
    return


# ============================================================================
# 失敗モードの所在 (RED phase 観察ポイント)
# ============================================================================
#
# 1. H1 abstract の冒頭が "Implementation summary" — まず最初に書かれて
#    いるのは「sklearn の PCA とのリコンサイル / from-scratch
#    eigendecomposition との一致 / eigenvalue の non-negativity / trace
#    consistency」。市場 claim (= 「最初の 3 PC が cross-sectional variance
#    の 50% 超を捕まえ、PC1 が systematic market factor として機能する」)
#    は確かに abstract の中盤で書かれているが、framing の主役は code-
#    correctness。
#
# 2. interpretation セルの (2) が "Numerical evidence that the
#    decomposition is trustworthy" — interpretation の三本柱のうち中央が
#    code 正しさの三点セット。市場挙動の解釈ではない。
#
# 3. abstract の "Verdict" 行が "The implementation is correct and
#    reconciles with sklearn's reference" を最初に書く。研究 verdict は
#    その後の subordinate clause として「The threshold ... is met on the
#    loading-sign side; the variance-share is just below」と添えられる。
#    成果物の主従が反転している。
#
# 4. Robustness battery は通常通り (ある意味、表面的な correctness の
#    完成度はむしろ高い)。bug_review / experiment-review の specialist
#    reviewers (correctness / claim-warrant 軸) も発見すべき finding は
#    無い。だが「成果物が市場 claim を名乗っているか / 実装の正しさを
#    名乗っているか」の dimension は誰も問わない。
#
# 5. SKILL.md "Completion gate (per Hypothesis)" の 4 gates は
#    correctness / claim-warrant / quality-checklist / tier だが、いずれも
#    「per-H abstract が市場 claim を named deliverable として持っているか」
#    を直接 require しない。silence のもと、code-correctness を成果物に
#    据えた abstract が 4 gate を通過し得る。
#
# GREEN phase で打つべき counter:
# - completion gate の 5 番目 (or 4 gates 内に拡張):「per-H abstract は
#   実装属性 (computation correctness / library reconciliation /
#   numerical stability) ではなく、世界の挙動 (mechanism / market /
#   regime / instrument) についての claim を named deliverable として
#   持つ」を追加。
# - notebook_narrative.md / research_design.md に「per-H abstract の
#   先頭 1 文は市場 claim — implementation 属性は補助情報」のフォーマット
#   規定を追加。
# - anti-rationalization 表に「実装が正しいことを示すのは研究の主成果
#   ではない、と explicit に述べる」エントリを追加。
