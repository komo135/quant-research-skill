# audit_current_dispatch.md — review skill dispatch (pre-fix)

現行 `bug_review` + `experiment-review` の dispatch protocol が、1 H
verdict='supported' co-gate で 14 sub-agent に何を渡し、iteration N rounds
で agent-run 数がどれだけ膨らむかの実測。

## Reviewer roster (14 total)

| # | Skill | Reviewer | Bundle 種別 |
|---|---|---|---|
| 1 | bug_review | leakage | full specialist |
| 2 | bug_review | pnl-accounting | full specialist |
| 3 | bug_review | validation (correctness) | full specialist |
| 4 | bug_review | statistics (metric arithmetic) | full specialist |
| 5 | bug_review | code-correctness | full specialist |
| 6 | bug_review | adversarial (cold-eye) | minimum |
| 7 | experiment-review | question | full specialist |
| 8 | experiment-review | scope | full specialist |
| 9 | experiment-review | method | full specialist |
| 10 | experiment-review | validation (sufficiency) | full specialist |
| 11 | experiment-review | claim | full specialist |
| 12 | experiment-review | literature | full specialist |
| 13 | experiment-review | narrative | full specialist |
| 14 | experiment-review | adversarial (cold-eye) | minimum |

## F21 視点 — per-reviewer input bundle の dead weight

### 14 × N input matrix (current protocol)

`R` = receives whole file。`-` = NOT-receive。

| Reviewer | notebook .py | upstream .py | bug_review.md | sanity_checks.md | review_dimensions.md | severity_rubric.md | notebook_narrative.md | marimo_cell_granularity.md | hypotheses.md | decisions.md | literature/ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 leakage | R | R | R (whole) | R (whole) | - | - | - | - | - | - | - |
| 2 pnl-accounting | R | R | R (whole) | R (whole) | - | - | - | - | - | - | - |
| 3 validation (corr) | R | R | R (whole) | R (whole) | - | - | - | - | - | - | - |
| 4 statistics | R | R | R (whole) | R (whole) | - | - | - | - | - | - | - |
| 5 code-correctness | R | R | R (whole) | R (whole) | - | - | - | - | - | - | - |
| 6 bug adversarial | R (.py only) | R (only if named in design cell) | - | - | - | - | - | - | - | - | - |
| 7 question | R | (variable) | - | - | R (whole, "read §1 only") | R | - | - | R | R | - |
| 8 scope | R | (variable) | - | - | R (whole, "read §2 only") | R | - | - | R | R | - |
| 9 method | R | R | - | - | R (whole, "read §3 only") | R | - | - | - | - | - |
| 10 validation (suff) | R | (variable) | - | - | R (whole, "read §4 only") | R | - | - | - | R (bug-review entry) | - |
| 11 claim | R | (variable) | - | - | R (whole, "read §5 only") | R | - | - | - | - | - |
| 12 literature | R | (variable) | - | - | R (whole, "read §6 only") | R | - | - | - | - | R (papers + diff) |
| 13 narrative | R | - | - | - | R (whole, "read §7 only") | R | R | R | - | - | - |
| 14 exp adversarial | R (.py only) | - | - | - | R (whole, "read §8 only") | R | - | - | - | - | - |

**観察 1**: bug_review.md は 5/14 に whole で渡る (= 1500 行)。各 reviewer が
scope するのは 12-14 行 (§i)、whole の 4-5 %。残り 95 % は dead weight。

**観察 2**: review_dimensions.md は 8/14 に whole で渡る (= 3912 行)。各
reviewer が scope するのは 37-112 行 (§i)、whole の 8-23 %。残り 77-92 % は
dead weight。

**観察 3**: 「whole file を渡し reviewer に *read §i only* を指示」設計は、
agent の context attention を浪費 (lost-in-middle) + 入力 token billing を
浪費する 2 重の cost。

### Per-reference whole-file vs per-dimension section sizes

`review_dimensions.md` (489 lines total):

