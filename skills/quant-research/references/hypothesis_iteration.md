# hypothesis_iteration.md

Protocol for iterating hypotheses inside a Purpose: routing of derived
H's (same notebook vs. new notebook), admissibility, run-now /
next-session / drop classification, and the exhaustion triggers that
force the iteration to stop and re-examine the Purpose's frame.

## Scope and ownership split

This file owns **routing of derived H's** — same Purpose / same
notebook (next `## H<id>` block) vs. new Purpose / new notebook;
classification as run-now / next-session / drop. It does **not** own
*content generation* of derived H's, and it does **not** own
*cross-H synthesis* of multiple H's into a Purpose-level
meta-finding.

| Concern | Owned by |
|---|---|
| Why-why analysis of the parent H result | `why_why_analysis.md` |
| Routing (where the next H lives) | This file |
| Content generation of a derived H | `hypothesis_generation.md` Pathway 4 |
| Cross-H synthesis (Purpose-level meta-finding from H1…HN) | `cross_h_synthesis.md` |

The four files compose: `why_why_analysis.md` produces the
mechanism-level chain on which the derived H stands;
`hypothesis_generation.md` writes the H's substance with a pathway
declaration; this file places it in the right notebook;
`cross_h_synthesis.md` reads N H's together at Purpose closure to
extract what the cluster says that no single H said.

## When to read

- A Hypothesis round inside the current notebook has just been
  completed (its observation + verdict are filled, and the why-why
  chain per `why_why_analysis.md` has been written).
- A whole notebook (one Purpose) has been wrapped up.
- Before declaring overall completion.

## Principle

Research is fundamentally an **iteration of hypothesis → test →
mechanism-level reading → derived hypothesis → re-test**. Stopping
after one Hypothesis yields a single experiment, not research.

The iteration plays out at two scales:

| Scale | Where the next round happens |
|---|---|
| **Within a Purpose** (most rounds) | Next H block inside the same notebook |
| **Across Purposes** | Next notebook (`pur_<NNN+1>_*.py`) |

Default to within-a-Purpose. Crossing into a new notebook is
reserved for cases where the Purpose itself has shifted (see
`references/experiment_protocol.md` for the Purpose-change triggers).

## Why iteration exists — and what stops it (read before the exhaustion section)

Iteration exists to elevate single-experiment evidence into knowledge
durable enough that a downstream consumer can act on it. The
iteration's goal is therefore **the knowledge output that closes the
consumer's decision gap** — not "a `verdict='supported'` on H1", not
"a Pattern A-E label", not "publication-grade evidence in the
abstract". See `references/purpose_design.md` for the five
pre-implementation Purpose-header items (Consumer / Decision /
Decision rule / Knowledge output / target_sub_claim_id) that pin
this frame.

The Purpose's investigation has two distinct kinds of stop signal:

### Primary stops (the Purpose finished its job)

The investigation ends when **any** of these fire — these are the
*intended* closures:

1. **Primary YES** — enough sub-claims have evidence flags that the
   consumer can apply the YES branch of the decision rule. The
   YES-supporting H's pass `bug_review`, robustness battery, and
   `experiment-review`.
2. **Fallback NO with binding axis identified** — the cluster of H's
   produces a Pattern A (`failure_mode` shared across rejections), a
   Pattern C (Pareto frontier), or a Pattern E (special-case scope)
   that the consumer can apply the NO branch to and inherit the
   binding axis as documented prior. *This is a full research
   output, not a degraded YES.*
3. **KICK-UP** — a structural finding (often via `bug_review`,
   `experiment-review` `scope` dimension, or unresolvable upstream
   issue) reveals that the Purpose's frame is the wrong layer for the
   consumer's decision. The investigation closes with the structural
   finding as its output; the consumer (often the researcher's own
   next-Purpose decision) inherits "this layer must be solved first".

All three are equivalent research outputs; the equivalence is what
prevents "produce YES" from quietly becoming the goal (which
reintroduces selection bias one layer up from the H level).

### Emergency stops (iteration is failing to converge)

When primary stops do not fire and H's keep accumulating without
landing the decision rule, the protocol provides emergency stops to
prevent unbounded sunk-cost iteration. The exhaustion-trigger rule
below (N=5 advisory, N=8 hard cap) is the emergency-stop machinery.
Its role is to **force cross-H synthesis and re-examine whether the
Purpose's frame matches the consumer's decision** — not to define
when the Purpose should normally end. A Purpose that hits the N=5
advisory typically means one of:

- The decision rule's YES branch has thresholds the H portfolio
  cannot reach (rule too aggressive — re-evaluate).
- The Purpose is too broad and H's are testing different sub-claims
  (Pattern B — split into derived Purposes).
- The consumer's decision actually requires a KICK-UP that has not
  yet been recognized as such.

