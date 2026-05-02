# Hypothesis portfolio (post-GREEN — fixture for cases G/H/I)

GREEN 後の `hypotheses.md` は派生 H の planning state (run-now / next-session / drop)
を `Status` 列で一元管理し、`target_sub_claim_id` で研究目標サブクレームに紐付ける。
notebook 本文側で派生 H 表を維持する必要は無くなった (= F12 / F13 が構造的に消える)。

新 Purpose handoff (exp_012 → exp_013) も、handoff 経緯を新ノートに書く必要は無く、
`hypotheses.md` の `experiment_id` 列が新 notebook を指し、`target_sub_claim_id` が
新 Purpose のサブクレームを指す形で link が成立する (= F14 が消える基盤の一部)。

## Status legend (関連抜粋)

- `planned-runnow` / `planned-nextsession` / `planned-drop`: 実行前の分類
- `in-progress`: ラウンド進行中
- `supported_provisional`: review 未通過の暫定 supported
- `rejected`: 棄却

## Entries

| ID | Statement | Status | experiment_id (= notebook = Purpose) | target_sub_claim_id | pathway | Acceptance condition | Last update |
|---|---|---|---|---|---|---|---|
| H101 | RSI(14) ≤ 30 entry × signal-flip exit、test Sharpe ≥ 0.5 | in-progress | exp_007 (EUR/USD 5min MR の net-fee 収益性) | G2.1 | 2 | test Sharpe ≥ 0.5 | 2026-04-30 |
| H102 | (Derived from H101, same Purpose) Bollinger(20, 2.0σ) lower-touch entry × signal-flip exit、test Sharpe ≥ 0.5 | in-progress | exp_007 | G2.1 | 4 | test Sharpe ≥ 0.5 | 2026-04-30 |
| H103 | (Derived from H101, same Purpose) regime conditional (trending / ranging) で H101 を分解 | planned-nextsession | exp_007 | G2.1 | 4 | trending Sharpe / ranging Sharpe を別計上、両方 ≥ 0.4 | 2026-04-30 |
| H104 | (Derived from H101, NEW Purpose) USD/JPY 5min への移植 | planned-nextsession | exp_009 (USD/JPY 5min MR) | G2.3 | 5 | test Sharpe ≥ 0.5 | 2026-04-30 |
| H201 | ROE rank long-only signal、WF mean Sharpe ≥ 0.4 | rejected | exp_011 (TOPIX500 quality factor の net 5bps 収益性) | G1.1 | 2 | WF mean Sharpe ≥ 0.4 | 2026-04-30 |
| H202 | (Derived from H201, same Purpose) ROE × OCF margin の rank-平均合成、WF mean Sharpe ≥ 0.4 | supported_provisional | exp_011 | G1.1 | 4 | WF mean Sharpe ≥ 0.4 | 2026-04-30 |
| H203 | (Derived from H202, same Purpose) H202 を trending regime のみに限定、WF mean Sharpe ≥ 0.5 | in-progress | exp_011 | G1.1 | 4 | trending regime WF mean Sharpe ≥ 0.5 | 2026-04-30 |
| H204 | (Derived from H201, same Purpose) sector-neutral 版で H201 を再評価 | planned-nextsession | exp_011 | G1.1 | 4 | sector-neutral WF mean Sharpe ≥ 0.4 | 2026-04-30 |
| H205 | (Derived from H201, same Purpose) long-short 化で market-neutral 版を実装 | planned-nextsession | exp_011 | G1.1 | 4 | market-neutral WF mean Sharpe ≥ 0.3 | 2026-04-30 |
| H206 | (Drop) earnings revision 系 factor の追加: papers.md の Asness et al. (2019) で JP universe の弱さが既知 | planned-drop | n/a | n/a | n/a | n/a | 2026-04-30 |
| H207 | (Derived from H202, same Purpose) H202 を turnover-cap 30%/month で制約した版 | planned-nextsession | exp_011 | G1.1 | 4 | turnover-capped WF mean Sharpe ≥ 0.4 | 2026-04-30 |
| H208 | (Derived from H202, same Purpose) H202 の重み比を 70:30 / 30:70 で sweep | planned-nextsession | exp_011 | G1.1 | 4 | 重み比間で Sharpe 不安定化が出ない | 2026-04-30 |
| H209 | (Derived from H203, same Purpose) H203 を sector-neutral × regime の 2 軸 cross で評価 | planned-nextsession | exp_011 | G1.1 | 4 | sector-neutral × trending regime WF mean Sharpe ≥ 0.4 | 2026-04-30 |
| H210 | (Derived from H203, NEW Purpose) H203 を US large-cap (S&P500) に移植 | planned-nextsession | exp_015 (S&P500 quality factor) | G3.1 | 5 | WF mean Sharpe ≥ 0.4 | 2026-04-30 |
| H301 | turnover-cap 30%/month 制約下で RSI(14) ≤ 30 × signal-flip 構成、test Sharpe ≥ 0.5 | in-progress | exp_013 (EUR/USD 5min MR を turnover-cap 制約下で再検証) | G2.2 | 4 | test Sharpe ≥ 0.5 かつ turnover ≤ 30%/month | 2026-04-30 |

## Notes

- H101-H104 は exp_007 (Case G post) 由来の H 群。H102 が「Bollinger 派生」で
  Status は in-progress、`target_sub_claim_id` は親 H101 から G2.1 を継承。
- H201-H210 は exp_011 (Case H post) 由来。多ラウンド (H201-H203) + 派生候補 (H204-H210)
  が並んでも、ノート本文には派生表が無い (= F13 解消)。各派生の planning state は
  `Status` 列だけで判別できる。
- H301 は exp_013 (Case I post) 由来で、`target_sub_claim_id = G2.2` (live-tradeability 層
  のサブクレーム) を持つ。これは exp_012 の Pattern A 由来であることが README サブクレーム
  状態 + decisions.md の exp_012 entry 側で読み取れる; 新ノート本文に handoff 経緯を
  書く必要は無い (= F14 解消基盤の一部)。
