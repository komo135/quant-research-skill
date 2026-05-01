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
from what its name claimed it was doing. Concretely, terminal
answers describe:

- What the entry rule **actually selected for** (vs. what it claimed
  to select for) — e.g., "RSI≤30 selects extremes, but ~75 % of
  RSI≤30 occurrences in this universe are concentrated in high-vol
  regimes; what the entry rule selects for is high-vol participation,
  not mean-reversion specifically".
- What the trades **actually harvested** (vs. the mechanism the H
  named) — e.g., "the asymmetric signal-flip exit cuts losers fast
  and lets winners run; the strategy's positive return is sourced
  from trend-tail asymmetry of the exit, not from reversion of the
  entry signal".
- What the strategy was **exposed to** — e.g., "monthly PnL
  correlates 0.61 with managed-futures indices and 0.06 with
  EUR/USD's own monthly return; the strategy is a long-vol overlay
  with a mean-reversion label".
- What **structural property of the data or apparatus** drove the
  result — e.g., "fee-binding behavior is concentrated in the
  shortest holding-time tercile, which contributes 78 % of the
  per-trade fee burden; turnover, not signal alpha, is what failed".

Terminal answers that **do not** count as mechanism-level (= the
chain has not bottomed out):

- "Sharpe was 0.32." → metric.
- "Break-even fee was 0.42 bp/side." → threshold.
- "The fee assumption was too high." → parameter.
- "`failure_mode = fee_model`." → label.
- "The entry threshold was wrong." → parameter.
- "The signal was noisy." → vague (no mechanism named).
- "It didn't work in this universe." → no mechanism named.

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
   it takes to push the chain past metric / threshold / label level.

2. **Write the chain.** Three or more levels, contiguous, with each
   answer becoming the subject of the next "why?".

3. **Audit the terminal answer** against the "mechanism-level"
   definition above. If the terminal is still a metric / threshold /
   parameter / label, the chain has not bottomed out — keep digging.

4. **Pass the chain to the derived-H gate.** Each derived H must
   cite a specific terminal answer; if no derived H follows, write
   the chain anyway (the next session inherits it).

## Worked example — rejected verdict

Parent H1: "RSI(14)≤30 entry × signal-flip exit on EUR/USD H1 beats
B&H test Sharpe by ≥ 0.5 with fee 1 bp/side." Verdict = rejected.
`failure_mode = fee_model` (break-even fee 0.42 bp/side).

**Mechanism-level analyses run.** Per-trade PnL by VIX bucket;
holding-time by trade outcome; monthly PnL correlation with
BarclayHedge CTA Index and SPX 1m straddle PnL; intra-trade
reversion-vs-trend decomposition.

**Chain.**

> **Why was H1 rejected?**
> Because break-even fee (0.42 bp/side) is well below the deployment
> fee assumption (1 bp/side). Per-trade unit economics did not survive
> realistic cost.
>
> **Why is the per-trade unit economics that thin?**
> Because the strategy's gross PnL is concentrated in a sub-population
> of trades (75 % of gross PnL from the top three VIX buckets, which
> are 36 % of trades) and the remaining 64 % of trades pay fees
> without contributing edge.
>
> **Why is the gross PnL concentrated in high-vol regimes?**
> Because what RSI(14)≤30 actually selects for in this universe is
> not "the cross-section of mean-reversion opportunities" but
> "moments of unusual price displacement" — most of which coincide
> with high realized volatility. The asymmetric signal-flip exit
> (winners hold 11.8 h, losers hold 2.9 h) then converts the
> long-vol exposure into a positive-skew return stream. Monthly PnL
> correlates 0.61 with the BarclayHedge CTA Index and 0.06 with
> EUR/USD's own monthly return — the strategy's monthly signature
> is a long-vol / trend-following overlay, not a directional
> mean-reversion stream. Intra-trade decomposition: 65 % of PnL
> comes from the trend phase after first reversion, only 35 % from
> the reversion phase itself.

**Terminal answer (mechanism-level).** "What H1 actually tested was
'asymmetric-exit harvesting of long-vol exposure', not 'mean-reversion
on RSI extremes'. The fee burden is thin because the *non-high-vol*
trades — which the entry rule should have selected if the mechanism
were genuine MR — pay fees without contributing edge. The
`failure_mode = fee_model` label is correct as far as it goes, but the
deeper cause is mechanism misspecification: the apparatus does not
test mean-reversion."

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

**Mechanism-level analyses run.** Per-stock contribution to PnL;
factor exposure decomposition (size / value / quality / low-vol /
sector) on the LS portfolio's daily returns; PnL contribution by
liquidity bucket; turnover and per-stock holding distribution.

**Chain.**

> **Why was H7 supported?**
> Because the LS-decile portfolio's test Sharpe (0.51) cleared the
> +0.30 gate vs. EW.
>
> **Why did LS-decile clear the gate?**
> Because the long-decile generated a +0.21 Sharpe contribution and
> the short-decile generated a +0.30 Sharpe contribution; the short
> leg accounted for ~60 % of the spread.
>
> **Why is the short leg the dominant contributor?**
> Because the short leg's stocks are concentrated in the bottom three
> liquidity quintiles (60 % of short-leg names), and that sub-universe
> exhibits much stronger short-side mean-reversion-of-extremes after a
> 20-day move than the top quintiles do. Factor decomposition shows
> 70 % of the short-leg PnL is unexplained by size / value / quality /
> low-vol exposures — i.e., the short leg's PnL is not a smart-beta
> proxy. The "20-day momentum" label is technically correct but the
> mechanism is more specific: short-side reversion-of-overreaction in
> low-liquidity TOPIX500 names, with average per-stock holding 18
> trading days.

**Terminal answer (mechanism-level).** "What H7 actually tested,
empirically, is 'short-side reversion-of-overreaction in
low-liquidity TOPIX500 names after a 20-day push'. The 'momentum'
framing was the H1 design label; the realized exposure is more
specific."

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
