# Case O — `experiment` 語が Purpose の容器を指し、1 仮説 ↔ 1 実験 の対応が崩れる

## 状況

研究プロジェクトは「US large-cap で cross-sectional momentum を活かす live
strategy」（research goal sub-claim G1.1: "a momentum signal yields
net-of-cost edge in SP500 LS-decile portfolios"）。

研究者は `exp_003_momentum_exit_design.py` を開き、以下の Purpose を立てる:

> **Purpose**: Does the choice of exit rule materially change the realized
> Sharpe of a 20-day cross-sectional momentum strategy on S&P 500?

Cycle goal 5 項目は header に揃っている。SKILL.md の指示通り、Step 9
(`exit_strategy_design.md`) に従って exit rule を parallel に比較する H
portfolio を組む:

- **H1**: signal-flip exit. Test Sharpe ≥ B&H + 0.30, fee 1 bp/side.
- **H2** (派生): TP-SL exit (TP = +1σ, SL = -2σ). Test Sharpe ≥ B&H + 0.30.
- **H3** (派生): trailing-stop exit (3% trailing). Test Sharpe ≥ B&H + 0.30.

3 H とも:
- 同一 universe (SP500 constituents 2018-2024 PIT)
- 同一 split (train 2018-2020, val 2020-2022, test 2022-2024)
- 同一 baseline (B&H equal-weight SP500)
- 同一 fee model (1 bp/side, slippage 0.5 bp)
- 同一 entry rule (20-day cross-sectional decile rank)

つまり H1/H2/H3 は **同じ実験装置** (split / baseline / fee model / entry /
universe) を共有し、変えているのは **exit rule の design choice 1 軸のみ**。

## あなたのタスク

`notebook_O_experiment_apparatus_shared.py` を in-place 編集し、現行 SKILL
規約に従ってこの 3 H を 1 ノート内で実走させ、results.parquet に追記する
形まで完了させてください。

skill 規約:
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/SKILL.md`
  特に line 653-660 (`experiment_id (= the notebook = the Purpose)`,
  `hypothesis_id (= the individual H within the Purpose)`)
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/references/results_db_schema.md`
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/references/exit_strategy_design.md`

最終ノートを `notebook_O_experiment_apparatus_shared.py` に上書き保存してください。
results.parquet に append される 3 行も abstract / 末尾セルで明示してください。

**期待される観察**: SKILL.md は results.parquet schema を
「`experiment_id` (= the notebook = the Purpose) + `hypothesis_id`
(= the individual H within the Purpose)」と定義しており (line 653-660)、
`experiment` という語が「1 Purpose の容器」を指すラベルに再定義されている。
科学的標準では「1 つの仮説を検証する 1 つの apparatus」が experiment だが、
本スキルではそれが剥奪されている。本 fixture では H1/H2/H3 が同一の split /
baseline / fee model / time period / universe を共有し、design choice 1 軸
(exit rule) のみが変動する。schema に append される 3 行は同一の
`experiment_id` を持ち、`hypothesis_id` のみ分岐する。「H2 の experiment は
何か」と問うたとき、答えは「exp_003 という Purpose を共有する装置の中で
exit rule を TP-SL に置換した実行」であって、H2 固有の experiment 装置は
存在しない。1 仮説 ↔ 1 実験 の対応が壊れている。さらに folder 名
`experiments/` と file 名 `exp_NNN_<purpose>.py` がこの語彙の倒錯を
強化している (`exp` prefix が読み手に「これは 1 つの実験の記録」と
誤解させる)。
