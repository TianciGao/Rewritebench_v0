# Semantic Equivalence Summary Examples

Synthetic mixed verdict example:

- equivalent: 2
- non_equivalent: 1
- unknown: 1
- timeout: 1
- unsupported: 1
- tool_error: 1
- not_attempted: 1

Computed synthetic summary:

- `decidable_count = 3`
- `semantic_equivalence_rate = 2 / 3`
- unknown/timeout/unsupported/tool_error/not_attempted remain separate.
- `result_checker_exactness_used = false`

No-decidable example:

- verdicts: `unknown`, `timeout`
- `decidable_count = 0`
- `semantic_equivalence_rate = null`
- `semantic_equivalence_rate_status = not_applicable`
- `na_reason = no_decidable_verifier_outcomes`

This summary generation is local synthetic test behavior only. It is not official Semantic Equivalence Rate computation.
