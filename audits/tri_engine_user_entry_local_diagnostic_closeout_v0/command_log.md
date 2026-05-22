# Command Log

Preflight:

- `git status -sb && git branch --show-current && git log --oneline -12`

Context reads:

- `sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md`
- `tail -n 120 project_control/MIGRATION_STATUS.md`
- `tail -n 140 project_control/MIGRATION_RUN_LOG.md`
- `sed -n '1,220p' project_control/DECISION_LOG.md`
- `sed -n '1,260p' project_control/USER_ENTRY_LOCAL_EVALUATION_ARCHITECTURE_PLAN.md`
- Read summaries and machine-readable counts under `audits/port_spark_numeric_normalization_v0/`.
- Read summaries and machine-readable counts under `audits/user_entry_pg_mysql_bounded_local_diagnostic_rerun_v0/`.
- Read summaries and machine-readable counts under `audits/port_bidirectional_cross_dialect_closeout_v0/`.
- Read summaries and machine-readable counts under `audits/port_spark_target_role_mapping_v0/`.

Rerun status:

- No local diagnostic reruns were performed for this closeout. The packet uses the latest committed audit packets and local diagnostic summaries.

Validation:

- Project-control readability check.
- CSV/JSON/Markdown sanity checks for `audits/tri_engine_user_entry_local_diagnostic_closeout_v0/`.
- `git diff --check`
- Protected-surface diff check.
- Git status/staging check confirming no `runs/user/` outputs are staged or committed.
