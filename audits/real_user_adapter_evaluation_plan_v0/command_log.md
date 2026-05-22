# Command Log

Preflight:

- `git status -sb && git branch --show-current && git log --oneline -8`

Context reads:

- `sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md`
- `tail -n 90 project_control/MIGRATION_STATUS.md`
- `tail -n 120 project_control/MIGRATION_RUN_LOG.md`
- `sed -n '1,220p' project_control/DECISION_LOG.md`
- `sed -n '1,260p' project_control/USER_ENTRY_LOCAL_EVALUATION_ARCHITECTURE_PLAN.md`
- Read `audits/tri_engine_user_entry_local_diagnostic_closeout_v0/`.
- Read `audits/port_spark_numeric_normalization_v0/`.
- Read `audits/user_entry_pg_mysql_bounded_local_diagnostic_rerun_v0/`.
- Read `audits/port_bidirectional_cross_dialect_closeout_v0/`.
- Read `audits/common_core_spark_local_diagnostic_v0/`.
- Inspected current adapter environment/capture behavior in `src/sql_rewrite_bench/adapter_runner.py`, `src/sql_rewrite_bench/user_run_schema.py`, `examples/user/noop_adapter.py`, and focused user-entry tests.

Rerun status:

- No real user adapter run was performed.
- No local diagnostic rerun was performed.

Validation:

- Project-control readability check.
- Audit Markdown/CSV/JSON sanity checks for `audits/real_user_adapter_evaluation_plan_v0/`.
- `git diff --check`.
- Protected-surface diff check.
- Git status/staging check confirming no `runs/user/` outputs are staged or committed.
