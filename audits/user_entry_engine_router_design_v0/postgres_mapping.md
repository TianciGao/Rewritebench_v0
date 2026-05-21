# PostgreSQL Mapping

## Current Module

Current implementation: `src/sql_rewrite_bench/postgres_execution.py`.

Current entrypoint: `execute_postgres_case(...)`.

`user_run.py` currently calls `execute_postgres_case` directly from `_apply_db_checker_for_row`. U7 minimal implementation should route this call through a future `engine_execution.py` dispatcher without changing behavior.

## Current Behavior

- Supports local PostgreSQL diagnostics only when `--enable-db-execution` is set.
- Uses external schema metadata by reading manifest `schema.external_profile` and then external profile `engines.postgres.ddl` and `engines.postgres.load`.
- Fails closed when manifest schema metadata is missing, external schema profile is missing, PostgreSQL engine metadata is missing, DDL/load files are missing, `psql` is unavailable, or connection config is absent.
- Writes local execution artifacts under the per-row `runs/user/{run_name}/workspaces/{case_id}/{engine}/execution/` directory.
- Converts CSV stdout to JSONL result artifacts.
- Returns local statuses and failure classes; it does not compute speedup or official metrics.

## Mapping To Common Interface

- `source_execution_status` maps directly.
- `candidate_execution_status` maps directly.
- `source_result_path` maps directly when present.
- `candidate_result_path` maps directly when present.
- `execution_artifact_dir` maps from current `db_artifact_dir`.
- `execution_failure_class` maps directly.
- `db_execution_attempted` should be true when the router invokes PostgreSQL execution after candidate preflight passes.
- `schema_setup_status` should be added by the future wrapper or PostgreSQL result expansion.
- `source_error_path` and `candidate_error_path` should be exposed by the future common result if files are written.
- `engine_version` may be collected later, but it is not required for U7 minimal routing.

## Gaps

- Current `PostgresExecutionResult` does not expose `schema_setup_status`.
- Current `PostgresExecutionResult` does not expose source/candidate error paths even though error files are written.
- Current `user_run.py` imports PostgreSQL execution directly.
- Current status vocabulary has local execution states but not explicit `not_implemented` or `not_configured` statuses for MySQL/Spark.

## Behavior-Preservation Risks

- Router extraction could accidentally change failure bucket priority.
- Unsupported engine behavior could silently fall back to PostgreSQL if dispatch is not explicit.
- Artifact paths could move outside the current per-row workspace layout.
- Checker handoff could receive incomplete result paths if the common result is not validated.

## Boundary

PostgreSQL execution remains local diagnostic only. It does not compute timing, speedup, official metrics, paper tables, retained evidence, reports/results updates, or leaderboard output.
