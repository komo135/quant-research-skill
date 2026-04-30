# bug_review.md

Multi-agent bug-review layer. Run *before* the robustness battery and *before* setting any
`verdict = "supported"`.

## When to read

- Any one of the **trigger conditions** below has fired
- About to run the robustness battery (running the battery on a buggy PnL wastes compute
  and produces credible-looking false positives)
- About to declare `verdict = "supported"` for any experiment
- After any change to the data pipeline, target definition, signal alignment, feature
  scaling / normalization, fold definition, or fee model

## Why this layer exists

A passing robustness battery is *necessary but not sufficient*. Robustness checks measure
overfitting and regime stability — not implementation correctness. A look-ahead leak, a
misaligned `shift`, a whole-period normalization, or a wrong sign convention will pass
every robustness gate, because the leak is present in every walk-forward window and every
bootstrap resample. Robustness checks operate on the PnL series; if the PnL series itself
is contaminated, all gates inherit the contamination.

A single linear self-review is also insufficient at notebook length. Long notebooks
exceed reliable single-pass attention. Distinct specialist reviewers in parallel, each
with a narrow scope, catch substantively different things than one pass trying to cover
everything. Narrowness is the point.

## Trigger conditions (any one fires the layer)

### Numeric red flags ("too good to be true")

These thresholds are aggressive on purpose — they fire on results that, *if real*, would
already be world-class. The point is to pause and verify, not to decide.

| Flag | Threshold |
|---|---|
| Test Sharpe (after costs) | > 3 |
| Walk-forward mean Sharpe | > 2 |
| Information Coefficient (Spearman) on financial returns | > 0.10 |
| ML AUC on a return-sign target | > 0.65 |
| Per-trade win rate | > 65 % |
| Max drawdown / annualized vol | < 0.5 (suspiciously smooth equity) |
| Bootstrap 95 % CI lower bound | > 1.5 (unusually tight CI is also a flag) |
| Test metric outside the bootstrap 95 % CI | any direction |
| Headline Sharpe ≥ 2 × walk-forward mean Sharpe | any |

### State-change triggers (run regardless of metrics)

- Before `verdict = "supported"` is set
- Before the test set is touched the only time
- After any change to: data ingestion, target, embargo, fold definition, feature
  scaling / normalization, signal alignment, fee model
- After a feature notebook is rebuilt and downstream notebooks are re-run
- After collapsing or re-deriving a multi-instrument panel

### Recommended (not strict)

- At the end of every research cycle, even when no flag has fired

## Reviewer roster (5 specialists + 1 adversarial, dispatched in parallel)

Each reviewer is a sub-agent invoked via the assistant's sub-agent tool. The five
specialist scopes are deliberately narrow. Do not collapse them — narrowness is what
makes parallel review catch what single-pass review misses. The sixth reviewer
(`adversarial-reviewer`) intentionally runs with a *different* (minimum) context bundle —
that asymmetry is what makes it catch what same-context review of the same model misses.

Each specialist receives only its own dimension scope and the artifacts
named in the **per-reviewer input contract** below — not whole-file
`bug_review.md` and not whole-file `sanity_checks.md`. Pre-extraction is
the parent assistant's pre-dispatch step, not the reviewer's
attention-budget exercise. The dimension scope is identified by section
anchor (`### N. <reviewer-name>`) and pulled inline.

The sixth reviewer (`adversarial-reviewer`) receives a *different* bundle — see its
section below and the input contract.

### 1. leakage-reviewer

Scope: look-ahead bias, target leakage, future-information contamination.

- Walk every feature definition. For each: does it use only data with `time ≤ t`?
- Whole-period normalization, target encoding, scaler-fit-on-all-data, whole-period
  imputation, whole-period quantile thresholds
- HMM / Kalman: smoothing (uses future) vs. filtering (causal) — which is used?
- `shift(-k)` on signals or features (target-only `shift(-k)` is OK)
- Cross-sectional ranks / standardizations: computed within each date only?
- PCA / factor decomposition: rolling vs. whole-period covariance
- Programmatic check: run `scripts/leakage_check.py::lookahead_check`

