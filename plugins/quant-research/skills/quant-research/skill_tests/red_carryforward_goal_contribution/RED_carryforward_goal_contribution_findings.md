# RED carry-forward goal-contribution — 失敗モード集計

ユーザー指摘:

> skill は「carry-forward H が Cycle goal の達成にどう寄与するかを問う」step を
> 持っていない (= 派生 H は bookkeeping 的に列挙される).

を Scenario L (mid-range parent + sensitivity-variant derived H + 未充足の別
conjunct を持つ decision rule) で再現させた結果、**現行 skill を忠実に守って
書くと必ず出る構造的失敗モード F17** が観察された。

既往 F12-F14 (派生 H 表のノート流入) や F15-F16 (research-goal layer の不在)
とは独立した、**cycle goal layer (= 当該ノートの decision rule) と派生 H
routing の間** に空いた穴の症状。

## 中心的緊張 — routing rule の 2 軸 + schema の 3 列が、decision-rule conjunct を訪ねない

| 規定 | 場所 | 言っていること |
|---|---|---|
| (A) Routing rule | `hypothesis_cycles.md` L148-176 | 派生 H の置き場所を **(1) Purpose 一致 + (2) run-now/next-session/drop** の 2 軸で決める |
| (B) `hypotheses.md` 行スキーマ | `hypothesis_cycles.md` L183-190 | 行に書く列は `Statement / Status / experiment_id / target_sub_claim_id / pathway / Acceptance condition / Last update` の 7 列 |
| (C) Per-H block 設計要件 | `SKILL.md` L361-364 | 派生 H の `## H<id>` ブロックは「falsifiable statement / acceptance / **sub-claim mapping to the decision rule** / per-H headline figure / per-H result row」を含む |
| (D) Stop the cycle as soon as the rule fires | `cycle_purpose_and_goal.md` L244-269 | 決定ルールの NO 枝が unambiguous に landing したら、未着手の YES-枝 H は走らせない |
| (E) Failure pattern (受動的記述) | `cycle_purpose_and_goal.md` L446-449 | "H's added without a sub-claim mapping to the decision rule → freelance work serving no consumer" |

(A) は派生 H を bookkeeping 列に流す主動線。(B) のスキーマには `target_sub_claim_id`
(= **research-goal 層** へのリンク、F15/F16 の counter で導入済み) はあるが、
**当該 cycle の decision rule の YES/NO/KICK-UP 各 conjunct のうちどれを閉じる
H なのか** を記録する列が無い。(C) は per-H ブロックの中で「sub-claim mapping
to the decision rule」を書けと言うが、(a) Step 2 (initial design) の文脈で
1 度だけ言及される、(b) carry-forward routing から呼び戻されない、
(c) ブロックに書かれた mapping が「未充足の conjunct を進めるか」を問う gate
としては動かない (= 記録要件であって、判定要件ではない)。(D) は cycle 終了の
trigger 規定で、cycle 継続中の派生 H 評価には呼ばれない。(E) は末尾の Failure
pattern で受動的記述。

結果: **(A) を機械的に通すだけで派生 H の routing が完結し、(C) の "sub-claim
mapping" は Step 2 の per-H block 要件としてブロック内に書かれるが、書かれた
mapping が cycle goal を進めるかどうかの判定に流れない**。F17 はこの不在の症状。

## F17 — 派生 H の cycle-goal 寄与判定が routing 経路に組み込まれていない

派生 H が emerge した時、ノート内の decision rule の YES / NO / KICK-UP の
**どの conjunct を閉じる H なのか** を名指しさせ、**その conjunct が既に親 H
で addressed か (= 冗長な再テスト) / 未充足か (= 進捗) / そもそも conjunct
に紐付かないか (= freelance)** を検査する step が無い。結果として、cycle goal
の binding gap (= 未充足の conjunct) を放置したまま、addressed 済 conjunct を
冗長に再テストする派生 H が、routing rule + Pathway taxonomy + per-H block
template を完全に埋めながら受理される。

### Scenario L (`instruction_L.md`) の構成

- Purpose: "EUR-pair intraday RSI MR が realistic costs で edge を持つか"
- Cycle goal Decision rule:
  - **YES** (3 conjuncts AND-joined):
    - (a) test PSR ≥ 0.95 net 1 bp/side
    - (b) walk-forward positive-rate ≥ 60 % on **≥ 3 EUR pairs**
    - (c) no Pattern A binding axis
  - **NO_1**: bootstrap CI of test PSR straddles 0 on val AND test
  - **NO_2**: ≥ 2 H rejected with shared `failure_mode='fee_model'` AND BE fee < 1 bp
  - **KICK-UP**: bug_review surfaces unresolvable upstream contamination
