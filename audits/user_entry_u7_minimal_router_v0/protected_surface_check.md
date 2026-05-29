# Protected Surface Check

## Allowed Changes

- `src/sql_rewrite_bench/engine_execution.py`
- `src/sql_rewrite_bench/mysql_execution.py`
- `src/sql_rewrite_bench/spark_execution.py`
- `src/sql_rewrite_bench/user_run.py`
- `tests/user_entry/test_candidate_preflight.py`
- `tests/user_entry/test_engine_execution_router.py`
- `audits/user_entry_u7_minimal_router_v0/*`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

## Protected Surfaces

No changes were made to:

- `cases/`
- manifests
- `sql/`
- `schema/`
- `checker/`
- `validation/`
- `case_sets/`
- `inventory/`
- `reports/`
- `results/`
- `benchmark_spec/`
- `repository_spec/`
- denominator scaffolds
- paper results
- raw retained evidence

## Boundary Result

Protected-surface check passed. U7 changed only allowed source/test/audit/project-control files.
