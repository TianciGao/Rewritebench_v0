# Command Log

Preflight:

- `git status -sb && git branch --show-current && git log --oneline -8`

Context reads:

- `sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md`
- `tail -n 90 project_control/MIGRATION_STATUS.md`
- `tail -n 120 project_control/MIGRATION_RUN_LOG.md`
- `sed -n '1,260p' project_control/DECISION_LOG.md`
- `sed -n '1,260p' project_control/USER_ENTRY_LOCAL_EVALUATION_ARCHITECTURE_PLAN.md`
- `sed -n '1,240p' baselines/sqlglot/README.md`
- `sed -n '1,260p' baselines/sqlglot/sqlglot_user_adapter.py`
- `sed -n '1,220p' audits/sqlglot_user_adapter_bounded_smoke_v0/README.md`
- `cat audits/sqlglot_user_adapter_bounded_smoke_v0/status_summary.json`
- `cat audits/sqlglot_user_adapter_bounded_smoke_v0/route_summary.csv`

Artifact inspection:

- `sed -n '1,220p' cases/CONS/CONS_0005/sql/source.sql`
- Inspected `runs/user/sqlglot_optimize_pg_bounded_smoke/candidate_sql/CONS_0005__postgres.sql`.
- Inspected `runs/user/sqlglot_optimize_mysql_bounded_smoke/candidate_sql/CONS_0005__mysql.sql`.
- Inspected `runs/user/sqlglot_optimize_spark_bounded_smoke/candidate_sql/CONS_0005__spark.sql`.
- Inspected `CONS_0005` ledger rows and candidate execution errors under the three optimize smoke workspaces.

SQLGlot-only reproducer checks:

- Inspected `sqlglot.optimizer.optimize` signature and docstring with Python `inspect`.
- Ran a standalone SQLGlot reproducer over `CONS_0005` source for `postgres`, `mysql`, and `spark`.
- Tested parse/emit only, optimize without schema, optimize with dialect argument, optimize with schema, and optimize with schema plus dialect argument.

Rerun status:

- No `user_run` rerun was performed.
- No broader optimize trial was performed.

Validation:

- Project-control readability check.
- Audit Markdown/CSV/JSON sanity checks.
- `git diff --check`.
- Protected-surface diff check.
- Git status/staging check confirming no `runs/user/` outputs are staged or committed.
