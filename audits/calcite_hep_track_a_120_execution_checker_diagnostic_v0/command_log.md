# Command Log

Preflight:

```bash
git status -sb
git branch --show-current
git fetch origin main feature/case-package-v2-external-schema
git merge-base --is-ancestor 04d50c9b91dfa57778ba8812022fc84edc6acdc9 HEAD
git show origin/main:project_control/MIGRATION_MASTER_PLAN.md
git show origin/main:project_control/MIGRATION_STATUS.md
git show origin/main:project_control/DECISION_LOG.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_MASTER_PLAN.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_STATUS.md
git show origin/feature/case-package-v2-external-schema:project_control/DECISION_LOG.md
test -d audits/calcite_hep_target_dialect_runtime_mode_v0
test -f baselines/calcite_hep_fail_closed/adapter.py
test -x /home/tianci_gao/.local/share/sqlrb/calcite_hep/bin/calcite-hep-rewrite-smoke
```

Engine probes:

```bash
source scripts/env_postgres.local.sh && psql -v ON_ERROR_STOP=1 -c 'SELECT 1;'
source scripts/env_mysql.local.sh && MYSQL_PWD="$SQLRB_MYSQL_PASSWORD" mysql -h "$SQLRB_MYSQL_HOST" -P "$SQLRB_MYSQL_PORT" -u "$SQLRB_MYSQL_USER" -e 'SELECT 1;'
source scripts/env_spark.local.sh && python - <<'PY'
from pyspark.sql import SparkSession
spark = SparkSession.builder.master('local[1]').appName('sqlrb-calcite-120-preflight').getOrCreate()
spark.sql('SELECT 1 AS ok').collect()
spark.stop()
PY
```

Execution/checker diagnostic:

```bash
source scripts/env_postgres.local.sh
source scripts/env_mysql.local.sh
source scripts/env_spark.local.sh
export SQLRB_CALCITE_HEP_CMD=/home/tianci_gao/.local/share/sqlrb/calcite_hep/bin/calcite-hep-rewrite-smoke
export SQLRB_CALCITE_HEP_ROOT=/home/tianci_gao/.local/share/sqlrb/calcite_hep
export SQLRB_CALCITE_HEP_TIMEOUT=30
python -m cli.main user evaluate \
  --case-set common_core_v0 \
  --engines postgres,mysql,spark \
  --adapter-command "python baselines/calcite_hep_fail_closed/adapter.py" \
  --output-root /tmp/sqlrb_calcite_hep_track_a_120_execution_checker_diagnostic_v0/output \
  --run-id calcite_hep_track_a_120_execution_checker_v0 \
  --enable-db-execution \
  --enable-checker
```

No `--collect-timing`, verifier, or `compute-local-metrics` command was run.
