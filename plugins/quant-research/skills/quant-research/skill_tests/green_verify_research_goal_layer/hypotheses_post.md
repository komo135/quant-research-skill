# Hypothesis portfolio (post-GREEN — fixture for cases J / K)

GREEN 後の `hypotheses.md` は `target_sub_claim_id` 列で各 H を研究目標サブクレーム
に紐付け、`pathway` 列で生成由来を記録する。派生 H 単発の根拠 (= 何の為にこの仮説を
立証したいのか) はこの 2 列で読み取れる (= F15 解消)。

## Status legend

planned-runnow / planned-nextsession / planned-drop / in-progress / supported / rejected /
supported_provisional / partial / parked

## Entries

| ID | Statement | Status | experiment_id (= notebook = Purpose) | target_sub_claim_id | pathway | Acceptance condition | Last update |
|---|---|---|---|---|---|---|---|
| H201 | ROE rank long-only signal、WF mean Sharpe ≥ 0.4 | rejected | exp_021 (TOPIX500 quality factor の net 5bps 収益性) | G1.1 | 2 (literature-extension; Asness et al. 2014 を JP universe に移植) | WF mean Sharpe ≥ 0.4 | 2026-04-25 |
| H202 | (Derived from H201, same Purpose) ROE × OCF margin の rank-平均合成、WF mean Sharpe ≥ 0.4 | supported_provisional | exp_021 | G1.1 | 4 (failure-derived from H201 turnover axis; cash-flow 軸を独立成分として加える) | WF mean Sharpe ≥ 0.4 | 2026-04-25 |
| H301 | 3-factor (ROE / OCF margin / accruals quality) 等重み合成、WF mean Sharpe ≥ 0.5 かつ 2-factor との DM 検定で有意に正 | in-progress | exp_022 (TOPIX500 quality factor を 3-factor に拡張) | G1.3 | 6 (mechanism-driven; accruals quality は accrual ratio として ROE / OCF margin と直交する独立成分) | 3-factor WF mean Sharpe ≥ 0.5 ∧ DM 検定 p < 0.05 | 2026-04-30 |
| H302 | (Derived from H301, same Purpose) 重み比 sweep (1-1-1 / 2-1-1 / 1-2-1 / 1-1-2) で sensitivity を測る | planned-nextsession | exp_022 | G1.3 | 4 (failure-derived; H301 の等重み 1 点だけでは打ち消し合いの強度を測れない) | 重み比間で Sharpe spread < 0.2 | 2026-04-30 |
| H401 | (planned, NEW Purpose) H202 の構成を turnover-cap 30%/month + ADV 上位フィルター下で実装し、live-tradeable な実装が成り立つか | planned-nextsession | exp_023 (TOPIX500 quality factor の live-tradeability) | G1.2 | 4 (failure-derived; H201 turnover 観察と H202 の supported を活用して live 制約下に拡張) | turnover-capped かつ ADV-filtered 構成で WF mean Sharpe ≥ 0.35 | 2026-04-30 |
| H501 | (planned, NEW Purpose) H202 を TOPIX1500 にスケール、small-cap 領域での収益性を測る | planned-nextsession | exp_024 (TOPIX1500 quality factor) | G1.4 | 5 (cross-asset / cross-regime; mid-cap → small-cap への extension) | small-cap subset で WF mean Sharpe ≥ 0.4 | 2026-04-30 |

## How this row format addresses F15

ユーザー指摘 (= 派生 H が放置される / 何の為にこの仮説を立証したいのか不明) は、
本表で 3 つの列によって解消される:

- **`target_sub_claim_id`**: その H が研究目標のどのサブクレームに貢献するか。
  例: H202 は G1.1 を直接 attack、H401 は G1.2 を attack。読者は「H202 が何の
  為にあるか」を 1 つの ID 参照で理解できる。
- **`pathway`**: その H がどう生成されたか。例: H202 は pathway=4 (failure-derived)
  で H201 の turnover 観察から派生したことが明示。H401 も pathway=4 だが parent は
  H201 / H202 の cluster で、別 Purpose 開設の根拠が project README サブクレーム
  status (G1.2 が `not started` だった) で読み取れる。
- **`Statement` 列の "(Derived from H<n>, same/NEW Purpose)" prefix**: 派生関係を
  1 行で示す。これにより派生 H が "interpretation セルに溶けて消える" 症状 (= F15) が
  発生しない。

## How this row format addresses F16 (= Purpose 終了時の研究目標との距離)

`hypotheses.md` 単独では F16 は解消しない。`hypotheses.md` は **H 単位** の anchoring
を担い、Purpose 終了時の sub-claim status 更新は `decisions.md` の Purpose entry
が担う (= "Research-goal sub-claim progress update" セクション + "Design hypothesis at
close")。両者を合わせて参照することで、各 Purpose が研究目標を何 % 進めたかが
追跡可能になる。
