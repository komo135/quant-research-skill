# research_state.md

`research_state.md` is the compact, current map of the investigation. It
prevents the project from becoming a pile of hypotheses and decisions.

## Required sections

```markdown
# Research state

## Mode
[R&D / Pure Research, with one-sentence reason.]

## Active questions
| ID | Question | Why it matters | Current best answer | Status | Next discriminating step |
|---|---|---|---|---|---|

## Explanations
| ID | Explanation | Supports | Weakened by | Status | Next test |
|---|---|---|---|---|---|

## R&D capabilities
| ID | Capability | Maturity | Exit criteria | Status | Next test |
|---|---|---|---|---|---|

## Claims
| ID | Claim | Evidence | Status | Promotion gate |
|---|---|---|---|---|

## Retired / merged / stale
| ID | Old row | New state | Reason | Date |
|---|---|---|---|---|
```

Use only the sections that apply. Pure Research may leave R&D capabilities
empty. R&D may leave pure explanatory claims sparse until a research question
emerges.

## Status meanings

- `active`: live and worth further discrimination
- `resolved`: answered enough for the current consumer / capability
- `rejected`: contradicted or no longer plausible
- `merged`: absorbed into another row
- `stale`: no longer valid after later evidence or scope change
- `parked`: deferred with a named unblock condition
- `blocked`: cannot progress until a dependency changes
- `supported`: claim has passed the required promotion gate; use only in
  Claims, never for an entire technology map row unless the R&D promotion rule
  in `SKILL.md` has passed

## Update rules

- Every session must update at least one row or explicitly state that no
  research progress occurred.
- Before adding a row, search for rows to merge, retire, or mark stale.
- A row cannot remain `active` indefinitely without a next discriminating step.
- `parked` requires an unblock condition. Without one, use `rejected` or
  `stale`.
- Promotion to `supported` belongs in `Claims` and requires the promotion gate
  from `hypothesis_quality.md`.
- Before accepting a new hypothesis ID, identify the parent question /
  explanation / capability. If the candidate is only a parameter or
  implementation variant of that parent, update the parent row's next
  discriminating step instead of adding a new active row.
- If the workspace is read-only or the ledger files do not yet exist, produce a
  proposed ledger update block in the response with exact rows that would be
  written. Mark it as `proposed`, not as completed state.
