# /// script
# requires-python = ">=3.10"
# ///
"""
exp_002_btc_funding_carry.py  —  Case D fixture (skill upgrade migration)

このノートは quant-research skill v0.7.0 当時に書かれたものを v0.8.0 規約に
あわせて in-place で upgrade したもの。

v0.8.0 で導入され、本ノートに反映した変更点 (元の v0.7.0 当時のノートには
存在しなかった):

  1. Purpose ヘッダー直下に Cycle goal の 4 項目を追加
     (Consumer / Decision / Decision rule (YES/NO/KICK-UP) /
      Knowledge output)
     根拠: references/cycle_purpose_and_goal.md
  2. H1 ブロックに「Sub-claim of the decision rule that this H tests」を追加
     根拠: references/research_design.md
  3. cycle 終了条件の記述を primary stops (Primary YES / Fallback NO /
     KICK-UP) と emergency stops (N=5 advisory / N=8 hard cap) に
     概念的に分離
     根拠: references/hypothesis_cycles.md

いずれも v0.8.0 で必須化された項目。値は本ノート想定の内部 consumer に
合わせて補完しており、過去のノート利用者が "この migration 時点では
何が新規追加で何が既存記述か" を本 docstring から追えるように残してある。
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

        ## Cycle goal — 4 items (added in v0.8.0 upgrade)
        以下 4 項目は v0.7.0 ノートには無く、v0.8.0 規約 (`cycle_purpose_and_goal.md`)
        にあわせて後付けで追加した。値は本ノートが想定していた内部 consumer に
        合わせて再構成してある。

        ### Consumer
        本ノートを開いた研究者自身の "次の Purpose" — すなわち
        `exp_003 — funding rate を multi-day horizon / 別 sizing で carry に
        使えるか` を開くか、あるいは funding-rate を alpha source として
        当面 park するかの判断主体。
        ("My own next Purpose, named as <slug>" 形の legal escape hatch を
        利用、`cycle_purpose_and_goal.md` 参照。)

        ### Decision the consumer is blocked on
        BTC perp の funding-sign carry を、production sub-alpha 候補として
        さらに研究投資を続けるかどうか — 続けるとしたらどの軸 (horizon /
        sizing / regime / cost) で次 Purpose を切るか。

        ### Decision rule (committed BEFORE the cycle runs)
        - **YES** (次 Purpose を horizon / sizing 軸で開く):
          test PSR ≥ 0.95 net of 5 bp/side AND walk-forward positive-rate
          ≥ 60% AND 3 splits 全てで Sharpe > 0 AND cross-H synthesis で
          Pattern A binding axis なし。
        - **NO with binding axis = `fee_model`**:
          ≥1 H が `fee_model` を共通 failure_mode として reject AND
          break-even fee < 5 bp/side。→ 次 Purpose は低頻度版へ pivot
          するか lineage を close。
        - **NO with binding axis = `regime_mismatch`**:
          Pattern E 相当 (signal が low-vol regime のみで成立) → narrowed
          scope の derived Purpose を提案するか close。
        - **KICK-UP**: bug_review が funding-rate 履歴の不可逆な
          pre-2020 contamination を surface したとき、もしくは
          experiment-review の `scope` 次元が "consumer's decision は本
          Purpose では到達不能な capacity test を要求" と判定したとき。
          → 上流データパイプラインの Purpose を先に開く。

        ### Knowledge output
        H1 (および必要なら H2/H3) の per-H 行 (`results.parquet`) +
        Purpose-level synthesis paragraph (Pattern A-E のいずれかを命名) +
        headline cumulative-PnL 図 (B&H + price-momentum upper baseline
        を併記、3 splits 縦線、walk-forward Sharpe inset)。
        この 3 点が揃うと上記の YES / NO / KICK-UP 述語が consumer から
        applicable になる。

        ## Hypotheses tested
        - **H1** — funding rate 8h ローリング平均の符号と同方向の perp pos を取る
          単純ストラテジが、年率 Sharpe 1.0 以上 (5 bps fee 込み) を達成する。

        ## Conclusion (filled after all H rounds — preliminary)
        H1 は train/val で WF mean Sharpe = 1.4、test で 0.9。コスト 5 bps
        では薄利。**verdict 未確定** (primary stops のいずれもまだ landing
        していない; emergency stop の N=5 advisory にも届いていない)。

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
        (項目自体は v0.8.0 upgrade で追加。`research_design.md` 準拠。)

        H1 は decision rule の以下の conjunct に対する evidence を生成する:

        - **YES branch** の `test PSR ≥ 0.95 net of 5 bp/side` および
          `walk-forward positive-rate ≥ 60%` 条件 — funding-sign carry
          そのものの "存在 + コスト後生存" を測る。
        - 同時に **NO branch** の `binding axis = fee_model` 識別 —
          break-even fee を出力するため、コスト感度由来の reject であれば
          失敗軸を直接命名できる。
        - **KICK-UP precondition** (funding-rate 履歴の構造的 contamination)
          は H1 の bug_review 出力経由でのみ発火し、H1 自体の design では
          直接テストしない。

        したがって H1 は YES / NO 両 branch にまたがる中核 H であり、
        portfolio に占める位置は "broad-scope の core test"。後続の derived
        H は必要に応じ horizon / sizing / regime 軸を narrow scope で詰める。
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
    mo.md(
        r"""
        ### H1 abstract
        funding rate 8h ローリング平均 (window=3 = 24h) の符号方向に perp pos を取る。
        train/val WF mean Sharpe = 1.4、test = 0.9。コスト 5 bps で薄利。
        """
    )
    return


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
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ### H1 verdict — **PENDING**

        ### Cycle stop status (v0.8.0 規約: primary vs emergency stops の分離)
        本欄は v0.8.0 upgrade で追記。`hypothesis_cycles.md` の
        "Why the cycle exists — and what stops it" セクション参照。

        - **Primary stops** (cycle がその役割を終えた intended closure):
          - *Primary YES* — まだ landing していない (test Sharpe = 0.9
            は YES branch の PSR/positive-rate 閾値を満たすか未確認、
            bug_review / robustness battery / experiment-review 4 ゲートが
            いずれも未通過)。
          - *Fallback NO with binding axis* — 未 landing (single H で
            Pattern A 由来の binding axis は不確定; break-even fee 評価が
            未実施で `fee_model` を NO の binding として呼べない)。
          - *KICK-UP* — 未発火 (bug_review が unresolvable な funding-rate
            データ汚染を surface していない; experiment-review の `scope`
            次元も未起動)。
        - **Emergency stops** (primary が立たないまま H が累積したときの
          打ち止め):
          - *N=5 advisory* — 現在 N=1。advisory 距離あり。
          - *N=8 hard cap* — 同様に未到達。
          いずれも cycle 終了の "intended" 経路ではなく、frame mismatch を
          疑わせる failsafe である点に注意。本 H1 で primary stop が
          landing しなければ、derived H (horizon / regime narrowing / fee
          sensitivity) を同 notebook に追加し、primary stop に向けて運用
          する。
        """
    )
    return


if __name__ == "__main__":
    app.run()
