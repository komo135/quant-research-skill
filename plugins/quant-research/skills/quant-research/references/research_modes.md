# research_modes.md

Select the research mode before any hypothesis, notebook, or implementation.

## Mode selection

Use **R&D / technology establishment** when the user's real goal is to make a
technical capability exist. Examples:

- Build a reusable validation method for intraday signals.
- Establish whether a foundation-model embedding pipeline can be made useful.
- Create a robust execution-cost modeling technique.
- Turn a fragile notebook idea into a repeatable research capability.

Use **Pure Research** when the user's real goal is knowledge. Examples:

- Understand why a phenomenon appears in one regime and disappears in another.
- Resolve a disagreement between prior papers or prior notebooks.
- Characterize a market mechanism before deciding whether it is useful.
- Produce a paper-like research finding.

If both are present, split them. "Can we build a model that captures X?" is R&D
if the deliverable is the model capability; it is Pure Research if the deliverable
is understanding X.

## Output differences

| | R&D | Pure Research |
|---|---|---|
| Primary object | Technology / capability map | Research state |
| Unit of progress | Capability maturity increases or dependency is clarified | Unknown is narrowed; explanations are pruned |
| Good negative result | Capability is blocked by a named dependency | Explanation is weakened or research question is split |
| Stop condition | Exit criteria for the capability fire | Next discriminating question is clear or conclusion gate passes |
| Bad behavior | Testing whole target without decomposition | Producing a fast conclusion from surface observations |

## Shared rules

- Write the mode choice explicitly.
- State what kind of artifact will count as progress.
- Do not switch modes mid-stream without a ledger update explaining why.
- Treat prior notebooks and decision logs as prior work.
