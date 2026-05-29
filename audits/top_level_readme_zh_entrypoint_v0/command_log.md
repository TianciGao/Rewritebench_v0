# Command Log

Commands and short outcomes only.

- `git status -sb`: clean worktree before task edits.
- `git branch --show-current`: `feature/case-package-v2-external-schema`.
- `git log --oneline -10`: latest commits included the user-entry external-schema repair.
- Read project-control files: master plan, status, decision log, and run-log tail reviewed.
- Read `README.md`, `docs/USER_BENCHMARK_GUIDE.md`, `examples/user/noop_adapter.py`, the latest user-entry repair audit packet, and Common-core scaffolds.
- Confirmed Common-core v0 count: 40 cases.
- Confirmed pool split: 16 PERF / 9 CONS / 9 PORT / 6 LONGTAIL.
- Confirmed same-engine denominator scaffold: 120 planned rows across PostgreSQL, MySQL, and Spark SQL.
- Rewrote top-level `README.md` in Chinese as a public entrypoint.
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --help`: passed.
- `python scripts/user/run_user_benchmark.py --help`: passed.
- Documented public smoke dry-run command: passed, selected_rows=2, candidate_generated_rows=0.
- Documented public smoke adapter-capture command: passed, selected_rows=2, candidate_generated_rows=2.
- `pytest tests/user_entry`: failed during collection because the src-layout package was not importable without installation or `PYTHONPATH`.
- `PYTHONPATH=src pytest tests/user_entry`: passed, 32 tests passed and 1 skipped.
- Removed `runs/user/smoke_dry_run` and `runs/user/smoke_dummy_adapter` outputs created by this task.
- Removed pytest-generated `__pycache__` directories.
- `git diff --check`: passed.
- Protected-surface diff check: passed.
- Final validation: passed.
