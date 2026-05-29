# Command Log

Preflight:

- `git status -sb`: clean before edits.
- `git branch --show-current`: `feature/case-package-v2-external-schema`.
- `git log --oneline -15`: reviewed.
- `source scripts/env_postgres.local.sh`, `source scripts/env_mysql.local.sh`; `scripts/env_spark.local.sh` was absent.
- `python scripts/dev/check_local_engine_env.py`: PostgreSQL ok, MySQL ok, Spark unavailable/fail-closed.

Implementation validation:

- `PYTHONPATH=src python -m py_compile src/sql_rewrite_bench/spark_execution.py src/sql_rewrite_bench/engine_execution.py scripts/dev/check_local_engine_env.py tests/user_entry/test_engine_execution_router.py`: passed.
- `PYTHONPATH=src python -m unittest tests.user_entry.test_engine_execution_router`: passed.
- `python scripts/dev/check_local_engine_env.py`: passed.
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --engine spark --smoke --explain-selection`: passed.
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --show-output-schema`: passed.
- `PYTHONPATH=src python -m py_compile src/sql_rewrite_bench/spark_execution.py src/sql_rewrite_bench/engine_execution.py src/sql_rewrite_bench/user_run.py src/sql_rewrite_bench/user_ledger.py src/sql_rewrite_bench/user_run_schema.py scripts/dev/check_local_engine_env.py`: passed.
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --help`: passed.
- `python scripts/user/run_user_benchmark.py --help`: passed.
- `git diff --check`: passed.
- `PYTHONPATH=src pytest tests/user_entry`: failed to start because `pytest` is not installed.
- `PYTHONPATH=src python -m unittest discover tests/user_entry`: passed.
- `PYTHONPATH=src python scripts/dev/validate_case_package_v2_refs.py --case <case>` for all 40 Common-core cases: passed.
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --engine spark --smoke --adapter-command "python examples/user/noop_adapter.py" --out runs/user/spark_live_backend_env_blocked_smoke --enable-db-execution --enable-checker`: passed as fail-closed smoke; output removed before commit.
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --engine postgres --smoke --adapter-command "python examples/user/noop_adapter.py" --out runs/user/spark_live_backend_pg_regression_smoke --enable-db-execution --enable-checker`: passed; selected 2, exact 2; output removed before commit.
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --engine mysql --smoke --adapter-command "python examples/user/noop_adapter.py" --out runs/user/spark_live_backend_mysql_regression_smoke --enable-db-execution --enable-checker`: passed; selected 2, exact 2; output removed before commit.

Live Spark smoke:

- Not run because `pyspark` is unavailable and Spark local environment is not configured.