### 2. pnl-accounting-reviewer

Scope: position-to-return alignment, sign conventions, fee accounting, currency, turnover.

- Verify `pnl[t] = position[t-1] * ret[t]` (or the explicit alternative the notebook
  documents) — and verify the notebook documents the convention
- Same-bar `signal[t] * ret[t→t+1]` requires MOC fills; demand explicit justification or
  reject
- Cost: `position.diff().abs() * fee` is only valid when `position` is per-symbol; on a
  flattened multi-instrument frame it generates fake trades at ticker boundaries
- Fee monotonicity: increasing fee must monotonically reduce PnL
- Sign-flip identity: reversing all signals should mirror PnL minus 2× costs
- Programmatic checks: `scripts/sanity_checks.py::pnl_reconciliation`,
  `cost_monotonicity`, `sign_flip_test`

### 3. validation-reviewer

Scope: split correctness, embargo, test-set discipline, walk-forward purging.

- Train < val < test ordering by time, no overlap
- Embargo size ≥ target horizon
- Purged k-fold or CPCV used where overlap exists
- Test set touched exactly once — verify by counting code paths that read the test
  partition
- Walk-forward windows do not leak across boundaries (refit per window; no global
  statistic carried across windows)
- The robustness battery runs on val / CPCV, NOT on the test set (a common silent leak)

### 4. statistics-reviewer

Scope: metric correctness, trial counting, regime claims, internal consistency.

- DSR trial count: does it include every parameter combination tried across the project,
  not just this notebook? Recompute if unsure.
- Bootstrap CI must bracket the headline metric. Headline outside CI ⇒ bug.
- Walk-forward mean and test Sharpe must be roughly consistent. Test ≫ walk-forward mean
  ⇒ a single favorable test window or test-set leakage.
- AUC reported on a regression target ⇒ an undisclosed binarization step.
- Regime "positive in 5/5 regimes": how many bars per regime? A regime with 30 bars
  proves nothing.
- Sharpe annualization factor matches bar frequency.

### 5. code-correctness-reviewer

Scope: generic correctness, independent of domain.

- Off-by-one in indexing, slicing, `iloc` vs `loc`
- Sort order assumed but not enforced (`sort_values('date')`, `sort_values(['symbol','date'])`)
- NaN handling: does the model see NaNs? Does PnL silently treat NaN as zero?
- Dtype surprises (int division, datetime tz mismatch)
- Hidden global state (random seeds not set, mutable defaults)
- Multi-instrument operations missing `groupby('symbol')`
- Exception swallowing (`try / except: pass`)
- Hard-coded paths or magic constants that disagree with the design cell

### 6. adversarial-reviewer (cold-eye)

Scope: from code and reported numbers alone, identify at least one implementation bug
that could plausibly contaminate the result. This reviewer is structurally different
from the five specialists — same model, but a *deliberately different* (minimum)
context bundle. The asymmetry is the mechanism: same-context same-model review shares
priors, anchoring, and lost-in-middle effects. Stripping context forces the reviewer
to reason from the artifact alone, not from the author's narrative.

**Receives (minimum bundle)**:

- The notebook `.py` file body
- Upstream feature notebook `.py` files named in the design cell (only if named there)
- Reported headline numbers as listed in the abstract cell (Sharpe, DSR, win rate,
  max drawdown, etc.)

**Does NOT receive**:

- This file (`bug_review.md`) — including the trigger table
- The five specialist reviewers' findings
- `sanity_checks.py` output
- `decisions.md` / `hypotheses.md`
- Chat context / design-process discussion

**Instruction (give verbatim)**:

> "You are reading this code and the reported numbers cold, as an external reviewer.
> Identify at least one implementation bug that could plausibly explain the reported
> numbers. The five specialist reviewers' findings are intentionally withheld — the
> goal is to keep you from anchoring on the priors that the same model shares with
> them. Adopt the working hypothesis 'these numbers are the output of a bug' and try
> to falsify the result."

