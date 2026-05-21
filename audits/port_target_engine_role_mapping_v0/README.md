# PORT Target-Engine Role Mapping v0

Verdict: `completed_local_diagnostic_role_mapping`.

This packet documents target-engine-aware PORT local diagnostic role mapping for all 9 Common-core PORT manifests. The runner now resolves `local_diagnostic.engine_roles.<selected-engine>` instead of relying on one case-level diagnostic mode.

## Summary

- All 9 PORT manifests now use `schema_version: port_target_engine_diagnostic_v0`.
- Each manifest declares explicit `postgres`, `mysql`, and `spark` target-engine roles.
- The five MySQL-source cases (`PORT_0004`, `PORT_0013`, `PORT_0022`, `PORT_0024`, `PORT_0025`) preserve the MySQL source-reference to PostgreSQL target-candidate controlled path.
- The four PostgreSQL-source cases (`PORT_0003`, `PORT_0005`, `PORT_0008`, `PORT_0012`) declare the reverse PostgreSQL source-reference to MySQL target-candidate role. The current runner fails that reverse route closed as unsupported instead of executing PostgreSQL-like source SQL in MySQL.
- MySQL-source PORT cases now have an explicit MySQL same-engine role for `--engine mysql`.
- Spark remains explicit unsupported/deferred.

## Local Diagnostic Checks

- PostgreSQL target controlled diagnostic for the five MySQL-source cases reached exact 5/5.
- MySQL reverse-role guard for the four PostgreSQL-source cases selected 4 rows and failed closed with `unsupported_engine=4`, `execution_failure_class=cross_dialect_route_unsupported`; no wrong-engine source execution was attempted.
- A MySQL-source same-engine sample (`PORT_0004 --engine mysql`) reached exact locally under the no-op adapter.

## Boundary

This is local diagnostic metadata and runner behavior only. No SQL files, schema files, checker configs, validation files, `case_sets/`, reports/results, denominators, paper results, case membership, raw retained evidence, timing/speedup, official metrics, leaderboard, release tag, or export branch were changed or created.

## Next Safe Action

Review the explicit reverse PostgreSQL-source to MySQL-target route for the four guarded cases. If live reverse cross-dialect execution is desired, authorize a narrow follow-up to implement PostgreSQL source-reference plus MySQL target-candidate execution without SQL edits or official metrics.
