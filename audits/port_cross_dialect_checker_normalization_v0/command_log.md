# Command Log

Repository snapshot:

```bash
git status -sb
git branch --show-current
git log --oneline -12
```

Environment:

```bash
source scripts/env_mysql.local.sh
source scripts/env_postgres.local.sh
python scripts/dev/check_local_engine_env.py
```

Context read:

```bash
sed -n '...' project_control/MIGRATION_MASTER_PLAN.md
sed -n '...' project_control/MIGRATION_STATUS.md
sed -n '...' project_control/DECISION_LOG.md
tail -n 130 project_control/MIGRATION_RUN_LOG.md
sed -n '...' project_control/PORT_CROSS_DIALECT_DIAGNOSTIC_EXECUTION_PLAN.md
sed -n '...' audits/port_cross_dialect_pg_target_reference_diagnostic_v0/README.md
python -m json.tool audits/port_cross_dialect_pg_target_reference_diagnostic_v0/live_run_summary.json
sed -n '...' audits/port_cross_dialect_pg_target_reference_diagnostic_v0/checker_outcome_summary.csv
sed -n '...' audits/port_cross_dialect_checker_normalization_audit_v0/*
sed -n '...' src/sql_rewrite_bench/local_result_checker.py
sed -n '...' src/sql_rewrite_bench/case_package_resolver.py
sed -n '...' src/sql_rewrite_bench/user_run.py
sed -n '...' src/sql_rewrite_bench/engine_execution.py
sed -n '...' src/sql_rewrite_bench/mysql_execution.py
sed -n '...' src/sql_rewrite_bench/postgres_execution.py
sed -n '...' src/sql_rewrite_bench/user_ledger.py
sed -n '...' src/sql_rewrite_bench/user_run_schema.py
sed -n '...' examples/user/port_postgres_target_reference_adapter.py
sed -n '...' tests/user_entry/*
```

Implementation and validation commands are summarized in `test_results.md`.

Protected-surface validation:

```bash
python - <<'PY'
# Compare changed paths against the task allowlist.
PY
git status --short --ignored runs/user/port_pg_target_reference_normalized
git diff --cached --name-only
```

Result: protected surface passed; local run output is ignored and unstaged.

Controlled rerun output was written to ignored local path `runs/user/port_pg_target_reference_normalized/` and must not be staged or committed.