**Rationale**: Cross-Context Review (Song, arxiv 2603.12123) showed that
review with only the artifact (no production history, no intermediate reasoning, no
generation prompt) yielded the largest gains specifically on code review (+4.7 F1).
The mechanism: a fresh session has no anchor. Same-model perplexity preference is
not addressed by this — that is an accepted residual risk of single-model review —
but anchoring, sycophancy, and lost-in-middle are removed.

## Per-reviewer input contract (efficiency-class, F21)

Each specialist receives **only its own dimension scope** plus the shared
artifacts named below. Whole-file `bug_review.md` and whole-file
`sanity_checks.md` are NOT delivered to specialists — that was the prior
"whole file + read §i only" pattern, which billed dead weight (~96 % of
`bug_review.md` and ~68 % of `sanity_checks.md` per specialist) and
diluted attention. Pre-extract the dimension scope by **section anchor**
(the `### N. <reviewer-name>` heading) before dispatch. Anchor missing →
reviewer flags `severity: high, what: missing input section §<N>` per
the graceful-degradation pattern; do not abort dispatch.

| # | Reviewer | Required scope (extract) | Required shared | NOT-receive |
|---|---|---|---|---|
| 1 | leakage | `bug_review.md` §1 (anchor `### 1. leakage-reviewer`, ~12 lines) | notebook .py, upstream feature notebook .py (only those named in design cell), `sanity_checks.md` §1, §6, §7, §8, §9, §11, §12 | `bug_review.md` outside §1, `sanity_checks.md` outside the named subset, `decisions.md` / `hypotheses.md` / `literature/`, other reviewers' findings |
| 2 | pnl-accounting | `bug_review.md` §2 (anchor `### 2. pnl-accounting-reviewer`, ~14 lines) | notebook .py, `sanity_checks.md` §3, §4, §5, §6, §11 | `bug_review.md` outside §2, `sanity_checks.md` outside the named subset, `decisions.md` / `hypotheses.md` / `literature/` |
| 3 | validation (correctness) | `bug_review.md` §3 (anchor `### 3. validation-reviewer`, ~12 lines) | notebook .py, `sanity_checks.md` §12 | `bug_review.md` outside §3, `sanity_checks.md` outside §12, `decisions.md` / `hypotheses.md` / `literature/` |
| 4 | statistics (metric arithmetic) | `bug_review.md` §4 (anchor `### 4. statistics-reviewer`, ~13 lines) | notebook .py, `sanity_checks.md` §10 | `bug_review.md` outside §4, `sanity_checks.md` outside §10, `decisions.md` / `hypotheses.md` / `literature/` |
| 5 | code-correctness | `bug_review.md` §5 (anchor `### 5. code-correctness-reviewer`, ~12 lines) | notebook .py | `bug_review.md` outside §5, `sanity_checks.md` (no specific section needed), `decisions.md` / `hypotheses.md` / `literature/` |
| 6 | adversarial (cold-eye) | `bug_review.md` §6 (anchor `### 6. adversarial-reviewer`, ~39 lines) — verbatim instruction only | notebook .py (the abstract cell within is the "reported headline numbers" — no separate extract), upstream feature notebook .py (only those named in design cell) | `bug_review.md` outside §6, `sanity_checks.md`, the five specialist reviewers' findings, `decisions.md` / `hypotheses.md` / chat context — full minimum-bundle list per §6 |

**Section anchor as source of truth** — extraction reads the section by
its `### N. <reviewer-name>` heading anchor, not by line range. The
approximate line counts above are reader hints; line ranges in this
file shift when other sections are edited, but anchors don't. A renamed
or removed anchor surfaces a `severity: high, what: missing input
section §<N>` finding from the affected reviewer (graceful degradation),
which is the correct signal for an out-of-sync contract — silent
recovery would mask a real protocol drift.

**Adversary rule**: pre-extraction applies to the adversary as well —
adversary receives §6 only (= 39 lines vs 300). The asymmetry is preserved:
**no §1-§5 specialist scope reaches the adversary**, exactly per the
existing minimum-bundle list. Pre-extraction tightens, not weakens, the
asymmetry.

