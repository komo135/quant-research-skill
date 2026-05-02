# GREEN verify — 結果

RED で観察した F1〜F8 が、新スキル (post_review_reconciliation.md +
SKILL.md Step 11b/13b + notebook_narrative.md/bug_review.md 補強) のもとで
どこまで消えるかを、同じ 3 ケース (A: leakage / B: pnl-accounting /
C: claim-warrant) を `notebook_skeleton.py` の clean copy に対して再走させて
確認した。

## 結果サマリ

| 失敗モード | A (leakage) | B (pnl-accounting) | C (claim-warrant) | 全体 |
|---|---|---|---|---|
| F1 編集履歴の本文化 | ✓ 解消 | ✓ 解消 | ✓ 解消 | **解消** |
| F2 レビュー用語の本文化 | ✓ 解消 | ✓ 解消 | ✓ 解消 (`(literature dimension)` も消えた) | **解消** |
| F3 intercalary 章 (`§6a`, `§7b`, `Fig 2b`) | ✓ 解消 (§5 (continued) で章番号変更なし) | ✓ 解消 (`## Post-review addenda` に集約) | ✓ 解消 (`## Post-review addenda` に A1/A2) | **解消** |
| F4 旧値 audit (`*_pre_fix`、取り消し線) | ✓ 解消 | ✓ 解消 | ✓ 解消 | **解消** |
| F5 タスクメモ本文化 (`parked` / `follow-up` / `next-session`) | ✓ 解消 | ✓ 解消 (low finding は本文に出さず park) | ✓ 解消 | **解消** |
| F6 数値 / figure / observation の不整合 | ✓ 完全整合 (§0/§3/§7/§8 obs/§9 すべて post-fix) | ✓ 整合 (微差は四捨五入の範囲) | n/a (C は pipeline を触らない) | **解消** |
| F7 cross-round 整合性 | n/a | n/a | n/a | **未検証 (既知残)** |
| F8 セル位置の不統一 | ✓ P1 + 同セクション末尾 (P2) で統一 | ✓ P1 + `## Post-review addenda` (P3) | ✓ P1 + `## Post-review addenda` (P3) | **解消** |

## Why 品質 (advisor 予想の懸念点)

advisor は「reviewer 用語が消えた後 vague な why が残るのでは」と予想したが、
3 ケースとも具体的な why が書かれた:

- **A §5 (continued)** — 「per-date 標準化は cross-section が 1〜2 銘柄しか
  無い日に 1/sd で極端値を生む。極端値が test 期間に集中していると §6 以降の
  PnL がその日に支配されてしまうので、ここで早期に検知する。」
- **B Post-review addenda A1 (gross exposure)** — 「5bps の fee はポジション
  規模に対して引かれる。複数銘柄の long/short が日によって 50 銘柄なのか
  300 銘柄なのかで実質コスト負担は大きく変わる。Fig 2 の cum PnL を読むときに
  「どの規模の建玉に対する net 5bps なのか」を読者が同じ画面で判断できる
  ようにする。」
- **C Post-review addenda A2 (mechanism boundary)** — 「§9 H1 interpretation
  で「メカニズムは X」と単一の説明を選ぶと、集計 PnL では同じ Sharpe が複数の
  メカニズムから生じうるため claim が証拠の幅を超える。ここでは「現状の
  デザインで何までは言えて、何からが言えないのか」の境界を読者に明示する。」

`post_review_reconciliation.md` の bad/good why pair と 3-question self-test
が効いた可能性が高い。

## 検証されなかった範囲 — F7 (cross-round consistency)

DoD (5) 「過去ラウンドの finding との整合チェック」は、単一ラウンドの
fixture (各ケースが clean な skeleton から開始) では発火しない。これは
RED 段階でも同じ。

検証するには A → B → C を同じ notebook で順次走らせる sequential fixture が
必要。現状は `post_review_reconciliation.md` 内 "Cross-round consistency"
節にて「累積 finding 一覧を手元に置いた状態で通読する」運用ルールとして
書いてあるのみ。次のテストの機会があれば sequential 4 ケース目を作る価値あり。

## 結論

- ユーザーの 2 症状 (「構造ずれ」「目的不明セル」) を生む 7 / 8 の失敗モードが
  GREEN で解消した
- 残る F7 は単一ラウンド fixture では検証不能、運用ルールとして文書化済み
- skill changes: `post_review_reconciliation.md` (新規)、SKILL.md Step 11b/13b、
  `notebook_narrative.md` checklist 拡張、`bug_review.md` dispatch protocol
  step 6 追加
