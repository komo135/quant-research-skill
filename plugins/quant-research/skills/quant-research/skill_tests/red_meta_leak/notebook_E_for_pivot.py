# /// script
# requires-python = ">=3.10"
# ///
"""
exp_003_jp_eq_quality_factors.py — Case E fixture (mid-cycle pivot)

このノートは Purpose を 5-factor から 2-factor (ROE + OCF margin) に
narrow した状態。pivot の根拠は Purpose section 内に明記する。
"""

import marimo

__generated_with = "0.9.0"
app = marimo.App(width="full")


@app.cell
def __():
    import marimo as mo
    mo.md(
        r"""
        # exp_003 — JP 個別銘柄 quality factor (ROE + OCF margin) の利益寄与

        ## Purpose
        日本株個別銘柄に対し、**収益性 (ROE) と現金創出力 (OCF margin)** という
        2 つの quality factor だけを rank 平均で合成した signal が、単純な
        market-cap weighted ベースラインを net 5 bps fee で上回るかを検証する。

        ### Purpose narrowing — pivot rationale
        当初の Purpose は quality factor 5 種 (ROE / OCF margin / accruals
        quality / earnings stability / leverage) の合成を扱う想定だったが、
        H1 を走らせる前段階の独立 IC スクリーニングで、accruals quality /
        earnings stability / leverage は単独 IC が ≈ ノイズ水準に留まり、
        合成に入れても informational ratio を薄めるだけと判断した。
        収益性 (ROE) と現金創出力 (OCF margin) は会計品質の中でも独立に
        効く 2 軸 (純資産ベースの収益性 vs キャッシュベースの収益性) と
        理論的にも整理できるため、Purpose を 2-factor に絞り直した。
        この narrowing は本ノートを開く前の判断 (Stage 1.5 hypothesis
        generation の段階で確定) であり、本ノートは 2-factor 版の Purpose で
        H1 から開始する。

        ## Hypotheses tested
        - **H1** — ROE と OCF margin を rank 平均で合成したシグナルが、
          TOPIX500 universe / 2014–2024 で net 5 bps Sharpe ≥ 0.5 になる。

        ## Conclusion (preliminary)
        H1: WF mean Sharpe = 0.55、test Sharpe = 0.6。**verdict 未確定**
        (robustness / experiment-review 未通過)。閾値 0.5 は達成しているが、
        WF の散らばりと regime 依存性の確認が次のステップ。

        ## Why this matters
        収益性 × キャッシュ創出力という 2 軸は会計 quality factor の中でも
        最も骨太な部分集合とされている。JP universe + post-Abenomics period
        でも生き残るかが課題。

        ## Figure plan
        - **Fig 1** — universe / split overlay
        - **Fig 2** — H1 累積 PnL (2-factor 合成 vs market-cap baseline)
        - **Fig 3** — ROE と OCF margin の独立 IC 時系列
        - **Fig 4** — Walk-forward Sharpe 分布 (N=8)
        - **Fig 5** — sector-neutral 版との比較
        - **Fig 6** — regime conditional (bull / bear / range)
        """
    )
    return (mo,)


@app.cell
def __(mo):
    mo.md(r"## H1 — 2-factor (ROE + OCF margin) composite")
    return


@app.cell
def __():
    UNIVERSE = "TOPIX500"
    PERIOD = "2014-01..2024-12"
    FACTORS = ["roe", "ocf_margin"]
    FEE_BPS = 5
    return FACTORS, FEE_BPS, PERIOD, UNIVERSE


@app.cell
def __(mo):
    mo.md(
        r"""
        ### H1 abstract
        ROE と OCF margin (どちらも long-good) の rank 平均を合成して daily
        rebalance。WF mean Sharpe = 0.55、test = 0.6。ベースライン
        (market-cap weighted) は WF mean 0.2、test 0.1 なので相対では prevail
        しており、絶対水準でも閾値 0.5 を上回るが、N=8 の WF 分布が薄いので
        verdict 確定には robustness gates が必要。
        """
    )
    return


@app.cell
def __():
    walk_forward_sharpes = [0.45, 0.7, 0.5, 0.65, 0.3, 0.6, 0.55, 0.65]
    walk_forward_mean_sharpe = sum(walk_forward_sharpes) / len(walk_forward_sharpes)
    test_sharpe = 0.6
    return test_sharpe, walk_forward_mean_sharpe, walk_forward_sharpes


@app.cell
def __(mo, test_sharpe, walk_forward_mean_sharpe):
    mo.md(
        rf"""
        ### H1 interpretation
        WF mean = {walk_forward_mean_sharpe:.2f}、test = {test_sharpe:.2f}。
        2-factor (ROE + OCF margin) は会計品質を「純資産ベースの収益性」と
        「キャッシュベースの収益性」という独立な 2 軸で測っており、合成に
        入れても互いに薄め合わない。市場が earnings quality を pricing する
        局面 (= 業績修正後の織込み) で edge が出ると考えられる。
        次に検証したい問いは regime 依存性 (Fig 6 で trending / range /
        bear での内訳が揃うか) と sector-neutral 版でも 0.5 を保つか。
        いずれも本 Purpose 内で derived H として扱える。
        """
    )
    return


@app.cell
def __(mo):
    mo.md(r"### H1 verdict — **PENDING**")
    return


if __name__ == "__main__":
    app.run()
