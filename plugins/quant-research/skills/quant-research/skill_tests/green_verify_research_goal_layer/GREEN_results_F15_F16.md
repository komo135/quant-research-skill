# GREEN verify — F15 / F16 が解消したことの照合

RED (`skill_tests/red_research_goal_layer/`) で抽出した 2 つの構造的失敗モード
(= 規定の不在から生じる) が、GREEN 後の skill では発生しないことを確認する。

## skill 変更点 (該当 commit に含まれる)

- `references/research_goal_layer.md` 新設で 4 階層モデル (Research goal /
  Design hypothesis / Purpose / Hypothesis) を明示。`target_sub_claim_id`
  運用ルール、cheat sheet (どの情報がどこに住むか)、anti-rationalizations を
  集約。
- `assets/README.md.template` を改訂、`## Research goal` + `### Sub-claims` 表
  (G1.1, G1.2, ... の ID 付き) を必須化。
- `assets/hypotheses.md.template` のスキーマに `target_sub_claim_id` /
  `pathway` 列を追加。派生 H は親から `target_sub_claim_id` を継承、override
  時は `Statement` 列に reason を 1 phrase で記録。
- `assets/decisions.md.template` の Purpose entry に **Design hypothesis at
  open**、**Research-goal sub-claim progress update**、**Design hypothesis at
  close** の 3 セクションを追加 (mandatory)。
- `references/cycle_purpose_and_goal.md` に Cycle goal の **5 番目** の項目
  (`target_sub_claim_id`) を追加。SKILL.md と research_design.md も整合化。

## F15 — 派生 H 単発の根拠が研究目標に紐付かない

| RED 引用 | GREEN 後の状態 |
|---|---|
| Case J `notebook_J_derivation_orphan.py`: §H1 interpretation で「H1 で turnover が edge を食い切った、…OCF margin を合成軸に加える方向で試せる」と書かれるだけで、H2 が research-goal sub-claim のどれに貢献するかはノートにも `decisions.md` にも `hypotheses.md` にも記録されない。研究目標 (`README` の "live tradeable な quality factor") との紐付けが不在 | `notebook_J_post.py` + `hypotheses_post.md`: H202 行が `target_sub_claim_id = G1.1` (親 H201 から継承)、`pathway = 4` (failure-derived from H201 turnover axis; cash-flow 軸を独立成分として加える) と明示。読者は H202 の存在意義を「G1.1 を attack する派生 H、turnover failure axis から派生」と 1 行で理解可能 |

ノート本文 (= research artifact) には sub-claim ID を再述しない (= 単一情報源
原則)。代わりに **Cycle goal の 5 番目 `target_sub_claim_id = Primary G1.1`**
が Purpose 全体のレベルで anchor を提供し、その下の H 群はデフォルト継承。
override 時のみ `hypotheses.md` 側に reason 記録。

これによりユーザー指摘 (= 「派生 H は現状放置される、やるとしても仮説が主に
なり、何の為にこの仮説を立証したいのかが不明になる」) は解消する:

- 派生 H は `hypotheses.md` 行として永続化される (= 放置されない)
- 派生 H の anchor は research-goal sub-claim ID (= 仮説が主ではなく研究目標が主)
- "何の為に" は `target_sub_claim_id` が即答 (= 不明にならない)

## F16 — Purpose 終了 → 次 Purpose 開始時に研究目標との距離が更新されない

| RED 引用 | GREEN 後の状態 |
|---|---|
| Case K `decisions_fixture.md`: Purpose A 終了時の entry は現行テンプレ通りで、`Purpose-level synthesis` / `Derived Purposes for the next notebook` / `Direction rejected` がある。研究目標 (`live tradeable な quality factor を 1〜2 件特定する`) との距離更新は **テンプレに無いので書かれない** | `decisions_post.md`: Purpose A entry に `Design hypothesis at open` (predict G1.1 を進める)、`Research-goal sub-claim progress update` (G1.1: not started → confirmed、G1.2: not started → not started、G1.3: not started → not started、G1.4: not started → not started)、`Design hypothesis at close` (CONFIRMED) の 3 つの新セクション |

Purpose B (= exp_022) を開く時の根拠は、Purpose A の per-H 数値観察ではなく、
**`README_post.md` の sub-claim status table** (= G1.1 confirmed、G1.2/G1.3/G1.4
not started) を読むことで決まる。`exp_022` の "Design hypothesis at open" は
"G1.1 と G1.3 のうち、G1.3 のほうが consumer の意思決定に直接的に必要" と
明示的に推論を残す。

ユーザー指摘 (= 「1 サイクルでも目標達成にこういう実験が必要そう、でも終わって
みればサイクルの目標は達成できなかった、じゃーどうする?」) への回答も
`Design hypothesis at open` / `at close` が担う:

- at open: 「Purpose A を解けば G1.1 が confirmed か falsified に進む」予想を pre-commit
- at close: 予想が CONFIRMED か FALSIFIED かを記録、外れた時の binding axis を
  記録、次 Purpose 選定の根拠を README sub-claim status から再導出
- これにより「Purpose の設計仮説が外れた時にどうするか」の流れが構造化される

## F14 と F16 の独立性 (再確認)

`notebook_K_post.py` は F14 (handoff の本文流入) を踏まずに F16 を解消する形
で書かれている — `## Origin` セクションなし、`cross_h_synthesis Pattern 名` なし、
exp_021 への substantive な前向き参照なし、ただし Cycle goal 5 項目目で
`target_sub_claim_id = G1.3` を明示。

Purpose B 選定根拠は notebook 本文ではなく `decisions_post.md` の exp_021 entry
(= Research-goal sub-claim progress update + Design hypothesis at close +
Derived Purposes) と `README_post.md` の sub-claim status から読み取れる。
F14 の counter (= 新ノート本文に旧 synthesis を書かない) と F16 の counter
(= decisions.md / README に研究目標距離更新を書く) が **別経路で同時に効いて**
派生 Purpose の handoff が研究文書としても planning artifact としても整合する。

## 副次効果の確認

- `INDEX.md.template` が `target_sub_claim_id` 列を持つようになった結果、
  experiments/INDEX.md 単独で「どの Purpose がどの sub-claim を attack したか」が
  俯瞰可能。F16 解消に副次的に貢献。
- `cycle_purpose_and_goal.md` の Cycle goal 5 番目項目導入によって、Stage 0
  (= sub-claim 未決) と Stage 1 以降 (= sub-claim ID 付き) の境界が明示される。
  Stage 0 escape hatch ("my own next Purpose, named as <slug>") は依然として
  legal だが、Stage 1 以降の Purpose は `target_sub_claim_id` 必須。
