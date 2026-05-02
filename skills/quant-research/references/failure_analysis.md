# failure_analysis.md

Use this whenever a hypothesis misses, a result is ambiguous, or the first
interpretation feels obvious.

## Rule

Generic labels are not causes. "Noise", "data quality", "sample size",
"regime", "overfitting", "cost", and "model weakness" are starting labels.
They must be decomposed before they can explain anything.

## Failure analysis block

```markdown
## Failure / ambiguity analysis for <trial>

### Observed pattern
[Numbers and plots, stated without interpretation.]

### Immediate non-conclusions
[Things the result does NOT prove.]

### Candidate explanations
| ID | Explanation | Evidence for | Evidence against | Test that would distinguish it | Status |
|---|---|---|---|---|---|
| E1 | ... | ... | ... | ... | active |

### Decomposition of convenient labels
[If using labels like noise/regime/data quality, break them into observable
sub-claims.]

### What became weaker
[Which explanation or hypothesis lost support, and why.]

### What remains alive
[Which explanations still survive.]

### Next smallest discriminating test
[The smallest next action that separates live explanations.]
```

## Depth checks

Before finalizing interpretation, answer:

- What exact observation forced this analysis?
- Which explanation would I prefer if I were trying to finish quickly?
- What alternative explanation would a skeptical reviewer raise?
- What evidence would make my preferred explanation false?
- If all tool / library / model names are masked, what claim remains?

If the answers are vague, the analysis is not complete.

## Prohibited endings

Do not end with:

- "The hypothesis was rejected because the data is noisy."
- "The model failed because the market regime changed."
- "More data is needed."
- "Try another parameter."

Allowed ending shape:

- "E2 is weaker because observation O contradicts prediction P. E1 and E3
  remain active. The next discriminating test is T because it separates E1 from
  E3 on observable axis A."
