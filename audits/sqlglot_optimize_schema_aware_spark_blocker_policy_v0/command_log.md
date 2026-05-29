# Command Log

Commands run for this task:

```bash
git status -sb
git branch --show-current
git fetch origin main feature/case-package-v2-external-schema
git show origin/feature/case-package-v2-external-schema:project_control/DECISION_LOG.md | rg 'D033|D034|D035'
test -d audits/sqlglot_optimize_schema_aware_post_array_any_tri_engine_rerun_v0
test -d audits/sqlglot_optimize_schema_aware_bounded_tri_engine_blocker_triage_v0
test -d audits/sqlglot_optimize_schema_aware_mysql_array_any_fail_closed_v0
git status --porcelain -- runs/user output reports results
sed -n '1,220p' audits/sqlglot_optimize_schema_aware_post_array_any_tri_engine_rerun_v0/per_row_execution_checker_status.csv
python -m json.tool audits/sqlglot_optimize_schema_aware_post_array_any_tri_engine_rerun_v0/diagnostic_summary.json
python -m json.tool /tmp/sqlrb_sqlglot_optimize_schema_aware_post_array_any_tri_engine_rerun_v0/runtime/sqlglot_optimize_schema_aware_post_array_any_tri_engine_rerun_v0/workspaces/CONS_0005/spark/checker/mismatch_summary.json
python -m json.tool /tmp/sqlrb_sqlglot_optimize_schema_aware_post_array_any_tri_engine_rerun_v0/runtime/sqlglot_optimize_schema_aware_post_array_any_tri_engine_rerun_v0/workspaces/CONS_0036/spark/checker/mismatch_summary.json
sed -n '1,160p' /tmp/sqlrb_sqlglot_optimize_schema_aware_post_array_any_tri_engine_rerun_v0/runtime/sqlglot_optimize_schema_aware_post_array_any_tri_engine_rerun_v0/workspaces/CONS_0005/spark/execution/source_query.sql
sed -n '1,160p' /tmp/sqlrb_sqlglot_optimize_schema_aware_post_array_any_tri_engine_rerun_v0/runtime/sqlglot_optimize_schema_aware_post_array_any_tri_engine_rerun_v0/workspaces/CONS_0005/spark/execution/candidate_query.sql
sed -n '1,80p' /tmp/sqlrb_sqlglot_optimize_schema_aware_post_array_any_tri_engine_rerun_v0/runtime/sqlglot_optimize_schema_aware_post_array_any_tri_engine_rerun_v0/workspaces/CONS_0005/spark/execution/source_result.jsonl
sed -n '1,80p' /tmp/sqlrb_sqlglot_optimize_schema_aware_post_array_any_tri_engine_rerun_v0/runtime/sqlglot_optimize_schema_aware_post_array_any_tri_engine_rerun_v0/workspaces/CONS_0005/spark/execution/candidate_result.jsonl
sed -n '1,160p' /tmp/sqlrb_sqlglot_optimize_schema_aware_post_array_any_tri_engine_rerun_v0/runtime/sqlglot_optimize_schema_aware_post_array_any_tri_engine_rerun_v0/workspaces/CONS_0036/spark/execution/source_query.sql
sed -n '1,160p' /tmp/sqlrb_sqlglot_optimize_schema_aware_post_array_any_tri_engine_rerun_v0/runtime/sqlglot_optimize_schema_aware_post_array_any_tri_engine_rerun_v0/workspaces/CONS_0036/spark/execution/candidate_query.sql
sed -n '1,80p' /tmp/sqlrb_sqlglot_optimize_schema_aware_post_array_any_tri_engine_rerun_v0/runtime/sqlglot_optimize_schema_aware_post_array_any_tri_engine_rerun_v0/workspaces/CONS_0036/spark/execution/source_result.jsonl
sed -n '1,80p' /tmp/sqlrb_sqlglot_optimize_schema_aware_post_array_any_tri_engine_rerun_v0/runtime/sqlglot_optimize_schema_aware_post_array_any_tri_engine_rerun_v0/workspaces/CONS_0036/spark/execution/candidate_result.jsonl
python -m json.tool /tmp/sqlrb_sqlglot_optimize_schema_aware_post_array_any_tri_engine_rerun_v0/runtime/sqlglot_optimize_schema_aware_post_array_any_tri_engine_rerun_v0/workspaces/CONS_0005/spark/checker/checker_result.json
python -m json.tool /tmp/sqlrb_sqlglot_optimize_schema_aware_post_array_any_tri_engine_rerun_v0/runtime/sqlglot_optimize_schema_aware_post_array_any_tri_engine_rerun_v0/workspaces/CONS_0036/spark/checker/checker_result.json
python - <<'PY'
from pathlib import Path
root = Path('audits/sqlglot_optimize_schema_aware_spark_blocker_policy_v0')
empty = [p.name for p in root.glob('*.md') if not p.read_text(encoding='utf-8').strip()]
assert not empty, empty
PY
git diff --check
git status --porcelain -- runs/user output reports results
git status -sb
```

No experiment rerun, timing run, verifier run, or checker change was performed for this task.

Validation results:

- Audit Markdown validation passed.
- `git diff --check` passed.
- Protected path status checks produced no `runs/user`, repository-level `output`, top-level `reports`, or top-level `results` artifacts.
