# MySQL Fail-Closed Plan

## Future Module

Future module: `src/sql_rewrite_bench/mysql_execution.py`.

U7 design does not implement this module. A later minimal router task may add a stub that returns explicit fail-closed local diagnostic results.

## Expected Inputs

- `repo_root`
- selected case-engine row with `engine=mysql`
- resolved case package
- candidate SQL path
- per-row workspace directory under `runs/user/{run_name}/`
- timeout/config values
- future MySQL connection configuration

## Expected Outputs

- Common `EngineExecutionResult`.
- Source/candidate result artifact paths when implementation exists and execution succeeds.
- Error artifact paths when implementation exists and execution fails.
- Explicit unsupported/not_configured/not_implemented local diagnostic result before implementation or when configuration is absent.

## Schema-Load Responsibilities

Future MySQL execution should resolve DDL/load through:

- case manifest `schema.external_profile`
- external schema profile `engines.mysql.ddl`
- external schema profile `engines.mysql.load`

It must not use case-local `schema/mysql/` unless the current manifest/resolver explicitly authorizes that path. It must not silently reuse PostgreSQL DDL/load.

## Fail-Closed Statuses

Recommended local diagnostic failure classes:

- `mysql_execution_not_implemented`
- `mysql_config_missing`
- `mysql_schema_metadata_missing`
- `mysql_schema_setup_failed`
- `mysql_source_execution_failed`
- `mysql_candidate_execution_failed`
- `mysql_execution_timeout`
- `mysql_execution_internal_error`

Recommended execution statuses:

- `execution_not_enabled`
- `execution_unsupported`
- `source_execution_failed`
- `candidate_execution_failed`
- `execution_timeout`
- `execution_internal_error`

## Expected Tests

- Router dispatches `engine=mysql` to the MySQL interface.
- Stub returns fail-closed not-implemented or not-configured result.
- No adapter rerun occurs in the engine interface.
- No PostgreSQL fallback occurs.
- No artifacts are written outside `runs/user/{run_name}/`.
- Ledger records unsupported/not-configured local diagnostic failure cleanly.

## Non-Goals

- Live MySQL DB execution.
- MySQL timing.
- Cross-engine performance claim.
- Official metrics.
- Reports/results updates.
- Paper table rendering.
- Leaderboard output.
