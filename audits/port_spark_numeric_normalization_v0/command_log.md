# Command Log

Preflight and context:
- `git status -sb && git branch --show-current && git log --oneline -12`
- Read project-control files and `audits/port_spark_target_role_mapping_v0/`.
- Inspected `runs/user/port_spark_target_reference_controlled/` artifacts for `PORT_0004` and `PORT_0013`.

Focused implementation checks:
- `PYTHONPATH=src python -m py_compile src/sql_rewrite_bench/local_result_checker.py src/sql_rewrite_bench/user_run.py tests/user_entry/test_cross_dialect_checker_normalization.py`
- `PYTHONPATH=src pytest tests/user_entry/test_cross_dialect_checker_normalization.py -q`

Diagnostic reruns:
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --engine spark --case-list /tmp/sqlrb_port_spark_controlled_cases.txt --adapter-command "python examples/user/port_spark_target_reference_adapter.py" --out runs/user/port_spark_target_reference_controlled_after_numeric_fix --enable-db-execution --enable-checker`
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --engine spark --case-list /tmp/sqlrb_port_spark_unsupported_cases.txt --adapter-command "python examples/user/noop_adapter.py" --out runs/user/port_spark_unsupported_role_check_after_numeric_fix --enable-db-execution --enable-checker`
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --engine postgres --case-list /tmp/sqlrb_port_pg_forward_cases.txt --adapter-command "python examples/user/port_postgres_target_reference_adapter.py" --out runs/user/port_pg_forward_preservation_after_numeric_fix --enable-db-execution --enable-checker`
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --engine mysql --case-list /tmp/sqlrb_port_mysql_reverse_cases.txt --adapter-command "python examples/user/port_mysql_target_reference_adapter.py" --out runs/user/port_mysql_reverse_preservation_after_numeric_fix --enable-db-execution --enable-checker`
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --engine spark --case-list /tmp/sqlrb_spark_two_case_after_numeric_fix.txt --adapter-command "python examples/user/noop_adapter.py" --out runs/user/spark_two_case_regression_after_numeric_fix --enable-db-execution --enable-checker`

Final validation:
- `PYTHONPATH=src pytest tests/user_entry -q`
- Case-package v2 reference validator loop over all 40 Common-core case paths.
- `PYTHONPATH=src python scripts/dev/check_local_engine_env.py`
- `git diff --check`
- CSV/JSON/Markdown sanity checks for audit files.
- Protected-surface diff check.
