# Command Log

Initial checks:

- `git status -sb`: branch `feature/case-package-v2-external-schema`; only P4 working changes after implementation.
- `git branch --show-current`: `feature/case-package-v2-external-schema`.
- `git log --oneline -12`: reviewed recent P1-P3 and release-surface commits.

Implementation validation:

- `PYTHONPATH=src python -m py_compile src/sql_rewrite_bench/mysql_execution.py src/sql_rewrite_bench/engine_execution.py src/sql_rewrite_bench/user_run.py src/sql_rewrite_bench/user_ledger.py src/sql_rewrite_bench/user_run_schema.py`: passed.
- `PYTHONPATH=src pytest tests/user_entry/test_mysql_source_reference_backend.py tests/user_entry/test_port_local_diagnostic_metadata.py tests/user_entry/test_engine_execution_router.py`: passed, 15 passed.
- `PYTHONPATH=src pytest tests/user_entry`: passed, 80 passed and 1 skipped.
- `git diff --check`: passed.

Help/readability/smoke:

- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --help`: passed.
- `python scripts/user/run_user_benchmark.py --help`: passed.
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --list-cases`: passed.
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --engine postgres --smoke --explain-selection`: passed.
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --show-output-schema`: passed.
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --engine postgres --smoke --adapter-command "python examples/user/noop_adapter.py" --out runs/user/p4_mysql_dry_run --dry-run`: passed.
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --engine postgres --smoke --adapter-command "python examples/user/noop_adapter.py" --out runs/user/p4_mysql_dummy_adapter`: passed.

MySQL environment and targeted run:

- `command -v mysql`: `/usr/bin/mysql`.
- `env | rg '^SQLRB_MYSQL_|^MYSQL_PWD'`: no required MySQL connection variables present.
- Targeted five-case run for `PORT_0004`, `PORT_0013`, `PORT_0022`, `PORT_0024`, and `PORT_0025`: completed with `mysql_config_missing=5`.

Cleanup:

- Removed `runs/user/p4_mysql_dry_run`.
- Removed `runs/user/p4_mysql_dummy_adapter`.
- Removed `runs/user/p4_mysql_port_targeted`.
