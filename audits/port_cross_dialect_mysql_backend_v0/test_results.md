# Test Results

Validation commands run:

- `git diff --check`: passed.
- `PYTHONPATH=src python -m py_compile src/sql_rewrite_bench/mysql_execution.py src/sql_rewrite_bench/engine_execution.py src/sql_rewrite_bench/user_run.py src/sql_rewrite_bench/user_ledger.py src/sql_rewrite_bench/user_run_schema.py`: passed.
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --help`: passed.
- `python scripts/user/run_user_benchmark.py --help`: passed.
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --list-cases`: passed.
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --engine postgres --smoke --explain-selection`: passed.
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --show-output-schema`: passed.
- Public smoke dry-run for `runs/user/p4_mysql_dry_run`: passed and output was removed.
- Public smoke adapter-capture for `runs/user/p4_mysql_dummy_adapter`: passed and output was removed.
- `PYTHONPATH=src pytest tests/user_entry`: passed, 80 passed and 1 skipped.
- `PYTHONPATH=src pytest tests/case_package_v2/test_case_package_v2_resolver.py::CasePackageV2ResolverTests::test_all_common_core_port_local_diagnostic_metadata_validates`: passed.
- Targeted five-case cross-dialect local run: completed with `cross_dialect_backend_missing=5`, `mysql_config_missing=5`, and no PostgreSQL source syntax failures; output was removed.

Live MySQL diagnostic:

- Not run because required MySQL connection environment variables were missing.
- Live MySQL was not required for tests.
