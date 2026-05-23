# Fail-Closed Policy

The Calcite HEP route must not emit candidate SQL unless a separately authorized backend contract exists.

Current fail-closed statuses:

- `calcite_runtime_unavailable`: no Calcite command, JAR, or root is configured.
- `calcite_java_missing`: Java is not found.
- `calcite_runtime_incomplete`: partial Calcite configuration points to missing paths.
- `calcite_backend_not_implemented`: a possible runtime is discovered, but this scaffold has no authorized HEP invocation contract.

Current ledger mapping:

- Fail-closed adapter success with no SQL maps to `extraction_status=no_candidate_sql`.
- The user ledger maps this to `failure_bucket=no_candidate_sql`.
- Route-specific details remain in the workspace status artifact and exported adapter logs.

This policy prevents an unavailable or unimplemented Calcite path from being mistaken for a generated rewrite candidate.
