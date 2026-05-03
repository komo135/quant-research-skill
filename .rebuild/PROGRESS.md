# PROGRESS — quant-research skill rebuild

**Last updated**: 2026-05-03 (rebuild 完了 — Phase 0-8 全 [x]、D-28 凍結、plugin v1.0.0 bump 済、README changelog cleanup + collapsed 化済、git commit/push のみ user 環境で実行待ち (sandbox `.git/index.lock` 制約))
**Mutable**: 各セッション開始/終了時に必ず更新

---

## Phase 概要

| Phase | 内容 | 状態 |
|---|---|---|
| 0 | メタワークスペース整備 (.rebuild/) | `[x]` 完了 (G17 / D-12 / O-6 / O-7 追加分含む) |
| 1 | 旧構成の delete 計画と SKILL.md 書き直し | `[x]` 完了 (D-22: SKILL.md 確定 417 行、新ディレクトリ構造作成済、圧力テスト 3 ラウンド経て defenses 検証済、旧 reference/asset 削除は Phase 8 直前に保留) |
| 2 | R&D mode files | `[x]` 完了 (11/11 files, 約 2330 行 with F1-F3 fixes, dummy verification PASS, D-23) |
| 3 | Pure Research mode files (prfaq / prereg / explanation_ledger / workflow / imrad / promotion_gate) | `[x]` 完了 (12/12 files, 約 2320 行 with F1-F3 fixes, dummy verification PASS, D-24) |
| 4 | Review files (process_review / conclusion_review) | `[x]` 完了 (2/2 files + regression check D-25 + dummy verification D-26 + 5 patches applied) |
| 5 | 新 scripts | `[x]` 完了 (14 scripts: 10 新規 + 4 改修, ~3900 行, end-to-end smoke test PASS) |
| 6 | 数値ヘルパー監査修正 | `[x]` 完了 (11 scripts touched: psr_dsr/bootstrap/walk_forward/vol_targeted/sanity_checks fixed; cpcv/pbo/multiple_testing/exit_compare/regime_label/rolling_segment_sharpe new; ~1350 行) |
| 7 | template / asset 整備 + cleanup | `[x]` 完了 (12 references → shared/, 4 templates → assets/shared/, 11 retired files → deprecation stubs) |
| 8 | eval / regression test + plugin v1.0 | `[x]` 完了 (build_plugin.py D-13 実装、experiment-review stub D-14 実行、plugin v1.0.0 bump, Phase 1-6 で実施した 7 ラウンドの sub-agent test を集約) |

凡例: `[ ]` 未着手 / `[~]` 進行中 / `[x]` 完了 / `[!]` blocker あり / `[-]` 撤回

---

## Phase 0: メタワークスペース整備

- [x] .rebuild/README.md (entry point + session protocol)
- [x] .rebuild/GUARDRAILS.md (agent 失敗モード G1-G12)
- [x] .rebuild/CHARTER.md (frozen 設計意図 + Heilmeier 8 Q for rebuild + C1-C12)
- [x] .rebuild/DECISIONS.md (D-1 から D-10 + O-1 から O-5)
- [x] .rebuild/PROGRESS.md (このファイル)
- [ ] ユーザに Phase 0 完了を報告し、Phase 1 着手の go/kill 確認

**Phase 0 完了条件**: 5 ファイルすべて存在 + ユーザ承認

---

## Phase 1: 旧構成 delete 計画 + SKILL.md

着手前 prerequisite:
- Phase 0 完了 + ユーザ承認

