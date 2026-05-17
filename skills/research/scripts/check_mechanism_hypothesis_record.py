#!/usr/bin/env python3
"""Verify a Mechanism hypothesis record against the research ideation contract.

Checks:
- If a Mechanism hypothesis record section is present and applicable, it
  contains diagnosis, lens consideration, adopted lenses, mechanistic analysis,
  and the final mechanism hypothesis record.
- The final record includes a hypothesis, competing hypothesis, discriminating
  prediction, minimal test, required evidence, decision, and reason.
- Decisions are exactly commit / park / kill.
- A blocked diagnosis cannot be committed.

Exit code 0 if all checks pass, 1 if any issue is reported.

Usage:
    python check_mechanism_hypothesis_record.py <path_to_plan.md>
"""
import argparse
import re
import sys
from pathlib import Path


REQUIRED_SUBSECTIONS = [
    "Research situation diagnosis",
    "Analysis lenses considered",
    "Adopted analysis lenses",
    "Mechanistic analysis",
    "Mechanism hypothesis record",
]

SECTION_FIELDS = {
    "Research situation diagnosis": [
        "Available material",
        "Missing material",
        "Why hypothesis generation is allowed or blocked",
    ],
    "Analysis lenses considered": [
        "Lens",
        "What it would inspect",
        "What it may miss",
        "Use decision",
    ],
    "Adopted analysis lenses": [
        "Primary lens",
        "Auxiliary lenses",
        "Reason",
    ],
    "Mechanistic analysis": [
        "Observation",
        "Analysis lens used",
        "Mechanistic interpretation",
        "Assumptions exposed",
        "What would be different if this interpretation is true",
    ],
    "Mechanism hypothesis record": [
        "Hypothesis",
        "Competing hypothesis",
        "Discriminating prediction",
        "Minimal test",
        "Required evidence",
        "Decision",
        "Reason",
    ],
}

PLACEHOLDER_PATTERNS = [
    re.compile(r"<[^>]+>"),
    re.compile(r"\bTODO\b", re.IGNORECASE),
    re.compile(r"\bTBD\b", re.IGNORECASE),
    re.compile(r"\{\{"),
]

DECISIONS = {"commit", "park", "kill"}


def extract_mechanism_section(text: str) -> str | None:
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if re.match(r"^##\s+Mechanism hypothesis record\s*$", line, flags=re.IGNORECASE):
            start = i + 1
            break
    if start is None:
        return None

    end = len(lines)
    for i in range(start, len(lines)):
        if re.match(r"^##\s+\S", lines[i]):
            end = i
            break
    return "\n".join(lines[start:end]).strip()


def extract_subsections(section: str) -> dict[str, str]:
    sections: dict[str, str] = {}
    current = None
    buffer: list[str] = []

    for line in section.splitlines():
        m = re.match(r"^###\s+(.+?)\s*$", line)
        if m:
            if current is not None:
                sections[current] = "\n".join(buffer).strip()
            current = m.group(1).strip()
            buffer = []
        elif current is not None:
            buffer.append(line)

    if current is not None:
        sections[current] = "\n".join(buffer).strip()
    return sections


def section_key(sections: dict[str, str], expected: str) -> str | None:
    for key in sections:
        if expected.lower() == key.lower():
            return key
    return None


def has_placeholder_only(body: str) -> bool:
    content_lines = [line.strip() for line in body.splitlines() if line.strip()]
    if not content_lines:
        return True
    return all(any(pattern.search(line) for pattern in PLACEHOLDER_PATTERNS) for line in content_lines)


def value_for_field(body: str, field: str) -> str | None:
    pattern = re.compile(rf"^\s*-\s*{re.escape(field)}\s*:\s*(.*?)\s*$", re.IGNORECASE | re.MULTILINE)
    match = pattern.search(body)
    if match:
        return match.group(1).strip()
    return None


def is_meaningful(value: str | None) -> bool:
    if value is None:
        return False
    stripped = value.strip()
    if not stripped:
        return False
    lowered = stripped.lower().strip(" .;:-")
    if lowered in {"none", "n/a", "na", "not applicable"}:
        return False
    return not any(pattern.search(stripped) for pattern in PLACEHOLDER_PATTERNS)


def check_required_subsections(sections: dict[str, str]) -> list[str]:
    issues: list[str] = []
    for expected in REQUIRED_SUBSECTIONS:
        key = section_key(sections, expected)
        if key is None:
            issues.append(f"  Missing required Mechanism hypothesis record subsection: '{expected}'")
            continue
        body = sections[key]
        if len(body.strip()) < 20 or has_placeholder_only(body):
            issues.append(f"  Mechanism hypothesis record subsection '{key}' is empty or placeholder-only")
    return issues


def check_fields(sections: dict[str, str]) -> list[str]:
    issues: list[str] = []
    for section, fields in SECTION_FIELDS.items():
        key = section_key(sections, section)
        if key is None:
            continue
        body = sections[key]
        for field in fields:
            value = value_for_field(body, field)
            if value is None:
                issues.append(f"  Section '{key}' missing required field: '{field}'")
            elif not is_meaningful(value):
                issues.append(f"  Section '{key}' field '{field}' is empty or placeholder-only")
    return issues


def check_decision(sections: dict[str, str]) -> list[str]:
    key = section_key(sections, "Mechanism hypothesis record")
    if key is None:
        return []

    issues: list[str] = []
    body = sections[key]
    decision = value_for_field(body, "Decision")
    if is_meaningful(decision):
        normalized = decision.strip().lower().strip(" .;")
        if normalized not in DECISIONS:
            issues.append("  Decision must be exactly one of: commit, park, kill")
    return issues


def check_blocked_commit(sections: dict[str, str]) -> list[str]:
    diagnosis_key = section_key(sections, "Research situation diagnosis")
    record_key = section_key(sections, "Mechanism hypothesis record")
    if diagnosis_key is None or record_key is None:
        return []

    diagnosis = sections[diagnosis_key].lower()
    decision = value_for_field(sections[record_key], "Decision")
    if decision and decision.strip().lower().strip(" .;") == "commit" and "blocked" in diagnosis:
        return ["  blocked diagnosis cannot commit"]
    return []


def check_record(text: str) -> list[str]:
    section = extract_mechanism_section(text)
    if section is None:
        return []

    lowered = section.lower()
    if "not applicable" in lowered and "objective" in lowered and "chosen" in lowered and "###" not in section:
        return []

    sections = extract_subsections(section)
    issues: list[str] = []
    issues.extend(check_required_subsections(sections))
    issues.extend(check_fields(sections))
    issues.extend(check_decision(sections))
    issues.extend(check_blocked_commit(sections))
    return issues


def main():
    parser = argparse.ArgumentParser(description="Verify a Mechanism hypothesis record against the research ideation contract.")
    parser.add_argument("path", help="Path to plan markdown file")
    args = parser.parse_args()

    p = Path(args.path).resolve()
    if not p.exists():
        print(f"Error: file not found: {p}", file=sys.stderr)
        sys.exit(1)

    text = p.read_text(encoding="utf-8")
    issues = check_record(text)

    print(f"Checking Mechanism hypothesis record: {p}")
    if issues:
        print(f"\n{len(issues)} issue(s):")
        for issue in issues:
            print(issue)
        sys.exit(1)

    print("Mechanism hypothesis record passes contract checks.")


if __name__ == "__main__":
    main()
