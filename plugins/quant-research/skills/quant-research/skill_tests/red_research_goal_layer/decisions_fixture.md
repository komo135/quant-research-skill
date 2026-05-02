# decisions.md fixture (Case K の前提状態)

ケース K の前提として、Purpose A (exp_021) 終了時に `decisions.md` に書かれる
エントリを、`hypothesis_cycles.md` "Updating decisions.md" の現行テンプレ通りに
記録した状態。研究目標 (= project README の Question) との距離 / 設計仮説の
更新欄は **テンプレに無いので書かれない**。これがケース K の失敗 (F16) の素地。

---

## 2026-04-25 cycle 1 (exp_021_topix_quality_factor) — Purpose: TOPIX500 quality factor の net 5 bps 収益性

- Tested H1: ROE rank long-only signal、WF mean Sharpe ≥ 0.4
  - Observation: WF mean = 0.18、月次 turnover = 45%、edge が手数料に食われる
  - Verdict: rejected
- Tested H2 (derived from H1): ROE × OCF margin の rank-平均合成、WF mean Sharpe ≥ 0.4
  - Observation: WF mean = 0.41、月次 turnover = 32%、net 5 bps 帯で edge 残存
  - Verdict: supported_provisional
- Purpose-level synthesis: ROE 単独は turnover で retire したが、OCF margin との
  合成で net 5 bps 帯に残る。Decision rule の YES 条件は H2 で達成。
- Derived Purposes for the next notebook:
  - Purpose B (run-now): 3-factor (ROE / OCF margin / accruals quality) 拡張で
    Sharpe を更に伸ばせるか
- Direction rejected: ROE 単独 (turnover で retire)
- Robustness battery status (per H): H1 — N/A (rejected)、H2 — pending (review 未通過)

---

## 2026-04-30 cycle 2 (exp_022_topix_quality_3factor) — Purpose: TOPIX500 quality factor を 3-factor に拡張

- Tested H1: 3-factor (ROE / OCF margin / accruals quality) 等重み rank-平均合成、WF mean Sharpe ≥ 0.5
  - Observation: PENDING (実装中)
  - Verdict: PENDING