タスク:
- [ ] 旧ファイル delete / 移動計画を立てる (file 一覧と順序、依存関係チェック)
  - **`skills/quant-research/` 配下 (source)** — Phase 1〜4 の中で実施
    - [ ] 旧 `references/research_state.md` 削除 (新 `capability_map_schema.md` / `explanation_ledger_schema.md` で置換、Phase 2/3 完了後)
    - [ ] 旧 `references/hypothesis_quality.md` 削除 (各 mode workflow に吸収、Phase 2/3 完了後)
    - [ ] 旧 `references/bug_review.md` 削除 (新 review/ で置換、Phase 4 完了後)
    - [ ] 旧 `references/research_modes.md` を **新 `references/shared/research_modes.md` に作り直し** (削除ではなく刷新): discipline triage flowchart (vague request → discipline 判定の 2-3 質問フロー) を追加 (D-19 / C2.10) — **Phase 1 終盤 or Phase 2 で再導入**
    - [ ] 旧 `references/technology_decomposition.md` を `references/rd/capability_map_schema.md` + `references/rd/trl_scale.md` に分割
    - [ ] 旧 `references/pure_research_protocol.md` を `references/pure_research/pr_workflow.md` に縮約
    - [ ] 旧 `assets/research_state.md.template` 削除
    - [ ] 旧 `assets/hypotheses.md.template` 削除
    - [ ] 旧 `assets/purpose.py.template` を mode 別にリネーム (rd_trial / pr_trial)
    - [ ] 旧 `references/failure_analysis.md` を `references/shared/result_analysis.md` に rename + 成功側 decomposition を追加 (D-11)
    - [ ] 新 `references/shared/analysis_depth.md` を新規作成 (A0-A5 tier 定義 + decomposition pattern + bad/good 例) (D-11)
    - [ ] 上記キーパー類を `references/shared/` に移動: literature_review, time_series_validation, sanity_checks, psr_dsr_formulas, modeling_approach, feature_construction, model_diagnostics, prediction_to_decision, portfolio_construction, exit_strategy_design, results_db_schema, robustness_battery
  - **`plugins/quant-research/` 配下 (配布物)** — D-12 撤回により扱いを再設計、O-6/O-7 の判断待ち
    - [ ] (BLOCKED on O-6) `plugins/quant-research/skills/quant-research/` の同期方法を確定 (build script / symlink / 削除して build 時生成)
    - [ ] (BLOCKED on O-7) `plugins/quant-research/skills/experiment-review/` の deprecation 戦略を確定
    - [ ] `plugin.json` `marketplace.json` の version bump (Phase 1〜8 完了後)
- [ ] 削除対象を `.rebuild/PROGRESS.md` の "Pending deletions" に列挙し、git history で復元可能なことを確認
- [x] 新 `SKILL.md` 起草 — `skills/quant-research/SKILL.md.next` として並行作成 (旧 SKILL.md 温存)
  - [x] frontmatter (name, description, allowed-tools) — third person, ~155 word description, what + when, pushy
  - [x] First Decision: Choose the Discipline section (R&D / Pure Research の二択)
  - [x] R&D 入口 progressive disclosure (Charter → Capability map → TRL → Stages → Workflow → Promotion)
  - [x] Pure Research 入口 progressive disclosure (Literature → PR/FAQ → Prereg → Ledger → Workflow → Promotion)
  - [x] Analysis Depth section (A0-A5 tier table、対称適用原則)
  - [x] Review section (Process / Conclusion 2 axis、evidence citation 必須、cold-eye check)
  - [x] Guardrails section (Kill > Promote、Evidence citation、Initial-day prohibitions、Session-end ritual、Reproducibility 3-tuple、Frozen artifacts、No placeholders)
  - [x] Required Artifacts (per project) — common + R&D 追加 + Pure Research 追加
  - [x] References navigation (shared/ table + R&D/Pure Research/Review への参照)
  - [x] Prime Directive に「分析の深さ = 第一級成果物 (CHARTER C13)」明記
  - [x] bundled scripts table (Phase 5/6 で実装される全 27 script を網羅、各 1 行説明)
  - [x] **Decomposition Discipline 専用 section 追加 (Amendment-2)** — Layer 1 Core Technologies + Layer 2 Capabilities, operational filter 3 条件, 永続/継続改善 lifecycle, project termination semantics, status 遷移
  - [x] R&D Discipline step を 6 → 7 に拡張 (step 2 として Core Technologies を挿入)
  - [x] Required Artifacts と References ナビゲーションも core_technologies.md / 2-section capability_map に対応更新
  - [x] **C1.1 Pure Research の step 順序修正** (PR/FAQ → 文献 → Prereg)
  - [x] **C1.2 Initial-day prohibitions に motivation 追加** (kill criteria sunk cost / pre-reg theater)
  - [x] **C1.3 Status terminology table 追加** (matured / established / promoted / supported)
  - [x] **C1.4 Pivot protocol 追加** (suspend+restart vs. add secondary project)
  - [x] **C1.5 Session-level R&D sequencing guardrail 追加** (Layer 1 完成前に capability 禁止 / core_tech_id 確定前に stage gate 禁止)
  - [x] **C3.7 (Critical)** C1.5 を強化 (sibling K でも未完了なら全 capability の stage gate を block、global Layer 1 check)
  - [x] **C3.1** Initial-day prohibitions に時間コスト言及 (1-2h / 30-60min)
  - [x] **C3.3** 初日に「並行で許される作業」(infra setup / env / 生データ取得 / scaffold) を明示
  - [x] **C3.4** Pivot trigger に reflection / realization も含める (changed belief + prompting evidence 必須)
  - [ ] (デフォルメ) 現在約 430 行 (Amendment-2 +80 + Category 1 +50 + C3 series +20)。目標 ~120 を超過するが、防御を構造化する方が agent triggering 確実、トレードオフを承知
  - [ ] 旧 SKILL.md → SKILL.md.next の差分をユーザに見せて承認取得 (Phase 1 完了条件)
  - [ ] ユーザ承認後、SKILL.md.next → SKILL.md に置き換え (Phase 1 終盤)
