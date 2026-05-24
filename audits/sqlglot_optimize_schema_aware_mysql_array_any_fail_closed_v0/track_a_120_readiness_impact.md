# Track A 120 Readiness Impact

Route:

- `sqlglot_optimize_schema_aware`

## Improved

MySQL `CONS_0005` no longer reaches DB execution with known-unsupported `ARRAY_ANY` / lambda SQL. The route now fails closed before execution with explicit adapter status bucket:

- `mysql_unsupported_array_any`

This improves failure classification and prevents a misleading `candidate_execution_failed` row for known unsupported generated SQL.

## Still blocked

Full Track A 120 local diagnostic readiness remains blocked.

Reasons:

- Spark `CONS_0005` remains a value/row-count semantic mismatch.
- Spark `CONS_0036` remains a strict-label mismatch unless a separate label policy is authorized.
- Current evidence is still bounded smoke evidence, not all Common-core 40 x 3 evidence.
- Timing, official metrics, paper-facing promotion, verifier support, and leaderboard output remain unauthorized.

## Next readiness step

The route is ready for another bounded tri-engine execution/checker smoke to confirm aggregate movement after the MySQL fail-closed guard. It is not ready for full Track A 120.
