# GREEN findings — derived-hypothesis depth (after #1 abolish-cycle + #2 why-why GREEN)

## Setup recap

Same fixture as RED (`fixture_parent_H1.md`): only H1 headline numbers,
the one-line H1 observation cell, and `failure_mode = fee_model`. No
mechanism-level post-mortem pre-baked. Subagent dispatched under the
revised skill (`acceptance_criteria.md` and `RED_findings.md` withheld).

## What the subagent produced

Pre-amble: an explicit decision-rule reconstruction (admitting it was
inferred), a list of mechanism-level analyses required, and a why-why
chain.

**Why-why chain (≥ 3 levels, mechanism-level termination).**
Three consecutive "why?" levels written contiguously:

> Why was H1 rejected? → break-even fee 0.42 < 1 bp/side; per-trade
> unit economics did not survive cost.
>
> Why are the unit economics that thin? → gross PnL concentrated in a
> high-vol sub-population; modal trades pay fees without comparable
> gross edge; fee burden concentrates in shortest-holding tercile.
>
> Why is gross PnL concentrated in the high-vol sub-population, and
> why is the asymmetric exit converting that exposure to a positive-
> skew stream? → RSI(14)≤30 selects for high-vol participation rather
> than for MR opportunities; signal-flip exit holds winners through
> the post-reversion trend phase and cuts losers fast; monthly PnL
> correlates more with long-vol / managed-futures proxies than with
> EUR/USD's own monthly return.

Three distinct **terminal answers** (A/B/C) explicitly named, each
mechanism-level (entry-rule selection / exit-rule mechanism / fee-
burden distribution).

**Three derived H's**:

- **H2** — residual edge after regressing H1 monthly PnL on long-vol
  benchmark; cites Terminal-A.
- **H3** — symmetric-exit replacement isolates exit-rule contribution;
  cites Terminal-B.
- **H4** — holding-time-tercile stratification + holding-time-floor
  filter; cites Terminal-C.

All three same-notebook routing (parent thesis not yet verdicted at
N=1; opening a re-paraphrased Purpose now would violate the
Purpose-level closure gate).

## Evaluation against `acceptance_criteria.md`

| Criterion | Verdict |
|---|---|
| **G-1** (agent performs / demands a mechanism-level post-mortem before deriving) | **PASS.** Agent listed five mechanism-level analyses to run on the available artifacts (regime stratification / holding-time conditional on outcome / external-proxy correlation / fee-burden by holding-time tercile / intra-trade reversion-vs-trend) before writing the chain. |
| **G-2** (0 surface-derived H) | **PASS.** Each of H2/H3/H4 cites a specific chain terminal and articulates an alternative reading of the parent's claim. None are derived directly from the `fee_model` label. |
| **G-3** (0 parameter-variation H modulo also-mechanism-grounded) | **PASS.** H2 swaps method type entirely (residual regression vs. running the original apparatus). H3 swaps exit-rule type (symmetric vs. asymmetric — different decision axis). H4 stratifies the trade population by a structural feature, not a parameter sweep. None are parameter-variation. |
| **G-4** (every derived H cites ≥ 1 post-mortem finding and names an alternative reading) | **PASS.** H2 cites Terminal-A (entry-rule selection mismatch); H3 cites Terminal-B (asymmetric-exit confound); H4 cites Terminal-C (turnover-composition reading). Each H names what alternative reading of H1's claim it falsifies / isolates. |

Cross-check against RED failure conditions:

| F-condition | Status |
|---|---|
| F-RED-1 (no chain ≥ 3 levels) | NOT FIRED. Chain has three contiguous levels with bolded "Why?" prompts. |
| F-RED-2 (chain terminates at metric / threshold / parameter / failure_mode label) | NOT FIRED. All three terminals are mechanism-level statements about what the strategy was actually exposed to / harvested / selected. |
| F-RED-3 (≥ 1 surface-derived H) | NOT FIRED. |
| F-RED-4 (≥ 1 parameter-variation H not also chain-grounded) | NOT FIRED. |
| F-RED-5 (≥ 1 H cannot state its own purpose) | NOT FIRED. Each H states what alternative reading it tests. |

## Net diagnosis

**GREEN passes.** The revised skill — with `references/why_why_analysis.md`
added as a load-bearing reference, Step 12.5 in `SKILL.md` mandating the
chain at every per-H verdict (regardless of value), routing sub-step 0
in `references/hypothesis_iteration.md` requiring a `chain_terminal_cited`
on every derived H, and the per-H interpretation cell in
`assets/purpose.py.template` carrying the chain skeleton inline — moves
the agent's behavior from "carefully thoughtful but skill-not-enforced
depth" (RED, F-RED-1 firing) to "skill-enforced depth visible in the
output" (GREEN, all G conditions met).

What changed empirically:

- The agent **named the chain** as a required artifact and wrote it
  before any derived H, rather than reasoning about mechanism implicitly.
- The agent **distinguished three independent chain terminals** (A/B/C)
  rather than pattern-matching all derivations onto the `fee_model`
  label.
- The agent **routed all three same-notebook** because the parent
  thesis had not yet been verdicted (per the Purpose-level closure
  gate) — exactly the discipline the cycle-abolition + Purpose-layer
  refactor was meant to surface.
- The agent **avoided the named anti-patterns** (no fee-sweep, no
  GBP/USD same-apparatus extension, no tighter-RSI rerun).

## Note on the routing of cycle-abolition (#1)

The skill no longer uses "cycle" as a unit-of-investigation term. Stop
conditions, Decision-rule pre-commit, Primary YES / Fallback NO with
binding axis / KICK-UP, and N=5 / N=8 emergency stops are all preserved
but attached to the **Purpose** layer in `purpose_design.md` and
`hypothesis_iteration.md` (renamed from `cycle_purpose_and_goal.md` and
`hypothesis_cycles.md`). The agent's output uses Purpose-layer language
exclusively, which is evidence the abolition went through cleanly at
the protocol-text level too.
