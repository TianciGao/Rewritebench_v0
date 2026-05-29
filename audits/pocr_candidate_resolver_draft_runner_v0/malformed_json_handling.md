# Malformed JSON Handling

The live Stage A smoke previously produced one malformed provider JSON row for `PERF_0006`. This task adds deterministic fail-closed handling in `src/sql_rewrite_bench/pocr/json_output_guard.py`.

Behavior:

- Strict JSON objects are accepted.
- One safe JSON code fence may be stripped deterministically.
- Malformed JSON returns `raw_status=malformed_json`.
- Non-object JSON returns `raw_status=not_json_object`.
- `repaired=false` is recorded for all supported paths.
- Repair mode is not implemented or authorized; requesting it raises an error.

Boundary:

- Malformed JSON becomes `schema_invalid`.
- Malformed JSON is not silently repaired.
- Malformed rows contribute zero validated operation atoms.
- No malformed row can contribute to official POCR.

Tests:

- strict JSON object parse;
- safe JSON fence parse;
- malformed JSON fail-closed;
- repair mode rejected.
