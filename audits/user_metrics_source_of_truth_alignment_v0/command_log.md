# Command Log

Preflight:

```bash
git status -sb
git branch --show-current
git status --porcelain -- runs/user output reports results
git fetch origin main feature/case-package-v2-external-schema
```

Project-control reads:

```bash
git show origin/main:project_control/MIGRATION_MASTER_PLAN.md
git show origin/main:project_control/MIGRATION_STATUS.md
git show origin/main:project_control/DECISION_LOG.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_MASTER_PLAN.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_STATUS.md
git show origin/feature/case-package-v2-external-schema:project_control/DECISION_LOG.md
```

Code inspection:

```bash
rg -n "compute-local-metrics|local_metrics|compute_and_write_local_metrics|evaluate|output-root|run-id|collect-timing|enable-checker|enable-db" src/cli/main.py src/sql_rewrite_bench/local_metrics.py src/sql_rewrite_bench/user_run.py src/sql_rewrite_bench/user_output.py
sed -n '1,390p' src/cli/main.py
sed -n '1,720p' src/sql_rewrite_bench/local_metrics.py
sed -n '95,150p' src/sql_rewrite_bench/user_run.py
sed -n '720,790p' src/sql_rewrite_bench/user_run.py
sed -n '320,390p' src/sql_rewrite_bench/user_output.py
sed -n '1,180p' baselines/sqlglot/sqlglot_user_adapter.py
sed -n '1,180p' baselines/calcite_hep_fail_closed/adapter.py
```

CLI contract inspection:

```bash
python -m cli.main user evaluate --help
python -m cli.main user compute-local-metrics --help
python -m cli.main user show-output-schema
```

Audit packet classification:

```bash
find audits/<packet> -maxdepth 1 -type f
rg -n "local_metrics|compute_and_write_local_metrics|compute-local-metrics|route_card|diagnostic_gm|local_generation_rate|gm_speedup|comparison_table|projection" <reviewed audit packets>
find <reviewed audit packets> -name local_metrics_summary.json -o -name local_metrics_by_engine.csv -o -name local_metrics_by_pool.csv -o -name local_timing_speedup_rows.csv -o -name local_metrics_boundary.md
find <reviewed audit packets> -name ledger.csv -o -name config.yaml
```

Validation:

```bash
python - <<'PY'
import csv
from pathlib import Path
path = Path("audits/user_metrics_source_of_truth_alignment_v0/audit_output_classification.csv")
rows = list(csv.DictReader(path.open(newline="", encoding="utf-8")))
required = [
    "audit_packet",
    "route_or_scope",
    "reviewed_outputs",
    "standard_user_run_dir_present",
    "canonical_metrics_outputs_present",
    "manual_route_card_or_projection_present",
    "classification",
    "required_action",
    "notes",
]
assert rows and list(rows[0]) == required
assert len(rows) == 6
print("classification_csv_ok")
PY
git diff --check
git status -sb
git status --porcelain -- runs/user output reports results
```

Observed validation results:

- `audit_output_classification.csv` header validation passed.
- `audit_output_classification.csv` row count: 6.
- Empty-file check under the audit packet produced no output.
- `git diff --check`: passed.
- Protected-path status check for `runs/user`, repository-level `output`, top-level `reports`, top-level `results`, `src`, `tests`, `baselines`, `cases`, `case_sets`, `schemas`, and `inventory`: no output.
