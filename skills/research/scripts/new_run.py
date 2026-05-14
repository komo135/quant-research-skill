#!/usr/bin/env python3
"""Create a run directory for a plan execution.

Naming: <plan_id>__<n>__seed<N>, where n is auto-incremented.

This is a convenience for consistent naming only. The agent is free to write
whatever helps inside the run directory — there is no required schema.

Usage:
    python new_run.py <project_root> --plan <id> --slug <slug> [--seed <N>]
"""
import argparse
import sys
from datetime import datetime
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Create a run directory for a plan.")
    parser.add_argument("project", help="Project root path")
    parser.add_argument("--plan", required=True, help="Plan ID, e.g., 01")
    parser.add_argument("--slug", required=True, help="Plan slug")
    parser.add_argument("--seed", type=int, default=0, help="Random seed for this run")
    args = parser.parse_args()

    project = Path(args.project).resolve()
    plan_name = f"{args.plan}_{args.slug}"
    runs_dir = project / "experiments" / plan_name / "runs"
    if not runs_dir.parent.exists():
        print(
            f"Error: plan experiments directory does not exist: {runs_dir.parent}",
            file=sys.stderr,
        )
        print(f"Run new_plan.py first to create the plan.", file=sys.stderr)
        sys.exit(1)
    runs_dir.mkdir(parents=True, exist_ok=True)

    # Count existing run directories to auto-increment.
    existing = [d for d in runs_dir.iterdir() if d.is_dir()]
    n = len(existing) + 1

    run_name = f"{args.plan}__{n:03d}__seed{args.seed}"
    run_dir = runs_dir / run_name
    if run_dir.exists():
        print(f"Error: run directory already exists: {run_dir}", file=sys.stderr)
        sys.exit(1)
    run_dir.mkdir()
    (run_dir / "outputs").mkdir()

    # README with conventions (not enforcement).
    (run_dir / "README.md").write_text(
        f"# Run {run_name}\n\n"
        f"Created: {datetime.now().isoformat(timespec='seconds')}\n"
        f"Plan: {plan_name}\n"
        f"Seed: {args.seed}\n\n"
        f"This directory is the agent's freedom zone — no required schema.\n"
        f"Common files (use what helps):\n"
        f"- config.yaml — settings used for this run\n"
        f"- metrics.json — numeric outputs\n"
        f"- stdout.log, stderr.log — captured output\n"
        f"- outputs/ — generated artifacts (csv, npz, ckpt, etc.)\n"
        f"- notes.md — observations specific to this run\n",
        encoding="utf-8",
    )

    print(f"Created run: {run_dir.relative_to(project)}/")


if __name__ == "__main__":
    main()
