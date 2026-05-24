# Command Log

Preflight and environment:

```bash
git status -sb
git fetch origin main feature/case-package-v2-external-schema
git merge-base --is-ancestor 81ec6b347c22a13ed710b548d95a9da3770ebe8d HEAD
git show origin/main:project_control/MIGRATION_MASTER_PLAN.md
git show origin/main:project_control/MIGRATION_STATUS.md
git show origin/main:project_control/DECISION_LOG.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_MASTER_PLAN.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_STATUS.md
git show origin/feature/case-package-v2-external-schema:project_control/DECISION_LOG.md
curl -s https://api.github.com/repos/TianciGao/Rewritebench_v0/actions/runs?branch=feature/case-package-v2-external-schema
psql --version
mysql --version
python - <<'PY'
import pyspark
print("pyspark_available=true")
PY
```

Diagnostic run:

```bash
PYTHONPATH=src python audits/sqlglot_optimize_schema_aware_track_a_120_execution_checker_diagnostic_v0/run_track_a_120_checker.py
```

Artifact validation:

```bash
python - <<'PY'
import csv, json
from pathlib import Path
root = Path("audits/sqlglot_optimize_schema_aware_track_a_120_execution_checker_diagnostic_v0")
rows = list(csv.DictReader((root / "per_row_execution_checker_status.csv").open()))
assert len(rows) == 120
json.loads((root / "diagnostic_summary.json").read_text())
json.loads((root / "route_card.json").read_text())
route_rows = list(csv.DictReader((root / "route_card.csv").open()))
assert len(route_rows) == 1
PY
```

Focused validation:

```bash
pytest tests/user_entry/test_sqlglot_adapter.py tests/user_entry/test_local_timing.py -q
# 21 passed, 1 skipped

git diff --check
git status -sb
git status --porcelain -- runs/user output reports results src tests baselines cases case_sets schemas inventory
find audits/sqlglot_optimize_schema_aware_track_a_120_execution_checker_diagnostic_v0 -type d -name __pycache__ -print
```
