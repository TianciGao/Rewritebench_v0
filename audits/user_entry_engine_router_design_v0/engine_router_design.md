# Engine Router Design

## Purpose

`src/sql_rewrite_bench/engine_execution.py` should be a thin router between `user_run.py` and engine-specific execution modules. It should make engine dispatch explicit and keep `user_run.py` from importing PostgreSQL execution directly.

## Responsibilities

- Accept one selected case-engine row, resolved package context, candidate SQL path, run/workspace paths, and execution options.
- Dispatch to the correct engine module based on `row.engine`.
- Validate that the engine-specific result conforms to the common local execution result interface.
- Return an `EngineExecutionResult` to the orchestrator.
- Fail closed for unsupported, unimplemented, or unconfigured engines.

## Inputs

- `repo_root`
- `run_id`
- `row`
- `resolved_package`
- `candidate_sql_path`
- `workspace_dir`
- `timeout_sec`
- engine-specific optional configuration such as PostgreSQL DSN environment variable
- future engine config objects for MySQL and Spark

## Outputs

- One common `EngineExecutionResult` object or dict.
- No direct ledger writes.
- No checker writes.
- No report/result writes outside `runs/user/{run_name}/`.

## Supported And Fail-Closed Handling

- `postgres`: dispatch to current PostgreSQL local diagnostic executor.
- `mysql`: dispatch to future `mysql_execution.py`; until implemented/configured, return fail-closed `execution_not_enabled` or `execution_unsupported` local result.
- `spark`: dispatch to future `spark_execution.py`; until implemented/configured, return fail-closed `execution_not_enabled` or `execution_unsupported` local result.
- unknown engine: return fail-closed unsupported result. Do not silently fall back to PostgreSQL.

## Non-Goals

- PostgreSQL-specific command construction.
- MySQL-specific command construction.
- Spark-specific command construction.
- Result consistency checking.
- Candidate preflight.
- Timing metric computation.
- Official metrics.
- Paper table rendering.
- Reports/results updates.
- Retained-evidence parsing or promotion.
- Leaderboard output.
