# Fail-Closed Mapping Policy

Annotation replay must fail closed when identity, schema, or contract requirements are not met.

Status mapping:

- `schema_invalid`: JSON parsed but required fields, atom fields, values, or schema shape are invalid.
- `malformed_json`: a JSONL row cannot be parsed as JSON.
- `missing_annotation`: no annotation row exists for a candidate row.
- `duplicate_annotation`: multiple annotation rows match the same case/engine/method/route/candidate identity.
- `case_mismatch`: annotation `case_id` differs from the selected candidate row.
- `engine_mismatch`: annotation `engine` differs from the selected candidate row.
- `method_mismatch`: annotation `method_id` differs from the selected candidate row.
- `route_mismatch`: annotation `route_id` differs from the selected candidate row.
- `candidate_mismatch`: annotation candidate identity, path, or SHA does not match the candidate row.
- `skills_contract_mismatch`: annotation skills hash differs from the current skills contract.
- `provider_call_failed`: the future annotation call did not produce a usable annotation row.
- `skipped_no_candidate`: no candidate SQL exists for the planned row.
- `skipped_unsupported_engine`: the route did not support the planned engine.

Fail-closed rows must not contribute to official POCR, route-level POCR, paper-facing metrics, or leaderboard output.
