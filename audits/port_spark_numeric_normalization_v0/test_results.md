# Test Results

Focused checks:
- `PYTHONPATH=src python -m py_compile src/sql_rewrite_bench/local_result_checker.py src/sql_rewrite_bench/user_run.py tests/user_entry/test_cross_dialect_checker_normalization.py`: passed.
- `PYTHONPATH=src pytest tests/user_entry/test_cross_dialect_checker_normalization.py -q`: passed, 18 tests.

Live diagnostics:
- Spark PORT controlled rerun: selected/source/candidate/checker/exact/mismatch rows `4/4/4/4/4/0`.
- Spark unsupported role check: selected/source/candidate/checker rows `5/0/0/0`, `unsupported_engine=5`.
- PostgreSQL PORT target route preservation: exact `5/5`.
- MySQL PORT target route preservation: exact `4/4`.
- Non-PORT Spark two-case smoke: exact `2/2`.

Full validation:
- `PYTHONPATH=src pytest tests/user_entry -q`: passed, 130 passed, 1 skipped, 12 subtests passed.
- Case-package v2 reference validator over all 40 Common-core case paths: passed 40/40.
- `PYTHONPATH=src python scripts/dev/check_local_engine_env.py`: PostgreSQL probe ok, MySQL probe ok, Spark PySpark available.
- `git diff --check`: passed.

Common-core Spark full no-op note:
- Not rerun in this task. The targeted PORT controlled run and non-PORT Spark two-case smoke were run instead because after PORT Spark role mapping, a full `--engine spark` no-op run includes four manifest-declared cross-dialect Spark target roles and is no longer equivalent to the earlier pure same-engine 31-row diagnostic.
