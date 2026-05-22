# Validation Results

## Focused Tests

```bash
PYTHONPATH=src pytest tests/user_entry/test_local_metrics.py -q
```

Result: passed, 6 tests.

## Full User-Entry Tests

```bash
PYTHONPATH=src pytest tests/user_entry -q
```

Result: passed, 159 tests, 1 skipped, 12 subtests passed.

## Python Compile

```bash
PYTHONPATH=src python -m py_compile src/sql_rewrite_bench/local_metrics.py scripts/dev/compute_local_user_metrics.py
```

Result: passed.

## Bounded Metrics Smoke

Result: passed for PostgreSQL, MySQL, and Spark bounded SQLGlot noop timing smoke runs.

## Protected Surface

No cases, baselines, `case_sets/`, reports, results, retained evidence, or committed `runs/user/` outputs changed.
