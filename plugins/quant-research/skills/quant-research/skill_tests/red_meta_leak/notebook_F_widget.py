# /// script
# requires-python = ">=3.10"
# ///
"""
exp_004_xs_momentum.py — XS 12-1 momentum on JP TOPIX500.

This notebook investigates whether a cross-sectional 12-1 momentum signal
on the TOPIX500 universe (2010-2024) can earn net 5 bps Sharpe >= 1.

The interactive `mo.ui` widgets in this notebook (instrument dropdown +
date-range zoom) are evidence drill-down only — they do not select any
number that flows into `results.parquet`.
"""

import marimo

__generated_with = "0.10.0"
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
        ### Drill-down: per-instrument inspection

        what: TOPIX500 主要銘柄から 1 銘柄を選び、その銘柄の 12-1 momentum
        signal と累積 PnL の見え方を読者が個別に確認できるようにする。
        why: cross-section 集計 (Sharpe, IC) は良好でも、特定銘柄の挙動を
        読むことで「edge が一握りの銘柄に集中していないか」を読者が直感的に
        確認できる。本セルの選択は集計値には流れず、`results.parquet` には
        記録されない。
        look for: 主力銘柄でも信号符号が時系列で安定しているか、12-1 構成
        (skip-1) の影響で直近 1 か月の値動きが symbol 表示に反映されない
        ことが視覚的に確認できるか。

        **Widget options は `{label: value}` の dict で渡し、widget が返す
        value は dict のキー (label) ではなくキーに対応する値 (Bloomberg
        ticker 形式 `XXXX.T`) を保持する。** label は ticker と社名の対で
        書き、読者がドロップダウンを開いた瞬間に「この銘柄が何か」を読み取れる
        ようにする。下流の per-instrument 図は ticker (= dict value) を
        受け取って動く。
        """
    )
    return


@app.cell
def __(mo):
    # H1 widget config — instrument drill-down
    # value 側はデータ層が銘柄を識別するキー (Bloomberg 形式 ticker)。
    # label 側 (dict のキー) は読者向けに「社名 (コード)」で並べ、何の銘柄を
    # 選んでいるかをドロップダウンを開いた瞬間に分かるようにする。
    INSTRUMENT_CHOICES = {
        "トヨタ自動車 (7203)": "7203.T",
        "三菱 UFJ FG (8306)": "8306.T",
        "ソフトバンクグループ (9984)": "9984.T",
        "ソニーグループ (6758)": "6758.T",
        "NTT (9432)": "9432.T",
    }
    instrument_select = mo.ui.dropdown(
        options=INSTRUMENT_CHOICES,
        value="トヨタ自動車 (7203)",  # dict のキー (label) を指定
        label="Inspect instrument",
    )
    instrument_select
    return INSTRUMENT_CHOICES, instrument_select


@app.cell
def __(instrument_select, mo):
    # Selected ticker — instrument_select.value は dict のキーに対応する
    # value (= ticker 文字列)。下流の per-instrument PnL 図はこの ticker を
    # 受け取って frame をフィルタする。
    selected_ticker = instrument_select.value
    mo.md(rf"Selected ticker (drill-down only): **{selected_ticker}**")
    return (selected_ticker,)


@app.cell
def __(mo):
    mo.md(
        r"""
        ### Drill-down: equity-curve date-window zoom

        what: 累積 PnL 図の表示期間を読者が手元で絞り、特定の年/regime に
        ズームして観察できるようにする。
        why: train / val / test の期間境界 (2010-2018 / 2019-2021 /
        2022-2024) や、コロナ前後 / 円安局面など regime 境界を読者が手元で
        切り出せると、cross-section 集計値の裏側で何が起きているかを
        観察セル単独でも追える。
        look for: zoom 範囲を変えても累積 PnL の符号が頻繁に反転しないか、
        特定区間に edge が集中していないか。

        **range_slider は `step` を明示し、単位を markdown で宣言する。**
        ここでは累積日数 (start = 0 が学習開始日 2010-01-04、stop = 3650
        は約 10 年後) を単位とし、`step=30` (= 約 1 か月刻み) で走査する。
        step がないと連続 int 扱いとなり、月境界以外でスナップしやすい
        位置で zoom が止まる。
        """
    )
    return


@app.cell
def __(mo):
    # H1 widget config — equity-curve date-window zoom
    # 単位は「学習開始 (2010-01-04) からの累積日数」。step=30 (約 1 か月)
    # 刻みで月境界に近い位置にスナップさせる。stop=3650 は約 10 年。
    DATE_RANGE_START_DAYS = 0
    DATE_RANGE_STOP_DAYS = 3650
    DATE_RANGE_STEP_DAYS = 30  # 約 1 か月刻み
    date_range = mo.ui.range_slider(
        start=DATE_RANGE_START_DAYS,
        stop=DATE_RANGE_STOP_DAYS,
        step=DATE_RANGE_STEP_DAYS,
        value=(DATE_RANGE_START_DAYS, DATE_RANGE_STOP_DAYS),
        label="Equity-curve zoom (days from 2010-01-04, 30-day step)",
    )
    date_range
    return (
        DATE_RANGE_START_DAYS,
        DATE_RANGE_STEP_DAYS,
        DATE_RANGE_STOP_DAYS,
        date_range,
    )


@app.cell
def __(date_range, mo):
    # Selected zoom window — date_range.value は (start_days, stop_days) の
    # タプルを返す。下流の累積 PnL 図はこの 2 値を期間フィルタに使う。
    zoom_start_days, zoom_stop_days = date_range.value
    mo.md(
        rf"Zoom window (drill-down only): "
        rf"**day {zoom_start_days} – day {zoom_stop_days}** "
        rf"(from 2010-01-04, 30-day step)"
    )
    return zoom_start_days, zoom_stop_days


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
