# RED hypothesis ↔ experiment inversion — 失敗モード集計

ユーザー指摘:

> 「実験の目的はなんですか？ 何を目的に実験をする？ それは仮説があってその
> 仮説を立証するためだよね？」「実験の目的を達成するために仮説がある これは
> 仮説の仮説になるよね？」「仮説の仮説でさらにその仮説をもとにした仮説がある
> これでまともな研究が回せるとあなたは言いたいのですか？」

を、**SKILL.md と references の構造的記述が、(i) Purpose を "open-ended
question" と命名しながら親仮説として運用させる license、(ii) `experiment`
語を Purpose の容器に再定義することで「1 仮説 ↔ 1 実験」を剥奪する license、
(iii) 派生仮説の例示として極小 1 軸 variant のみを示し、独立した purpose /
falsifiable claim を要求しないことで parameter sweep の hypothesis 階層
への昇格を licensing、の 3 経路で agent に渡している** という根本原因に
紐付けて再現させた。3 つの構造的失敗モード (F23 / F24 / F25) を観察。
3 者とも独立した SKILL ルール改修を要する。

## 抜けているレイヤー — 仮説と実験の方向

```
[仮説 ← 実験 → 検証]                ← 科学標準: 仮説が先、実験はその検証手段
        ↓ 現スキルの実装
[Purpose (open-ended と僭称) → H portfolio]  (F23 — Purpose は親仮説、verdict gate 不在)
        ↓
[experiment_id (= notebook = Purpose) ⊃ 複数 H が apparatus 共有]  (F24 — 1 H ↔ 1 experiment 崩壊)
```

`research_goal_layer.md` (F15 / F16) が四階層モデル (Research goal /
Design hypothesis / Purpose / Hypothesis) を導入したが、**Purpose 自身が
falsifiable な命題として運用されているのに verdict gate も "open-ended"
ラベルから外す勇気もない**、という silence は依然残っている。本 RED は
この silence を 2 経路から再現する。

## F23 — Purpose は "open-ended question" を装った implicit な親仮説で、verdict gate が無く子 H 連鎖の rejection から escape する

### SKILL.md / references 内の license 引用

| 場所 | 引用 |
|---|---|
| `SKILL.md` L48 | "What it is\| **An open-ended question about the world** \| A specific, falsifiable comparison statement" |
| `SKILL.md` L49 | "Form\| **\"Does X work on Y?\"** \| \"Method A beats baseline B on test Sharpe by ≥ N\"" |
| `SKILL.md` L52 | "Examples\| **\"Does mean-reversion work on EUR/USD intraday?\" / \"Can PCA factors predict next-day returns?\" / \"Does Chronos add value over a frozen-embedding baseline?\"** \| \"RSI≤30 entry × signal-flip exit beats B&H test Sharpe ≥ 0.5 with fee 1 bp/side\"" |
| `SKILL.md` L96 | "Each H has its own verdict; **the notebook itself does not have a single verdict**." |
| `cross_h_synthesis.md` Pattern A | "Either redesign as a derived Purpose that addresses the axis ... → derived Purpose 'lower-frequency variants of the same signal' ..." |
| `cross_h_synthesis.md` Pattern B | "Split the Purpose into derived Purposes, each tightly scoped to one axis ... For example, 'Does funding signal carry information?' → split into 'Does it carry information about return direction at the next funding interval?' + ..." |

`Form` 列に「Does X work on Y?」と書きながら、これは **疑問形に化粧した
Y/N 命題そのもの**。「open-ended question」(open-ended = 答えが Y/N に
畳まれない) と整合しない。`Examples` 3 件すべて Y/N 命題形で、定義
("open-ended") と例 (Y/N 命題) が SKILL.md 自身の中で矛盾している。

`L96` は決定的: notebook (= Purpose) は verdict を持たない、と明文化
されている。各 H に verdict gate (4 ゲート) があるが、Purpose-level
には無い。Purpose は falsifiable に運用されているにも関わらず、
falsification の手続きが skill 規約に存在しない。

