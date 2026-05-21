# Spark Fail-Closed Plan

## Future Module

Future module: `src/sql_rewrite_bench/spark_execution.py`.

U7 design does not implement this module. A later minimal router task may add a stub that returns explicit fail-closed local diagnostic results.

## Expected Inputs

- `repo_root`
- selected case-engine row with `engine=spark`
- resolved case package
- candidate SQL path
- per-row workspace directory under `runs/user/{run_name}/`
- timeout/config values
- future Spark SQL execution configuration

## Expected Outputs

- Common `EngineExecutionResult`.
- Source/candidate result artifact paths when implementation exists and execution succeeds.
- Error artifact paths when implementation exists and execution fails.
- Explicit unsupported/not_configured/not_implemented local diagnostic result before implementation or when configuration is absent.

## Schema-Load Responsibilities

Future Spark execution should resolve DDL/load through:

- case manifest `schema.external_profile`
- external schema profile `engines.spark.ddl`
- external schema profile `engines.spark.load`

It must not use case-local `schema/spark/` unless the current manifest/resolver explicitly authorizes that path. It must not silently reuse PostgreSQL or MySQL assets.

## Fail-Closed Statuses

Recommended local diagnostic failure classes:

- `spark_execution_not_implemented`
- `spark_config_missing`
- `spark_schema_metadata_missing`
- `spark_schema_setup_failed`
- `spark_source_execution_failed`
- `spark_candidate_execution_failed`
- `spark_execution_timeout`
- `spark_execution_internal_error`

Recommended execution statuses:

- `execution_not_enabled`
- `execution_unsupported`
- `source_execution_failed`
- `candidate_execution_failed`
- `execution_timeout`
- `execution_internal_error`

## Expected Tests

- Router dispatches `engine=spark` to the Spark interface.
- Stub returns fail-closed not-implemented or not-configured result.
- No adapter rerun occurs in the engine interface.
- No PostgreSQL fallback occurs.
- No artifacts are written outside `runs/user/{run_name}/`.
- Ledger records unsupported/not-configured local diagnostic failure cleanly.

## Non-Goals

- Live Spark SQL execution.
- Spark timing.
- Full PORT closure.
- Cross-engine speedup claim.
- Official metrics.
- Reports/results updates.
- Paper table rendering.
- Leaderboard output.
