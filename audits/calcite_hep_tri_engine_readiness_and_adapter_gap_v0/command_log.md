# Command Log

Preflight and inspection:

```bash
git status -sb
git branch --show-current
git fetch origin main feature/case-package-v2-external-schema
git show origin/main:project_control/MIGRATION_MASTER_PLAN.md
git show origin/main:project_control/MIGRATION_STATUS.md
git show origin/main:project_control/DECISION_LOG.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_MASTER_PLAN.md
git show origin/feature/case-package-v2-external-schema:project_control/MIGRATION_STATUS.md
git show origin/feature/case-package-v2-external-schema:project_control/DECISION_LOG.md
test -f baselines/calcite_hep_fail_closed/adapter.py
test -x /home/tianci_gao/.local/share/sqlrb/calcite_hep/bin/calcite-hep-rewrite-smoke
source scripts/env_postgres.local.sh && psql -v ON_ERROR_STOP=1 -c 'SELECT 1;'
source scripts/env_mysql.local.sh && MYSQL_PWD="$SQLRB_MYSQL_PASSWORD" mysql -h "$SQLRB_MYSQL_HOST" -P "$SQLRB_MYSQL_PORT" -u "$SQLRB_MYSQL_USER" -e 'SELECT 1;'
source scripts/env_spark.local.sh && python - <<'PY'
from pyspark.sql import SparkSession
spark = SparkSession.builder.master("local[1]").appName("sqlrb-preflight").getOrCreate()
spark.sql("SELECT 1").collect()
spark.stop()
PY
```

Bounded case list:

```bash
printf '%s\n' PERF_0006 CONS_0005 CONS_0036 CONS_0037 PORT_0004 PORT_0024 > /tmp/sqlrb_calcite_hep_tri_engine_readiness_cases.txt
```

Pre-guard smoke:

```bash
source scripts/env_postgres.local.sh
source scripts/env_mysql.local.sh
source scripts/env_spark.local.sh
export SQLRB_CALCITE_HEP_CMD=/home/tianci_gao/.local/share/sqlrb/calcite_hep/bin/calcite-hep-rewrite-smoke
export SQLRB_CALCITE_HEP_ROOT=/home/tianci_gao/.local/share/sqlrb/calcite_hep
export SQLRB_CALCITE_HEP_TIMEOUT=30
python -m cli.main user evaluate \
  --case-set common_core_v0 \
  --case-list /tmp/sqlrb_calcite_hep_tri_engine_readiness_cases.txt \
  --engines postgres,mysql,spark \
  --adapter-command "python baselines/calcite_hep_fail_closed/adapter.py" \
  --output-root /tmp/sqlrb_calcite_hep_tri_engine_readiness_and_adapter_gap_v0/output \
  --run-id calcite_hep_tri_engine_readiness_smoke_v0 \
  --enable-db-execution \
  --enable-checker
```

Post-guard smoke:

```bash
source scripts/env_postgres.local.sh
source scripts/env_mysql.local.sh
source scripts/env_spark.local.sh
export SQLRB_CALCITE_HEP_CMD=/home/tianci_gao/.local/share/sqlrb/calcite_hep/bin/calcite-hep-rewrite-smoke
export SQLRB_CALCITE_HEP_ROOT=/home/tianci_gao/.local/share/sqlrb/calcite_hep
export SQLRB_CALCITE_HEP_TIMEOUT=30
python -m cli.main user evaluate \
  --case-set common_core_v0 \
  --case-list /tmp/sqlrb_calcite_hep_tri_engine_readiness_cases.txt \
  --engines postgres,mysql,spark \
  --adapter-command "python baselines/calcite_hep_fail_closed/adapter.py" \
  --output-root /tmp/sqlrb_calcite_hep_tri_engine_readiness_and_adapter_gap_v0/output \
  --run-id calcite_hep_tri_engine_readiness_after_guard_v0 \
  --enable-db-execution \
  --enable-checker
```

Validation commands are recorded after validation in the final report and
project-control entry.
