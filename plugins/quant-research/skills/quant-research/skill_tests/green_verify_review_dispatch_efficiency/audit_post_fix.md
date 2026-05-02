# audit_post_fix.md — review skill dispatch (post-fix)

GREEN counter (= F21 per-dimension input contract + F22 trigger-conditional
re-verify dispatch) を `bug_review.md` + `experiment-review/SKILL.md` +
`experiment-review/references/review_protocol.md` に適用した後の dispatch
構造の再 audit。

## Reviewer roster — 不変

post-fix でも 14 reviewer (5 + 1 + 7 + 1)。roster の構成、specialist 数、
adversary asymmetry はすべて不変。GREEN counter は dispatch *規約* のみを
変更し reviewer instruction は触れない。

## F21 view — per-reviewer input bundle (post-fix)

`s§i` = DIMENSION-SPECIFIC SUFFIX に置く (= 該当 reviewer のみ受領)。
`-` = NOT-receive (= 入力 bundle に含めない)。

### bug_review (6 reviewer)

| Reviewer | notebook .py | upstream .py | bug_review.md | sanity_checks.md | hypotheses.md | decisions.md | literature/ |
|---|---|---|---|---|---|---|---|
| 1 leakage | inline | s (only those named in design cell) | s§1 (12 行) | s§1, §6, §7, §8, §9, §11, §12 | - | - | - |
| 2 pnl-accounting | inline | s | s§2 (14 行) | s§3, §4, §5, §6, §11 | - | - | - |
| 3 validation (corr) | inline | s | s§3 (12 行) | s§12 | - | - | - |
| 4 statistics | inline | s | s§4 (13 行) | s§10 | - | - | - |
| 5 code-correctness | inline | s | s§5 (12 行) | - | - | - | - |
| 6 bug adversarial | inline | s (only if named) | s§6 (39 行 instruction only) | - | - | - | - |

### experiment-review (8 reviewer)

| Reviewer | notebook .py | upstream .py | review_dimensions.md | severity_rubric.md | notebook_narrative.md | marimo_cell_granularity.md | hypotheses.md | decisions.md | literature/ |
|---|---|---|---|---|---|---|---|---|---|
| 7 question | inline | - | s§1 (39 行) | inline | - | - | inline | inline | - |
| 8 scope | inline | - | s§2 (63 行) | inline | - | - | inline | inline | - |
| 9 method | inline | s (only if named in design cell) | s§3 (40 行) | inline | - | - | - | - | - |
| 10 validation (suff) | inline | - | s§4 (37 行) | inline | - | - | - | s (bug-review entry only) | - |
| 11 claim | inline | - | s§5 (38 行) | inline | - | - | - | - | - |
| 12 literature | inline | - | s§6 (66 行) | inline | - | - | - | - | s (papers + diff) |
| 13 narrative | inline | - | s§7 (75 行) | inline | s (whole, narrative-specific) | s (whole, narrative-specific) | - | - | - |
| 14 exp adversarial | inline | - | s§8 (112 行 instruction + axes) | inline | - | - | - | - | - |

**観察**:

- whole-file `bug_review.md` / whole-file `review_dimensions.md` の R エントリが消滅、すべて s§i (section-only) に置換 (= F21 解消)
- narrative reviewer の `notebook_narrative.md` / `marimo_cell_granularity.md` のみ whole-file 維持 — これは reviewer の dimension scope 全体がそれらと一致する ("entirety is `narrative` scope"、no irrelevant sub-section)。anti-rationalization 表で明示済み

### F21 — raw 送信量 比較 (14 reviewer 合算)

仮定: notebook .py 1000 行、project artifacts は前回と同条件。

