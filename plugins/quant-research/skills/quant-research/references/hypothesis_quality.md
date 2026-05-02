# hypothesis_quality.md

Hypothesis quality management keeps the research state small and useful.
It is not a paperwork system.

## Four gates

### 1. Entry gate

Before adding or running a hypothesis, answer:

- Which active research question, explanation, or R&D capability does this update?
- Is this a duplicate, parameter variation, or weaker wording of an existing row?
- What row will be updated if this test succeeds?
- What row will be updated if this test fails?

If no row changes under failure, do not run it.

### 2. Design gate

Write:

- Success distinguishes: ...
- Failure distinguishes: ...
- Cannot distinguish: ...
- Minimum evidence needed: ...
- Stop condition: ...

Success criteria alone are insufficient. A test whose failure teaches nothing is
not a research test.

### 3. Interpretation gate

After the result:

- State the observation first.
- State what cannot be concluded.
- Compare competing explanations.
- Mark which explanations became weaker.
- Avoid terminal generic labels.

Read `failure_analysis.md` for any miss or ambiguity.

### 4. State update gate

Update ledgers before proposing more work:

- `active`: still live and worth discriminating
- `resolved`: answered or capability exit criteria fired
- `rejected`: contradicted or no longer tenable
- `merged`: duplicate or variant absorbed into another row
- `stale`: made irrelevant by later evidence or scope change
- `parked`: intentionally deferred with a named unblock condition

New rows are allowed only after pruning existing rows.

## Heavy review trigger

Run full bug-review / robustness / experiment-review only when:

- promoting a claim to `supported`
- using a result for deployment, allocation, or production build decisions
- sharing externally or drafting paper-like claims
- closing a research line or making a major direction change
- a numeric red flag suggests the result may be too good or contaminated

Good headline metrics are never sufficient for promotion. Metrics can make a
claim eligible for promotion review, but they do not themselves establish
`supported`. Missing competing explanations, missing serious alternatives, or
missing promotion gates block `supported` even when Sharpe, walk-forward, and
fee sensitivity look favorable.

Routine exploratory trials use the four gates above. Over-reviewing every
trial creates a false sense of rigor while letting bad state accumulate.

## Anti-accumulation rules

- Do not keep rejected hypotheses "for later" unless a concrete unblock
  condition exists.
- Do not create H2 when H1 should become a robustness sweep, merged variant, or
  stale row.
- Do not create a new hypothesis by relaxing a failed threshold, lowering fees,
  narrowing to a favorable regime, or changing a parameter after seeing the
  result. First decide whether the change is a robustness sweep, a merged
  variant, a stale row, or a genuinely new research question with an entry-gate
  answer under both success and failure.
- If the proposed hypothesis differs only by a parameter value from an active
  or retired hypothesis, the default action is `merged`, not `planned`. A new
  row requires naming the distinct research-state row that success and failure
  would update.
- In R&D mode, a large benchmark or backtest is not a hypothesis entry gate by
  itself. It must name the specific capability row it updates. If success would
  tempt promotion of the whole technology while failure would only lead to
  parameter / model swapping, the test is too broad and must be decomposed.
- Do not write decisions that merely narrate activity. `decisions.md` records
  durable state transitions and commitments.
- Do not let `hypotheses.md` become a wish list. It is a queue of tests that
  passed the entry gate.