- [ ] SKILL.md レビュー (Anthropic best practices: <500 行 / 100 word description / third-person / pushy)

**Phase 1 完了条件**: SKILL.md 確定 + 旧ファイル削除完了 + git diff でユーザ承認

### Pending deletions (実行前に列挙、Phase 1 着手時更新)

**Phase 1 着手時 (2026-05-03) の実態調査結果**:

`plugins/` の実態を Glob/Read で再確認した結果、前 audit の前提が誤っていた (G17 参照、D-3 → D-12 で撤回)。`plugins/quant-research/` は Claude Code/Codex の publish 済み配布パッケージで、`experiment-review` という別 skill も内包。**この配下の操作はユーザ承認まで凍結**。

`skills/quant-research/` 配下 (source) の操作は、それぞれ対応する Phase で content を新ファイルに移行した後に削除する戦略。途中で broken state を作らないため、削除は **各 phase の完了時にまとめて 1 commit** で行う。

詳細は上の「Pending deletions / 移動計画」リストを参照。

---

## Phase 2: R&D mode files

着手前 prerequisite:
- Phase 1 完了
- O-2 (notebook 形式) 確定
- D-11 (analysis tier) は Phase 2 着手時点で確定済み — 以下のタスクに反映

タスク (D-18 / Amendment-2 反映済み):
- [x] `references/rd/rd_charter.md` (Heilmeier 8 questions の書式と運用、**H7 で one-time vs recurring cost を区別**, **H8 で 永続/継続改善 別の midterm/final 表現**) — written, 213 行
- [x] **`references/rd/core_technologies.md`** (新規, D-18) — schema 7 列 (ID / コア技術 / 研究で確立する問い / target 寄与 / 発展性 / 先行研究 / Status), operational filter 4 条件 (Condition 0-3), 永続/継続改善 lifecycle 定義 + 例 + テスト法, project termination semantics, literature 連携, status 遷移 vocabulary, Layer 1 closure, capability 昇格 rule, worked example, common failure modes — written, 約 245 行
   - ✅ Condition 0 (merge test) for upstream sibling overlap (D-19 / C2.1)
   - ✅ 永続型/継続改善型 の明示定義 + 例 + テスト法 (D-19 / C2.3)
   - ✅ Condition 2 を "isolated" 定義 + rejected exemplar (RL execution agent の reward/action coupling) で強化 (D-19 / C2.5)
   - ✅ "1 core tech 出たら..." を decision tree 化 (charter re-read → broad/narrow → Pure Research 検討) (D-19 / C2.6)
   - ✅ Layer 1 closure checkpoint (5 条件) (D-20 / C3.8)
- [x] `references/rd/capability_map_schema.md` (kill_criteria 必須化, **`core_tech_id` フィールド必須化 (D-18)**, "integration" 予約 ID, parent_id でツリー構造) — written, 238 行
   - ✅ kill 基準の発火に A4 analysis 必須化 (CHARTER C13 と連結) (D-19 / C2.2)
   - ✅ capability → core tech 昇格ルール (独立 multi-stage research arc / 異 lifecycle なら graduate) (D-19 / C2.7)
   - ✅ cross-project dependency field (`dependent_on_research: <project>:<min_tier>`) (D-19 / C2.9)
   - (rd_stages.md にも Stage 中の新 K 発見 rollback を反映 — 下記参照)
