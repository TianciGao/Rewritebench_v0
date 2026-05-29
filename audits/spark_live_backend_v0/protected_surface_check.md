# Protected Surface Check

Allowed modified surfaces for this task:

- `src/sql_rewrite_bench/spark_execution.py`
- `src/sql_rewrite_bench/engine_execution.py`
- `scripts/dev/check_local_engine_env.py`
- `docs/LOCAL_ENGINE_SETUP.md`
- `scripts/env_spark.example.sh`
- `tests/user_entry/test_engine_execution_router.py`
- `audits/spark_live_backend_v0/*`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Protected surfaces confirmed unchanged:

- SQL files: unchanged.
- Manifest files: unchanged.
- Schema/checker/validation files: unchanged.
- `case_sets/`: unchanged.
- `inventory/`: unchanged.
- `reports/`: unchanged.
- `results/`: unchanged.
- `benchmark_spec/`: unchanged.
- `repository_spec/`: unchanged.
- Raw retained evidence: unchanged.
- Root metadata files: unchanged.
- `.github/workflows/`: unchanged.
- Release tags/export branches: not created.

Local `runs/user/` output from the fail-closed Spark smoke was removed before commit.