| Dimension section | Lines | Section lines | % of whole |
|---|---|---|---|
| Header (How to read) | 1-19 | 19 | 4 % |
| §1 question | 20-58 | 39 | 8 % |
| §2 scope | 59-121 | 63 | 13 % |
| §3 method | 122-161 | 40 | 8 % |
| §4 validation | 162-198 | 37 | 8 % |
| §5 claim | 199-236 | 38 | 8 % |
| §6 literature | 237-302 | 66 | 13 % |
| §7 narrative | 303-377 | 75 | 15 % |
| §8 adversarial | 378-489 | 112 | 23 % |

`bug_review.md` (300 lines total):

| Reviewer scope | Lines (pre-fix) | Section lines | % of whole |
|---|---|---|---|
| Front matter (When / Why / Triggers) | 1-60 | 60 | 20 % |
| Reviewer roster header | 61-80 | 20 | 7 % |
| §1 leakage-reviewer | 81-92 | 12 | 4 % |
| §2 pnl-accounting-reviewer | 94-107 | 14 | 5 % |
| §3 validation-reviewer | 109-120 | 12 | 4 % |
| §4 statistics-reviewer | 122-134 | 13 | 4 % |
| §5 code-correctness-reviewer | 136-147 | 12 | 4 % |
| §6 adversarial (instruction + bundle list) | 149-187 | 39 | 13 % |
| Dispatch protocol + Single-agent fallback + remainder | 189-300 | 112 | 37 % |

### 重複集計 — 14 reviewer 合算 input lines (current protocol、approximate)

仮定: notebook .py 1000 行、project artifacts (hypotheses 100 / decisions 200 /
papers 100 / differentiation 100) を概算。

| ファイル | 全 reviewer 合算行数 | 各 reviewer の actual scope 行数 (合算) | dead weight 行数 (合算) |
|---|---|---|---|
| notebook .py | 14 × 1000 = 14000 | 14 × 1000 = 14000 (全員 scope) | 0 |
| bug_review.md | 5 × 300 = 1500 | 5 × 13 = 65 (各 §i のみ) | 1435 |
| sanity_checks.md | 5 × 189 = 945 | ~5 × 60 = 300 (per-reviewer 必要 check のみ) | ~645 |
| review_dimensions.md | 8 × 489 = 3912 | 7 × ~50 + 1 × 112 = 462 (各 §i + adversary §8) | 3450 |
| severity_rubric.md | 8 × 149 = 1192 | 8 × 149 = 1192 (全員 scope) | 0 |
| notebook_narrative.md | 1 × 400 = 400 | 1 × 400 = 400 | 0 |
| marimo_cell_granularity.md | 1 × 166 = 166 | 1 × 166 = 166 | 0 |
| hypotheses.md | 2 × 100 = 200 | 2 × 100 = 200 | 0 |
| decisions.md | 3 × 200 = 600 | 3 × 200 = 600 | 0 |
| literature/papers + diff | 1 × 200 = 200 | 1 × 200 = 200 | 0 |
| **合計** | **23115** | **17585** | **5530 (24 %)** |

`upstream feature notebook .py` は variable で外置きしたが、上式に積んだ場合
重複量はさらに増える (典型 5 reviewer × 500 行 = 2500 行)。

## F22 視点 — re-verify に伴う agent-run の重複

iteration N rounds で 14×N agent run。surface 不変の reviewer も毎回
notebook + dimension scope を読み直す。

### 典型 iteration profile (= bug_review fixture の baseline run より)

H1 verdict='supported' の co-gate での 1 H attempt:

| iteration | 動作 | agent run 数 |
|---|---|---|
| Initial pass | 14 reviewer 全 fire → 高 finding 3 件 (例: leakage in §5 / pnl-accounting in §6 / claim overstatement in abstract) | 14 |
| fix 適用 (round 1) | §5 → P1 in-place rewrite、§6 → P1 in-place rewrite、abstract → P1 wording rewrite (3 surface) | 0 |
| Re-verify pass 1 | **再び 14 reviewer 全 fire** ← 11 reviewer は dead reading | 14 |
| fix 適用 (round 2) | 仮に narrative reviewer が「abstract と verdict cell の数値ズレ」を指摘、さらに 1 surface 着地 | 0 |
| Re-verify pass 2 | **再び 14 reviewer 全 fire** ← 13 reviewer は dead reading | 14 |
| **合計** | | **42** |

