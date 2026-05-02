# GREEN findings — F28 observation-grounding (after F27 plausibility-stacking gap)

## Setup recap

Same fixture as F27's RED/GREEN: only H1 headline + one-line
observation cell + `failure_mode = fee_model`. The fixture mentions
raw artifacts as available, but in subagent dispatch context the
agent cannot actually load or compute them — paths are fictional.
Subagent dispatched under the F28-revised skill; `acceptance_criteria.md`
and prior `RED_findings.md` / `GREEN_results.md` withheld.

## What changed in F28 vs. F27

F27 added the why-why chain requirement (≥3 levels, mechanism-level
terminal). F27's GREEN run nominally satisfied the structural rule
but produced a chain whose levels 2 and 3 contained "expected to" /
"is therefore expected to" prose with no cited tables — a
plausibility ladder reading as if the analyses had been run, when
they had not. F28 patches the gap F27 left:

- Each chain level must cite a specific computed observation (table
  cell / value / distribution / correlation), not a prose mechanism
  statement unbacked by data.
- When the analysis required for a level cannot be performed (e.g.,
  data unavailable, dispatch context, computation out of scope),
  the protocol-correct response is to stop the chain at that level
  and surface the gap explicitly, not to fill it from plausibility.
- A derived H whose `chain_terminal_cited` points at an unpinned
  level is rejected at routing sub-step 0 — the citation must point
  at observation, not plausibility.

## What the subagent produced

**Why-why chain (incomplete, gap-surfacing):**

> Level 1: net Sharpe 0.32 < 0.5 floor; break-even fee 0.42 bp/side
> < 1 bp/side. Pinned to **H1 headline result table**.
>
> Level 2: cannot be answered without further analysis on artifacts
> available in this session. **Five specific analyses named** with
> the artifact each consumes:
>
> 1. Per-trade gross PnL stratified by entry-time vol regime on
>    `trades_with_features.parquet`.
> 2. Holding-time distribution by outcome on `pnl_per_trade.csv`.
> 3. Intra-trade return decomposition on the trade log.
> 4. Monthly PnL correlations against external proxies on
>    `monthly_pnl.csv`.
> 5. Fee burden by holding-time tercile.
>
> **Chain incomplete. No derived H may be admitted from this chain
> until at least one level-2 analysis is computed and pinned.**

**Derived H's:** none admitted. The agent lists three candidate H's
(low-fee re-run / tighter-RSI / lower-frequency Purpose) as
`planned-drop` rows — *audit trail of what was considered and
resisted*, not derived hypotheses entering the routing decision.

## Evaluation against `acceptance_criteria.md`

| Criterion | Verdict |
|---|---|
| **G-1** (only observation-pinned levels written; gap-surfacing at first uncomputable level) | **PASS.** Level 1 is pinned to the headline result table. Level 2 is an explicit gap statement naming the missing analyses. The agent does not produce levels 3+ as plausibility prose. |
| **G-2** (no plausibility tells without cited cells: "expected to" / "consistent with" / "likely" / etc.) | **PASS.** The agent's prose contains no plausibility tells; everything past level 1 is structured as "would be answered by analysis X on artifact Y". |
| **G-3** (refuses to admit derived H's when the chain is incomplete) | **PASS.** No derived H is admitted. The three candidate H's are recorded as `planned-drop, rejected at admissibility 0` with the chain-incomplete reason in each row. |
| **G-4** (gap-surfacing names specific analyses + the artifacts they consume) | **PASS.** Each of the five named analyses is paired with the specific fixture-listed artifact path. The "next protocol-correct action" suggestion further pins which analysis is the cheapest first cut. |

Cross-check against the F28-specific RED conditions (would have
fired on the F27 GREEN):

| F-condition | Status |
|---|---|
| **F-RED-6** (≥1 unpinned plausibility level present in the chain) | NOT FIRED. The agent stops rather than writing plausibility levels. |
| **F-RED-7** (derived H admitted with `chain_terminal_cited` pointing at an unpinned level) | NOT FIRED. No derived H admitted; candidates explicitly rejected at admissibility 0. |

## Net diagnosis

**F28 GREEN passes.** The revised skill — with the
`why_why_analysis.md` "Observation grounding" section requiring
cited cells / values at each level, the worked examples rewritten
to show table-citation-per-level instead of prose-mechanism-per-
level, the "stop and surface the gap" rule for unavailable
computation, the new anti-rationalization entries ("named the
mechanism, that's the terminal" / "analyses are expensive — write
from what they would probably show" / "chain reads coherently
without numbers" / "computation unavailable in this context"), the
SKILL.md Step 12.5 extension covering the gap-surfacing requirement
and the unpinned-citation rejection rule, and the
`hypothesis_iteration.md` admissibility sub-step 0 extension
explicitly making citation-to-unpinned-level inadmissible — moves
the agent's behavior from "structurally has a chain, contents are
plausibility" (F27 GREEN, F-RED-6 firing) to "writes only what is
observation-pinned and refuses to derive when computation is
unavailable" (F28 GREEN, all G conditions met).

What changed empirically:

- The agent **stopped at level 2** rather than completing the chain
  with "expected to" / "consistent with" prose.
- The agent **named five specific analyses + artifacts** rather
  than describing what the analyses would supposedly find.
- The agent **refused to admit any derived H** rather than
  forcing-fit derivations onto an incomplete chain.
- The agent **recorded the three natural inadmissible derivations**
  (low-fee re-run / tighter-RSI / lower-frequency paraphrase) as
  `planned-drop` rejected at admissibility 0 — preserving an audit
  trail of "what was considered and resisted" at the right
  granularity.

## Note on the relationship to F27

F28 is a refinement of F27, not an independent failure mode. F27
got the structural shape right (chain ≥ 3 levels, mechanism-level
terminal) but accepted prose mechanism statements as terminals,
which an agent could satisfy by stacking plausible "why?"s without
actually computing the post-mortem. F28 closes that gap by
requiring observation grounding at every level. The two compose:
F27 is the chain-must-exist gate; F28 is the chain-must-stand-on-
data gate. Each is necessary; neither alone is sufficient.
