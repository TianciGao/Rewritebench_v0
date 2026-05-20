# Command Log

Commands and short outcomes only.

- `git status -sb`: clean worktree before task edits.
- `git branch --show-current`: `feature/case-package-v2-external-schema`.
- `git log --oneline -10`: latest commits included the Chinese README rewrite.
- Read project-control files: master plan, status, decision log, and run-log tail reviewed.
- Read top-level `README.md`, user benchmark guide, public no-op adapter, user-entry source files, thin wrapper, and Common-core scaffolds.
- Confirmed case selection is metadata-driven through `case_sets/common_core_v0/`.
- Confirmed smoke cases are `PERF_0006` and `CONS_0005`.
- Added the `用户入口数据流与文件位置` section to the top-level README.
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --help`: passed.
- `python scripts/user/run_user_benchmark.py --help`: passed.
- Documented public smoke dry-run command: passed, selected_rows=2, candidate_generated_rows=0.
- Documented public smoke adapter-capture command: passed, selected_rows=2, candidate_generated_rows=2.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src pytest tests/user_entry`: passed, 32 tests passed and 1 skipped.
- Common-core scaffold count check: passed, 40 cases and 120 denominator rows.
- Removed `runs/user/smoke_dry_run` and `runs/user/smoke_dummy_adapter` outputs created by this task.
- Removed pytest-generated `__pycache__` directories.
- `git diff --check`: passed.
- Protected-surface diff check: passed.
- Final validation: passed.
