# Command Log

Preflight:

```bash
git status -sb
git branch --show-current
git status --porcelain -- runs/user output reports results
git fetch origin main feature/case-package-v2-external-schema
git merge-base --is-ancestor 2290122f72fd0fddd4b0cdb71e7698d875a4f1ec HEAD
rg -n "D033|D034|D035" project_control/DECISION_LOG.md
git show origin/main:project_control/MIGRATION_MASTER_PLAN.md
git show origin/main:project_control/MIGRATION_STATUS.md
git show origin/main:project_control/DECISION_LOG.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_MASTER_PLAN.md
```

Environment and runner inspection:

```bash
python scripts/dev/check_local_engine_env.py
sed -n '1,180p' src/sql_rewrite_bench/user_run.py
sed -n '360,540p' src/sql_rewrite_bench/user_run.py
sed -n '1580,1728p' src/sql_rewrite_bench/engine_execution.py
```

Execution/checker run:

```bash
PYTHONPATH=src python audits/sqlglot_optimize_schema_aware_bounded_tri_engine_execution_checker_v0/run_bounded_execution_checker.py
```

Failure inspection:

```bash
sed -n '1,240p' /tmp/sqlrb_sqlglot_optimize_schema_aware_bounded_tri_engine_execution_checker_v0/runtime/sqlglot_optimize_schema_aware_bounded_tri_engine_execution_checker_v0/candidate_sql/CONS_0005__mysql.sql
sed -n '1,120p' /tmp/sqlrb_sqlglot_optimize_schema_aware_bounded_tri_engine_execution_checker_v0/runtime/sqlglot_optimize_schema_aware_bounded_tri_engine_execution_checker_v0/workspaces/CONS_0005/mysql/execution/mysql_same_engine/candidate_error.txt
find /tmp/sqlrb_sqlglot_optimize_schema_aware_bounded_tri_engine_execution_checker_v0/runtime/sqlglot_optimize_schema_aware_bounded_tri_engine_execution_checker_v0/workspaces/CONS_0005/spark/checker -type f -maxdepth 2 -print -exec sed -n '1,160p' {} \;
find /tmp/sqlrb_sqlglot_optimize_schema_aware_bounded_tri_engine_execution_checker_v0/runtime/sqlglot_optimize_schema_aware_bounded_tri_engine_execution_checker_v0/workspaces/CONS_0036/spark/checker -type f -maxdepth 2 -print -exec sed -n '1,160p' {} \;
```

Validation commands are recorded in the run log after final validation.

Validation:

```bash
python - <<'PY'
# Validated per_row_execution_checker_status.csv required headers/9 rows
# and diagnostic_summary.json expected aggregate counts.
PY
pytest tests/user_entry/test_sqlglot_adapter.py tests/user_entry/test_local_timing.py -q
python -m py_compile audits/sqlglot_optimize_schema_aware_bounded_tri_engine_execution_checker_v0/run_bounded_execution_checker.py
find audits/sqlglot_optimize_schema_aware_bounded_tri_engine_execution_checker_v0 -name '*.md' -type f -empty -print
git diff --check
git status -sb
git status --porcelain -- runs/user output reports results src tests baselines cases case_sets schemas inventory
```
