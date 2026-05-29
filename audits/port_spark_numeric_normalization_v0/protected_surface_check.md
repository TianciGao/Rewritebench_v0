# Protected Surface Check

Allowed changed surfaces used:
- `src/sql_rewrite_bench/local_result_checker.py`
- `src/sql_rewrite_bench/user_run.py` for the resolved-role opt-in pass-through to the checker.
- `tests/user_entry/test_cross_dialect_checker_normalization.py`
- `audits/port_spark_numeric_normalization_v0/`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Protected surfaces checked:
- SQL files modified: no.
- Case manifests modified: no.
- Schema files modified: no.
- Checker YAML/config files modified: no.
- Case validation scripts modified: no.
- `case_sets/` changed: no.
- `inventory/` changed: no.
- `reports/` changed: no.
- `results/` changed: no.
- `benchmark_spec/` changed: no.
- `repository_spec/` changed: no.
- Raw retained evidence changed: no.
- `project_control/MIGRATION_MASTER_PLAN.md` changed: no.
- `project_control/DECISION_LOG.md` changed: no.
- Release tags/export branches created: no.

Local run outputs were created under `runs/user/` and are ignored/untracked; they are not staged or committed.
