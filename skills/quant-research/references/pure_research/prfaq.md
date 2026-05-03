# prfaq.md

Amazon "Working Backwards" PR/FAQ — the entry document for any Pure
Research project. Write the press release for the finding you would
publish if research succeeded, then anticipate the skeptical reviewer's
questions.

## When to read

- The very first step of any Pure Research project, before literature
  search, pre-registration, or trial design
- When a Pure Research project's question feels unfocused
- Before pivoting from R&D into Pure Research mode

## Purpose

The PR/FAQ forces the question to be **scoped before the search**. Without
a press release and the questions a skeptical reviewer would ask, the
literature search drifts, the pre-registration is premature, and the
trial design has no anchor.

The acid test: **if you cannot write a coherent PR/FAQ, the question is
not ready**. This is not a failure — it is a signal to refine the
question before investing in trials.

The PR/FAQ is a **frozen artifact** — once committed, it can be amended
only with a dated deviation entry in `decisions.md`. Hash-lock via
`scripts/prereg_freeze.py` (same mechanism as charter and
pre-registration).

## Two parts

### Part 1: Press Release (1 page maximum)

Imagine the finding has been completed and you are publishing it. Write
the press release as if announcing to a quantitative-finance audience.
The format:

```markdown
**[Date] — [Headline that states the finding in 1 sentence]**

[Lead paragraph: what was found, in concrete terms. State the phenomenon,
the mechanism, and the scope conditions.]

[Supporting paragraph: the discriminating evidence — what alternative
explanations were ruled out, and how. Cite the type of evidence
(numerical / structural / null-result).]

[Implications paragraph: what changes downstream of this finding —
practitioners, theory, future research. Be honest about scope.]

[Closing: what was NOT shown — the limits of the finding, what next.]
```

Length: 200-400 words. **One page**, hard limit.

### Part 2: FAQ (skeptical questions)

Anticipate the questions a critical reviewer would ask. The FAQ is where
honesty about limitations and scope becomes structural. Typical
question categories:

- **Statistical sufficiency**: How was multiple testing handled? What is
  the t-statistic / p-value adjusted for the trial count? (Harvey-Liu-Zhu
  recommends t > 3.0 for new financial factors.)
- **Robustness**: What happens in different regimes / sub-periods /
  sub-universes?
- **Mechanism**: Why does this mechanism produce this effect? Walk
  through the causal chain.
- **Alternatives**: What competing explanations were considered? What
  evidence weakened them?
- **Replication**: Does this hold on independent data sources?
- **Scope**: Where does this NOT apply? Be explicit.
- **Practical implication**: If a practitioner used this, what would they
  do differently? At what cost?
- **HARKing risk**: Was the analysis pre-registered before data was
  inspected? Show the pre-reg hash.

10-20 FAQ entries is typical. Each gets a 1-3 sentence answer.

## Good vs bad PR/FAQ

### Bad PR

> "We trained a transformer model on intraday futures data and found it
> predicts returns with high accuracy. The methodology is novel and
> applicable broadly."

Problems: no concrete finding, no scope, no mechanism, no alternatives
ruled out. This is an ML demo, not a research finding.

### Good PR

> **[2026-XX-XX] Volatility carry alpha in US listed VIX products
> declined 80% in 2020-2024 vs 2010-2019 due to retail vol-selling
> crowding, not regime change.**
>
> Sharpe ratio for short-vol carry strategies on VIX-linked ETFs and
> futures dropped from 1.8 (2010-2019) to 0.4 (2020-2024). Bootstrap
> 95% CI on the difference is [-1.65, -1.05], p < 0.01 after Bonferroni
> correction across 3 sub-strategies.
>
> CFTC Commitments of Traders data shows non-commercial vol-seller
> positioning grew 4× over 2020-2024. The vol-of-vol stability test
> (rolling 60-day vol-of-vol unchanged across periods) weakens the
> alternative explanation that volatility-regime structure changed
> fundamentally.
>
> Two sub-universes (S&P-linked vs Russell-linked vol products) confirm
> the pattern with directionally consistent decay magnitudes (-78% and
> -82% respectively).
>
> The finding suggests vol-carry strategies should not be sized
> identically to historical sharpe; capacity is materially compressed.
> The finding does NOT establish whether the crowding will persist or
> reverse, nor does it apply to non-listed OTC vol products.

Why this is good: concrete metric, scope precise, alternative ruled out
with evidence type, replicated, limits stated explicitly.

### Bad FAQ

> **Q: Is this just data mining?**
> A: We don't think so.

Problem: hand-wave. Reviewer will press; this is a thin defense.

### Good FAQ