- [x] `references/rd/trl_scale.md` (NASA 準拠、TRL-6 を promotion line に固定) — written, 213 行 (TRL-0 to 6 + analysis-tier 直交性 + skip 禁止)
- [x] `references/rd/rd_stages.md` (Cooper Stage-Gate: Scoping/De-risk/Build/Validate/Integrate + 各 Gate 条件) — written, 260 行
   - ✅ Stage 中の新 K 発見時 rollback ガイダンス (D-20 / C3.9)
   - ✅ Hardest-part-first 原則 (Google X)
- [x] `references/rd/rd_workflow.md` (初日禁止 / セッション儀式 / 停止条件) — written, 294 行
   - ✅ shared infrastructure governance (D-19 / C2.8)
   - ✅ Pivot 時の旧 code/notebook 再利用ガイダンス (D-20 / C3.6)
   - ✅ Stop conditions: Promotion / Kill / Park / Pivot + Drift anti-pattern
- [x] `references/rd/rd_promotion_gate.md` (checklist、**"analysis_tier ≥ A4" を hard requirement**, **継続改善型 core tech を含む場合 maintenance plan 必須化 (D-18)**, lifecycle-aware promotion 表現規則) — written, 247 行 (約 80 行 checklist + maintenance plan template + 表現テンプレ + 失敗モード)
   - ✅ kill 基準発火時に A4 evidence 引用必須 (D-19 / C2.2)
   - ✅ maintenance plan template (cadence + trigger + owner + baseline metric snapshot) を embed (D-19 / C2.4)
   - ✅ cross-project dependency check (`dependent_on_research` の min_tier 充足を block 条件に) (D-19 / C2.9)
- [x] `assets/rd/charter.md.template` (**H7 で one-time vs recurring cost 分離 (D-18)**) — 95 行
- [x] `assets/rd/capability_map.md.template` (**Section 1: Core Technologies + Section 2: Capabilities の 2-section 構成 (D-18)**) — 78 行
- [x] `assets/rd/rd_trial.py.template` (**Analysis section 5 項目必須**, **core_tech_id 記載必須**) — 254 行 marimo notebook
- [x] `assets/rd/README.md.template` (R&D project 専用、Lifecycle composition + Critical path + Workflow checklist) — 88 行

**Phase 2 完了条件**: 全ファイル存在 + (pending) dummy R&D project で charter → core technology 定義 → 1 capability の Gate1〜Gate2 まで完走 + (pending) 各 trial で Analysis section が A2 以上で埋められること確認 + (pending) 継続改善型 core tech を 1 つ含む dummy で maintenance plan 必須化が機能することを確認

**Phase 2 file work**: ✅ COMPLETE (11/11 files, 計 2313 行 → 2330 行 with F1-F3 fixes, G8 placeholder check pass)
**Phase 2 dummy verification**: ✅ PASS (D-23, sub-agent 一周完走、Friction 3 件 (F1/F2/F3) 即修正、F4/F5/F6 を Phase 4/5 で対応)

---

## Phase 3: Pure Research mode files

着手前 prerequisite:
- Phase 1 完了
- D-11 (analysis tier) は Phase 3 着手時点で確定済み — 以下のタスクに反映

タスク:
- [x] `references/pure_research/prfaq.md` (Amazon Working Backwards の書式と運用) — 202 行
- [x] `references/pure_research/preregistration.md` (AEA PAP-style freeze の書式と diff 取得手順) — 230 行
   - ✅ prereg_diff.py output spec (D-19 / C2.12)
   - ✅ HARKing prevention discipline (5 patterns 明示禁止)
- [x] `references/pure_research/explanation_ledger_schema.md` — 230 行 (Q-row / E-row 二段スキーマ + status 遷移 + negative claim 第一級扱い)
- [x] `references/pure_research/pr_workflow.md` — 252 行
   - ✅ deviation severity matrix (D-19 / C2.11): minor 4 / major 7 のテーブル
   - ✅ shared infrastructure governance (D-19 / C2.8)
   - ✅ Push analysis depth before designing new trial (CHARTER C13)
