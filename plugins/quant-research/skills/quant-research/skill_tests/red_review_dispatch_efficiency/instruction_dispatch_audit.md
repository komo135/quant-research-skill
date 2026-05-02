# Case (audit) — review skill dispatch efficiency audit

## 状況

`bug_review` (5 specialists + 1 adversarial) と `experiment-review` (7
specialists + 1 adversarial) は H verdict='supported' の co-gate として
両方が走る。1 H verdict ごとに **14 sub-agent が並列 dispatch** され、
fix 反映後の re-verify でも **再び 14 sub-agent が全 fire** する。

ユーザー指摘:

> 「レビュースキルの TOKEN 負荷が高すぎるので質は落とさずに軽くしたい」

質を構成する mechanism (= **narrowness / bundle asymmetry / parallelism /
trigger discipline before verdict='supported'**) は触らずに、token / agent
run 負荷だけを削るレバーを探す。

## あなたのタスク (audit-type fixture なので artifact ではなく audit を作る)

現行 dispatch protocol を読み、以下を `audit_current_dispatch.md` に
書き出してください。

### F21 視点 (per-reviewer input bundle の dead weight)

1. **14 reviewer × 入力ファイル の matrix**: 行 = 14 reviewer (bug_review
   1-6 + experiment-review 7-14)、列 = 各入力ファイル (notebook .py /
   bug_review.md / sanity_checks.md / review_dimensions.md /
   severity_rubric.md / notebook_narrative.md / marimo_cell_granularity.md /
   hypotheses.md / decisions.md / literature/* / upstream feature notebook
   .py)。各セルに「全文 / 該当 section / NOT-receive」を埋める。
2. **重複量の集計**: 各入力ファイルが N/14 reviewer に渡されるかを集計。
3. **per-dimension scope の section 行数**: review_dimensions.md
   §1-§8 と bug_review.md §1-§5 の section 別行数を測定し、whole-file
   サイズと比較。
4. **理論的削減量**: pre-extraction (= whole-file → section-only) でどれだけ
   行数が削減されるか。

### F22 視点 (re-verify dispatch の agent-run 重複)

5. **典型 iteration profile**: H verdict='supported' attempt が何 round
   走るか。Initial → fix → re-verify (1) → fix → re-verify (2) ... の
   rounds 数別に、現行プロトコルでは全 14 reviewer が毎 round fire する
   ことを確認。
6. **agent-run 集計**: iteration N rounds で 14×N。surface 変化のない
   reviewer も毎回再走することの確認。
7. **理論的削減量**: surface map ベースの conditional dispatch を導入
   したときの agent-run count 削減 (Initial 14 + Re-verify per-round
   ~4 specialist + adversary)。

### 不採用となった F20 候補の整理

8. F20 (prompt caching) を当初候補化していたが skill scope 外と判断した
   経緯を 1 段落で整理。Claude Code 内で動くスキルが API-level の
   `cache_control` marker を mandate する根拠が無いこと、並列 sub-agent
   間の cache 共有が harness 依存で不確定なこと、を理由として明記。

skill 規約:
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/references/bug_review.md`
- `C:/Users/komo_/project/quant-research-skill/skills/experiment-review/SKILL.md`
- `C:/Users/komo_/project/quant-research-skill/skills/experiment-review/references/review_protocol.md`
- `C:/Users/komo_/project/quant-research-skill/skills/experiment-review/references/review_dimensions.md`

audit を `audit_current_dispatch.md` に上書き保存してください。

**期待される観察**:

- F21: matrix は **重複が支配的** であることを示す ─ notebook .py は 14/14、
  bug_review.md は 5/14 に whole で渡るが、各 reviewer が実際に scope する
  のは 13 行程度の自身の section のみ。review_dimensions.md は 8/14 に
  whole で渡るが各 reviewer が scope するのは 36-74 行のうち 1 section
  のみ。残り 80%+ は dead weight。
- F22: typical iteration profile (Initial + 2 re-verify) で 42 agent-run
  発生。re-verify 2 round で 28 agent-run が dead reading (= surface 変化
  なし reviewer の再走)。
- F20: skill 文言で mandate する根拠なしと整理、本 RED から除外。
