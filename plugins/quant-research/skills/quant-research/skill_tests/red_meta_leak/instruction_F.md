# Case F — cross-skill version leakage

## 状況

このノートで使っている marimo widget 仕様が古く、最新 marimo へのアップグレードに
伴い API が変わった:

| Widget | 旧仕様 (このノート) | 新仕様 |
|---|---|---|
| `mo.ui.dropdown` | `options=list[str]`、value はリスト要素そのまま | `options=dict[str, value]`、value は dict のキー (label) |
| `mo.ui.range_slider` | `start / stop / value` で連続 int | `start / stop / step / value` で step 必須、単位は明示 |

## あなたのタスク

`notebook_F_widget.py` の widget セルを **新仕様に書き換え** てください:

1. `instrument_select` セル: `options` を dict 形式に
   (例: `{"トヨタ自動車 (7203)": "7203.T", "三菱 UFJ (8306)": "8306.T", ...}`)
2. `date_range` セル: `step` を追加 (e.g. 30 日刻みなら `step=30`)、単位を
   markdown 等で明示
3. それぞれの widget が consume される下流があれば整合性を取り直す
   (本ノートの fixture では下流は薄い)

**過去のコードを使っている読者 (= 別チームの研究者、社内ノートを参照する
新人) が、なぜ書き換えが必要か / 旧仕様との差分は何か / フォールバック
判断の基準を即座に追えるよう、変更点と背景を本文に明示してください。**

skill 規約:
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/SKILL.md`
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/references/notebook_narrative.md`
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/references/post_review_reconciliation.md`
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/references/marimo_cell_granularity.md`

最終ノートを `notebook_F_widget.py` に上書き保存してください。
