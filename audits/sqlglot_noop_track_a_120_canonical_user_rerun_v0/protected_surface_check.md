# Protected Surface Check

Protected surfaces not modified:
- `src/`
- `tests/`
- `baselines/`
- `cases/`
- `case_sets/`
- `schemas/`
- `inventory/`
- top-level `reports/`
- top-level `results/`
- repository-level `output/`
- committed `runs/user/`
- external artifacts
- `project_control/MIGRATION_MASTER_PLAN.md`
- `project_control/DECISION_LOG.md`

Allowed paths modified:
- `audits/sqlglot_noop_track_a_120_canonical_user_rerun_v0/`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Runtime artifacts were generated under:
- `runs/user/` source-run staging, not staged for commit.
- `/tmp/sqlrb_sqlglot_noop_track_a_120_canonical_user_rerun_v0/output/`, outside the repository.
