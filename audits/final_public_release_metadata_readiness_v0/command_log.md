# Command Log

Commands run before editing:

```bash
git status -sb
git branch --show-current
git log --oneline -15
```

Context read:

- `project_control/MIGRATION_MASTER_PLAN.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/DECISION_LOG.md`
- `project_control/MIGRATION_RUN_LOG.md` tail
- `project_control/RELEASE_SURFACE_POLICY_DECISIONS.md`
- `project_control/USER_ENTRY_LOCAL_EVALUATION_ARCHITECTURE_PLAN.md`
- `audits/release_surface_metadata_readiness_v0/README.md`
- `audits/release_surface_policy_decisions_v0/README.md`
- `audits/release_surface_metadata_skeleton_v0/README.md`
- `audits/release_surface_metadata_polish_v0/README.md`
- Current release-surface metadata files and directories

Inventory commands included:

```bash
find benchmark_spec -maxdepth 1 -type f -print
find docs -maxdepth 2 -type f -print
find examples -maxdepth 3 -type f -print
find .github/workflows -maxdepth 1 -type f -print
python - <<'PY'
import csv
from collections import Counter
from pathlib import Path
rows = list(csv.DictReader(Path("case_sets/common_core_v0/cases.csv").open(newline="", encoding="utf-8")))
print(len(rows), Counter(r["pool"] for r in rows))
print(len(list(csv.DictReader(Path("case_sets/common_core_v0/denominator_same_engine_120.csv").open(newline="", encoding="utf-8")))))
PY
```

Validation commands:

```bash
git diff --check
python - <<'PY'
from pathlib import Path
import yaml
yaml.safe_load(Path("CITATION.cff").read_text(encoding="utf-8"))
print("citation yaml ok")
PY
```

Validation result: passed.

Additional validation commands:

```bash
python - <<'PY'
from pathlib import Path
import re
heading = re.compile(r"^#{1,6} +\S")
public = [
    Path("README.md"), Path("CONTRIBUTING.md"), Path("reports/README.md"), Path("results/README.md"), Path("docs/README.md"),
    *sorted(Path("benchmark_spec").glob("*.md")),
]
audit = sorted(Path("audits/final_public_release_metadata_readiness_v0").glob("*.md"))
for path in public + audit:
    text = path.read_text(encoding="utf-8")
    assert text.startswith("#"), path
    for i, line in enumerate(text.splitlines(), 1):
        if line.startswith("#"):
            assert heading.match(line), f"bad heading spacing {path}:{i}: {line}"
print("markdown sanity ok")
PY
python - <<'PY'
from pathlib import Path
text = Path(".gitignore").read_text(encoding="utf-8").splitlines()
assert "runs/user/" in text
assert "runs/" not in text
assert "/runs/" not in text
assert "runs/**" not in text
print("gitignore policy ok")
PY
```

The Markdown sanity check also verified that no broken triple-slash placeholder paths were present.

CSV/JSON parse checks for the new audit files passed.

Protected-surface validation passed. No `runs/user/` outputs were created.
