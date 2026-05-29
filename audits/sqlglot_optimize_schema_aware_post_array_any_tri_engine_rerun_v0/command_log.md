# Command Log

Commands run for this task:

```bash
git status -sb
git branch --show-current
git fetch origin main feature/case-package-v2-external-schema
git merge-base --is-ancestor 2bc11d08352dff4c81f6bff9852795ebfa1c16a1 HEAD
git show origin/main:project_control/MIGRATION_MASTER_PLAN.md
git show origin/main:project_control/MIGRATION_STATUS.md
git show origin/main:project_control/DECISION_LOG.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_MASTER_PLAN.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_STATUS.md
git show origin/feature/case-package-v2-external-schema:project_control/DECISION_LOG.md
test -d audits/sqlglot_optimize_schema_aware_bounded_tri_engine_execution_checker_v0
test -d audits/sqlglot_optimize_schema_aware_bounded_tri_engine_blocker_triage_v0
test -d audits/sqlglot_optimize_schema_aware_mysql_array_any_fail_closed_v0
test -d baselines/sqlglot
git status --porcelain -- runs/user output reports results
psql --version
mysql --version
python - <<'PY'
import pyspark
print("pyspark_available=true")
PY
PYTHONPATH=src python audits/sqlglot_optimize_schema_aware_post_array_any_tri_engine_rerun_v0/run_post_guard_execution_checker.py
python -m json.tool audits/sqlglot_optimize_schema_aware_post_array_any_tri_engine_rerun_v0/diagnostic_summary.json
python -m py_compile audits/sqlglot_optimize_schema_aware_post_array_any_tri_engine_rerun_v0/run_post_guard_execution_checker.py
pytest tests/user_entry/test_sqlglot_adapter.py tests/user_entry/test_local_timing.py -q
python - <<'PY'
import csv, json
from pathlib import Path
root = Path('audits/sqlglot_optimize_schema_aware_post_array_any_tri_engine_rerun_v0')
with (root / 'per_row_execution_checker_status.csv').open(newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))
assert len(rows) == 9
summary = json.loads((root / 'diagnostic_summary.json').read_text(encoding='utf-8'))
assert summary['planned_rows'] == 9
assert summary['fail_closed_rows'] == 1
assert summary['candidate_execution_failed_rows'] == 0
assert summary['exact_rows'] == 6
assert summary['mismatch_rows'] == 2
assert summary['cons0005_mysql_fail_closed'] is True
PY
git diff --check
git status --porcelain -- runs/user output reports results
git status -sb
```

Validation results:

- CSV/JSON/Markdown validation passed.
- `python -m py_compile` for the audit helper passed.
- Focused SQLGlot tests passed: 21 passed, 1 skipped.
- `git diff --check` passed.
- Protected path status checks produced no `runs/user`, repository-level `output`, top-level `reports`, or top-level `results` artifacts.

Runtime output root:

- `/tmp/sqlrb_sqlglot_optimize_schema_aware_post_array_any_tri_engine_rerun_v0/`
