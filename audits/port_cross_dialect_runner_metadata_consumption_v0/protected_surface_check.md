# Protected Surface Check

Changed surfaces intended for P3:

- `src/sql_rewrite_bench/case_package_resolver.py`
- `src/sql_rewrite_bench/case_package_v2_resolver.py`
- `src/sql_rewrite_bench/engine_execution.py`
- `src/sql_rewrite_bench/tag_slices.py`
- `src/sql_rewrite_bench/user_ledger.py`
- `src/sql_rewrite_bench/user_run.py`
- `src/sql_rewrite_bench/user_run_schema.py`
- `tests/case_package_v2/test_case_package_v2_resolver.py`
- `tests/user_entry/test_port_local_diagnostic_metadata.py`
- `audits/port_cross_dialect_runner_metadata_consumption_v0/*`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Protected surfaces unchanged:

- SQL files unchanged.
- Manifest files unchanged.
- Schema files unchanged.
- Checker files unchanged.
- Validation files unchanged.
- `case_sets/` unchanged.
- `reports/` and `results/` unchanged.
- Denominator scaffolds unchanged.
- Paper results unchanged.
- Raw retained evidence unchanged.
- No release tag or export branch created.

Local run outputs under `runs/user/` were diagnostic only and are not intended for commit.
