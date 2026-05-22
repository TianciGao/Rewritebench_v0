# Command Log

Preflight:

```bash
git status -sb
git branch --show-current
git log --oneline -20
```

Project-control files read:

```bash
sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md
sed -n '1,260p' project_control/MIGRATION_STATUS.md
sed -n '1,220p' project_control/DECISION_LOG.md
tail -n 160 project_control/MIGRATION_RUN_LOG.md
sed -n '1,220p' project_control/USER_ENTRY_LOCAL_EVALUATION_ARCHITECTURE_PLAN.md
sed -n '1,220p' project_control/PORT_CROSS_DIALECT_DIAGNOSTIC_EXECUTION_PLAN.md
```

Audit packets read:

```bash
audits/user_entry_pg_mysql_local_diagnostic_closeout_v0/README.md
audits/user_entry_pg_mysql_bounded_local_diagnostic_rerun_v0/README.md
audits/mysql_same_engine_backend_v0/README.md
audits/common_core_mysql_local_diagnostic_v0/README.md
audits/port_bidirectional_cross_dialect_closeout_v0/README.md
audits/port_reverse_cross_dialect_mysql_target_diagnostic_v0/README.md
audits/port_cross_dialect_checker_normalization_v0/README.md
audits/spark_backend_design_v0/README.md
audits/spark_fail_closed_skeleton_v0/README.md
```

Implementation inventory read:

```bash
src/sql_rewrite_bench/user_run.py
src/sql_rewrite_bench/engine_execution.py
src/sql_rewrite_bench/postgres_execution.py
src/sql_rewrite_bench/mysql_execution.py
src/sql_rewrite_bench/spark_execution.py
src/sql_rewrite_bench/local_result_checker.py
src/sql_rewrite_bench/user_ledger.py
src/sql_rewrite_bench/user_quality_report.py
src/sql_rewrite_bench/tag_slices.py
scripts/dev/check_local_engine_env.py
docs/LOCAL_ENGINE_SETUP.md
```

Validation:

```bash
git diff --check
python - <<'PY'
# CSV/JSON/Markdown sanity checks for audit files
PY
python - <<'PY'
# Protected-surface diff check
PY
git status -sb
```

No local diagnostic runs were executed and no `runs/user/` outputs were created.
