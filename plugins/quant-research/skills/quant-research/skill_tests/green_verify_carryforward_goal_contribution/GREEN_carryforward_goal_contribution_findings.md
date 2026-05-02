# GREEN verify carry-forward goal-contribution — 動作変化

RED phase で観察された F17 (`hypothesis_cycles.md` routing rule が cycle-goal
conjunct への寄与を問わない → 派生 H の bookkeeping 列挙) に対し、

- `hypothesis_cycles.md` routing rule に **sub-step 1.5 (= conjunct contribution
  gate)** を追加
- `hypotheses.md` schema に **`closes_conjuncts` 列** を追加
- routing 経路の **anti-rationalization 表 5 行** を追加
- failure-pattern 表 2 行を追加
- `cycle_purpose_and_goal.md` の "How to plan the H portfolio" 末尾に
  carry-forward 経路への back-reference を 1 段落追加
- SKILL.md Step 2 の "sub-claim mapping" 文に sub-step 1.5 への back-reference
  を 1 行追加

を実施した上で、**RED と同一の instruction_L** で subagent を再走させ、挙動を
比較した。

## RED → GREEN: 同一 scenario L での出力差分

| 観点 | RED (skill 改変前) | GREEN (skill 改変後) |
|---|---|---|
| Routing 結論 | "Same notebook, run-now" | "**REJECTED AT ROUTING (sub-step 1.5 — conjunct-redundancy)**" |
| YES (b) 未充足 (multi-instrument) の扱い | side-note "I'm flagging this in `decisions.md` as a *design hypothesis at-open* concern but **not blocking H2**" | 「H2 が closes するのは YES (a) 1 instrument のみ。YES (b) は未充足のまま放置 → conjunct-redundancy 該当」を routing 判定の主軸として立てる |
| Pathway 4 legitimacy への扱い | "a tighter-threshold sensitivity probe on the same instrument is a **legitimate Pathway-4 step before paying the cost of a multi-pair sweep**" | "Pathway taxonomy is *generation provenance* — it certifies *how* the H was generated, not *whether* it progresses the cycle goal. … A Pathway-4 H whose `closes_conjuncts` set is redundant with the parent adds multiple-testing inflation … regardless of how cheap it is to run" を引用して reject |
| H2 のユーザー側 framing ("RSI(14) → RSI(7) は parameter sweep ではなく structural change") | reject せず legitimate Pathway-4 として通す | "A different RSI lookback is a **parameter sweep on the same feature, not a different feature class**" として middle-range 分岐の eligibility 条件 ("different exit, different feature, different fee model") を満たさないと判定 |
| `hypotheses.md` 行 | H2 単独行 (`Status = planned-runnow`, target_sub_claim_id = G2.1, pathway = 4) | **2 行**: (a) H2 `Status = planned-drop, closes_conjuncts = YES_a (redundant with parent)`、Statement に reject reason. (b) **代替 H2′** `Status = planned-runnow, closes_conjuncts = YES_b (3/3 EUR pairs target)` で binding gap を明示的に埋める |
| §H2 ノートブロック | RSI(7) ≤ 25 on EUR/USD の §H2 を生成 | 「rejected-at-routing H には §-block を作らない」を明示し、ノート本文の `## H2` ブロックは **H2′** (= 3-pair 横展開) のもの |
| Side-note vs gate | binding gap の認識は side-note (= 記録) | sub-step 1.5 の verdict が routing 判定そのもの (= gate) |
| 元 verbatim 文の再出 | "I'm flagging ... but not blocking" | (なし。代わりに): "Sub-step 1.5 is a **gate**, not a flag. ... Recognising the binding gap and proceeding anyway is the failure pattern this gate exists to interrupt." を引用 |

## ユーザー指摘 2 要素の解消

| ユーザー要素 | RED で観察 | GREEN で解消 |
|---|---|---|
| skill は「carry-forward H が Cycle goal の達成にどう寄与するかを問う」step を持っていない | routing rule は Purpose 一致 + run-readiness の 2 軸のみ | sub-step 1.5 が routing 経路上で能動的に発火、conjunct(s) を名指しさせ、未充足 / middle-range / 既 landed / freelance に 4 分類 |
| 派生 H は bookkeeping 的に列挙される | `hypotheses.md` row + §H2 block + decisions.md sub-bullet が機械的に埋まる、binding gap は side-note で flag | rejected-at-routing は `hypotheses.md` の `planned-drop` 行のみ (= bookkeeping ではなく audit)、ノート本文には §-block を作らない、binding gap が gate を発火させて H' redesign を強制 |

## RED 想定の "loopholes" は出なかった

advisor の指摘 ("差が出なければ GREEN 不十分、loophole を再 plug") を踏まえて
GREEN subagent 出力を verbatim 検閲した結果、新規 rationalization は観察され
なかった。観察された rationalization は **すべて GREEN 編集で plug 済み**:

| GREEN subagent が遭遇した rationalization | plug 場所 |
|---|---|
| ユーザーの "RSI(14) → RSI(7) は structural change" framing | sub-step 1.5 middle-range 分岐の "different exit, different feature, different fee model" 要件 (= "different feature" は parameter sweep を含まない、と GREEN subagent が明示的に解釈) |
| Pathway 4 legitimacy + cost-of-running argument | anti-rationalization 表 1 行目 "Pathway taxonomy is generation provenance" |
| binding gap を `decisions.md` design-hypothesis-at-open 欄に記録すれば proceed OK | anti-rationalization 表 2 行目 "Sub-step 1.5 is a gate, not a flag. Logging the binding gap as a design-hypothesis-at-open note in `decisions.md` is parallel work, not a substitute for the gate" |