The contract is **structured**, not prose advice. Tailoring is no longer a
reviewer-discretion decision; it is the parent assistant's pre-dispatch
extraction step (see "Dispatch protocol" step 2 below).

## Trigger-conditional dispatch on re-verify (efficiency-class, F22)

A typical H verdict='supported' attempt enters the gate multiple times:
once on initial pass, then again on each re-verify after fix
reconciliation. The naive contract — "fire all 6 every time" — re-pays
for unchanged surfaces. F22 splits the dispatch into two cases.

### Initial pass

First time this H enters the gate (= no prior clean review on this H in
the current session). **All 6 reviewers fire** as the full gate — the
input contract above is what each reviewer receives.

### Re-verify pass

Triggered after the parent has applied fixes from a prior bug-review
inline summary and completed `references/post_review_reconciliation.md`'s
Definition of Done for those fixes. The parent then identifies **which
surface map entries the fixes touched** and fires only the dimensions
whose surface intersects.

**Adversary auto-fires on re-verify whenever any specialist re-fires** —
its standalone-readability + claim-warrant check is on the
*current* artifact and any change can affect either axis. If no
specialist fires (= no surface change at all), nothing is being
re-verified and the prior clean state stands.

### Surface map per reviewer

Each reviewer's surface = the union of cell categories / file types
whose change re-fires the dimension.

| # | Reviewer | Surface (re-fire if any of these changed since last clean review) |
|---|---|---|
| 1 | leakage | feature definition cells, signal computation cells, normalization / scaling cells, cross-sectional rank / z-score cells, factor-decomposition cells, leak-check cells, target / horizon definition |
| 2 | pnl-accounting | PnL formula cells, position weight cells, fee / cost model cells, turnover calculation cells, currency conversion cells, sign-convention cells |
| 3 | validation (correctness) | split definition (train / val / test boundary), embargo declaration, walk-forward setup, purged k-fold / CPCV setup, test-set evaluation cell |
| 4 | statistics (metric arithmetic) | bootstrap setup, walk-forward summary cells, DSR / PSR cells, headline metric definition, annualization-factor cells, regime-bucketing cells |
| 5 | code-correctness | catch-all on any code cell change in the surfaces above + any indexing / sort / NaN / dtype / RNG cell change anywhere |
| 6 | adversarial (cold-eye) | auto-fires whenever any specialist re-fires (= any change to the artifact); does not have its own surface map because its scope is the entire `.py` standalone |

### When in doubt, fire

Surface classification is the parent assistant's reasoning step. If a
fix doesn't fit any surface entry cleanly — or fits multiple ambiguously
— **default to firing the affected dimensions plus adversary**. The
gate's job is not to skip work but to skip *redundant* work; ambiguity
is not a redundancy signal.

### Cross-session boundary

The "last clean review" baseline is **session-local**. A researcher
returning to the same H next session has no in-context record of which
dimensions were verified clean — the new dispatch is an Initial pass.
Trigger-conditional savings come from the in-session iteration loop
(initial → fix → re-verify → fix → re-verify), which is the modal cost
profile.

If the user explicitly attests in a prior `decisions.md` entry that
"dimensions {X, Y, Z} were verified clean against state S" and the
agent can verify the artifact's relevant surfaces are unchanged from S,
the agent may treat the next dispatch as a re-verify. Without that
attestation in `decisions.md`, treat as Initial.

## Dispatch protocol

1. The assistant verifies that at least one trigger has fired. State the trigger
   explicitly to the user.
2. The assistant determines whether this is an **Initial pass** or a
   **Re-verify pass** (per F22 above).
   - On **Initial**, the assistant **pre-extracts each reviewer's
     dimension scope** from `bug_review.md` (§1-§6) and
     `sanity_checks.md` (per the input contract above), assembles two
     bundles — the full bundle for the five specialists (each with its
     own §i suffix), and the minimum bundle for the adversarial reviewer
     (notebook + §6 instruction). All six reviewers dispatch **in
     parallel** in a single tool-call batch.
   - On **Re-verify**, the assistant identifies the fixes' locations,
     intersects each dimension's surface map, dispatches the affected
     specialists + adversary in parallel. Skipped dimensions are listed
     by name in the inline summary with "skipped: no surface change
     since last clean review" and the surfaces checked.
   Parallelism is required: it forces independent reads, which is the
   mechanism that makes specialist review work. Bundle asymmetry is
   required: it is the mechanism that makes the adversarial pass add
   value over what a sixth specialist would add.