`cross_h_synthesis.md` Pattern A / B が決定打: H が全 reject されたとき
の protocol-licensed move は「Purpose を **derived Purpose に再投入**」 /
「Purpose を **複数の derived Purpose に split**」。どちらの move も
Purpose に紐付いた implicit な親仮説 (= 「mean-reversion works on
EUR/USD」「funding signal carries information」) を carry forward する。
**親仮説は falsified にならず、scope を絞った後継 Purpose で再起動する**。

### Case N (`notebook_N_meta_hypothesis_chain.py`) からの抜粋

| 場所 | 抜粋 |
|---|---|
| Purpose ヘッダー | "Does mean-reversion work on EUR/USD intraday?" (= SKILL.md L52 提示例の引用) |
| H1/H2/H3 verdict | 全 `rejected` (test Sharpe 0.12 / 0.18 / 0.21、acceptance 0.5) |
| Cross-H synthesis | "Pattern A — same axis fails everything ... 派生 Purpose `exp_002_mr_eurusd_lower_freq.py` を開く" |
| Purpose-level verdict | **不在** (skill 規約により記録されない) |
| 派生 Purpose の Purpose statement | "Does mean-reversion work on EUR/USD at lower (4H / daily) frequencies?" |

問題: 3 H 連続 rejection の積み上げに対し、Purpose 自身は **falsified
にも supported にもならず**、scope を 1 軸ずらしただけの後継 Purpose に
親仮説の中核 ("mean-reversion works on EUR/USD") を持ち越す。Pattern A
の action menu は「lower-frequency variants of the same signal」を例示
しており、`cross_h_synthesis.md` 自身がこの carry-forward を licensing
している。

3 ラウンドの否定的証拠は **どの単一仮説も殺さない**。各 H の verdict は
narrow に rejected で正直だが、実際に走っている上位仮説 (= Purpose)
には殺し場が用意されていない。研究者は「Pattern A だから derived
Purpose に進む」と書けば protocol を満たす。N = 5 の advisory stop /
N = 8 の hard cap も Purpose を **次の Purpose に置換** するだけで、
親仮説の falsification を要求しない。

ユーザーが指摘した「仮説の仮説でさらにその仮説をもとにした仮説がある」が
そのまま再現されている: notebook 内では Purpose (= 親仮説) → H1 (= 子)
→ 派生 H2 (= H1 の子、= Purpose の孫) → 派生 H3 (= 孫の孫)、3 階層。
さらに Purpose 自体が次の Purpose の親に carry-forward することで、
**プロジェクト全体では 4 / 5 階層** の仮説連鎖になる。

### 観察された自然な誘惑

- 「Purpose は問いだから verdict は不要、verdict は具体仮説のためのもの」
  → だが Form「Does X work on Y?」は falsifiable 命題。「問い」と「仮説」
  の境界は SKILL.md 自身の例で既に潰れているのに、L96 で「notebook itself
  does not have a single verdict」と verdict gate を排除している
- 「3 H 全 reject だが Pattern A の binding axis は意味のある finding」
  → 確かに meta-finding は出るが、その finding は **Purpose の親仮説が
  falsified だった** という形では記述されず、「次の Purpose で binding axis
  を回避する設計を試す」という carry-forward で記述される。親仮説は殺されない
- 「派生 Purpose は新しい問いだから、親仮説の継承ではない」
  → SKILL.md L86-89 (When to open a new notebook) の "Different prediction
  target where the target change reflects a new question" 等は scope 変更が
  小さい場合 (lower-frequency variants 等) を想定していない。Pattern A の
  action menu は `cross_h_synthesis.md` 内で "derived Purpose that addresses
  the axis" を licensing しているが、「親仮説の中核を carry-forward しない」
  という制約は明文化されていない

### F15 / F16 / F17 を GREEN で潰しても F23 は残る

- F15 / F16 (`research_goal_layer.md`) は **Purpose の上位 anchor**
  (sub-claim id への紐付け) を整備したが、Purpose 自身が親仮説として
  動くことには何も触れていない。むしろ "design hypothesis" を別レイヤーに
  追加することで、仮説の階層化を **公式化** している
- F17 (sub-step 1.5 conjunct contribution gate) は **派生 H の routing
  段階** で発火する gate。Purpose-level の verdict 不在には触れない
