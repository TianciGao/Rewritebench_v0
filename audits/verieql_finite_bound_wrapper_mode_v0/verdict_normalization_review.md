# Verdict Normalization Review

## Implemented Policy

The JSONL output normalizer now applies strict finite-bound logic:

- all returned states are `EQU`, no error: `equivalent`
- any `NEQ`: `non_equivalent`
- any `TMO`: `timeout`
- any `NSE`: `unsupported`
- any `UNK`: `unknown`
- any `SYN`, `NIE`, `OOM`, or `OTE`: `tool_error`
- empty states: `unknown`

`EQU,TMO` is still `timeout`; it is never reinterpreted as equivalent.

## Output Metadata

Finite-bound verdict records include local diagnostic metadata in `artifact_paths`:

- `verifier_mode`
- `bound_size`
- `timeout_seconds`
- `raw_states`
- `normalized_verdict`
- `tool_available`
- `command_shape`
- `result_checker_exactness_used=false`

Summary output also includes:

- `verifier_mode`
- `bound_size`
- `result_checker_exactness_used=false`
