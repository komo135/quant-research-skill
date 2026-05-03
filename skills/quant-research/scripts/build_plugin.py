"""build_plugin.py — Sync skills/quant-research/ → plugins/quant-research/skills/quant-research/.

Per D-13 (`.rebuild/DECISIONS.md`): the source-of-truth is `skills/quant-research/`;
the plugin distribution at `plugins/quant-research/skills/quant-research/` must
be kept in sync via this script (or via CI drift detection in `--check` mode).

Usage:
    # Build (copy source → plugin/)
    python scripts/build_plugin.py [--repo-root <path>]

    # Check (CI drift detection: exit 1 if source ≠ plugin/)
    python scripts/build_plugin.py --check

Exit codes:
    0: success (build completed OR check found no drift)
    1: drift detected (in --check mode)
    2: setup error (paths invalid)
"""

from __future__ import annotations

import argparse
import filecmp
import hashlib
import shutil
import sys
from pathlib import Path

CHUNK = 65536

# Paths relative to repo root
SOURCE_REL = Path("skills/quant-research")
PLUGIN_REL = Path("plugins/quant-research/skills/quant-research")

# Top-level entries to sync (relative to SOURCE_REL)
SYNC_DIRS = ("references", "assets", "scripts")
SYNC_FILES = ("SKILL.md",)

# Skip patterns (do not copy / not part of source-of-truth comparison)
SKIP_NAMES = {"__pycache__", ".pytest_cache", ".DS_Store"}


def compute_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(CHUNK), b""):
            h.update(chunk)
    return h.hexdigest()


def list_tree(root: Path) -> dict[str, str]:
    """Walk a directory tree and return {relative_path: sha256} for all files."""
    out: dict[str, str] = {}
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if any(part in SKIP_NAMES for part in p.parts):
            continue
        rel = p.relative_to(root).as_posix()
        out[rel] = compute_sha256(p)
    return out


def find_repo_root(start: Path | None = None) -> Path:
    """Find the repo root by looking for SKILL.md / plugins/ siblings.

    Defaults to walking up from this script's location.
    """
    if start is None:
        start = Path(__file__).resolve()
    cur = start.parent
    while cur != cur.parent:
        if (cur / "skills").is_dir() and (cur / "plugins").is_dir():
            return cur
        cur = cur.parent
    raise FileNotFoundError(
        "could not find repo root (looking for sibling 'skills/' and 'plugins/')"
    )


def build(repo_root: Path) -> None:
    """Copy source → plugin destination."""
    source = repo_root / SOURCE_REL
    dest = repo_root / PLUGIN_REL
    if not source.exists():
        raise FileNotFoundError(f"source not found: {source}")

    dest.mkdir(parents=True, exist_ok=True)

    # Top-level files
    for name in SYNC_FILES:
        src = source / name
        if src.exists():
            shutil.copy2(src, dest / name)
            print(f"copy: {name}")

    # Subdirectories (full tree replace)
    for sub in SYNC_DIRS:
        src_dir = source / sub
        dst_dir = dest / sub
        if not src_dir.exists():
            continue
        if dst_dir.exists():
            shutil.rmtree(dst_dir)
        shutil.copytree(src_dir, dst_dir, ignore=shutil.ignore_patterns(*SKIP_NAMES))
        n_files = sum(1 for _ in dst_dir.rglob("*") if _.is_file())
        print(f"copy: {sub}/ ({n_files} files)")


def check_drift(repo_root: Path) -> list[str]:
    """Return list of drift descriptions; empty if no drift."""
    source = repo_root / SOURCE_REL
    dest = repo_root / PLUGIN_REL
    if not source.exists():
        return [f"ERROR: source not found: {source}"]
    if not dest.exists():
        return [f"DRIFT: plugin destination does not exist: {dest}"]

    drifts: list[str] = []

    # Compare top-level files
    for name in SYNC_FILES:
        s = source / name
        d = dest / name
        if not s.exists() and d.exists():
            drifts.append(f"plugin has {name} but source does not")
            continue
        if s.exists() and not d.exists():
            drifts.append(f"source has {name} but plugin does not")
            continue
        if s.exists() and d.exists():
            if compute_sha256(s) != compute_sha256(d):
                drifts.append(f"hash mismatch: {name}")

    # Compare subdirectory trees
    for sub in SYNC_DIRS:
        src_dir = source / sub
        dst_dir = dest / sub
        src_tree = list_tree(src_dir) if src_dir.exists() else {}
        dst_tree = list_tree(dst_dir) if dst_dir.exists() else {}

        only_src = set(src_tree) - set(dst_tree)
        only_dst = set(dst_tree) - set(src_tree)
        common = set(src_tree) & set(dst_tree)

        for f in sorted(only_src):
            drifts.append(f"in source only: {sub}/{f}")
        for f in sorted(only_dst):
            drifts.append(f"in plugin only: {sub}/{f}")
        for f in sorted(common):
            if src_tree[f] != dst_tree[f]:
                drifts.append(f"hash mismatch: {sub}/{f}")

    return drifts


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--repo-root", type=Path, default=None,
                   help="repo root containing skills/ and plugins/ (auto-detected if omitted)")
    p.add_argument("--check", action="store_true",
                   help="check for drift only (CI mode); exit 1 if drift")
    args = p.parse_args()

    try:
        repo_root = args.repo_root.resolve() if args.repo_root else find_repo_root()
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(2)

    print(f"repo_root: {repo_root}")

    if args.check:
        drifts = check_drift(repo_root)
        if not drifts:
            print(f"\n✅ No drift between {SOURCE_REL} and {PLUGIN_REL}")
            sys.exit(0)
        print(f"\n🔴 Drift detected ({len(drifts)} entries):")
        for d in drifts:
            print(f"  - {d}")
        print(f"\nRun without --check to sync source → plugin.")
        sys.exit(1)

    print(f"Building: {SOURCE_REL} → {PLUGIN_REL}")
    try:
        build(repo_root)
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(2)

    # Verify post-build
    drifts = check_drift(repo_root)
    if drifts:
        print(f"\n⚠️  Post-build drift detected ({len(drifts)} entries):")
        for d in drifts[:10]:
            print(f"  - {d}")
        sys.exit(1)
    print("\n✅ Build complete; no drift.")


if __name__ == "__main__":
    main()
