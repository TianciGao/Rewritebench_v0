# Test Coverage

Focused tests added:

- Single-run metrics behavior remains covered by existing `test_local_metrics.py`.
- Multi-engine aggregate consumes synthetic per-engine run dirs.
- Aggregate selected/generated/executable/exact counts are summed correctly.
- Exact-timed speedup rows are concatenated across engines.
- GM speedup is computed by canonical `local_metrics.py`.
- SER remains N.A. without verifier evidence.
- Formal Regression@20 is not emitted as a local metric.
- CLI aggregate mode delegates to `compute_and_write_aggregate_local_metrics`.
- CLI aggregate mode rejects incomplete aggregate options.
- Aggregate output refuses to reuse a source run directory as the aggregate target.

Validation run:

```bash
pytest tests/user_entry/test_local_metrics.py tests/user_entry/test_cli_facade.py -q
pytest tests/user_entry -q
python -m py_compile src/sql_rewrite_bench/local_metrics.py src/cli/main.py tests/user_entry/test_local_metrics.py tests/user_entry/test_cli_facade.py
```

Results:

- Focused tests: 31 passed.
- Full user-entry tests: 244 passed, 1 skipped, 15 subtests passed.
- Py compile: passed.
