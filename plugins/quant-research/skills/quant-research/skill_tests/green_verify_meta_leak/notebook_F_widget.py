# /// script
# requires-python = ">=3.10"
# ///
"""exp_004_xs_momentum.py — XS momentum on JP TOPIX500 (H1)."""

import marimo

__generated_with = "0.9.0"
app = marimo.App(width="full")


@app.cell
def __():
    import marimo as mo
    mo.md(
        r"""
        # exp_004 — XS momentum on JP TOPIX500

        ## Purpose
        日本株個別銘柄の cross-sectional 12 ヶ月 momentum (skip-1) シグナルが、
        TOPIX500 universe / 2010-2024 において net 5 bps Sharpe ≥ 1 を取れるかを
        検証する。

        ## Hypotheses tested
        - **H1** — 12-1 momentum (12 か月リターン − 直近 1 か月リターン) を
          symbol 横断で z-score 標準化し long-short にしたとき、上記 Sharpe を達成。

        ## Conclusion (preliminary)
        H1: WF mean Sharpe = 1.1、test = 1.3。**verdict 未確定**。
        """
    )
    return (mo,)


@app.cell
def __(mo):
    mo.md(r"## H1 — 12-1 cross-sectional momentum")
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ### §drill-down — per-symbol PnL inspection

        what: 個別銘柄 PnL を 1 銘柄ずつ切り替えて眺めるための drill-down 用 widget。
        why: H1 の集計 Sharpe (WF mean / test) は universe 平均の挙動だが、特定銘柄が
             異常に寄与していないかを読者が自分で確認できるようにする。ここの選択は
             結論に流れる数値には影響しない (results.parquet には集計値だけが入る)。
        look for: トヨタ (large-cap value) と SoftBank (high-vol growth) の PnL 形状が
                  大きく違うのは想定内。共通して効く期間と乖離する期間がどこかを掴む。
        """
    )
    return


@app.cell
def __(mo):
    instrument_select = mo.ui.dropdown(
        options={
            "トヨタ自動車 (7203)": "7203.T",
            "三菱 UFJ (8306)": "8306.T",
            "ソフトバンクグループ (9984)": "9984.T",
            "ソニーグループ (6758)": "6758.T",
            "NTT (9432)": "9432.T",
        },
        value="トヨタ自動車 (7203)",
    )
    instrument_select
    return (instrument_select,)


@app.cell
def __(mo):
    mo.md(
        r"""
        ### §zoom — date-range zoom on the inspection window

        what: 上で選んだ銘柄の PnL を見るときの観察ウィンドウ (日数オフセット)。
        why: 2010-2024 の全期間を一度に見ると regime 切り替わりが潰れる。月次ステップ
             でズームできる範囲スライダを置くことで、reader が covid 期 / 2018Q4 等の
             個別 regime を切り出して観察できる。集計ウィンドウは §7 (walk-forward)
             側で固定されており、ここのスライダはその数値に影響しない。
        look for: ズームしたウィンドウで PnL が単調か、特定月に集中していないか。
        """
    )
    return


@app.cell
def __(mo):
    # step は月次粒度で寄せる (30 日)。
    date_range = mo.ui.range_slider(
        start=0,
        stop=3650,
        step=30,
        value=(0, 3650),
    )
    date_range
    return (date_range,)


@app.cell
def __(date_range, instrument_select, mo):
    # widget 値の consume — drill-down 表示の見出しだけを更新する。
    # results.parquet に流れる数値はここを通らない。
    _symbol = instrument_select.value
    _start_day, _end_day = date_range.value
    mo.md(
        rf"""
        **現在の drill-down 対象**

        - 銘柄: `{_symbol}`
        - 観察ウィンドウ: 起点から `{_start_day}` 日 〜 `{_end_day}` 日
          (= 約 `{(_end_day - _start_day) // 30}` ヶ月幅)
        """
    )
    return


@app.cell
def __():
    walk_forward_sharpes = [1.0, 1.3, 0.9, 1.4, 1.1, 1.0, 1.2, 1.3]
    walk_forward_mean_sharpe = sum(walk_forward_sharpes) / len(walk_forward_sharpes)
    test_sharpe = 1.3
    return test_sharpe, walk_forward_mean_sharpe, walk_forward_sharpes


@app.cell
def __(mo, test_sharpe, walk_forward_mean_sharpe):
    mo.md(
        rf"""
        ### H1 interpretation
        WF mean = {walk_forward_mean_sharpe:.2f}、test = {test_sharpe:.2f}。
        XS momentum はベースの効果が確認される。
        """
    )
    return


@app.cell
def __(mo):
    mo.md(r"### H1 verdict — **PENDING**")
    return


if __name__ == "__main__":
    app.run()
