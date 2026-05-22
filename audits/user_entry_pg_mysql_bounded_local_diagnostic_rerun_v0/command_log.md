# Command Log

Preflight commands:

```bash
git status -sb
git branch --show-current
git log --oneline -15
source scripts/env_mysql.local.sh && source scripts/env_postgres.local.sh && python scripts/dev/check_local_engine_env.py
```

Context read commands:

```bash
sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md
sed -n '1,260p' project_control/MIGRATION_STATUS.md
sed -n '1,220p' project_control/DECISION_LOG.md
tail -n 220 project_control/MIGRATION_RUN_LOG.md
sed -n '1,240p' project_control/USER_ENTRY_LOCAL_EVALUATION_ARCHITECTURE_PLAN.md
sed -n '1,240p' project_control/PORT_CROSS_DIALECT_DIAGNOSTIC_EXECUTION_PLAN.md
sed -n '1,180p' audits/user_entry_pg_mysql_local_diagnostic_closeout_v0/README.md
sed -n '1,180p' audits/user_entry_common_core_pg_local_diagnostic_v0/README.md
sed -n '1,180p' audits/common_core_mysql_local_diagnostic_v0/README.md
sed -n '1,180p' audits/mysql_same_engine_backend_v0/README.md
sed -n '1,180p' audits/port_bidirectional_cross_dialect_closeout_v0/README.md
sed -n '1,180p' audits/port_target_engine_role_mapping_v0/README.md
sed -n '1,180p' audits/port_reverse_cross_dialect_mysql_target_diagnostic_v0/README.md
sed -n '1,180p' audits/port_cross_dialect_checker_normalization_v0/README.md
rg -n "diagnostic_mode|engine_roles|cross_dialect|source_reference|target_candidate|quality_summary|tag_slices|failure_bucket|source_like" src/sql_rewrite_bench/user_run.py src/sql_rewrite_bench/engine_execution.py src/sql_rewrite_bench/postgres_execution.py src/sql_rewrite_bench/mysql_execution.py src/sql_rewrite_bench/spark_execution.py src/sql_rewrite_bench/local_result_checker.py src/sql_rewrite_bench/user_ledger.py src/sql_rewrite_bench/user_quality_report.py src/sql_rewrite_bench/tag_slices.py examples/user/noop_adapter.py
```

Diagnostic run commands:

```bash
source scripts/env_mysql.local.sh && source scripts/env_postgres.local.sh && PYTHONPATH=src python -m sql_rewrite_bench.user_run   --case-set common_core_v0   --engine postgres   --adapter-command "python examples/user/noop_adapter.py"   --out runs/user/bounded_pg_noop_db_checker_current   --enable-db-execution   --enable-checker

source scripts/env_mysql.local.sh && source scripts/env_postgres.local.sh && PYTHONPATH=src python -m sql_rewrite_bench.user_run   --case-set common_core_v0   --engine mysql   --adapter-command "python examples/user/noop_adapter.py"   --out runs/user/bounded_mysql_noop_db_checker_current   --enable-db-execution   --enable-checker
```

Observed run completion:

- PostgreSQL: `selected_rows=40`, `candidate_generated_rows=40`.
- MySQL: `selected_rows=40`, `candidate_generated_rows=40`.

Validation commands will be appended after final checks.

Cleanup command:

```bash
rm -rf runs/user/bounded_pg_noop_db_checker_current runs/user/bounded_mysql_noop_db_checker_current
```

Validation commands:

```bash
git diff --check

python - <<'PY'
import csv,json
from pathlib import Path
root=Path('audits/user_entry_pg_mysql_bounded_local_diagnostic_rerun_v0')
for p in sorted(root.glob('*.json')):
    json.loads(p.read_text())
for p in sorted(root.glob('*.csv')):
    list(csv.DictReader(p.open(newline='')))
for p in sorted(root.glob('*.md')):
    text=p.read_text()
    assert text.startswith('#')
    assert '\r' not in text
PY

python - <<'PY'
from pathlib import Path
import subprocess
allowed_prefixes=(
    'audits/user_entry_pg_mysql_bounded_local_diagnostic_rerun_v0/',
    'project_control/MIGRATION_STATUS.md',
    'project_control/MIGRATION_RUN_LOG.md',
)
changed=subprocess.check_output(['git','status','--short'], text=True).splitlines()
paths=[line[3:] for line in changed]
bad=[p for p in paths if not any(p == pref or p.startswith(pref) for pref in allowed_prefixes)]
assert not bad, bad
PY

git status --short -- runs/user/bounded_pg_noop_db_checker_current runs/user/bounded_mysql_noop_db_checker_current
```

Validation result:

- Diff whitespace check: passed.
- CSV/JSON parse checks: passed.
- Markdown sanity checks: passed.
- Protected-surface check: passed.
- Local run outputs committed: no.