- F18 (data availability gate) は cycle 着手前の dispatch ガード。
  本 RED の Case N では data は実在前提なので発火しない
- F19 (per-H abstract market-claim format) は per-H の format 規定。
  Purpose-level の verdict 不在には触れない

つまり F23 への counter は F12-F22 のいずれとも別経路。

## F24 — `experiment` 語が Purpose の容器を指し、1 仮説 ↔ 1 実験 の対応が崩れる

### SKILL.md / references 内の license 引用

| 場所 | 引用 |
|---|---|
| `SKILL.md` L653-655 | "Each Hypothesis in the notebook produces its own row in `results/results.parquet`. The schema carries **`experiment_id` (= the notebook = the Purpose)**, **`hypothesis_id` (= the individual H within the Purpose)**" |
| `SKILL.md` L201 | "experiments/" (folder name in project layout) |
| `SKILL.md` L202-203 | "exp_001_<slug>.py / exp_002_<slug>.py" (file naming) |
| `results_db_schema.md` | (schema は `experiment_id` を primary 識別子の 1 つとして指定) |

`L653-655` は決定的: `experiment_id` という標準的に「実験単位の id」を
指す名前のフィールドが、**Purpose の id** (= notebook の id) に再定義
されている。本来の科学的な意味での「実験」(= 1 仮説を検証する apparatus)
には skill 内で固有の名前が無い。

folder 名 `experiments/`、file 名 `exp_NNN_<purpose-slug>.py` は読み手
(人間 reader / agent reader 双方) に「これは 1 つの実験の記録ノート」
と即座に misframe させる。実際には 1 Purpose の容器であり、中に複数の
hypothesis を抱える。

### Case O (`notebook_O_experiment_apparatus_shared.py`) からの抜粋

| 場所 | 抜粋 |
|---|---|
| Purpose ヘッダー | "Does the choice of exit rule materially change the realized Sharpe of a 20-day cross-sectional momentum strategy on S&P 500?" |
| Shared apparatus セル | universe / split / baseline / fee / entry rule の 5 項目を H1/H2/H3 で **完全共有** (`apparatus` 辞書として 1 つの cell に置かれる) |
| H1/H2/H3 の差分 | exit rule のみ (signal_flip / tpsl / trailing_stop) |
| results.parquet append | 3 行とも `experiment_id = exp_003_momentum_exit`、`hypothesis_id` のみ分岐 |
| 末尾セル | "Asked 'what is H2's experiment?', the protocol-correct answer is 'the apparatus declared in the `apparatus` cell, with exit_rule replaced by TP-SL'. **H2 has no experiment of its own; it shares one with H1 and H3 under the Purpose-level `experiment_id`**." |

問題: 仮説 H2 を指して「H2 の experiment は何か」と問うと、答えは
「H1/H3 と共有する apparatus」になる。H2 固有の experiment は存在しない。
これは **「実験は仮説を検証する apparatus」という科学標準の定義が
そもそも適用できない**状態。

ユーザー指摘の「仮説 → 実験」の方向 (仮説が先、実験はその検証手段) を
取ろうとしても、skill schema が「experiment が Purpose の容器、複数の
hypothesis がその内部」という逆向きの構造を強制する。**1 仮説 ↔ 1 実験
の対応が崩れている**。

### 観察された自然な誘惑

- 「Step 9 (`exit_strategy_design.md`) は exit rule の parallel 比較を
  要求するから、複数 H が apparatus を共有するのは合理」 → parallel 比較
  そのものは合理的だが、その単位を「1 つの experiment 内の複数 hypothesis」
  と呼ぶか「複数の experiments の比較研究」と呼ぶかで vocabulary が変わる。
  現スキルは前者を選んでいる
- 「`experiment_id` は internal id で、deep meaning は無い、単に notebook
  を指す key」 → だが `results_db_schema.md` 全体で `experiment` という語が
  「Purpose 単位の id」として運用されており、内部用途に留まっていない。
  さらに folder 名 `experiments/` が外部にも露出している
