# Protected Surface Check

## Intended Files

Source/test changes:

- `src/sql_rewrite_bench/local_result_checker.py`
- `src/sql_rewrite_bench/user_quality_report.py`
- `tests/user_entry/test_cross_dialect_checker_normalization.py`
- `tests/user_entry/test_quality_report.py`

Audit/project-control changes:

- `audits/checker_label_only_diagnostics_patch_v0/*`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

## Protected Surfaces

The following protected surfaces must remain unchanged:

- cases, manifests, SQL files, schemas, checker configs, and validation scripts
- `baselines/sqlglot/`
- `case_sets/`
- `inventory/`
- `reports/`
- `results/`
- `benchmark_spec/`
- `repository_spec/`
- retained evidence
- `project_control/MIGRATION_MASTER_PLAN.md`
- `project_control/DECISION_LOG.md`
- tracked `runs/user/` outputs

## Local Run Outputs

The targeted local diagnostic run output is under:

- `runs/user/mysql_label_only_diagnostics_patch_check`

This output is not committed.

## Validation Status

Passed.

Commands/results:

- `PYTHONPATH=src pytest tests/user_entry/test_cross_dialect_checker_normalization.py tests/user_entry/test_quality_report.py -q`: 30 passed.
- `PYTHONPATH=src pytest tests/user_entry -q`: 146 passed, 1 skipped, 12 subtests passed.
- `git diff --check`: passed.
- project-control readability check: passed.
- audit Markdown sanity check: passed.
- audit CSV sanity check: passed.
- protected-surface diff check: passed.
- `git status -sb -- runs/user`: no tracked or staged `runs/user/` changes.

Only intended source/test/audit/project-control files changed.
