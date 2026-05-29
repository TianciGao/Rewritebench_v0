# Bound-4 Policy

Declared verifier policy for the next small feature-aware pass:

- `verifier_tool=verieql`
- `verifier_mode=finite_bound`
- `bound_size=4`
- `timeout_seconds=30`
- `cores=1`
- schema canonicalization enabled
- `result_checker_exactness_used=false`

Policy label:

- `finite_bound_bound4_timeout30_cores1`

Strict normalization remains required:

- all returned states are `EQU`, with no `TMO`, `NSE`, `UNK`, `SYN`, `NIE`, `OOM`, or `OTE`: `equivalent`
- any `NEQ`: `non_equivalent`
- any `TMO`: `timeout`
- any `NSE`: `unsupported`
- `SYN`: `syntax_error`
- `NIE`: `not_implemented`
- `OOM`: `out_of_memory`
- `OTE`: `tool_error`
- `UNK`: `unknown`

Policy constraint:

- Do not mix results from different `bound_size` values in one Semantic Equivalence Rate denominator.
- Bound-4 evidence does not imply equivalence under `bound_size=10`.
- Local result checker exactness must not be substituted for formal verifier equivalence.
