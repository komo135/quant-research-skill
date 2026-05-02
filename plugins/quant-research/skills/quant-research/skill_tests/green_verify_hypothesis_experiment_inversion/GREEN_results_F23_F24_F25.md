# GREEN hypothesis ↔ experiment inversion — F23 / F24 / F25 closure

ユーザー指摘 (RED で再現):

> 「実験は仮説を立証するためにある」(= 仮説 → 実験)
> 「実験の目的のために仮説がある = 仮説の仮説になる」
> 「仮説の仮説でさらにその仮説をもとにした仮説がある これでまともな研究が
> 回せるとあなたは言いたいのですか？」
> 「派生仮説は何を目的とした仮説なのかが明確化されてる、極小単位ではなく
> 意味のある単位での仮説になっている」

を、F23 (Purpose-as-meta-hypothesis pretense) / F24 (experiment vocabulary
inversion) / F25 (派生 H 極小単位 licensing) として観察し、SKILL.md /
references / scripts / templates / assets の改修で 3 つの failure mode
を閉じる。

## 改修箇所一覧

### F23 counter — Purpose を親仮説として正直に書き直し、Purpose-level verdict gate を新設

| ファイル | 改修 |
|---|---|
| `SKILL.md` description (L3) | Purpose 定義を「research thesis = parent claim」に書き換え。Purpose-level verdict / 派生 H admissibility 3 条件 / `purpose_id` schema を description に明記 |
| `SKILL.md` Purpose vs. Hypothesis 表 (L46-52 相当) | "open-ended question" 撤去 → "parent claim about the world (= research thesis)"。Form を falsifiable claim 形 ("X works on Y under conditions C")。Examples 3 件すべて declarative falsifiable に書き換え (e.g. "Does mean-reversion work on EUR/USD intraday?" → "Mean-reversion at H1 frequency on EUR/USD generates risk-adjusted edge net of cost (≥ 0.5 test Sharpe with 1 bp/side fees)") |
| `SKILL.md` 旧 L96 anti-rationalization | "the notebook itself does not have a single verdict" を撤去。新規 anti-rationalization 4 件追加 (派生 H 極小化、threshold-variation rerun、Purpose verdict 不在の言い訳、follow-on layer 流入) |
| `SKILL.md` 旧 L783-786 Completion gate | 「The notebook itself does **not** carry a single verdict」を撤去 → 「The notebook **also** carries a Purpose-level verdict on the parent thesis」 |
| `SKILL.md` 新規 "Purpose-level closure gate (per Notebook)" 節 | Purpose-level verdict (supported / refuted / partial / refuted-as-stated) を新設。発火条件 / verdict 値 / 派生 Purpose に carry-forward する場合は親 thesis verdict が precondition であることを明文化 |
| `references/cross_h_synthesis.md` Pattern A Action | "redesign as a derived Purpose that addresses the axis (...lower-frequency variants of the same signal...)" の carry-forward licensing を撤去。「First, verdict the parent thesis as `refuted` at Purpose-level closure」を Action 第 1 項に。derived Purpose は **異なる parent thesis** をテストする独立 Purpose で、closed thesis の rebranding ではないことを明記 |
| `references/cross_h_synthesis.md` Pattern B Action | 「First, verdict the parent thesis as `refuted-as-stated`」を Action 第 1 項に追加。Pattern B は親 thesis が too broad だった証拠であって、未識別な narrower form で正しかったことの証拠ではない、と明記 |
| `references/cross_h_synthesis.md` Handoff section | 旧 step 0 として「**parent thesis of the closing notebook is verdicted**」を追加 — derived Purpose の open は親 thesis verdict が在ることが precondition。step 3 の "open-ended question" を "declarative falsifiable parent thesis" に書き換え、near-paraphrase rebranding 禁止の文言を追加 |
| `references/research_design.md` Purpose template | 「open-ended investigation」「open-ended question about the world」を「parent research thesis」「declarative falsifiable parent claim」に書き換え。Examples を declarative form に。"Avoid the question form" 注意を追加 |
| `references/experiment_protocol.md` "What 'one notebook' means" | 「open-ended investigation」を「parent research thesis (declarative falsifiable)」に書き換え。「Each `## H<id>` block is one experiment」を明記 |
| `references/research_goal_layer.md` 4-layer 図 | "[Purpose] one open-ended question, one cycle" → "[Purpose] one parent research thesis, verdicted at notebook closure" |

