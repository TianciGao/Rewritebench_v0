# User-Entry Engine Router Design v0

## Purpose

This U7 design packet defines the next engine-execution layer for the user-entry local diagnostic harness.

The design covers:

- future `src/sql_rewrite_bench/engine_execution.py` router
- common engine execution result interface
- current PostgreSQL execution mapping
- future fail-closed MySQL and Spark execution module contracts
- checker and ledger handoffs
- timing and official-metric boundaries

## Verdict

Verdict: `ready_for_minimal_router`.

The current user-entry path already has selection, package resolution, adapter capture, candidate preflight, PostgreSQL local diagnostic execution, local checker, ledger writing, quality report, tag slices, and readability commands. A minimal future router can be added without changing benchmark semantics if it preserves PostgreSQL behavior and implements MySQL/Spark as explicit fail-closed stubs.

## Design Summary

- `engine_execution.py` should dispatch by selected engine and validate a common local execution result object.
- `postgres_execution.py` remains the only implemented live DB executor for now.
- `mysql_execution.py` and `spark_execution.py` should initially return explicit local diagnostic fail-closed results when unsupported, unconfigured, or not implemented.
- `local_result_checker.py` should consume only result artifacts and checker configs; it should not execute SQL, preflight candidates, compute timing, or act as a formal verifier.
- `user_ledger.py` should receive execution statuses, artifact paths, and failure classes from the common execution result.

## Boundary

This packet is design-only. No source code was modified, no live DB/checker execution was run, no timing or speedup was computed, no official metrics were computed, no paper tables were rendered, no reports/results were updated, no retained evidence was promoted, and no global leaderboard was created.

## Next Safe Action

Authorize a minimal U7 implementation task only if the design is accepted. That task may add `engine_execution.py` plus fail-closed `mysql_execution.py` and `spark_execution.py` stubs while preserving existing PostgreSQL behavior. It must not authorize timing, official metrics, paper rendering, reports/results updates, retained-evidence parsing, or leaderboard output.
