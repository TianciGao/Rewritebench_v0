# Environment Check

Command:

```bash
source ~/code/sql-rewrite-bench/.venv/bin/activate
source scripts/env_postgres.local.sh
source scripts/env_mysql.local.sh
source scripts/env_spark.local.sh
PYTHONPATH=src python scripts/dev/check_local_engine_env.py
```

Accepted environment check result:

- PostgreSQL probe result: `ok`.
- MySQL probe result: `ok`.
- Spark readiness result: ready for live local diagnostic backend.
- PySpark import result: `available`.
- `PYSPARK_PYTHON`: set.
- `SQLRB_SPARK_MASTER`: set.
- Spark backend status: live local diagnostic backend available through PySpark.
- Secrets printed: no. The checker explicitly reports that passwords and DSN values are not printed.

Notes:

- A sandboxed preliminary environment check could not read local network routing for `PGHOST` and could not create a MySQL TCP socket. The accepted readiness check was rerun with local network/socket access and passed.
- `SPARK_HOME` was unset, but PySpark was importable and sufficient for the implemented local Spark backend.
