# Protected Surface Check

Allowed write surfaces for this task:

- User-entry source files under `src/sql_rewrite_bench/`
- `scripts/user/run_user_benchmark.py` if needed
- `docs/USER_BENCHMARK_GUIDE.md`
- Public smoke examples under `examples/`
- `tests/user_entry/`
- `audits/user_entry_external_schema_repair_v0/`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Protected surfaces that must remain unchanged:

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
- raw retained evidence
- `project_control/MIGRATION_MASTER_PLAN.md`
- `project_control/DECISION_LOG.md`

## Boundary Result

Final protected-surface diff check passed.

Changed paths were limited to:

- `src/sql_rewrite_bench/case_selection.py`
- `src/sql_rewrite_bench/user_run.py`
- `src/sql_rewrite_bench/postgres_execution.py`
- `docs/USER_BENCHMARK_GUIDE.md`
- `examples/user/noop_adapter.py`
- `tests/user_entry/test_case_selection.py`
- `tests/user_entry/test_db_checker_execution_mvp.py`
- `tests/user_entry/test_user_run_outputs.py`
- `audits/user_entry_external_schema_repair_v0/`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`

Protected surfaces unchanged:

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
- raw retained evidence
- `project_control/MIGRATION_MASTER_PLAN.md`
- `project_control/DECISION_LOG.md`

No live DB/checker execution, official metrics, paper table rendering, reports/results update, denominator change, paper result change, case membership change, raw legacy evidence change, or global leaderboard creation was performed.
