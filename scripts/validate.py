#!/usr/bin/env python3
"""Static integrity checks for the Pen Design Skills suite and Chinese evals."""

import json
import re
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent
SKILLS_ROOT = REPO_ROOT / "skills"
MANIFEST_PATH = REPO_ROOT / "manifest.json"
EVALS_PATH = REPO_ROOT / "evals" / "pen-command-suite.json"
EXPECTED_SKILLS = {
    "ask-pen",
    "pen-system",
    "pen-component",
    "pen-page",
    "pen-review",
    "pen-polish",
    "pen-sync-code",
    "pen-design-core",
}
EXPECTED_COMMANDS = {
    "pen-system",
    "pen-component",
    "pen-page",
    "pen-review",
    "pen-polish",
    "pen-sync-code",
}
EXPECTED_REFERENCES = {
    "interview.md",
    "workflow.md",
    "reuse-and-context.md",
    "execution-and-recovery.md",
    "quality.md",
    "design-code.md",
}


def main():
    errors = []
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    evals = json.loads(EVALS_PATH.read_text(encoding="utf-8"))
    entries = {item["name"]: item for item in manifest["skills"]}

    if set(entries) != EXPECTED_SKILLS:
        errors.append(f"manifest: skill set mismatch {sorted(entries)}")

    for name, entry in entries.items():
        folder = SKILLS_ROOT / name
        skill_file = folder / "SKILL.md"
        ui_file = folder / "agents" / "openai.yaml"
        if not skill_file.is_file():
            errors.append(f"{name}: missing SKILL.md")
            continue
        text = skill_file.read_text(encoding="utf-8")
        match = re.search(r"(?m)^name:\s*([^\s]+)\s*$", text)
        if not match or match.group(1) != name:
            errors.append(f"{name}: frontmatter name mismatch")
        if not re.search(r"(?m)^description:\s*.+$", text):
            errors.append(f"{name}: missing description")
        if not ui_file.is_file():
            errors.append(f"{name}: missing agents/openai.yaml")
        else:
            ui = ui_file.read_text(encoding="utf-8")
            expected = "true" if entry["invocation"] == "implicit" else "false"
            if f"allow_implicit_invocation: {expected}" not in ui:
                errors.append(f"{name}: invocation policy should be {expected}")
        for dependency in entry["depends_on"]:
            if dependency not in entries:
                errors.append(f"{name}: unknown dependency {dependency}")

    core = SKILLS_ROOT / "pen-design-core"
    core_text = (core / "SKILL.md").read_text(encoding="utf-8")
    actual_refs = {path.name for path in (core / "references").glob("*.md")}
    if actual_refs != EXPECTED_REFERENCES:
        errors.append(f"pen-design-core: reference set mismatch {sorted(actual_refs)}")
    for reference in EXPECTED_REFERENCES:
        if f"references/{reference}" not in core_text:
            errors.append(f"pen-design-core: missing pointer to {reference}")
    if not (core / "scripts" / "audit_pen.py").is_file():
        errors.append("pen-design-core: missing audit_pen.py")

    review_text = (SKILLS_ROOT / "pen-review" / "SKILL.md").read_text(encoding="utf-8").lower()
    if "read-only" not in review_text or "不修改" not in review_text:
        errors.append("pen-review: read-only boundary is not explicit")

    cases = evals.get("cases", [])
    commands = {case.get("command") for case in cases}
    if len(cases) != 6 or commands != EXPECTED_COMMANDS:
        errors.append("evals: expected exactly one primary case for each command")
    for case in cases:
        for field in ("id", "command", "prompt", "must", "must_not"):
            if not case.get(field):
                errors.append(f"evals: {case.get('id', '(unknown)')} missing {field}")

    for required in (
        REPO_ROOT / "README.md",
        REPO_ROOT / "scripts" / "install.py",
        REPO_ROOT / "evals" / "forward-test-protocol.md",
    ):
        if not required.is_file():
            errors.append(f"missing repository file: {required.relative_to(REPO_ROOT)}")

    if errors:
        for error in errors:
            print(f"FAIL {error}")
        raise SystemExit(1)
    print(
        f"PASS {len(entries)} skills · "
        f"{len(EXPECTED_REFERENCES)} references · "
        f"{len(cases)} Chinese eval cases"
    )


if __name__ == "__main__":
    main()