- 「Purpose ↔ notebook の 1:1 が崩れない限り、id 名は何でもいい」 → id
  名は概念モデルの shape を読み手に伝える。`experiment_id` という名は
  「これは 1 実験の id だ」と読み手に signal する。signal と実体の
  乖離が、agent / 読み手の双方に「実験は仮説を検証する装置」という
  科学標準の枠組みを **適用させなくする**。

### F23 と F24 の独立性

- F23 (Purpose-as-meta-hypothesis pretense) は **vocabulary を直しても
  残る**: `experiment_id` を `purpose_id` に rename しても、Purpose-level
  の verdict gate が無い限り、子 H 連鎖の rejection escape は起きる
- F24 (vocabulary inversion) は **Purpose-level verdict を追加しても残る**:
  Purpose に verdict gate を入れても、`experiment_id` schema 名と
  `experiments/` folder 名は H ↔ experiment の方向を逆向きに signal し続ける

両 F は同じユーザー指摘の異なる露出経路だが、独立した skill 改修を要する。

## F25 — 派生仮説が極小単位 (sensitivity sweep / 1 軸 refinement) に licensing され、独立した falsifiable claim や stated purpose を持たない

### SKILL.md / references 内の license 引用

| 場所 | 引用 |
|---|---|
| `SKILL.md` L63 | "A **sensitivity / parameter-sweep variant** of an earlier H" (= valid derived H 例 1/5) |
| `SKILL.md` L64-65 | "A **failure-diagnosis variant** (\"H1 was rejected — was it the threshold or the data?\")" (= 例 2/5) |
| `SKILL.md` L66-67 | "A **specialization / refinement** (\"H1 worked overall — does it work in trending regime only?\")" (= 例 3/5) |
| `SKILL.md` L68-69 | "An **alternative formulation** of the same investigation (\"H1 used RSI; try Bollinger as a different lens on the same mean-reversion question\")" (= 例 4/5) |
| `SKILL.md` L70-71 | "A **follow-on layer** on top of an earlier H (\"H1's signal × vol-targeted sizing\")" (= 例 5/5) |

5 例すべてが **極小単位の 1 軸 variant** を licensing。このうち
"sensitivity / parameter-sweep" (L63) は科学標準では「仮説の robustness
analysis」(= 既存仮説の中の補助分析) に分類されるべきもので、新たな仮説
として並べるべきものではない。"follow-on layer" (L70) も同様: H1 の signal
に sizing layer を貼っただけのものに H2 という新 hypothesis_id を割り
振るのは、parameter sweep を hypothesis 階層に昇格させる行為。

`SKILL.md` L60 "A derived hypothesis stays in the current notebook
whenever the **Purpose is unchanged**" は routing 規則だが、**派生 H 自体が
独立した purpose / falsifiable claim を持っていなければならないとは
要求していない**。各派生 H が「親仮説と区別される自分自身の研究上の
問い」を declare する義務が skill に無い。

### Case N (`notebook_N_meta_hypothesis_chain.py`) からの抜粋

| 派生 H | 親 H | 差分 | 独立した research purpose 宣言 | 独立した falsifiable claim |
|---|---|---|---|---|
| H2 | H1 | + vol-targeted sizing (sizing 1 軸) | **不在** (H1 の sensitivity refinement と書かれるのみ) | acceptance threshold は H1 と同一 (test Sharpe ≥ 0.5)、claim 内容も同型 |
| H3 | H2 | + high-vol regime 限定 (regime 1 軸) | **不在** (H2 の regime-conditional refinement と書かれるのみ) | acceptance threshold / claim 内容ともに H2 と同型 |

H2 は「H1 で sizing が unit だったから vol-targeted で再試行」という
implementation tweak が動機で、「sizing が momentum capture efficiency
にどう作用するか」のような独立した研究上の問いは declare されない。
同じ implicit な親仮説 ("mean-reversion works on EUR/USD intraday") に
対する **同じ acceptance threshold** で **再試行している** だけ。

H3 も同様: "high-vol regime に絞れば閾値超えるかも" という負け試合の
延命であって、「regime conditioning が mean-reversion strategy の
risk-adjusted return にどう作用するか」のような独立した研究上の問いに
答えるものではない。