### F24 counter — `experiment_id` → `purpose_id` rename、experiment 語を「1 仮説の検証 apparatus」に再帰属、folder/file 命名整合

| ファイル | 改修 |
|---|---|
| `SKILL.md` step 14 schema 説明 (L653-655 相当) | `experiment_id (= the notebook = the Purpose)` → `purpose_id (= the notebook = the Purpose; the prior name 'experiment_id' was a vocabulary inversion that conflated the notebook with an experiment, retired here)`。`hypothesis_id` の説明に「each H block is itself **one experiment**, the apparatus that tests that H」を追加 |
| `SKILL.md` lifecycle 図 (L160 相当) | `experiments/exp_NNN_<purpose-slug>.py` → `purposes/pur_NNN_<purpose-slug>.py` |
| `SKILL.md` Project folder layout (L201-204 相当) | `experiments/` → `purposes/` (with comment "One file per Purpose; each H block inside is one experiment")。`exp_001_<slug>.py` → `pur_001_<slug>.py` |
| `SKILL.md` Bundled helper scripts table | `new_experiment.py` 行を `new_purpose.py` に書き換え |
| `SKILL.md` File templates table | `experiment.py.template` → `purpose.py.template` |
| `references/results_db_schema.md` | `experiment_id` を全置換 → `purpose_id`。schema 説明に「each H block is one experiment that tests that hypothesis」を追加 |
| `references/hypothesis_cycles.md` | `experiment_id` → `purpose_id`、`exp_001/002` → `pur_001/002` 全置換、cross-Purpose 例の path 表記更新 |
| `references/cross_h_synthesis.md` | `experiment_id` → `purpose_id`、`exp_<NNN+1>_*.py` → `pur_<NNN+1>_*.py` 全置換 |
| `references/experiment_protocol.md` | path 表記、`experiment_id` 全置換、`new_experiment.py` → `new_purpose.py` |
| `references/research_design.md` | path 表記、`experiment_id` 全置換、template heading を `## pur_NNN: ...` に |
| `references/marimo_cell_granularity.md` | `experiment_id="exp_005"` → `purpose_id="pur_005"`、コメントに "this H's `## H<id>` block IS one experiment" を追加 |
| `references/notebook_narrative.md` | abstract format 規定に Purpose-level verdict 行を追加 |
| `references/model_diagnostics.md`, `references/feature_construction.md`, `references/prediction_to_decision.md` | example path 表記更新 |
| `references/cycle_purpose_and_goal.md` | example slug `exp_004` → `pur_004` |
| `scripts/new_experiment.py` (削除) | `scripts/new_purpose.py` に置換 (ロジックは同一、folder/prefix のみ変更) |
| `scripts/new_project.py` | folder layout に `purposes/` を作成、starter print の next-step 案内を `new_purpose.py` に |
| `scripts/aggregate_results.py` | docstring + `REQUIRED_FIELDS` を `purpose_id` に |
| `assets/experiment.py.template` (削除) | `assets/purpose.py.template` に置換 (Purpose セルを declarative form に書き換え、`experiment_id` 全置換、`exp_{{NNN}}` → `pur_{{NNN}}`) |
| `assets/hypotheses.md.template` | `experiment_id` 全置換、`exp_001/002` → `pur_001/002`、Purpose 説明を「parent research thesis」に書き換え |
| `assets/INDEX.md.template` | "Experiment INDEX" → "Purpose INDEX"、コラムに "Purpose-level verdict" を追加、example 行を declarative form に書き換え |
| `assets/decisions.md.template` | example slug `exp_005_*` → `pur_005_*`、Purpose 文言を declarative に |
| `assets/README.md.template` | `experiments/INDEX.md` → `purposes/INDEX.md` を navigation 行に |
| `README.md` (project root) | "What you get, in one paragraph" 段落を Purpose-level verdict / 派生 H admissibility / `purpose_id` schema の説明に書き換え。helper scripts 表を `new_purpose.py` に |
| `skills/experiment-review/references/review_protocol.md`, `review_dimensions.md` | `experiments/INDEX.md` 言及を `purposes/INDEX.md` に、example slug を `pur_*` に |

