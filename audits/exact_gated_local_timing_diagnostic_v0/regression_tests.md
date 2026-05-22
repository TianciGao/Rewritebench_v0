# Regression Tests

## Focused Tests

```bash
PYTHONPATH=src pytest tests/user_entry/test_local_timing.py -q
```

Result: passed, 7 tests.

## Relevant User-Entry Subset

```bash
PYTHONPATH=src pytest tests/user_entry/test_user_run_outputs.py tests/user_entry/test_db_checker_execution_mvp.py tests/user_entry/test_quality_report.py tests/user_entry/test_engine_execution_router.py tests/user_entry/test_local_timing.py -q
```

Result: passed, 45 tests.

## Full User-Entry Tests

```bash
PYTHONPATH=src pytest tests/user_entry -q
```

Result: passed, 153 tests, 1 skipped, 12 subtests passed.

## Python Compile

```bash
PYTHONPATH=src python -m py_compile src/sql_rewrite_bench/local_timing.py src/sql_rewrite_bench/user_run.py src/sql_rewrite_bench/user_ledger.py src/sql_rewrite_bench/user_run_schema.py
```

Result: passed.

## Bounded Timing Smoke

All three ready local engines completed the two-case SQLGlot noop timing smoke:

- PostgreSQL: 2 timed rows.
- MySQL: 2 timed rows.
- Spark: 2 timed rows.

No PORT rows, SQLGlot optimize route, full Common-core run, official metrics, route-level metrics, reports/results update, retained-evidence promotion, paper table rendering, or leaderboard output was performed.
