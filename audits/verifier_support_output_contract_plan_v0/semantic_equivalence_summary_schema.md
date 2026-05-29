# Semantic Equivalence Summary Schema

`semantic_equivalence_summary.json` summarizes verifier outcomes for one local run.

Required fields:

- `run_id`
- `verifier_tools_requested`
- `verifier_tools_completed`
- `pairs_planned`
- `pairs_attempted`
- `equivalent_count`
- `non_equivalent_count`
- `unknown_count`
- `timeout_count`
- `unsupported_count`
- `tool_error_count`
- `decidable_count`
- `semantic_equivalence_rate`
- `verifier_decidability_rate`
- `na_reason`
- `local_diagnostic_only`
- `official_metric_input`
- `paper_result_input`
- `retained_evidence_promoted`
- `leaderboard_input`

Definitions:

- `decidable_count = equivalent_count + non_equivalent_count`
- `semantic_equivalence_rate = equivalent_count / decidable_count` when `decidable_count > 0`
- `semantic_equivalence_rate = null` with `na_reason` when `decidable_count == 0`
- `verifier_decidability_rate = decidable_count / result_consistent_pairs` when that denominator exists

N.A. policy:

- If no verifier evidence exists, Semantic Equivalence Rate remains `N.A.`.
- Local result checker exactness is not a substitute for formal semantic equivalence verification.
- Unknown/undecidable outcomes must be reported separately, not forced into equivalent or non-equivalent buckets.
