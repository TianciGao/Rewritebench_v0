# Spark Environment Contract

## Recommended Runtime Interface

Use `pyspark` for the eventual backend, not the `spark-sql` CLI. `pyspark` gives direct control over session configuration, per-case database names, DataFrame result export, type-aware serialization, and exception handling. The `spark-sql` CLI may remain a fallback candidate only if a later task proves it can emit stable machine-readable results without weakening isolation.

## Required Future Gates

A future fail-closed skeleton should check these conditions before any execution is allowed:

- Spark local execution is explicitly enabled for diagnostics, for example with a future `SQLRB_SPARK_ENABLE_LOCAL=1` opt-in.
- A Spark runtime is available, preferably importable `pyspark` in the active Python environment.
- A local master is declared or safely defaulted, for example `SQLRB_SPARK_MASTER=local[1]` or `local[*]` after review.
- A local bind address is configured when needed, commonly `SPARK_LOCAL_IP=127.0.0.1`.
- A per-run warehouse/scratch root can be created under the user-run workspace, not under case packages or retained evidence.

`SPARK_LOCAL_IP` alone is not enough to enable local diagnostics. It helps Spark bind locally, but it does not prove `pyspark` exists, that a session can start, that a safe warehouse is configured, or that schema assets can be loaded.

## Optional Environment Variables

- `SPARK_HOME`: optional if `pyspark` or Spark binaries need discovery.
- `PYSPARK_PYTHON`: optional Python executable for Spark workers.
- `SQLRB_SPARK_MASTER`: optional local master string.
- `SQLRB_SPARK_WAREHOUSE_DIR`: optional scratch directory; if unset, backend should create one inside the per-run workspace.
- `SQLRB_SPARK_DRIVER_MEMORY`: optional memory setting for live smoke only.
- `SQLRB_SPARK_EXTRA_CONF`: optional future key/value list; do not implement broad parsing without tests.

## Secret and Logging Rules

Do not print secrets, private paths beyond repo-relative audit paths, full environment dumps, or Spark configuration values that may contain credentials. Error excerpts in audit artifacts should be short and redacted.

## Fail-Closed Cases

- `spark_not_configured`: explicit Spark diagnostic opt-in or required local configuration is absent.
- `spark_client_missing`: `pyspark` or required Spark runtime is not available.
- `spark_session_failed`: local Spark session cannot start.
- `spark_timeout`: startup, schema setup, source execution, candidate execution, or export exceeds the runner timeout.
- `spark_internal_error`: unexpected backend exception after redaction.

No fail-closed case may fall back to PostgreSQL or MySQL.
