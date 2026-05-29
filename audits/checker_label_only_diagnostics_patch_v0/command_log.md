# Command Log

```bash
git status -sb
git branch --show-current
git log --oneline -8
git merge-base --is-ancestor 6236ba8 HEAD
rg -n "checker_label_policy_design_v0" project_control/MIGRATION_STATUS.md project_control/MIGRATION_RUN_LOG.md
```

```bash
sed -n '1,220p' project_control/MIGRATION_MASTER_PLAN.md
sed -n '1,220p' project_control/MIGRATION_STATUS.md
tail -n 180 project_control/MIGRATION_RUN_LOG.md
sed -n '1,220p' project_control/DECISION_LOG.md
sed -n '1,220p' project_control/USER_ENTRY_LOCAL_EVALUATION_ARCHITECTURE_PLAN.md
```

```bash
find audits/mysql_label_policy_triage_v0 -maxdepth 1 -type f -print | sort
find audits/checker_label_policy_design_v0 -maxdepth 1 -type f -print | sort
find audits/sqlglot_noop_common_core_local_diagnostic_closeout_v0 -maxdepth 1 -type f -print | sort
sed -n '1,260p' src/sql_rewrite_bench/local_result_checker.py
sed -n '1,340p' src/sql_rewrite_bench/user_quality_report.py
find tests/user_entry -maxdepth 1 -type f -print | sort
```

```bash
PYTHONPATH=src pytest tests/user_entry/test_cross_dialect_checker_normalization.py -q
PYTHONPATH=src pytest tests/user_entry/test_quality_report.py -q
PYTHONPATH=src pytest tests/user_entry -q
```

```bash
printf 'PERF_0062\nPORT_0004\nPORT_0013\nPORT_0022\nPORT_0024\n' > /tmp/sqlrb_mysql_label_only_cases.txt
source ~/code/sql-rewrite-bench/.venv/bin/activate
source scripts/env_postgres.local.sh
source scripts/env_mysql.local.sh
source scripts/env_spark.local.sh
export PYTHONPATH=src
python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --engine mysql \
  --case-list /tmp/sqlrb_mysql_label_only_cases.txt \
  --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route noop" \
  --out runs/user/mysql_label_only_diagnostics_patch_check \
  --enable-db-execution \
  --enable-checker
```

```bash
PYTHONPATH=src python - <<'PY'
from pathlib import Path
import csv, json

root = Path('runs/user/mysql_label_only_diagnostics_patch_check')
case_ids = ['PERF_0062','PORT_0004','PORT_0013','PORT_0022','PORT_0024']
rows = {row['case_id']: row for row in csv.DictReader((root / 'ledger.csv').open(newline='', encoding='utf-8'))}
for cid in case_ids:
    row = rows[cid]
    mismatch_path = Path(row['mismatch_artifact_path'])
    payload = json.loads(mismatch_path.read_text(encoding='utf-8')) if mismatch_path.exists() else {}
    label = payload.get('label_diagnostics', {})
    print(cid, row['checker_status'], row['exact_status'], row['failure_bucket'], label)
print('quality diagnostic counts:', json.loads((root / 'quality_summary.json').read_text(encoding='utf-8')).get('diagnostic_counts'))
PY
```

Validation commands were run after audit and project-control writeback; see `protected_surface_check.md` for final validation summary.
