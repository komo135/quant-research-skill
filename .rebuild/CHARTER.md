# CHARTER — quant-research skill rebuild

**Status**: frozen
**Last frozen**: 2026-05-03
**Frozen by**: ユーザ承認 ("おおむねいい" + "途中でやることや意図が変わらないように")

このファイルは **再構成プロジェクトの設計意図** を凍結する。
書き換え禁止。修正は本ファイル末尾の "Amendments" にユーザ承認付きで append する。

---

## DARPA Heilmeier Catechism for this rebuild

### H1. What capability should exist? (no jargon)

「定量金融研究のために agent が, **R&D (技術確立) と Pure Research (知識獲得) という二つの規律を独立に駆動でき**, 各規律の自然な deliverable (R&D = TRL-6 demonstrated capability, Pure Research = IMRAD-shaped manuscript draft) まで agent 単独で到達できる skill」

### H2. How is this approximated today, and what are the limits?

現状のスキルは:
- R&D と Pure Research が「同じ ledger を共有する 2 モード」として実装されている (research_state.md 内に 4 セクション併存)
- レビューが 423 行の bug_review.md + 6 reviewer 並列 dispatch + 外部 experiment-review skill の三層で重い
- 数値ヘルパーの引用と実装が乖離 (psr_dsr の per-period 混乱、bootstrap の Politis-Romano 誤引用、walk_forward の名前と実装の乖離など)
- agent の構造的弱点 (sycophancy, 事後合理化, anchoring) に対する構造的防御が弱い

限界:
- R&D 側に「kill 基準を入口で書く」(Google X 流) 規律がない → 楽観バイアスが構造で抑制されない
- Pure Research 側に「事前登録」(AEA 流) がない → p-hacking が構造で防げない
- 完了形態 (deliverable shape) が "supported" という曖昧フラグになっており、論文ドラフト・運用引き渡し可能 prototype といった具体に落ちない

### H3. What is new in the proposed approach, and why might it work?

5 つの実証された業界実践を **agent 用に圧縮して埋め込む**:

| 業界実践 | 出典 | この skill での役割 |
|---|---|---|
| Heilmeier Catechism (8 Q) | DARPA, 1970s | R&D 入口 charter |
| Cooper Stage-Gate | Cooper, 1980s | R&D capability 進行管理 (5 stage + Go/Kill gate) |
| NASA TRL | NASA, 1989 | R&D capability の maturity 尺度 (TRL-6 = promotion line) |
| Amazon Working Backwards (PR/FAQ) | Amazon, 2004 | Pure Research 入口 |
| AEA Pre-Analysis Plan | AEA, 2018 | Pure Research の p-hacking 防止 (hash-locked) |
| IMRAD | 19世紀末 | Pure Research deliverable 形式 |

agent 特化の追加:
- すべての凍結 (charter, pre-reg, kill criteria) を **SHA-256 hash-lock + timestamp** で構造的に改ざん不可に
- 完了判定を「checkbox 全 pass + 具体 evidence 引用」必須に。"全体的に OK" 表現禁止
- review skill を **process review (進め方) + conclusion review (結論)** の 2 軸 ~100 行ずつにスリム化、6 並列 reviewer 廃止

### H4. Who cares? Who is the consumer, and what decision does this capability serve?

**Consumer**: ユーザ (komo) が、AI agent (Claude / 他) に定量金融研究を委託または共同で進めるとき。

**Decision served**:
- (R&D) ある定量技術 (新しい validation 手法、新しい signal pipeline、新しい execution model 等) を確立してよいか / 捨てるか / 留保するか
- (Pure Research) ある現象 (anomaly の decay、regime dependence、market mechanism 等) について promotion 可能な claim が立つか / 立たないか / 何が足りないか

このスキルがないと: agent は楽観的に "supported" を出して promotion し、本番投入で破綻する (replication crisis 寄与モデル)。

### H5. If we succeed, what changes downstream?

- agent の出力する研究結果が **business decision に投入できる品質** になる (kill 基準を通過した R&D capability、pre-registration 通過した Pure Research claim)
- ユーザが過去研究を **横断 query** できる (results.parquet が mode-aware schema、IMRAD draft が deliverable として残る)
- 別の agent / 人間がプロジェクトを **継承可能** になる (ledger + decisions + reproducibility 3-tuple で再現できる)
- agent の "楽観・短絡" バイアスを **構造で防御** したパターンの再利用可能例になる

