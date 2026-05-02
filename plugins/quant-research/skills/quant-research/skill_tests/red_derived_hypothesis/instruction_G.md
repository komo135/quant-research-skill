# Case G — 同 Purpose run-now 派生 H を次の `## H<id>` ブロックに昇格

## 状況

`exp_007_eurusd_intraday_meanreversion.py` (EUR/USD 5min mean-reversion) で
H1 (RSI(14) ≤ 30 entry × signal-flip exit) のラウンドが終わった。
verdict は PENDING (robustness 未通過、test Sharpe = 0.55 / WF mean = 0.42)。

H1 末尾の `### Derived hypotheses` 表に、同 Purpose に属する run-now 派生 H が
1 件含まれている:

| New hypothesis | Where | Run-now / next-session / drop | Reason |
|---|---|---|---|
| H2: Bollinger(20, 2.0σ) lower-touch entry × signal-flip exit、test Sharpe ≥ 0.5 | same notebook | run-now | 同 Purpose、別レンズで MR 再検証 (alternative formulation) |

`hypothesis_cycles.md` の routing rule (1) は "current notebook's Purpose statement
still cover the new H → next `## H<id>` block in the same notebook" と規定して
いるので、H2 はこのノート内の次 H ブロックとして昇格する。

## あなたのタスク

`notebook_G_promotion.py` を in-place 編集し、`## H2 — Bollinger…` 以下の
ブロックを追記してください。最低限必要なセル:

1. `## H2` 見出し
2. config cell (UNIVERSE / PERIOD / Bollinger window / k)
3. H2 abstract (markdown セル)
4. H2 result セル (今回は実装途中で OK、placeholder 数値で可)
5. H2 verdict セル (PENDING でよい)

H1 末尾の `### Derived hypotheses` 表に書かれていた **H2 の内容** を、新しい
`## H2` ブロック側で abstract / config / verdict セルに反映するのが本タスクの主旨。

`hypothesis_cycles.md` の "next round inside the same notebook" を文字通り
適用してください。表の H2 行をどう扱うか (残す / 消す / 印を付ける) の判断は
あなたの裁量で構いません — `hypothesis_cycles.md` 側に明示規定が無いため、
合理的と思う方法を採ってください。

skill 規約:
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/SKILL.md`
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/references/hypothesis_cycles.md`
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/references/research_design.md`
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/references/notebook_narrative.md`

最終ノートを `notebook_G_promotion.py` に上書き保存してください。
