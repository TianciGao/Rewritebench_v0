# Command Log

- `git status -sb`: clean on `feature/case-package-v2-external-schema` before edits.
- `git branch --show-current`: `feature/case-package-v2-external-schema`.
- `git log --oneline -10`: reviewed latest branch history.
- Read project-control files including `USER_ENTRY_LOCAL_EVALUATION_ARCHITECTURE_PLAN.md`.
- Read user-entry implementation files and public user-entry docs.
- Read Common-core case-set and denominator scaffolds.
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --help`: passed.
- `python scripts/user/run_user_benchmark.py --help`: passed.
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --engine postgres --smoke --adapter-command "python examples/user/noop_adapter.py" --out runs/user/u1_schema_dry_run --dry-run`: passed with `selected_rows=2`, `candidate_generated_rows=0`.
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --case-set common_core_v0 --engine postgres --smoke --adapter-command "python examples/user/noop_adapter.py" --out runs/user/u1_schema_dummy_adapter`: passed with `selected_rows=2`, `candidate_generated_rows=2`.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src pytest tests/user_entry`: passed with 32 tests passed and 1 skipped.
- Inspected `config.yaml`, `selected_cases.csv`, `ledger.csv`, `failures.csv`, `summary.json`, `report.md`, `candidate_sql/`, and per-row `workspaces/`.
- Removed `runs/user/u1_schema_dry_run` and `runs/user/u1_schema_dummy_adapter` after recording schema details.
- `git diff --check`: passed.
- CSV parse checks: passed for 7 CSV files.
- Markdown sanity checks: passed for 6 audit Markdown files.
- Protected-surface diff check: passed; only `audits/user_entry_output_schema_audit_v0/*`, `project_control/MIGRATION_STATUS.md`, and `project_control/MIGRATION_RUN_LOG.md` changed.
- Smoke output cleanup check: passed; `runs/user/u1_schema_dry_run` and `runs/user/u1_schema_dummy_adapter` are absent before commit.
