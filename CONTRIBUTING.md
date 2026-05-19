# Contributing

Thanks for considering a contribution to `research-skill`. This repository contains the `research` plugin, its bundled skills, public templates, and small utility scripts for agent-driven R&D workflows.

## Development setup

Use Python 3.12 or newer.

```bash
python -m pip install -r requirements-dev.txt
```

Run the full verification suite before opening a pull request:

```bash
python -m pytest
python -m json.tool .codex-plugin/plugin.json
python -m json.tool .claude-plugin/plugin.json
python -m json.tool .claude-plugin/marketplace.json
git diff --check
```

Useful targeted checks:

```bash
python -m pytest tests/test_research_docs_contract.py
python -m pytest tests/test_multiple_testing.py
```

## Project boundaries

- `.codex-plugin/plugin.json` is the Codex plugin manifest.
- `.claude-plugin/` contains Claude Code plugin metadata.
- `skills/research/` owns the proposition-first R&D lifecycle.
- `skills/research-plan-review/` owns independent pre-execution plan review.
- `skills/research-result-analysis/` owns independent post-execution result analysis.
- `skills/quant-research/` extends the base research protocol for time-series and statistically rigorous quantitative R&D.
- `tests/` protects stable public contracts and selected executable utilities.

Do not change skill behavior casually. This plugin is a protocol surface: wording changes can change agent behavior.

## Test Admission Gate

Before adding or changing tests, classify the work:

- Behavior / public contract change
- Bug regression
- Characterization / protection test
- Documentation contract
- Release / packaging / cache operation
- Refactor only

Add repository tests only when they protect externally observable contracts that should remain true across future versions.

Do not add repository tests for:

- current version numbers;
- release checklist state;
- cache or installation state;
- PR, push, or merge state;
- implementation path preferences;
- non-contractual wording;
- preferred `SKILL.md` phrasing enforced through string-search tests.

For release, packaging, cache, and plugin metadata work, use verification commands and report evidence instead of adding tests.

## Pull request checklist

Before opening a pull request:

1. Keep the diff scoped to one public behavior, documentation, or packaging concern.
2. Update plugin manifests when public protocol, version, or user-facing description changes.
3. Run the verification commands above.
4. Include the test classification in the PR description.
5. Explain any skipped checks and why they were not applicable.

## Skill documentation changes

For `SKILL.md` behavior, prefer pressure scenarios over brittle repository tests:

1. Give an agent only the skill content and the scenario.
2. Hide the expected answer.
3. Check whether the agent makes the intended judgment under pressure.
4. Tighten the skill text only after the failure mode is clear.

Use repository tests for stable generated file shapes, script inputs/outputs, and release-quality gates, not for incidental phrasing.
