# Policy Interpretation

Strict normalization policy:
- all states are `EQU`, with no timeout/unsupported/unknown/error states: `equivalent`
- any `NEQ`: `non_equivalent`
- any `TMO`: `timeout`
- any unsupported, syntax, implementation, memory, or tool error state remains separately visible
- `EQU...TMO` is never reinterpreted as equivalent
- local result-checker exactness is never used as verifier equivalence

Interpretation for `CONS_0037`:
- Bounds 1 through 4 at 30 seconds are clean bounded-equivalent local verifier-support outcomes.
- Bounds 5 and 10 are timeout-prone.
- Increasing timeout from 30 seconds to 120 seconds did not make bounds 5 or 10 decidable in the wrapper run.
- `bound_size=10` is not feasible for `CONS_0037` under the tested settings.
- A smaller declared bound, especially `bound_size=4`, is feasible for `CONS_0037`.

Metric-denominator policy:
- Do not mix `bound_size=4` and `bound_size=10` results inside one Semantic Equivalence Rate denominator unless a separate durable policy explicitly authorizes mixed-bound reporting.
- If a future small feature-aware subset includes `CONS_0037`, the pass should declare one uniform verifier policy, for example `verifier_mode=finite_bound`, `bound_size=4`, `timeout_seconds=30`, `cores=1`.
- A `bound_size=4` local diagnostic pass would be a bounded verifier-support claim, not a substitute for an official Semantic Equivalence Rate.

Recommendation:
- Include `CONS_0037` in the next feature-aware subset only under a declared uniform smaller-bound policy such as `bound_size=4`, or exclude it from any `bound_size=10` subset.
- Keep full Common-core exact-candidate verifier expansion blocked.