### H6. What are the dominant risks, and what evidence would kill this rebuild?

**Risk-1**: skill が重くなりすぎて agent が起動しない / 守れない。
**Kill evidence**: 実プロジェクトで skill を起動した agent が、`SKILL.md` を読んだ後に mode 選択を間違える / 規律を省略する事例が連続 3 回。

**Risk-2**: pre-registration 強制が個人研究の負担として大きすぎ、結果的に skill を使われなくなる。
**Kill evidence**: ユーザ自身が「prereg を skip したい」と申告 → スキル設計が現実と乖離している証拠。緩和ルートを検討。

**Risk-3**: review skill が薄すぎて、bug を見逃す。
**Kill evidence**: 旧 bug_review が catch していた既知 bug pattern を新 review が catch しない (regression test で検出)。

**Risk-4**: 数値ヘルパーの修正で旧 API が壊れ、既存 notebook が動かなくなる。
**Kill evidence**: 既存 notebook の breakage が連鎖し、ユーザが旧版に戻すことを選択。

**Risk-5**: agent が CHARTER を読まずに drift する (このリスクが本ディレクトリ存在の理由)。
**Kill evidence**: CHARTER に反する変更が DECISIONS への記録なく入る。

### H7. Cost: budget for this rebuild

- 文書執筆: ~10 日 (SKILL.md + references + assets templates)
- スクリプト実装: ~6 日 (新規ヘルパー + 既存ヘルパーの監査修正)
- eval / regression test: ~2 日

合計目安: 約 18 日相当 (agent 駆動なら数セッションで圧縮可能)

### H8. Midterm exam (capability_v0) and final exam (operational capability)

**Midterm**: SKILL.md + R&D charter + Pure Research PR/FAQ + Pre-registration + 各 promotion gate の最初版が揃い、**dummy project** で R&D 1 capability と Pure Research 1 trial を完走できる。

**Final**: 既存の audit 指摘 (psr_dsr / bootstrap / walk_forward / cpcv / pbo / vol_targeted / multiple_testing / plugins重複) を全て解消した上で、**実プロジェクト** で agent が単独で R&D capability を 1 つ promote、Pure Research trial を 1 つ paper draft まで持っていける。

---

## 設計の中核命題 (frozen, 再交渉禁止)

以下はユーザ承認済みの中核命題。これに反する変更は CHARTER 違反:

### C1. R&D と Pure Research は別ディシプリン

「同じプロトコルの中の 2 モード」ではなく、**入口・進行・状態オブジェクト・promotion 条件・deliverable のすべてが違う 2 つの規律**。skill は入口で片方を選び、その規律のみを駆動する。混合は禁止、混合プロジェクトは split する。

### C2. R&D の主役は capability_map.md

`research_state.md` の 1 セクションから **第一級 ledger に昇格**。R&D ではこの 1 ファイルが状態のすべて。`hypotheses.md` は R&D で消滅 (R&D の "次の一手" = capability の TRL を上げる test そのもの)。

各 capability 行は **kill_criteria を必須フィールド** とする (Google X moonshot 原則)。

### C3. Pure Research の主役は explanation_ledger.md

`research_state.md` の 2 セクションを統合。`hypotheses.md` は Pure Research でも消滅 (Pure Research の "次の一手" = explanation pair を識別する trial そのもの)。

### C4. R&D 入口は Heilmeier Catechism Charter

8 質問の 1 ページ document を `charter.md` として書かない限り、capability decomposition に進めない。

### C5. Pure Research 入口は PR/FAQ + Pre-registration

PR/FAQ (Amazon 流) で deliverable を先に書く。**書けない = 質問が熟していない = trial 禁止**。

Pre-registration を SHA-256 hash + timestamp で凍結し、trial 後に actual との diff を機械的に取る。**事後改ざん構造的に不可能**。

### C6. Stage-Gate (5 stage + 5 Gate) を R&D capability ごとに適用

Scoping → De-risk (hardest part first) → Build → Validate → Integrate。各 gate は Go/Kill 二択。

### C7. Promotion line は NASA TRL-6 (operational prototype)

R&D の promotion 判定ライン。TRL-7 以降は engineering hand-off で skill 範囲外。

### C8. Pure Research deliverable は IMRAD ドラフト

「supported」という曖昧フラグではなく、**論文形式の draft が書ける状態** が完了の真の定義。`imrad_draft.md` を出口必須化。

