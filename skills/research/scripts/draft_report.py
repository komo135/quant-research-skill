#!/usr/bin/env python3
"""Initialize a report directory from a hypothesis plan.

Creates:
    propositions/<P>/hypotheses/<H>/reports/<report_id>_<slug>/report.md
    propositions/<P>/hypotheses/<H>/reports/<report_id>_<slug>/figures/
    propositions/<P>/hypotheses/<H>/reports/<report_id>_<slug>/tables/

Usage:
    python draft_report.py <project_root> \
        --proposition P001_slug --hypothesis H001_slug \
        --id R01 --slug <report-slug> \
        --category basic_research|applied_research|experimental_development
"""
import argparse
import re
import sys
from datetime import date
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parent.parent
ASSETS = SKILL_ROOT / "assets"
PROP_DIR_RE = re.compile(r"^P\d{3}_[a-z0-9]+(?:-[a-z0-9]+)*$")
HYP_DIR_RE = re.compile(r"^H\d{3}_[a-z0-9]+(?:-[a-z0-9]+)*$")
REPORT_ID_RE = re.compile(r"^R\d{2,3}$")
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def fail(message: str) -> None:
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(1)


def ensure_inside(path: Path, root: Path, label: str) -> None:
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        fail(f"{label} escapes expected root: {path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Initialize a report from a hypothesis plan.")
    parser.add_argument("project", help="Project root path")
    parser.add_argument("--proposition", required=True, help="Parent proposition directory, e.g. P001_slug")
    parser.add_argument("--hypothesis", required=True, help="Hypothesis directory, e.g. H001_slug")
    parser.add_argument("--id", required=True, help="Report ID, e.g. R01")
    parser.add_argument("--slug", required=True, help="Report slug")
    parser.add_argument(
        "--category",
        required=True,
        choices=["basic_research", "applied_research", "experimental_development"],
    )
    parser.add_argument("--title", default=None, help="Report title (defaults to slug)")
    args = parser.parse_args()

    project = Path(args.project).resolve()
    if not PROP_DIR_RE.fullmatch(args.proposition):
        fail("proposition must match P###_kebab-case-slug")
    if not HYP_DIR_RE.fullmatch(args.hypothesis):
        fail("hypothesis must match H###_kebab-case-slug")
    if not REPORT_ID_RE.fullmatch(args.id):
        fail("report id must match R## or R###")
    if not SLUG_RE.fullmatch(args.slug):
        fail("slug must be kebab-case using lowercase letters, numbers, and hyphens")
    hyp_root = project / "propositions" / args.proposition / "hypotheses"
    hyp_dir = hyp_root / args.hypothesis
    ensure_inside(hyp_dir, hyp_root, "hypothesis path")
    if not hyp_dir.exists():
        fail(f"hypothesis directory does not exist: {hyp_dir}")

    report_dir = hyp_dir / "reports" / f"{args.id}_{args.slug}"
    ensure_inside(report_dir, hyp_dir / "reports", "report path")
    if report_dir.exists():
        fail(f"report directory already exists: {report_dir}")
    report_dir.mkdir(parents=True)
    (report_dir / "figures").mkdir()
    (report_dir / "tables").mkdir()

    tpl_path = ASSETS / "report" / f"{args.category}_report.md.template"
    if not tpl_path.exists():
        fail(f"template not found: {tpl_path}")

    title = args.title or args.slug.replace("-", " ").title()
    plan_path = f"propositions/{args.proposition}/hypotheses/{args.hypothesis}/plan.md"
    run_path = f"propositions/{args.proposition}/hypotheses/{args.hypothesis}/experiments/runs/"
    content = (
        tpl_path.read_text(encoding="utf-8")
        .replace("YYYY-MM-DD", str(date.today()))
        .replace("<report-id>", args.id)
        .replace("<plan-id>", args.hypothesis.split("_", 1)[0])
        .replace("<slug>", args.hypothesis.split("_", 1)[1] if "_" in args.hypothesis else args.hypothesis)
        .replace("<Report Title>", title)
        .replace("propositions/<Pxxx_slug>/hypotheses/<Hxxx_slug>/plan.md", plan_path)
        .replace("propositions/<Pxxx_slug>/hypotheses/<Hxxx_slug>/experiments/runs/", run_path)
    )

    (report_dir / "report.md").write_text(content, encoding="utf-8")
    (report_dir / "figures" / ".gitkeep").touch()
    (report_dir / "tables" / ".gitkeep").touch()

    print(f"Created report directory: {report_dir.relative_to(project)}/")
    print()
    print("Reminders:")
    print(f"  - Fill in {report_dir.relative_to(project)}/report.md")
    print(f"  - Generate real figures into {report_dir.relative_to(project)}/figures/")
    print("    (placeholder figure references fail the report contract)")
    print("  - Run check_claims.py against report.md before sharing")


if __name__ == "__main__":
    main()
