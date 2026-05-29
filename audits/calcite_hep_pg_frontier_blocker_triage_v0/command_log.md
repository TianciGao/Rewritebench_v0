# Command Log

Preflight:

```bash
git status -sb
git branch --show-current
git fetch origin main feature/case-package-v2-external-schema
git merge-base --is-ancestor 64b645772397b763139f42dd8bc9fc2486393bff HEAD
git show origin/main:project_control/MIGRATION_MASTER_PLAN.md
git show origin/main:project_control/MIGRATION_STATUS.md
git show origin/main:project_control/DECISION_LOG.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_MASTER_PLAN.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_STATUS.md
git show origin/feature/case-package-v2-external-schema:project_control/DECISION_LOG.md
rg -n "D033|D034|D035" project_control/DECISION_LOG.md
test -f baselines/calcite_hep_fail_closed/adapter.py
git status --porcelain -- runs/user output reports results
```

Source audit review:

```bash
sed -n '1,220p' audits/calcite_hep_pg_bounded_candidate_generation_v0/fail_closed_review.md
sed -n '1,220p' audits/calcite_hep_pg_execution_checker_diagnostic_v0/failure_bucket_review.md
sed -n '1,220p' audits/calcite_hep_pg_execution_checker_diagnostic_v0/schema_fallback_review.md
sed -n '1,220p' audits/calcite_hep_pg_local_metrics_projection_v0/blocker_summary.md
python - <<'PY'
import csv
from pathlib import Path
G=list(csv.DictReader(Path('audits/calcite_hep_pg_bounded_candidate_generation_v0/per_row_candidate_status.csv').open()))
E=list(csv.DictReader(Path('audits/calcite_hep_pg_execution_checker_diagnostic_v0/per_row_execution_checker_status.csv').open()))
ids={r['case_id'] for r in E if r['failure_bucket']!='none'}
ids.update(r['case_id'] for r in G if r['candidate_review_status']=='generated_parse_only_schema_fallback_review')
for cid in sorted(ids):
    g=next(r for r in G if r['case_id']==cid)
    e=next(r for r in E if r['case_id']==cid)
    print(cid, g['blocker_category'], g['candidate_review_status'], e['failure_bucket'], e['candidate_origin'])
PY
```

Validation:

```bash
python - <<'PY'
import csv,json
from collections import Counter
from pathlib import Path
root=Path('audits/calcite_hep_pg_frontier_blocker_triage_v0')
md=list(root.glob('*.md'))
empty=[p.name for p in md if not p.read_text(encoding='utf-8').strip()]
rows=list(csv.DictReader((root/'frontier_inventory.csv').open()))
summary=json.loads((root/'frontier_summary.json').read_text())
stage=Counter(r['prior_stage_status'].split(';')[0] for r in rows)
assert not empty
assert len(rows)==20
assert stage==Counter({'no_candidate':7,'mismatch':3,'source_execution_failed':2,'candidate_execution_failed':8})
assert summary['frontier_rows']==20
assert summary['tri_engine_full_120_ready'] is False
PY
git diff --check
git status --porcelain -- runs/user output reports results
git status -sb
```

Validation result: passed.
