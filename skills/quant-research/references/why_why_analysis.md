# why_why_analysis.md

How an H result becomes a *mechanism-level reading* before any derived H
is allowed to leave the parent. Without this step, derived H's are
generated from the bare verdict / `failure_mode` label of the parent
and the protocol cannot tell what they are for.

## When to read

- **Every time an H block has just been verdicted** — supported,
  rejected, partial, or parked. Not optional, not conditional on
  "the result was surprising"; the chain runs on every verdict.
- **Before** writing any derived H into `hypotheses.md` or into the
  next `## H<id>` block.
- **Before** the per-H "interpretation for H<id>" cell is treated as
  finished.

## The rule

A derived hypothesis must be founded on a **why-why chain (5-whys)**
of the parent H's result, dug down to a **mechanism-level cause**.
The bare fact of the parent's verdict — including the
`failure_mode` label — is **not** a legitimate root for a derived H.

The rule applies to **both supported and rejected** parent verdicts:

- A rejected H without a why-why chain produces "the parent failed,
  let's tweak X" derivations — surface refinements aimed at recovery.
- A supported H without a why-why chain produces "the parent worked,
  let's try a sibling instrument / period / regime" derivations —
  surface extensions aimed at proliferation.

Both are the same shallowness pattern (deriving from the verdict
rather than from the mechanism). Both are forbidden.

## What "mechanism-level" means