### C9. レビューは Process / Conclusion の 2 軸 + 各 ~100 行

旧 bug_review.md (423 行) + 6 reviewer 並列 dispatch + 外部 experiment-review の三層は **全廃**。Process review (進め方の質) と Conclusion review (結論の妥当性) の 2 ファイルに圧縮。adversarial cold-eye check は conclusion_review の最終 section に embed。

### C10. Kill > Promote の非対称バイアス

kill 基準は 1 項目 fire で kill 確定。promote は全項目 pass 必須。agent の楽観バイアスを構造で打ち消す。

### C11. 完了判定は「checkbox 全 pass + 具体 evidence 引用」必須

"全体的に OK" / "おおむね pass" のような summary 表現禁止。各項目に file:line, hash, metric value のいずれかの具体 evidence を書く。

### C12. agent 特化の補強

- 並列文献調査 (`scripts/lit_fetch.py`)
- ledger linting (`scripts/validate_ledger.py`)
- 凍結 (charter / prereg) は SHA-256 hash-locked
- 再現性 3-tuple (data hash + git commit + env lock) を trial 単位で stamp
- IMRAD draft 自動生成 (`scripts/draft_imrad.py`)
- Heilmeier 質問の対話的 inquiry (`scripts/charter_interview.py`)

これらは **agent が得意な領域を最大化** する道具。人間が苦手で agent が得意なところを構造化する。

---

## ファイル構成 (frozen, 詳細は最終提案メッセージ参照)

```
SKILL.md (~120 行)
references/
  shared/   (failure_analysis, literature_review, sanity_checks, time_series_validation,
             psr_dsr_formulas, multiple_testing[新], reproducibility[新], modeling_approach,
             feature_construction, model_diagnostics, prediction_to_decision,
             portfolio_construction, exit_strategy_design, results_db_schema)
  rd/       (rd_charter[新], capability_map_schema, trl_scale, rd_stages[新],
             rd_workflow, rd_promotion_gate)
  pure_research/  (prfaq[新], preregistration[新], explanation_ledger_schema,
                   pr_workflow, imrad_draft[新], pr_promotion_gate)
  review/   (process_review, conclusion_review)
assets/     (shared / rd / pure_research の各 template)
scripts/    (前回提案の 24 ファイル)
```

---

## ユーザ "確認したい論点" 7 件への扱い

ユーザは前メッセージで「おおむねいい」と回答しただけで個別 7 件には答えていないが、**承認のシグナル + 即実装フェーズへの移行指示** から、以下のデフォルトを採用する。実装中にユーザから明示的に異論があれば再検討:

| Q | デフォルト採用 |
|---|---|
| Q1 R&D 入口を Heilmeier 8 Q Charter に | ✅ 採用 |
| Q2 Pure Research で PR/FAQ + Prereg 必須化 | ✅ 採用 (緩和オプション無し、ただし Q7 で論文化レベルは選択可) |
| Q3 Stage-Gate 5 stages + 5 gates | ✅ 採用 |
| Q4 Review を Process/Conclusion 2 軸に圧縮、6 並列廃止 | ✅ 採用 |
| Q5 Kill > Promote の非対称バイアス | ✅ 採用 |
| Q6 references/ の 3 階層分割 (`shared/`, `rd/`, `pure_research/`, `review/`) | ✅ 採用 |
| Q7 IMRAD ドラフトの強度 | ✅ Pure Research の出口は **IMRAD draft 必須**。ただし draft の対象読者 (個人 / 内部 / 外部 publication) は project ごとに選択可、それに応じて draft の精度要求が変わる |

---

## Amendments

(ユーザ承認付きの修正のみ append。本文書き換え禁止)

---

### Amendment-3 (2026-05-03): C15 — Integration pattern is an explicit charter decision

**Trigger**: ユーザ指摘「技術を分割するのは必要だけど いつまでたっても動くもの (その技術で作成したいもの) ができないのでは」+ "framework-first だと難しい技術や未知の技術に対して効果を発揮できないのでは"

**追加する中核命題**:

#### C15. Integration pattern is an explicit charter decision

R&D project は **integration pattern を charter (Heilmeier H8) で明示宣言** する。3 パターン:

