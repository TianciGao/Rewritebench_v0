# Command Log

Task: `common_core_tri_engine_sqlglot_noop_local_diagnostic_snapshot_v0`

Branch: `feature/case-package-v2-external-schema`

## Preflight

```bash
git status -sb
git branch --show-current
git log --oneline -8
```

Starting state was clean and on `feature/case-package-v2-external-schema`, up to date with origin.

Environment check:

```bash
source ~/code/sql-rewrite-bench/.venv/bin/activate
source scripts/env_postgres.local.sh
source scripts/env_mysql.local.sh
source scripts/env_spark.local.sh
export PYTHONPATH=src
python scripts/dev/check_local_engine_env.py
```

Result:

- PostgreSQL probe: ok.
- MySQL probe: ok.
- Spark readiness: PySpark available, `PYSPARK_PYTHON` set, `SQLRB_SPARK_MASTER` set, backend status live through PySpark.
- No secrets printed.

SQLGlot dependency check:

```bash
python - <<'PY'
import sqlglot
print(sqlglot.__version__)
PY
```

Result: `30.2.1`.

## Context Read

Read the required project-control, SQLGlot, and recent audit context:

- `project_control/MIGRATION_MASTER_PLAN.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/MIGRATION_RUN_LOG.md`
- `project_control/DECISION_LOG.md`
- `project_control/USER_ENTRY_LOCAL_EVALUATION_ARCHITECTURE_PLAN.md`
- `baselines/sqlglot/README.md`
- `audits/tri_engine_user_entry_local_diagnostic_closeout_v0/`
- `audits/sqlglot_user_adapter_bounded_smoke_v0/`
- `audits/sqlglot_context_free_optimize_doc_warning_v0/`

## Diagnostic Runs

PostgreSQL:

```bash
python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --engine postgres \
  --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route noop" \
  --out runs/user/common_core_sqlglot_noop_postgres_snapshot \
  --enable-db-execution \
  --enable-checker
```

Result: completed, selected rows 40, candidate generated rows 35.

MySQL:

```bash
python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --engine mysql \
  --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route noop" \
  --out runs/user/common_core_sqlglot_noop_mysql_snapshot \
  --enable-db-execution \
  --enable-checker
```

Result: completed, selected rows 40, candidate generated rows 40.

Spark:

```bash
python -m sql_rewrite_bench.user_run \
  --case-set common_core_v0 \
  --engine spark \
  --adapter-command "python baselines/sqlglot/sqlglot_user_adapter.py --route noop" \
  --out runs/user/common_core_sqlglot_noop_spark_snapshot \
  --enable-db-execution \
  --enable-checker
```

Result: completed, selected rows 40, candidate generated rows 40. Spark logged fail-visible local candidate execution errors for failed rows; the runner completed and wrote ledger/failure artifacts.

## Inspection

Inspected:

- `selected_cases.csv`
- `ledger.csv`
- `failures.csv`
- `summary.json`
- `quality_summary.json`
- `report.md`
- `quality_report.md`
- `tag_slices.csv`

Generated audit summaries from those local run artifacts.

## Validation

Validation commands:

```bash
PYTHONPATH=src python - <<'PY'
from pathlib import Path
for path in [
    Path("project_control/MIGRATION_STATUS.md"),
    Path("project_control/MIGRATION_RUN_LOG.md"),
]:
    text = path.read_text(encoding="utf-8")
    assert "common_core_tri_engine_sqlglot_noop_local_diagnostic_snapshot_v0" in text
PY

PYTHONPATH=src python - <<'PY'
import csv, json
from pathlib import Path
base = Path("audits/common_core_tri_engine_sqlglot_noop_local_diagnostic_snapshot_v0")
json.loads((base / "status_summary.json").read_text(encoding="utf-8"))
for name in ["route_summary.csv", "engine_summary.csv", "failure_buckets.csv", "tag_slice_summary.csv"]:
    with (base / name).open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
        assert rows, name
for name in ["README.md", "command_log.md", "protected_surface_check.md", "boundary_checklist.md"]:
    text = (base / name).read_text(encoding="utf-8")
    assert text.startswith("#"), name
PY

git diff --check
```

Validation result: passed.