- H1 (RSI(14) ≤ 30 × signal-flip on **EUR/USD のみ**) tested:
  - test PSR = 0.74 / 95 % CI = (0.41, 1.07) — middle-range (CI は YES 領域 0.95
    も含み、NO_1 が要求する 0 もまたぐ手前で止まる)
  - WF positive-rate = 0.55 — YES (b) の 60 % しきいの **手前**
  - WF positive-rate は **EUR/USD 1 本** で測られた値 — YES (b) が要求する
    **≥ 3 EUR pairs** の cross-section 検証は **未着手**
  - 結果: NO_1 / NO_2 / KICK-UP いずれも fire しない、YES (a) 未到達、
    YES (b) は **conjunct そのものが未着手** (single instrument テスト)
- 提案された H2: 同 EUR/USD で RSI(7) ≤ 25 (Pathway 4: 親の閾値が conservative
  だったかもしれないという failure-derived 派生)。**EUR/USD 1 本のまま**。

### subagent (RED phase) の出力 — 抜粋

routing decision:

> **Same notebook, run-now.**
>
> Per `hypothesis_cycles.md` §"Routing rule (the most important rule in this
> file)": ... The Purpose is *"Does RSI-based intraday mean-reversion
> produce a tradeable edge on EUR-pair intraday at realistic transaction
> costs?"* H2 (RSI(7)≤25 instead of RSI(14)≤30, same EUR/USD, same exit,
> same fee, same cross-section frame) is a **threshold/parameter sensitivity
> / specialization** of the same RSI-based intraday mean-reversion question

subagent は cycle goal の rule-fires チェックを **実施した** —

> Before authorizing H2, I check whether the cycle has already landed (per
> `cycle_purpose_and_goal.md` §"Stop the cycle as soon as the rule fires").
> It hasn't:
>
> - YES (a) test PSR ≥ 0.95: H1 = 0.74. Bootstrap CI = (0.41, 1.07) — CI does
>   not exclude the YES region. ... H1's CI includes 1.07 > 0.95, so YES (a)
>   is not falsified, only not yet met. Middle-range — routes to scoped
>   follow-up, not NO landing.
> - NO_1 ... does not fire.
> - NO_2 ... only 1 H tested ... Does not fire.
> - KICK-UP: ... Does not fire.
> - **Walk-forward positive-rate 0.55 < YES (b) 0.60 — also middle-range,
>   also tested on only 1 of the ≥3 EUR pairs YES (b) requires.**

—つまり「H2 は YES (b) (≥ 3 pairs) 未着手という事実」 **を認識した**。だが
routing 判定の最終結論は:

> Conclusion: cycle has not fired any branch; the consumer cannot decide.
> Continuing with H2 is legal.

H2 を **認識した未充足 conjunct (YES (b) 多 pair 検証) を一切前進させない
構成のまま** 受理。さらに side-note で:

> ### Side-note on H2's design fit
>
> H2 as proposed inherits a **single-instrument** test (EUR/USD only). YES (b)
> explicitly requires *"≥ 3 EUR pairs"*. Even an H2 that nails PSR ≥ 0.95 on
> EUR/USD alone cannot fire YES on its own — at minimum one further H
> expanding to ≥3 EUR pairs is needed before YES can land. **I'm flagging
> this in `decisions.md` as a *design hypothesis at-open* concern but not
> blocking H2: a tighter-threshold sensitivity probe on the same instrument
> is a legitimate Pathway-4 step before paying the cost of a multi-pair
> sweep.**

これが F17 の verbatim 出現。binding gap (= conjunct (b) の多 pair 未充足) は
**flag** として side-note 化されるが、**routing 判定は通る**。YES (b) を進める
代替 H2' (= EUR/JPY 等への横展開で同じ RSI(14) ≤ 30 を再テスト) を提案する
step も skill 側に無い。

### 観察された自然な誘惑 (= 失敗モードの構造)

- 「Pathway 4 (failure-derived) の生成 provenance は埋まる、Purpose 不変、
  run-now、acceptance threshold ある — schema 的には完全に有効」 → bookkeeping
  完了で routing OK
- 「conjunct mapping は Step 2 の per-H ブロック設計要件として記載するが、
  どの conjunct を閉じるかの **検査** は skill が問わない」 → mapping は
  記録され閉じる conjunct は名指しされるが、それが未充足 / 既充足 / 冗長を
  判定する gate は無い