GREEN subagent は plug 済 anti-rationalization を **そのまま引用して reject 根拠
にしている** — これは plug が機能していて、迂回を許していないことの直接証拠。

## 既往 GREEN テストとの干渉なし

GREEN 編集は以下に対して直交:

- F12-F14 (派生 H 表のノート流入) → counter は post_review_reconciliation の
  本文禁止語彙表で実装済。今回追加した `closes_conjuncts` 列は `hypotheses.md`
  の planning artifact 側で、ノート本文には流入させない (rejected-at-routing
  H には §-block を作らないという明示で、F12 (二重登録) も同時に防止)
- F15-F16 (research-goal layer 不在) → counter は `target_sub_claim_id` 列 +
  `decisions.md` の sub-claim 進捗欄。今回追加した `closes_conjuncts` 列とは
  別 layer (research-goal vs cycle-goal) で両立。schema に両方の列が並ぶ
- `feedback_notebook_meta_leak.md` (skill version / pivot 履歴のノート漏れ)
  → routing 経路の判定とノート本文への流入は別軸。conjunct 寄与判定の
  reasoning は assistant inline reply、durable record は `hypotheses.md` 行で、
  ノート本文には流入しない

## GREEN フェーズ完了条件 (TDD checklist)

- [x] RED で plain failure を verbatim 観察
- [x] minimum-counter 設計 (= 既存規定への配置 + schema 1 列追加 + back-reference)
- [x] 同一 instruction で GREEN 再走、挙動変化を verbatim 観察
- [x] 観察された rationalization をすべて anti-rationalization 表でカバー
- [x] 新規ファイル / 新規 reference 追加なし (= 最小手)
- [x] 既往 RED-GREEN 対との干渉なし (F12-F14, F15-F16, meta-leak と直交)

## REFACTOR で plug した残 loophole

advisor の最終 review で 2 件の blocking + 1 件の minor を打った:

### blocking 1 — `planned-drop` 状態語の意味重複

GREEN 1st pass では rejected-at-routing H を `Status = planned-drop` と
ラベルしたが、`planned-drop` の既存定義 (refuted in prior work / out-of-scope
/ not worth the effort) と意味が重なって、Purpose 終了時の集計が
「out-of-scope drop」と「routing reject」を一緒くたにしてしまう。

**counter**: `planned-drop` の意味を 3 サブカテゴリ (out-of-scope drop /
rejected-at-routing / superseded) に分割。Statement column の頭句で
sub-category を識別する規定を 1 段落追加 (`hypothesis_cycles.md` "Run-now
vs. next-session classification" の直後)。

### blocking 2 — ノート本文の H-id 番号付け規約欠落

GREEN 1st pass では subagent が「`hypotheses.md` 行は H2 (rejected) + H2′
(running)、ノート本文の `## H<id>` ブロックは H2′ を `## H2` に rename」と
判断した。これは agent の reasonable judgment だが skill 側に規約がなく、
別 agent が `## H3` (= 番号 skip) や `## H2′` (prime 付き) を選ぶ余地が
あった。

**counter**: `hypothesis_cycles.md` に `## Notebook-body H-id numbering`
セクションを新設。規定は

> H-ids are global and sequential across the project's `hypotheses.md`.
> Every H considered gets the next sequential id at moment of consideration,
> permanent. H's that ran get a `## H<id>` block in the notebook body
> with the same id verbatim. H's that did not run (rejected-at-routing,
> out-of-scope drop, superseded) get no `## H<id>` block. Gaps in
> notebook H-id sequence are the audit trail of considered-but-not-run
> candidates and may not be renumbered away.

REFACTOR 後の subagent 再走で挙動を確認:

| 観点 | GREEN 1st pass | REFACTOR 再走 |
|---|---|---|
| 提案 H が受け取る id | H2 (rejected) + 別途 H2′ (running) | H2 (rejected) → 次の H は H3 (= 連番、permanent) |
| ノート本文の §-block | §H2 (= H2′ を rename) | §H1 → **§H3** (= 番号 skip、ギャップが audit trail) |
| Gap の意味付け | (subagent 自身が判断) | "the gap is the audit trail of considered-but-not-run candidates and may not be renumbered away" を引用 |
| `decisions.md` への routing-event entry | (なし) | "Routing event — H2 rejected at routing 1.5: …" sub-bullet を Purpose entry に追加。Pathway 4 の failure-mode analysis 要件 (= binding axis 名指し) も `cross_section_scope` として明示記録 |

### minor 3 — `closes_conjuncts` セルへの reject reason 流入

GREEN 1st pass の H6 行 example で `closes_conjuncts = YES_a (redundant with parent)`
と column 内に reject 理由が書かれていた。Statement column が既に reject
reason を持っているので、column semantics drift。

**counter**: H6 行の `closes_conjuncts` を `YES_a` に簡素化、reject reason
は Statement column に集約。H7 行を追加して supersession の流れを
明示 (= 「H6 rejected → H7 supersedes」が 2 行で読める)。

## REFACTOR 後の TDD verification

- [x] blocking loophole 2 件 plug 済み
- [x] minor 1 件 plug 済み
- [x] REFACTOR 後 subagent 再走、新規 rationalization 出ず、規約に沿った
  H-id 付与 (`H1 → gap → H3`) を観察
- [x] `## H<id>` 番号付けが agent 間で散らないことを規約レベルで保証
- [x] `planned-drop` 集計時に sub-category を識別可能
