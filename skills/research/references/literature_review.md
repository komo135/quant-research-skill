# Literature Review

## Purpose

Document what is already known about the research question before claiming novelty or building a method.

The job is not to be exhaustive. It is to:

1. Know what is already established so you are not re-running prior work
2. Identify the closest prior approaches so your method's contribution is clear
3. Cite the baselines you will compare against (in applied research)

## When to do this

- At the start of any new plan, before writing the Plan section
- Before claiming a method is novel
- Before claiming a baseline does not exist
- When the agent encounters an unfamiliar method during execution

A brief pass is appropriate for most plans (a handful of relevant works). Comprehensive review is appropriate only for plans that will produce external claims of novelty.

## Files

- `literature/papers.md` — annotated list of relevant prior work
- `literature/differentiation.md` — how this work differs from prior approaches

## papers.md format

```markdown
## <Author year — short title>

- Citation: <full bib reference or URL>
- Method / Finding: <one-paragraph summary, in your own words>
- Relevance: <why this matters for the current plan>
- Used as baseline: yes / no
```

Two paragraphs per entry maximum. Longer summaries belong in the agent's session notes, not in the project state. The point is to make the entry scannable when a future session is checking what was considered.

## differentiation.md format

```markdown
# How this work differs

## <Prior approach A — cite papers.md entry>
- What it does: <summary>
- What it does not do: <gap or limitation>
- Our work: <how this plan addresses the gap>

## <Prior approach B>
- ...
```

If the work does not differ from prior approaches in a meaningful way, this is itself an important finding. Basic-research replication is valuable, but the report should be honest about being a replication.

## Common failures

- **Claiming novelty without literature search.** "To our knowledge" is not a search; it is an absence of search. If the agent has not actually searched, the claim of novelty is unsupported.
- **Listing tangentially related papers to look thorough.** Each entry should connect to the current plan, not pad a citation count.
- **Comparing against the wrong baselines.** If you compare to a 5-year-old baseline because the recent ones are hard to run, the comparison is biased — say so explicitly in differentiation.md and in the report.
- **Not updating papers.md mid-investigation.** When a new relevant paper appears during execution (e.g., the agent finds it while debugging), add it to papers.md and update differentiation.md if relevant.
