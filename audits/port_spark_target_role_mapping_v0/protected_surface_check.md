# Protected Surface Check

Allowed changed surfaces:
- 9 Common-core PORT `manifest.yaml` files, limited to `local_diagnostic.engine_roles.spark` metadata.
- `src/sql_rewrite_bench/engine_execution.py` for Spark target-engine role consumption.
- `examples/user/port_spark_target_reference_adapter.py`.
- Tests under `tests/user_entry/`.
- Audit packet under `audits/port_spark_target_role_mapping_v0/`.
- `project_control/MIGRATION_STATUS.md`.
- `project_control/MIGRATION_RUN_LOG.md`.

Protected surfaces checked:
- SQL files modified: no.
- Schema files modified: no.
- Checker config files modified: no.
- Validation files modified: no.
- `case_sets/` changed: no.
- `reports/` changed: no.
- `results/` changed: no.
- Denominator scaffolds changed: no.
- Paper results changed: no.
- Raw retained evidence changed: no.
- `.github/workflows/` changed: no.
- Root metadata files changed: no.
- Release tags or export branches created: no.

Local run outputs:
- `runs/user/port_spark_target_reference_controlled/`: not committed.
- `runs/user/port_spark_unsupported_role_check/`: not committed.
- `runs/user/port_pg_forward_preservation_after_spark_roles/`: not committed.
- `runs/user/port_mysql_reverse_preservation_after_spark_roles/`: not committed.
- `runs/user/spark_two_case_regression_after_port_spark_roles/`: not committed.

Protected-surface validation command is recorded in `command_log.md`.