The fact that a Purpose hits the emergency stop at all is a signal
worth recording in `decisions.md` — it indicates a frame mismatch
that the project should learn from, not just a stop event.

## What to write at the end of each H round

### Inside the notebook body

```markdown
### H<id> conclusion
- Observed values: [Sharpe X, win rate Y, IC Z, ...]
- Verdict for H<id>: [supported / rejected / partially supported / parked]

### Why-why chain for H<id>
[≥3 consecutive levels per `references/why_why_analysis.md`,
terminating at a mechanism-level cause. Required for every verdict —
supported, rejected, partial, parked — before any derived H is
proposed. The chain is the artifact each derived H's design header
must cite.]

### Cannot conclude
- [State which dimensions are not tested by this H specifically]
```

That is all the notebook body carries about derived hypotheses
themselves. The notebook's research record stops at "what this H
said, what mechanism-level reading the chain produced, and what the
H did not say". Where the next H will live and when it will run is
*planning state*, not research record, and is kept out of the
notebook (see `references/post_review_reconciliation.md` F5 counter
and the four-layer model in `references/research_goal_layer.md`).

### Outside the notebook — hypotheses.md and decisions.md

Each derived hypothesis becomes a row in `hypotheses.md`:

| Where the derived H goes (per the routing rule below) | What `hypotheses.md` carries |
|---|---|
| Same notebook (Purpose unchanged) | New row, same `purpose_id` as the parent; Status = `planned-runnow` / `planned-nextsession`; `target_sub_claim_id` inherited from parent unless overridden in Statement column with reason; `pathway` declared (typically 4 = failure-derived); `chain_terminal_cited` recording which terminal answer of the parent's why-why chain the H is grounded in |
| New notebook (Purpose changed) | New row, new `purpose_id` (the next `pur_<NNN+1>_*.py`); Status = `planned`; `target_sub_claim_id` chosen from sub-claims still `not started` or `in progress`; `pathway` declared |
| Dropped | New row, Status = `planned-drop`; reason in the Statement column ("dropped: refuted in `papers.md`") |

