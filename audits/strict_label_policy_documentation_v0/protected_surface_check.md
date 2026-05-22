# Protected Surface Check

## Intended Files

- `docs/user_entry_checker_policy.md`
- `audits/strict_label_policy_documentation_v0/*`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

## Protected Surfaces

The following surfaces must remain unchanged:

- `src/`
- `tests/`
- `cases/`
- checker configs
- SQL files
- `baselines/`
- `case_sets/`
- `inventory/`
- `reports/`
- `results/`
- retained evidence
- `project_control/MIGRATION_MASTER_PLAN.md`
- `project_control/DECISION_LOG.md`
- `runs/user/`

## Validation Status

Passed.

Commands/results:

- `git diff --check`: passed.
- project-control readability check: passed.
- Markdown sanity check for `docs/user_entry_checker_policy.md` and audit files: passed.
- protected-surface check: passed.
- `git status -sb -- runs/user`: no tracked or staged `runs/user/` changes.
- Protected path diff across `src/`, `tests/`, `cases/`, `baselines/`, `case_sets/`, `inventory/`, `reports/`, `results/`, `benchmark_spec/`, `repository_spec/`, and `runs/user/`: no output.

Only the intended documentation, audit, and project-control files changed.
