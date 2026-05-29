# Command Log

Commands and short outcomes only.

- `git status -sb`: clean worktree on `feature/case-package-v2-external-schema`.
- `git branch --show-current`: `feature/case-package-v2-external-schema`.
- `git log --oneline -10`: latest commits included the prior user-entry compatibility audit.
- Read project-control files: master plan, status, decision log, and run-log tail reviewed.
- Read prior audit packet: compatibility README, gap list, reorganization plan, and future repair prompt.
- Inspected user-entry implementation, tests, docs, and representative normalized case manifests/external schema profiles.
- Implemented `--smoke` deterministic selection for `PERF_0006` and `CONS_0005`.
- Added `examples/user/noop_adapter.py`.
- Repaired PostgreSQL schema resolution to use manifest `schema.external_profile` and external profile `engines.postgres.ddl/load`.
- Updated user guide to separate supported public smoke, optional local PostgreSQL diagnostics, and deferred paper reproduction/metrics/reporting work.
- Added/updated user-entry tests for smoke selection, public smoke outputs, external schema resolution, and fail-closed DB execution metadata handling.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src python -m unittest discover -s tests/user_entry -v`: passed, 33 tests with 1 skipped.
- `PYTHONPATH=src python -m sql_rewrite_bench.user_run --help`: passed.
- `python scripts/user/run_user_benchmark.py --help`: passed.
- Public smoke dry-run under `runs/user/smoke_dry_run`: passed, selected_rows=2, candidate_generated_rows=0; output removed.
- Public smoke adapter-capture under `runs/user/smoke_dummy_adapter`: passed, selected_rows=2, candidate_generated_rows=2; output removed.
- Live DB/checker execution: not run.
- Audit CSV parse/header check: passed.
- `git diff --check`: passed.
- Protected-surface diff check: passed; changed paths were limited to allowed user-entry source/docs/tests/example, audit packet, and project-control writeback files.
- Final validation: passed.
