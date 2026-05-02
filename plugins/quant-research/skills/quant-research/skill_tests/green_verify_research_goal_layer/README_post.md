# jp_quality_factor_live_tradeable

(Project README — fixture for cases J / K post-GREEN)

## Research goal

Does JP equity quality-factor stacking yield a live-tradeable strategy
on TOPIX500 / TOPIX1500?

### Sub-claims

| ID | Sub-claim | Status |
|---|---|---|
| G1.1 | Quality factor (some signal in the family) yields net-of-cost edge in TOPIX500 at 5 bps/side | confirmed |
| G1.2 | The signal survives realistic execution constraints (turnover-cap ≤ 30%/month, ADV constraints) | not started |
| G1.3 | The signal stacks with other quality factors without canceling (合成 Sharpe ≥ 2-factor 単独 Sharpe) | in progress |
| G1.4 | The signal generalizes to TOPIX1500 with comparable Sharpe | not started |

Sub-claim IDs (G1.1, G1.2, ...) are stable within the project and never
reused after retirement. Each Purpose's notebook references these IDs in
its Cycle goal's 5th item (`target_sub_claim_id`). Each H row in
`hypotheses.md` references these IDs in its `target_sub_claim_id` column.

## Status summary

- Current cycle: 2 of ~5 planned
- Purposes opened: exp_021 (G1.1 → confirmed), exp_022 (G1.3, in progress)
- Sub-claims confirmed: G1.1
- Sub-claims falsified: (none)
- Sub-claims in progress: G1.3
- Sub-claims not started: G1.2, G1.4

## Why this matters under the four-layer model

The next Purpose's selection (= exp_022 attacking G1.3) is justified by
the sub-claim status table above, NOT by exp_021's per-H numeric
observations alone. After exp_021 advanced G1.1 from `not started` to
`confirmed`, the choice between attacking G1.2 or G1.3 next is a
research-goal-layer decision recorded in `decisions.md` as the design
hypothesis at open of exp_022. See `references/research_goal_layer.md`
for the full model.
