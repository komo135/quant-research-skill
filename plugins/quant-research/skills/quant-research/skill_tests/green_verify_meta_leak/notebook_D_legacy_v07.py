# /// script
# requires-python = ">=3.10"
# ///
"""
exp_002_btc_funding_carry.py  —  Case D fixture (skill upgrade migration)

このノートは quant-research skill v0.7.0 当時に書かれたものという想定。
Purpose ヘッダーには Consumer / Decision / Decision rule / Knowledge output
の 4 項目が含まれていない (v0.8.0 で必須化された)。

v0.8.0 にプロジェクトを upgrade する研究者は、これら 4 項目を後付けする。
"""

import marimo

__generated_with = "0.9.0"
app = marimo.App(width="full")


@app.cell
def __():
    import marimo as mo
    mo.md(
        r"""
        # exp_002 — BTC perpetual funding rate carry

        ## Purpose
        BTC perpetual の funding rate を carry シグナルとして用いると、
        spot - perp ベイシスの方向と一致する形で日次リターンを取れるかを検証する。

        ### Consumer
        本ノート終了後に自分が開く次の Purpose
        (= "lower-frequency variant of the funding-rate carry signal" を
        新ノートで検証するか、それとも funding-rate を alpha source として
        放棄するか) の判断者は研究者自身。

        ### Decision the consumer is blocked on
        BTC perpetual の funding-rate carry を、(a) 現行の 8h 平滑化のまま
        production 構築に進めるか、(b) lower-frequency variant に派生 Purpose
        を切るか、(c) このユニバースで funding-rate を alpha source として
        放棄するか、を決められない。

        ### Decision rule (committed before any H is run)
        - **YES (進む)**: H1 が test PSR ≥ 0.95 を fee 5 bps/side 込みで
          満たし、walk-forward positive-rate ≥ 60 % かつ fee_model / regime_mismatch
          を binding axis とする失敗が出ない。→ production 構築 Purpose を新規開設。
        - **NO (進まない、binding axis を残す)**: bootstrap 95 % CI の Sharpe
          下限が 0 を含む、または break-even fee が 5 bps/side 未満で fee_model
          が binding。→ lower-frequency variant の派生 Purpose を新ノートで開設。
        - **KICK-UP (frame 不適合)**: funding-rate の取引所側定義変更や
          履歴データ汚染が解消不能な形で見つかる、もしくは consumer の判断に
          必要な capacity test がこのノートのデータでは構造的に作れないことが
          明らかになる。→ 上流データパイプライン Purpose を先に解く。

        ### Knowledge output
        H1 (および派生 H が走った場合は H2, H3) の results.parquet 行
        (verdict / failure_mode / achieved_tier 付き)、Purpose-level synthesis
        段落 (binding axis を含む)、headline 図 (cumulative PnL gross / net 5 bps、
        train/val/test 縦線、B&H と funding-naive の上下ベースライン重ね)。
        この 3 点で consumer は YES / NO / KICK-UP を当てはめられる。

        ## Hypotheses tested
        - **H1** — funding rate 8h ローリング平均の符号と同方向の perp pos を取る
          単純ストラテジが、年率 Sharpe 1.0 以上 (5 bps fee 込み) を達成する。

        ## Conclusion (filled after all H rounds — preliminary)
        H1 は train/val で WF mean Sharpe = 1.4、test で 0.9。コスト 5 bps
        では薄利。**verdict 未確定**。
        consumer の decision rule に当てはめると、現状は YES の PSR 閾値
        を満たすかどうかが確定しておらず、NO の bootstrap 下限条件にも
        まだ到達していない。次の round で robustness battery を回すまで
        cycle は閉じない。

        ## Why this matters
        funding を別 alpha に頼らず carry として直接使えるなら、ベイシス
        マーケットメーキングの sub-alpha として組み込める。

        ## Figure plan (decided up-front)
        - **Fig 1** — Universe: BTC-USDT perp + spot, train/val/test split
        - **Fig 2** — H1 累積 PnL (gross / net 5bps), 3 splits 縦線
        - **Fig 3** — funding rate と forward 8h returns の散布図
        - **Fig 4** — Walk-forward window 別 Sharpe 分布 (N=8)
        - **Fig 5** — Bootstrap Sharpe 分布
        """
    )
    return (mo,)


@app.cell
def __(mo):
    mo.md(r"## H1 — funding-sign carry")
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ### Sub-claim of the decision rule that this H tests
        H1 は decision rule の YES 分岐の `test PSR ≥ 0.95 net of 5 bps`
        と `walk-forward positive-rate ≥ 60 %` の 2 conjunct を同時に
        評価する。同じ実験から、NO 分岐の `bootstrap CI 下限が 0 を含む`
        条件と `break-even fee < 5 bps/side` (= binding axis = fee_model)
        の identification も得る。すなわち、YES が出ない場合に
        consumer が NO を当てはめるための binding axis 情報も
        この H1 ひとつから読めるよう設計する。

        ### H1 abstract
        funding rate 8h ローリング平均 (window=3 = 24h) の符号方向に perp pos を取る。
        train/val WF mean Sharpe = 1.4、test = 0.9。コスト 5 bps で薄利。
        """
    )
    return


@app.cell
def __():
    FUNDING_WINDOW_8H = 3       # 24h 平滑のための 8h × 3 = 1 day
    POS_CLIP = 1.0
    FEE_BPS = 5
    SPLIT = {"train": "2019-09-01..2022-12-31",
             "val":   "2023-01-01..2023-12-31",
             "test":  "2024-01-01..2024-12-31"}
    return FEE_BPS, FUNDING_WINDOW_8H, POS_CLIP, SPLIT


@app.cell
def __(mo):
    mo.md(r"### §3 — Walk-forward Sharpe")
    return


@app.cell
def __():
    walk_forward_sharpes = [1.6, 1.2, 1.5, 0.9, 1.7, 1.3, 1.4, 1.6]
    walk_forward_mean_sharpe = sum(walk_forward_sharpes) / len(walk_forward_sharpes)
    test_sharpe = 0.9
    return test_sharpe, walk_forward_mean_sharpe, walk_forward_sharpes


@app.cell
def __(mo, test_sharpe, walk_forward_mean_sharpe):
    mo.md(
        rf"""
        ### H1 interpretation
        WF mean Sharpe = {walk_forward_mean_sharpe:.2f}、test Sharpe = {test_sharpe:.2f}。
        funding-sign のみで carry が拾えるかは regime 依存性が強い可能性。
        decision rule に当てはめると、YES の PSR 条件は bootstrap CI 下限を
        確認するまで判定保留、NO の bootstrap 下限条件もまだ確定していない。
        cycle はここでは閉じず、bootstrap CI と break-even fee を計算した
        上で consumer が YES / NO のどちらを当てはめられるかを再評価する。
        """
    )
    return


@app.cell
def __(mo):
    mo.md(r"### H1 verdict — **PENDING**")
    return


if __name__ == "__main__":
    app.run()
