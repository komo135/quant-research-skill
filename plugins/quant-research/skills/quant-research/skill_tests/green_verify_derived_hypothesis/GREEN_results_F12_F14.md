# GREEN verify — F12 / F13 / F14 が解消したことの照合

RED (`skill_tests/red_derived_hypothesis/`) で抽出した 3 つの失敗モードが、
GREEN 後の skill では構造的に発生しないことを確認する。

## skill 変更点 (該当 commit に含まれる)

- `references/hypothesis_cycles.md` L120-128 の `### Derived hypotheses`
  表テンプレを削除。各 H ラウンド末尾は `### H<id> conclusion` + `### Cannot
  conclude` のみ。派生 H 表は `hypotheses.md` の `Status` 列 (planned-runnow
  / planned-nextsession / planned-drop) に一元化。
- `assets/hypotheses.md.template` のスキーマに `target_sub_claim_id` /
  `pathway` 列を追加、Status を細分化。
- `references/cross_h_synthesis.md` に「Handoff to the next notebook」セクション
  を新設。新ノート本文には旧 Purpose の synthesis / Pattern 名 / handoff 経緯を
  書かない (research content は OK、handoff prose は禁止)。
- `references/research_goal_layer.md` 新設で 4 階層モデルと `target_sub_claim_id`
  紐付けルールを集約。

## F12 — 派生 H 昇格時の二重登録

| RED 引用 | GREEN 後の状態 |
|---|---|
| Case G `notebook_G_promotion.py`: §H1 末尾の `H2: Bollinger... \| same notebook \| run-now` 行と §H2 ブロックが同時存在、二重登録 | `notebook_G_post.py`: §H1 末尾は `### H1 conclusion` + `### Cannot conclude` のみ。H2 の planning state は `hypotheses_post.md` H102 行の `Status` 列で記録 (in-progress)、§H2 ブロックの存在自体が "実装着手済" の証拠 |

GREEN 後は **`### Derived hypotheses` 表が skill のテンプレから消えた** ため、
F12 の根本構造 (= 表行のライフサイクル無規定 / 二重登録) が発生する余地が
無い。

## F13 — 多ラウンド表累積で TODO ボード化

| RED 引用 | GREEN 後の状態 |
|---|---|
| Case H `notebook_H_table_carryover.py`: §H1 / §H2 / §H3 各末尾に `### Derived hypotheses` 表が並列、消化済み行と生きている行が判別不能、ラウンド数 N で表数 N に成長 | `notebook_H_post.py`: 各 H ラウンド末尾は `### H<id> conclusion` + `### Cannot conclude` のみ。派生候補 (H204-H210) は `hypotheses_post.md` 側で行として並ぶが、Status 列で `planned-nextsession` / `planned-drop` と一元判定可能 |

ノートはラウンド数 N に対して表数 0 で固定。`hypotheses.md` 側でも各 H 行は
1 つの `Status` 値しか持たないので、消化済み / 生きている / 別ラウンドで吸収済み
の判定が単一情報源で可能。

## F14 — 新 Purpose handoff で旧 synthesis が新ノート本文に侵入

| RED 引用 | GREEN 後の状態 |
|---|---|
| Case I `notebook_I_purpose_handoff.py`: docstring に `cross_h_synthesis.md の Pattern A (binding axis = turnover) が出た結果として開かれた、派生 Purpose のうちの 1 本`、`## Origin (handoff from exp_012)` セクション、Purpose ヘッダーに `exp_012 で binding axis として特定された turnover を 30%/month に制約 (= 強い一次制約)` | `notebook_I_post.py`: docstring に handoff 経緯なし、`## Origin` セクション削除、Purpose ヘッダーは「EUR/USD 5min において、月次 turnover を 30%/month 以下に制約 (= 一次制約) した上で…」 の独立記述。`target_sub_claim_id = G2.2` を Cycle goal 5th item に明示 |

新ノートは旧ノートを **読まなくても** 独立した研究文書として成立する。
旧ノート synthesis / handoff 経緯は `decisions.md` の exp_012 Purpose entry
側にだけ存在 (= cross_h_synthesis.md の "Handoff to the next notebook" rule
と research_goal_layer.md の "What goes where" cheat sheet が同時に効いている)。

minimal cross-reference (= Figure plan の `Fig 4 ... h1_old / h1_capped` 比較系列名) は
research content として残るが、これは F14 が問題視する handoff prose では
ない (cross_h_synthesis.md の handoff rule で明示的に許容)。

## 副次効果の確認

skill 内の規定間整合不全 (= `hypothesis_cycles.md` の表テンプレ vs
`post_review_reconciliation.md` 禁止語彙表 L62-66 の `run-now` /
`next-session` / `parked` / `follow-up`) は、表テンプレ削除によって自動的に
解消した。`post_review_reconciliation.md` 自体には変更を入れていない (= 既存の
F5 counter は派生 H 表が消えたことで、carve-out なしに本文禁止ルールが
維持できる)。
