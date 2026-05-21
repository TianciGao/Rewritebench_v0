# Protected Surface Check

Allowed changed surfaces:

- `src/sql_rewrite_bench/mysql_execution.py`
- `src/sql_rewrite_bench/engine_execution.py`
- `src/sql_rewrite_bench/user_run.py`
- `src/sql_rewrite_bench/user_run_schema.py`
- `tests/user_entry/`
- `audits/port_cross_dialect_mysql_backend_v0/`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Protected surfaces unchanged:

- SQL files
- manifests
- schema files
- checker files
- validation files
- `case_sets/`
- `reports/`
- `results/`
- `benchmark_spec/`
- `repository_spec/`
- raw retained evidence
- denominator scaffolds
- paper results
- root metadata files
- release tags and branches

Run output cleanup:

- `runs/user/p4_mysql_dry_run`: removed.
- `runs/user/p4_mysql_dummy_adapter`: removed.
- `runs/user/p4_mysql_port_targeted`: removed.

No local user-run outputs are staged or intended for commit.
