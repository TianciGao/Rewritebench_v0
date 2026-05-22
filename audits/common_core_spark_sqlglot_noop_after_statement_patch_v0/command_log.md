# Command Log

Preflight:

```bash
git status -sb
git branch --show-current
git log --oneline -5
tail -120 project_control/MIGRATION_RUN_LOG.md | sed -n '/spark_statement_boundary_comment_aware_patch_v0/,$p'
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

Result: PostgreSQL probe ok, MySQL probe ok, PySpark import available, `PYSPARK_PYTHON` set, `SQLRB_SPARK_MASTER` set, Spark backend live through PySpark.

Spark-only Common-core SQLGlot noop run:

```bash
source ~/code/sql-rewrite-bench/.venv/bin/activate
source scripts/env_postgres.local.sh
source scripts/env_mysql.local.sh
source scripts/env_spark.local.sh
export PYTHONPATH=src
python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --engine spark \
  --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route noop" \
  --out runs/user/common_core_spark_sqlglot_noop_after_statement_patch \
  --enable-db-execution \
  --enable-checker
```

Result: selected rows 40, candidate generated rows 40.

Summary extraction:

```bash
PYTHONPATH=src python - <<'PY'
from pathlib import Path
import csv, json
from collections import Counter
root = Path('runs/user/common_core_spark_sqlglot_noop_after_statement_patch')
rows = list(csv.DictReader((root / 'ledger.csv').open(newline='', encoding='utf-8')))
summary = json.loads((root / 'summary.json').read_text(encoding='utf-8'))
print(summary)
for field in ['candidate_generated','candidate_preflight_status','source_execution_status','candidate_execution_status','checker_status','exact_status','failure_bucket','diagnostic_mode']:
    print(field, dict(Counter(row[field] for row in rows)))
PY
```

No PostgreSQL engine snapshot, MySQL engine snapshot, SQLGlot optimize run, timing/speedup, official metrics, reports/results update, retained-evidence promotion, or leaderboard output was run.

Validation:

```bash
python - <<'PY'
from pathlib import Path
import csv, json
base = Path('audits/common_core_spark_sqlglot_noop_after_statement_patch_v0')
for csv_path in [base / 'aggregate_comparison.csv', base / 'affected_statement_rows.csv', base / 'remaining_failures.csv']:
    with csv_path.open(newline='', encoding='utf-8') as handle:
        assert list(csv.DictReader(handle))
json.loads((base / 'status_summary.json').read_text(encoding='utf-8'))
for md_path in base.glob('*.md'):
    assert md_path.read_text(encoding='utf-8').strip()
print('audit markdown/csv/json sanity passed')
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
