# Command Log

Preflight:

```bash
git status -sb
git branch --show-current
git log --oneline -8
```

Required context reads:

```bash
sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md
tail -90 project_control/MIGRATION_STATUS.md
tail -140 project_control/MIGRATION_RUN_LOG.md
sed -n '1,220p' project_control/DECISION_LOG.md
sed -n '1,260p' project_control/USER_ENTRY_LOCAL_EVALUATION_ARCHITECTURE_PLAN.md
sed -n '1,220p' audits/common_core_tri_engine_sqlglot_noop_local_diagnostic_snapshot_v0/README.md
sed -n '1,220p' audits/common_core_tri_engine_sqlglot_noop_local_diagnostic_snapshot_v0/status_summary.json
sed -n '1,220p' audits/common_core_sqlglot_noop_failure_triage_v0/README.md
sed -n '1,80p' audits/common_core_sqlglot_noop_failure_triage_v0/failure_triage_matrix.csv
sed -n '1,160p' audits/common_core_sqlglot_noop_failure_triage_v0/recommendation.md
sed -n '1,220p' audits/spark_sqlglot_noop_statement_preflight_triage_v0/README.md
sed -n '1,80p' audits/spark_sqlglot_noop_statement_preflight_triage_v0/affected_rows.csv
sed -n '1,220p' audits/spark_statement_boundary_comment_aware_patch_v0/README.md
sed -n '1,120p' audits/spark_statement_boundary_comment_aware_patch_v0/affected_rows_before_after.csv
sed -n '1,220p' audits/common_core_spark_sqlglot_noop_after_statement_patch_v0/README.md
sed -n '1,220p' audits/common_core_spark_sqlglot_noop_after_statement_patch_v0/status_summary.json
sed -n '1,80p' audits/common_core_spark_sqlglot_noop_after_statement_patch_v0/remaining_failures.csv
sed -n '1,180p' baselines/sqlglot/README.md
```

No reruns were performed:

- PostgreSQL rerun: no.
- MySQL rerun: no.
- Spark rerun: no.
- SQLGlot optimize run: no.
- Timing/speedup: no.
- Official metrics: no.
- Reports/results update: no.
- Retained-evidence promotion: no.
- Leaderboard output: no.

Validation:

```bash
python - <<'PY'
from pathlib import Path
import csv, json
base = Path('audits/sqlglot_noop_common_core_local_diagnostic_closeout_v0')
for csv_path in [
    base / 'engine_current_summary.csv',
    base / 'remaining_failure_matrix.csv',
    base / 'spark_before_after_patch_summary.csv',
]:
    with csv_path.open(newline='', encoding='utf-8') as handle:
        assert list(csv.DictReader(handle))
json.loads((base / 'closeout_status.json').read_text(encoding='utf-8'))
for md_path in base.glob('*.md'):
    assert md_path.read_text(encoding='utf-8').strip()
print('audit markdown/csv/json sanity passed')
PY
python - <<'PY'
from pathlib import Path
for path in ['project_control/MIGRATION_STATUS.md', 'project_control/MIGRATION_RUN_LOG.md']:
    assert Path(path).read_text(encoding='utf-8').strip()
print('project-control readable')
PY
git diff --check
git diff --name-only
git status -sb
```
