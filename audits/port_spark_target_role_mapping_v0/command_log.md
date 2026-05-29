# Command Log

Preflight:
- `git status -sb`
- `git branch --show-current`
- `git log --oneline -15`
- `source ~/code/sql-rewrite-bench/.venv/bin/activate`
- `source scripts/env_postgres.local.sh`
- `source scripts/env_mysql.local.sh`
- `source scripts/env_spark.local.sh`
- `export PYTHONPATH=src`
- `PYTHONPATH=src python scripts/dev/check_local_engine_env.py`

Focused checks:
- `PYTHONPATH=src python -m py_compile src/sql_rewrite_bench/engine_execution.py examples/user/port_spark_target_reference_adapter.py tests/user_entry/test_port_spark_target_reference_adapter.py tests/user_entry/test_port_local_diagnostic_metadata.py`
- YAML parse check for the 9 Common-core PORT manifests.
- `PYTHONPATH=src pytest tests/user_entry/test_port_spark_target_reference_adapter.py tests/user_entry/test_port_local_diagnostic_metadata.py -q`

Controlled diagnostics:
- Created `/tmp/sqlrb_port_spark_controlled_cases.txt` with `PORT_0003`, `PORT_0004`, `PORT_0005`, and `PORT_0013`.
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --engine spark --case-list /tmp/sqlrb_port_spark_controlled_cases.txt --adapter-command "python examples/user/port_spark_target_reference_adapter.py" --out runs/user/port_spark_target_reference_controlled --enable-db-execution --enable-checker`
- Created `/tmp/sqlrb_port_spark_unsupported_cases.txt` with `PORT_0008`, `PORT_0012`, `PORT_0022`, `PORT_0024`, and `PORT_0025`.
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --engine spark --case-list /tmp/sqlrb_port_spark_unsupported_cases.txt --adapter-command "python examples/user/noop_adapter.py" --out runs/user/port_spark_unsupported_role_check --enable-db-execution --enable-checker`

Behavior preservation:
- Created `/tmp/sqlrb_port_pg_forward_cases.txt` with `PORT_0004`, `PORT_0013`, `PORT_0022`, `PORT_0024`, and `PORT_0025`.
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --engine postgres --case-list /tmp/sqlrb_port_pg_forward_cases.txt --adapter-command "python examples/user/port_postgres_target_reference_adapter.py" --out runs/user/port_pg_forward_preservation_after_spark_roles --enable-db-execution --enable-checker`
- Created `/tmp/sqlrb_port_mysql_reverse_cases.txt` with `PORT_0003`, `PORT_0005`, `PORT_0008`, and `PORT_0012`.
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --engine mysql --case-list /tmp/sqlrb_port_mysql_reverse_cases.txt --adapter-command "python examples/user/port_mysql_target_reference_adapter.py" --out runs/user/port_mysql_reverse_preservation_after_spark_roles --enable-db-execution --enable-checker`
- Created `/tmp/sqlrb_spark_two_case_after_port_roles.txt` with `PERF_0006` and `CONS_0005`.
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --engine spark --case-list /tmp/sqlrb_spark_two_case_after_port_roles.txt --adapter-command "python examples/user/noop_adapter.py" --out runs/user/spark_two_case_regression_after_port_spark_roles --enable-db-execution --enable-checker`

Validation:
- `PYTHONPATH=src pytest tests/user_entry -q`
- `PYTHONPATH=src python scripts/dev/check_local_engine_env.py`
- Case-package v2 reference validator loop over all 40 Common-core case paths.
- `git diff --check`
- CSV/JSON parse checks for audit files.
- Markdown sanity checks for audit files.
- Protected-surface diff check.