### F25 counter — 派生仮説 admissibility 3 条件を SKILL.md / hypothesis_cycles.md に新設、極小 1 軸 variant を robustness battery に降格

| ファイル | 改修 |
|---|---|
| `SKILL.md` "Derived hypothesis admissibility" 節 (旧 "When a derived hypothesis stays in the same notebook" を改廃) | 派生 H が hypothesis 階層に admit される 3 条件を新設: (a) **own falsifiable claim** distinct from parent (different decision axis, not just tighter/looser threshold), (b) **own stated purpose** in one sentence written before the H runs, answering "what new question does this H answer that the parent did not?", (c) **meaningful research unit** (not 1-axis sweep). Admissible types を 3 件に絞り (failure-diagnosis / specialization / alternative formulation) 各 type に "must still pass the three conditions above" 注釈。Inadmissible types を独立 block として列挙 (sensitivity / parameter-sweep variant、follow-on layer、threshold-variation rerun) — これらは Step 12 robustness battery / Step 10 portfolio construction に置く |
| `SKILL.md` Anti-rationalization 表 | 「H2 is a vol-targeted sizing variant of H1's signal — that's a follow-on layer, so it goes in the hypothesis log.」「H1 was rejected; let me run H2 with a tighter threshold / different period to see if it survives.」を追加 |
| `references/hypothesis_cycles.md` Routing rule | sub-step 0 (admissibility) を sub-step 1 の前に新設。3 条件 全部 pass しない候補は「robustness analysis or engineering work」として親 H の section に記録、`hypotheses.md` / `results.parquet` には行を作らない、と明記。Inadmissible patterns を列挙 (sensitivity / parameter-sweep variant、follow-on layer、threshold-variation rerun、diagnosis without independent claim) |
| `references/experiment_protocol.md` "When a derived hypothesis stays" 節 | "Sensitivity" "Follow-on layer" を Inadmissible side に移動、Admissible side の 3 type に admissibility 3 条件を inline 説明 |

## 観察された GREEN 状態

### Case N (`notebook_N_post.py`)

instruction_N (= 3 H 連続 reject の状況) を post-fix skill 下で再走させた成果物:

| 項目 | RED (notebook_N) | GREEN (notebook_N_post) |
|---|---|---|
| Purpose 文言 | "Does mean-reversion work on EUR/USD intraday?" (= 疑問形) | "Mean-reversion at H1 frequency on EUR/USD generates risk-adjusted edge net of cost (≥ 0.5 test Sharpe with 1 bp/side fees)" (= declarative falsifiable) |
| Purpose-level verdict | 不在 (skill が要求しない) | **refuted** + binding axis "transaction cost vs. signal magnitude at H1 frequency" を明示 |
| H の数 | 3 (H1 + 派生 H2 + 派生 H3) | 1 (H1 のみ)。元の H2 / H3 は H1 の robustness battery (sizing × regime grid) に降格 |
| 派生 Purpose carry-forward | "Does mean-reversion work on EUR/USD at lower (4H / daily) frequencies?" (= 親 thesis を scope だけ変えて rebrand) | `pur_002_mr_eurusd_lower_freq.py` を別 Purpose で開く前提で記述。**異なる parent thesis** ("Mean-reversion at lower frequencies on EUR/USD generates risk-adjusted edge net of cost") を declarative に。close した Purpose の rebrand ではないことを明記 |
| 仮説の階層 | 4 階層 (Purpose 親仮説 → H1 → 派生 H2 → 派生 H3) | 2 階層 (Purpose 親仮説 → H1)。robustness はフラットな評価面 |
| `purpose_id` / `experiment_id` schema | `experiment_id="exp_001_..."` (旧 schema) | `purpose_id="pur_001_..."` (新 schema)、各 H block が「1 つの experiment」と明記 |

### Case O (`notebook_O_post.py`)