3. Each reviewer returns findings in this schema:

   ```
   - severity: high | medium | low
     where:    <file>:<cell-or-line>
     what:     <one-sentence description>
     why:      <which check / reference / convention is violated>
     fix:      <concrete remediation or a follow-up question>
   ```

4. The assistant aggregates findings into a single structured summary
   **delivered inline in the assistant's reply** — trigger that fired,
   reviewer roster, every finding grouped by severity and dimension, and the
   resolution intent. The skill does not write to `decisions.md` and does not
   create any file.
5. The assistant addresses every `high` and every `medium` finding before re-running
   the battery or declaring a verdict. `low` findings are noted in the same inline
   summary and may be parked. If the user wants a durable record they can copy the
   summary into `decisions.md` themselves.
6. **Post-review reconciliation pass** (mandatory before re-running the robustness
   battery). After fixing the findings in code, run `references/post_review_reconciliation.md`:
   assign every reflected change to one of P1 (in-place rewrite), P2 (same-section
   re-compute / sanity cell at the end of the existing `§N`), P3 (single
   `## Post-review addenda` block before the verdict cell), or P4 (new `## H<id>`).
   New chapters with lowercase / decimal suffixes (`§6a`, `§7b`) and figures that
   violate the up-front figure plan (`Fig 2b`) are forbidden. Re-execute every
   dependent cell, regenerate every figure, rewrite every observation, align all
   abstract / per-H abstract / interpretation numbers with the post-fix pipeline,
   and confirm past-round findings are still reflected. End with a top-to-bottom
   verification pass that confirms no reviewer vocabulary, edit-history language, or
   planning notes (`parked` / `follow-up` / `next-session`) has leaked into the
   notebook body. Without this step, "fixed" in the inline summary is premature —
   the finding is at most "addressed in code."

### Anti-rationalizations (efficiency-class, F21 / F22)

| Excuse | Why it is wrong |
|---|---|
| "Whole-file `bug_review.md` is safer — what if the reviewer needs context outside §i?" | Cross-dimensional findings are caught by the *parallel ensemble*, not by each reviewer reading every section. The five specialists in parallel are designed to overlap defensively at the dimension *level*, not by sharing prose. The whole-file pattern bills 96 % dead weight per specialist and dilutes attention via lost-in-middle. |
| "The adversary should also receive `bug_review.md` outside §6, in case there's context it would benefit from." | The asymmetry IS the mechanism. Giving adversary access to specialist scope (§1-§5) makes it a sixth specialist with the same priors, not a cold-eye reader. CCR (arxiv 2603.12123) showed the gain comes from minimum-context, not from richer-context. |
| "Pre-extraction is brittle — what if the section anchor is renamed?" | Rename a `### N. <reviewer-name>` heading and the dispatch surfaces a graceful-degradation finding (`severity: high, what: missing input section §<N>`). The skill does not silently swallow the rename. The brittleness is *desirable*: a renamed anchor without contract-side update is an actual bug, and the gate catches it. |
| "User asked for 'all findings the file might generate', so safer to send whole file." | The contract names what the reviewer needs to do its dimension's job. "All findings the file might generate" is a search prompt; this is a structured review. If a section outside §i is genuinely needed, edit the contract, do not bypass it case-by-case. |
| "The fix is small / cosmetic, just re-fire all 6 to be safe." (F22) | Re-firing all 6 on a fix that touched a single surface is the dead-weight pattern F22 exists to interrupt. The surface map is what determines re-fire — *any* fix lands on at least one surface, so the firing set is non-empty; cosmetic changes that genuinely touch nothing (e.g. a markdown comment edit) re-fire only narrative + adversary, not the full 6. "Just to be safe" is the exact rationalization the surface map replaces. |
| "I'm unsure which surface this fix touches, default to skipping the dispatch." (F22) | Default is *fire*, not skip. Surface ambiguity → fire the candidates plus adversary. The gate skips only when the parent can confidently classify the fix as not-touching a dimension's surface. Skipping under ambiguity is the failure mode; firing under ambiguity is the safety. |
| "Cross-session: I remember the prior verdict was clean, treat next dispatch as re-verify." (F22) | Without an attestation in `decisions.md` naming which dimensions were verified clean against which artifact state, cross-session is Initial. In-context memory of "I think it was clean" is anchoring on a prior session, not evidence the current artifact's surfaces match the prior clean state. |

