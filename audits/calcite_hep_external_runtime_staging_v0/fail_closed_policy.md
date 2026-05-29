# Fail-Closed Policy

The Calcite HEP route remains fail-closed despite having an external runtime path.

Fail-closed statuses:

- `calcite_runtime_unavailable`
- `calcite_java_missing`
- `calcite_runtime_incomplete`
- `calcite_schema_unavailable`
- `calcite_invocation_failed`
- `calcite_invocation_timeout`
- `calcite_no_candidate_sql`

For these statuses, the adapter writes `calcite_hep_status.json`, emits no candidate SQL, and exits `0` so the user-entry ledger records a route-level no-candidate outcome rather than an infrastructure crash.

Candidate generation is accepted only when:

- runtime discovery succeeds;
- per-engine DDL resolves;
- the external command exits `0`;
- the declared candidate SQL file exists and is non-empty.

This task did not add official metric, timing, verifier, report/paper, retained-evidence, or leaderboard behavior.
