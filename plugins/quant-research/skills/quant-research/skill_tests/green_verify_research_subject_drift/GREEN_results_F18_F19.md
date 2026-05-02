# GREEN research-subject drift — F18 / F19 反映後の挙動

RED phase で観察された 2 失敗モード (F18 / F19) に対する skill 改修と、
post-fix fixture (`notebook_L_post.py` / `notebook_M_post.py`) で確認された
GREEN 側の挙動。

## 改修箇所

| 失敗モード | 改修ファイル | 改修内容 |
|---|---|---|
| F18 | `references/experiment_protocol.md` | 新節 "Data availability gate" — research subject が real-world AND real data 不在 → cycle BLOCKED。substitution を禁ずる。protocol 外の synthetic scaffolding (no Cycle goal / no verdict / no results.parquet row) は engineering work として許容。synthetic data IS the research subject の例外規定 (estimator recovery on a known DGP)。BLOCKED forward path 規定 (decisions.md に structural finding として記録、cycle 停止、別 cycle / project portfolio へ pivot)。anti-rationalization 5 件。 |
| F18 | `references/experiment_protocol.md` Pre-flight checklist | "Data availability gate cleared" checkbox 追加 |
| F18 | `SKILL.md` Step 2 末尾 | データ availability gate の 1 段落 + experiment_protocol.md "Data availability gate" へのポインタ |
| F19 | `references/notebook_narrative.md` 1b | "Format rule — first sentence is the market claim, not the implementation" を追加。good / anti-pattern の lead 例 3 + 3。Reproducibility note のバウンド規定。anti-rationalization 5 件。 |
| F19 | `references/notebook_narrative.md` Quick checklist | "Per-H abstract first sentence names the falsifiable claim's answer in market terms" checkbox 追加 |
| F19 | `assets/experiment.py.template` H1 round | per-H abstract section "### H1 abstract (filled AFTER H1 cells run)" を新設、format rule を inline 説明 + good / anti-pattern 例 |
| F19 | `SKILL.md` Step 16 末尾 | per-H abstract format rule の 1 段落 + notebook_narrative.md 1b へのポインタ |

新 reference は作らず、anti-rationalization 表は references の中に留めた
(SKILL.md に新 table を作らない、advisor 推奨)。verification 側 (=
experiment-review skill の `narrative` dimension) は notebook_narrative.md
1b を読むことで自然に担保される (= 新 gate machinery 不要、既存 2 層 fix)。

## F18 の解消 — `notebook_L_post.py`

| RED 兆候 (`notebook_L_synthetic_pipeline_drift.py`) | GREEN (`notebook_L_post.py`) |
|---|---|
| abstract "Why this matters" が "verifies that the pipeline ... is wired correctly end to end" | abstract が "Status: BLOCKED — data unavailable" を冒頭で named state として宣言 |
| `data_source = "synthetic"` の if/else を notebook 内に持つ | data load セル自体が存在しない |
| robustness battery (2D surface / fee sweep / WF / bootstrap) が走り、observation cell が "the pipeline correctly assigns a null result to a null process" と書く | robustness battery セル自体が存在しない |
| verdict cell が `verdict_h1 = "parked"` を出力 | verdict cell が存在しない |
| results.parquet 行追加セルが synthetic dry-run の row を append | results.parquet 行追加セルが存在しない |
| 1 cycle 分の作業投入があるのに知識生成は 0 bit | notebook 自体が ~75 行 (markdown + decisions.md excerpt のみ) で停止、forward path が decisions.md に書かれている |

「実装セルが一切無い」「robustness が走らない」「verdict が無い」「results.parquet
に row が無い」**こと自体が GREEN の証拠**。RED で見られた pipeline-correctness
scaffold の構造的兆候はすべて消える。

forward path として:
- decisions.md (= 計画レイヤー、議事側) に BLOCKED structural finding が記録される
- 研究者は別 cycle (= 例: exp_002 CSI300 PCA factor screening) に pivot する
- design hypothesis at close = PARTIAL (G1.1 が data acquisition 待ちで blocked、
  G1.2 / G1.3 が confirmed G1.1 を inherit できないため sub-claim attack 順を
  portfolio level で再評価)

