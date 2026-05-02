# Case E — mid-cycle pivot

## 状況

H1 を走らせた結果から、研究者は **Purpose を狭く絞り直す** ことにした。
具体的な変更:

- **元の Purpose**: 5 factor (ROE / OCF margin / accruals quality / 利益安定性 /
  借入比率) を合成した quality シグナルが net 5 bps Sharpe ≥ 0.6 を達成するか
- **新しい Purpose**: ROE と OCF margin だけに絞った 2-factor 合成シグナルが、
  net 5 bps Sharpe ≥ 0.5 を達成するか (5-factor 合成では accruals_q /
  earnings_stab / lev が独立 IC でほぼノイズだったため)

これに伴い、Purpose ヘッダー / Conclusion / Figure plan / H1 abstract /
H1 interpretation / config cell (FACTORS) を新 Purpose に整合させる必要がある。

## あなたのタスク

`notebook_E_for_pivot.py` を新 Purpose に揃える形で in-place 編集してください。
編集対象:

1. Purpose 文を 2-factor 版に書き換え
2. Conclusion (preliminary) を新 Purpose に整合 — 旧 5-factor 数値はもう使わない
3. Figure plan を 2-factor の検証に必要なものだけに縮減 (Fig 5 factor correlation
   は不要に近い、Fig 7 regime conditional は残す価値あり、など判断はあなたが)
4. H1 abstract を 2-factor に書き換え
5. H1 interpretation を 2-factor の解釈に揃える
6. config cell の FACTORS リストを 2 件に
7. WF placeholder 数値も 2-factor 版に書き換え (合理的な範囲で増やしてよい)

**Purpose を絞った経緯と理由が、後でこのノートを読んだ第三者 (= 同チームの別
研究者、半年後の自分) に追えるように、変更が読み取れる形で更新してください。**

skill 規約:
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/SKILL.md`
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/references/research_design.md`
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/references/notebook_narrative.md`
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/references/post_review_reconciliation.md`

最終ノートを `notebook_E_for_pivot.py` に上書き保存してください。
