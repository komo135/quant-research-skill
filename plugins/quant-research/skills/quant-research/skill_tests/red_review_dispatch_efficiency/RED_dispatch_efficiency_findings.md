# RED dispatch efficiency — F21 / F22 の集計

ユーザー指摘:

> 「レビュースキルの TOKEN 負荷が高すぎるので質は落とさずに軽くしたい」

を、`bug_review` + `experiment-review` の dispatch protocol が **per-dimension
pre-extraction を機械化していない** + **re-verify 時にも全 reviewer が再発火
する** という構造的不在に紐付けて再現させた結果、2 つの efficiency-class
失敗モード (F21 / F22) が観察された。

## Class 表記 (taxonomy 上の位置)

F1-F19 はすべて **quality-class** (silence-licensed inversion / leak /
sub-claim anchor 不在 / structural drift)。F21 / F22 はそれと別軸の
**efficiency-class** (dead weight / redundant dispatch)。失敗内容が「quality
低下」ではなく「input cost / agent run count 浪費」であることに留意。GREEN
counter は cost のみを下げ、**quality machinery (narrowness / bundle
asymmetry / parallelism / trigger discipline before verdict='supported')
には触れない**。

| F-id | Class | 内容 |
|---|---|---|
| F1-F8 | quality | 本文への履歴 / レビュー用語の流入 |
| F9-F11 | quality | skill version / migration / cross-skill API tutorials in body |
| F12-F14 | quality | 派生 H 表のノート流入 |
| F15-F16 | quality | research-goal layer 不在 |
| F17 | quality | carryforward conjunct contribution gate |
| F18-F19 | quality | research-subject drift |
| ~~F20~~ | (skipped) | 当初 "prompt caching" として候補化したが、Claude Code 内のスキルから API-level の `cache_control` を mandate するのは越権 + 並列 sub-agent 間の cache 共有が harness 依存で不確定、と判断して採用せず |
| **F21** | **efficiency** | dispatch protocol が per-dimension pre-extraction を機械化していない |
| **F22** | **efficiency** | re-verify 時にも全 reviewer が再発火、surface-map ベースの conditional dispatch が無い |

## F21 — dispatch protocol が per-dimension scope を pre-extract していない

`bug_review.md` (300 lines) と `review_dimensions.md` (489 lines) は **whole
file が specialist に渡され、reviewer agent が attention で section を絞る**
設計。各 reviewer の actual scope は 4-23 % のみ、残り 77-96 % は dead
weight。

### 該当箇所

| ファイル | 行 | 抜粋 |
|---|---|---|
| `bug_review.md` | 69-77 (pre-fix) | "The five specialists each receive: ... `bug_review.md` ... The reviewer-specific scope below" (whole file + read §i only の設計) |
| `experiment-review/references/review_protocol.md` | 53-58 (pre-fix) | "Your scope and checklist: skills/experiment-review/references/review_dimensions.md (read only the section for [dimension name])" (whole file + read §i only の設計) |
| `experiment-review/references/review_protocol.md` | 36-39 (pre-fix) | "Tailor each specialist's input bundle accordingly to keep the brief tight." (prose 規定のみ、dimension 毎の **required / optional / NOT-receive** を明文化した structured contract が無い) |

### 現行の dead weight (audit_current_dispatch.md より)

| ファイル | 全 reviewer 合算行数 | actual scope 行数 | dead weight 行数 |
|---|---|---|---|
| bug_review.md | 1500 (5 reviewer × 300) | 65 (各 §i のみ) | 1435 (96 %) |
| review_dimensions.md | 3912 (8 reviewer × 489) | 462 (各 §i + adversary §8) | 3450 (88 %) |
| sanity_checks.md | 945 (5 reviewer × 189) | ~300 (per-reviewer 必要 check のみ) | ~645 (68 %) |

合算 dead weight ≈ **5530 行** (~22K tokens at 4 tokens/line)。

### 理論的削減量

pre-extraction (= whole-file → section-only) でこの 5530 行を除去できる。
これは pure に prompt 内容の整形なので、スキルが直接 control できる。
quality 不変 (= 各 reviewer は元々 §i scope に集中する設計、whole file 渡しは
"safety blanket" にすぎず削っても reviewer の検査内容に影響なし)。

- **Without pre-extraction**: 5530 dead-weight lines billed (= 全 reviewer
  合算 23115 行 のうち 24 %)
- **With pre-extraction**: 0 (= whole file の代わりに section だけ渡す)
- **削減**: raw 送信量 **-24 %**

## F22 — re-verify 時にも全 reviewer が再発火する

現行 dispatch protocol は **trigger-conditional でない**。verdict='supported'
の前に bug-review + experiment-review が走り、findings を反映する fix が
当てられた後、re-verify するときに **全 6 + 全 8 = 14 reviewer が再発火**
する。reviewer のうち多くは「自身の surface に変化が無い」のに再走している。

### 該当箇所

| ファイル | 行 | 抜粋 |
|---|---|---|
| `bug_review.md` | 11 (pre-fix) | "About to declare `verdict = "supported"` for any experiment" — supported 宣言の度に 6 reviewer 全 fire |
| `experiment-review/SKILL.md` Process step 4 (pre-fix) | "Dispatch all eight reviewers *in parallel* via the assistant's sub-agent tool" — re-verify でも 8 全 fire |
| `bug_review.md` step 6 Post-review reconciliation | 反映後 "re-running the battery" を要求するが、battery と review の関係に "どの reviewer が再発火するか" の規定が無い |

### 現行の挙動 (= 典型 iteration)

