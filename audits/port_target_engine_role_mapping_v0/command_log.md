# Command Log

Initial checks:

```bash
git status -sb
git branch --show-current
git log --oneline -12
source scripts/env_mysql.local.sh
source scripts/env_postgres.local.sh
python scripts/dev/check_local_engine_env.py
```

Context read:

```bash
sed -n '1,240p' project_control/MIGRATION_MASTER_PLAN.md
sed -n '1,120p' project_control/MIGRATION_STATUS.md
tail -100 project_control/MIGRATION_RUN_LOG.md
sed -n '1,260p' project_control/PORT_CROSS_DIALECT_DIAGNOSTIC_EXECUTION_PLAN.md
sed -n '1,260p' project_control/USER_ENTRY_LOCAL_EVALUATION_ARCHITECTURE_PLAN.md
sed -n '1,220p' audits/mysql_same_engine_source_failure_triage_v0/README.md
cat audits/mysql_same_engine_source_failure_triage_v0/failed_case_triage.csv
sed -n '1,220p' audits/port_cross_dialect_local_diagnostic_closeout_v0/README.md
sed -n '1,220p' audits/port_cross_dialect_checker_normalization_v0/README.md
sed -n '1,220p' audits/common_core_mysql_local_diagnostic_v0/README.md
```

Implementation inspection covered resolver, runner, engine execution, PostgreSQL/MySQL/Spark execution modules, checker, ledger/schema modules, tests, and all 9 PORT manifests.

Validation and diagnostics:

```bash
python - <<'PY'
import yaml
from pathlib import Path
for case in ['PORT_0003','PORT_0004','PORT_0005','PORT_0008','PORT_0012','PORT_0013','PORT_0022','PORT_0024','PORT_0025']:
    yaml.safe_load((Path('cases/PORT')/case/'manifest.yaml').read_text())
print('yaml ok')
PY
PYTHONPATH=src python -m py_compile src/sql_rewrite_bench/case_package_resolver.py src/sql_rewrite_bench/case_package_v2_resolver.py src/sql_rewrite_bench/user_run.py src/sql_rewrite_bench/engine_execution.py src/sql_rewrite_bench/user_run_schema.py
PYTHONPATH=src python -m unittest discover -s tests/user_entry -p 'test_*.py'
PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -p 'test_*.py'
PYTHONPATH=src python -m sql_rewrite_bench.user_run --help
python scripts/user/run_user_benchmark.py --help
PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --list-cases
PYTHONPATH=src python -m sql_rewrite_bench.user_run --show-output-schema
PYTHONPATH=src python scripts/dev/validate_case_package_v2_refs.py --case <each Common-core case path>
git diff --check
python - <<'PY'
# Parse all audit CSV/JSON/Markdown files and all 9 PORT manifests.
PY
python - <<'PY'
# Protected-surface diff check over changed and untracked paths.
PY
```

`pytest` was requested, but the local environment has no `pytest` module installed. Equivalent `unittest` discovery was run and passed for the relevant suites.

Targeted local diagnostics:

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --engine postgres \
  --case-list /tmp/sqlrb_port_pg_cases.txt \
  --adapter-command "python examples/user/port_postgres_target_reference_adapter.py" \
  --out runs/user/port_target_engine_pg_controlled \
  --enable-db-execution \
  --enable-checker

PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --engine mysql \
  --case-list /tmp/sqlrb_port_mysql_reverse_cases.txt \
  --adapter-command "python examples/user/noop_adapter.py" \
  --out runs/user/port_target_engine_mysql_reverse_guard \
  --enable-db-execution \
  --enable-checker

PYTHONPATH=src python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --engine mysql \
  --case-list /tmp/sqlrb_port_mysql_source_case.txt \
  --adapter-command "python examples/user/noop_adapter.py" \
  --out runs/user/port_target_engine_mysql_source_same_engine \
  --enable-db-execution \
  --enable-checker
```

Local run outputs are not committed.
