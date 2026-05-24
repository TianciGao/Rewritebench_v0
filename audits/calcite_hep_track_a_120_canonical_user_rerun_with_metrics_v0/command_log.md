# Command Log

Commands run:

```bash
git status -sb
git branch --show-current
git fetch origin main feature/case-package-v2-external-schema
git merge-base --is-ancestor a5443236d8eac9ff4dbd5719b304879d256ab7c0 HEAD
git status --porcelain -- runs/user output reports results
```

```bash
for ref in origin/main origin/feature/case-package-v2-external-schema; do
  for f in project_control/MIGRATION_MASTER_PLAN.md project_control/MIGRATION_STATUS.md project_control/DECISION_LOG.md; do
    git show "$ref:$f" >/dev/null || exit 1
  done
done
```

```bash
rg -n "D033|D034|D035" project_control/MIGRATION_MASTER_PLAN.md project_control/MIGRATION_STATUS.md project_control/DECISION_LOG.md
test -d audits/calcite_hep_track_a_120_execution_checker_diagnostic_v0
test -d audits/canonical_user_metrics_multiengine_path_v0
test -f baselines/calcite_hep_fail_closed/adapter.py
test -x /home/tianci_gao/.local/share/sqlrb/calcite_hep/bin/calcite-hep-rewrite-smoke
```

```bash
python -m cli.main user evaluate --help
python -m cli.main user compute-local-metrics --help
```

```bash
source scripts/env_postgres.local.sh && psql -v ON_ERROR_STOP=1 -c 'SELECT 1;'
source scripts/env_mysql.local.sh && MYSQL_PWD="$SQLRB_MYSQL_PASSWORD" mysql -h "$SQLRB_MYSQL_HOST" -P "$SQLRB_MYSQL_PORT" -u "$SQLRB_MYSQL_USER" -e 'SELECT 1;'
source scripts/env_spark.local.sh && python - <<'PY'
from pyspark.sql import SparkSession
spark = SparkSession.builder.master('local[1]').appName('sqlrb-preflight').getOrCreate()
spark.sql('SELECT 1 AS ok').collect()
spark.stop()
print('spark_select_1_ok')
PY
```

```bash
source scripts/env_postgres.local.sh && \
source scripts/env_mysql.local.sh && \
source scripts/env_spark.local.sh && \
export SQLRB_CALCITE_HEP_CMD=/home/tianci_gao/.local/share/sqlrb/calcite_hep/bin/calcite-hep-rewrite-smoke && \
export SQLRB_CALCITE_HEP_ROOT=/home/tianci_gao/.local/share/sqlrb/calcite_hep && \
export SQLRB_CALCITE_HEP_TIMEOUT=30 && \
python -m cli.main user evaluate \
  --case-set common_core_v0 \
  --engines postgres,mysql,spark \
  --adapter-command "python baselines/calcite_hep_fail_closed/adapter.py" \
  --output-root /tmp/sqlrb_calcite_hep_track_a_120_canonical_user_rerun_with_metrics_v0/output \
  --run-id calcite_hep_track_a_120_canonical_v0 \
  --enable-db-execution \
  --enable-checker \
  --collect-timing
```

```bash
python -m cli.main user compute-local-metrics \
  --run-id-prefix calcite_hep_track_a_120_canonical_v0 \
  --engines postgres,mysql,spark \
  --aggregate-run-id calcite_hep_track_a_120_canonical_v0 \
  --source-run-root runs/user \
  --output-root /tmp/sqlrb_calcite_hep_track_a_120_canonical_user_rerun_with_metrics_v0/output
```

Validation commands are recorded after validation in this same packet.

Validation:

```bash
python - <<'PY'
import csv,json
from pathlib import Path
base=Path('runs/user/calcite_hep_track_a_120_canonical_v0/metrics')
json.loads((base/'local_metrics_summary.json').read_text())
for name in ['local_metrics_by_engine.csv','local_metrics_by_pool.csv','local_timing_speedup_rows.csv']:
    with (base/name).open(newline='') as f:
        rows=list(csv.DictReader(f))
        if not rows:
            raise SystemExit(f'{name} has no rows')
print('canonical_metrics_parse_ok')
PY
```

Result: passed. `local_metrics_by_engine.csv` has 3 rows; `local_timing_speedup_rows.csv` has 120 data rows.

```bash
test -d /tmp/sqlrb_calcite_hep_track_a_120_canonical_user_rerun_with_metrics_v0/output/results/calcite_hep_track_a_120_canonical_v0
test -d /tmp/sqlrb_calcite_hep_track_a_120_canonical_user_rerun_with_metrics_v0/output/logs/calcite_hep_track_a_120_canonical_v0
test -d /tmp/sqlrb_calcite_hep_track_a_120_canonical_user_rerun_with_metrics_v0/output/reports/calcite_hep_track_a_120_canonical_v0
test -f /tmp/sqlrb_calcite_hep_track_a_120_canonical_user_rerun_with_metrics_v0/output/results/calcite_hep_track_a_120_canonical_v0/metrics/local_metrics_summary.json
```

Result: passed.

```bash
python -m cli.main user compute-local-metrics --help
pytest tests/user_entry/test_calcite_hep_fail_closed_route.py -q
git diff --check
git status -sb
git status --porcelain -- runs/user output reports results
```

Results:
- `compute-local-metrics --help`: passed.
- `pytest tests/user_entry/test_calcite_hep_fail_closed_route.py -q`: 10 passed.
- `git diff --check`: passed.
- no staged `runs/user`, repository-level `output`, top-level `reports`, or top-level `results` artifacts.
