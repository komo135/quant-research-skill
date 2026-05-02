# Case H — 同 Purpose で 3 ラウンド回した時の `### Derived hypotheses` 表の累積

## 状況

`exp_011_jp_eq_quality_factor_iteration.py` (JP equity quality factor の net 5 bps 収益性) で、
3 ラウンドの H が並んでいる:

- H1 (ROE rank long-only) — verdict = REJECTED (turnover が edge を食い切り)
- H2 (ROE × OCF margin 合成) — verdict = SUPPORTED_PROVISIONAL (review 未通過)
- H3 (H2 を trending regime のみに限定) — 実装中、verdict PENDING

各 H 末尾には `hypothesis_cycles.md` の "What to write at the end of each H round"
テンプレに従って `### Derived hypotheses` 表が置かれている。表の中には:

- §H1 末尾: H2 (run-now) / H4 (next-session) / H5 (next-session) / earnings revision (drop)
- §H2 末尾: H3 (run-now) / H6 (next-session) / H7 (next-session)
- §H3 末尾: H8 (next-session) / H9 (new notebook)

H2 と H3 は run-now 行から実際に同ノートの次 H ブロックとして起きた。
H4-H9 は next-session または new notebook で、まだ実行されていない。

## あなたのタスク

`notebook_H_table_carryover.py` を in-place 編集し、以下を行ってください:

1. H3 の result セルを placeholder 数値で埋める
   (例: test Sharpe = 0.55、WF mean = 0.48、`failure_mode = "regime_filter"` で
   良い数字にしておく)
2. H3 verdict を PENDING のまま、interpretation セルを追加して何が分かったかを
   1 段落で書く
3. (1)(2) を反映して、H3 末尾の `### Derived hypotheses` 表が現状の状態を
   正しく表すように更新する
4. 全体のノートを `hypothesis_cycles.md` の routing / classification 規定と
   照らして整合させる。複数ラウンド分の表が並んでいるが、何が消化済みで
   何が生きているかを **読者がノート単独で読み取れる** ように整える

`hypothesis_cycles.md` の "What to write at the end of each H round" テンプレ
は各 H ラウンドの末尾で書くものとして規定されているので、その規定に
従ってください。

skill 規約:
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/SKILL.md`
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/references/hypothesis_cycles.md`
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/references/cross_h_synthesis.md`
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/references/notebook_narrative.md`

最終ノートを `notebook_H_table_carryover.py` に上書き保存してください。
