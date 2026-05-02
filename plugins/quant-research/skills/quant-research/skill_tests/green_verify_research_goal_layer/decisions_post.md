# Decision log (post-GREEN — fixture for cases J / K)

GREEN 後の `decisions.md` は Purpose entry に **Design hypothesis at open**、
**Research-goal sub-claim progress update**、**Design hypothesis at close** の
3 つの新セクションを持つ。これにより Purpose 終了時の研究目標との距離更新が
明示される (= F16 解消) し、次 Purpose の選定根拠が研究目標 sub-claim status
を読んで行われる構造になる (= F15-F16 共通の解消基盤)。

なお派生 Hypothesis の planning state (run-now / next-session / drop) は
`hypotheses.md` の `Status` 列で一元管理されており、本ファイルでは
**Purpose 単位** の "Derived Purposes" のみが書かれる (= 二重情報源を避ける)。

---

## 2026-04-25 cycle 1 (exp_021_topix_quality_factor) — Purpose: TOPIX500 quality factor の net 5 bps 収益性

- **Design hypothesis at open**: 本 Purpose を解けば G1.1 (`quality factor が
  net 5 bps で edge を持つ`) を confirmed か falsified に進められる。
  G1.2 (`live-tradeability`) や G1.3 (`stack せず打ち消し合わない`) は本 Purpose
  では触れない。

- **Tested H201 (target_sub_claim_id = G1.1)**: ROE rank long-only signal、WF mean Sharpe ≥ 0.4
  - Observation: WF mean = 0.18、月次 turnover = 45%、edge が手数料に食われる
  - Verdict: rejected
  - Robustness battery (this H): N/A (rejected)

- **Tested H202 (derived from H201, same Purpose, target_sub_claim_id = G1.1 inherited)**: ROE × OCF margin の rank-平均合成、WF mean Sharpe ≥ 0.4
  - Observation: WF mean = 0.41、月次 turnover = 32%、net 5 bps 帯で edge 残存
  - Verdict: supported_provisional
  - Robustness battery (this H): pending (review 未通過)

- **Purpose-level synthesis**: TOPIX500 quality factor のうち、ROE 単独は turnover で
  retire したが、OCF margin との合成で net 5 bps 帯に残る。Pattern E (1 H supported,
  others rejected on the same axis = turnover); 閉じ方は Primary YES (= H202 が
  Decision rule の YES 条件を達成)。

- **Research-goal sub-claim progress update**:
  - G1.1: not started → **confirmed** (H202 が YES 条件達成、合成軸さえ加えれば JP
    quality factor は net 5 bps で edge を持つ)
  - G1.2: not started → not started (turnover / ADV / capacity は本 Purpose では未検証)
  - G1.3: not started → not started (factor 同士の打ち消し合いは未検証 — 2-factor で
    合成軸が要ることは判明したが、3 軸目以上での挙動は別 Purpose 領域)
  - G1.4: not started → not started

- **Design hypothesis at close**: **CONFIRMED**。at-open の予想 (本 Purpose で
  G1.1 を進める、G1.2/G1.3/G1.4 は触れない) は実際の結果と一致。H202 の合成軸
  必要性は G1.1 内部の refinement で、G1.2 (live-tradeability) への shift には
  ならなかった (turnover 32% は cap を要する閾値ではない)。

- **Derived Purposes** (= candidates for new notebooks):
  - P_quality_3factor_stack (target_sub_claim_id = G1.3): 3-factor (ROE + OCF margin
    + accruals quality) で factor 同士が打ち消し合わずに合成 Sharpe を保つかを検証。
    G1.1 が confirmed なので G1.3 が次に attack すべき sub-claim。run-now eligible。
  - P_quality_capacity (target_sub_claim_id = G1.2): H202 の構成を、turnover-cap
    と ADV 制約下で再評価。G1.2 を attack。next-session (capacity データ取得が要る)。
  - P_quality_topix1500 (target_sub_claim_id = G1.4): H202 を TOPIX1500 にスケール。
    G1.4 を attack。next-session。

- **Direction rejected**: ROE 単独 (turnover で retire)。理由: 月次 turnover 45% は
  net 5 bps fee を edge が下回る水準で、cash-flow 軸を加えない限り JP では成立しない。

---

## 2026-04-30 cycle 2 (exp_022_topix_quality_3factor) — Purpose: TOPIX500 quality factor を 3-factor に拡張 (G1.3 attack)

- **Design hypothesis at open**: 本 Purpose を解けば G1.3 (`signal stacks with
  other quality factors without canceling`) を confirmed か falsified に進められる。
  G1.1 は exp_021 で既に confirmed 済なので本 Purpose では再確認のみ; G1.2 と G1.4
  は触れない。本 Purpose の選定根拠 = G1.1 と G1.3 のうち、G1.3 のほうが consumer
  の「多 factor スタック組み込み判断」に直接的に必要 (= multi-factor 設計の
  prerequisite); G1.2 は単独で先行実施しても G1.3 が canceling パターンなら
  最終的な live-tradeability の議論が立たないので、G1.3 を先行する。

- **Tested H301 (target_sub_claim_id = G1.3)**: 3-factor 等重み合成、WF mean Sharpe ≥ 0.5 かつ 2-factor との DM 検定で有意に正
  - Observation: PENDING (実装中)
  - Verdict: PENDING
  - Robustness battery (this H): not yet run

(...本 Purpose 終了時に Purpose-level synthesis / sub-claim progress update / Design
hypothesis at close を追記。)
