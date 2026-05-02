# Case K — Purpose 終了 → 次 Purpose 開始時、研究目標との距離レビューが無い

## 状況

前ノート `exp_021_topix_quality_factor.py` (= ケース J で扱った Purpose A) は
Primary YES で closing 完了している:

- Decision rule の YES 条件 = 少なくとも 1 シグナルで WF mean Sharpe ≥ 0.4 を
  H2 (ROE × OCF margin 合成) が達成 (WF mean = 0.41)
- Purpose A の Purpose-level synthesis: 「TOPIX500 quality factor のうち、ROE
  単独は turnover で retire したが、OCF margin との合成で net 5 bps 帯に残る」
- `decisions.md` には現行テンプレ通りのエントリが記録されている (`### YYYY-MM-DD
  cycle 1 (exp_021_topix_quality_factor) — Purpose: ...` 形式)

研究者は次の Purpose B を開く判断をした:

- **Purpose B** = TOPIX500 quality factor を 3-factor (ROE / OCF margin / accruals
  quality) に拡張して更に Sharpe を伸ばせるかを検証する

## あなたのタスク

新ノート `notebook_K_purpose_close_no_review.py` を、`hypothesis_cycles.md` の
"Across Purposes — next notebook" 規定と `cycle_purpose_and_goal.md` / `research_design.md` の
Purpose ヘッダー規定に従って書いてください。最低限必要なセル:

1. docstring
2. Purpose ヘッダー (`## Purpose`)
3. Cycle goal — 4 items
4. Hypotheses tested セクション (H1 のみ)
5. Conclusion (preliminary)
6. Figure plan
7. `## H1` ブロック (config / abstract / result placeholder / verdict PENDING)

**重要な制約 — F14 を踏まないこと**:

- `## Origin (handoff from exp_021)` のような独立セクションは書かないでください
  (F14 = 旧ノート synthesis の新ノート本文流入の対象)
- `cross_h_synthesis.md` Pattern 名 / 「派生 Purpose」「handoff」のような skill
  プロセス由来語は新ノート本文に侵入させないでください
- exp_021 への参照は最小限 (= 必要なら Figure plan の `Fig 4` で「1-factor /
  2-factor / 3-factor の累積 PnL 比較」と書く程度) にしてください

研究プロジェクトの研究目標 (project README の Question) は **「JP equity universe
で live tradeable な quality factor を 1〜2 件特定する」** です。本ノート
(Purpose B) はこの研究目標達成の **次のステップ** として開かれています。

skill 規約:
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/SKILL.md`
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/references/hypothesis_cycles.md`
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/references/cycle_purpose_and_goal.md`
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/references/research_design.md`
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/references/notebook_narrative.md`
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/references/cross_h_synthesis.md`
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/references/post_review_reconciliation.md`

最終ノートを `notebook_K_purpose_close_no_review.py` に上書き保存してください。
