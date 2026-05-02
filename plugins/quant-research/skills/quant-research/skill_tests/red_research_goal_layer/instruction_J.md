# Case J — 派生 H 単発の根拠不在 (research goal anchor 欠落)

## 状況

`exp_021_topix_quality_factor.py` で H1 (ROE rank long-only) のラウンドを回した
結果、verdict は REJECTED (WF mean = 0.18、月次 turnover = 45% で edge を食い切り)。

研究者は H2 (ROE × OCF margin の rank-平均合成) を試す判断をした。
`hypothesis_cycles.md` routing rule (1) に従い、H2 は同 Purpose 内の次 H ブロック
として昇格する (= F12-14 で扱った routing 自体は問題なく成立)。

## あなたのタスク

`notebook_J_derivation_orphan.py` を in-place 編集し、`## H2 — ROE × OCF margin
の rank-平均合成` 以下のブロックを追記してください。最低限必要なセル:

1. `## H2` 見出し
2. config cell
3. H2 abstract / interpretation (markdown セル)
4. H2 result セル (placeholder 数値で OK)
5. H2 verdict セル

**重要な制約 — F12-14 を踏まないこと**:

- `### Derived hypotheses` 表は書かないでください (GREEN で表をノート本文から
  退去させた世界を仮定)
- `parked` / `next-session` / `run-now` / `follow-up` などの状態語をノート本文に
  残さないでください (`post_review_reconciliation.md` L62-66 の禁止語彙ルール)
- §H1 → §H2 の接続は、interpretation セルでの自然な研究上の判断 (= 「H1 で
  turnover が edge を食い切った、次に独立軸を加えた合成を試したい」) として
  書いてください

研究プロジェクトの研究目標 (project README の Question) は **「JP equity universe
で live tradeable な quality factor を 1〜2 件特定する」** です。本タスクはこの
研究目標を達成する Purpose A (= TOPIX500 quality factor の net 5 bps 収益性) の
中で行われています。

skill 規約:
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/SKILL.md`
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/references/hypothesis_cycles.md`
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/references/research_design.md`
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/references/notebook_narrative.md`
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/references/post_review_reconciliation.md`

最終ノートを `notebook_J_derivation_orphan.py` に上書き保存してください。
