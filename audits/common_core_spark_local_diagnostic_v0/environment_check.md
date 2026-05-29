# Environment Check

Command:

```bash
source ~/code/sql-rewrite-bench/.venv/bin/activate
source scripts/env_postgres.local.sh
source scripts/env_mysql.local.sh
source scripts/env_spark.local.sh
export PYTHONPATH=src
PYTHONPATH=src python scripts/dev/check_local_engine_env.py
```

Accepted environment check result:

- PostgreSQL probe result: `ok`.
- MySQL probe result: `ok`.
- Spark readiness result: ready for live local diagnostic backend.
- PySpark import result: `available`.
- `PYSPARK_PYTHON`: set.
- `SQLRB_SPARK_MASTER`: set.
- `SQLRB_SPARK_APP_NAME`: set by `scripts/env_spark.local.sh`.
- `SPARK_LOCAL_IP`: set.
- `SPARK_HOME`: unset.
- Spark backend status: live local diagnostic backend available through PySpark.
- Secrets printed: no. The checker explicitly reports that passwords and DSN values are not printed.

No packages were installed and no system configuration was changed.