1. **Initial pass**: 14 reviewer 全 fire → 高 finding 3 件 (例: leakage / pnl-accounting / claim) 出力
2. **fix 適用**: 3 surface に対して P1 (in-place rewrite) を当てる
3. **Re-verify pass 1**: **再び 14 reviewer 全 fire** ← 11 reviewer は自身の surface に変化なしで dead reading
4. (高 finding 残れば) **fix 適用**: 1-2 surface
5. **Re-verify pass 2**: **再び 14 reviewer 全 fire** ← 12-13 reviewer は dead reading

iteration N round で 14×N agent run が課金される。surface 不変の reviewer も
毎回 notebook + dimension scope を読み直す。

### 理論的削減量

surface map ベースの conditional dispatch を導入:

- Initial pass: 14 fire (不変)
- Re-verify pass: 該当 surface に変化のあった specialist + adversary のみ fire
  - 典型 fix: 2-4 surface に着地 → 2-4 specialist + adversary = 3-5 reviewer
  - 11-9 reviewer は skip (= "no surface change since last clean review")

iteration profile 別の agent-run count 削減:

| iteration rounds | Without F22 (= 全 fire) | With F22 (Initial 14 + 再 verify n×4 avg) | 削減率 |
|---|---|---|---|
| 1 (= initial only) | 14 | 14 | 0 % (= initial では効かない) |
| 2 (= initial + 1 re-verify) | 28 | 14 + 4 = 18 | -36 % |
| 3 | 42 | 14 + 4 + 4 = 22 | -48 % |
| 4 | 56 | 14 + 4 + 4 + 4 = 26 | -54 % |

re-verify 1 回あたりの specialist 平均 4 (例: 5 surface fix のうち 4 が
distinct dimension に着地) を仮定。実際は fix 内容次第で 2-7 程度に分散。

## 共通失敗パターン — quality 機構との直交性

F21 / F22 は両方とも **dispatch 前の parent assistant の prompt 組み立て /
発火判定の規約に対する欠落**。reviewer agent 自体の挙動 (= narrowness /
specialist 独立性 / cold-eye asymmetry / parallel) は何も変わらない。

| Quality 機構 | 現行 | F21/F22 GREEN counter 後 |
|---|---|---|
| narrowness | 各 reviewer が §i scope を read | 各 reviewer が §i だけを inline で受領 → narrowness が **より厳密に** |
| asymmetry | adversary が minimum bundle | 同上 (whole file → §8 のみ抽出で **強化**) |
| parallelism | 14 並列 dispatch | 同上 (Initial)、再 verify では subset 並列 |
| trigger discipline | verdict='supported' 直前必発火 | Initial では不変。Re-verify は surface map 経由で必要 dimension のみ — gate 全体としては無傷 |

GREEN counter は **dispatch 規約のみを変更し、reviewer instruction も
specialist 数も roster も touch しない**。

## 想定 GREEN counter (詳細は GREEN フェーズ)

### F21 — Per-dimension input contract

`bug_review.md` + `experiment-review/references/review_protocol.md` に
dimension 毎の **required / optional / NOT-receive** 表を新設。dispatch
protocol に「parent assistant が dispatch 前に該当 section を anchor (見出し名)
ベースで extract」を明記。

### F22 — Trigger-conditional dispatch on re-verify

`bug_review.md` + `experiment-review/references/review_protocol.md` に
**Initial pass vs Re-verify pass** の区別 + **surface map per reviewer**
を新設。Re-verify では fix locations と surface map を intersect、該当
specialist + adversary のみ fire。Cross-session は Initial 扱い (decisions.md
attestation がない限り)。"When in doubt, fire" のデフォルト規定で skip-side
の error を防ぐ。

## ユーザー指摘との対応関係

| ユーザー要素 | RED で観察された側面 |
|---|---|
| 10 以上の Agent が走る | 14 sub-agent が verdict='supported' の度に発火 |
| TOKEN 負荷が高い | F21: 14 reviewer 合算 23115 行のうち 5530 行 dead weight (24 %)。F22: re-verify ごとに 14 全 fire = iteration N rounds で agent run 14×N |
| 質は落としたくない | F21/F22 は **dispatch 規約の変更**、quality machinery (narrowness / asymmetry / parallelism / trigger discipline) は不変 |

## F1-F19 を GREEN で潰しても F21 / F22 は残る

これは GREEN フェーズで重要な区別:

- F1-F11 / F12-F14 / F15-F16 / F17 / F18-F19 はすべて quality-class、
  prompt 内容 / structure に対する failure mode。
- F21 / F22 は **dispatch process** に対する failure mode で、quality-class
  fixture をどれだけ修正しても残る。

回帰として、既存 RED fixtures の expected GREEN 挙動は不変。

## Scope 限界 — 本 RED でカバーしないもの

- **F20 (prompt caching)**: 当初候補化したが skill scope 外と判断。Claude
  Code 内で動くスキルは API-level の `cache_control` marker を直接指定
  できない (harness 責任)、また並列 sub-agent 間の cache 共有挙動も
  harness 依存で不確定。skill 文言で mandate する根拠がないため採用せず。
- **実測 (= 実際の sub-agent dispatch で billed input tokens を計測)**:
  本 RED は理論値 (line counts / agent-run counts) のみ。実測がほしくなったら
  future RED で別途。
- **Specific items to chase の機械化**: efficiency に効く第 3 のレバー、
  本 RED では未採用、future RED 候補。
- **Cross-session re-verify を attestation 経由で受け付ける機能の精緻化**:
  GREEN counter で skeleton を提示するが、attestation の format /
  verifiability の詰めは future iteration 候補。
