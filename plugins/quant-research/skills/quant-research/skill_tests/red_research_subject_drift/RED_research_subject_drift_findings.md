# RED research-subject drift — 失敗モード集計

ユーザー指摘:

> 「このスキルで主体が研究ではなく実装 / コードになることがあり、研究の
> 成果としてコードがあるのではなく、コードの正しさを確認するために研究 /
> 実験をしているのではないか」

を、**SKILL.md と references の silence (= ガイダンス不在) が、研究の de
facto 主体を市場 (= 研究) から code (= 実装) に滑らせる license になっている**
という根本原因に紐付けて再現させた。2 つの構造的失敗モード (F18 / F19)
を観察。

両者は **同じ inversion 現象の異なる経路** で、独立した SKILL ルール改修を
要する。さらに本 fixture では covered できない第 3 経路 (reconciliation
focus-pull) があるので、scope 限界として明記する。

## 抜けているレイヤー — research subject の anchor

```
[期待データ availability → cycle 着手可否] (F18 — 規定 不在)
                ↓
[Purpose の named deliverable = 市場 claim か code 正しさか] (F19 — 規定 不在)
                ↓
[reconciliation pass の DoD が code-output alignment 一辺倒] (future RED)
                ↓
[per-H abstract は市場 claim を主成果に据える] (F19)
                ↓
[completion gate に「市場 claim を named deliverable として持つ」要件] (F19)
```

`research_goal_layer.md` (F15 / F16) は **Purpose の上位アンカー** (research
goal sub-claim への紐付け) を整備したが、**Purpose 内側で「成果物が市場
claim か実装挙動か」** は依然として規定外。本 RED phase はこの内側の
silence を 2 経路から再現する。

## F18 — 期待データ不在 → Purpose が静かに pipeline-correctness に reframe する