The chain terminates only when the next "why?" can no longer be
answered by another metric, threshold, parameter, or failure_mode
label. At the terminal level, the answer must be a statement about
**what the strategy was actually doing in the world** — distinct
from what its name claimed it was doing — **and the answer must be
backed by a specific computed observation**, not by a prose
hypothesis the data would supposedly support (see "Observation
grounding" below). Concretely, terminal answers describe:

- What the entry rule **actually selected for** (vs. what it claimed
  to select for) — backed by a stratification of entries by some
  feature (vol regime, session, regime indicator) showing the
  selection bias. Example terminal: "RSI≤30 selects extremes, but
  the computed gross-PnL distribution by VIX-bucket on this universe
  is [VIX<12: 6%, 12-18: 18%, 18-25: 28%, 25-35: 38%, ≥35: 10%]
  (table T2) — the top three buckets are 36% of trades and produce
  75% of gross PnL, so what the entry rule selects for is high-vol
  participation, not mean-reversion specifically".
- What the trades **actually harvested** (vs. the mechanism the H
  named) — backed by an intra-trade decomposition or
  holding-time-by-outcome table. Example: "Per-trade decomposition
  (table T5) shows the reversion phase is 35% of intra-trade gross
  return and the trend phase is 65%; combined with mean holding
  time of winners 11.8h vs losers 2.9h (table T3), the strategy's
  positive return is sourced from trend-tail asymmetry of the exit".
- What the strategy was **exposed to** — backed by an external-proxy
  correlation table. Example: "Monthly PnL correlation
  (table T4): BarclayHedge CTA = 0.61, SPX 1m straddle = 0.49,
  EUR/USD monthly = 0.06; the strategy is a long-vol overlay
  with a mean-reversion label".
- What **structural property of the data or apparatus** drove the
  result — backed by a stratification of the binding metric by
  trade sub-population. Example: "Fee burden by holding-time
  tercile (table T6): bottom tercile 78%, middle 15%, top 7%;
  turnover composition, not signal alpha, is what `fee_model`
  encodes here".

Terminal answers that **do not** count as mechanism-level (= the
chain has not bottomed out):

- "Sharpe was 0.32." → metric.
- "Break-even fee was 0.42 bp/side." → threshold.
- "The fee assumption was too high." → parameter.
- "`failure_mode = fee_model`." → label.
- "The entry threshold was wrong." → parameter.
- "The signal was noisy." → vague (no mechanism named).
- "It didn't work in this universe." → no mechanism named.
- "RSI≤30 likely selects high-vol participation in this universe." →
  prose hypothesis without observation. "Likely" is the tell.
- "Asymmetric exit is consistent with trend-tail harvesting." →
  "consistent with" = the data has not been computed; the level is
  reasoning about what the data would show, not citing what it
  shows.

## Observation grounding (= the rule the chain stands on)

Each "why?" answer in the chain — including the terminal — must
**cite a specific computed observation** from the parent
experiment's artifacts: a numeric value, a stratified table cell, a
distribution shape, a correlation, a regression coefficient, a
ranked breakdown. The observation is named, computed, and visible
(as a table or figure) in the notebook before the chain references
it; the chain's prose is a *summary of* that observation, not a
*description of* what the observation would supposedly be.

Two layers, both required:

1. **Named analyses performed and their output visible.** Before
   any chain level past level 1 can be answered, the analysis it
   draws on has been computed and its output (a table, a
   distribution, a correlation matrix, a stratified statistic)
   exists as a cell in the notebook with a referenceable label
   (e.g., "table T3: holding-time distribution by trade outcome").
2. **Each level's claim pins to a specific cell / value of that
   output.** "Gross PnL is concentrated in high-vol regimes" is
   not yet pinned. "Per table T2 the top three VIX buckets are
   36% of trades and produce 75% of gross PnL" is pinned. The
   prose in the chain is a one-line summary; the value lives in
   the cited table.

A chain level whose answer **does not pin to a cited cell / value**
is not bottomed out — even if the prose names a mechanism. Common
tells that the level is unpinned:

- "expected to" / "is expected to" / "should" / "ought to"
- "consistent with" / "would be consistent with"
- "likely" / "presumably" / "presumably because"
- "based on typical patterns" / "in this kind of strategy"
- prose mechanism statements with no number nearby and no
  table / figure citation

When the analysis a level depends on **cannot be performed** (e.g.,
data unavailable, the artifact required does not exist, the
computation is out of scope for the current session), the
protocol-correct response is to **stop the chain and surface the
gap** — not to complete the chain from plausibility. Concretely:
write the levels that *are* observation-backed, then a final entry
that says:

> **Level N: cannot be answered without analysis A on artifact X.**
> Chain incomplete. No derived H may be admitted from this chain
> until A is computed and table T<n> is present.

The chain is *not eligible* to ground a derived H's
`chain_terminal_cited` until every level (including the terminal)
is pinned. This is the discipline that distinguishes "ran the
post-mortem" from "described the post-mortem the data would
probably show". The latter is the failure mode this rule exists to
catch.

## Required shape of the chain

- **At least three consecutive levels.** Each "why?" question takes
  the previous answer as its subject and asks "why is *that*?" until
  the terminal level is reached.
- **Written contiguously.** The chain is a single readable artifact in
  the per-H "interpretation" cell of the notebook (and / or in
  `decisions.md`'s Purpose entry under the H sub-bullet) — not
  scattered across multiple cells, not implicit.
- **Cited by every derived H.** Each derived H's per-H design header
  cites the specific terminal answer from the chain that the H is
  designed to falsify or isolate. A derived H that does not cite a
  chain terminal is inadmissible (see "Admissibility integration"
  below).

## Required steps

1. **Run the per-H mechanism-level analyses needed to support the
   chain.** Headline numbers + verdict + `failure_mode` label are
   not enough material to dig with. At minimum, look at *some* of:

   - Per-trade PnL composition by regime (vol bucket, session-of-day,
     macro regime) — surfaces conditional exposure.
   - Holding-time distribution by trade outcome — surfaces exit-rule
     asymmetry.
   - Monthly / weekly PnL correlation with external proxies (vol
     indices, managed-futures indices, factor returns) — surfaces
     conflation with known exposures.
   - Intra-trade return decomposition (reversion vs. trend phase) —
     surfaces what the trade actually harvested.
   - Sub-population stratification (terciles by signal strength /
     holding time / regime / instrument) of the binding metric —
     surfaces whether the headline result is uniform or driven by a
     sub-population.

   The choice of which to run is judgment. The minimum is whatever
   it takes to push the chain past metric / threshold / label level
   *with each level pinned to a computed observation* (see
   "Observation grounding" above). Computing one analysis to support
   one level is the unit; "I'll run the analyses later, write the
   chain now" is the failure mode this step exists to interrupt.

2. **Write the chain.** Three or more levels, contiguous, with each
   answer becoming the subject of the next "why?". **Each level
   cites a specific cell / value of an analysis output** (table T<n>,
   figure F<n>, regression coefficient, distribution shape) computed
   in step 1.

3. **Audit the terminal answer** against the "mechanism-level"
   definition above. If the terminal is still a metric / threshold /
   parameter / label, the chain has not bottomed out — keep digging.
   **Audit each non-terminal level for observation grounding** — if
   any level's prose contains "expected to" / "consistent with" /
   "likely" / "should" without a cited cell, the chain is not yet
   eligible. Either compute the missing analysis or stop the chain
   and surface the gap (per the "Observation grounding" rule).

4. **Pass the chain to the derived-H gate.** Each derived H must
   cite a specific terminal answer; if no derived H follows, write
   the chain anyway (the next session inherits it). A chain whose
   levels are not all observation-pinned is **not eligible** to
   ground a derived H — the agent stops and surfaces the gap rather
   than admitting a derived H from a partial chain.

## Worked example — rejected verdict

Parent H1: "RSI(14)≤30 entry × signal-flip exit on EUR/USD H1 beats
B&H test Sharpe by ≥ 0.5 with fee 1 bp/side." Verdict = rejected.
`failure_mode = fee_model` (break-even fee 0.42 bp/side).

**Mechanism-level analyses run** (each produces a referenceable
output cell in the notebook before the chain is written):

- **Table T2** — per-trade gross PnL by entry-time VIX bucket
  (5-bucket: <12 / 12-18 / 18-25 / 25-35 / ≥35).
- **Table T3** — holding-time distribution conditional on trade
  outcome (winners vs. losers).
- **Table T4** — monthly PnL correlations against BarclayHedge CTA
  Index, SPX 1m ATM straddle PnL, EUR/USD monthly return.
- **Table T5** — intra-trade return decomposition (reversion phase
  before first sign-flip vs. trend phase after).

**Chain.** Each level pins to a cited cell / value.

> **Why was H1 rejected?**
> Because break-even fee (0.42 bp/side, headline table) is below the
> deployment fee assumption (1 bp/side). Per-trade unit economics
> did not survive realistic cost.
>
> **Why is the per-trade unit economics that thin?**
> Per **table T2**, gross PnL by VIX bucket is
> [<12: 6%, 12-18: 18%, 18-25: 28%, 25-35: 38%, ≥35: 10%]; the top
> three buckets are 36% of trades and contribute 75% of gross PnL.
> The remaining 64% of trades pay round-trip fees on a per-trade
> gross PnL too small to clear them.
>
> **Why is the gross PnL concentrated in the high-vol buckets, and
> what is the apparatus actually testing?**
> Three observations pin this:
>
> - **Table T3** — winners' mean holding time is 11.8h vs. losers'
>   2.9h; the asymmetric signal-flip exit cuts losers fast and lets
>   winners run.
> - **Table T4** — monthly PnL correlation = 0.61 with BarclayHedge
>   CTA, 0.49 with SPX 1m straddle, 0.06 with EUR/USD's own monthly
>   return. The monthly signature is long-vol / trend-following, not
>   directional FX.
> - **Table T5** — intra-trade decomposition is 35% reversion phase /
>   65% trend phase; the dominant intra-trade source of return is
>   the trend phase after the first reversion, not the reversion
>   phase itself.
>
> Read together with table T2's regime concentration: what the
> RSI(14)≤30 entry actually selects on this universe is high-vol
> participation, and the asymmetric exit then harvests trend tails
> within those participations.

**Terminal answer (mechanism-level, observation-pinned).** "What
H1 actually tested, per tables T2/T3/T4/T5, was 'asymmetric-exit
harvesting of trend tails on a high-vol-biased entry population',
not 'mean-reversion on RSI extremes'. The fee burden is thin
because the non-high-vol trades — which the entry rule should have
selected uniformly if the mechanism were genuine MR — pay fees on
small per-trade gross PnL (T2 buckets <12 and 12-18). The
`failure_mode = fee_model` label is correct at level 1; the
mechanism-level cause is misspecification of what the apparatus
selects and harvests."

**What the chain licenses (= admissible derived H's).**

- An H that *isolates* mean-reversion edge from long-vol exposure —
  e.g., regress monthly PnL on a long-vol benchmark and test whether
  the residual carries a mean-reversion signature.
- An H that *swaps the exit rule* to a non-asymmetric form (TP/SL or
  pure-reversion) on the same entry, to test whether asymmetric
  exits manufacture the apparent edge.
- An H that *isolates the entry rule's information content* by
  comparing the H1-entry × symmetric-exit leg against a
  random-entry × asymmetric-exit leg, attributing edge between
  entry and exit.

**What the chain does NOT license.**

- An H that *lowers the fee assumption* — that addresses the metric
  layer of the chain (level 1), not the mechanism level. Inadmissible
  unless re-justified from the chain terminal.
- An H that *extends to GBP/USD with the same apparatus* — the
  apparatus has been characterized as testing the wrong mechanism;
  porting it to a sibling pair propagates the same misspecification.
- An H that *tightens RSI to ≤ 20* — parameter sweep on the layer-1
  cause. Inadmissible.

## Worked example — supported verdict

Parent H7: "Cross-sectional 20-day momentum on TOPIX500 LS-decile
beats EW baseline by test Sharpe ≥ 0.30." Verdict = supported (test
Sharpe = 0.51).

**Mechanism-level analyses run** (each produces a referenceable
output cell before the chain is written):

- **Table U1** — per-stock contribution to PnL, ranked.
- **Table U2** — Sharpe decomposition by leg (long / short) for
  the LS portfolio.
- **Table U3** — short-leg holdings stratified by liquidity quintile
  (1 = least liquid).
- **Table U4** — Fama-French / quality / low-vol factor regression
  on the LS portfolio's daily returns.
- **Table U5** — turnover and per-stock holding-period distribution.

**Chain.** Each level pins to a cited cell / value.

> **Why was H7 supported?**
> Because the LS-decile portfolio's test Sharpe (0.51, headline
> table) cleared the +0.30 gate vs. EW.
>
> **Why did LS-decile clear the gate?**
> Per **table U2**, the long-leg contributed Sharpe = 0.21 and the
> short-leg contributed Sharpe = 0.30; the short leg accounts for
> ≈60% of the spread. The result is asymmetric across legs.
>
> **Why is the short leg the dominant contributor?**
> Two observations pin this:
>
> - **Table U3** — 60% of short-leg names sit in the bottom three
>   liquidity quintiles (Q1 + Q2 + Q3 of trailing-21d ADV). That
>   sub-universe's short-side cross-sectional return after a 20-day
>   push is materially more negative than the top-two-quintile
>   sub-universe (per-quintile breakdown in U3, with the bottom-3
>   group at -1.8% mean 21d-forward vs. -0.4% in Q4+Q5).
> - **Table U4** — factor regression of the LS daily PnL shows R² =
>   0.30, with size / value / quality / low-vol jointly explaining
>   only ~30% of variance; ≈70% of the spread is residual to those
>   four factors. Short-leg-only regression gives the same shape.
>
> The "20-day momentum" label correctly names the entry rule (= 20-d
> return rank), but per U3 + U4, the realized exposure is short-side
> reversion-of-overreaction concentrated in low-liquidity TOPIX500
> names, with the per-stock average holding period (table U5) of 18
> trading days.

**Terminal answer (mechanism-level, observation-pinned).** "What
H7 actually tested, per tables U2/U3/U4/U5, is 'short-side
reversion-of-overreaction in low-liquidity TOPIX500 names after a
20-day push, with ≈70% factor-residual return'. The 'momentum'
framing was the design label; the realized exposure (per U3's
liquidity stratification + U4's factor residual) is more specific."

**What the chain licenses.**

- An H that *isolates the short-leg / liquidity-bucket effect* by
  testing the long leg alone (under the original momentum framing)
  vs. the short leg alone in the bottom-liquidity sub-universe.
- An H that *tests the mechanism on a higher-liquidity universe*
  (TOPIX100 instead of TOPIX500), explicitly framed as a
  liquidity-mechanism falsification rather than a "extend to a
  sibling universe" extension.
- An H that *separates reversion-of-overreaction from continuation*
  by conditioning on the magnitude of the 20-day push.

**What the chain does NOT license.**

- An H that *extends to KOSPI200 with the same 20-day-momentum
  apparatus* — the H7 mechanism is liquidity-conditional, and a
  port to KOSPI200 without addressing that conditioning is
  surface-extension. Inadmissible without first stating which
  KOSPI200 sub-population the H is targeting under the H7
  mechanism.
- An H that *tries 30-day or 60-day windows* on the same universe —
  parameter sweep on H7's headline. Robustness, not a new H.

## Admissibility integration (= what changes for derived-H gating)

The derived-H admissibility gate (in `hypothesis_iteration.md`,
Routing rule sub-step 0) requires three properties of any derived
H. The why-why chain is the **fourth required property**, and it is
the property that prevents the other three from being satisfied
syntactically with no real depth:

| Property | Without why-why | With why-why |
|---|---|---|
| Own falsifiable claim distinct from parent | A claim on a different metric / threshold satisfies syntactically | The claim must isolate or falsify a specific chain terminal |
| Own stated purpose | "Test whether X under Y" suffices syntactically | The purpose must name the chain terminal it addresses |
| Meaningful research unit | "Bigger universe" / "different exit" satisfies syntactically | The unit must produce evidence that updates the chain (changes the terminal answer) |
| **Why-why chain citation (NEW)** | — | The H's design header cites a specific terminal answer; without the citation, the H is surface-derived and inadmissible |

The why-why citation is what prevents "I have a hunch about why H_n
failed" (rejected by Pathway 4, but the rejection is easy to evade
syntactically) from sneaking through as a sufficient
failure-mode-analysis entry. The chain replaces the hunch.

## Common rationalizations

| Excuse | Reality |
|---|---|
| "The verdict is unambiguous; the why-why is overhead." | The verdict is the *result*; the chain explains the result. The next H's purpose is derived from the chain, not from the verdict. Skipping the chain is what produces "I cannot state the H's purpose" failure. |
| "The `failure_mode` label *is* the cause." | A label is a one-word categorization; it is the chain's level-1 answer at most. Treating the label as the cause prevents the chain from reaching mechanism level. The label is necessary (it routes the H to the right `failure_mode` controlled-vocabulary value) but not sufficient. |
| "The H was supported, so there is nothing to dig into." | A supported H without a chain produces sibling-extension derivations ("now try GBP / try 30 days / try Q1 only") that propagate whatever the apparatus *actually tested*. If the apparatus tested a mechanism-misspecified version of the named claim, sibling extensions multiply the misspecification. The chain is what catches this before the next H is committed. |
| "Three levels is arbitrary." | Three is the minimum that forces the chain past metric → reason-shaped-like-metric → mechanism. Two levels are routinely satisfied with "low Sharpe → high fee", which is the surface failure this rule exists to interrupt. Three is the floor; chains often need four or five. |
| "I'll skip the chain on this H and run it on the next one." | Skipping is what produces a derived H that "cannot state its own purpose". The next H is the audit trail of the skip; running the chain at that point is too late — the derived H is already on the page. |
| "I ran the analyses but didn't write the chain — the analyses speak for themselves." | The chain is the artifact the derived-H gate reads. Analyses scattered across cells with no synthesis cannot be cited by a derived H's design header. The chain is the synthesis. |
| "The chain is just a post-hoc rationalization of the next H I already wanted to run." | If you already know the next H, write the chain *first* and check whether the chain terminal licenses that H. If it does not, the chain is doing its job — the H you wanted to run is surface-derived and the chain reveals what depth was missing. |
| "I named the mechanism — that's the terminal." | Naming a mechanism in prose ("the strategy harvests trend tails") is a hypothesis, not an observation. Without a cited table cell / distribution / correlation that the prose summarizes, the level is unpinned. Compute the analysis or stop the chain — do not paper over the gap with a plausible sentence. |
| "The analysis is expensive — let me write the chain from what it would probably show." | "Probably show" is the failure mode this rule is built to catch. A chain whose answers describe what the data *would* show, not what it *does* show, is a plausibility ladder dressed as a post-mortem. Stop the chain at the level whose analysis hasn't run; surface the gap as "level N: cannot be answered without analysis A on artifact X — chain incomplete". |
| "Each level reads coherently — the chain is fine even without numbers." | Coherent prose is the output an LLM produces by default; that is not evidence the chain reflects the data. The grounding rule exists *because* coherent prose is cheap. A chain with no numbers nearby and no table citations is a coherent piece of writing about the data, not an analysis of the data. |
| "The analyses can't be run in this context (subagent dispatch / sandboxed environment / data not loaded) — the chain is the best I can do." | Then the chain cannot be completed in this context, and the protocol-correct response is to write the levels that *are* observation-backed (often only level 1, the headline metric) and stop with "level N: requires analysis A — not available in this context. Chain incomplete; no derived H may be admitted." Writing a plausible chain to compensate for missing data inverts the discipline. |

## What the chain is *not*

- **Not a literature review.** Why-why is *internal* to this
  experiment's evidence; literature integration happens at H
  generation (see `hypothesis_generation.md`).
- **Not a robustness battery.** The robustness battery
  (`robustness_battery.md`) tests whether the headline result holds
  under perturbations. The chain explains *why the headline result
  is what it is*. Different question.
- **Not bug review.** Bug review (`bug_review.md`) asks whether the
  reported numbers are contaminated. The chain assumes the numbers
  are clean and asks what the strategy *actually did*.
- **Not experiment review.** Experiment review (`experiment-review`
  skill) asks whether the *claim* is warranted by the *design*. The
  chain asks what the realized *behavior* of the design tells us
  about the world.

The chain runs at the per-H interpretation step (notebook section 9
in the template), after bug-review's findings are reflected and
before any derived H is proposed. It is the entry point for the
derivation of the next H, not a review of the current one.
