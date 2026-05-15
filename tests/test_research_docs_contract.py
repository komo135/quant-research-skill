from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def assert_mentions(text: str, *terms: str):
    lowered = text.lower()
    missing = [term for term in terms if term.lower() not in lowered]
    assert not missing, f"missing terms: {missing}"


def assert_ordered_fragments(text: str, *fragments: str):
    normalized = " ".join(text.lower().split())
    cursor = 0
    missing = []
    for fragment in fragments:
        index = normalized.find(fragment.lower(), cursor)
        if index == -1:
            missing.append(fragment)
        else:
            cursor = index + len(fragment)
    assert not missing, f"missing ordered fragments: {missing}"


def assert_absent(text: str, *terms: str):
    lowered = text.lower()
    present = [term for term in terms if term.lower() in lowered]
    assert not present, f"unexpected terms present: {present}"


def test_report_format_distinguishes_material_conditions_from_env_locks():
    report_format = read("skills/research/references/report_format.md")

    assert_ordered_fragments(
        report_format,
        "reports should describe material conditions",
        "not environment locks",
        "methods reproducibility",
        "not computational replicability",
    )
    assert_ordered_fragments(
        report_format,
        "seed information",
        "variability disclosure",
        "not a substitute for reporting variance",
    )


def test_research_skill_frames_provenance_as_audit_not_reproducibility_itself():
    skill = read("skills/research/SKILL.md")

    assert_mentions(skill, "material execution conditions")
    assert_ordered_fragments(
        skill,
        "provenance",
        "audit pointer",
        "not the source of reproducibility",
    )
    assert_ordered_fragments(
        skill,
        "claim-to-artifact",
        "integrity check",
        "rather than making the method reproducible",
    )


def test_report_format_frames_claim_to_artifact_as_integrity_not_reproducibility():
    report_format = read("skills/research/references/report_format.md")

    assert_mentions(
        report_format,
        "claim-to-artifact",
        "evidence-integrity",
    )
    assert_ordered_fragments(
        report_format,
        "claim-to-artifact consistency",
        "evidence-integrity check",
        "not a separate reproducibility theory",
    )


def test_plan_schema_requires_material_conditions_not_env_locks():
    rd_plan = read("skills/research/references/rd_plan.md")

    assert_ordered_fragments(
        rd_plan,
        "audit trail",
        "not a substitute for methodology",
    )
    assert_ordered_fragments(
        rd_plan,
        "methods reproducibility",
        "material conditions",
        "not env locks or commit hashes",
    )
    assert_ordered_fragments(
        rd_plan,
        "changing a seed value",
        "before seeing outcomes",
        "usually not material",
        "changing the seed policy",
        "train/test split seed",
        "after seeing a result",
        "is material",
    )


def test_readme_keeps_experiment_replicability_out_of_the_core_contract():
    readme = read("README.md")

    assert_ordered_fragments(
        readme,
        "research-level reproducibility",
        "is enforced",
        "experiment-level replicability",
        "agent's discretion",
    )
    assert_ordered_fragments(
        readme,
        "reports record",
        "material conditions",
        "not environment locks",
    )
    assert_ordered_fragments(
        readme,
        "claim-to-artifact consistency checks",
        "evidence-integrity checks",
        "rather than a replacement for methods reproducibility",
    )
    assert_ordered_fragments(
        readme,
        "experiment-level replicability infrastructure",
        "not skill-enforced",
        "provenance or variability logs",
        "not substitutes for methods reproducibility",
    )


def test_report_templates_prompt_for_material_conditions():
    template_dir = ROOT / "skills" / "research" / "assets" / "report"

    for template in template_dir.glob("*.template"):
        text = template.read_text(encoding="utf-8")
        assert "Material conditions" in text, template
        assert "when applicable" in text.lower(), template
        assert "not environment locks" in text, template


def test_applied_report_keeps_material_conditions_in_methods_area():
    text = read("skills/research/assets/report/applied_research_report.md.template")

    material_position = text.index("### Material conditions")
    results_position = text.index("## Results")

    assert material_position < results_position


def test_claim_and_analysis_docs_frame_evidence_and_seed_variability():
    claim_structure = read("skills/research/references/claim_structure.md")
    analysis = read("skills/research/references/analysis.md")

    assert_ordered_fragments(
        claim_structure,
        "evidence-integrity anchor",
        "not by itself a reproducibility guarantee",
        "method and tested conditions",
        "reproducibility burden",
    )
    assert_ordered_fragments(
        analysis,
        "do not treat a single fixed seed as reproducibility",
        "report seed count, dispersion, and failed seeds",
        "claim is supported by the distribution of outcomes",
    )


