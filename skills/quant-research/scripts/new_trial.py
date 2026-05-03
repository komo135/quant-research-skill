"""new_trial.py — Create a numbered trial notebook (mode-aware).

Replaces the older `new_purpose.py`. Mode-aware: chooses the correct
template based on whether the project is R&D or Pure Research.

Per CHARTER C1 and the templates:
- R&D: assets/rd/rd_trial.py.template (capability-anchored)
- Pure Research: assets/pure_research/pr_trial.py.template
  (pre-registration-anchored)

Trial files are named `trial_NNN_<slug>.py` in `<project>/purposes/`.

Usage:
    # R&D
    python scripts/new_trial.py --project-dir <path> --slug regime_classifier_zeroshot \\
        --capability-id C1 --core-tech-id K1 --stage de-risk

    # Pure Research
    python scripts/new_trial.py --project-dir <path> --slug vol_carry_decay_test \\
        --prereg-id PR_001 --question-id Q1 --discriminating "E1 vs E2"

Exit codes:
    0: trial notebook created
    1: project not found
    2: missing required argument for the project's mode
    3: trial slug collides
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"


def detect_mode(project_dir: Path) -> str:
    """Detect project mode by which top-level artifact is present."""
    has_charter = (project_dir / "charter.md").exists()
    has_prfaq = (project_dir / "prfaq.md").exists()
    if has_charter and has_prfaq:
        raise ValueError(
            "Both charter.md and prfaq.md present — mode mixing detected. "
            "Per CHARTER C1, project must be one mode only."
        )
    if has_charter:
        return "rd"
    if has_prfaq:
        return "pure-research"
    raise FileNotFoundError(
        "Neither charter.md nor prfaq.md found in project — "
        "run scripts/new_project.py to scaffold first."
    )


def next_trial_number(purposes_dir: Path) -> int:
    """Return next sequence number based on trial_NNN_*.py and pur_NNN_*.py files."""
    purposes_dir.mkdir(parents=True, exist_ok=True)
    pattern_trial = re.compile(r"trial_(\d{3})_.*\.py")
    pattern_pur = re.compile(r"pur_(\d{3})_.*\.py")
    existing: list[int] = []
    for f in purposes_dir.glob("*.py"):
        for pat in (pattern_trial, pattern_pur):
            m = pat.match(f.name)
            if m:
                existing.append(int(m.group(1)))
                break
    return max(existing, default=0) + 1


def find_template(mode: str) -> Path:
    if mode == "rd":
        candidates = [
            ASSETS_DIR / "rd" / "rd_trial.py.template",
            ASSETS_DIR / "purpose.py.template",  # legacy fallback
        ]
    else:
        candidates = [
            ASSETS_DIR / "pure_research" / "pr_trial.py.template",
            ASSETS_DIR / "purpose.py.template",  # legacy fallback
        ]
    for c in candidates:
        if c.exists():
            return c
    raise FileNotFoundError(f"trial template not found in any of: {candidates}")


def substitute_rd(content: str, capability_id: str, core_tech_id: str,
                  stage: str, slug: str, nnn: str, project_name: str) -> str:
    """Replace <REPLACE: ...> markers in R&D trial template that we can fill from args."""
    return (
        content
        .replace("<REPLACE: NNN>", nnn)
        .replace("<REPLACE: short title>", slug.replace("_", " "))
        .replace("<REPLACE: project name>", project_name)
        .replace("C<REPLACE: capability id>", capability_id)
        .replace("K<REPLACE: K-id>", core_tech_id)
        .replace("<REPLACE: Scoping | De-risk | Build | Validate | Integrate>", stage)
    )


def substitute_pr(content: str, prereg_id: str, question_id: str,
                  discriminating: str, slug: str, nnn: str, project_name: str) -> str:
    """Replace <REPLACE: ...> markers in PR trial template that we can fill from args."""
    return (
        content
        .replace("<REPLACE: NNN>", nnn)
        .replace("<REPLACE: short title>", slug.replace("_", " "))
        .replace("<REPLACE: project name>", project_name)
        .replace("Q<REPLACE: Q-id>", question_id)
        .replace("E<REPLACE: id> vs E<REPLACE: id>", discriminating)
        .replace("prereg/PR_<REPLACE: id>", f"prereg/{prereg_id}")
        .replace("PR_<REPLACE: id>", prereg_id)
    )


def create_trial(args: argparse.Namespace) -> Path:
    project_dir: Path = args.project_dir.resolve()
    if not project_dir.exists():
        raise FileNotFoundError(f"project not found: {project_dir}")

    mode = detect_mode(project_dir)

    if mode == "rd":
        if not (args.capability_id and args.core_tech_id and args.stage):
            raise ValueError(
                "R&D project requires --capability-id, --core-tech-id, --stage"
            )
    else:
        if not (args.prereg_id and args.question_id and args.discriminating):
            raise ValueError(
                "Pure Research project requires --prereg-id, --question-id, --discriminating"
            )

    purposes_dir = project_dir / "purposes"
    n = next_trial_number(purposes_dir)
    nnn = f"{n:03d}"
    slug = args.slug
    out_path = purposes_dir / f"trial_{nnn}_{slug}.py"
    if out_path.exists():
        raise FileExistsError(f"already exists: {out_path}")

    template_path = find_template(mode)
    content = template_path.read_text(encoding="utf-8")

    if mode == "rd":
        content = substitute_rd(
            content, args.capability_id, args.core_tech_id, args.stage,
            slug, nnn, project_dir.name,
        )
    else:
        content = substitute_pr(
            content, args.prereg_id, args.question_id, args.discriminating,
            slug, nnn, project_dir.name,
        )

    out_path.write_text(content, encoding="utf-8")

    # Append to INDEX.md
    index_path = purposes_dir / "INDEX.md"
    if index_path.exists():
        index = index_path.read_text(encoding="utf-8")
        if mode == "rd":
            new_row = (
                f"| trial_{nnn} | rd | {args.capability_id} ({args.core_tech_id}) | "
                f"stage={args.stage} | active | pending |\n"
            )
        else:
            new_row = (
                f"| trial_{nnn} | pure-research | {args.question_id} ({args.prereg_id}) | "
                f"discriminating: {args.discriminating} | active | pending |\n"
            )
        # Append to end (simple approach)
        index_path.write_text(index.rstrip() + "\n" + new_row, encoding="utf-8")

    return out_path


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--project-dir", required=True, type=Path)
    p.add_argument("--slug", required=True, help="trial slug (alphanumeric + _)")
    # R&D-specific
    p.add_argument("--capability-id", help="(R&D) capability ID, e.g. C1")
    p.add_argument("--core-tech-id", help="(R&D) parent core tech ID, e.g. K1")
    p.add_argument("--stage", help="(R&D) Stage-Gate stage: scoping | de-risk | build | validate | integrate")
    # Pure Research-specific
    p.add_argument("--prereg-id", help="(Pure Research) pre-registration ID, e.g. PR_001")
    p.add_argument("--question-id", help="(Pure Research) question ID, e.g. Q1")
    p.add_argument("--discriminating", help="(Pure Research) E pair, e.g. 'E1 vs E2'")
    args = p.parse_args()

    try:
        out_path = create_trial(args)
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(2)
    except FileExistsError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(3)

    print(f"✅ Created: {out_path}")
    print()
    print("Next steps:")
    print(f"  1. Open {out_path} in marimo: marimo edit {out_path}")
    print("  2. Fill the Trial design header (markdown cells) per the template")
    print("  3. Run sanity checks BEFORE the main test")
    print("  4. After trial, run prereg_diff.py (Pure Research) and fill the 5-field Analysis section")
    print("  5. Update the relevant ledger row (capability_map.md or explanation_ledger.md)")


if __name__ == "__main__":
    main()
