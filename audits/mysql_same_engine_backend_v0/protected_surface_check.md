# Protected Surface Check

Allowed changed surfaces for this task:

- `src/sql_rewrite_bench/mysql_execution.py`
- `src/sql_rewrite_bench/engine_execution.py`
- `src/sql_rewrite_bench/user_run.py`
- Tests under `tests/user_entry/`
- `audits/mysql_same_engine_backend_v0/`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Protected surfaces confirmed unchanged:

- SQL files: unchanged.
- Manifest files: unchanged.
- Schema files: unchanged.
- Checker config files: unchanged.
- Validation files: unchanged.
- `case_sets/`: unchanged.
- `reports/` and `results/`: unchanged.
- Denominator scaffolds: unchanged.
- Paper results: unchanged.
- Case membership: unchanged.
- Raw retained evidence: unchanged.
- Docs/examples/scripts/workflows/root metadata: unchanged.
- Release tags/export branches: not created.

Local run outputs:

- `runs/user/mysql_same_engine_smoke/` was generated for local diagnostic inspection only.
- `runs/user/port_pg_target_reference_normalized_regression/` was generated for local regression inspection only.
- PostgreSQL smoke output directories were generated for validation only.
- These run outputs are ignored local artifacts and are not staged or committed.
