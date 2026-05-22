# Spark Backend Design v0

Verdict: `ready_for_fail_closed_skeleton`.

This packet designs a future Spark local diagnostic backend for user-entry engine execution. It is design/audit only. No Spark execution is implemented or run here.

## Summary

Spark should fit behind the existing `engine_execution.py` router as an engine-specific local diagnostic backend in `spark_execution.py`. The backend should mirror the PostgreSQL and MySQL local diagnostic contract: resolve explicit Spark schema assets from manifest/external schema metadata, set up an isolated per-case Spark namespace, execute source SQL and adapter candidate SQL, export source/candidate result artifacts as JSONL, and return an `EngineExecutionResult` for ledger/checker/quality/tag-slice consumption.

The recommended implementation path is conservative: first add only an environment detector and clearer fail-closed statuses, then add Spark schema/load resolution, then add mocked execution tests, and only then consider optional live local Spark smoke on one or two safe cases.

## Main Risks

- Spark local startup can be slow and environment-sensitive, so the backend must remain opt-in and fail closed when runtime dependencies or configuration are missing.
- Spark SQL type rendering differs from PostgreSQL/MySQL for decimals, dates, timestamps, booleans, and complex values; result export needs a stable JSONL serialization policy before checker handoff.
- Some Spark DDL/load files are migration draft assets, especially PORT schemas, so live smoke should start with known simple same-engine cases and avoid treating success or failure as official evidence.
- PORT manifests currently mark Spark target roles as unsupported/manual-review; Spark must not guess cross-dialect roles from filenames, SQL text, or schema assets.

## Recommended Next Safe Action

Authorize a narrow fail-closed Spark skeleton/environment detector only. That follow-up should improve Spark-specific status reporting without executing Spark SQL, without live smoke, without timing, without official metrics, without reports/results updates, and without leaderboard output.