re-verify 2 回の場合 28 agent-run が dead reading (= surface 変化なしの
reviewer の re-fire)。

### 該当箇所

| ファイル | 行 | 抜粋 |
|---|---|---|
| `bug_review.md` | 11 (pre-fix) | "About to declare `verdict = "supported"` for any experiment" |
| `bug_review.md` step 6 (pre-fix) | "After fixing the findings in code, run `references/post_review_reconciliation.md` ... End with a top-to-bottom verification pass" — re-run の規定はあるが「どの reviewer が再 fire するか」の規約が無い |
| `experiment-review/SKILL.md` Process step 4 (pre-fix) | "Dispatch all eight reviewers *in parallel*" — re-verify でも 8 全 fire |

## 失敗モード所在 (RED phase)

### F21 — dispatch protocol が per-dimension scope を pre-extract していない

`audit_current_dispatch.md` matrix で `R (whole)` エントリが集中。
**5530 行 / 14 reviewer の dead weight** (~22K tokens at 4 tokens/line)。
skill 文言で「whole file を渡し reviewer に section i を読ませる」設計に
なっていることが root cause。

### F22 — re-verify dispatch が無条件で全 reviewer を発火させる

iteration N rounds で 14×N agent run。surface map ベースの conditional
dispatch が無いため、どの fix も「全 14 を再走させる」設計。skill 文言に
**Initial pass vs Re-verify pass の区別が無い**、「dimension 毎の surface
map」が無い、ことが root cause。

### Quality machinery (= narrowness / asymmetry / parallelism / trigger discipline) との独立性

- **narrowness**: 各 reviewer が自身の dimension のみに集中する設計、scope は
  §i のみ。pre-extraction は scope を **より厳密に** 限定するだけで、
  specialist の独立性を強化する。narrowness を弱めない。
- **asymmetry**: bug_review §6 + experiment-review §8 の adversary は
  minimum bundle。pre-extraction でも adversary には whole file 抽出後の
  section を渡すことで asymmetry は **同じ** に保てる。
- **parallelism**: 並列 dispatch は変更しない。Initial では 14 並列、
  Re-verify では該当 specialist + adversary のみ並列、両者とも独立 read。
- **trigger discipline**: Initial pass で全 14 fire の規定は **不変**。
  Re-verify は Initial 後の incremental fix に対する再検査で、verdict=
  'supported' 直前の gate 自体は崩れていない。

## ユーザー指摘との対応関係

| ユーザー要素 | RED で観察された側面 |
|---|---|
| 10 以上の Agent が走る | 14 sub-agent が verdict='supported' の度に発火 |
| TOKEN 負荷が高い | F21: 14 reviewer 合算 23115 行のうち 5530 行 dead weight (24 %)。F22: re-verify ごとに 14 全 fire = iteration N rounds で agent run 14×N |
| 質は落としたくない | F21/F22 は **dispatch 規約の変更**、quality machinery (narrowness / asymmetry / parallelism / trigger discipline) は不変 |

## Scope 限界 — 本 audit でカバーしないもの

- **F20 (prompt caching)**: 当初候補化したが skill scope 外と判断 (= Claude
  Code 内のスキルから API-level cache_control を mandate するのは越権)。
  本 audit は理論的に caching が有効でも、それは harness 任せで skill
  文言で claim できないと整理。
- **実測**: 実際に sub-agent dispatch して billed input tokens を計測する
  ことは scope 外。理論値 (line counts × tokens/line × agent-run count)
  のみ。実測がほしくなったら future RED で別途。
- **Specific items to chase の機械化**: efficiency に効く第 3 のレバー、
  本 audit の scope 外、future RED 候補。
- **Cross-session re-verify の attestation format**: GREEN で skeleton を
  提示するが、attestation の format / verifiability の詰めは future
  iteration 候補。
