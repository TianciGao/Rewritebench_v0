# Protected Surface Check

## Intended Files

- `audits/latest_paper_metrics_timing_protocol_alignment_v0/*`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

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
- `MIGRATION_MASTER_PLAN.md`
- `DECISION_LOG.md`
- `runs/user/`

## Validation Status

Passed.

Commands/results:

- `git diff --check`: passed.
- project-control readability check: passed.
- audit Markdown sanity check: passed.
- protected-surface check: passed.
- `git status -sb -- runs/user`: no tracked or staged `runs/user/` changes.
- Protected path diff across `src/`, `tests/`, `scripts/`, `cases/`, `baselines/`, `case_sets/`, `inventory/`, `reports/`, `results/`, `repository_spec/`, `benchmark_spec/`, `runs/user/`, and `project_control/DECISION_LOG.md`: no output.

Only the intended audit packet and migration status/run-log files changed.
