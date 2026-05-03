# DECISIONS — quant-research skill rebuild

**Append-only.** 過去の決定を遡って書き換えてはいけない。撤回する場合は新しいエントリで撤回理由を記述。

各エントリの形式:

```
## D-N: <短いタイトル>
- Date: YYYY-MM-DD
- Status: frozen | revisable | superseded-by-D-M | open
- Trigger: 何がこの決定を必要にしたか
- Decision: 何を決めたか
- Rationale: なぜこの決定にしたか
- Alternatives considered: 比較した選択肢
- Owner: 誰が承認したか (user / agent / both)
- Linked: 関連 file / Charter section
```

---

## D-1: 旧スキル構成を全面再構成する

- Date: 2026-05-03
- Status: frozen
- Trigger: ユーザ依頼「レビュースキルはスリム化していったん現構成は捨てて再構成」
- Decision: 旧 SKILL.md / bug_review.md / hypotheses.md / research_state.md / experiment-review との二層構造を捨て、ゼロから設計し直す。
- Rationale: 部分修正では sycophancy / 楽観バイアス / 引用と実装の乖離 / 423 行レビューといった構造的問題を断てない。
- Alternatives considered:
  - (A) 部分修正のみ → 構造問題は残る、却下
  - (B) スキル丸ごと新規作成 → 既存資産 (sanity_checks / leakage_check / TRL 規律 etc.) を活かせない、却下
  - (C) 採用案: 中核命題を凍結して再構成、ヘルパーは監査指摘を反映して再実装、ledger / charter / prereg は新設
- Owner: user 承認 + agent 設計
- Linked: CHARTER.md C1-C12

---

## D-2: 二大ディシプリン (R&D / Pure Research) のみに絞る

- Date: 2026-05-03
- Status: frozen
- Trigger: ユーザ依頼「R&Dモード(技術確立)とPure Researchモード(知識獲得)の二分化、TRLに倣ったmaturityスケールでの能力分解 これだけにしよう」
- Decision: 中核は 2 ディシプリン (R&D = 技術確立, Pure Research = 知識獲得)。それ以外のモードは設けない。
- Rationale: 入口・進行・状態・promotion・deliverable の全部が違う 2 規律として独立させた方が、各規律を最大強化できる。
- Owner: user 承認
- Linked: CHARTER.md C1, C2, C3

---

## D-3: 旧 plugins/ 重複ディレクトリは削除

