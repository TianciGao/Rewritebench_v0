# Test Results

Validation commands run:

- `git diff --check`: passed.
- `PYTHONPATH=src python -m py_compile examples/user/port_mysql_target_reference_adapter.py src/sql_rewrite_bench/engine_execution.py`: passed.
- `python scripts/dev/check_local_engine_env.py` after sourcing local PostgreSQL/MySQL env files: PostgreSQL ok, MySQL ok, Spark deferred/fail-closed.
- `PYTHONPATH=src pytest tests/user_entry`: not run because `pytest` is not installed in the local environment.
- `PYTHONPATH=src python -m unittest discover -s tests/user_entry -p 'test_*.py'`: passed, 111 tests with 2 skipped.
- `PYTHONPATH=src python -m unittest discover -s tests/case_package_v2 -p 'test_*.py'`: passed, 24 tests.
- Common-core v2 validator loop: passed, 40/40 cases.
- Reverse controlled diagnostic: selected 4, exact 4, mismatch 0.
- Forward PORT controlled regression: selected 5, exact 5, mismatch 0.
- Public smoke capture: selected 2, candidate generated 2.

No official metrics, timing/speedup, reports/results updates, retained-evidence promotion, or leaderboard output were produced.
