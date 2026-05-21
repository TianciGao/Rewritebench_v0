# User-Entry U7 Minimal Engine Router v0

## Summary

U7 added a minimal local diagnostic engine execution router for user-entry runs.

Implemented modules:

- `src/sql_rewrite_bench/engine_execution.py`
- `src/sql_rewrite_bench/mysql_execution.py`
- `src/sql_rewrite_bench/spark_execution.py`

`user_run.py` now calls the router for optional DB execution instead of calling PostgreSQL execution directly. PostgreSQL behavior is preserved by delegating to the existing `postgres_execution.py` implementation. MySQL and Spark are explicit fail-closed stubs only.

## Boundaries

- PostgreSQL remains the only implemented live DB diagnostic backend.
- MySQL and Spark do not open connections, start sessions, execute SQL, or fall back to PostgreSQL.
- The router does not run checkers, compute timing, compute speedup, compute official metrics, render paper tables, update `reports/` or `results/`, parse retained evidence, or create a global leaderboard.
- User-run outputs remain local diagnostics under `runs/user/`.

## Behavior Preservation

The existing public smoke paths are preserved:

- `--smoke --dry-run`
- `--smoke` adapter capture
- readability commands
- quality report output
- tag slice output

## Result

U7 minimal router implemented: yes.

Next safe action: human review of the U7 router/stub behavior, then authorize U8 timing diagnostic design only if desired. Timing, speedup, official metrics, paper rendering, reports/results updates, retained-evidence parsing, and leaderboard output remain deferred.