Each Purpose closure also appends to `decisions.md` (see "Updating
decisions.md" below) — including the Research-goal sub-claim
progress update and the design-hypothesis verification at close.
Derived *Purposes* (= candidates for new notebooks) are listed in
the Purpose entry's "Derived Purposes" section there. Derived
*Hypotheses* are not re-listed in `decisions.md` — they live as
rows in `hypotheses.md`, single source of truth.

## Routing rule (the most important rule in this file)

When a derived H emerges, decide where it goes by the following
test, in order. Sub-step 0 (admissibility) runs **before** routing —
a candidate that fails admissibility is not an H at all and does not
enter routing; it is reclassified as robustness analysis or
engineering work and recorded in the parent H's section, not in
`hypotheses.md`.

0. **Admissibility — is this a hypothesis at all, or is it
   robustness on the parent?** A derived hypothesis is admissible
   only when it simultaneously satisfies all four:

   - **Why-why chain citation** — the H's per-H design header cites
     a specific terminal answer from the parent H's why-why chain
     (see `references/why_why_analysis.md`). The parent H's chain
     must already exist (≥ 3 levels, mechanism-level terminal,
     written in the parent's per-H "interpretation" cell or the
     `decisions.md` H sub-bullet). A derived H that does not cite
     a chain terminal is **inadmissible** — its existence relies on
     the bare fact of the parent's verdict / `failure_mode` label
     rather than on a mechanism-level reading. This admissibility
     test fires identically on parents with `verdict='supported'`
     and on parents with `verdict='rejected'`: a "the parent
     worked, let's try a sibling instrument" derivation that does
     not cite a chain terminal is the same shallowness pattern as
     a "the parent failed, let's vary the threshold" derivation,
     and is rejected for the same reason.
   - **Own falsifiable claim** distinct from the parent H (different
     decision axis, not just a tighter / looser threshold on the
     parent's axis). The "different axis" is what the chain
     terminal isolates — the citation makes the distinct-axis
     property explicit instead of leaving it as the researcher's
     intuition.
   - **Own stated purpose** in one sentence, written in the per-H
     design header *before* the H is run, answering "what new
     question does this H answer that the parent did not?" The
     answer must be derivable from the chain terminal — i.e., the
     "new question" is *to falsify or isolate the chain terminal*,
     not "to retry the parent under different parameters".
   - **Meaningful research unit** — the H is at the granularity of
     an independent finding, not a 1-axis sweep over sizing /
     threshold / regime / lookback / cost / fee. Sweeps belong in
     the Step 12 robustness battery, recorded inside the parent
     H's section as 2D / 3D grids.

   Inadmissible patterns (record as robustness inside parent H, not
   as a new H):

   - Sensitivity / parameter-sweep variant ("H1 + tighter threshold",
     "H1 + sizing variant", "H1 with 30-day lookback instead of 20").
   - Follow-on layer that does not change the underlying claim ("H1
     × vol-targeted sizing", "H1 + portfolio overlay", "H1 with
     trailing stop adjusted").
   - Threshold-variation rerun aimed at recovering a rejected H1.
   - Diagnosis without an independent claim ("rerun H1 with a
     smaller test set to see what happens").
   - **No why-why chain or chain not at mechanism-level** — the
     derived H proposal arrived without the parent's chain in
     place, OR the parent's chain terminates at a metric / threshold
     / parameter / `failure_mode` label rather than a mechanism-level
     cause. Run the chain first per `why_why_analysis.md`; only then
     is a derived H eligible.

   When inadmissible, the work is real and may still be necessary,
   but it is **not** an H<id> and does not get its own row in
   `hypotheses.md` or `results.parquet`. It lives inside the parent
   H's robustness section and contributes to the parent H's verdict,
   not to a new verdict of its own.

1. **Does the current notebook's Purpose statement still cover the
   new H?**
   - Yes → run sub-step 1.5 below before placing the H.
   - No → the new H reflects a new Purpose; it goes in the next
     notebook. Conjunct contribution is checked at the new
     notebook's open against its own (new) decision rule —
     `purpose_design.md` "How to plan the H portfolio — sub-claim
     decomposition" — not here.

   **Sub-step 1.5 (same-notebook branch only) — conjunct
   contribution gate.** Read the YES / NO / KICK-UP branches of the
   decision rule in the notebook header. Name the conjunct(s) the
   new H tests. Compare to what the parent H already addressed
   (parent's `results.parquet` row read against the same decision
   rule):
   - **The new H closes an unaddressed conjunct** (e.g. parent
     tested YES (a) on 1 instrument; the new H expands to a 2nd /
     3rd instrument toward YES (b)) → progresses the decision rule
     → eligible for step 2.
   - **The new H closes a middle-range conjunct in a way that
     tightens its CI or sharpens the threshold** — and is
     structurally different from the parent (different exit,
     different feature, different fee model) — → eligible
     (multi-testing inflation will be checked at the completion
     gate by `experiment-review`'s validation-sufficiency
     dimension).
   - **The new H closes only conjunct(s) the parent has already
     *landed*** (parent point estimate past threshold AND CI
     excluding the opposite region — definition of "landed" is in
     `purpose_design.md` "Stop the investigation as soon as the
     rule fires") → redundant. Do **not** run. The proposed H must
     be redesigned (different cross-section, different feature,
     different exit) so that its `closes_conjuncts` set covers at
     least one unaddressed or middle-range conjunct, OR it must be
     dropped and a replacement H' proposed targeting the binding
     gap.
   - **The new H closes no conjunct of the decision rule** →
     freelance work serving no consumer (per `purpose_design.md`
     "Failure patterns"). Do **not** run. Either expand the
     decision rule itself (with the expansion's justification
     recorded in `decisions.md`) and re-test 1.5, or drop the
     candidate.

   The check fires per derived H, not per Purpose. The conjunct(s)
   the H targets are the durable record (= `closes_conjuncts`
   column in `hypotheses.md`, schema below). The eligible /
   redundant / freelance verdict at sub-step 1.5, when one fires,
   is reported inline in the assistant's reply alongside the
   routing decision — the skill does not write to `decisions.md`
   for routing rejects (rejected-at-routing H's persist as a
   `planned-drop` row in `hypotheses.md` with the reject reason in
   the Statement column; the chat transcript is the audit surface).

   Sub-step 1.5 is a **gate**, not a flag. Recognising the binding
   gap and proceeding anyway is the failure pattern this gate
   exists to interrupt. Sub-step 1.5 complements but does not
   replace the closure rule "Stop as soon as the rule fires" in
   `purpose_design.md`: rule-fires closes the whole Purpose when
   YES / NO / KICK-UP unambiguously land; sub-step 1.5 evaluates
   each derived H mid-iteration and is the more granular gate.

2. (Subordinate to 1, 1.5) Run-now / next-session / drop:
   - **Run-now**: testable in the current session with current
     data / features / compute.
   - **Next-session**: requires data acquisition, new feature
     construction, or hours of compute.
   - **Drop**: refuted in prior work, out of scope, or judged not
     worth the effort.

The old rule "run-now derived hypothesis ⇒ start the next notebook"
has been **replaced**. Run-readiness no longer routes the H to a new
file; only Purpose change does.

The classification (run-now / next-session / drop) is recorded in
`hypotheses.md`'s `Status` column as `planned-runnow` /
`planned-nextsession` / `planned-drop` — single source of truth for
H-level planning state. Notebook body, `decisions.md`, and any
other derived-H listing must not duplicate the classification (=
avoid sync drift; the row is the authoritative state).

### Common rationalizations at routing (especially around sub-step 0 and 1.5)

| Excuse | Reality |
|---|---|
| "The why-why chain is documentation overhead; the H is obviously a refinement of the parent." | "Obviously a refinement" is exactly what the chain interrupts. If the H is genuinely a refinement of a *mechanism-level* finding, the chain has already been written and the citation is one phrase. If the citation cannot be produced, the H is not a mechanism-level refinement — it is a verdict-level reflex (the parent failed / succeeded → derive at the verdict layer). Sub-step 0's chain-citation gate is what catches this. |
| "The parent was supported, so we just extend to a sibling instrument; no chain needed." | The chain is required for *both* supported and rejected verdicts. A supported parent without a chain produces sibling extensions ("now try GBP / try 30 days") that propagate whatever the apparatus *actually tested*. If what it tested is mechanism-misspecified, sibling extensions multiply the misspecification. The chain catches this before the next H ships. |
| "The derived H is Pathway 4 (failure-derived) — that makes it legitimate; the cost-of-running argument says we should run a sensitivity sweep before paying for a multi-pair / multi-feature expansion." | Pathway taxonomy is *generation provenance* — it certifies *how* the H was generated, not *whether* it progresses the decision rule. Pathway 4 legitimacy is necessary but not sufficient; sub-step 0 (chain citation) and sub-step 1.5 (conjunct contribution) are the depth gates. A Pathway-4 H whose `closes_conjuncts` set is redundant with the parent adds multiple-testing inflation (worse DSR trial counts) without progress, regardless of how cheap it is to run. The cost of running a redundant H *plus* the cost of the eventually-needed multi-pair H is strictly larger than the cost of the multi-pair H alone. |
| "The unaddressed conjunct is flagged in `decisions.md` as a design-hypothesis-at-open concern; the derived H proceeds in parallel." | Sub-step 1.5 is a **gate**, not a flag. Logging the binding gap as a design-hypothesis-at-open note in `decisions.md` is parallel work, not a substitute for the gate. If the H does not progress an unaddressed or middle-range conjunct, redesign it (different cross-section, different feature, different exit) so its `closes_conjuncts` covers the binding gap, or drop it and propose H' that does. |
| "Sub-step 1.5 will rarely fire — most derived H's emerge precisely *because* the parent didn't land a conjunct." | Mostly true, and that is the eligible case. The gate's purpose is to catch the *minority* of derived H's that look natural under Pathway 4 but actually re-test a landed conjunct. Scenarios where sub-step 1.5 reliably fires: (a) parent landed YES (a) on instrument 1, derived H proposes parameter sweep on instrument 1; (b) parent landed NO_2 (`fee_model` axis) at break-even fee 0.6 bp, derived H proposes another fee variant on the same feature; (c) parent's KICK-UP precondition fired, derived H ignores the structural finding and proposes a refinement inside the same broken frame. |
| "I'll just write `closes_conjuncts = (TBD)` and figure it out when I run the H." | "TBD" is only legal for new-Purpose H's whose target notebook hasn't been opened yet (see H4 in the schema example). For same-Purpose derived H's, the decision rule is already on the page in the notebook header — the conjuncts are nameable now. Postponing the naming postpones sub-step 1.5; postponing 1.5 is exactly the failure mode the gate exists to interrupt. |
| "If sub-step 1.5 keeps rejecting my derived H's, the iteration is stuck — I'll skip 1.5 once to make progress." | Sub-step 1.5 rejecting a series of derived H's is a *signal*, not an obstruction: it says the iteration is locally exhausted under the current frame and the next move is *cross-H synthesis* (per `cross_h_synthesis.md`) — likely Pattern A (binding axis identified, close on Fallback NO) or Pattern B (Purpose too broad, split into derived Purposes). Skipping the gate to keep iterating is the sunk-cost path the gate exists to surface. |

## Updating hypotheses.md

At the end of every H round (and whenever a derived H is
generated), update `hypotheses.md`:

```markdown
| ID | Statement | Status | purpose_id (= notebook = Purpose) | target_sub_claim_id | closes_conjuncts | pathway | chain_terminal_cited | Acceptance condition | Last update |
|---|---|---|---|---|---|---|---|---|---|
| H1 | ... | supported | pur_001 (mean-reversion EUR/USD intraday) | G1.1 | YES_a, YES_b (1/3 instruments) | 2 | n/a (initial H, no parent chain) | test PSR ≥ 0.95 | 2026-04-28 |
| H2 | (Derived from H1, same Purpose; expands cross-section toward YES (b); cites H1's chain terminal "RSI selects high-vol participation, not MR specifically") ... | supported | pur_001 | G1.1 | YES_b (3/3 instruments) | 4 | H1.chain.terminal-A: "RSI selects high-vol participation" | walk-forward positive-rate ≥ 0.60 on 3 EUR pairs | 2026-04-28 |
| H3 | (Derived from H2, same Purpose; cites H2's chain terminal "fee burden concentrates in shortest-holding tercile") ... | rejected | pur_001 | G1.2 | YES_c (Pattern A guard, fee axis) | 4 | H2.chain.terminal-B: "fee burden in shortest-holding tercile" | break-even fee ≥ 1.5 bp/side | 2026-04-28 |
| H4 | (Derived from H1, NEW Purpose) ... | planned-runnow | pur_002 (momentum EUR/USD intraday) | G1.3 | (per pur_002 decision rule — TBD at notebook open) | 5 | H1.chain.terminal-C: "asymmetric exit converts long-vol to PnL" | ... | 2026-04-28 |
| H5 | ... | planned-drop | n/a | n/a | n/a | n/a | n/a | n/a | 2026-04-28 |
| H6 | (Derived from H1, same Purpose; **rejected at routing 0: chain_terminal_cited = none — proposed without citing H1's chain**. Superseded by H7 grounded in H1.chain.terminal-A.) | planned-drop | pur_001 | G1.1 | YES_a | 4 | none — rejected at admissibility | n/a — rejected at routing | 2026-04-28 |
| H7 | (Derived from H1, same Purpose; cites H1.chain.terminal-A; expands cross-section to land unaddressed YES_b — supersedes routing-rejected H6.) | planned-runnow | pur_001 | G1.1 | YES_b (3/3 instruments target) | 4 | H1.chain.terminal-A: "RSI selects high-vol participation" | walk-forward positive-rate ≥ 0.60 on 3 EUR pairs | 2026-04-28 |
```

Each H row points to the `purpose_id` (= notebook = Purpose) it
lives under. Multiple H's per Purpose share the same `purpose_id`.
The H6 row above shows an admissibility-stage rejection (sub-step
0 of the routing rule fired): the row exists as the planning
artifact's record of "this candidate was considered and rejected",
not as a notebook entry — no `## H6` block is created in the
notebook because H6 never ran.

Five columns are load-bearing for the iteration / research-goal
layers (`references/research_goal_layer.md`):

- **`Status`** carries the planning state (`planned-runnow` /
  `planned-nextsession` / `planned-drop`) for derived H's that have
  not yet run. This is the single source of truth for run-now /
  next-session / drop classification. The notebook body and
  `decisions.md` do not duplicate this.
- **`target_sub_claim_id`** anchors the H in the project's
  research-goal sub-claim list (project README). A derived H
  inherits its parent's value by default; an override is recorded
  in the Statement column with a one-phrase reason (see H3 in the
  example above).
- **`closes_conjuncts`** anchors the H in the **decision rule
  layer** (= the notebook's decision rule). It enumerates the
  YES / NO / KICK-UP conjuncts the H tests, optionally annotated
  with structural progress (e.g. `YES_b (3/3 instruments)`). The
  routing rule's sub-step 1.5 reads this against the parent H's
  `closes_conjuncts` and the parent's `results.parquet` row to
  decide whether the new H progresses the decision rule or is
  redundant. Without this column, derived H's are enumerated
  bookkeeping-style with no link to what the Purpose is trying to
  close. For new-Purpose H's (a different `purpose_id`), the
  column references the new notebook's decision rule and is
  finalized when that notebook opens; mark "TBD at notebook open"
  in the meantime (see H4 in the example).
- **`pathway`** declares the H's generation provenance (1-6 from
  `hypothesis_generation.md`, or `ad-hoc`). Derived H's typically
  have `pathway = 4` (failure-derived) but may be 5 (cross-asset)
  or 6 (mechanism-driven) depending on the mechanism that
  motivated them.
- **`chain_terminal_cited`** records which terminal answer of the
  parent H's why-why chain the derived H is grounded in (e.g.
  `H1.chain.terminal-A: "RSI selects high-vol participation"`). Use
  `n/a` for initial H's that have no parent chain. Use `none —
  rejected at admissibility` for H's that proposed without a
  chain citation and were rejected at sub-step 0. Without this
  column, the depth gate is not auditable across the project — the
  chain is a notebook-internal artifact and the cross-notebook
  link to "which chain terminal does this derivation address?"
  needs an explicit pointer.

`closes_conjuncts`, `pathway`, and `chain_terminal_cited` are
orthogonal: `pathway` certifies *how* the H was generated (Pathway
4 legitimacy = generation provenance is failure-derived),
`closes_conjuncts` certifies *what decision-rule work* the H does,
`chain_terminal_cited` certifies *what mechanism-level reading the
H is grounded in*. A Pathway-4 H whose `closes_conjuncts` is
redundant with the parent fails sub-step 1.5 even though Pathway 4
is otherwise valid. A Pathway-4 H with no `chain_terminal_cited`
fails sub-step 0 even when `closes_conjuncts` is novel — generation
legitimacy and conjunct-contribution legitimacy are necessary but
not sufficient; mechanism-level grounding is the third necessary
condition.

## Updating decisions.md

Append a time-ordered entry per Purpose. A Purpose with multiple
H's yields one entry with H sub-bullets. The Purpose entry also
carries the research-goal layer's bookkeeping (design hypothesis at
open, sub-claim progress update at close, design hypothesis at
close — see `references/research_goal_layer.md`):

```markdown
## YYYY-MM-DD pur_<NNN>_<purpose-slug> — Purpose: <one-line>

- Design hypothesis at open: [the prediction made BEFORE the
  Purpose's investigation ran — which research-goal sub-claim(s)
  this Purpose is expected to advance, and in what direction]
- Tested H1 (target_sub_claim_id = G1.<X>): [one-line restatement]
  - Observation: [observed values, anomalies]
  - Verdict: [supported / rejected / partially supported / parked]
  - Why-why chain terminal: [one-phrase summary of the chain's
    terminal answer; full chain lives in the notebook's H1
    interpretation cell]
  - Robustness battery (this H): [pass / fail per item]
- Tested H2 (derived from H1, target_sub_claim_id = G1.<X>
  inherited; cites H1.chain.terminal-<X>): …
- Tested H3 (derived from H2, target_sub_claim_id = G1.<Y>
  overridden — reason; cites H2.chain.terminal-<Y>): …
- Purpose-level synthesis: [one or two sentences across H1…HN;
  Pattern (A-E) match per `cross_h_synthesis.md`; primary closure
  form (Primary YES / Fallback NO with binding axis / KICK-UP)]
- Research-goal sub-claim progress update: [transition for each
  sub-claim this Purpose touched; sub-claims not touched are still
  listed as unchanged so the project's running state is fully
  visible]
  - G1.1: in progress → confirmed
  - G1.2: not started → not started
  - G1.3: not started → not started
- Design hypothesis at close: [verification of the at-open
  prediction — CONFIRMED / FALSIFIED / PARTIAL with one-phrase
  reason]
- Derived Purposes for the next notebook:
  - P<id> (target_sub_claim_id = G1.<X>): …
  - P<id> (target_sub_claim_id = G1.<Y>): …
- Direction rejected: [what was tried inside this Purpose and did
  not work, with reason]
```

Note: derived *Hypotheses* (= future H rounds) are NOT listed in
`decisions.md`. They live as rows in `hypotheses.md` with the
appropriate `Status` (`planned-runnow` / `planned-nextsession` /
`planned-drop`). Single source of truth for H-level planning state.

## Run-now vs. next-session classification

| Run-now | Next-session |
|---|---|
| Testable with current data | Requires new data acquisition |
| Existing features suffice | Requires new feature construction |
| Runs in under ~30 minutes | Needs hours of compute |
| Upstream notebooks complete | Upstream is still in planning |

This classification is orthogonal to the same-notebook-vs-new-notebook
decision. A run-now H whose Purpose is unchanged is the next round
inside the current notebook *now*. A run-now H whose Purpose has
changed opens the next notebook *now*.

`planned-drop` covers four sub-categories that share the "this
candidate H will not run" outcome: (a) **out-of-scope drop**
(refuted in prior work, not worth the effort, judged outside the
project scope); (b) **rejected-at-admissibility** (sub-step 0 of
the routing rule fired — the candidate proposed without a why-why
chain citation, or with a chain that does not reach mechanism
level); (c) **rejected-at-routing** (sub-step 1.5 of the routing
rule fired redundant or freelance — the candidate cannot progress
the decision rule as designed); (d) **superseded** (replaced by a
redesigned H' that targets the binding gap or grounds in the
chain). For audit, the Statement column's leading clause identifies
which sub-category fired (e.g., "rejected at admissibility 0:
no chain citation", "rejected at routing 1.5: …", "superseded by
H<id>′: …"). Cross-H synthesis at Purpose closure distinguishes the
sub-categories when reading the dropped-H rows.

## Notebook-body H-id numbering

H-ids are **global and sequential across the project's
`hypotheses.md`**: the H-id assigned to an H is its row position in
`hypotheses.md`, in order of consideration. Rules:

- Every H **considered** — whether it ran, was dropped out-of-scope,
  was rejected at admissibility 0, was rejected at routing 1.5, or
  was superseded — gets the next sequential H-id at the moment of
  consideration. The id is permanent; subsequent renumbering is
  forbidden.
- Every H that **actually runs** gets one `## H<id>` block in its
  notebook, numbered with its `hypotheses.md` row id verbatim (so
  `## H7` in the notebook ↔ row H7 in `hypotheses.md`).
- H's that **did not run** (rejected-at-admissibility,
  rejected-at-routing, out-of-scope drop, superseded) get no `##
  H<id>` block in the notebook. Their `hypotheses.md` row is the
  only artifact about them.

Consequence: notebook H-ids may have gaps (e.g., `## H1`, `## H2`,
`## H3`, `## H7` is legal — H4 went to a different notebook, H5
was dropped, H6 was rejected at admissibility). Gaps are not a
defect; they are the audit trail of which candidates were
considered but did not produce a notebook block. Renumbering the
notebook to close gaps would erase the audit trail and is forbidden.

This rule applies uniformly whether `hypotheses.md` is project-global
or per-notebook in the project's convention; the load-bearing
invariant is "every notebook `## H<id>` matches the row of the same
id in `hypotheses.md`, and every row without a corresponding `##
H<id>` in any notebook is a non-running candidate".

## Exhaustion criteria — the emergency-stop rule

This section defines the **emergency stops** — the triggers that
force the researcher to stop generating H's and look at the cluster
*when the primary stops (above) have not fired*. Patterns A-E in
`cross_h_synthesis.md` define the *action* for each cluster shape;
this section defines the *trigger* that forces the researcher to
invoke them.

Primary stops (Primary YES / Fallback NO with binding axis /
KICK-UP, see the section above) are the intended way a Purpose
ends. The emergency stops below exist because Purposes can fail to
land any of those — typically when the decision rule was set with
thresholds the H portfolio cannot reach, when the Purpose is too
broad, or when a structural KICK-UP has not yet been recognized as
one. Without an explicit trigger, researchers mid-iteration on a
Purpose keep generating H's and the iteration runs unbounded.

### Hard trigger (mandatory)

A Purpose has accumulated **5 H tested without any
`verdict='supported'`** → the next action is **not** H6. The next
action is the cross-H synthesis per `cross_h_synthesis.md`. No new
H may be appended to this Purpose until the synthesis has produced
a Pattern match (A-E or combined) and the corresponding action has
been recorded in `decisions.md`.

The 5-H count is over the Purpose, not the project. It includes
any mix of `verdict ∈ {rejected, parked, preliminary}`. A single
truly-supported H (all four completion gates pass — see SKILL.md
"Completion gate per Hypothesis") resets the trigger; the Purpose
has produced a working result and further H's are exploring the
result's scope, not searching for one.

### Soft trigger (advisory)

The hard trigger fires at N=5. Earlier soft triggers are
advisory — the researcher can ignore them without violating the
protocol, but the protocol surfaces them so iteration is not blind:

- **N=3 advisory**: First synthesis check. If a pattern is already
  visible at N=3 (e.g., all three rejections share the same
  `failure_mode` → Pattern A), close or derive without waiting for
  N=5.
- **Pattern-C-shape advisory**: As soon as a Pareto trajectory is
  visible in the metric shape (one metric improving, another
  worsening, regardless of verdict count), trigger synthesis.
  Pattern C's mechanism is metric-shape-driven, not count-driven.

### Default-to-Pattern-B rule

If the synthesis at N=5 matches *no* clear pattern (mixed signals,
no shared `failure_mode`, no Pareto trajectory, no monotonic
improvement), the **default is Pattern B** (Purpose is too broad,
split into derived Purposes).

The reason: a Purpose that has produced 5 unconnected rejections is
empirically a Purpose whose H's are testing different things. The
researcher's intuition that a 6th H "might fit" is exactly the
sunk-cost rationalization the trigger exists to interrupt.

Default-to-B is overridable: the researcher can argue against the
default in `decisions.md` if they have a specific Pattern-A
mechanism that didn't surface in the cluster yet. But the *default*
is split, not continue.

### Hard cap (escape valve)

Beyond **N=8 H tested under one Purpose** without
`verdict='supported'`, no H_{N+1} is appendable to this Purpose.
The Purpose closes mechanically. If the researcher believes more
work is warranted, it is opened as a new Purpose (new notebook,
new `purpose_id`) carrying the previous Purpose's synthesis as
documented prior.

The hard cap is statistical, not punitive: beyond 8 H, the
multiple-testing inflation makes any subsequent `supported`
verdict's DSR honest-trial-count too punishing to clear cleanly.
Continued iteration is busywork.

### What resets the trigger

Only a **truly supported** H resets the trigger — i.e., one for
which all four completion gates pass (`bug_review`,
`experiment-review`, `research_quality_checklist`, achieved_tier ≥
Medium). A provisional `verdict='supported'` written at append-time
but downgraded to `partial` or `preliminary` after review **does
not** reset.

This robustness matters: the trigger cannot be escaped by writing
`verdict='supported'` on a shaky H. The reset is gated on the same
four-gate machinery that gates real publication-grade verdicts.

### Common rationalizations

| Excuse | Reality |
|---|---|
| "I'm at N=5 but I have a really good idea for H6" | The trigger doesn't ask whether your H6 idea is good. It asks you to look at H1-H5 first. Run synthesis; if Pattern A emerges and your H6 is a Pathway-4 derivation against the binding axis, H6 is legal. If Pattern B emerges, H6 belongs in a derived Purpose, not this one. |
| "The synthesis is overhead; let me just append H6 and synthesize later" | "Later" historically does not happen. The trigger fires *before* H6 specifically because the synthesis is what determines whether H6 is the right next step. |
| "I'll mark H4 as supported provisionally to reset the trigger" | Reset requires four-gate-clean. A provisional supported that hasn't passed both review layers does not count. |
| "N=5 is arbitrary; I'll override it" | Yes, 5 is arbitrary; any cutoff is. The override is legal but documented in `decisions.md` with a Pattern-A mechanism argument. Overriding without that argument is sunk-cost. |
| "I'm at N=8, the cap is unfair, let me do H9" | Cap is mechanical. Open a new Purpose; the work continues but with fresh DSR trial count and the previous synthesis as inheritance. |

## Completion criteria

A research project counts as complete when all of these hold:

- (a) Every Purpose's investigation has landed on a **primary stop**
  — Primary YES, Fallback NO with binding axis, or KICK-UP (see
  "Why iteration exists" above and `purpose_design.md`). A Purpose
  closed only by emergency stop (N=5 advisory or N=8 hard cap)
  without an articulated primary-stop outcome is preliminary
  screening, not completion. The primary-stop outcome is recorded in
  `decisions.md` per Purpose.
- (b) The seven items in `robustness_battery.md` pass for every H
  whose verdict is `supported` (= every H supplying evidence for a
  Primary YES).
- (c) Every H whose verdict has been declared has a why-why chain
  written into the notebook body per `why_why_analysis.md`,
  regardless of verdict value.
- (d) Every candidate H is classified (executed / next-session /
  dropped).
- (e) Every candidate Purpose is classified (executed-as-its-own-
  notebook / next-session / dropped).
- (f) `hypotheses.md` has no entries left in an "untriaged" state.
- (g) `decisions.md` provides a traceable history across all
  Purposes, with H sub-bullets under each Purpose and the
  primary-stop outcome named.

If any is missing, the work is preliminary screening.

## Failure patterns

- "Next hypothesis" listed as TODO with no further round → iteration
  stopped; if it can run now and the Purpose is unchanged, run it
  as the next H block in the same notebook.
- "Next H needs a new notebook because the Purpose feels different"
  stated but the Purpose statement was never re-read → re-read the
  Purpose statement before splitting; many "feels different" cases
  are sensitivities or refinements.
- Conclusion declared after one supporting H → reverse-test against
  contradictory variants in the same notebook.
- "Diminishing returns" claimed without verification → check the
  robustness-battery status (per H) before stopping.
- Derived H proposed without a `chain_terminal_cited` entry from
  the parent's why-why chain → admissibility-stage reject; sub-step
  0 fires. Either run the parent's why-why chain (per
  `why_why_analysis.md`) and re-propose with citation, or drop the
  candidate.
- Derived H proposed without a `closes_conjuncts` value naming a
  conjunct of the decision rule → freelance work serving no
  consumer; sub-step 1.5 fires reject-at-routing. Either fill
  `closes_conjuncts` from the decision rule's YES / NO / KICK-UP
  branches, or expand the decision rule (with justification
  recorded in `decisions.md`) and re-test 1.5, or drop the
  candidate.
- Derived H is a sensitivity / parameter-sweep variant of the
  parent H on the **same instrument / same feature / same fee
  model** while a multi-instrument / cross-section conjunct of the
  decision rule's YES branch remains unaddressed →
  conjunct-redundancy reject; sub-step 1.5 fires. Redesign the H
  so its `closes_conjuncts` covers the binding gap, or drop and
  propose H' that does.

## H-round count guidance

| H rounds across all notebooks | Assessment |
|---|---|
| 1 | Single hypothesis, not research |
| 2-3 | Initial screening |
| 5-8 | Standard research |
| 10+ | Substantial body of work, approaching publication grade |

A "round" here is one Hypothesis. Multiple rounds inside one
notebook all count. Quality of derived-hypothesis generation —
specifically, whether each derivation is grounded in a
mechanism-level chain — matters more than raw count.
