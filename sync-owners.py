#!/usr/bin/env python3
"""Generate per-repo OWNERS files from maintainers.yaml."""
import yaml
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
MAINTAINERS_FILE = SCRIPT_DIR / "maintainers.yaml"
GENERATED_DIR = SCRIPT_DIR / "generated"


def gen_owners(entry):
    lines = []
    teams = {t["name"]: t.get("members", []) for t in entry.get("teams", [])}

    approvers = teams.get("project-maintainers", [])
    reviewers = teams.get("reviewers", [])

    if approvers:
        lines.append("approvers:")
        for a in approvers:
            lines.append(f"  - {a}")
    if reviewers:
        lines.append("reviewers:")
        for r in reviewers:
            lines.append(f"  - {r}")
    return "\n".join(lines) + "\n"


def main():
    with open(MAINTAINERS_FILE) as f:
        data = yaml.safe_load(f)

    GENERATED_DIR.mkdir(exist_ok=True)

    for entry in data.get("maintainers", []):
        repo = entry["project_id"]
        repo_dir = GENERATED_DIR / repo
        repo_dir.mkdir(exist_ok=True)
        owners_file = repo_dir / "OWNERS"
        owners_file.write_text(gen_owners(entry))
        print(f"  {repo}: maintainers={len(entry['teams'][0].get('members',[]))}, reviewers={len(entry['teams'][1].get('members',[])) if len(entry['teams'])>1 else 0}")


if __name__ == "__main__":
    main()
