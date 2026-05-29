# Semantic Equivalence Summary Review

Summary path:

```text
/tmp/sqlrb_verieql_cons0007_one_pair_canary_v0/results/verieql_cons0007_one_pair_canary_v0/verifier/semantic_equivalence_summary.json
```

Key fields:

```json
{
  "run_id": "verieql_cons0007_one_pair_canary_v0",
  "pairs_planned": 1,
  "pairs_attempted": 1,
  "equivalent_count": 0,
  "non_equivalent_count": 0,
  "unknown_count": 0,
  "timeout_count": 0,
  "unsupported_count": 1,
  "tool_error_count": 0,
  "not_attempted_count": 0,
  "decidable_count": 0,
  "semantic_equivalence_rate": null,
  "semantic_equivalence_rate_status": "not_applicable",
  "na_reason": "no_decidable_verifier_outcomes",
  "result_checker_exactness_used": false,
  "tool_available": true,
  "detection_reason": "verieql_root_available",
  "invocation_mode": "jsonl_batch"
}
```

Boundary flags:

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

- The local summary is present and contract-shaped.
- Semantic Equivalence Rate is not computed because the only pair was unsupported and therefore not decidable.
- Local result-checker exactness was not used as verifier evidence.
- This remains local canary evidence only.
