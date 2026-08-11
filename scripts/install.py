#!/usr/bin/env python3
"""Safely install the Pen Design Skills suite without overwriting destinations."""

import argparse
import json
import shutil
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
SOURCE_ROOT = REPO_ROOT / "skills"
MANIFEST = REPO_ROOT / "manifest.json"


def load_skill_names():
    with MANIFEST.open(encoding="utf-8") as handle:
        data = json.load(handle)
    return [entry["name"] for entry in data["skills"]]


def validate_destination(destination):
    unresolved = destination.expanduser()
    if unresolved.exists() and unresolved.is_symlink():
        raise SystemExit(f"Refusing symlink destination: {unresolved}")
    resolved = unresolved.resolve()
    home = Path.home().resolve()
    unsafe = {Path("/"), home, REPO_ROOT.resolve(), SOURCE_ROOT.resolve()}
    if resolved in unsafe:
        raise SystemExit(f"Refusing unsafe destination: {resolved}")
    return resolved


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dest", required=True, type=Path, help="Exact destination skills directory")
    parser.add_argument("--apply", action="store_true", help="Copy after validation; default is dry-run")
    args = parser.parse_args()

    destination = validate_destination(args.dest)
    skills = load_skill_names()
    missing_sources = [name for name in skills if not (SOURCE_ROOT / name / "SKILL.md").is_file()]
    if missing_sources:
        raise SystemExit(f"Missing source skills: {', '.join(missing_sources)}")

    conflicts = [name for name in skills if (destination / name).exists()]
    if conflicts:
        raise SystemExit(f"Destination already contains: {', '.join(conflicts)}")

    print(f"Source: {SOURCE_ROOT}")
    print(f"Destination: {destination}")
    for name in skills:
        print(f"  {name}")

    if not args.apply:
        print("Dry-run only. Add --apply to copy the suite.")
        return

    destination.mkdir(parents=True, exist_ok=True)
    for name in skills:
        shutil.copytree(SOURCE_ROOT / name, destination / name)
    print(f"Installed {len(skills)} skills without overwriting existing directories.")


if __name__ == "__main__":
    main()