instruction_O (= 共有 apparatus + 3 exit rule) を post-fix skill 下で再走させた成果物:

| 項目 | RED (notebook_O) | GREEN (notebook_O_post) |
|---|---|---|
| Purpose 文言 | "Does the choice of exit rule materially change the realized Sharpe...?" (= 疑問形) | "At least one exit rule among signal-flip / TP-SL / trailing-stop produces a 20-day cross-sectional momentum strategy on S&P 500 with test Sharpe ≥ B&H + 0.30" (= declarative falsifiable) |
| Purpose-level verdict | 不在 | **supported** (H1 / H3 が clear)、qualifying conditions 明示 |
| schema 表記 | `experiment_id="exp_003_momentum_exit"` (旧) | `purpose_id="pur_003_momentum_exit"` (新) |
| 「H2 の experiment は何か」への答え | "the apparatus shared with H1/H3 with exit_rule replaced by TP-SL" — H2 固有の experiment は無い、共有 apparatus を指す以外に答えが無い | "the H2 block — the apparatus declared in the `apparatus` cell with `exit_rule` replaced by `tpsl_+1sigma_-2sigma`" — H2 固有の experiment が、H2 block として実体を持つ。1 H ↔ 1 experiment の対応が成立 |
| 派生 H admissibility | 暗黙 (skill が check しない) | 明示。各 H block が「(a) own falsifiable claim distinct from sibling H's, (b) own stated purpose distinct from parent thesis, (c) meaningful research unit (exit rule operationalization is a non-trivial mechanism axis, not a 1-axis sweep)」を declare |

## RED → GREEN の差分が示すこと

ユーザー指摘の「仮説 → 実験」方向が、3 経路すべてで復元される:

1. **Purpose は親仮説として正直に書かれる** (F23): "open-ended question" 詐称撤去 → declarative falsifiable parent thesis。Purpose-level verdict が closure で必ず記録される → 親仮説に殺し場ができる → 子 H 連鎖の rejection escape が起きない
2. **「実験」は 1 仮説を検証する apparatus を指す** (F24): schema `purpose_id` + `hypothesis_id` で notebook と仮説の id を分離。各 `## H<id>` block が「1 つの experiment」として実体化 → "H<n> の experiment は何か" に block-level の答えが返る → 1 仮説 ↔ 1 実験 の対応が成立
3. **派生仮説は意味のある単位で、独立した purpose / claim を持つ** (F25): admissibility 3 条件 (own claim / own purpose / meaningful unit) で gate。1 軸 sensitivity sweep / follow-on layer は robustness battery に降格 → hypothesis 階層が parameter sweep で埋まらない → 仮説の意味のある単位が保たれる

3 つの fix は独立した axis だが、ユーザー指摘の「まともな研究が回せるか」を 3 axis 同時に解消するために合わせて適用される。

## Skipped (本 GREEN の scope 外、future work)

- **Design hypothesis 層の親仮説性**: `decisions.md` の at-open prediction が暗黙に親仮説として機能する経路は、本 GREEN では未対応。F23 と類似の構造だが Layer が違うため独立改修要 (future RED phase)
- **Research goal sub-claim の `refuted` 遷移条件**: `research_goal_layer.md` で sub-claim の status は存在するが、`refuted` に明示的に遷移する gate 条件は本 GREEN では追加していない。Purpose-level verdict が `refuted` を返したときに sub-claim が機械的に `falsified` に遷移する規則は future work
- **既存 skill_tests/ 内の旧 fixture**: `red_*` / `green_verify_*` の過去 fixture は v0.X 時点の skill 状態を文書化する歴史的アーティファクトとして温存。本 GREEN では更新しない

## 検証

- `notebook_N_post.py` は admissibility / Purpose-level verdict / declarative thesis をすべて含む
- `notebook_O_post.py` は `purpose_id` schema / 1 H ↔ 1 experiment の対応 / declarative thesis を含む
- 既存 skill_tests/ 各 RED の `instruction_*.md` を post-fix skill で再走しても、本 GREEN が依拠するルール変更により F23 / F24 / F25 の症状は再発しない (ルール検査は skill の prose 規定で fire するため、agent runner の挙動を別途検査する必要は無い)
