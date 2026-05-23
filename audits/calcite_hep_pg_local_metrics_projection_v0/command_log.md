# Command Log

Preflight and source inspection:

```bash
git status -sb
git branch --show-current
git fetch origin main feature/case-package-v2-external-schema
git merge-base --is-ancestor 245b19d1ae3f69ae1cd519434511407c3e3d33f0 HEAD
git show origin/main:project_control/MIGRATION_MASTER_PLAN.md
git show origin/main:project_control/MIGRATION_STATUS.md
git show origin/main:project_control/DECISION_LOG.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_MASTER_PLAN.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_STATUS.md
git show origin/feature/case-package-v2-external-schema:project_control/DECISION_LOG.md
rg -n "D033|D034|D035" project_control/DECISION_LOG.md
ls -d audits/calcite_hep_pg_bounded_candidate_generation_v0 audits/calcite_hep_pg_execution_checker_diagnostic_v0 audits/calcite_hep_pg_exact_timing_diagnostic_v0
test -f baselines/calcite_hep_fail_closed/adapter.py
git status --porcelain -- runs/user output reports results
```

Input audit review:

```bash
python - <<'PY'
import csv,json
from pathlib import Path
base=Path('audits')
for name, file in [('gen','calcite_hep_pg_bounded_candidate_generation_v0/diagnostic_summary.json'),('exec','calcite_hep_pg_execution_checker_diagnostic_v0/diagnostic_summary.json'),('timing','calcite_hep_pg_exact_timing_diagnostic_v0/diagnostic_summary.json')]:
    data=json.loads((base/file).read_text())
    print(name, json.dumps(data, sort_keys=True))
rows=list(csv.DictReader((base/'calcite_hep_pg_execution_checker_diagnostic_v0/per_row_execution_checker_status.csv').open()))
print('mismatches', [r['case_id'] for r in rows if r['mismatch']=='true'])
PY
```

Validation:

```bash
python - <<'PY'
import csv,json
from pathlib import Path
root=Path('audits/calcite_hep_pg_local_metrics_projection_v0')
md=list(root.glob('*.md'))
empty=[p.name for p in md if not p.read_text(encoding='utf-8').strip()]
card=json.loads((root/'route_card.json').read_text())
with (root/'route_card.csv').open(newline='', encoding='utf-8') as f:
    rows=list(csv.DictReader(f))
assert not empty
assert card['selected_rows']==40
assert card['generated_candidate_rows']==33
assert card['exact_rows']==20
assert len(rows)==1
assert rows[0]['method_id']=='calcite_hep_fail_closed'
PY
git diff --check
git status --porcelain -- runs/user output reports results
git status -sb
```

Validation result: passed.
