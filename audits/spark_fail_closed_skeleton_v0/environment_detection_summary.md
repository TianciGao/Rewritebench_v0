# Environment Detection Summary

`python scripts/dev/check_local_engine_env.py` completed successfully and exited 0.

Observed local probes:

- PostgreSQL probe: ok.
- MySQL probe: ok.
- Spark `spark-sql` CLI: not found.
- Spark `SPARK_LOCAL_IP`: unset.
- Spark `SPARK_HOME`: unset.
- Spark `PYSPARK_PYTHON`: unset.
- Spark `pyspark` import: unavailable.
- Spark backend status: fail-closed/not live implemented with `spark_not_configured`.

The environment checker does not print passwords, DSN values, or connection strings. Spark absence does not fail the whole environment checker because Spark remains optional/deferred.