| ファイル | Pre-fix (送信量) | Post-fix (送信量) | 削減 |
|---|---|---|---|
| notebook .py | 14000 | 14000 | 0 |
| bug_review.md | 1500 (whole × 5) | 102 (s§i × 6) | -1398 |
| sanity_checks.md | 945 (whole × 5) | 300 (s§i × 5) | -645 |
| review_dimensions.md | 3912 (whole × 8) | 469 (s§i × 8) | -3443 |
| severity_rubric.md | 1192 | 1192 | 0 |
| notebook_narrative.md | 400 | 400 | 0 |
| marimo_cell_granularity.md | 166 | 166 | 0 |
| hypotheses.md | 200 | 200 | 0 |
| decisions.md | 600 | 600 | 0 |
| literature/ | 200 | 200 | 0 |
| **合計** | **23115** | **17629** | **-5486 (-24 %)** |

`upstream feature notebook .py` は variable で外置き (5 reviewer × 500 行 =
2500 行 が典型) — pre-extraction 対象外、両 case で同じ。

## F22 view — trigger-conditional dispatch on re-verify

Initial pass = 14 fire (不変)。Re-verify pass = surface map intersect ≠ ∅ の
specialist + adversary auto-fire。

### 典型 iteration profile (= bug_review fixture の baseline run と同条件)

H1 verdict='supported' の co-gate での 1 H attempt (Initial + 2 re-verify
rounds):

| iteration | 動作 | 発火 reviewer (post-fix) | agent run 数 |
|---|---|---|---|
| Initial pass | 14 reviewer 全 fire → 高 finding 3 件 (例: leakage in §5 / pnl-accounting in §6 / claim overstatement in abstract) | 全 14 | 14 |
| fix 適用 (round 1) | §5 → P1 in-place rewrite (leakage surface)、§6 → P1 in-place rewrite (pnl-accounting surface)、abstract → P1 wording rewrite (claim + narrative surface) | 0 | 0 |
| Re-verify pass 1 | surface intersect: leakage / pnl-accounting / code-correctness (catch-all) / claim / narrative + adversary (auto on any) | 1, 2, 5 + 11, 13 + 6, 14 = 7 | 7 |
| fix 適用 (round 2) | narrative reviewer が「abstract と verdict cell の数値ズレ」を指摘、verdict cell を P1 (claim + narrative + statistics surface 着地) | 0 | 0 |
| Re-verify pass 2 | surface intersect: claim / narrative / statistics + adversary | 4, 11, 13 + 6, 14 = 5 | 5 |
| **合計** | | | **26** |

vs Pre-fix (= 全 fire each round): 14 × 3 = **42 agent run**。

**削減**: 42 → 26 = **-38 %**。

### iteration depth 別の累積 agent run

| iteration rounds | Without F22 (= 全 fire) | With F22 (Initial 14 + 再 verify 平均 5) | 削減率 |
|---|---|---|---|
| 1 (Initial only) | 14 | 14 | 0 % |
| 2 (Initial + 1 re-verify) | 28 | 14 + 5 = 19 | -32 % |
| 3 | 42 | 14 + 5 + 5 = 24 | -43 % |
| 4 | 56 | 14 + 5 + 5 + 5 = 29 | -48 % |

re-verify per round の agent run は fix profile に依存 (1-7 specialist +
adversary)。conservative avg 5 で計算。

### Surface map intersect 判定の動作確認

具体 fix 例:

| Fix location | Surface intersect (= 再 fire 対象 dimension) |
|---|---|
| 信号計算式 (signal_h1 = ...) の P1 修正 | leakage (signal computation surface)、code-correctness (catch-all) + adversary |
| fee 値の literal を const cell から書き換え | pnl-accounting (fee model surface)、code-correctness + adversary |
| abstract cell の "supported" → "parked" 言い換え | claim (verdict / abstract surface)、narrative (markdown change) + adversary |
| literature/papers.md に新 paper 追加 | literature (literature/ files surface) + adversary |
| §5 の data load cell を polars version 上げ対応で書き換え (= 数値不変) | code-correctness (any code change) + adversary (=2 reviewer) |
| markdown comment 1 行直し | narrative (markdown surface) + adversary (=2 reviewer) |

**When in doubt, fire** rule によりエッジケース (例: 微妙に複数 surface に
跨る fix) は default で affected dimensions を全 fire、adversary が safety
net。

## Cross-session boundary 確認

