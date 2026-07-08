#!/usr/bin/env python3
"""Generate per-repo OWNERS and CONTRIBUTING.md from maintainers.yaml."""
import yaml
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
MAINTAINERS_FILE = SCRIPT_DIR / "maintainers.yaml"
CONTRIBUTING_TMPL = SCRIPT_DIR / "CONTRIBUTING.md"
GENERATED_DIR = SCRIPT_DIR / "generated"


ROLE_MAP = {"project-maintainers": "approvers", "reviewers": "reviewers"}


def gen_owners(teams):
    lines = []
    for team_name, role_name in ROLE_MAP.items():
        members = teams.get(team_name, [])
        if members:
            lines.append(f"{role_name}:")
            for m in members:
                lines.append(f"  - {m}")
    return "\n".join(lines) + "\n"


def main():
    with open(MAINTAINERS_FILE) as f:
        data = yaml.safe_load(f)

    contributing_tmpl = CONTRIBUTING_TMPL.read_text()
    GENERATED_DIR.mkdir(exist_ok=True)

    for entry in data.get("maintainers", []):
        repo = entry["project_id"]
        org = entry["org"]
        teams = {t["name"]: t.get("members", []) for t in entry.get("teams", [])}

        repo_dir = GENERATED_DIR / repo
        repo_dir.mkdir(exist_ok=True)
        (repo_dir / "OWNERS").write_text(gen_owners(teams))
        (repo_dir / "CONTRIBUTING.md").write_text(
            contributing_tmpl.replace("Project-HAMi/.project", f"{org}/{repo}")
        )

        counts = {role: len(teams.get(name, [])) for name, role in ROLE_MAP.items()}
        print(f"  {repo}: " + ", ".join(f"{r}={c}" for r, c in counts.items()))


if __name__ == "__main__":
    main()
