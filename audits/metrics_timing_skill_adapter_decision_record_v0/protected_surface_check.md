# Protected Surface Check

## Intended Files

- `project_control/DECISION_LOG.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`
- `audits/metrics_timing_skill_adapter_decision_record_v0/*`

## Protected Surfaces

The following surfaces must remain unchanged:

- `src/`
- `tests/`
- `scripts/`
- `cases/`
- manifests
- SQL files
- schemas
- checker configs
- validation scripts
- `baselines/`
- `case_sets/`
- `inventory/`
- `reports/`
- `results/`
- retained evidence
- `repository_spec/`
- `benchmark_spec/`
- `project_control/MIGRATION_MASTER_PLAN.md`
- `runs/user/`

## Validation Status

Passed.

Commands/results:

- `git diff --check`: passed.
- project-control readability check: passed.
- audit Markdown sanity check: passed.
- protected-surface check: passed.
- `git status -sb -- runs/user`: no tracked or staged `runs/user/` changes.
- Protected path diff across `src/`, `tests/`, `scripts/`, `cases/`, `baselines/`, `case_sets/`, `inventory/`, `reports/`, `results/`, `repository_spec/`, `benchmark_spec/`, and `runs/user/`: no output.

Only the intended decision-log, migration status/run-log, and audit packet files changed.
