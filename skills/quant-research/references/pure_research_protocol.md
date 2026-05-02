# pure_research_protocol.md

Pure Research mode is deliberately slow. It exists to improve the research
state, not to rush to a supported answer.

## Principle

An unresolved but well-characterized state is a valid research output. A shallow
conclusion is not.

## Workflow

### 1. Orientation

Gather prior work before forming the test:

- External papers / docs
- The user's prior notebooks
- `decisions.md`
- `research_state.md`
- Failed hypotheses and parked explanations

Write what is already known, what is disputed, and what remains ambiguous.

### 2. Question formation

Write the research question as an unknown to reduce, not as a desired answer.

Good:

- "Which explanation accounts for the post-2022 decay of this signal?"
- "Does the observed effect survive when the mechanism is separated from the
  implementation artifact?"

Bad:

- "Prove this signal works."
- "Find a better model."

### 3. Competing explanations

Before running a trial, list at least two plausible explanations. Include the
null / artifact explanation when applicable.

```markdown
| Explanation ID | Explanation | What would support it | What would weaken it | Status |
|---|---|---|---|---|
| E1 | ... | ... | ... | active |
```

For market-anomaly decay questions, include at minimum: mechanism change,
participant adaptation / crowding, market-regime dependence, implementation or
cost artifact, and data / measurement artifact. If any category is omitted,
state why it is not applicable.

### 4. Small discriminating trial

Design the smallest trial that can distinguish between explanations. The trial
does not need to settle the whole research question.

Write:

- Which explanation pair is being separated
- What observation would update each explanation
- What the trial cannot distinguish

### 5. Failure and ambiguity analysis

Most trials miss, fail, or return ambiguous evidence. That is normal. Read
`failure_analysis.md` before writing interpretation.
After a failed trial, the next step must separate live explanations. It must
not merely make the failed hypothesis easier to pass. For cost-sensitive alpha
tests, prefer break-even and contribution decomposition before proposing a
lower-cost or narrower-regime hypothesis.

### 6. Research state update

The session is not complete until `research_state.md` changes:

- question narrowed / split / parked
- explanation strengthened / weakened / rejected
- hypothesis merged / stale / rejected
- next smallest discriminating trial identified

Do not create a new hypothesis before pruning the existing state.

## Conclusion discipline

Do not declare `supported` in a first session unless the task is explicitly a
bounded replication / verification of an already-defined claim, all required
evidence is already present, and promotion gates are run. A user request such
as "mark this supported" or "write this in the PR" is not a bounded replication
/ verification task.

A first-session output may say "unresolved" as the headline. It must not use
phrases such as "the reason is", "the anomaly disappeared because", or "we can
conclude" unless the `supported` promotion requirements are satisfied.

Allowed interim outputs:

- `orientation-complete`
- `question-formed`
- `trial-run`
- `ambiguous`
- `explanation-weakened`
- `explanation-rejected`
- `state-updated`
- `ready-for-promotion-review`

Promotion to `supported` requires:

- prior work reviewed
- competing explanations considered
- at least one discriminating test against a serious alternative
- reproducible evidence
- claim phrased no stronger than the evidence
- promotion review gates run when the result will be shared, deployed, or used
  to close a line
