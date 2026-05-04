from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class ProjectBoundaryTests(unittest.TestCase):
    def test_skill_defines_framework_boundary_contract(self) -> None:
        skill = read_text("skills/quant-research/SKILL.md")

        for phrase in [
            "## Framework Boundary",
            "protocol layer",
            "project instance layer",
            "Generated reports are snapshots",
            "Do not embed active candidates",
        ]:
            self.assertIn(phrase, skill)

    def test_new_project_scaffold_separates_protocol_from_instance_work(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "skills/quant-research/scripts/new_project.py"),
                    "alpha",
                    "--mode",
                    "rd",
                    "--root",
                    tmp,
                ],
                check=True,
                cwd=ROOT,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            project = Path(tmp) / "alpha"
            for path in [
                "charter.md",
                "capability_map.md",
                "decisions.md",
                "configs/.gitkeep",
                "src/.gitkeep",
                "tests/.gitkeep",
                "results/figures/.gitkeep",
                "results/intermediate/.gitkeep",
            ]:
                self.assertTrue((project / path).exists(), path)

            readme = (project / "README.md").read_text(encoding="utf-8")
            for phrase in [
                "Boundary contract",
                "Protocol/state source of truth",
                "Project-instance artifacts",
                "Generated report snapshots",
            ]:
                self.assertIn(phrase, readme)

    def test_pure_research_scaffold_creates_first_preregistration_draft(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "skills/quant-research/scripts/new_project.py"),
                    "alpha",
                    "--mode",
                    "pure-research",
                    "--root",
                    tmp,
                ],
                check=True,
                cwd=ROOT,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            project = Path(tmp) / "alpha"
            self.assertTrue((project / "prereg/PR_001.md").exists())
            content = (project / "prereg/PR_001.md").read_text(encoding="utf-8")
            self.assertIn("Pre-Registration", content)

    def test_project_helpers_do_not_fall_back_to_retired_templates(self) -> None:
        new_project = read_text("skills/quant-research/scripts/new_project.py")
        new_trial = read_text("skills/quant-research/scripts/new_trial.py")

        self.assertNotIn("legacy", new_project.lower())
        self.assertNotIn("legacy", new_trial.lower())
        self.assertNotIn("purpose.py.template", new_trial)


if __name__ == "__main__":
    unittest.main()