> **Q: Is this just data mining? How many strategies were tested before
> selecting this one?**
> A: This was a single pre-registered hypothesis, not a search. The
> pre-registration (hash b9d2..., frozen 2026-01-15, 5 weeks before
> trial) specified the test as "rolling 3-year Sharpe with bootstrap
> CI on short-vol carry returns", with 3 competing explanations
> (regime change, crowding, null). No alternative test designs were
> tried. The Bonferroni correction across the 3 sub-strategies
> (S&P-linked, Russell-linked, VIX-linked) gives p < 0.01.

## How the PR/FAQ blocks downstream work

Without a frozen PR/FAQ:

- **Literature search is unfocused**. You don't know what to search
  for; you'd browse "vol carry" generally instead of "vol carry +
  crowding hypothesis + 2020s structural change".
- **Pre-registration is premature**. You don't know what competing
  explanations to enumerate, what test to design, or what to predict
  under each explanation.
- **The promotion gate has no anchor**. The "discriminating test against
  ≥1 serious alternative passed" requirement is meaningless if the
  alternatives weren't named upfront.
- **HARKing risk is high**. Without a frozen PR/FAQ, finding-driven
  rationalization is undetectable.

If the user pushes to "skip PR/FAQ and just look at the data", the
response is: looking at the data first is a shopping trip. Once you
have seen the data, the PR/FAQ you produce is an artifact of the data
you saw, not of the question you wanted to answer.

### Orientation search is allowed

Writing the PR/FAQ requires naming **mechanisms** and **alternatives**
upfront. For a researcher unfamiliar with the domain, this can create a
bootstrap problem: how do you name plausible mechanisms without first
reading the relevant literature?

**Light orientation search is allowed and expected** before PR/FAQ:

- Read 3-5 review papers / canonical references on the phenomenon
  (typically 30-60 minutes of reading)
- Browse abstracts to surface candidate mechanisms and known
  alternatives
- Note: this is **not** the targeted literature search of step 2
  (which happens after PR/FAQ scoping); it is prior-knowledge
  bootstrapping

The prohibition that remains in force during orientation search:

- **No data inspection** (no plot of the actual returns / regimes /
  metrics being studied)
- **No trial execution** (no model fits, no backtests, no metric
  computed on real data)

The line: orientation search recalls **prior knowledge**; data
inspection produces **new knowledge** that would shape the PR/FAQ
post-hoc.

If you find yourself unable to write a coherent PR/FAQ even after
orientation search, that is itself a signal — the question may not be
ready, or the domain expertise required is missing.

## Freezing the PR/FAQ

After Part 1 and Part 2 are complete and reviewed:

```bash
python scripts/prereg_freeze.py --type prfaq --path prfaq.md
```

This:
1. Computes SHA-256 of the file content
2. Writes `prereg/prfaq.lock` with hash + UTC timestamp + path
3. Records the freeze in `decisions.md` as a state transition

After freezing, **`prfaq.md` cannot be edited in place**. Any change
requires a dated deviation entry in `decisions.md`. Frequent deviations
to PR/FAQ are a sign the question was not ready when frozen — next
project, spend more time on this step.

## Common failure modes

| Failure | Symptom | Fix |
|---|---|---|
| PR has no concrete finding | "We will study vol carry decay" (intent, not finding) | Re-write as if research succeeded; the PR is the post-success announcement |
| FAQ is shallow | 3-5 surface questions | Imagine a senior reviewer; what 15 questions would they ask? |
| Mechanism unstated | "Sharpe declined" without explanation | Mechanism is part of the finding; if you can't state one, the question is not ready |
| Scope unstated | Universal claim ("vol carry doesn't work") | Scope must be precise (US listed VIX, monthly, 2020-2024) |
| HARKing-vulnerable PR | Question phrased to fit known data ("we found that 2020-2024 differs from 2010-2019") | Re-frame ex ante: was this prediction made before looking at the data? If not, the PR is post-hoc |

## Relationship to other references

- After PR/FAQ is frozen → read `references/shared/literature_review.md`
  for targeted literature search (now scoped by the PR/FAQ).
- Then `references/pure_research/preregistration.md` for the formal
  pre-analysis plan (PAP), which formalizes the test design.
- Then `references/pure_research/explanation_ledger_schema.md` for the
  state object that tracks question / explanation pruning.
- The PR/FAQ feeds directly into `references/pure_research/imrad_draft.md`
  — the IMRAD draft's Discussion section answers the FAQ as a starting
  point.
- See `references/pure_research/pr_promotion_gate.md` for the
  pre-promotion checklist; the PR/FAQ being on file is a hard
  pre-condition.
