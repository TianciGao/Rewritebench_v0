# Command Log

Preflight commands:

```bash
git status -sb
git branch --show-current
git log --oneline -15
```

Context and inventory commands:

```bash
sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md
sed -n '1,260p' project_control/MIGRATION_STATUS.md
sed -n '1,220p' project_control/DECISION_LOG.md
tail -n 240 project_control/MIGRATION_RUN_LOG.md
sed -n '1,260p' project_control/USER_ENTRY_LOCAL_EVALUATION_ARCHITECTURE_PLAN.md
sed -n '1,240p' project_control/PORT_CROSS_DIALECT_DIAGNOSTIC_EXECUTION_PLAN.md
sed -n '1,180p' audits/user_entry_pg_mysql_local_diagnostic_closeout_v0/README.md
sed -n '1,180p' audits/user_entry_pg_mysql_bounded_local_diagnostic_rerun_v0/README.md
sed -n '1,180p' audits/mysql_same_engine_backend_v0/README.md
sed -n '1,180p' audits/port_bidirectional_cross_dialect_closeout_v0/README.md
sed -n '1,180p' audits/port_target_engine_role_mapping_v0/README.md
rg -n "spark|Spark|unsupported|fail|ExecutionResult|source_result|candidate_result|schema|engine_roles|diagnostic_mode|failure_bucket|checker|tag_slices|quality_summary" src/sql_rewrite_bench/user_run.py src/sql_rewrite_bench/engine_execution.py src/sql_rewrite_bench/postgres_execution.py src/sql_rewrite_bench/mysql_execution.py src/sql_rewrite_bench/spark_execution.py src/sql_rewrite_bench/local_result_checker.py src/sql_rewrite_bench/case_package_resolver.py src/sql_rewrite_bench/user_ledger.py src/sql_rewrite_bench/user_quality_report.py src/sql_rewrite_bench/tag_slices.py
sed -n '1,260p' docs/LOCAL_ENGINE_SETUP.md
sed -n '1,220p' scripts/env_spark.example.sh
sed -n '1,220p' scripts/env_all.example.sh
rg -n "Spark|SPARK|spark" scripts/dev/check_local_engine_env.py
find schemas -path '*/spark/*' -maxdepth 4 -type f | sort
```

Observed inventory:

- Current `spark_execution.py` is an explicit fail-closed stub and does not execute SQL.
- Representative Common-core manifests point to external profiles that include `engines.spark.ddl` and `engines.spark.load` assets.
- All 9 Common-core PORT manifests declare `local_diagnostic.engine_roles.spark` as unsupported/manual-review.
- Current engine setup docs say `SPARK_LOCAL_IP` is a placeholder only and does not enable Spark execution.

Validation commands:

```bash
git diff --check

python - <<'PY'
import csv
from pathlib import Path
root = Path('audits/spark_backend_design_v0')
for p in sorted(root.glob('*.csv')):
    with p.open(newline='', encoding='utf-8') as f:
        list(csv.DictReader(f))
for p in sorted(root.glob('*.md')):
    text = p.read_text(encoding='utf-8')
    assert text.startswith('#')
    assert '\r' not in text
PY

python - <<'PY'
import subprocess
allowed = (
    'audits/spark_backend_design_v0/',
    'project_control/MIGRATION_STATUS.md',
    'project_control/MIGRATION_RUN_LOG.md',
)
lines = subprocess.check_output(['git', 'status', '--short'], text=True).splitlines()
paths = [line[3:] for line in lines]
bad = [p for p in paths if not any(p == a or p.startswith(a) for a in allowed)]
assert not bad, bad
PY

git status --short -- runs/user
```

Validation result:

- Diff whitespace check: passed.
- CSV parse checks: passed.
- Markdown sanity checks: passed.
- Protected-surface check: passed.
- Local run outputs created or committed: no.
