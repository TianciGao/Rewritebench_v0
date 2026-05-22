# Protected Surface Check

Allowed tracked changes for this task:

- `audits/common_core_sqlglot_noop_local_metrics_projection_v0/*`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Protected surfaces expected unchanged:

- `src/`
- `tests/`
- `scripts/`
- `cases/`
- `baselines/`
- `case_sets/`
- `reports/`
- `results/`
- retained evidence
- `repository_spec/`
- `benchmark_spec/`
- `project_control/MIGRATION_MASTER_PLAN.md`
- `project_control/DECISION_LOG.md`
- tracked `runs/user/` outputs

Review result:

- The local metrics calculator wrote ignored local outputs under `runs/user/*/metrics/`.
- No `runs/user/` output is staged or committed.
- No protected tracked surfaces were modified.
- Final protected-surface validation is recorded in the command log and final report.