- **Pattern 1 (vertical slice / framework-first)**: framework + 各 K の baseline 実装を day 1 に建て、K_real が baseline を置換していく。Day 1 から動くが framework 設計の lock-in 危険あり。
- **Pattern 2 (bottom-up / component-first)**: 各 K を TRL-6 まで isolated に成熟させ、最後に integrate。動くものが late、現プロトコルの implicit default。
- **Pattern 3 (skeleton + spike) — recommended default**: throwaway skeleton を day 1-3 で建て、その後 K identification を行い、各 K が skeleton component を置換。Pattern 1 の framework lock-in も Pattern 2 の "no working version" も回避。

##### 選択基準 (decision tree)

1. Architecture が well-understood → Q2 / 不明 → Pattern 2
2. K の baseline が書けるか → YES なら Q3 / NO なら Pattern 2
3. K の interface が stable か → YES なら Q4 / NO なら Pattern 3
4. Stakeholder confidence が重要か → YES なら Pattern 1 / NO なら Pattern 2
5. 不明 → **Pattern 3 (default)**

##### Stage-Gate workflow への影響

- Pattern 1: Project Scoping で framework + baselines、各 K の Stage 5 (Integrate) は baseline 置換 + A/B
- Pattern 2: 各 K の Stage 5 は stub 環境での integration、最後に `core_tech_id == integration` capability で end-to-end
- Pattern 3: Skeleton phase (engineering, not Stage-Gate)、その後各 K の Stage 5 は skeleton component 置換 + A/B、optional final integration capability

##### この命題が触発する設計変更

1. `references/rd/integration_patterns.md` 新規作成 (430 行) — 3 パターン詳細 + decision tree + Stage-Gate mapping + capability_map differences + 4 anti-patterns + worked example
2. `references/rd/rd_charter.md` § H8 を expand: "Midterm + Final + Integration pattern (REQUIRED)" の 3 サブセクション
3. `references/rd/rd_stages.md` に "Pre-condition: integration pattern declared" + Stage 5 を pattern-aware に書き直し
4. `assets/rd/charter.md.template` H8 に Integration pattern + baselines/skeleton の REPLACE field 追加

##### Anti-pattern A の回避

「Implicit Pattern 2 (no decision)」が最も多い失敗。charter で明示宣言を強制することで構造的に防ぐ。

**Approved by**: ユーザ "よいです ありがとう すすめて"
**Linked**: DECISIONS.md D-27、PROGRESS.md Phase 2 amendment

---

### Amendment-2 (2026-05-03): C14 — Core Technology layer (intellectual decomposition)

**Trigger**: ユーザ提案 (R&D で capability に砕く前に「コア技術 / 研究で確立する問い / 寄与 / 発展性」で intellectual 分解が必要)、ユーザ確認 "y"

**追加する中核命題**:

#### C14. R&D 分解は二層構造 (Core Technology + Capability)

R&D の decomposition は **intellectual** 層と **operational** 層の二段階。

```
Charter (Heilmeier 8 Q, target を 1 文で)
   ↓
Core Technologies (intellectual decomposition)
   - 研究すべき最小限の技術群
   - 各 core tech は研究問いと target 寄与を持つ
   - 発展性 = lifecycle 区分 (永続型 / 継続改善型)
   ↓
Capability map (operational decomposition)
   - 各 capability は 1 つの core tech に紐づく (cross-cutting は "integration")
   - 1 capability = 1 test で TRL を 1 段上げる粒度
   ↓
TRL / Stage-Gate / Promotion (各 capability に適用)
```

##### Core Technology の operational filter (粒度ルール)

候補 X が core tech である ⇔ 以下の 3 つすべてを満たす:

1. この target のために research / establishment work が必要 (off-the-shelf で済まない)
2. 単一の「確立する研究問い」として表現できる
3. その問いは他の core tech の問いと独立 (重複なら merge)

そうでない場合:
- off-the-shelf で済む → dependency (使うだけ、core tech ではない)
- 他の core tech の sub-detail → 親に merge
- 問いが立たない (単なる作業項目) → capability に格下げ

**数値目安なし**。target の難しさで自然に決まる。書けない / 重複する候補が出始めたら降格。

##### 発展性 (lifecycle 区分)

