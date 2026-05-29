# Command Log

Initial repository and environment checks:

```bash
git status -sb
git branch --show-current
git log --oneline -12
set -a; [ -f scripts/env_mysql.local.sh ] && source scripts/env_mysql.local.sh; [ -f scripts/env_postgres.local.sh ] && source scripts/env_postgres.local.sh; set +a; python scripts/dev/check_local_engine_env.py
```

Context and implementation inspection included the required project-control documents, recent MySQL/PORT/local-diagnostic audit packets, and implementation files under `src/sql_rewrite_bench/` plus `tests/user_entry/`.

Validation commands run during implementation:

```bash
PYTHONPATH=src python -m py_compile src/sql_rewrite_bench/mysql_execution.py src/sql_rewrite_bench/engine_execution.py src/sql_rewrite_bench/user_run.py src/sql_rewrite_bench/user_ledger.py src/sql_rewrite_bench/user_run_schema.py
PATH=/tmp/sqlrb_pytest_venv/bin:$PATH PYTHONPATH=src pytest tests/user_entry/test_mysql_source_reference_backend.py tests/user_entry/test_engine_execution_router.py tests/user_entry/test_cross_dialect_checker_normalization.py
PATH=/tmp/sqlrb_pytest_venv/bin:$PATH PYTHONPATH=src pytest tests/user_entry
PYTHONPATH=src python -m sql_rewrite_bench.user_run --help
python scripts/user/run_user_benchmark.py --help
PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --list-cases
PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --engine mysql --smoke --explain-selection
PYTHONPATH=src python -m sql_rewrite_bench.user_run --show-output-schema
```

Live MySQL same-engine smoke:

```bash
rm -rf runs/user/mysql_same_engine_smoke
set -a; [ -f scripts/env_mysql.local.sh ] && source scripts/env_mysql.local.sh; [ -f scripts/env_postgres.local.sh ] && source scripts/env_postgres.local.sh; set +a; PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --engine mysql --smoke --adapter-command "python examples/user/noop_adapter.py" --out runs/user/mysql_same_engine_smoke --enable-db-execution --enable-checker
```

PORT cross-dialect regression:

```bash
cat > /tmp/sqlrb_port_cross_dialect_cases.txt <<'EOF'
PORT_0004
PORT_0013
PORT_0022
PORT_0024
PORT_0025
EOF
rm -rf runs/user/port_pg_target_reference_normalized_regression
set -a; [ -f scripts/env_mysql.local.sh ] && source scripts/env_mysql.local.sh; [ -f scripts/env_postgres.local.sh ] && source scripts/env_postgres.local.sh; set +a; PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --engine postgres --case-list /tmp/sqlrb_port_cross_dialect_cases.txt --adapter-command "python examples/user/port_postgres_target_reference_adapter.py" --out runs/user/port_pg_target_reference_normalized_regression --enable-db-execution --enable-checker
```

PostgreSQL behavior preservation:

```bash
rm -rf runs/user/validation_pg_smoke_dryrun runs/user/validation_pg_smoke_capture
PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --engine postgres --smoke --adapter-command "python examples/user/noop_adapter.py" --out runs/user/validation_pg_smoke_dryrun --dry-run
PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --engine postgres --smoke --adapter-command "python examples/user/noop_adapter.py" --out runs/user/validation_pg_smoke_capture
```

Common-core static validation:

```bash
python - <<'PY'
import csv, os, subprocess, sys
from pathlib import Path
rows = list(csv.DictReader(Path('case_sets/common_core_v0/cases.csv').open()))
failed = []
for row in rows:
    completed = subprocess.run(
        [sys.executable, 'scripts/dev/validate_case_package_v2_refs.py', '--case', row['case_path']],
        cwd=Path.cwd(),
        env={**os.environ, 'PYTHONPATH': 'src'},
        text=True,
        capture_output=True,
    )
    if completed.returncode != 0:
        failed.append(row['case_path'])
if failed:
    raise SystemExit(failed)
print(f'v2 validators passed for {len(rows)} Common-core case paths')
PY
```

Final validation and cleanup commands are recorded in `test_results.md` and the final task report. Local `runs/user/` outputs are not staged or committed.
