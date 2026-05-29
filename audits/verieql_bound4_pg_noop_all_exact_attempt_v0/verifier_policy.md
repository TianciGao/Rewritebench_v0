# Verifier Policy

Declared uniform policy:

- `verifier_tool=verieql`
- `verifier_mode=finite_bound`
- `bound_size=4`
- `timeout_seconds=30`
- `cores=1`
- schema canonicalization enabled
- `result_checker_exactness_used=false`

Policy label:

- `finite_bound_bound4_timeout30_cores1`

Strict normalization:

- all states are `EQU`, with no `TMO`, `NSE`, `UNK`, `SYN`, `NIE`, `OOM`, or `OTE`: `equivalent`
- any `NEQ`: `non_equivalent`
- any `TMO`: `timeout`
- any `NSE`: `unsupported`
- `SYN`: `syntax_error`
- `NIE`: `not_implemented`
- `OOM`: `out_of_memory`
- `OTE`: `tool_error`
- `UNK`: `unknown`
- non-exact rows: `not_attempted`

This policy does not mix bound sizes. Bound-4 outcomes must not be combined with earlier bound-10 outcomes inside one denominator.