| 区分 | 意味 | 含意 |
|---|---|---|
| **永続型** | 一度 establish すれば再投資なしで持続的に使える (e.g. embargo logic、purged k-fold 実装、既知統計の応用) | establish 後 maintenance 不要、project 終了で freeze 可 |
| **継続改善型** | 定期的な update / re-tune / 再 validate が必要 (e.g. regime classifier、特定 feature set、alpha signal、market 適応必要) | establish 後も maintenance plan 必須、別 project で revisit 可能性、project 完了 = "v1 establish + maintenance scheduled" |

novelty 軸 (既存/発展的/新規) は **Heilmeier H3 (What's new) に任せる**。core tech 層には載せない。

##### Schema (capability_map.md の Section 1 として配置)

| ID | コア技術 | 研究で確立する問い | target への寄与 | 発展性 | 先行研究 | Status |
|---|---|---|---|---|---|---|
| K1 | ... | ... | ... | 永続型 \| 継続改善型 | papers.md §A | active \| established \| blocked \| split \| merged \| stale \| parked |

Capability 行は `core_tech_id` (K-id) フィールドを必須化。"integration" は cross-cutting 用の予約 ID。

##### Project termination semantics

- 全 core tech が `永続型` で全て `established` → "fully completed", project freeze 可
- 1 つでも `継続改善型` を含む → 完了時に **maintenance plan を required artifact** として要求 (再評価 cadence、再投資 trigger 条件、別 project で revisit する場合の入口)
- これは `decisions.md` の最終エントリで明示

##### Promotion gate への影響

- 継続改善型 core tech を含む target の promotion 表現は **「v1 established + maintenance plan あり」** に固定
- 永続型のみの target の promotion 表現は **「established」** で完結

##### この命題が触発する設計変更

1. SKILL.md.next に **Decomposition Discipline** 専用 section を新設 (Analysis Depth と並列、R&D の二大柱を可視化)。Core tech 層と Capability 層の 2 段、operational filter、発展性 区分を明記
2. SKILL.md.next の R&D Discipline step を 7 段階に拡張 (Charter → Core Technologies → Capability map → TRL → Stage-Gate → Workflow → Promotion)
3. `references/rd/core_technologies.md` を新規作成 (schema + filter + 発展性 定義 + lifecycle implications + literature 連携)
4. `references/rd/capability_map_schema.md` に `core_tech_id` フィールド必須化を追加
5. `assets/rd/capability_map.md.template` を 2-section 構成に (Section 1: Core Technologies, Section 2: Capabilities)
6. `assets/rd/charter.md.template` の H7 (cost) で one-time vs recurring を分けて記述
7. `references/rd/rd_promotion_gate.md` に lifecycle-aware の promotion 表現規則を追加
8. `aggregate_results.py` schema に `core_tech_id` 列、`lifecycle` 列を追加
9. `decisions.md` の project closure entry template に "maintenance plan" 必須項目を追加 (継続改善型を含む project の場合)

**Approved by**: ユーザ ("y")
**Linked**: DECISIONS.md D-18、PROGRESS.md Phase 2 の更新

---

### Amendment-1 (2026-05-03): C13 — 分析の深さは研究の第一級成果物

**Trigger**: ユーザ指示
> 結果に対する分析だね ここをすごく大事にしたい それは研究の上では何よりも大事だから
> 経験的研究も意味はあるけど，それだって試行錯誤の上でなんで失敗したのかなぜうまくいったのかを分析して推定してあるはずだと思うので
> 事実を分析で詰めて なんでそうなったのかを断言できるか推定できるレベルまで分析する

**追加する中核命題**:

#### C13. 分析の深さこそが研究の第一級成果物

**事実の収集 (observation) は研究ではない。事実の収集 + その因果の分析 (assertion または bounded estimation) が研究である。**

この命題は R&D / Pure Research の両モードに等しく適用される。試行錯誤型の R&D 実験であっても、「動いた / 動かなかった」だけでは未完了。**なぜ動いたか / なぜ動かなかったか** の分析を、断言レベルか境界の明示された推定レベルまで詰める。

##### Analysis depth tier (A0–A5)

TRL が capability の maturity を測るのと同様に、analysis tier は **causal explanation の深さ** を測る共通尺度:

| Tier | 意味 | 例 |
|---|---|---|
| **A0** | 事実のみ記録、解釈なし | 「Sharpe 1.2 in 2018-2022」 |
| **A1** | 仮説的説明を 1 つ命名、evidence は仮説の存在のみ | 「Momentum 効果が原因と思われる」 |
| **A2** | 競合説明を ≥1 同定、まだ識別はしていない | 「Momentum か institutional flow か、いずれかが原因」 |
| **A3** | 主要説明と ≥1 競合説明を **discriminating evidence で分離**、scope の上限が示されている | 「Momentum で説明可能、institutional flow による代替説明は X 観測で weakened、ただし 2020 危機期間は別機構の可能性」 |
| **A4** | **推定レベル** — 機構が同定済み、競合説明が主要なものまで除外、scope conditions が precise、複数 source の supporting evidence | 「機構 M により 2018-2022 に成立、危機期間で破綻するのは機構 M の前提 P が成立しないため、複数 instrument / 複数 sub-period で再現」 |
| **A5** | **断言レベル** — 因果機構が同定済み、競合説明が体系的に除外、scope が precise、複数 instrument / 複数 period / out-of-sample で replicable、生成過程の予測が成立 | 「機構 M により成立、X で破綻、Y で再生、外部 prediction が事後検証で成立」 |

**Promotion 要件**:
- `supported` 判定 (R&D capability の TRL-6 promotion / Pure Research claim の supported promotion) は **A4 以上必須**
- A3 は `preliminary` 止まり
- A0–A2 は研究としてはまだ完了していない (observation 段階)
- "supported" を主張するためには **assertion レベル (A5) または well-bounded estimation レベル (A4)** に到達していること

##### 対称性: 成功と失敗の両方に適用

「成功した」も「失敗した」も A0 (観測) でしかない。**成功の理由を A4+ で説明できない promotion は禁止**。これは agent が陥りがちな「動いたから良し」バイアスへの構造的防御。

failure_analysis.md の「generic label を terminal cause として使うな」原則を、**成功側にも対称適用**:

| Bad (terminal label, A1 止まり) | Good (decomposed, A3+) |
|---|---|
| 「モデルが良かった」 | 「モデル M の特徴 F が、market mechanism X に固有の構造 S を捉えた。代替モデル M' は S を捉えないため out-performed」 |
| 「regime に合っていた」 | 「regime R は条件 C1, C2 を満たし、これがモデル M の前提 P と整合。R 外で破綻する閾値は C1 が値 V を下回る点」 |
| 「signal が強かった」 | 「signal S の strength は IC=0.05 で、これは Y 機構による flow の predictability に由来。Y 機構が消えた瞬間 (event Z) で IC は 0.01 まで低下」 |
| 「データが多かった」 | 「N=10000 で primary metric の SE が σ になり、競合説明 H1 を t=3.2 で reject。N=1000 では H1 を reject 不能」 |

##### 分析が要求する作業

各 trial の analysis section は最低限:

1. **Observation** (facts only, no interpretation, past tense)
2. **Decomposition** (この観察を生み得る機構を ≥3 列挙)
3. **Evidence weighing** (各候補に対し、support と weaken の証拠を列挙)
4. **Tier rating** (A0–A5 の現在地と、その判定根拠)
5. **Gap to next tier** (A4 未満なら、A4 に上げる discriminating test の設計)

「次の trial」を提案する前に、**現 trial の analysis tier を上げきる** ことが優先。新しい trial を増やすより、**現 trial の分析を深める** ことが研究の第一義。

##### この命題が触発する設計変更

1. `references/shared/failure_analysis.md` を `references/shared/result_analysis.md` に rename + scope を 失敗 + 成功の両側に拡張
2. `references/shared/analysis_depth.md` を新規作成 (tier 定義 + decomposition pattern + 例)
3. R&D / PR 両 trial template に **Analysis section** を必須化 (Observation / Decomposition / Evidence weighing / Tier rating / Gap to next tier)
4. `references/rd/rd_promotion_gate.md` と `references/pure_research/pr_promotion_gate.md` に **"analysis tier ≥ A4"** を hard requirement で追加
5. `references/review/conclusion_review.md` に **analysis depth axis** を主要 axis として追加 (correctness / sufficiency / claim discipline / **analysis depth** / reproducibility / cold-eye)
6. `references/pure_research/imrad_draft.md` の Discussion section に "tier ≥ A4 必須" を明記
7. `scripts/validate_ledger.py` で各 trial の analysis tier 記載を check
8. `aggregate_results.py` の schema に `analysis_tier` 列を追加

**Approved by**: ユーザ
**Linked**: GUARDRAILS.md G13-G16 (analysis 関連の agent 失敗モード)、DECISIONS.md D-11