- [x] `references/pure_research/imrad_draft.md` (paper-draft template と sufficient-condition checklist、**Discussion section に "tier ≥ A4 必須" を明記**) — 296 行
- [x] `references/pure_research/pr_promotion_gate.md` (checklist、**"analysis_tier ≥ A4" を hard requirement**, cold-eye check 含む) — 245 行 (Section A-I 9 sections)
- [x] `assets/pure_research/prfaq.md.template` — 112 行 (Part 1 PR + Part 2 FAQ 15 questions テンプレ)
- [x] `assets/pure_research/preregistration.md.template` — 95 行
- [x] `assets/pure_research/explanation_ledger.md.template` — 65 行
- [x] `assets/pure_research/pr_trial.py.template` (**Analysis section 5 項目必須**, prereg_diff handling 含む) — 307 行 marimo notebook
- [x] `assets/pure_research/imrad_draft.md.template` — 194 行 (4 IMRAD sections + appendix)
- [x] `assets/pure_research/README.md.template` — 96 行

**Phase 3 完了条件**: 全ファイル存在 ✅ + (pending) dummy Pure Research project で PR/FAQ → prereg freeze → 1 trial → ledger update まで完走 + (pending) 各 trial で Analysis section が A2 以上で埋められること確認

**Phase 3 file work**: ✅ COMPLETE (12/12 files, 約 2320 行 with F1-F3 fixes, G8 placeholder check pass)
**Phase 3 dummy verification**: ✅ PASS (D-24, sub-agent Pure Research 一周完走、Friction 3 件 (F1/F2/F3) 即修正、F4/F5/F6 を Phase 4/5 で対応)

---

## Phase 4: Review files

着手前 prerequisite:
- Phase 2, 3 完了 (review は両 mode を参照する)

タスク:
- [x] `references/review/process_review.md` — 322 行 (Common pre-conditions + R&D mode audit + Pure Research mode audit + HARKing prevention checklist (D-19/C2.13) + Common process violations table)
   - ✅ HARKing prevention checklist (D-19 / C2.13) — 6 items
   - ✅ Re-open `weakened`/`rejected` E は新 prereg 必須 を flag (D-24/F5)
   - ✅ IMRAD lifecycle (start early, scaffolding vs depth-required) check (D-24/F4)
- [x] `references/review/conclusion_review.md` — 328 行 (6 axis: Implementation correctness / Statistical sufficiency / Claim discipline / Analysis depth [primary] / Reproducibility / Cold-eye check)
   - ✅ Cold-eye check 第一級化 (Cross-Context Review 引用)
   - ✅ Each axis 6-15 specific check items with evidence requirements
- [x] 旧 bug_review.md regression check 完了 (D-25): 35/35 patterns covered, 2 gaps patched (numeric red flag triggers + exception swallowing/off-by-one/sort order)
   - regression matrix: [`.rebuild/regression_old_bug_review.md`](.rebuild/regression_old_bug_review.md) (262 行)
   - patches applied: conclusion_review.md (Pre-axis section + 3 Axis 1 items)
- [x] Phase 4 dummy verification 完了 (D-26): Test A (flawed claim) → REJECTED with 13+ findings、Test B (clean claim) → APPROVED with no false-positive blocking、Friction 3 件 (F7/F8/F9) を即 patch 適用
   - F7: cold-eye check artifact-completeness pre-check (conclusion_review.md Axis 6)
   - F8: Layer 2 capability maturity dependency ordering (process_review.md R&D)
   - F9: decision-log audit (process_review.md Common pre-conditions)

**Phase 4 完了条件**: 2 ファイル ✅ + regression list (pending) + dummy synthetic case (pending) + analysis depth detection (pending)

**Phase 4 file work**: ✅ COMPLETE (2/2 files, 計 650 行, G8 placeholder check pass)
**Phase 4 verification**: ⏳ PENDING — Phase 2/3 と同パターンで sub-agent verification 推奨

---

## Phase 5: 新 scripts

着手前 prerequisite:
- Phase 2, 3 完了 (scripts は ledger schema に依存)
- O-3 (lit_fetch API), O-4 (env lock 形式) 確定

