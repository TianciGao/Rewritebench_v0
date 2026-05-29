# Command Log

Preflight:

```bash
git status -sb
git branch --show-current
git log --oneline -12
rg -n "spark_sqlglot_noop_statement_preflight_triage_v0|4d9f392" project_control/MIGRATION_STATUS.md project_control/MIGRATION_RUN_LOG.md audits/spark_sqlglot_noop_statement_preflight_triage_v0 -g '*'
```

Required context/code reads:

```bash
sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md
tail -100 project_control/MIGRATION_STATUS.md
tail -140 project_control/MIGRATION_RUN_LOG.md
sed -n '1,220p' project_control/DECISION_LOG.md
sed -n '1,260p' project_control/USER_ENTRY_LOCAL_EVALUATION_ARCHITECTURE_PLAN.md
sed -n '1,220p' audits/spark_sqlglot_noop_statement_preflight_triage_v0/README.md
sed -n '1,120p' audits/spark_sqlglot_noop_statement_preflight_triage_v0/root_cause_matrix.csv
sed -n '1,120p' audits/spark_sqlglot_noop_statement_preflight_triage_v0/recommendation.md
sed -n '1,220p' audits/common_core_sqlglot_noop_failure_triage_v0/README.md
sed -n '1,80p' audits/common_core_sqlglot_noop_failure_triage_v0/failure_triage_matrix.csv
sed -n '1,220p' audits/common_core_tri_engine_sqlglot_noop_local_diagnostic_snapshot_v0/README.md
sed -n '1,220p' audits/common_core_tri_engine_sqlglot_noop_local_diagnostic_snapshot_v0/status_summary.json
sed -n '1,270p' src/sql_rewrite_bench/candidate_preflight.py
sed -n '250,315p' src/sql_rewrite_bench/spark_execution.py
sed -n '1,260p' tests/user_entry/test_candidate_preflight.py
```

Environment check:

```bash
source ~/code/sql-rewrite-bench/.venv/bin/activate
source scripts/env_postgres.local.sh
source scripts/env_mysql.local.sh
source scripts/env_spark.local.sh
export PYTHONPATH=src
python scripts/dev/check_local_engine_env.py
```

Result: PostgreSQL probe ok, MySQL probe ok, PySpark import available, Spark backend status live local diagnostic backend available through PySpark.

Focused tests and local diagnostics:

```bash
PYTHONPATH=src pytest tests/user_entry/test_candidate_preflight.py -q
PYTHONPATH=src pytest tests/user_entry -q
PYTHONPATH=src python -m py_compile src/sql_rewrite_bench/candidate_preflight.py src/sql_rewrite_bench/spark_execution.py tests/user_entry/test_candidate_preflight.py
```

Affected-row rerun:

```bash
printf 'PERF_0008\nPERF_0013\nPERF_0017\nPERF_0019\nPERF_0024\nPERF_0082\n' > /tmp/sqlrb_spark_statement_boundary_cases.txt
PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --engine spark \
  --case-list /tmp/sqlrb_spark_statement_boundary_cases.txt \
  --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route noop" \
  --out runs/user/spark_sqlglot_noop_statement_boundary_after_patch \
  --enable-db-execution \
  --enable-checker
```

Result: selected 6, generated 6, source executable 6, candidate executable 6, checker attempted 6, exact 6, mismatch 0.

Spark smoke:

```bash
printf 'PERF_0006\nCONS_0005\n' > /tmp/sqlrb_spark_statement_boundary_smoke.txt
PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --engine spark \
  --case-list /tmp/sqlrb_spark_statement_boundary_smoke.txt \
  --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route noop" \
  --out runs/user/spark_sqlglot_noop_two_case_smoke_after_statement_patch \
  --enable-db-execution \
  --enable-checker
```

Result: selected 2, generated 2, source executable 2, candidate executable 2, checker attempted 2, exact 2, mismatch 0.

Final validation:

```bash
python - <<'PY'
from pathlib import Path
import csv
base = Path('audits/spark_statement_boundary_comment_aware_patch_v0')
for csv_path in [base / 'affected_rows_before_after.csv']:
    with csv_path.open(newline='', encoding='utf-8') as handle:
        assert list(csv.DictReader(handle))
for md_path in base.glob('*.md'):
    assert md_path.read_text(encoding='utf-8').strip()
print('audit markdown/csv sanity passed')
PY
python - <<'PY'
from pathlib import Path
for path in ['project_control/MIGRATION_STATUS.md', 'project_control/MIGRATION_RUN_LOG.md']:
    assert Path(path).read_text(encoding='utf-8').strip()
print('project-control readable')
PY
git diff --check
git diff --name-only
git status -sb
```
