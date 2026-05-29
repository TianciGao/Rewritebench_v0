# Protected Surface Check

Allowed modified surfaces:

- `audits/common_core_spark_sqlglot_noop_after_statement_patch_v0/`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Protected surfaces not modified:

- `src/`
- `tests/`
- `baselines/sqlglot/`
- `cases/`
- manifests
- SQL files
- schemas
- checker configs
- validation scripts
- `case_sets/`
- `inventory/`
- `reports/`
- `results/`
- `benchmark_spec/`
- `repository_spec/`
- retained evidence
- `project_control/MIGRATION_MASTER_PLAN.md`
- `project_control/DECISION_LOG.md`
- `runs/user/` tracked outputs

Local run outputs were written only under:

`runs/user/common_core_spark_sqlglot_noop_after_statement_patch`

Those outputs are local diagnostics and are not staged or committed.