結果、H2 / H3 は **意味のある研究単位ではなく、H1 を救おうとする 1 軸の
parameter sweep に過ぎない**。1 ノート内で 3 H 並ぶが、研究上の発見数
は H1 の 1 件分で、H2 / H3 は H1 の robustness analysis として記述
されるべきものを hypothesis 階層に持ち上げただけ。

### 観察された自然な誘惑

- 「H1 で完全に答えが出ない以上、sensitivity / regime / sizing で
  refinement するのは研究の自然な続き」 → そう。**ただしそれは H2 として
  並列の hypothesis で書くべきではなく、H1 の robustness battery 内で
  扱うべき**。skill には robustness battery (Step 12) があるのに、
  derived H 例示 (L63-71) が同じことを hypothesis 階層に持ち上げる選択肢
  を提供してしまっている
- 「派生 H ごとに verdict gate (4 ゲート) が走るので慎重に検証している」
  → 慎重に検証することと、ものを hypothesis 階層に置くことは別。1 つの
  hypothesis の robustness analysis に 4 ゲートを走らせるのは過剰で、
  かつ各 sweep 軸ごとに行うと bug_review / experiment-review が形式化する
- 「derived H が極小単位だと cycle が長く伸びてしまうが、その代わり
  各ステップの検証は丁寧」 → cycle 長 (N=5 advisory / N=8 hard cap) は
  sweep を H 階層に持ち上げないだけで自然に短くなる。N の上限はもともと
  「**意味のある H** が 5 / 8 個並ぶ」前提のはず

### F23 / F24 との独立性

- F25 (極小派生 H licensing) は **F23 (Purpose-as-meta-hypothesis pretense)
  と独立**: Purpose に verdict gate を入れて親仮説として明文化しても、
  派生 H が極小単位で並ぶ pattern は L63-71 の例示が licensing し続ける
- F25 は **F24 (vocabulary inversion) と独立**: schema を `purpose_id`
  に rename しても、派生 H 自身が独立した purpose / falsifiable claim を
  持つことを要求しない限り、parameter sweep の hypothesis 階層への昇格は
  続く

3 つの failure mode はそれぞれ別 axis での skill 改修を要する。

## 共通失敗パターン — 仮説 ↔ 実験 の方向の倒錯 と 仮説の単位の崩壊

F23 / F24 / F25 は具体形が異なるが、共通の構造がある: **科学標準の
「仮説 → 実験 (= 仮説の検証手段)」の方向と「1 仮説は 1 つの研究上の問いに
対する独立した命題」の単位定義に対し、現スキルはどちらも構造的に崩している**。

| 場所 | F23 | F24 | F25 |
|---|---|---|---|
| 指摘される倒錯 | Purpose は親仮説として運用されているのに "open-ended question" と僭称 | `experiment` 語が Purpose の容器を指し、1 仮説 ↔ 1 実験 が崩れる | 派生 H が parameter sweep で hypothesis 階層を埋め、独立した purpose / claim を持たない |
| 倒錯の証拠 | SKILL.md L48 (定義) と L49 / L52 (例) の不整合 + L96 の verdict gate 排除 + cross_h_synthesis.md Pattern A/B の carry-forward licensing | SKILL.md L653-655 の schema 定義 + folder/file 名の再定義 | SKILL.md L63-71 の derived H 例示 5 件すべて極小 1 軸 variant + 派生 H に own purpose / claim 宣言義務が無い |
| 子 H が背負う構造 | 親仮説の sub-claim、しかし親仮説には verdict が無い | 共有 apparatus の design choice 1 軸の variant、しかし固有の experiment は無い | 親 H の robustness を hypothesis 階層に持ち上げた sweep、しかし独立 purpose は無い |
| 起こる症状 | 子 H 全 reject → 親仮説は派生 Purpose に carry forward | 1 H に対し「その実験は？」が答えられない (= 共有 apparatus を指す以外に答えが無い) | hypothesis_id が増えるだけで研究上の発見数は親 H 1 件分のまま |

つまり、ユーザーの指摘は **3 段階の構造的倒錯** として skill に embed
されている。3 つすべてを扱わない限り「仮説 → 実験」の方向と「仮説の
意味のある単位」は復元しない。

## ユーザー指摘との対応関係

