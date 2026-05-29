# Command Log

Commands were run from `/home/tianci_gao/code/Rewritebench_v0` on branch `feature/case-package-v2-external-schema`.

## Preflight

```bash
pwd
git branch --show-current
git status -sb
```

## Project-Control Reads

```bash
sed -n '1,200p' project_control/MIGRATION_MASTER_PLAN.md
sed -n '1,200p' project_control/MIGRATION_STATUS.md
sed -n '1,200p' project_control/DECISION_LOG.md
sed -n '1,200p' project_control/MIGRATION_RUN_LOG.md
```

## Source Inventory Reads

```bash
python - <<'PY'
import csv
for p in [
    'audits/pocr_candidate_sql_inventory_v0/candidate_root_inventory.csv',
    'audits/pocr_candidate_sql_inventory_v0/candidate_file_inventory.csv',
]:
    with open(p, newline='') as f:
        print(p, next(csv.reader(f)))
PY
```

The reconciliation CSVs were generated from `audits/pocr_candidate_sql_inventory_v0/candidate_root_inventory.csv`; no broad `runs/user` rescan was performed.

## Validation Commands

```bash
python - <<'PY'
import csv
from pathlib import Path
base = Path('audits/pocr_paper_table_route_candidate_reconciliation_v0')
for path in base.glob('*.csv'):
    with path.open(newline='') as f:
        rows = list(csv.DictReader(f))
    print(path, len(rows))
PY

python - <<'PY'
from pathlib import Path
base = Path('audits/pocr_paper_table_route_candidate_reconciliation_v0')
for path in base.glob('*.md'):
    assert path.read_text(encoding='utf-8').strip(), path
    print(path)
PY

git status --short -- runs/user
git diff --name-status -- runs/user cases output reports results
test ! -e output
git diff --check
git diff --name-only
git diff --cached --name-only
```

No live API, API-key, annotation-generation, DB/checker/timing, baseline, verifier, official metrics, paper rendering, or leaderboard commands were run.
