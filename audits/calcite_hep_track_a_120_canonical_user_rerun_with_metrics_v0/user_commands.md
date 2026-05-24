# User Commands

Preflight checks:

```bash
git status -sb
git branch --show-current
git fetch origin main feature/case-package-v2-external-schema
git merge-base --is-ancestor a5443236d8eac9ff4dbd5719b304879d256ab7c0 HEAD
python -m cli.main user evaluate --help
python -m cli.main user compute-local-metrics --help
```

Engine probes:

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

Canonical evaluate command:

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

Canonical metrics command:

```bash
python -m cli.main user compute-local-metrics \
  --run-id-prefix calcite_hep_track_a_120_canonical_v0 \
  --engines postgres,mysql,spark \
  --aggregate-run-id calcite_hep_track_a_120_canonical_v0 \
  --source-run-root runs/user \
  --output-root /tmp/sqlrb_calcite_hep_track_a_120_canonical_user_rerun_with_metrics_v0/output
```

The evaluate command produced per-engine source runs. The metrics command aggregated those source runs through `local_metrics.py`.
