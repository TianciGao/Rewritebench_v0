# Command Log

Preflight and context:

```bash
git status -sb
git branch --show-current
git log --oneline -8
sed -n '250,315p' src/sql_rewrite_bench/spark_execution.py
sed -n '80,230p' src/sql_rewrite_bench/candidate_preflight.py
sed -n '1,220p' audits/common_core_tri_engine_sqlglot_noop_local_diagnostic_snapshot_v0/status_summary.json
sed -n '1,220p' audits/common_core_sqlglot_noop_failure_triage_v0/recommendation.md
```

Artifact inspection:

```bash
PYTHONPATH=src python - <<'PY'
from pathlib import Path
import csv

root = Path('runs/user/common_core_sqlglot_noop_spark_snapshot')
ids = ['PERF_0008','PERF_0013','PERF_0017','PERF_0019','PERF_0024','PERF_0082']
rows = {r['case_id']: r for r in csv.DictReader((root / 'ledger.csv').open(newline='', encoding='utf-8'))}
for cid in ids:
    row = rows[cid]
    artifact = Path(row['db_artifact_dir'])
    print(cid, row['candidate_preflight_status'], row['source_execution_status'], row['candidate_execution_status'])
    print((artifact / 'candidate_error.txt').read_text(encoding='utf-8').strip())
PY
```

Statement-boundary diagnostic:

```bash
PYTHONPATH=src python - <<'PY'
from pathlib import Path
import csv
from sql_rewrite_bench.spark_execution import _split_sql_statements
from sql_rewrite_bench.candidate_preflight import _semicolon_positions, _has_multiple_statements

root = Path('runs/user/common_core_sqlglot_noop_spark_snapshot')
ids = ['PERF_0008','PERF_0013','PERF_0017','PERF_0019','PERF_0024','PERF_0082']
rows = {r['case_id']: r for r in csv.DictReader((root / 'ledger.csv').open(newline='', encoding='utf-8'))}
for cid in ids:
    artifact = Path(rows[cid]['db_artifact_dir'])
    candidate = (artifact / 'candidate_query.sql').read_text(encoding='utf-8')
    source = (artifact / 'source_query.sql').read_text(encoding='utf-8')
    print(cid, candidate.count(';'), len(_semicolon_positions(candidate)), len(_split_sql_statements(candidate)), source.count(';'), len(_split_sql_statements(source)), _has_multiple_statements(candidate))
PY
```

No Common-core rerun, SQLGlot optimize run, timing, official metric computation, reports/results update, retained-evidence promotion, or leaderboard generation was performed.

Validation:

```bash
python - <<'PY'
from pathlib import Path
import csv

base = Path('audits/spark_sqlglot_noop_statement_preflight_triage_v0')
for csv_path in [base / 'affected_rows.csv', base / 'root_cause_matrix.csv']:
    with csv_path.open(newline='', encoding='utf-8') as handle:
        list(csv.DictReader(handle))
for md_path in base.glob('*.md'):
    text = md_path.read_text(encoding='utf-8')
    assert text.strip(), md_path
print('audit files parse')
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
