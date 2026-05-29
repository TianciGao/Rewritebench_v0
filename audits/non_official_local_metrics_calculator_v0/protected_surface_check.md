# Protected Surface Check

Allowed changes for this task:

- `src/sql_rewrite_bench/local_metrics.py`
- `scripts/dev/compute_local_user_metrics.py`
- `tests/user_entry/test_local_metrics.py`
- `audits/non_official_local_metrics_calculator_v0/`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Protected surfaces confirmed unchanged:

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
- `benchmark_spec/`
- `project_control/MIGRATION_MASTER_PLAN.md`
- `project_control/DECISION_LOG.md`
- skill folders

Local metrics smoke outputs were written under ignored `runs/user/*/metrics/` directories and were not committed.
