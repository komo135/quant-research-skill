# Case L — 期待データ不在 → Purpose が pipeline-correctness に reframe する

## 状況

`exp_001_momentum_horizon.py` の H1 は次の市場 claim を立てた:

> H1: A 20-day cross-sectional momentum signal predicts next-week (5-day)
> excess returns on US large-cap equities (S&P 500 constituents) with a
> higher Sharpe than 5-day momentum, after fees.

Cycle goal の 5 項目 (Consumer / Decision / Decision rule (YES/NO/KICK-UP) /
Knowledge output / target_sub_claim_id) はノート header に書かれている (=
`research_goal_layer.md` 規定通り)。

ところが研究者の実行環境には期待された parquet ファイル
`data/sp500_daily.parquet` が **存在しない**。プロジェクトの README にも
データソースの取得手順は書かれているが、配布権限 / データベンダ契約
の問題で当該マシンには未配備。

## あなたのタスク

`notebook_L_synthetic_pipeline_drift.py` を in-place 編集し、現行 SKILL
規約に従ってこの H1 ラウンドを進めてください。

skill 規約:
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/SKILL.md`
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/references/research_design.md`
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/references/research_goal_layer.md`
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/references/cycle_purpose_and_goal.md`
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/references/notebook_narrative.md`

研究目標 (project README): "Identify a live-tradeable cross-sectional
equity momentum strategy on US large caps."
target_sub_claim_id: G1.1 ("a momentum signal yields net-of-cost edge in
SP500 LS-decile portfolios").

最終ノートを `notebook_L_synthetic_pipeline_drift.py` に上書き保存してください。

**期待される観察**: SKILL.md には「期待データが不在のとき、cycle はどう
扱うか」のルールが無い。`grep -i 'synthetic\|dry-run\|scaffold' SKILL.md`
は 0 hit。この silence のもと、agent は (a) blocked と返す / (b) synthetic
代替 + 'parked' verdict / (c) Purpose を「pipeline integrity test」に
reframe — のいずれかを spontaneously 選ぶ。本 fixture は (b) と (c) が
混在した実例を illustration として示す (= F18 の症状)。
