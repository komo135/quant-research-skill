---
name: research
description: Use when conducting R&D work that needs claim discipline, planning structure, or human-facing reports. Triggers when planning experiments, designing baselines, writing up findings, deciding what to do next after a result, characterizing a phenomenon, building a prototype, or maintaining research state across sessions. Applies to basic research (understanding phenomena, building baselines), applied research (achieving measurable objectives), and experimental development (building working systems). Use this skill even when the user does not say the word "research" if the task involves the activities above.
---

# Research

A protocol skill for agent-driven R&D. The job: keep research state honest while preserving research velocity. Use shared vocabulary so multiple sessions and tools can interoperate. Produce human-readable reports that someone outside the session can act on.

## What this skill covers and what it does not

**Covered (audited by this skill):**

- The narrative of what was done, what was found, and what decision follows: `plans/<id>.md`, `decisions.md`, `reports/<id>/report.md`
- Research-level reproducibility — methods description, data identification, statistical setup. Enough that another researcher can re-implement the work based on the prose.
- Claim structure — explicit alternatives and conditions, not buried in prose.

**Not covered (agent's discretion):**

- Experiment-level replicability infrastructure: env locks, commit pinning, seed databases, container files.
- The exact layout of `experiments/<plan>/runs/<run_id>/`.
- Code style, build systems, dependency management.

This separation matters. If the skill audited experiment-level artifacts, agents would spend their effort producing perfect env.lock files instead of doing good research. Replicability of the *scripts* is a personal-tooling concern; reproducibility of the *research* — what someone else can reproduce from your description — is what this skill enforces.

This distinction follows Drummond (2009) and Goodman et al. (2016): methods reproducibility is not the same as computational replicability. We enforce the former.

## R&D Categories

Every plan declares exactly one category. The choice changes the planning style, completion criteria, and report shape. Categories are from the Frascati Manual (OECD 2015) — they are the field-standard vocabulary.

| Category | When to use | Typical output | Default plan mode | Report shape |
|---|---|---|---|---|
| **basic_research** | Investigating a phenomenon, building a baseline, characterizing failure modes, refining a question | New observations, refined question, theoretical insight, reference baseline, failure-mode catalog | exploratory | Phenomenon → Mechanism → Learned → Refined question |
| **applied_research** | Achieving a measurable objective by designing a new method or system | Method achieving target metric, ablation results, comparison vs baselines | confirmatory | Background → Method → Experiments → Ablations → Discussion |
| **experimental_development** | Engineering a working system, prototype, or process improvement | Functioning artifact, performance metrics, operational limits | milestone | System → Performance → Limits → Next iteration |

Categories are not a one-way pipeline. A project may cycle: basic research characterizes a phenomenon → applied research builds a method against the resulting baseline → development engineers it into a system → basic research investigates the new failure modes. The non-linear view is the modern consensus (Kline & Rosenberg 1986; Stokes 1997). Cycling is normal.

Read `references/categories/<category>.md` after picking a category.

## Project Structure

```
<project-root>/
├── README.md                          # entry, goal, status
├── project_state.md                   # current plans, blockers, priorities
├── decisions.md                       # durable state transitions only
│
├── plans/<id>_<slug>.md               # R&D state per plan (the research narrative)
├── literature/papers.md
├── literature/differentiation.md
│
├── lib/                               # shared curated code
│   ├── data/ eval/ viz/ utils/
│   └── tests/
│
├── experiments/                       # per-plan isolation
│   └── <plan_id>_<slug>/
│       ├── code/                      # plan-specific scripts (agent's freedom)
│       ├── configs/
│       ├── runs/                      # execution artifacts (agent's freedom)
│       │   └── <plan_id>__<n>__seed<N>/
│       └── notebooks/
│
├── data/{raw,processed}/
│
└── reports/<id>_<slug>/               # human-facing deliverables
    ├── report.md
    ├── figures/
    └── tables/
```

Boundaries that matter:

- `lib/` is shared. Tests required. Promotion from `experiments/<plan>/code/` requires a `decisions.md` entry, a test, and a docstring. This prevents experiment-specific code from quietly becoming load-bearing infrastructure.
- `experiments/<plan>/` is owned by one plan. Other plans must not import from it. To share, promote to `lib/` first. This prevents cross-plan zombie dependencies.
- `runs/` artifacts have no required schema. Put what helps you. The skill does not audit them.

## The Plan → Execute → Compare → Report cycle

```
1. scripts/new_plan.py creates plans/<id>_<slug>.md from a mode-specific template
2. Write the Plan section. git commit. (Plan is now time-anchored by git.)
3. Execute. Save artifacts under experiments/<plan>/runs/<run_id>/.
4. ANALYZE — apply the EDA / result-analysis discipline (references/analysis.md).
   Observations live in plans/<id>.md Observations and in experiments/<plan>/notebooks/.
5. Write Actual section in plans/<id>.md. Compare planned vs actual.
6. Record load-bearing claims using the structure in references/claim_structure.md.
   Observation → Interpretation → Claim is a staged progression — do not skip stages.
7. Pick exactly one of the 5 iteration branches and record in decisions.md.
8. If the result is human-facing, draft a report with scripts/draft_report.py.
```

Git is the time-anchor for the plan. There is no separate preregistration directory. The plan section of `plans/<id>.md` IS the preregistration; the initial commit IS the time-stamping mechanism. Subsequent commits show the evolution. This avoids the redundancy of maintaining a separate prereg artifact whose only job is "plan existed before result" — git already proves that.

## Vocabulary the skill enforces

Agents must use these labels exactly. They are how other agents, downstream scripts, and audits parse the state.

**Plan modes** (in `plans/<id>.md` YAML front matter):

- `exploratory` — variable space + decision rules fixed; specific predictions not required
- `confirmatory` — hypothesis + primary metric + baseline + decision threshold fixed
- `milestone` — working/not-working criteria + performance target

**Iteration decisions** (in `decisions.md` entries):

- `NEXT_STEP` — continue same plan
- `REFINE` — narrow or change the question within this plan
- `ADJACENT` — open a new related plan
- `PARK` — pause, with named unblock condition
- `CLOSE` — completed, terminal kill, or replaced

**R&D categories**: `basic_research`, `applied_research`, `experimental_development`.

Informal substitutes ("diagnostic detour," "let me keep exploring," "exploratory mechanism research") break interoperability. Use the exact labels.

## Claims

Every load-bearing claim in `plans/<id>.md` and in `reports/<id>/report.md` uses this structure:

```yaml
- claim: <one sentence with specific assertion>
  evidence: <file:line / numeric value / artifact path / citation>
  alternatives_not_excluded: [...]    # empty list claims exhaustion
  conditions_tested: <variable ranges, datasets, parameters>
  conditions_not_tested: [...]        # empty list claims full coverage
```

The discipline: claim strength is read off the contents of `alternatives_not_excluded` and `conditions_not_tested`. There is no numeric strength score, no A0-A5, no TRL ladder. Empty lists are claims about exhaustion and are open to audit.

The schema derives from Toulmin's argument model (1958) but is adapted for machine parsing — `scripts/check_claims.py` verifies the fields. See `references/claim_structure.md`.

## Reports

Reports are for humans. They live under `reports/<id>_<slug>/`. Each report is a snapshot — figures and tables ship inside the report directory so the report is self-contained.

Required sections (category-specific shapes in `references/report_format.md`):

1. **Summary** — 1–2 paragraphs. A reader who reads only this should understand what was done, what was found, and what is next.
2. **Background** — what was known before, what motivated the work.
3. **Methods & Conditions** — substantive enough for re-implementation. Methods reproducibility lives here.
4. **Results** — actual generated figures or tables. Placeholders are not acceptable.
5. **Limitations** — what alternatives remain plausible, what conditions were not tested.
6. **Next action** — one of the 5 iteration decisions, or a specific request to the human reader.

Reports do not need env locks, commit hashes, or seed lists in the prose. One line pointing to `experiments/<plan>/runs/` is enough if a reader wants to dig into raw artifacts.

## When you are unsure

| Situation | Action |
|---|---|
| New project | `scripts/new_project.py` lays down the structure |
| New investigation in an existing project | `scripts/new_plan.py` (asks for category and mode) |
| Result came in | Update `plans/<id>.md` (Actual + Claims), then pick an iteration decision |
| Human asked for a writeup | `scripts/draft_report.py` starts a report from a plan |
| Claim feels strong | Re-read `references/claim_structure.md` and verify alternatives/conditions honestly |
| Don't know which category | Read `references/categories/*.md`; pick the closest fit |

## Quick reference

| What | Where | When to read |
|---|---|---|
| Pick a category | `references/categories/<category>.md` | First action when starting a plan |
| Plan schema | `references/rd_plan.md` | Writing or reviewing `plans/<id>.md` |
| Analysis discipline | `references/analysis.md` | Before or during analysis (EDA / post-experiment), and before promoting an observation to a load-bearing claim |
| Iteration branches | `references/iteration_loop.md` | After every interpreted result |
| Claim schema | `references/claim_structure.md` | Writing or reviewing any load-bearing claim |
| Report shape | `references/report_format.md` | Drafting `reports/<id>/report.md` |
| Literature | `references/literature_review.md` | Project start, before claiming novelty |

## Iron rules

These are not formatting preferences. They are what makes other agents and humans able to reuse the work.

- **One declared category per plan.** Don't dodge the choice. If you can't pick, read `references/categories/*.md`.
- **One declared mode per plan.** `exploratory`, `confirmatory`, or `milestone`. Hidden hypotheses inside exploratory plans are forbidden.
- **No placeholder figures in reports.** Generate the figure or remove the reference. `scripts/check_report.py` verifies figure references resolve.
- **Plan content exists before execution.** The Plan section must be filled in and committed before any execution begins. `created_commit` in the front matter is meaningful only if the Plan section is non-empty at that commit. After-the-fact plan rewriting is detectable in git diff.
- **Decisions are labeled.** "Diagnostic detour," "let me keep going" are not decision labels. Pick from the 5.
- **Claim records have all five fields.** Empty list `[]` is allowed; a missing field is not.
- **Plan is the canonical Methods. Report summarizes, does not duplicate.** Full re-implementation detail lives in `plans/<id>.md` Methodology subsection. The report's Methods section is a human-readable summary that cites the plan for depth. Duplicating content is friction without audit value. See `references/report_format.md`.
- **REFINE appends an Amendment, does not rewrite the Plan.