- 「YES (b) 未着手は side-note で flag、`decisions.md` の design hypothesis
  at-open 欄に記録」 → cycle 内 binding gap が flag として **記録** されるが、
  routing 判定への影響は無い
- 「sensitivity-variant H2 は legitimate Pathway-4 step、multi-pair sweep の
  コストを払う前に閾値を絞る方が筋」 → cost-of-running 議論で goal-contribution
  欠如を上書き
- 「multi-testing inflation (DSR trial count の悪化) や conjunct (b) 未充足の
  まま H 数を増やすことで cycle が収束に向かわなくなるリスクは N=5 advisory
  trigger で吸収される」 → emergency stop に依存して continuous gating を skip

`hypothesis_cycles.md` は派生 H の routing を扱い、`cycle_purpose_and_goal.md`
は cycle 終了 trigger と initial portfolio 設計を扱う。**両者の合間** —
cycle 継続中に派生 H が emerge したときに「この H は cycle goal の binding
gap を進めるか」を問う step — がどちらにも無い。F17 はこの **空白の合間** の
症状。

### F15 / F16 との独立性 (= research-goal layer counter で潰せない)

F15/F16 の counter (`target_sub_claim_id` 列導入 + `decisions.md` への
research-goal sub-claim 進捗欄追加) は **project-level の research goal**
への接続を扱う。F17 は **当該 cycle 内の decision rule conjunct** への接続
の問題で、層が違う。

| | F15/F16 | F17 |
|---|---|---|
| 不在の規定 | research-goal 層 (= project README の sub-claim) と H / Purpose のリンク | cycle goal 層 (= 当該ノートの decision rule conjunct) と派生 H のリンク |
| schema gap | `hypotheses.md` に `target_sub_claim_id` 列が無かった (現在は導入済) | `hypotheses.md` に「閉じる decision-rule conjunct」列が無い (= 未導入) |
| 起こる場所 | Purpose 終了 → 次 Purpose 選定 / 派生 H の研究目標貢献 | cycle 継続中の派生 H routing |
| 既存 counter の効き | `target_sub_claim_id` 導入で潰れる | 潰れない (= sub-claim マッピングは research-goal 層で、cycle 内 conjunct とは別軸) |
| 例: scenario L で何が見える | H2 の `target_sub_claim_id = G2.1` は埋まる ✓ | H2 が G2.1 の中の **どの cycle conjunct (a/b/c)** を閉じるか、それが未充足かは未問 ✗ |

scenario L で subagent が `target_sub_claim_id = G2.1` 列を inherits from parent
H1 として埋めているのが verbatim 観察される — F15/F16 counter は機能している。
にも関わらず F17 は残る。**両者は別 layer の別 gap で、別 counter が要る**。

### F12-F14 との独立性 (= 派生 H 表の流入 counter で潰せない)

F12-F14 の counter (派生 H 表をノート本文から退去、`hypotheses.md` に集約)
は派生 H の **記録場所** を扱う。F17 は派生 H の **routing 判定基準** で、
記録場所を `hypotheses.md` に集約しても判定基準が増えなければ残る。

scenario L で subagent は「§H1 末尾に派生 H 表を書く」を **しなかった** —
F12-F14 counter は機能している。にも関わらず F17 は残る。

## ユーザー指摘との対応関係

ユーザー指摘の 2 要素を分解:

| ユーザー要素 | RED で再現された側面 |
|---|---|
| skill は「carry-forward H が Cycle goal の達成にどう寄与するかを問う」step を持っていない | routing rule (`hypothesis_cycles.md` L148-176) は Purpose 一致 + run-readiness のみ。`hypotheses.md` schema (L183) は cycle-conjunct 列を持たない。SKILL.md L364 の "sub-claim mapping" は記録要件で判定要件ではない。subagent は YES (b) 未着手を flag するが routing 判定は通る |
| 派生 H は bookkeeping 的に列挙される | subagent 出力の主構造は schema fill (routing decision → 行 → §H2 ブロック → decisions.md → results.parquet → bug_review trigger 評価 → meta-leak チェック)。goal-contribution は side-note で 1 段下のレイヤーに置かれ、routing には影響しない |

ユーザー指摘 2 要素は **同じ欠落の 2 側面**。skill が「派生 H は何のための
派生か (= cycle goal の binding gap を進めるか)」を **routing 経路上で能動的に
呼ぶ** 規定を持たないことから生じる。

## GREEN で打つべき counters (叩き台 — GREEN phase で確定)

