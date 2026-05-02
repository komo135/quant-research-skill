# Case D — skill upgrade migration

## 状況

このプロジェクトは quant-research skill v0.7.0 で運用していたが、最近 v0.8.0 に
upgrade された。v0.8.0 で導入された主要変更:

- Purpose ヘッダーに 4 項目が必須化:
  Consumer / Decision / Decision rule (YES/NO/KICK-UP) / Knowledge output
  (`references/cycle_purpose_and_goal.md` 参照)
- 各 H ブロックに「Sub-claim of the decision rule that this H tests」を
  記述する (`references/research_design.md` 参照)
- cycle 終了の primary stops (Primary YES / Fallback NO / KICK-UP) と
  emergency stops (N=5 / N=8) の概念分離 (`references/hypothesis_cycles.md`)

## あなたのタスク

`notebook_D_legacy_v07.py` は v0.7.0 当時に書かれた既存実験ノート。これを
v0.8.0 規約にあわせて in-place で upgrade してください。具体的には:

1. Purpose ヘッダー直下に Consumer / Decision / Decision rule / Knowledge
   output の 4 項目を追加する。値は適宜あなたの判断で記入してよい (本ノートが
   想定する内部消費先を 1 つ名付けるなど)。
2. H1 ブロックに「Sub-claim of the decision rule that this H tests」を追加。
3. cycle 終了条件 (primary stops vs emergency stops) を意識した記述に揃える。

**過去のノート利用者が、このノートが skill upgrade を経たことと、何が更新
されたかを後で追えるよう、変更点が読み取れる形で更新してください。**

skill 規約:
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/SKILL.md`
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/references/cycle_purpose_and_goal.md`
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/references/research_design.md`
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/references/hypothesis_cycles.md`
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/references/notebook_narrative.md`
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/references/post_review_reconciliation.md`

最終ノートを `notebook_D_legacy_v07.py` に上書き保存してください。
