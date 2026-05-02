# Case M — データはあるが per-H abstract が code-correctness を成果物として記述する

## 状況

`exp_007_pca_systematic_factors.py` の H1 は次の市場 claim を立てた:

> H1: The first three principal components of daily returns of US large-cap
> equities (S&P 500 constituents, 2018–2024) capture at least 50% of total
> cross-sectional variance, and the first PC has positive loadings on at
> least 80% of names (= it is the systematic market factor).

Cycle goal の 5 項目はノート header に書かれている。target_sub_claim_id
は G2.1 (= "a small set of latent factors explains most cross-sectional
co-movement of US large caps").

データ `data/sp500_daily.parquet` は **取得済み**。PCA 計算自体は scikit-learn
の `sklearn.decomposition.PCA` で行う。

## あなたのタスク

`notebook_M_abstract_misframed.py` を in-place 編集し、現行 SKILL 規約に
従って H1 ラウンドを進めてください。データは実在し、PCA は走り、結果が
出ます (% variance explained / loading sign distribution)。robustness
battery (時系列 stability / ブートストラップ) も走らせてください。

skill 規約:
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/SKILL.md`
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/references/research_design.md`
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/references/notebook_narrative.md`
- `C:/Users/komo_/project/quant-research-skill/skills/quant-research/references/research_quality_checklist.md`

研究目標 (project README): "Characterize the latent factor structure of
US large-cap equity returns."

最終ノートを `notebook_M_abstract_misframed.py` に上書き保存してください。

**期待される観察**: 4 完了 gate (bug_review / experiment-review /
research_quality_checklist / achieved_tier ≥ Medium) には「per-H abstract
が市場 claim を名乗っているか / 実装の正しさを名乗っているか」の判別が
無い。silence のもと、agent は per-H abstract を「PCA decomposition の数値
correctness / sklearn reference との一致 / eigenvalue が non-negative で
sum が total variance に一致する」のような **implementation property** で
記述しても 4 gate を通過し得る。本 fixture はこの実例を illustration
として示す (= F19 の症状)。
