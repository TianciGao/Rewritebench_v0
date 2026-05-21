# Test Results

Validation commands run for this task:

```bash
PYTHONPATH=src python -m py_compile src/sql_rewrite_bench/local_result_checker.py src/sql_rewrite_bench/case_package_resolver.py src/sql_rewrite_bench/user_run.py src/sql_rewrite_bench/user_run_schema.py
```

Result: passed.

```bash
bash -lc 'source scripts/env_mysql.local.sh && source scripts/env_postgres.local.sh && python scripts/dev/check_local_engine_env.py'
```

Result: PostgreSQL probe ok; MySQL probe ok; Spark deferred/fail-closed.

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run --help
python scripts/user/run_user_benchmark.py --help
```

Result: both help commands passed.

```bash
PATH=/tmp/sqlrb_pytest_venv/bin:$PATH PYTHONPATH=src pytest tests/user_entry/test_cross_dialect_checker_normalization.py tests/user_entry/test_db_checker_execution_mvp.py tests/user_entry/test_port_local_diagnostic_metadata.py
```

Result: 28 passed.

```bash
PATH=/tmp/sqlrb_pytest_venv/bin:$PATH PYTHONPATH=src pytest tests/user_entry
```

Result: 95 passed, 2 skipped.

```bash
PYTHONPATH=src python scripts/dev/validate_case_package_v2_refs.py --case <case_path>
```

Result: passed for all 40 Common-core case paths. The legacy `validate_case_package.py --mode canonical-case/full-case` validator is not applicable to the current clean v2 layout and still expects v1-era paths.

```bash
PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --engine postgres --case-list /tmp/sqlrb_port_cross_dialect_cases.txt --adapter-command "python examples/user/port_postgres_target_reference_adapter.py" --out runs/user/port_pg_target_reference_normalized --enable-db-execution --enable-checker
```

Result: selected 5; MySQL source-reference executable 5; PostgreSQL target-candidate executable 5; checker attempted 5; exact 5; mismatch 0.

```bash
git diff --check
```

Result: passed.
