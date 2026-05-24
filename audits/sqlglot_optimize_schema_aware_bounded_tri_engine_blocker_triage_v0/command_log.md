# Command Log

Commands run for preflight and inspection:

```bash
git status -sb
git branch --show-current
git fetch origin main feature/case-package-v2-external-schema
git merge-base --is-ancestor 10f9ac9ac07703ab62a980e6b19f8d34aa65b11f HEAD
git show origin/main:project_control/MIGRATION_MASTER_PLAN.md | sed -n '1,80p'
git show origin/main:project_control/MIGRATION_STATUS.md | tail -n 40
git show origin/main:project_control/DECISION_LOG.md | rg -n "D033|D034|D035"
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_MASTER_PLAN.md | sed -n '1,80p'
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_STATUS.md | tail -n 60
git show origin/feature/case-package-v2-external-schema:project_control/DECISION_LOG.md | rg -n "D033|D034|D035"
test -d audits/sqlglot_optimize_schema_aware_bounded_tri_engine_execution_checker_v0
test -d baselines/sqlglot
git status --porcelain -- runs/user output reports results
sed -n '1,220p' audits/sqlglot_optimize_schema_aware_bounded_tri_engine_execution_checker_v0/per_row_execution_checker_status.csv
cat audits/sqlglot_optimize_schema_aware_bounded_tri_engine_execution_checker_v0/diagnostic_summary.json
find /tmp/sqlrb_sqlglot_optimize_schema_aware_bounded_tri_engine_execution_checker_v0 -maxdepth 5 -type f | sort | rg 'CONS_0005|CONS_0036|mismatch|candidate.sql|stderr|stdout'
sed -n '1,120p' /tmp/sqlrb_sqlglot_optimize_schema_aware_bounded_tri_engine_execution_checker_v0/runtime/sqlglot_optimize_schema_aware_bounded_tri_engine_execution_checker_v0/candidate_sql/CONS_0005__mysql.sql
cat /tmp/sqlrb_sqlglot_optimize_schema_aware_bounded_tri_engine_execution_checker_v0/runtime/sqlglot_optimize_schema_aware_bounded_tri_engine_execution_checker_v0/workspaces/CONS_0005/mysql/adapter_stderr.txt
cat /tmp/sqlrb_sqlglot_optimize_schema_aware_bounded_tri_engine_execution_checker_v0/runtime/sqlglot_optimize_schema_aware_bounded_tri_engine_execution_checker_v0/workspaces/CONS_0005/mysql/execution/mysql_same_engine/candidate_error.txt
cat /tmp/sqlrb_sqlglot_optimize_schema_aware_bounded_tri_engine_execution_checker_v0/runtime/sqlglot_optimize_schema_aware_bounded_tri_engine_execution_checker_v0/workspaces/CONS_0005/spark/checker/mismatch_summary.json
cat /tmp/sqlrb_sqlglot_optimize_schema_aware_bounded_tri_engine_execution_checker_v0/runtime/sqlglot_optimize_schema_aware_bounded_tri_engine_execution_checker_v0/workspaces/CONS_0036/spark/checker/mismatch_summary.json
cat /tmp/sqlrb_sqlglot_optimize_schema_aware_bounded_tri_engine_execution_checker_v0/runtime/sqlglot_optimize_schema_aware_bounded_tri_engine_execution_checker_v0/workspaces/CONS_0005/spark/execution/source_result.jsonl
cat /tmp/sqlrb_sqlglot_optimize_schema_aware_bounded_tri_engine_execution_checker_v0/runtime/sqlglot_optimize_schema_aware_bounded_tri_engine_execution_checker_v0/workspaces/CONS_0005/spark/execution/candidate_result.jsonl
cat /tmp/sqlrb_sqlglot_optimize_schema_aware_bounded_tri_engine_execution_checker_v0/runtime/sqlglot_optimize_schema_aware_bounded_tri_engine_execution_checker_v0/workspaces/CONS_0036/spark/execution/source_result.jsonl
cat /tmp/sqlrb_sqlglot_optimize_schema_aware_bounded_tri_engine_execution_checker_v0/runtime/sqlglot_optimize_schema_aware_bounded_tri_engine_execution_checker_v0/workspaces/CONS_0036/spark/execution/candidate_result.jsonl
```

Validation commands are recorded after validation in `project_control/MIGRATION_RUN_LOG.md`.

Notes:

- `origin/main` did not contain D033/D034/D035 in the searched decision log; `origin/feature/case-package-v2-external-schema` did.
- No diagnostic rerun was needed.

