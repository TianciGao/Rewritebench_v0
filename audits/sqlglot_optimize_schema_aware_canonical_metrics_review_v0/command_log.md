# Command Log

Preflight:

```bash
git status -sb
git branch --show-current
git fetch origin main feature/case-package-v2-external-schema
git merge-base --is-ancestor 521224fcc552a55727987f8dbf3b372290890da3 HEAD
wc -l project_control/MIGRATION_MASTER_PLAN.md project_control/MIGRATION_STATUS.md project_control/DECISION_LOG.md
rg "D033|D034|D035" project_control/DECISION_LOG.md
```

Canonical metrics existence and parse checks:

```bash
test -f runs/user/sqlglot_optimize_schema_aware_track_a_120_canonical_v0/metrics/local_metrics_summary.json
test -f runs/user/sqlglot_optimize_schema_aware_track_a_120_canonical_v0/metrics/local_metrics_by_engine.csv
test -f runs/user/sqlglot_optimize_schema_aware_track_a_120_canonical_v0/metrics/local_metrics_by_pool.csv
test -f runs/user/sqlglot_optimize_schema_aware_track_a_120_canonical_v0/metrics/local_timing_speedup_rows.csv
test -f runs/user/sqlglot_optimize_schema_aware_track_a_120_canonical_v0/metrics/local_metrics_boundary.md
python - <<'PY'
import csv, json
from pathlib import Path
root = Path("runs/user/sqlglot_optimize_schema_aware_track_a_120_canonical_v0/metrics")
json.loads((root / "local_metrics_summary.json").read_text())
list(csv.DictReader((root / "local_metrics_by_engine.csv").open(newline="")))
list(csv.DictReader((root / "local_metrics_by_pool.csv").open(newline="")))
list(csv.DictReader((root / "local_timing_speedup_rows.csv").open(newline="")))
PY
```

Final validation:

```bash
git diff --check
git status -sb
git status --porcelain -- runs/user output reports results
```