これで cycle が「市場の挙動を問う研究」として閉じる。pipeline 整備は skill の
管轄外にある engineering work として並走する。

## F19 の解消 — `notebook_M_post.py`

| RED 兆候 (`notebook_M_abstract_misframed.py`) | GREEN (`notebook_M_post.py`) |
|---|---|
| H1 abstract の第 1 段落 "**Implementation summary.** PCA was performed ... verified to match a from-scratch eigendecomposition" | H1 abstract の **第 1 文** "The first three PCs of SP500 daily residual returns 2018–2024 captured 47.0 % of cross-sectional variance, and PC1 loaded with the same sign on 92 % of names" — 市場 claim |
| H1 abstract の第 2 段落 "**Numerical correctness.** All eigenvalues are non-negative; ... trace within machine precision" | implementation correctness は abstract 末尾の "*Reproducibility note*" に bound、1 段落のみ |
| H1 abstract Verdict 行 "**The implementation is correct and reconciles with sklearn's reference**. The threshold ... is met on the loading-sign side; the variance-share is just below at 47 %" — implementation が主節、研究 verdict が subordinate clause | abstract Verdict 文 "Verdict = *parked*: the loading-sign gate (≥ 80 %) is met, the variance gate (≥ 50 %) is on the boundary at 47 %" — 研究 verdict が主節 |
| H1 interpretation (2) "Numerical evidence that the decomposition is trustworthy" — implementation correctness 三点セット | H1 interpretation (2) "Why is this the answer mechanistically?" — single market mode + secondary factors の 2018–2023 サンプルでの寄与不足 = 市場 mechanism |

ノートを scroll した読者が H1 abstract の lead 文だけ読んで離脱しても、
受け取るのは「世界 (SP500 cross-section) の挙動」であって「sklearn が正しく
動いた」ではない。これが format rule の bite。

## 完了 4 gate (bug_review / experiment-review / quality-checklist / tier) の維持

advisor 助言通り **5 番目の gate は作っていない**。format rule は agent の
generation 時 (= experiment.py.template の per-H abstract section)、書き
直し時 (= notebook_narrative.md 1b)、verification 時 (= experiment-review
skill の `narrative` dimension が notebook_narrative.md を読む形で自動
継承) の 3 タイミングで bite する。新 gate machinery 不要。

## Scope 限界 — 本 GREEN でカバーしない経路 (再掲)

ユーザー指摘の inversion は本 fixture (F18 / F19) では 2 経路を覆う。
**reconciliation focus-pull (post_review_reconciliation.md DoD が
code-output alignment に偏向する経路)** は別の inversion 経路で、本 GREEN
では fix しない。これは future RED phase で扱う:

- 想定される future F-id: F20 (e.g.) — reconciliation pass の Definition
  of Done が code/figure 整合作業を felt deliverable に変える
- 想定される future GREEN counter: DoD に「reconciliation 後のノート本文に
  market claim の `evidence content` が更新されているか」のステップを追加
- 想定される future fixture: 複数ラウンドの bug_review / reconciliation
  を経た notebook で、reconciliation 後の abstract の内容が市場 claim の
  実体を保っているか ↔ code/figure 整合作業のメモが abstract に染み出して
  いるか、を比較

本 GREEN は **silence-licensed の 1-round inversion** に focus する。
multi-round inversion via reconciliation pull は scope 外。

## F12-F17 / F1-F11 を re-run しても GREEN は維持される (回帰確認)

advisor 助言の通り、本改修は:

- F1-F8 (本文への履歴 / レビュー用語の流入) と直交 — 本文 cleanliness rule
  に触れない
- F9-F11 (skill version / migration / cross-skill API) と直交 — skill
  version vocabulary を本文に出さない既存 rule を維持
- F12-F14 (派生 H 表のノート流入) と直交 — `### Derived hypotheses`
  table の規定に触れない
- F15-F16 (research_goal_layer 4 階層モデル) と直交 — Cycle goal 5 項目 /
  target_sub_claim_id の規定を維持、本 fix は Cycle goal "5 items + data
  availability gate" として上に積む
- F17 (sub-step 1.5 conjunct contribution gate) と直交 — derived H routing
  に触れない

回帰として、既存 RED fixtures の expected GREEN 挙動は変わらない。
