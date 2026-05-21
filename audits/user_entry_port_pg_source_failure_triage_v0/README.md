# User-Entry PORT PostgreSQL Source Failure Triage v0

Verdict: triage completed. The five failures are reproducible PostgreSQL source-execution failures caused by MySQL-like PORT source SQL being executed directly by the current PostgreSQL local diagnostic path.

This is local diagnostic triage only. It is not official metrics, not paper reproduction, not timing or speedup, not reports/results migration, and not a leaderboard.

## Summary

- Target cases reviewed: `PORT_0004`, `PORT_0013`, `PORT_0022`, `PORT_0024`, `PORT_0025`.
- Targeted run output: `runs/user/port_pg_source_failure_triage/` local only, not committed.
- PostgreSQL environment ready: yes.
- Targeted run completed: yes.
- Selected rows: 5.
- Candidate generated rows: 5.
- Candidate preflight passed rows: 5.
- Source executable rows: 0.
- Candidate executable rows: 0.
- Checker attempted rows: 0.
- Exact rows: 0.
- Mismatch rows: 0.
- Failure buckets: `source_execution_failed=5`.

## Root Cause

All five `sql/source.sql` files are retained PARROT source queries with `source_dialect: mysql_like_candidate` in the manifest. They use MySQL-style backtick quoted identifiers, and several also use MySQL-style date/time or type expressions such as `DATE_FORMAT`, `CAST(... AS DATETIME)`, and `DOUBLE`.

The current user-entry PostgreSQL diagnostic path selects `cases/{POOL}/{CASE_ID}/sql/source.sql` from `case_sets/common_core_v0/` and executes that file directly for PostgreSQL. It does not currently choose an engine-aware source SQL variant. PostgreSQL therefore fails during source query execution before candidate execution or checker comparison.

This is not a schema setup failure: external PostgreSQL schema assets resolved and the recorded failure class is `source_execution_failed` with errors in `source_query.sql`.

This is not a rewriter-quality failure: the no-op adapter emitted source-like SQL, and the source oracle itself failed under PostgreSQL before candidate execution/checker.

## Variant Findings

- No target case has `sql/dialect_variants/postgres/...`.
- `PORT_0004` and `PORT_0013` retain Spark dialect variants only.
- All five cases have `sql/pos_01.sql` that appears PostgreSQL-like, but the manifest declares it as a positive rewrite, not as an engine-specific source oracle for PostgreSQL diagnostics.

## Recommended Next Safe Action

Create a narrow design task for engine-aware source/dialect variant selection. The task should decide whether PostgreSQL local diagnostics may use explicit manifest metadata or an approved role mapping to select a PostgreSQL-compatible source/reference SQL for PORT cases. Do not edit case SQL or manifests until that policy is approved.

If implementation is later authorized, keep it local-diagnostic only and preserve the boundaries: no official metrics, no timing/speedup, no reports/results updates, no denominator changes, no paper-result changes, and no leaderboard.
