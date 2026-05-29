# Command Log

Commands and short outcomes only.

- `git status -sb`: clean worktree on `feature/case-package-v2-external-schema`.
- `git branch --show-current`: `feature/case-package-v2-external-schema`.
- `git log --oneline -10`: latest commits included final public-release planning and source-path follow-up finalization.
- Read project-control files: master plan, status, decision log, and run-log tail reviewed.
- Read user-entry files: `README.md`, `docs/USER_BENCHMARK_GUIDE.md`, `scripts/user/run_user_benchmark.py`, `src/sql_rewrite_bench/user_run.py`, `src/sql_rewrite_bench/case_selection.py`, `src/sql_rewrite_bench/postgres_execution.py`, `src/sql_rewrite_bench/local_result_checker.py`, `src/sql_rewrite_bench/user_run_schema.py`, `baselines/sqlglot/sqlglot_user_adapter.py`, `tests/user_entry/`, `.github/workflows/`, and `pyproject.toml`.
- Read Common-core metadata: 40 cases, pool split 16 PERF / 9 CONS / 9 PORT / 6 LONGTAIL, 120 same-engine denominator rows, 360 control rows.
- Spot-checked representative case packages: normalized layout present; case-local `schema/postgres/` absent.
- Static all-Common-core source check: 0 missing `sql/source.sql` files.
- Static all-Common-core case-local PostgreSQL schema check: 0/40 cases have case-local `schema/postgres/ddl.sql` and `load.sql`.
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --help`: passed.
- `python scripts/user/run_user_benchmark.py --help`: passed.
- `PYTHONPATH=src python baselines/sqlglot/sqlglot_user_adapter.py --help`: passed.
- Created `/tmp/sqlrb_user_entry_cases.txt` with `PERF_0006` and `CONS_0005`.
- Non-DB dry-run smoke under `runs/user/audit_user_entry_dry_run`: passed, selected_rows=2, candidate_generated_rows=0.
- Non-DB dummy-adapter smoke under `runs/user/audit_user_entry_dummy_adapter`: passed, selected_rows=2, candidate_generated_rows=2.
- Recorded smoke output summaries and removed `runs/user/audit_user_entry_dry_run`, `runs/user/audit_user_entry_dummy_adapter`, and `/tmp/sqlrb_user_entry_cases.txt`.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m unittest discover -s tests/user_entry -v`: passed, 27 tests, 1 skipped.
- Removed local user-entry test outputs generated under `runs/user/unittest_*`.
- CSV parse/header checks for `entrypoint_inventory.csv`, `smoke_results.csv`, and `compatibility_matrix.csv`: passed.
- `git diff --check`: passed.
- Protected-surface diff check: passed; only this audit packet plus `project_control/MIGRATION_STATUS.md` and `project_control/MIGRATION_RUN_LOG.md` changed.
