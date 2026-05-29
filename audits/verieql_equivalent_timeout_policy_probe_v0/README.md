# verieql_equivalent_timeout_policy_probe_v0

Probe verdict: completed; no clean equivalent verdict was obtained.

This task ran a narrow local VeriEQL timeout-policy probe for the minimal synthetic equivalent pair that previously produced repeated `EQU` states followed by `TMO`.

Scope:

- Tool: VeriEQL only.
- Pair: `synthetic_from_equivalent` only.
- SQL: `SELECT a FROM T;` vs `SELECT a FROM T;`.
- Schema: `T(a integer, b integer)`.
- Timeout values: 30, 120, and 300 seconds.
- Runtime root: `/tmp/sqlrb_verieql_equivalent_timeout_policy_probe_v0`.

Result:

- All timeout values completed through the staged VeriEQL JSONL wrapper.
- All outputs contained repeated `EQU` states followed by `TMO`.
- All attempts remained normalized as `timeout`.
- No clean `equivalent` verdict was obtained.
- Local semantic-equivalence summaries remained `semantic_equivalence_rate=null` with `semantic_equivalence_rate_status=not_applicable`.

Interpretation:

- The correct policy is to keep `EQU+TMO` rows classified as `timeout`.
- Partial `EQU` states are not sufficient formal verifier evidence.
- This pattern is best described as `equivalent_path_timeout_or_internal_subcheck_timeout`.
- Future work should inspect VeriEQL internal state semantics, bound-size behavior, or schema/constraint encoding before expanding equivalent-path real-case canaries.

Boundary:

This is local verifier-support probing only. It is not Common-core evidence, not official Semantic Equivalence Rate, not paper evidence, not retained evidence, and not leaderboard input.