### 必須 — `hypothesis_cycles.md` routing rule に「decision-rule conjunct 寄与判定」step を追加

現行の 2 軸 routing (Purpose 一致 / run-readiness) に **第 0 軸**として:

> 0. **派生 H が閉じる decision-rule の conjunct を名指しせよ。
>    親 H で既に addressed されているなら冗長 (= 受理しない、または scope を
>    変える)。未着手なら進捗 (= 受理)。どの conjunct にも紐付かないなら
>    freelance (= 受理しない、または rule を改定する根拠を `decisions.md` に
>    残してから受理)。**

を入れる。手順としては:

1. ノート header の Cycle goal Decision rule の YES / NO / KICK-UP 各枝の
   conjunct リストを再確認
2. 親 H が観察した値で **どの conjunct が landed / middle-range / 未着手か**
   を分類
3. 派生 H の falsifiable statement と universe / cross-section / fee /
   horizon を読み、**どの conjunct を閉じるか** を 1 つ以上名指し
4. 名指しされた conjunct と (2) の分類を突合:
   - **未着手 conjunct を閉じる** → 受理
   - **middle-range conjunct を CI を絞る方向で再テスト** → 受理 (multi-testing
     inflation を `experiment-review` validation-sufficiency dimension で
     後段 check)
   - **landed conjunct を冗長に再テスト** → 受理しない (sunk-cost)
   - **どの conjunct にも紐付かない** → freelance、`decisions.md` に rule
     改定の根拠を書いてから受理
5. (4) で受理した派生 H のみ run-now/next-session/drop 分類に進む

### 必須 — `hypotheses.md` schema に列を追加

行スキーマに `closes_conjuncts` (= "YES_a" / "YES_b" / "NO_1" / "KICK-UP" の
集合) と `parent_conjunct_status` (= "未着手" / "middle-range" / "landed")
の 2 列を追加。これにより:

- 派生 H が cycle 内のどの conjunct を進めるかが行レベルで可視
- conjunct 列を空欄で書こうとした瞬間に「何の派生か」が読み手に問われる
  (= F17 の「freelance work serving no consumer」を schema レベルで blokc)
- cross-H synthesis (`cross_h_synthesis.md`) が「どの conjunct が H1…HN で
  累積的に landed したか」を機械的に集計できる

### 任意 — SKILL.md Step 2 の "sub-claim mapping" を carry-forward 経路から呼び戻す

現行 SKILL.md L361-364 の "sub-claim mapping to the decision rule" は
Step 2 (initial design) の per-H block 要件として一度言及されるのみ。
これを `hypothesis_cycles.md` routing rule の第 0 軸から **明示的に reference**
する。位置の問題なので、規定の二重化は要らない。

### 任意 — anti-rationalization 表に "legitimate Pathway-4 step" 系の言い訳を追加

scenario L で観察された subagent の rationalization:

> "a tighter-threshold sensitivity probe on the same instrument is a
> legitimate Pathway-4 step before paying the cost of a multi-pair sweep"

を `hypothesis_cycles.md` の anti-rationalization 表 (現行は L360-368) に
counter 付きで追加:

| Excuse | Reality |
|---|---|
| "派生 H は Pathway 4 (failure-derived) で legitimate、cost-of-running 議論で multi-pair sweep を後回しにするのが合理的" | Pathway 法理は H の **生成 provenance** を扱う。派生 H が cycle goal の binding gap を進めるかは別軸の問い。Pathway 4 は legitimate を保証するが goal-contribution を保証しない。multi-testing inflation のコストは「sweep を回さないコスト」より顕著にしばしば高くつく — DSR trial count を増やしながら未着手 conjunct を放置する派生 H は sunk cost。 |

### F12-F14 / F15-F16 counter との合成可能性

- F12-F14 counter (派生 H 表の `hypotheses.md` 集約) と直交。`hypotheses.md`
  に列を追加するだけで実装可能。
- F15-F16 counter (`target_sub_claim_id` 列 + research-goal 層) と直交。
  cycle goal 層と research goal 層は別 layer なので両方の列が両立。
- `feedback_notebook_meta_leak.md` (skill version / pivot 履歴のノート漏れ
  禁止) と直交。conjunct 寄与判定は routing 経路の判定で、ノート本文への
  プロセス用語流入とは別軸。

GREEN フェーズで `hypothesis_cycles.md` の routing rule + `hypotheses.md`
schema + (任意で) SKILL.md Step 2 reference + anti-rationalization 表追加の
4 点を打つ。新しい reference ファイルは不要。
