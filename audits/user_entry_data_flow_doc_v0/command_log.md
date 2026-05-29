# Command Log

Commands and outcomes:

- `git status -sb`: clean on `feature/case-package-v2-external-schema` before edits.
- `git branch --show-current`: `feature/case-package-v2-external-schema`.
- `git log --oneline -10`: reviewed current branch history.
- Read project-control files, current README, user benchmark guide, public no-op adapter, user-entry source files, wrapper, and Common-core case-set CSVs.
- `git diff --check`: passed.
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --help`: passed.
- `python scripts/user/run_user_benchmark.py --help`: passed.
- Public smoke dry-run command from README: passed, `selected_rows=2`, `candidate_generated_rows=0`.
- Public smoke adapter-capture command from README: passed, `selected_rows=2`, `candidate_generated_rows=2`.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src pytest tests/user_entry`: passed, 32 tests passed and 1 skipped.
- Placeholder path check: passed; no `cases///`, `runs/user//`, `schemas//`, or angle-bracket case/schema placeholder paths remain in public README/data-flow docs.
- README large-table check: passed; the detailed 20+ row file-location table is no longer in top-level `README.md`.
- Protected-surface diff check: passed; only allowed documentation, audit, and project-control files changed.
- Local smoke outputs under `runs/user/smoke_dry_run` and `runs/user/smoke_dummy_adapter` were removed after recording results.