## Single-agent fallback

If parallel sub-agent dispatch is unavailable (single-process platform, sub-agent quota,
etc.), the assistant runs the same six scopes sequentially in six distinct passes,
clearing context (or at least re-loading the notebook from scratch) between passes. Six
focused single-pass reviews still substantially outperform one mixed-scope pass. The
adversarial pass is run *with the minimum bundle only* even in the fallback — bundle
asymmetry is preserved. Pre-extraction (F21, per the input contract above) still applies
in fallback — each pass receives only its dimension scope, not whole-file
`bug_review.md`. Trigger-conditional dispatch (F22) also still applies on re-verify —
sequential passes still skip dimensions whose surfaces did not change.

Do not skip scopes. The temptation to merge "leakage" + "validation" into one pass is
exactly the failure mode this layer prevents. The temptation to give the adversarial
reviewer the full bundle "for fairness" is also a failure mode — that collapses the
asymmetry that makes the layer work.

## When findings disagree

Two reviewers can produce contradictory readings (e.g. the leakage-reviewer says "this is
filtering, OK" and the statistics-reviewer says "the in-sample fit is too tight"). Log
both. Do not silently pick the more convenient one. If unresolved after a code re-read,
raise it as a derived hypothesis and run a falsifying experiment (typically a randomized-
target test that the answer should fail).

## Failure mode this layer prevents

The most common failure: agent reads the robustness battery output (all green), declares
`verdict = "supported"`, appends to `results.parquet`, moves on. If the underlying PnL
had a leak, every robustness metric is corrupted in the same direction and the green
ticks are meaningless.

**Bug review precedes robustness battery, not the other way around.** Declaring
`verdict = "supported"` without having actually run a triggered bug-review pass
is a protocol violation that downgrades the result to *preliminary screening*.

## Relationship to `experiment-review` skill

This layer (`bug_review`) and the separate `experiment-review` skill are **distinct,
complementary, and both required** before `verdict = "supported"`. They are intentionally
not merged; their adversarial reviewers in particular receive *different* minimum
bundles tuned to different failure modes.

| | `bug_review` (here) | `experiment-review` (separate skill) |
|---|---|---|
| Question | Is the implementation correct? | Is the claim warranted by the design? |
| Failure mode prevented | Contaminated PnL passing all robustness gates | Real numbers that don't support the abstract's claim |
| Specialists | 5 (leakage / pnl-accounting / validation-correctness / statistics / code-correctness) | 7 (question / scope / method / validation-sufficiency / claim / literature / narrative) |
| Adversarial bundle | code + reported numbers | `.py` file alone |
| Order | Precondition (run first) | Postcondition (run after robustness battery) |

A clean `experiment-review` on top of a buggy implementation produces confidence in a
contaminated PnL — `bug_review` is the precondition. A clean `bug_review` on top of an
unsupported claim produces a deployment-ready overstatement — `experiment-review` is
the postcondition. Neither layer alone is sufficient.

## Audit

The inline summary delivered in the assistant's reply is the audit surface.
Every triggered review must include in that summary:

- The trigger that fired (numeric or state-change)
- The six reviewers that were run (the five specialist scopes plus the
  adversarial reviewer)
- The findings produced, severity-tagged
- What was done about each finding (fixed / parked-with-reason)

If any of these is missing from the reply, the layer was not actually run.
The skill itself does not write to `decisions.md` or any other file; the
session transcript is the trail. If the user wants a durable record they can
copy the inline summary themselves.
