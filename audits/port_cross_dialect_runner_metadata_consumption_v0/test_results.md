# Test Results

Commands run:

- `PYTHONPATH=src python -m py_compile src/sql_rewrite_bench/case_package_resolver.py src/sql_rewrite_bench/user_run.py src/sql_rewrite_bench/engine_execution.py src/sql_rewrite_bench/user_ledger.py src/sql_rewrite_bench/user_run_schema.py src/sql_rewrite_bench/mysql_execution.py src/sql_rewrite_bench/tag_slices.py src/sql_rewrite_bench/case_package_v2_resolver.py tests/user_entry/test_port_local_diagnostic_metadata.py tests/case_package_v2/test_case_package_v2_resolver.py`
- `PYTHONPATH=src pytest tests/user_entry/test_port_local_diagnostic_metadata.py tests/user_entry/test_engine_execution_router.py tests/case_package_v2/test_case_package_v2_resolver.py -q`
- `PYTHONPATH=src pytest tests/user_entry -q`
- `PYTHONPATH=src pytest tests/case_package_v2 -q`
- `PYTHONPATH=src python scripts/dev/validate_case_package_v2_refs.py --case ...` for all 9 PORT cases
- `PYTHONPATH=src python scripts/dev/validate_case_package_v2_refs.py --case ...` for all 40 Common-core cases
- Targeted five-case PostgreSQL local diagnostic with no-op adapter and DB/checker flags.
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --help`
- `python scripts/user/run_user_benchmark.py --help`
- Public smoke dry-run under `runs/user/p3_runner_metadata_dry_run`
- Public smoke adapter-capture under `runs/user/p3_runner_metadata_dummy_adapter`
- CSV parse checks for new audit files.
- Markdown sanity checks for new audit files.
- Protected-surface diff check.

Observed results before final closeout validation:

- Targeted tests: 31 passed and 17 subtests passed.
- User-entry tests: 74 passed, 1 skipped, and 3 subtests passed.
- Case-package v2 tests: 22 passed and 14 subtests passed.
- All 9 PORT manifests passed static v2 validation.
- All 40 Common-core case packages passed static v2 validation.
- Targeted five-case diagnostic selected 5 rows, generated 5 candidates, passed preflight for 5 rows, and failed closed with `cross_dialect_backend_missing=5`.
- Public smoke dry-run selected 2 rows and generated 0 candidates.
- Public smoke adapter-capture selected 2 rows and generated 2 candidates.
- `quality_summary.json` and `tag_slices.csv` were generated for public smoke outputs.
- Optional 40-row live PostgreSQL diagnostic was not rerun because `SQLRB_POSTGRES_DSN` was unset in this shell; P3 validation used the targeted cross-dialect fail-closed run, which does not require live MySQL/Spark or PostgreSQL source execution for the five rows.

No live MySQL or Spark execution was run.
