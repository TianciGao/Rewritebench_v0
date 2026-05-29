# Test Results

Validation commands run:

- `PYTHONPATH=src python -m py_compile src/sql_rewrite_bench/spark_execution.py src/sql_rewrite_bench/engine_execution.py src/sql_rewrite_bench/user_run.py src/sql_rewrite_bench/user_ledger.py src/sql_rewrite_bench/user_run_schema.py scripts/dev/check_local_engine_env.py`: pass.
- `python scripts/dev/check_local_engine_env.py`: pass; Spark reported fail-closed/not live implemented.
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --help`: pass.
- `python scripts/user/run_user_benchmark.py --help`: pass.
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --engine spark --smoke --explain-selection`: pass; selected 2 rows and created no outputs.
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --show-output-schema`: pass.
- `PYTHONPATH=src pytest tests/user_entry/test_engine_execution_router.py`: blocked because `pytest` is not installed in this environment.
- `PYTHONPATH=src python -m unittest tests.user_entry.test_engine_execution_router`: pass, 9 tests.
- `PYTHONPATH=src python -m unittest discover -s tests/user_entry`: pass, 115 tests, 2 skipped.
- `PYTHONPATH=src python scripts/dev/run_user_entry_ci_smoke.py`: pass.
- `PYTHONPATH=src python -m unittest discover -s tests/case_package_v2`: pass, 24 tests.
- Common-core v2 reference validator loop: pass, 40 validated, 0 failed.

Optional local diagnostic smokes:

- Spark fail-closed smoke: selected 2 rows, generated 2 candidates, `unsupported_engine=2`, checker not attempted, no source/candidate result artifacts created.
- PostgreSQL smoke: selected 2 rows, exact 2/2.
- MySQL smoke: selected 2 rows, exact 2/2.

These smokes are local diagnostics only. They are not official metrics, timing, paper results, reports/results updates, or leaderboard inputs.

Note: an earlier parallel validation attempt ran two user-entry test processes at the same time and produced transient `runs/user` directory race failures in readability tests. The suite was rerun serially and passed.