researcher が次セッションで同 H に戻る:

- in-context に「前セッションで dimension {X, Y, Z} が verified clean」の
  記録なし → **Initial pass 扱い** (= 全 14 fire)
- decisions.md に attestation がある + agent が現 artifact が attestation
  時の state と一致を verify できる → re-verify 扱い (= surface map
  intersect で fire)
- 「I think it was clean」の anchoring は disqualification (anti-rationalization
  表で明文化済み)

## Quality machinery (= narrowness / asymmetry / parallelism / trigger discipline) との独立性 — verification

### narrowness — 強化された

| 機構 | Pre-fix | Post-fix |
|---|---|---|
| 各 specialist の attention scope | whole file 受領 + "read §i only" 指示 | §i のみ inline 受領 |
| Lost-in-middle 効果 | あり | なし |
| 各 specialist の独立性 | dispatch parallel、各 reviewer 単独で finding 生成 | 同上 |
| cross-dimensional finding 取りこぼしリスク | parallel ensemble の overlap で防御 | 同上 (reviewer 数も roster も touch していない) |

### asymmetry — 防御された

| 機構 | Pre-fix | Post-fix |
|---|---|---|
| adversary の minimum bundle | 形式上 (whole file が bundle に入るが reviewer に "read §6/§8 only" を指示) | 物理的に minimum (§6/§8 のみ inline) |
| adversary が specialists の scope を見ない | 形式論依存 | **強化** |
| Re-verify での adversary | always re-fire | any specialist 再 fire 時に auto re-fire (safety net) |

### parallelism — 不変

| 機構 | Pre-fix | Post-fix |
|---|---|---|
| Initial 並列 dispatch | 14 並列 | 14 並列 |
| Re-verify 並列 dispatch | 14 並列 | subset 並列 (typical 5 reviewer)、必要分だけ |

### trigger discipline — gate 機能維持

| 機構 | Pre-fix | Post-fix |
|---|---|---|
| Initial 発火条件 | verdict='supported' 直前必発火 | 同じ |
| Re-verify 発火条件 | 全 14 fire | surface intersect ≠ ∅ の dimension fire (= 変化のあった surface のみ retest) |
| gate cover | 全 14 review を通る | Initial で全 14 review、re-verify は changed surface 全 review、adversary safety net — gate 機能 維持 |

surface map と "When in doubt, fire" + adversary auto-fire の三重防御で、
gate を緩めずに re-verify cost を削る設計。

## Anchor-based extraction の robustness 確認

GREEN counter は **section anchor (= 見出し)** ベースで extract する規約を
明文化:

- bug_review.md: `### N. <reviewer-name>` (例: `### 1. leakage-reviewer`)
- review_dimensions.md: `## N. <dimension>` (例: `## 1. question — falsifiability, pre-registration, cycle hygiene`)

**Anchor 欠損時の挙動**: parent assistant が anchor 検索失敗 → reviewer
prompt の suffix に "missing input section §N — see contract row N" を
inline。reviewer は graceful-degradation で `severity: high, dimension:
<name>, what: missing input section §<N>` を flag。dispatch は abort せず
他 reviewer は通常実行。これは既存の "missing artifact" graceful
degradation 規約と同じ shape。

**Renamed anchor の挙動**: 同上 (= 該当 dimension の reviewer が
"missing input section" finding を出す)。skill 改修時の input-contract
更新漏れを正面で flag する設計、silent failure を防ぐ。

## Scope 限界 — 本 audit でカバーしない (再掲)

- **F20 (prompt caching)**: skill scope 外 (= Claude Code 内のスキルから
  API-level の cache_control を mandate する根拠なし)。F-id taxonomy には
  gap として残す。
- **実測**: 実際に sub-agent dispatch して billed input tokens を計測する
  検証は scope 外。理論値 (line × agent-run count) のみで判定。
- **Specific items to chase の機械化**: future RED 候補。
- **Cross-session attestation の format 詳細**: GREEN は skeleton 規定のみ、
  attestation 表記の verifiability は future iteration 候補。