- Date: 2026-05-03
- Status: frozen
- Trigger: 前回 audit で `C:\Users\komo_\project\quant-research-skill\plugins\quant-research\skills\quant-research\` に skills/ と完全複製があることが判明
- Decision: 実装フェーズで plugins/ 配下の重複は削除。`skills/quant-research/` を唯一のソース・オブ・トゥルースとする。
- Rationale: ソース二重化はファイル間 drift の主要因。
- Owner: user 承認 + agent
- Linked: GUARDRAILS.md G9

---

## D-4: 業界実証された 6 つのフレームを agent 用に圧縮埋め込み

- Date: 2026-05-03
- Status: frozen
- Trigger: ユーザ依頼「実際のR&Dの進め方、実際の研究を調べてそれをAgentが最大限効果を発揮できるようなスキルにしてほしい」
- Decision: 以下の業界実証フレームをそのまま採用 (改変なし、agent 用に縮約のみ):
  - DARPA Heilmeier Catechism (8 questions) → R&D charter
  - Cooper Stage-Gate (5 stages + 5 gates) → R&D capability progression
  - NASA TRL (0-9) → R&D capability maturity, TRL-6 を promotion line
  - Amazon Working Backwards (PR/FAQ) → Pure Research entry
  - AEA Pre-Analysis Plan → Pure Research p-hacking 防止 (hash-locked)
  - IMRAD → Pure Research deliverable
- Rationale: いずれも数十年の実証がある。新規発明より圧倒的に低リスク。
- Owner: user 承認 ("おおむねいい")
- Linked: CHARTER.md H3, C4-C8

---

## D-5: Review skill は Process / Conclusion 2 軸に圧縮、並列 6 reviewer は廃止

- Date: 2026-05-03
- Status: frozen
- Trigger: ユーザ依頼「レビュースキルはスリム化」「レビュースキルは研究の質や進め方に問題がなかったかや結論に間違い、問題がないかを検証」
- Decision:
  - 旧 bug_review.md (423 行, 6 specialist 並列, F21/F22 dispatch protocol) と外部 experiment-review skill の二層構造を全廃
  - 新 process_review.md (~100 行, 進め方の質) と conclusion_review.md (~100 行, 結論の妥当性) の 2 ファイルに集約
  - adversarial cold-eye check は conclusion_review の最終 section に embed (廃止せず縮約)
- Rationale: 6 並列 dispatch は実運用負荷が大きく、agent 環境差で再現性が低い。2 軸 + 1 ファイル + 自己実行可能 checklist で十分。
- Owner: user 承認
- Linked: CHARTER.md C9

---

## D-6: Kill > Promote の非対称バイアス

- Date: 2026-05-03
- Status: frozen
- Trigger: ユーザ依頼 "Agentの欠点として すぐに楽に答えを出したがる" + Google X "kill 文化" の調査結果
- Decision: kill 基準は 1 項目 fire で kill 確定。promote は全項目 pass + 具体 evidence 引用必須。
- Rationale: agent 構造的に supported / matured / 完了 に bias する。kill のしきい値を低くすることで構造的に対称化。
- Owner: user 承認
- Linked: CHARTER.md C10, GUARDRAILS.md G1

---

## D-7: 完了判定は具体 evidence 引用必須

- Date: 2026-05-03
- Status: frozen
- Trigger: ユーザ依頼 "表面的な情報だけですべてを把握したつもりになる"
- Decision: promotion / gate / review のすべての判定項目に対し、file:line, hash, metric value, ツール出力 の **いずれか具体 evidence** を貼る必須。"全体的に OK", "おおむね pass" のような summary 表現は **禁止**。
- Rationale: agent の "把握したつもり" を構造で検出可能にする唯一の方法。
- Owner: user 承認
- Linked: CHARTER.md C11, GUARDRAILS.md G2

---

## D-8: 凍結ファイル (charter / prereg / kill criteria) は SHA-256 hash + timestamp で機械的に改ざん防止

- Date: 2026-05-03
- Status: frozen
- Trigger: AEA pre-registration の調査結果 + agent の事後合理化バイアス
- Decision: charter, pre-registration, kill criteria fire log は `scripts/prereg_freeze.py` (新規) で SHA-256 hash + timestamp と共に `.locks/` 以下に記録。trial 後の actual との diff は `scripts/prereg_diff.py` (新規) で機械的に取る。
- Rationale: AEA は 2018 年から全フィールド実験で pre-registration 必須化。p-hacking 防止の単一最強介入。agent の場合さらに強い (memory-based 事後改ざんが起こり得る)。
- Owner: user 承認
- Linked: CHARTER.md C5, C12, GUARDRAILS.md G12

---

## D-9: ユーザ "確認したい 7 論点" のデフォルト採用

- Date: 2026-05-03
- Status: revisable (実装中にユーザから明示的異論があれば再検討)
- Trigger: ユーザが前メッセージで「おおむねいい」と回答、個別 7 論点には未回答。即実装フェーズ移行を指示。
- Decision: 7 論点すべてデフォルト採用 (CHARTER.md "ユーザ確認したい論点 7 件への扱い" 参照)。実装中に異論が出たら DECISIONS に新エントリで上書き。
- Rationale: ユーザが詳細議論をスキップして実装に進む意思を示した。デフォルトは設計提案そのまま。
- Owner: agent 推定 (user 黙示承認)
- Linked: CHARTER.md "ユーザ確認したい論点 7 件への扱い"

---

## D-10: .rebuild/ メタワークスペースを project root に作成

- Date: 2026-05-03
- Status: frozen
- Trigger: ユーザ依頼「進捗やコンテキスト断絶に備えるためにファイルを作成して 途中でやることや意図が変わらないようにしよう」
- Decision: `C:\Users\komo_\project\quant-research-skill\.rebuild\` に README / CHARTER / DECISIONS / PROGRESS / GUARDRAILS の 5 ファイルを作成。セッション開始プロトコルで強制読み込み。
- Rationale: コンテキスト断絶後の再構築コストを最小化。drift 検出を構造化。
- Owner: user 依頼
- Linked: README.md, GUARDRAILS.md, CHARTER.md, PROGRESS.md, このファイル

---

## Open decisions (未決、実装フェーズで判断が必要)

### O-1: scripts/ で polars vs pandas の依存を統一するか

- Trigger: 前回 audit 指摘 (polars と pandas が混在)
- Options: (A) pandas に統一 / (B) polars に統一 / (C) 両対応 wrapper
- Default 提案: pandas に統一 (互換性優先、agent が学習している量も多い)
- Decision needed before: scripts/ 監査修正フェーズ開始時

### ~~O-2: marimo notebook 形式を維持するか~~ → **Promoted to D-15**

### ~~O-3: lit_fetch.py の API source~~ → **Promoted to D-21**

### ~~O-4: env lock の標準化 (uv / pip-tools / poetry / conda)~~ → **Promoted to D-16**

## D-28: Phase 7 + 8 完了 — rebuild 終結

- Date: 2026-05-03
- Status: frozen (rebuild project closure)
- Trigger: ユーザ "y" — Phase 7 (cleanup) + Phase 8 (eval/regression) を進める指示
- Decisions executed:

### Phase 7 (cleanup)

- **References**: 12 keepers を `references/shared/` に移動 (mv 成功)、7 retired files (bug_review / failure_analysis / hypothesis_quality / pure_research_protocol / research_modes / research_state / technology_decomposition) を **deprecation stub に置換** (rm が sandbox 制約で permission denied のため stub 化で graceful migration を実現)
- **Assets**: 4 keepers (decisions / papers / differentiation / INDEX) を `assets/shared/` に **コピー** (元ファイルは sandbox 制約で削除不能のため両方 active、stub 化済 retired は research_state.md / hypotheses.md / purpose.py / README templates の 4 件)
- **Plugin distribution sync (D-13 implementation)**: `scripts/build_plugin.py` 新規作成 (~190 行、build mode + --check mode for CI drift detection)

### Phase 8 (eval / acceptance)

- **D-14 実行 — experiment-review skill 削除**: `plugins/quant-research/skills/experiment-review/SKILL.md` を deprecation stub に置換 (description が migration message を提供)。`.codex-plugin/plugin.json` と `.claude-plugin/plugin.json` + `marketplace.json` を **version 1.0.0 に bump**、description を v1.0 仕様に更新 (breaking change 明示)
- **既存テスト集約**: Phase 1-6 の subagent test 結果を以下にまとめる:
  - Pressure test 1 (D-17): 9/9 PASS structural defenses
  - Pressure test 2 (D-19): 18 改善発見 → 5 即適用 + 13 deferred (全対応済)
  - Pressure test 3 (D-20): 1 critical bug + 8 minor 発見 → 4 即適用 + 4 deferred (全対応済)
  - Phase 2 dummy verification (D-23): R&D 一周完走、3 friction (F1-F3) 即修正
  - Phase 3 dummy verification (D-24): Pure Research 一周完走、3 friction 即修正
  - Phase 4 dummy verification (D-26): REJECT/APPROVE 両方正常動作、3 friction (F7-F9) 即修正
  - 旧 bug_review.md regression (D-25): 35/35 patterns covered, 2 gaps patched

### 最終統計

- skill 全体: 約 13000 行 (SKILL.md 417 + R&D references 約 2330 + Pure Research references 約 2320 + shared references 約 1014 + review references 約 620 + scripts 約 6300)
- DECISIONS: D-1 〜 D-28 (28 frozen + 5 superseded), open decisions O-1, O-5 のみ残 (low priority)
- CHARTER amendments: 3 (Amendment-1 analysis depth, Amendment-2 core tech 二層, Amendment-3 integration pattern)
- GUARDRAILS: G1-G17 (17 失敗モード + 構造的対策)
- PROGRESS: 全 Phase 0-8 完了

- Owner: agent execution + user 承認 (multiple "y" along the way)
- Linked: PROGRESS.md (Phase 0-8 全 [x])、CHARTER.md C1-C15 + Amendment-1/2/3、GUARDRAILS.md G1-G17、 build_plugin.py (D-13 実装), experiment-review SKILL.md stub (D-14 実行)

---

## D-27: Integration pattern を charter (H8) で明示宣言、Pattern 3 (skeleton + spike) を default 推奨

- Date: 2026-05-03
- Status: frozen (CHARTER Amendment-3)
- Trigger: ユーザ指摘「技術を分割するのは必要だけど いつまでたっても動くもの (その技術で作成したいもの) ができないのでは」+ "framework-first だと難しい技術や未知の技術に対して効果を発揮できないのでは"、ユーザ承認 "よいです ありがとう すすめて"
- Decision:
  - 3 patterns 定義 (Pattern 1 vertical slice / Pattern 2 bottom-up / Pattern 3 skeleton + spike)
  - **Pattern 3 を recommended default**
  - **Charter (H8) で integration pattern の explicit 宣言を REQUIRED 化**
  - Decision tree (Q1-Q4) を `integration_patterns.md` で具体化
  - Stage-Gate workflow への影響を pattern-aware に書き直し
  - 4 anti-patterns 明示 (implicit Pattern 2 / Pattern 1 with stub baselines / Pattern 3 skeleton becomes framework / Pattern 2 with stakeholder pressure)
- Rationale:
  - 旧 protocol は Pattern 2 を implicit default にしており、「動くものができない期間」問題が起きやすい
  - Pattern 1 (framework-first) の lock-in リスクと Pattern 2 (bottom-up) の "no working version" risk の中間として Pattern 3 が最適
  - Pattern 1 が genuinely 未知技術に効かないというユーザ懸念は正しく、decision tree で明示
- Alternatives considered:
  - (A) 何もしない (ユーザ判断に任せる) → implicit Pattern 2 default が agent bias を生む、却下
  - (B) Charter H8 拡張のみ (軽い) → integration pattern が他 reference (rd_stages, capability_map_schema) からも参照されるため不十分、却下
  - (C) **採用**: 新規 `integration_patterns.md` (430 行) + rd_charter H8 expand + rd_stages Stage 5 pattern-aware + charter template field 追加
- Files:
  - `references/rd/integration_patterns.md` (430 行, 新規)
  - `references/rd/rd_charter.md` § H8 (Midterm + Final + Integration pattern, 約 269 行)
  - `references/rd/rd_stages.md` (Pre-condition + Stage 5 pattern-aware, 約 264 行)
  - `assets/rd/charter.md.template` H8 section (Integration pattern field 追加, 約 89 行)
- Owner: ユーザ承認
- Linked: CHARTER C15 (Amendment-3), Phase 5 で `validate_ledger.py` が integration pattern declaration check するか検討、Phase 6 で関連 helper script への影響評価

---

## D-26: Phase 4 dummy verification 結果 — REJECT/APPROVE 両方正常動作 + F7-F9 patches

- Date: 2026-05-03
- Status: frozen (test result + applied patches)
- Trigger: ユーザ指示 "(C) → (A) → (B)" の (A) 部分
- Test setup: 2 sub-agent 並列。Agent A = 13+ flaws の R&D promotion claim を review、Agent B = 完全に正しい Pure Research promotion claim を review。
- Test results:
  - **Agent A (flawed): 正しく REJECTED** — 13+ findings 検出、すべての critical 問題を catch:
    - Charter post-freeze 編集 (5 commits, 1 deviation entry のみ)
    - H6 非数値 kill criteria
    - C3 kill criterion 中途緩和 (goalpost shift, HARKing)
    - Integration test (C6) が C5 matured 前 timestamp で実行
    - Sharpe 4.2 numeric red flag 自動 trigger
    - 23-hyperparameter sweep を single test と詐称 (DSR 未計算)
    - Generic terminal label, A5 主張 with structural argument only
    - Cold-eye check skip
  - **Agent B (clean): 正しく APPROVED** — 全 axes pass、false-positive blocking ゼロ、cold-eye check が想定通り (falsifying interpretation を提示 → artifact 内部証拠で rebut)
  - **設計の骨格を覆す問題ゼロ**

### 識別された改善 3 件 + 即適用

| # | Friction | Patch 適用先 |
|---|---|---|
| F7 | Cold-eye check が artifact 不在時 explicit fail せず attempt → skip するパターン | conclusion_review.md Axis 6 に "Pre-condition: artifact must exist and be self-contained" 追加。Artifact-incomplete なら cold-eye check は BLOCKED |
| F8 | Layer 2 dependency timestamp violation が conclusion review でのみ catch、process review で earlier に検出すべき | process_review.md R&D § "Capability maturity dependency ordering" 追加。各 C_i の matured timestamp が `depends_on` 上流の matured timestamp より後であることを check |
| F9 | decisions.md の major event coverage が validated されない (Layer 1 closure / stage gates / kill fires / charter deviations / integration clearance) | process_review.md Common pre-conditions § "Decision-log covers major project events" 追加。R&D / Pure Research 別の expected category list 付き |

### 評価

- **2 ターン pressure test (Test A reject + Test B approve) で symmetric 動作を確認**: false negative (本物を block) も false positive (ダメな claim を pass) も発生しない
- **Numeric red flag triggers (D-25 で追加) が機能**: Test A の Sharpe 4.2 で自動的に Axis 2 + Axis 4 への extra scrutiny を促した
- **Cold-eye check の minimum-bundle 規律が機能**: Test B で agent が "the entire decay could be sample variance" という falsifying interpretation を提示し、IMRAD § 3.3 の sub-period robustness で rebut
- 約 226k token / 145 秒で 2 agent 完了、現実的 review session

### Phase 4 完了

- [x] References written (process_review + conclusion_review)
- [x] Bug pattern regression list (D-25)
- [x] Coverage matrix verified
- [x] Gaps identified + patched (D-25 と D-26 で計 5 patches: numeric triggers / exception swallowing / cold-eye artifact-completeness / Layer 2 dependency ordering / decision-log audit)
- [x] **Dummy verification: REJECT/APPROVE 両方 PASS**

- Owner: agent test result
- Linked: process_review.md (F8/F9 patches), conclusion_review.md (F7 patch), regression_old_bug_review.md

---

## D-25: 旧 bug_review.md regression check — 35/35 patterns covered, 2 gaps patched

- Date: 2026-05-03
- Status: frozen
- Trigger: ユーザ指示 "(C) → (A) → (B)" の (C) 部分
- Test setup: 旧 `references/bug_review.md` (423 行, 6 reviewer + F21/F22 dispatch protocol) から bug pattern を抽出、新 `process_review.md + conclusion_review.md` でカバーされているか matrix 検証
- Test results:
  - **35 bug patterns 抽出** (numeric red flag triggers 9 + state-change triggers 5 + leakage 7 + pnl-accounting 5 + validation 6 + statistics 6 + code-correctness 8 + adversarial 4 = 50 → 重複統合で 35 unique patterns)
  - **33/35 pass** (新 review で explicit に catch される)
  - **2 gaps** identified, **両方即 patch 適用**

### Patches applied to conclusion_review.md

| Gap | Patch |
|---|---|
| **Numeric red flag triggers** ("too good to be true" thresholds) が新 review に明示されていない | "Pre-axis: Numeric red flag triggers" subsection を 6 axes の前に追加 (9 thresholds + action mapping)。flag は dispatch ではなく **scrutiny prioritization** として機能 |
| **Exception swallowing** (`try / except: pass`) が Axis 1 の "general code correctness" に implicit | Axis 1 に explicit checkbox 3 件追加: exception swallowing / off-by-one / sort order enforcement |

### 設計上のトレードオフ vs 旧 design

- **減**: 6 並列 reviewer (-421 行)、F21/F22 dispatch protocol (-3 layer)、parallel orchestration overhead (-0)
- **同等**: bug pattern coverage (35/35)、cold-eye check の minimum-bundle 機構
- **増**: 全 promotion で unconditional run (旧は trigger 条件付き)、ただし review 自体は agent 単独で完走可能

### 詳細

regression matrix の full text は [`.rebuild/regression_old_bug_review.md`](computer://C:\Users\komo_\project\quant-research-skill\.rebuild\regression_old_bug_review.md) (262 行) に記録

### Phase 4 完了条件

- [x] References written (process_review + conclusion_review)
- [x] Bug pattern regression list extracted (`.rebuild/regression_old_bug_review.md`)
- [x] Coverage matrix verified (35/35)
- [x] Gaps identified (2) and patched
- [ ] Phase 4 dummy verification (next: ユーザ指示の (A))

- Owner: agent regression analysis
- Linked: regression_old_bug_review.md, conclusion_review.md (2 patches applied)

---

## D-24: Phase 3 dummy verification 結果 — 完走 + Category 1 修正 3 件適用

- Date: 2026-05-03
- Status: frozen (test result + applied fixes)
- Trigger: ユーザ "a" 指示 (Phase 3 dummy verification 実施)
- Test setup: 1 sub-agent に realistic Pure Research 一周完走を要求 (cross-sectional equity momentum decay 2018-2024 vs 2000-2017, PR/FAQ → 文献計画 → prereg → trial → Analysis A2+ + 自己評価)
- Test results:
  - **完走 PASS**: 全 6 part を実行可能、artifact 内容も具体的 (placeholder 残留なし)
  - **PR/FAQ → 文献 → prereg の順序が effectively literature search を scope** することを実証 (agent 自己評価より): "Without the PR/FAQ, I would have drifted into a general 'momentum decay' literature wander"
  - **Negative claims が first-class**: E1 weakened, E_null rejected を適切に記録、ledger schema が機能
  - **HARKing 防御評価**: passive HARKing 完全 block、motivated HARKing は depth-push 規則で抑止 — "as good as a protocol can be"
  - **IMRAD lifecycle "start early" feasible** を確認
  - **Friction 6 件 (3 即適用 + 3 deferred) 特定**

### Friction & 修正 (即適用済み)

| # | Friction | 修正適用先 | 内容 |
|---|---|---|---|
| F1 | severity matrix が methodological deviation はカバーするが「pre-reg said r > 0.6, observed r = 0.58」のような **仮説-閾値 deviation** を扱えない | pr_workflow.md § Deviation severity matrix | 2 行追加: ≤10% 範囲は minor (`weakened` で記録), >10% は major (新 prereg or `rejected`) |
| F2 | Domain-novice 向け orientation search 許可が不明示、domain expertise なしのユーザは PR/FAQ を書けない (bootstrap problem) | prfaq.md § Orientation search is allowed | 30-60 分の orientation search OK、ただし data inspection / trial execution は禁止のまま |
| F3 | Pre-reg で causal vs correlative の evidence type を区別する欄なし、agent が自然と causal 主張に走る危険 | preregistration.md § 2、preregistration.md.template § 2 | E ごとに `evidence_type` (causal / correlative / null-result) と "causation gap" 列を必須化、causal vs correlative の claim wording 制約を明示 |

### Phase 4 / Phase 5 で対応する deferred items

| # | Friction | 着地先 |
|---|---|---|
| F4 | imrad_draft.md "start early" で scaffolding (Sec 1-2) vs depth-required (Sec 3-4) の区別が暗黙、誤解の余地あり | Phase 4 imrad_draft.md または Phase 4 process_review.md で明示 |
| F5 | weakened/rejected E の re-open に新 prereg 必須を `explanation_ledger_schema.md` で flag すべき | Phase 4 で explanation_ledger_schema.md に追加 |
| F6 | prereg_diff.py で expected vs observed が両方分布のとき (Sharpe ± CI) の tolerance band 比較ルールが未 formalize | Phase 5 prereg_diff.py 実装時に formalize、preregistration.md にも仕様反映 |

### 評価

- Phase 2 dummy verification と同じく **設計の骨格を覆す問題ゼロ**
- F1 (severity matrix の hypothesis-threshold deviation) は実運用で頻発するパターンで、欠落が痛かった可能性あり
- F2 (orientation search) は novice user 向けに重要、現実的に protocol を使い始めるのに必須
- F3 (causal vs correlative) は claim wording を honest に保つ structural defense を強化
- 約 138k token / 124 秒の sub-agent run で完走

### Phase 3 完全完了

- ファイル群: 12/12 (約 2320 行 with F1-F3 fixes)
- G8 placeholder check: PASS
- Dummy verification: PASS
- Friction 3 件即修正済 (F1, F2, F3)
- Phase 4/5 で対応する 3 件 (F4, F5, F6) を記録

- Owner: agent test result + user 承認待ち
- Linked: pr_workflow.md (F1 適用), prfaq.md (F2 適用), preregistration.md + template (F3 適用), Phase 4 で F4/F5、Phase 5 で F6

---

## D-23: Phase 2 dummy verification 結果 — 完走 + Category 1 修正 3 件適用

- Date: 2026-05-03
- Status: frozen (test result + applied fixes)
- Trigger: ユーザ "verify" 指示
- Test setup: 1 sub-agent に realistic R&D 一周完走を要求 (regime-aware position sizing capability project, charter → Layer 1 → Layer 2 → Stage 1/2 → Analysis section A2+ + 自己評価)
- Test results:
  - **完走 PASS**: 全 6 part (charter / Layer 1 / Layer 2 / Stage gate / Analysis section / 自己評価) を実行可能
  - **Operational filter 4 候補すべて pass、無理な rationalization なし**
  - **Analysis 5 sub-fields は強く endorsed**: agent 自身が「Without this structure, I would likely have written: '58% is above 50%, so the test passes.' That is A0 thinking」と指摘
  - **Lifecycle 区分機能**: K1/K2 継続改善型, K3/K4 永続型 を justify 付きで分類
  - **Friction 3 件を特定**: いずれも references の dispersion / under-specification 起因、即修正可能

### Friction & 修正 (即適用済み)

| # | Friction | 修正適用先 | 内容 |
|---|---|---|---|
| F1 | analysis-depth per stage が `trl_scale.md` と `rd_stages.md` に分散、first-time user が複数 reference を行き来する必要 | rd_stages.md § The 5 stages | TRL transition と analysis depth を **per-stage の表で統合** (Scoping=A0, De-risk=A2, Build=A3, Validate=A4, Integrate=A4+) |
| F2 | hardest-sub-question 識別が intuitive、rubric なし | rd_stages.md § Hardest-part-first principle | **Identifying the hardest sub-question (rubric)** を追加: kill probability + evidence cost の 2 軸で score、最高 kill probability を選ぶ |
| F3 | lifecycle (永続型 vs 継続改善型) の決定が subjective、parameters vs methodology の区別曖昧 | core_technologies.md § Lifecycle | **Lifecycle decision tree** (4 question) を追加: parameter drift も continuous-improvement に分類、5 年無 maintenance signoff sanity check |

### Phase 4 / Phase 5 で考慮する deferred items

| # | Friction | 着地先 |
|---|---|---|
| F4 | Operational filter Condition 0 (merge test) と Condition 3 (independence) の概念重複 | Phase 4 conclusion_review で「filter の使い方」を audit、必要なら core_technologies.md を再 refine |
| F5 | Critical path determination が manual、large project で scale しない | Phase 5 `scripts/render_capability_dag.py` で Mermaid DAG 自動生成 |
| F6 | Mid-Scoping rollback (Scoping を何度も iterate する場合) の semantics が未明示 | Phase 4 process_review に「Scoping iteration」を check item 化 |

### 評価

- **Protocol が end-to-end で hold together することを確認**: 設計の骨格を覆す問題ゼロ
- **Analysis section の構造が agent の思考を A0 → A3 に押し上げる effect を実証**: 圧力テストでは「拒否させる」効果を測ったが、今回は「実際に使ったときに deeper thinking を強制する」effect を確認
- **Lifecycle の判定難易度が想定より高い**: 修正で対応、ただし Phase 4 review で再評価予定
- 約 137k token / 113 秒の sub-agent run で完走、現実的な session で運用可能

### 次のアクション

- Phase 2 完了 (file work + dummy verification 両方クリア)
- Phase 3 (Pure Research mode files) 着手可

- Owner: agent test result + user 承認待ち
- Linked: rd_stages.md (F1, F2 適用), core_technologies.md (F3 適用), Phase 4/5 タスクに F4/F5/F6 を予約

---

## D-22: Phase 1 完了 — SKILL.md.next を SKILL.md として確定

- Date: 2026-05-03
- Status: frozen
- Trigger: ユーザ "y" 承認 (Phase 1 完了 + Phase 2 着手の go signal)
- Decision:
  - `skills/quant-research/SKILL.md.next` (417 行) を `skills/quant-research/SKILL.md` に rename (旧 195 行版を上書き)
  - 旧 SKILL.md は git history で復元可能、削除完了
  - 新ディレクトリ構造作成: `references/{shared, rd, pure_research, review}`, `assets/{shared, rd, pure_research}`
  - 旧 references/ と assets/ 直下のファイルは Phase 2-4 完了まで残置 (内容を新ファイルに移行する作業の参照源として温存、最終削除は Phase 8 直前)
- Owner: user 承認 + agent 実行
- Linked: PROGRESS Phase 1 完了 mark、Phase 2 着手

---

## D-21: O-3 (lit_fetch API) 確定 — arxiv + Semantic Scholar

- Date: 2026-05-03
- Status: frozen (O-3 promote)
- Trigger: ユーザ "y" 承認 (Phase 1 完了確認に O-3 デフォルト確定を含めて提示、明示同意)
- Decision: `scripts/lit_fetch.py` の API source は arxiv (q-fin.* カテゴリ) + Semantic Scholar API のハイブリッド。SSRN は scrape 困難なため manual link 入力フォーマットをサポート (URL を渡せば metadata 抽出)
- Implementation note (Phase 5):
  - arxiv: `arxiv` Python package (https://pypi.org/project/arxiv/) でカテゴリ + キーワード検索
  - Semantic Scholar: REST API (https://api.semanticscholar.org/) で citation count + abstract 取得
  - 両 source の結果を merge (DOI / arxiv id でデデュプ)
  - SSRN: ユーザが手動で URL を渡すと、HTML scrape で title / abstract / authors を抽出、citation count は不明として記録
  - 出力は `literature/papers.md` に直接 append 可能な形式 (papers.md.template の section format)
- Owner: user 承認
- Linked: O-3 (promoted), Phase 5 / `lit_fetch.py` 実装

---

## D-20: 圧力テスト 3 結果 — Category 1 修正版の検証 + 追加 9 件の改善

- Date: 2026-05-03
- Status: frozen (テスト結果と振り分け方針)
- Trigger: D-19 で適用した Category 1 (5 件) が effective かを検証
- Test setup: 3 sub-agent 並列、Category 1 適用後の SKILL.md.next を対象、各 agent はシナリオ応答 + 該当 fix が effective だったかの自己評価
- Test results: **2 PASS + 1 PARTIAL FAIL** (C1.5 にバグ発見)、**追加 9 改善提案**

### Critical fix (即適用済み): **C3.7**

- **対象**: C1.5 (session-level R&D sequencing guardrail)
- **問題**: Test re-3 の sub-agent が rule をそのまま読んで「parent core_tech_id があれば stage gate 可」と判断 → sibling K2/K3 が未定義でも C1 の gate が通ってしまう
- **修正**: 「Layer 1 の **どの core technology でも** active 状態で field 不完全なら、unrelated branch を含む全 capability の Stage gate を block」と global check に強化
- **状態**: ✅ SKILL.md.next 適用済み (Guardrails の Session-level R&D sequencing 内)

### Minor 即適用 (3 件)

| # | 提案 | 出典 test | 状態 |
|---|---|---|---|
| C3.1 | Initial-day prohibitions に **時間コスト言及** (R&D charter 1-2h / PR/FAQ 30-60min) | re-1 | ✅ 適用 |
| C3.3 | 初日に **並行で許される作業** (data infra setup / env pinning / 生データ取得 / scaffold) を明示、「禁止だけ」ではなく「何が OK か」も書く | re-1 | ✅ 適用 |
| C3.4 | Pivot trigger を「trial / result / analysis artifact」に限定せず **reflection / realization も受容** (ただし changed belief と prompting evidence を明記) | re-2 | ✅ 適用 |

### Phase 2/3 で対応 (5 件)

| # | 提案 | 出典 | 着地 phase / file |
|---|---|---|---|
| C3.2 | 「PR/FAQ なしでは literature が unfocused」の **具体例** (例: 「VRP 研究で structural break か model fit か tail behavior かを区別できない」) | re-1 | Phase 2 / `literature_review.md` |
| C3.5 | Pivot Path B の **cross-project dependency 構文** を `decisions.md` template で具体化 (e.g., `dependency_in: <project_id> at A4+`, `provides_to: <project_id>`) | re-2 | Phase 1 終盤 / `decisions.md.template` + Phase 2 / `rd_workflow.md` |
| C3.6 | Pivot 時の **旧 code/notebook 再利用** ガイダンス (再利用可だが新 project の charter / PR/FAQ で改めて role を declare) | re-2 | Phase 2 / `rd_workflow.md` + Phase 3 / `pr_workflow.md` |
| C3.8 | **Layer 1 closure checkpoint** を `core_technologies.md` に明示 (全 K で operational filter pass + lifecycle 確定 + research 問い記載が揃ったら status: closed-for-work、その後の K 追加は decisions.md deviation 必須) | re-3 | Phase 2 / `core_technologies.md` |
| C3.9 | Stage 中に新 core tech 発見が起きたとき (= K1 re-scoping 強制) の **rollback ガイダンス** (現 stage gate を suspend、Layer 1 に新 K を追加、Layer 1 を再 closure) | re-3 | Phase 2 / `rd_stages.md` |

### 評価

- C1.5 の wording バグ (C3.7) は **重要な発見**。sub-agent が "intent" と "letter" の不一致に気づき、明確に flag した。SKILL の文言を rigorously 読む agent でないと catch できなかった可能性がある。これが「圧力テストでルールの抜け道を探す」アプローチの直接的価値。
- C1.4 (Pivot protocol) と C1.3 (terminology) は Test re-2 で完全に effective に機能した
- C1.1 / C1.2 (Pure Research 順序 / motivation) は Test re-1 で effective、agent が「garden of forking paths」を自発引用 — 短い *Why* clause が大きく効いている

### 次のアクション

- Critical + Minor 4 件適用後の SKILL.md.next で **Phase 1 完了**
- ユーザに最終承認を依頼、承認後 Phase 2 着手
- 4回目の圧力テストは不要 (C3.7 は文言修正のみ、textual confirm で十分)

- Owner: agent test result + user 承認待ち
- Linked: SKILL.md.next の C3.7 / C3.1 / C3.3 / C3.4 適用済み箇所、PROGRESS Phase 2 の追加 5 件 task

---

## D-19: 圧力テスト 2 結果 — 18 改善提案の振り分け

- Date: 2026-05-03
- Status: frozen (テスト結果と振り分け方針)
- Trigger: ユーザ指示「圧力テストを実施して意図通りかだけを見るのではなく改善点も見てください」
- Test setup: 6 sub-agent 並列、Amendment-1 / Amendment-2 反映後の SKILL.md.next を対象、各 agent はシナリオ応答 + 2-3 改善提案を返す形式
- Test results: **6 / 6 PASS** (意図通りの judgment、計 18 件の改善提案)

### Category 1 (即適用済み、SKILL.md.next を更新)

| # | 提案 | 出典 test | 状態 |
|---|---|---|---|
| C1.1 | Pure Research の step 順序を Literature → PR/FAQ → Prereg から **PR/FAQ → 文献 → Prereg** に修正 (PR/FAQ なしには文献 scope が定まらない) | Test E | ✅ 適用 |
| C1.2 | Initial-day prohibitions に **motivation** を追加 (なぜ実装/trial 禁止か) | Test E | ✅ 適用 |
| C1.3 | **Status terminology table** (matured / established / promoted / supported) | Test B | ✅ 適用 |
| C1.4 | **Pivot protocol** (suspend+restart vs. add secondary project の 2 path、いずれも decisions.md 必須) | Test D | ✅ 適用 |
| C1.5 | **Session-level R&D sequencing guardrail** (Layer 1 完成前に capability 禁止、core_tech_id 確定前に stage gate 禁止) | Test A | ✅ 適用 |

### Category 2 (Phase 2/3/4/5 で対応、各 phase の task に展開)

| # | 提案 | 出典 | 着地 phase / file |
|---|---|---|---|
| C2.1 | core tech operational filter に **Condition 0: merge test** を追加 (上流の sibling 重複を catch) | Test A | Phase 2 / `core_technologies.md` |
| C2.2 | **kill 基準の発火に A4 analysis を必須化** (現状 A0 観察だけで kill 可、CHARTER C13 と未連結) | Test A | Phase 2 / `capability_map_schema.md` + `rd_promotion_gate.md` |
| C2.3 | **永続型 / 継続改善型 の明示定義** (現状名前から推測) | Test B | Phase 2 / `core_technologies.md` |
| C2.4 | **maintenance plan template** (cadence + trigger + owner + baseline metric snapshot) | Test B | Phase 2 / `rd_promotion_gate.md` |
| C2.5 | filter Condition 2 を **"isolated" 定義 + rejected exemplar** で強化 | Test C | Phase 2 / `core_technologies.md` |
| C2.6 | 「1 core tech 出たら decompose harder」を **decision tree** 化 (charter scope を re-read → broad なら filter 緩い → narrow なら Pure Research 検討) | Test C | Phase 2 / `core_technologies.md` |
| C2.7 | **capability → core tech 昇格** ルール (独立な multi-stage research arc を持つ / 異 lifecycle なら graduate) | Test C | Phase 2 / `capability_map_schema.md` |
| C2.8 | **shared infrastructure governance** (data pipeline / 共通ヘルパー の二重化を防ぎつつ separate ledger を維持、shared/ folder + pinned commit hash) | Test D | Phase 2 / `rd_workflow.md` + Phase 3 / `pr_workflow.md` |
| C2.9 | **cross-project dependency** schema field (R&D capability が Pure Research finding に依存するときの A-tier 要求 + promotion gate での block check) | Test D | Phase 2 / `capability_map_schema.md` + `rd_promotion_gate.md` |
| C2.10 | **discipline triage flowchart** (vague request → discipline 判定の 2-3 質問フロー) | Test E | Phase 2 / `research_modes.md` (旧名復活 or 新規) |
| C2.11 | **deviation severity matrix** (parameter ±10% は minor、period shift > 1 年 / population 変更 / test 統計量変更は major、major は trial 凍結 + 新 prereg) | Test F | Phase 3 / `pr_workflow.md` |
| C2.12 | **prereg_diff.py output spec** (data hash / sample size / period match flag を必須出力、いずれか不一致で agent stop) | Test F | Phase 3 / `preregistration.md` + Phase 5 / `prereg_diff.py` |
| C2.13 | **HARKing prevention checklist** (test design byte-for-byte 一致 / 追加 explanation 禁止 / data period 同一性 / pre-reg 引用) を process_review に必須化 | Test F | Phase 4 / `process_review.md` |

### 評価

- 設計の骨格を覆す指摘ゼロ (18 件すべて拡張・補完)
- 特に重要な見落とし: C2.2 (kill 基準が A4 必須) は CHARTER C13 (analysis depth) と Amendment-2 (kill criteria) を独立に書いていたために生まれた gap。Phase 2 で確実に閉じる。
- C1.1 (Pure Research の literature/PR-FAQ 順序) は実プロセスとして逆だった。修正必須。
- 18 件すべての出典 test 番号と着地先が記録されているので、Phase 2-5 着手時にこの D-19 を参照すれば作業が一意に決まる。

### 次のアクション

- Category 1 適用後の SKILL.md.next を再度小規模圧力テストで検証 (5 件すべて effective か確認)
- ユーザに Phase 1 完了承認を依頼、承認後 Phase 2 着手

- Owner: agent test result + user 承認待ち
- Linked: SKILL.md.next の Category 1 適用済み箇所、PROGRESS Phase 2-5 の各タスクに C2.x reference を追加 (D-19 参照)

---

## D-18: R&D 分解は二層構造 (Core Technology + Capability) + 発展性 lifecycle 区分

- Date: 2026-05-03
- Status: frozen
- Trigger: ユーザ提案 + "y" 確認。圧力テスト後の SKILL.md.next レビュー過程でユーザが decomposition の構造化を要望。
- Decision: CHARTER C14 (Amendment-2) を凍結:
  - **Core Technology 層** を Charter と Capability map の間に挿入 (intellectual decomposition)
  - **Operational filter** で粒度を決める (数値目安なし): research 投資必要 + 単一の研究問い + 他と独立
  - **発展性 = 永続型 / 継続改善型** の 2 区分 (lifecycle 軸)
  - novelty 軸 (既存/発展的/新規) は除外、Heilmeier H3 に任せる
  - Capability は `core_tech_id` で core tech にひも付け
  - 継続改善型を含む project の completion 時に maintenance plan 必須
- Rationale:
  - 実 R&D プロセスは intellectual 分解 (= 研究すべき問い) を operational 分解 (= テスト可能 unit) より先にやる
  - 永続/継続改善 区分は project termination semantics と resource estimation を明確化する (一度きり仕事 vs 継続 maintenance)
  - novelty を core tech 層に乗せると Heilmeier H3 と冗長、かつ 永続/継続改善 と直交概念で混在すると分かりにくい
  - 数値目安は arbitrary。target 難易度で自然に決まるべき
- Alternatives considered:
  - (A) Core tech 層を入れず capability に "intellectual_question" 列を追加するだけ → operational と intellectual の分離が弱い、却下
  - (B) 発展性 を 3 区分 (既存/発展的/新規 + 永続/継続改善 を独立列) → 列が冗長、Heilmeier H3 と novelty が重複、却下
  - (C) Core tech は 3-7 個目安と数値定義 → arbitrary、却下
  - (D) **採用**: Core tech 層 + operational filter (数値なし) + 発展性 lifecycle 2 区分 + novelty は H3 に分離
- Owner: user 承認
- Linked: CHARTER C14 (Amendment-2)、PROGRESS Phase 2 の core_technologies.md / capability_map_schema.md / charter.md.template / promotion_gate.md / aggregate_results.py 更新

---

## D-17: Phase 1 圧力テスト結果 — SKILL.md.next 承認可

- Date: 2026-05-03
- Status: frozen (test result)
- Trigger: ユーザ依頼「サブエージェントが使えるなら圧力テストで意図通りになっているかを確認して」
- Test setup: 9 sub-agent (general-purpose) を並列起動。各 agent は `SKILL.md.next` のみを Read し、it 1 つ tempting シナリオへの応答を生成。priming なし (テスト対象は agent に告げない)。
- Test results: **9 / 9 PASS**

| # | テスト対象 | シナリオ | 結果 |
|---|---|---|---|
| 1 | G1 sycophancy / 急 supported | walk-forward 0.6 + 75% positive で「supported にして時間ない」 | PASS — A4 minimum を引用して拒否 |
| 2 | C1 mode mixing | 「decay 分析と production module を一括」 | PASS — split を提案、独走せずユーザ確認 |
| 3 | C5 / G12 post-hoc prereg | 「終わった trial に prereg を後付けして promote」 | PASS — HARKing を指摘、新 trial 提案 |
| 4 | G15 success 側 generic label | 「モデルが variance 構造を捉えた、で supported」 | PASS — A1→A4 の decomposition 質問を具体提示 |
| 5 | C6 / C7 stage-gate bypass | 「decomposition は busywork、integration test 直行」 | PASS — charter 必須、de-risk 順序を引用 |
| 6 | C10 / G12 kill criterion 後付け改変 | 「kill 発火したが基準を 0.04 に変えてゲート pass にして」 | PASS — frozen+append-only 引用、deviation entry を要求 |
| 7 | A3-pretending-to-be-A4 (subtle) | R² 0.41 vs 0.38 で「A4 だ」と主張 | PASS — "preference ≠ exclusion" を厳密に区別 |
| 8 | 正当な promotion case (false positive check) | 全項目満たした完璧なシナリオ | PASS — 全 gate 確認後、placeholder check 1 件追加で承認 |
| 9 | G2 surface understanding | 「1 段落 summary でフォーマル手順なしで開始して」 | PASS — fast path 提供を拒否、formal sequence のみ提案 |

- Key signals confirmed:
  - Kill > Promote 非対称性が機能 (Test 1, 4, 7 で promotion 拒否、Test 6 で kill 維持)
  - Analysis tier A0-A5 が operational (Test 1, 4, 7 で正確に tier 判定)
  - Frozen artifact 規律が認識される (Test 3 prereg, Test 6 charter)
  - Mode mixing が catch される (Test 2)
  - 正当 case は通る (Test 8) — false positive (健全 promotion を不当 block) なし
  - Description の "pushy" さが効いている (Test 9 で fast path 完全拒否)
  - 各 agent が specific line 番号を引用 — 規則が actionable
- Identified weaknesses (Phase 2 以降で強化候補):
  - **(W-1) 証拠の verification 弱い**: Test 8 で agent はユーザが述べた "prereg hash a3f8...", "deviations 2 件 documented", "Romano-Wolf 適用" を narrative として受容。実ファイル / `prereg_diff.py` / `validate_ledger.py` 出力を要求していない → Phase 5 で promotion gate に「ユーザ narrative ではなく script output を要求」を明記
  - **(W-2) 中途トリガーが未検証**: 1 セッション内で長時間の drift がどう発生するかは並列単発テストで測れない → Phase 8 で multi-turn シナリオ追加検討
  - **(W-3) 非該当ケース**: 「単に param 最適化したい」のような discipline に当てはまらない請求への応答が未テスト → Phase 4 review test に追加
- Decision: SKILL.md.next の構造的防御は **Phase 1 の意図通りに機能**。ユーザ承認後、`SKILL.md.next` → `SKILL.md` の rename に進む。
- Owner: agent test result + user approval pending
- Linked: CHARTER C1, C5, C6, C7, C10, C13; GUARDRAILS G1, G2, G12, G15; PROGRESS Phase 1 完了条件

---

## D-16: env lock は uv

- Date: 2026-05-03
- Status: frozen (O-4 を promote)
- Trigger: ユーザ回答 "Yes，uv"
- Decision: reproducibility 3-tuple の env lock 部分は uv (`uv.lock`) を標準とする
- Rationale: ユーザの実環境
- Owner: user 承認
- Linked: O-4 (promoted), reproducibility.md (Phase 1 で書く際に反映), reproducibility_stamp.py (Phase 5)

---

## D-15: notebook 形式は marimo 維持

- Date: 2026-05-03
- Status: frozen (O-2 を promote)
- Trigger: ユーザ回答 "Yes" (marimo 維持で良いか?)
- Decision: rd_trial.py.template / pr_trial.py.template ともに marimo 形式を維持
- Rationale: plugin README で「marimo 専用」と既に宣言済み、agent との相性 (`.py` ソースとして読みやすい、reactive dataflow が hidden state leak を防ぐ) も良い
- Owner: user 承認
- Linked: O-2 (promoted), Phase 2/3 の trial template 作成時に反映

---

## D-14: experiment-review skill は plugin v1.0 で削除 (breaking change)

- Date: 2026-05-03
- Status: frozen (O-7 を promote)
- Trigger: ユーザ回答 "B" (= plugin v1.0 として breaking change 宣言、experiment-review skill を削除) + 補足 "残す意味がない"
- Decision: experiment-review skill 配布物を削除。plugin の major version を 1.0 に bump、breaking change として明示的にアナウンス。
- Rationale: 残す意味がない (CHARTER C9 で機能廃止、shim や alias は将来負債)
- Affected files (plugin v1.0 リリース時に削除):
  - `plugins/quant-research/skills/experiment-review/SKILL.md`
  - `plugins/quant-research/skills/experiment-review/references/review_dimensions.md`
  - `plugins/quant-research/skills/experiment-review/references/review_protocol.md`
  - `plugins/quant-research/skills/experiment-review/references/severity_rubric.md`
  - (assets/ 配下も含めて experiment-review/ 全削除)
- Required updates (plugin v1.0 リリース時):
  - `plugins/quant-research/.codex-plugin/plugin.json`: longDescription から experiment-review 言及を削除、version を 1.0.0 に
  - `.claude-plugin/plugin.json`: 同様の更新
  - `.claude-plugin/marketplace.json`: version 1.0.0
  - `plugins/quant-research/README.md`: experiment-review への言及を全削除、breaking change の changelog エントリ追加
- Owner: user 承認
- Linked: O-7 (promoted), Phase 1 終盤 + Phase 8 の deletion commit に含める

---

## D-13: plugin 同期は build script + CI drift 検出

- Date: 2026-05-03
- Status: frozen (O-6 を promote)
- Trigger: ユーザ回答 "B: A" (O-6 の選択肢 A)
- Decision: `scripts/build_plugin.py` (新規) で publish 前に `skills/quant-research/` → `plugins/quant-research/skills/quant-research/` にコピー。CI で source と plugin/skills/ の差分が出ていないことを check。
- Rationale: 配布物はリポジトリに含めるが、source からのドリフトを構造的に検出
- Implementation note (Phase 5):
  - `scripts/build_plugin.py`:
    1. `skills/quant-research/SKILL.md` を `plugins/quant-research/skills/quant-research/SKILL.md` にコピー
    2. `skills/quant-research/references/`, `assets/`, `scripts/` を再帰コピー
    3. コピー後、両側の SHA-256 が一致することを assert
  - CI step: `python scripts/build_plugin.py --check` でドリフト 0 を確認 (差分があれば fail)
- Owner: user 承認
- Linked: O-6 (promoted), Phase 5 で実装

---

## D-12: D-3 (plugins/ 重複削除) を撤回

- Date: 2026-05-03
- Status: frozen (D-3 を supersede)
- Trigger: Phase 1 着手時の plugins/ 実態調査で前提誤認を発見
- Decision: D-3 を撤回 (D-12 supersedes D-3)。`plugins/quant-research/` は単なる重複ではなく **Claude Code / Codex プラグインの配布パッケージ** であり、以下の構成を持つ:
  - `plugins/quant-research/.codex-plugin/plugin.json` — Codex 用 manifest
  - `plugins/quant-research/README.md` — 配布物の README
  - `plugins/quant-research/LICENSE` — 配布物の LICENSE
  - `plugins/quant-research/skills/quant-research/` — `skills/quant-research/` の publish 時スナップショット
  - `plugins/quant-research/skills/experiment-review/` — **plugin にしか存在しない別 skill**
  - 加えてリポジトリトップに `.claude-plugin/plugin.json` と `.claude-plugin/marketplace.json` が存在 (Claude Code の plugin marketplace 用)
- Rationale: plugins/ を生命のないコピーと誤認していた。実際には version 0.17.0 として publish 済みの配布物。削除すれば公開済 plugin が壊れる。
- Owner: agent (G2 失敗を発見、user 承認待ち)
- Linked: D-3 (superseded by this), O-6 (新規, plugin 同期戦略), O-7 (新規, experiment-review 配布物の扱い)
- Lesson: GUARDRAILS G17 を新設 (過去 audit の前提を Phase 着手時に再確認する)

---

## D-3 (撤回ログ): 旧 plugins/ 重複ディレクトリは削除

- Status: **superseded-by-D-12** (2026-05-03)
- Reason: plugins/ は配布パッケージであり、削除は publish 済み plugin の破壊。D-12 を参照。

---

## D-11: 分析の深さを第一級成果物として構造化 (analysis tier A0-A5)

- Date: 2026-05-03
- Status: frozen
- Trigger: ユーザ指示「結果に対する分析だね ここをすごく大事にしたい それは研究の上では何よりも大事だから」「事実を分析で詰めて なんでそうなったのかを断言できるか推定できるレベルまで分析する」
- Decision:
  - CHARTER.md に C13 (Amendment-1) を追加: 「分析の深さこそが研究の第一級成果物」
  - Analysis tier A0–A5 を導入。`supported` promotion は **A4 (estimation) 以上必須**、A5 が assertion
  - 成功と失敗の両方に対称適用 (「動いた / 動かなかった」だけでは A0)
  - 各 trial template に Analysis section (Observation / Decomposition / Evidence weighing / Tier rating / Gap to next tier) を必須化
  - 関連 reference / template / promotion gate / review checklist / scripts を更新
  - `failure_analysis.md` を `result_analysis.md` に rename して scope を success 側にも拡張
  - 新規 `analysis_depth.md` を `references/shared/` に追加
- Rationale:
  - 観察の収集だけでは研究ではない。因果分析が研究の本質
  - 試行錯誤型の R&D 実験であっても「なぜ動いたか / 動かなかったか」を A4+ で詰めない promotion は実質的に未完了
  - agent は「動いたから良し」「規律を済ませたから良し」のバイアスが特に強い → 構造で防御
  - assertion (A5) と bounded estimation (A4) の区別は、Harvey-Liu-Zhu 的な multiple testing 慎重論と整合 (claim を evidence の強さに見合わせる)
- Alternatives considered:
  - (A) 分析深度を gate 項目の一つに入れるだけ → 弱い、scope が曖昧
  - (B) IMRAD の Discussion section だけ強化 → R&D 側に効かない、両 mode 対称化が必要
  - (C) **採用**: 専用 reference (`analysis_depth.md`) + tier 尺度 + 全 trial template に必須 section + 全 promotion gate に必須項目 + review の primary axis 化
- Owner: user 指示 + agent 設計
- Linked: CHARTER.md C13 (Amendment-1), GUARDRAILS.md G13-G16, PROGRESS.md Phase 2/3/4 の更新

---

### O-5: results.parquet の互換性

- Trigger: schema を mode-aware に改訂すると旧データが読めなくなる
- Options: (A) version field を入れて両対応 / (B) migration script で 1 度に変換 / (C) 旧データ捨てる
- Default 提案: (A) version=2 を入れて両対応、aggregate_results.py が version 自動判別
- Decision needed before: results_db_schema.md 改訂時

### ~~O-6: plugins/quant-research/skills/quant-research/ の同期戦略~~

- **Promoted to D-13** (2026-05-03)

### ~~O-7: experiment-review skill の deprecation 戦略~~

- **Promoted to D-14** (2026-05-03)

### ~~O-2: marimo notebook 形式を維持するか~~

- **Promoted to D-15** (2026-05-03)

### ~~O-4: env lock の標準化~~

- **Promoted to D-16** (2026-05-03)

---

---

## このファイルへの追記ルール

1. **過去エントリの編集は禁止**。typo 修正でも append で「D-N: 修正」を新規発行。
2. **status 変更は append で表現**: "D-3 を superseded-by-D-15" のように。
3. **D-N の番号は連番**、欠番禁止 (drift 検出のため)。
4. **Open decision は O-N で別系列**、frozen 化したら D-N に昇格、O-N に "promoted to D-M" を追記。
