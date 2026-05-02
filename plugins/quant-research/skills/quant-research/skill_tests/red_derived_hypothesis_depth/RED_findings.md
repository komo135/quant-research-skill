# RED findings — derived-hypothesis depth

## Setup recap

Fixture provides only the parent H1's headline numbers, the one-line H1
observation cell, and `failure_mode = fee_model`. Mechanism-level
post-mortem has *not* been done. Subagent dispatched under the current
skill (no `acceptance_criteria.md` shown).

## What the subagent produced

H2/H3/H4 with the following shapes (paraphrased):

- **H2** — replace signal-flip exit with TP/SL volatility-scaled exit.
- **H3** — restrict H1 configuration to a pre-committed low-vol regime.
- **H4** — replace RSI(14) entry with Bollinger %B (operationalization-
  invariance test of the rejection).

Routing decisions: all three same-notebook, all `pathway = 4`.

## Evaluation against `acceptance_criteria.md`

| Criterion | Verdict |
|---|---|
| **F-RED-1** (no why-why chain ≥ 3 levels written before deriving) | **FIRES.** The agent jumps from `failure_mode = fee_model` directly to a one-shot list of candidate axes (turnover problem / wrong holding-time / regime-conditional). No recursive "why? → because A → why A? → because B → why B? → mechanism" structure. The deepest reasoning is a single-level "fee_model could be driven by X, Y, or Z." |
| **F-RED-2** (chain terminates at metric / parameter / `failure_mode` label) | Vacuous — no chain to evaluate. |
| **F-RED-3** (≥ 1 surface-derived H) | Does not fire. Each H carries a mechanism-flavored justification paragraph (e.g., H2 cites signal-flip's chop-sensitivity; H3 cites low-vol → signal-to-noise). The agent *does* think about mechanism implicitly. |
| **F-RED-4** (≥ 1 parameter-variation H not also mechanism-grounded) | Does not fire on this output. H2 changes exit *type* (not parameters); H3 adds a regime gate with mechanism justification; H4 changes feature operationalization. |
| **F-RED-5** (≥ 1 H cannot state its own purpose) | Does not fire. Each H names an alternative reading it tests. |

## Net diagnosis

The current skill **fails on F-RED-1** but does not fire F-RED-3/4/5.

What this means: the skill *does not mandate* a why-why chain, but a
careful agent (Sonnet, here) reaches mechanism-flavored derivations
anyway by its own thoroughness. The protocol-mandated discipline is
missing — it is being *substituted by the model's general competence*.

This is the empirical confirmation of the user's complaint reframed:
the skill *permits* a researcher to skip the why-why chain and derive
H's directly from the `failure_mode` label. A less careful researcher
(or the same researcher under fatigue or sunk-cost pressure) will
produce shallow derivations and the protocol provides no friction.

The agent itself flags the gap mid-output:

> "Pathway 4 formally requires the failure-mode-analysis entry. The
> fixture says no post-mortem has been done. The skill-correct move
> is: do the post-mortem first, then derive."

— but it then proceeds to derive anyway, treating the failure-mode
analysis as a "precondition to flag" rather than a hard gate. That
treatment is consistent with the current skill's text: Pathway 4
mentions a "failure-mode analysis entry" but does not specify its
required depth or shape.

## What GREEN must add

1. **A mandatory why-why chain** (≥ 3 consecutive levels) for *every*
   parent H whose verdict has been declared, **regardless of whether
   the verdict is supported or rejected**, before any derived H is
   admissible. The chain is written into the parent H's per-H block
   tail (and/or `decisions.md`'s Purpose entry) and is visible in the
   notebook artifact.
2. **A termination condition** on the chain: the terminal answer must
   be a mechanism-level statement (= what the strategy was actually
   exposed to / harvested / selected), **not** a metric, threshold,
   parameter, or `failure_mode` label.
3. **An admissibility gate on each derived H**: each derived H's
   justification must cite a specific terminal answer from the
   why-why chain. A derived H whose justification reads "the parent
   was rejected with `failure_mode = X`, so let's try Y" — without
   citing a chain terminal — is inadmissible.
4. **The rule applies to supported parent verdicts as well** —
   "the parent was supported, so let's try a sibling instrument" is
   the same shallowness pattern; the why-why must answer "why was
   the parent supported, mechanically?" before deriving.

These are the changes GREEN encodes.
