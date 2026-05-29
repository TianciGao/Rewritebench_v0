# Environment Check

Command: `python scripts/dev/check_local_engine_env.py`

- PostgreSQL probe: ok (`psql` found; libpq config present).
- MySQL probe: ok (`mysql` found; required `SQLRB_MYSQL_*` config present).
- Spark `spark-sql`: not found.
- Spark `SPARK_LOCAL_IP`: unset.
- Spark `SPARK_HOME`: unset.
- Spark `PYSPARK_PYTHON`: unset.
- Spark `SQLRB_SPARK_MASTER`: unset.
- Spark `pyspark` import: unavailable.
- Spark backend status: fail-closed until PySpark is available (`spark_config_missing`).

No passwords, DSNs, or local secrets were recorded.
