# Semantic Equivalence Summary Review

Summary path:

```text
/tmp/sqlrb_verieql_perf0062_one_pair_canary_v0/results/verieql_perf0062_one_pair_canary_v0/verifier/semantic_equivalence_summary.json
```

Key fields:

```json
{
  "pairs_planned": 1,
  "pairs_attempted": 1,
  "equivalent_count": 0,
  "non_equivalent_count": 0,
  "decidable_count": 0,
  "timeout_count": 1,
  "unsupported_count": 0,
  "tool_error_count": 0,
  "not_attempted_count": 0,
  "semantic_equivalence_rate": null,
  "semantic_equivalence_rate_status": "not_applicable",
  "na_reason": "no_decidable_verifier_outcomes",
  "result_checker_exactness_used": false
}
```

Boundary fields:

```json
{
  "local_diagnostic_only": true,
  "official_metric_input": false,
  "paper_result_input": false,
  "retained_evidence_promoted": false,
  "leaderboard_input": false
}
```

Interpretation:

- A local verifier-support summary was produced.
- It does not compute an official Semantic Equivalence Rate.
- The only pair timed out, so there are no decidable formal verifier outcomes.
- Local result-checker exactness was not substituted for verifier evidence.
