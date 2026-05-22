# Test Results

- `PYTHONPATH=src python -m py_compile src/sql_rewrite_bench/spark_execution.py src/sql_rewrite_bench/engine_execution.py src/sql_rewrite_bench/user_run.py src/sql_rewrite_bench/user_ledger.py src/sql_rewrite_bench/user_run_schema.py scripts/dev/check_local_engine_env.py`: passed.
- `python scripts/dev/check_local_engine_env.py`: passed; PostgreSQL ok, MySQL ok, Spark environment unavailable/fail-closed.
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --help`: passed.
- `python scripts/user/run_user_benchmark.py --help`: passed.
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --engine spark --smoke --explain-selection`: passed; selected 2 smoke rows and wrote no run outputs.
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --show-output-schema`: passed.
- `PYTHONPATH=src pytest tests/user_entry`: not run because `pytest` is not installed.
- `PYTHONPATH=src python -m unittest discover tests/user_entry`: passed; 119 tests, 2 skipped.
- `PYTHONPATH=src python -m unittest tests.user_entry.test_engine_execution_router`: passed; 13 tests.
- `PYTHONPATH=src python scripts/dev/validate_case_package_v2_refs.py --case <case>` loop over Common-core cases: passed; 40/40.
- Spark fail-closed smoke command: passed; selected 2 rows, generated 2 candidates, failed closed with `spark_config_missing` and no Spark SQL execution.
- PostgreSQL two-case DB/checker smoke: passed; selected 2, source executable 2, candidate executable 2, checker exact 2, mismatch 0.
- MySQL two-case DB/checker smoke: passed; selected 2, source executable 2, candidate executable 2, checker exact 2, mismatch 0.
- Live Spark smoke: not run because PySpark/Spark is not configured locally.

All results are local diagnostics only. No official metrics, timing/speedup, paper tables, reports/results updates, or leaderboard output were produced.
