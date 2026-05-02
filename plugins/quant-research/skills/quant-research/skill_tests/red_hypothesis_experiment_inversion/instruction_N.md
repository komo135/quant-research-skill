# Case N — Purpose は親仮説（仮説の仮説）として機能し、子 H 連鎖の rejection から escape する

## 状況

研究プロジェクトは「intraday FX 上での short-horizon mean-reversion 戦略の
live-tradeable 候補を 1 本見つける」（research goal sub-claim G1.1: "a
mean-reversion signal yields net-of-cost edge on EUR/USD H1"）。

研究者は SKILL.md line 52 の Purpose 例をそのまま採用し、最初のノートを
`exp_001_mr_eurusd_h1.py` で開始する:

> **Purpose**: Does mean-reversion work on EUR/USD intraday?

Cycle goal 5 項目 (Consumer / Decision / Decision rule (YES/NO/KICK-UP) /
Knowledge output / target_sub_claim_id) は header に書かれている。

H1 (RSI≤30 entry × signal-flip exit、test Sharpe ≥ 0.5) は test Sharpe
0.12 で **rejected**。failure_mode = `headline_below_threshold`。

H2 (派生 — H1 の sizing 軸を refine。RSI≤30 entry × signal-flip exit ×
vol-targeted size、test Sharpe ≥ 0.5) も test Sharpe 0.18 で **rejected**。
failure_mode = `headline_below_threshold`。

H3 (派生 — H2 の regime 条件を絞る。high-vol regime のみで RSI≤30 ×
signal-flip × vol-targeted、test Sharpe ≥ 0.5) も test Sharpe 0.21 で
**rejected**。failure_mode = `headline_below_threshold`。

3 H 連続 reject。N=3 の cross-H synthesis trigger 条件は満たしている。

## あなたのタスク

`notebook_N_meta_hypothesis_chain.py` を in-place 編集し、現行 SKILL 規約
（および `cross_h_synthesis.md` Pattern A の指示）に従って Purpose を閉じ、
synthesis paragraph を書き、derived Purpose 候補を `decisions.md` に
記録する形にしてください。

skill 規約:
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/SKILL.md`
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/references/cycle_purpose_and_goal.md`
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/references/cross_h_synthesis.md`
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/references/hypothesis_cycles.md`
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/references/research_goal_layer.md`

最終ノートを `notebook_N_meta_hypothesis_chain.py` に上書き保存してください。

**期待される観察**: SKILL.md は Purpose の定義として "An open-ended question
about the world" (line 48) を与えるが、提示例 3 件 (`Does mean-reversion
work on EUR/USD intraday?` 等、line 52) はすべて Y/N 命題形 — open-ended
question を装った implicit な親仮説。SKILL.md line 96 は「the notebook
itself does not have a single verdict」と明記しており、Purpose-level の
verdict gate は存在しない。`cross_h_synthesis.md` Pattern A は H 全 reject
を「binding axis を持つ derived Purpose に再投入」する protocol を licensing
する。結果、3 子 H が rejection されても、それらの上位にある Purpose
（"Does mean-reversion work on EUR/USD intraday?"）自体は falsified にも
supported にもならず、derived Purpose `exp_002_mr_eurusd_lower_freq.py`
に親仮説をそのまま carry forward する。同じ親仮説（mean-reversion works
on EUR/USD）が、scope を少し変えただけの新しい Purpose として再起動する。