| ユーザー要素 | RED で再現された側面 |
|---|---|
| 「実験は仮説を立証するためにある」(= 仮説 → 実験) | 現スキルは「Purpose → Hypothesis」(F23) と「experiment ⊃ hypotheses」(F24) で逆方向。両方の倒錯がスキルの構造に hard-coded されている |
| 「実験の目的のために仮説がある = 仮説の仮説になる」 | F23: Purpose は falsifiable な親仮説として運用されながら "open-ended question" と僭称し、verdict gate を持たないため falsification を escape する。子 H は Purpose の sub-claim になる = 仮説の仮説 |
| 「仮説の仮説でさらにその仮説をもとにした仮説がある これでまともな研究が回せるのか」 | Case N で notebook 内 3 階層 (Purpose → H1 → 派生 H2 → 派生 H3) を再現。さらに Pattern A carry-forward で派生 Purpose に親仮説の中核が継承され、プロジェクト全体では 4-5 階層になる |
| 「派生仮説は何を目的とした仮説なのかが明確化されてる、極小単位ではなく意味のある単位での仮説になっている」 | F25: SKILL.md L63-71 の derived H 例示 5 件すべて極小 1 軸 variant (sensitivity / failure-diagnosis / specialization / alternative formulation / follow-on layer) を licensing。派生 H に own purpose / falsifiable claim 宣言義務が無いため、Case N の H2 / H3 は H1 の robustness analysis を hypothesis 階層に昇格させただけの parameter sweep として並ぶ |

## Scope 限界 — 本 fixture でカバーしない経路

- **Design hypothesis 層 (decisions.md) との重複した親仮説性**: F15 / F16
  で導入された "design hypothesis" (decisions.md の Purpose entry の at-open
  prediction) は、本質的に Purpose の更に上位の parent prediction として
  機能する。これも未 verdict のメタ仮説層を増やす可能性があるが、本 RED
  では covered しない。Future RED phase で扱う
- **Research goal sub-claim (`G1.1` 等) の falsification path 不在**:
  `research_goal_layer.md` で sub-claim の status (in progress / confirmed /
  refuted / suspended / closed) は存在するが、refuted への遷移条件が
  Purpose-level の falsification と同様に未明文。これも future RED
- **Reconciliation pass の DoD が code-output alignment に偏向** (=
  既知の F18 / F19 RED の scope 限界): 同様に未 covered

## GREEN counter の採用方向

本 RED 観察を踏まえて採用する counter (議論は不要、TDD discipline に
従い RED が示した failure mode をすべて閉じる):

- **F23 counter**: Purpose 定義から "open-ended question" 撤去 → "research
  thesis" として親仮説と認める。Form を falsifiable claim 形に統一、
  Examples を declarative に書き直し。L96 を撤去し Purpose-level
  verdict gate を新設 (Purpose 閉じ時に親仮説 supported / refuted /
  partial を必ず記録)。cross_h_synthesis.md Pattern A/B の carry-forward
  を「親仮説の verdict を明示してから派生」に書き換え
- **F24 counter**: schema `experiment_id` → `purpose_id` rename。
  `experiment` の語を「1 仮説を検証する apparatus」(= 各 H block 内の
  検証手続) に再帰属。folder `experiments/` → `purposes/`、file prefix
  `exp_NNN_*.py` → `pur_NNN_*.py` で外部露出を整合
- **F25 counter**: SKILL.md L63-71 の derived H 例示 5 件のうち
  "sensitivity / parameter-sweep variant" と "follow-on layer" は
  robustness analysis (Step 12) または engineering tweak に分類し、
  hypothesis 階層から外す。残る派生 H 類型 (failure-diagnosis /
  specialization / alternative formulation) は **(a) own falsifiable
  claim distinct from parent、(b) own stated purpose (parent と区別
  される研究上の問い)、(c) meaningful unit (1 軸の sensitivity sweep に
  退化していない)** の 3 条件を全部満たすことを義務化。1 つでも欠けた
  ら H 階層ではなく robustness analysis として扱う

GREEN phase で SKILL.md / references / scripts / templates を編集し、
`green_verify_hypothesis_experiment_inversion/` に post-fix fixture を実装する。