def test_quant_docs_use_seed_variability_and_artifact_auditability_terms():
    modeling = read("skills/quant-research/references/shared/modeling_approach.md")
    feature_construction = read("skills/quant-research/references/shared/feature_construction.md")

    assert "Seed variability / RNG sensitivity" in modeling
    assert "report distribution over multiple seeds" in modeling
    assert "breaks artifact provenance and downstream auditability" in feature_construction


def test_plan_templates_prompt_for_material_conditions():
    template_dir = ROOT / "skills" / "research" / "assets" / "plan"

    for template in template_dir.glob("*.template"):
        text = template.read_text(encoding="utf-8")
        assert "material conditions" in text, template


def test_every_plan_template_requires_prior_work_grounding_before_plan():
    template_dir = ROOT / "skills" / "research" / "assets" / "plan"

    for template in template_dir.glob("*.template"):
        text = template.read_text(encoding="utf-8")
        assert "## Prior-work grounding" in text, template
        assert text.index("## Prior-work grounding") < text.index("## Plan"), template
        assert_mentions(
            text,
            "bounded but sufficient",
            "question/objective",
            "inherited assumptions",
            "method choice",
            "baselines/evaluation protocol",
            "known limitations",
        )
        assert_absent(
            text,
            "Novelty / differentiation thesis",
            "unknown-not-yet-reviewed if no novelty claim is made",
            "literature/differentiation.md",
        )


def test_plan_schema_makes_prior_work_grounding_first_class_not_novelty_optional():
    rd_plan = read("skills/research/references/rd_plan.md")

    assert_ordered_fragments(
        rd_plan,
        "## Question / Objective",
        "## Prior-work grounding",
        "## Divergence checkpoint",
        "## Plan",
    )
    assert_mentions(
        rd_plan,
        "bounded but sufficient",
        "question/objective",
        "inherited assumptions",
        "method choice",
        "baselines/evaluation protocol",
        "known limitations",
        "named constraint",
        "narrow or block relevant claims",
    )
    assert_absent(
        rd_plan,
        "Novelty / differentiation thesis",
        "unknown-not-yet-reviewed",
        "literature/differentiation.md",
    )


def test_literature_review_contract_uses_positioning_for_grounding_not_default_novelty():
    literature = read("skills/research/references/literature_review.md")

    assert_mentions(
        literature,
        "prior-work grounding",
        "bounded but sufficient",
        "literature/positioning.md",
        "stands on prior work",
        "claim scope",
        "comprehensive literature survey",
        "to our knowledge",
    )
    assert_ordered_fragments(
        literature,
        "every plan needs prior-work grounding",
        "not optional just because no novelty claim is made",
    )
    assert_absent(
        literature,
        "A brief pass is appropriate",
        "literature/differentiation.md",
        "differentiation.md format",
    )


def test_research_skill_and_project_seed_positioning_not_differentiation():
    skill = read("skills/research/SKILL.md")
    new_project = read("skills/research/scripts/new_project.py")
    project_readme = read("skills/research/assets/project/README.md.template")

    for text in [skill, new_project, project_readme]:
        assert_mentions(text, "literature/positioning.md")
        assert_absent(text, "literature/differentiation.md")

    assert_mentions(
        new_project,
        "positioning.md",
        "how the work stands on prior work",
    )
    assert_absent(new_project, "differentiation.md")


def test_readme_and_plugin_metadata_are_v204_prior_work_grounding_release():
    readme = read("README.md")
    codex_plugin = read(".codex-plugin/plugin.json")
    claude_plugin = read(".claude-plugin/plugin.json")
    marketplace = read(".claude-plugin/marketplace.json")

    for text in [readme, codex_plugin, claude_plugin, marketplace]:
        assert_mentions(text, "2.0.4", "prior-work grounding")
        assert_absent(text, '"version": "2.0.3"')

    assert_mentions(readme, "literature/{papers.md,positioning.md}")
    assert_absent(readme, "literature/{papers.md,differentiation.md}")


def test_research_docs_do_not_preserve_legacy_light_review_loopholes():
    docs = [
        "skills/research/SKILL.md",
        "skills/research/references/literature_review.md",
        "skills/research/references/rd_plan.md",
        "skills/research/assets/plan/rd_plan_exploratory.md.template",
        "skills/research/assets/plan/rd_plan_confirmatory.md.template",
        "skills/research/assets/plan/rd_plan_milestone.md.template",
        "README.md",
    ]

    for path in docs:
        assert_absent(
            read(path),
            "brief pass",
            "light review",
            "unknown-not-yet-reviewed if no novelty claim is made",
            "unknown-not-yet-reviewed is allowed only when",
            "Novelty / differentiation thesis",
            "literature/differentiation.md",
        )