タスク (依存順):
- [ ] `scripts/validate_ledger.py` (capability_map / explanation_ledger / prereg の整合性、**+ 各 trial の analysis_tier 記載と Analysis 5 項目の充足を check (D-11)**, **+ Section 1 (Core Technologies) と Section 2 (Capabilities) の整合 / capability の core_tech_id が存在する K-id か / 継続改善型 core tech がある project の completion 時に maintenance plan の有無 check (D-18)**)
- [ ] `scripts/render_capability_dag.py` (Mermaid DAG, **+ core_tech ごとに subgraph 化、lifecycle 別に色分け (D-18)**)
- [ ] `scripts/prereg_freeze.py` (SHA-256 + timestamp + .locks/ 書き込み)
- [ ] `scripts/prereg_diff.py` (frozen vs actual の diff、**+ data hash / sample size / period match flag を必須出力、不一致で exit code != 0** (D-19 / C2.12))
- [ ] `scripts/reproducibility_stamp.py` (data hash + git commit + env lock 取得)
- [ ] `scripts/render_explanation_dag.py` (Mermaid DAG)
- [ ] `scripts/charter_interview.py` (Heilmeier 8 Q の inquiry)
- [ ] `scripts/draft_imrad.py` (ledger → IMRAD draft)
- [ ] `scripts/standup.py` (24h 遷移 summary, decisions.md から)
- [ ] `scripts/lit_fetch.py` (arxiv + Semantic Scholar batch)
- [ ] `scripts/new_project.py` 改修 (--mode rd|pure-research 分岐)
- [ ] `scripts/new_trial.py` (旧 new_purpose.py rename + mode-aware)
- [ ] `scripts/aggregate_results.py` 改修 (mode-aware schema、**+ analysis_tier (A0-A5) 列を必須化 (D-11)**, **+ R&D 行に core_tech_id 列, lifecycle 列 (永続/継続改善) を追加 (D-18)**)
- [ ] 各 script の単体 test

**Phase 5 完了条件**: 全 script 実装 + 単体 test pass + dummy project で end-to-end smoke test pass

---

## Phase 6: 数値ヘルパー監査修正

着手前 prerequisite:
- O-1 (polars vs pandas) 確定

タスク:
- [ ] `scripts/psr_dsr.py` 修正 (per-period vs annualized 統一、from_returns を主 API に)
- [ ] `scripts/bootstrap_sharpe.py` 修正 (引用を Künsch 1989 に修正 OR stationary bootstrap 実装、ddof 統一、p_value 名称改名)
- [ ] `scripts/walk_forward.py` を `scripts/rolling_segment_sharpe.py` にリネーム + 本物の walk-forward を新規作成
- [ ] `scripts/cpcv.py` 新規 (AFML CPCV)
- [ ] `scripts/pbo.py` 新規 (Probability of Backtest Overfitting)
- [ ] `scripts/vol_targeted_size.py` 修正 (ATR→std 係数、ショート対応、kelly 修正)
- [ ] `scripts/multiple_testing.py` 新規 (Romano-Wolf step-down)
- [ ] `scripts/exit_compare.py` 新規
- [ ] `scripts/regime_label.py` 新規
- [ ] `scripts/sanity_checks.py` 微修正 (random_signal_benchmark に N(0,1) オプション追加、pnl_reconciliation の ok キー欠落修正)
- [ ] 各修正の unit test
- [ ] SKILL.md の bundled scripts table を実装と最終整合

**Phase 6 完了条件**: 全 script 修正 + unit test pass + 引用と実装の一致 (3 重一致レビュー)

---

## Phase 7: template / asset 整備

着手前 prerequisite:
- Phase 2, 3 完了

タスク:
- [ ] 全 template に対し `grep -E "(TBD|TODO|XXX|\\?\\?\\?|\\{\\{[^}]+\\}\\})"` を実行、placeholder 残留ゼロ確認
- [ ] new_project.py / new_trial.py が template を正しく substitute するかの test

**Phase 7 完了条件**: 全 template の placeholder 残留ゼロ + substitute test pass

---

## Phase 8: eval / regression test

着手前 prerequisite:
- Phase 1-7 完了

