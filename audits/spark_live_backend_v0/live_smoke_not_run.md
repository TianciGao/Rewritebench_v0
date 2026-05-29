# Live Spark Smoke Not Run

The requested live Spark smoke was not run because Spark is not configured locally.

Environment blocker:

- `spark-sql` was not found on `PATH`.
- `SPARK_LOCAL_IP` was unset.
- `SPARK_HOME` was unset.
- `PYSPARK_PYTHON` was unset.
- `pyspark` was not importable.

Implementation and mocked tests were completed. A fail-closed Spark smoke command selected `PERF_0006` and `CONS_0005`, generated candidates, and failed closed without crashing with `unsupported_engine=2` and `execution_failure_class=spark_config_missing`. That fail-closed smoke is not a live Spark validation and is not an official metric.
