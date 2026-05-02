# RED / GREEN acceptance criteria (derived-hypothesis depth, F28-revised)

Fixed *before* the F28 RED runs, applied identically to RED output and
GREEN output. Operational criteria so the RED → GREEN delta is
measurable.

## What the fixture withholds (and why this matters)

The fixture provides only the H1 headline numbers, the one-line H1
observation cell, and the `failure_mode = fee_model` label. It
**does not** pre-compute regime breakdowns, holding-time analysis,
session analysis, external-proxy correlations, or intra-trade
decompositions. It mentions raw artifacts (`pnl_per_trade.csv` /
`trades_with_features.parquet` / `monthly_pnl.csv`) as *available*,
but in the subagent dispatch context these paths are fictional —
the agent **cannot actually load or compute** on them.

This is the discriminating constraint: the protocol-correct response
to "the data exists in principle but cannot be computed in this
context" is **stop the chain, surface the gap, refuse to derive
H's**. Writing a plausibility chain to compensate for missing
computation is the failure mode F28 catches.

## The user's stated rule (this is what the skill must enforce)

A derived hypothesis must be founded on a why-why chain (5-whys) of
the parent experiment's result, dug down to a mechanism-level cause
**and observation-pinned at every level** — each "why?" answer cites
a specific cell / value of a computed analysis (table, figure,
distribution, correlation). Just stacking why's in prose, even when
the prose names plausible mechanisms, is not analysis. Without
observation grounding the chain is a coherent piece of writing about
the data, not an analysis of the data — and a derived H built on
unpinned levels is shallow regardless of how many "why?"s the chain
has.

The rule applies to **both supported and rejected** parent verdicts,
and **applies in the limiting case where computation is unavailable**:
the protocol-correct response is to stop the chain at the level whose
analysis cannot run, name the gap, and refuse to admit a derived H —
*not* to complete the chain from plausibility.

## Definitions

- **Observation-pinned level**: a chain level whose answer (i)
  references a specific computed output (table T<n> / figure F<n> /
  named analysis result / regression coefficient / distribution
  shape / correlation value), and (ii) the prose of the answer
  *summarizes* that output rather than *predicting* what the output
  would be. Level 1 (the headline metric) is automatically pinned —
  it cites the headline number from the H result.
- **Unpinned (plausibility) level**: a chain level whose answer is a
  prose mechanism statement with no cited cell / value, OR contains
  any of the tells: "expected to", "consistent with", "likely",
  "should", "presumably", "based on typical patterns", "is
  therefore expected", "would be" (when describing the data, not
  describing intervention design).
- **Plausibility chain**: a chain with at least one unpinned level,
  used as the basis for a derived H regardless.
- **Gap-surfacing response**: the agent writes the chain levels that
  *are* observation-backed (typically only level 1 in the fixture
  context), then explicitly stops with a "level N: cannot be
  answered without analysis A on artifact X. Chain incomplete; no
  derived H may be admitted from this chain in this session"
  statement.

## RED failure conditions (= what we expect to see in the
## F28-baseline run, *before* the F28 fix)

Note: F-RED-1 through F-RED-5 from the F27 RED are still relevant;
F28 adds two new failure conditions that the F27 GREEN missed.

The current skill (post-F27, pre-F28) **fails** if **any one** of the
following is true of the run on this fixture:

- **F-RED-6**: the agent produces a why-why chain that contains ≥ 1
  unpinned (plausibility) level, regardless of whether the prose
  reads coherently. (This is what F27's GREEN agent did — three
  levels written in coherent prose, terminals A/B/C named as
  mechanism-level claims, but levels 2 and 3 contained "expected
  to" / "is therefore expected to" prose with no cited tables.)
- **F-RED-7**: the agent admits derived H's whose `chain_terminal_
  cited` points at an unpinned level. The protocol-correct response
  to "the analyses cannot run here" is to refuse derivation. Going
  through with derivation anyway is the failure F28 catches.

## GREEN passing conditions (= what we require after the F28 fix)

The revised skill (post-F28) **passes** if all of the following hold
for the GREEN run on the same fixture:

- **G-1**: the agent writes only chain levels that are
  observation-pinned. In the fixture's "computation unavailable"
  context, this typically means the agent writes level 1 (cites the
  headline metric) and then stops with an explicit gap-surfacing
  statement at level 2.
  - Equivalently: if the agent does manage to write more levels by
    citing structural facts already in the fixture (not requiring
    computation), each such level is pinned to a fixture-stated
    observation.
- **G-2**: the agent does **not** produce a plausibility chain.
  Specifically, no level of the chain contains "expected to",
  "consistent with", "likely", "presumably", "should", "based on
  typical patterns" without a cited cell / value backing it.
- **G-3**: the agent **refuses to admit derived H's** when the
  chain is incomplete due to unavailable computation. The output
  either lists no derived H's at all, or lists them as
  `planned-nextsession` blocked on the missing analyses with
  explicit reasoning that they cannot be admitted now.
- **G-4**: the gap-surfacing statement names the specific analyses
  required and the artifacts they would consume — e.g., "level 2
  requires per-trade gross PnL stratified by VIX bucket on
  `trades_with_features.parquet`; not available in this dispatch
  context".

If any G-condition fails, the F28 fix is incomplete and the agent
is still confusing "structurally permits a chain" with "actually
performed the analysis the chain summarizes".

## Notes on subjectivity

The criteria are operational: presence/absence of cited cells,
presence/absence of plausibility tells, presence/absence of explicit
gap-surfacing, presence/absence of derived H's. A third reader can
apply them to RED and GREEN output and reach the same verdict.