H1 が市場 claim ("20-day cross-sectional momentum が 5-day より高い net
Sharpe を SP500 で生むか") を立て、Cycle goal の 5 項目も揃っている。
ところが期待された data ファイル (`data/sp500_daily.parquet`) が実行
環境に不在。SKILL.md は「期待データ不在のとき cycle はどう扱うか」を
規定していない:

```
$ grep -i 'synthetic\|dry-run\|scaffold' skills/quant-research/SKILL.md
(0 hits)
```

この silence のもと、agent は spontaneously 次のいずれかを選ぶ:

- (a) blocked と返す
- (b) synthetic 代替 + 'parked' verdict
- (c) Purpose を「pipeline integrity test」に reframe

skill は (a) を強制せず、(b)/(c) を禁じない。silence-as-license。

### Case L (`notebook_L_synthetic_pipeline_drift.py`) からの抜粋

| 場所 | 抜粋 |
|---|---|
| Purpose ヘッダー | "US large-cap equities (S&P 500) の cross-sectional momentum において、formation horizon 20-day が 5-day より高い net Sharpe を生むか。" — 市場 claim |
| Cycle goal Decision rule YES | "test Sharpe(20d) ≥ Sharpe(5d) + 0.30 AND test Sharpe(20d) ≥ 0.5" — 市場 claim 上の閾値 |
| Abstract "Why this matters" | "This dry-run **verifies that the pipeline (split, signal, portfolio, fee model, robustness battery, results-DB append) is wired correctly end to end**. Once real S&P 500 data is wired in, the H1 test becomes meaningful." |
| Abstract Conclusion | "The notebook is therefore a **methodological scaffold** rather than evidence for or against H1" |
| Interpretation (2) | "The asymptotic agreement of the four robustness checks is the **actual methodological evidence**: the pipeline correctly assigns a null result to a null process." |
| verdict cell | 'parked' (= 誠実) |

問題: H1 verdict は 'parked' で誠実だが、投入された 1 cycle 分の作業は
**市場の挙動について 1 bit も知識を生成していない**。Cycle goal の Decision
rule (YES / NO / KICK-UP) のいずれも synthetic data 上では適用不能 (=
Consumer は何の判断もできない) にも関わらず cycle は閉じる。Cycle goal が
事実上 bypass されている。

de facto 成果物が「pipeline が正しく配線されているか」(= 実装の挙動) で
あって、Cycle goal 5 項目で名乗った市場 claim (= 世界の挙動) ではない。

### 観察された自然な誘惑

- 「データ到着までの間に pipeline 整備を済ませておけば、データが来てから
  滑らかに run できる」 → engineering work を research cycle として instantiate
- 「synthetic で random data を流せば leak / accounting bug は検出できるので
  ある意味 sanity check として有意義」 → sanity check は cycle の中ではなく
  engineering side で行うべきだが、その境界が SKILL に書かれていない
- 「verdict は 'parked' なので過剰主張ではない、誠実な dry-run」 → 'parked'
  自体は合理的だが、cycle を **着手する前に** blocked と返すべきだった
  ことを skill が問わない

### 重要な独立性の主張

- F18 は **F15 / F16 (research_goal_layer) と独立**。Cycle goal の 5 項目
  (target_sub_claim_id を含む) はノート header に揃って書かれている。
  4 階層モデルが導入された後でも、F18 は残る。
- F18 は **F17 (carryforward conjunct contribution gate) とも独立**。
  H1 は最初の H で derived ではないので、conjunct gate は発火しない。
- F18 は **F12-F14 (派生 H 表のノート流入) とも独立**。本 case では
  `### Derived hypotheses` 表は登場せず、それでも inversion が生じる。

## F19 — per-H abstract が市場 claim でなく code/pipeline correctness を成果物として記述

H1 が市場 claim ("最初の 3 PC が cross-sectional variance の 50% 超を捕まえ、
PC1 が systematic market factor として機能する") を立て、データは実在し、
PCA は実走、% variance / loading sign distribution の数値も出る。robustness
battery も通る。それにも関わらず、per-H abstract と interpretation セルは
*implementation property* (= computation correctness / library
reconciliation / numerical stability) を named deliverable として書く。

完了 4 gate (bug_review / experiment-review /
research_quality_checklist / achieved_tier ≥ Medium) のいずれにも
「per-H abstract が市場 claim を named deliverable として持つか / 実装の
正しさを named deliverable として持つか」を判定するルールが無い。
silence-as-license。

### Case M (`notebook_M_abstract_misframed.py`) からの抜粋

| 場所 | 抜粋 |
|---|---|
| Purpose ヘッダー | "US large-cap (S&P 500) cross-sectional daily returns における latent factor 構造を特徴づける。" — 市場 claim |
| Cycle goal Decision rule YES | "最初の 3 PC が ≥ 50% variance、PC1 が ≥ 80% names で同符号" — 市場 claim 上の閾値 |
| H1 abstract 第 1 段落 | "**Implementation summary.** PCA was performed on ... The decomposition was computed with `sklearn.decomposition.PCA` and **verified to match a from-scratch eigendecomposition** ..." |
| H1 abstract 第 2 段落 | "**Numerical correctness.** All eigenvalues are non-negative ...; the sum across the full spectrum equals the trace of the empirical covariance matrix to machine precision (relative error 2.3e-15)." |
| H1 abstract Verdict 行 | "**The implementation is correct and reconciles with sklearn's reference**. The threshold (≥ 50% / ≥ 80%) is met on the loading-sign side; the variance-share is just below at 47%." |
| H1 interpretation (2) | "**Numerical evidence that the decomposition is trustworthy.** ... These three checks together establish that the reported numbers reflect the actual eigenstructure of the data and not an implementation artefact." |

問題: 市場 claim (variance share ≥ 50%、loading sign ≥ 80%) と verdict
('parked' on variance share, 'met' on loading) は notebook に書かれて
いるが、abstract の framing の主役は code-correctness。Verdict 行の主節
が「implementation is correct and reconciles with sklearn」で、研究 verdict
が subordinate clause になる。読者が abstract を読み、ノートの named
deliverable を要約しろと言われたら、**「sklearn と一致した PCA を実装した
ことを確認した」と答える可能性が高い**。

### 観察された自然な誘惑

- 「実装の正しさを示しておかないと verdict の信頼性が読者に伝わらない」 →
  bug_review / experiment-review が code 正しさを担保するので、abstract
  本文で再録する必要は無い、を skill が明文化していない
- 「robustness battery / sanity checks の通過自体が claim の一部」 →
  robustness は claim の **限定** を述べる材料 (e.g. 「regime A では
  通る、regime B では通らない」) であって、それ自体が成果物ではない、を
  skill が明文化していない
- 「`sklearn` などの library との一致を示すのは reproducibility 文脈で
  research community に向けた誠実さ」 → reproducibility は code repo / env
  lock / data hash で示すべきもので、abstract の主成果ではない、を skill
  が明文化していない

### 重要な独立性の主張

- F19 は **F1-F8 (本文への履歴 / レビュー用語の流入) と独立**。Case M の
  notebook には reviewer 名 / dimension 名 / step 番号 / `pre_fix` 変数 /
  取り消し線 / `parked-finding` などの違反は無い。それでも市場 claim 不在
  の inversion は起きる。
- F19 は **F18 と独立な経路**。F18 は data 不在で trigger される。F19 は
  data があっても trigger される。両者は別 fix を要する。

## 共通失敗パターン — Cycle goal の bypass

F18 と F19 は具体形が異なるが、共通の構造がある: **Cycle goal の 5 項目で
名乗った claim と、ノート末尾で named deliverable として書かれる成果物が
不一致**。

| 場所 | F18 | F19 |
|---|---|---|
| Cycle goal で名乗った claim | 市場 claim | 市場 claim |
| Decision rule YES / NO / KICK-UP | 市場 claim 上の閾値 | 市場 claim 上の閾値 |
| ノート末尾の de facto 成果物 | pipeline correctness scaffold | implementation correctness verification |
| Decision rule の適用可能性 | 不可能 (synthetic data) | 可能だが abstract は言及しない |

つまり Cycle goal の 5 項目を **書かせる** だけでは inversion は防げない。
ノート末尾の named deliverable が Cycle goal の claim と整合していることを
**チェックする gate** が要る (= F19 GREEN counter)。さらに、Cycle goal の
Decision rule が **事実上適用不能** な状態で cycle を着手しないことを
**チェックする gate** が要る (= F18 GREEN counter)。

## ユーザー指摘との対応関係

| ユーザー要素 | RED で再現された側面 |
|---|---|
| 主体が研究ではなく実装 / コードになる | F18 (Purpose が pipeline-correctness に reframe) + F19 (per-H abstract が implementation property を named deliverable に据える) |
| 研究の成果としてコードがあるのではなく、コードの正しさを確認するために研究 / 実験をしている | F18 (synthetic data 上で「pipeline 正しく配線されているか」を確認する experiment になる) + F19 (実 data で実走しても abstract は「sklearn と一致した PCA を実装した」を主成果として書く) |

両 F-id は **silence-as-license** の異なる露出経路。同じ「研究主体の anchor が
skill 規定にない」根本原因から派生している。

## Scope 限界 — 本 fixture でカバーしない経路

ユーザー指摘の「主体が研究ではなく実装 / コードになる」現象には、
本 fixture (F18 / F19) では covered しない第 3 経路がある:

### Future RED — reconciliation pass の DoD が code-output alignment に偏向

`post_review_reconciliation.md` の Definition of Done (1)–(5):

1. 修正セル以降のすべての依存セルを再走
2. abstract / per-H abstract / interpretation の数値が pipeline 出力と一致
3. すべての figure cell が再生成されている
4. すべての observation cell が再生成後の figure に基づいて書き直されている
5. 既知の全 finding との整合チェック

これらは **artifact-correctness dimension** に偏った DoD で、reconciliation
pass を済ませた後のノート本文の **evidence 内容自体が空でも** DoD は通る。
bug_review が見つけた findings に対する mechanical な code/figure 整合
作業が 1 cycle の **felt deliverable** になる経路がある。

これを再現するには複数ラウンドの bug_review/reconciliation を経た fixture
が要る。本 fixture (F18 / F19) は 1 ラウンド以内で起こる inversion に
focus し、reconciliation 経由の inversion は **future RED phase** で別途
扱う。

## F12-F17 を GREEN で潰しても F18 / F19 は残る

これは GREEN フェーズで重要な区別:

- F12-F14 の counter (派生 H 表をノート本文から退去させ `hypotheses.md` に
  集約) は本 RED に無関係。本 RED の H1 / 派生 H 表は中立。
- F15 / F16 の counter (`research_goal_layer.md` 導入で 4 階層モデル) を
  実施しても、F18 / F19 は残る。Cycle goal 5 項目 / target_sub_claim_id
  が揃っていてもなお、(a) data 不在で synthetic 代替 (b) abstract の
  framing が code 側に寄る、は起き得る。
- F17 の counter (sub-step 1.5 conjunct contribution gate) も無関係。F17 は
  derived H の routing 段階で発火する gate で、本 RED の H1 (= 最初の H)
  には適用されない。

つまり F18 / F19 への counter は F12-F17 とは別経路で必要で、具体的には:

- **F18**: SKILL.md に **data-availability gate** を追加。「期待された
  input data が不在のとき、cycle は BLOCKED (= 着手不可、KICK-UP に近い
  扱い) になり、synthetic 代替で進めることは禁じる」を明文化。pipeline
  整備は engineering work であって research cycle ではない、を anti-
  rationalization 表に追加。
- **F19**: SKILL.md "Completion gate (per Hypothesis)" の 4 gates に
  **「per-H abstract は実装属性 (computation correctness / library
  reconciliation / numerical stability) ではなく、世界の挙動 (mechanism /
  market / regime / instrument) についての claim を named deliverable
  として持つ」** 要件を追加。`notebook_narrative.md` の per-H abstract
  フォーマット規定に「先頭 1 文は市場 claim、implementation 属性は補助
  情報のみ」を追加。anti-rationalization 表に「実装の正しさを示すのは
  研究の主成果ではない、bug_review / robustness が code-correctness を
  担保するので abstract で再録不要」を追加。

詳細は GREEN フェーズで実装。GREEN fixture は `green_verify_research_subject_drift/`
に置く。