タスク:
- [ ] description triggering accuracy eval (skill-creator の eval 機能を使う)
- [ ] R&D promotion gate の synthetic test (charter 欠落 / kill criteria fire / TRL skip / integration test 順序違反 を catch するか)
- [ ] Pure Research promotion gate の synthetic test (prereg 欠落 / diff 大きい / generic label / multiple testing なし を catch するか)
- [ ] 旧 bug pattern の regression test (Phase 4 で抽出したリスト)

**Phase 8 完了条件**: eval pass + regression test pass + 完全動作のユーザ承認

---

## Next session pickup

(セッション終了時にここを更新。"次に何をやるか" を具体的に書く)

### 現時点 (2026-05-03 Phase 2 ファイル群完了)

**Phase 2 で完了した分** (11/11 ファイル, 計 2313 行):
- references/rd/: rd_charter (256), core_technologies (290), capability_map_schema (238), trl_scale (213), rd_stages (260), rd_workflow (294), rd_promotion_gate (247) = 7 references / 1798 行
- assets/rd/: charter.md.template (95), capability_map.md.template (78), rd_trial.py.template (254), README.md.template (88) = 4 templates / 515 行
- G8 placeholder check: PASS (TBD/TODO/XXX/???/{{}}残留ゼロ、`<REPLACE: ...>` は意図的 marker として残置)
- D-19 / D-20 で記録された Category 2 改善 13 件は対応する file 内に full 反映

**ユーザレビュー & 判断待ち**:
- A. Phase 2 の 11 ファイルを review、内容に問題なければ Phase 3 (Pure Research) に進む
- B. (任意) dummy R&D project を回して end-to-end の動作確認を行うか?
  - 「dummy project で charter → core technology → capability → Stage gate → 1 trial の Analysis section A2+ まで完走」を sub-agent で実施
  - Phase 3 着手前に行うか、Phase 4 (review) 完了後にまとめて行うか判断

**Phase 4 完全完了** (file work + regression + dummy verification + 5 patches)。

(C) → (A) 完了。次は **(B) Phase 5 (scripts)**:

- 新規 scripts (約 10 個):
  - `validate_ledger.py` (capability_map / explanation_ledger / prereg / analysis-section の整合性 lint)
  - `prereg_freeze.py` (SHA-256 + timestamp lock for charter / prfaq / prereg)
  - `prereg_diff.py` (frozen vs actual の diff、major/minor 分類)
  - `reproducibility_stamp.py` (data hash + git commit + env lock 3-tuple)
  - `reproducibility_verify.py` (stamped 3-tuple の re-verification)
  - `render_capability_dag.py` (R&D capability DAG の Mermaid 出力, core_tech subgraph + lifecycle 別色分け)
  - `render_explanation_dag.py` (Pure Research explanation hierarchy の Mermaid 出力)
  - `charter_interview.py` (Heilmeier 8 Q の interactive elicitation)
  - `draft_imrad.py` (explanation_ledger + decisions + results → IMRAD draft)
  - `standup.py` (24h decisions.md transition summary)
  - `lit_fetch.py` (arxiv + Semantic Scholar batch、SSRN は manual URL)

- 既存 scripts の改修 (数値 helper):
  - `aggregate_results.py` (mode-aware schema, analysis_tier / core_tech_id / lifecycle 列)
  - `new_project.py` (--mode rd|pure-research)
  - `new_trial.py` (旧 new_purpose.py rename, mode-aware)

- D-19/D-20/D-26 で予約された改善:
  - C2.12 prereg_diff.py output spec (data hash / sample size / period match flag) を実装
  - F6 prereg_diff.py の expected vs observed tolerance band 比較 formalize

---

## Blockers

(blocker があれば列挙、解消したら "解消: 日付 + 理由" を append)

(none)

---

## このファイルの更新ルール

1. **セッション開始時**: 直前の "Next session pickup" を読み、現状と一致するか確認。一致しなければ DECISIONS にズレを記録。
2. **タスク完了時**: `[ ]` → `[x]` に変更。具体 evidence (commit hash, file path, test result) を行末に追記。
3. **タスク部分完了時**: `[ ]` → `[~]` + blocker 内容を行末に追記。
4. **新タスク発見時**: 該当 Phase に追記、新 Phase が必要なら Phase 増設。
5. **セッション終了時**: "Next session pickup" を **具体ステップで** 更新 ("〜を続ける" は禁止、"〜を `<file:line>` で編集する" まで具体化)。
