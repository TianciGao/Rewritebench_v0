# Semantic Equivalence Summary Review

Generated summary path:

```text
/tmp/sqlrb_verieql_synthetic_from_clause_smoke_v0/results/verieql_synthetic_from_clause_smoke_v0/verifier/semantic_equivalence_summary.json
```

Summary fields of interest:

```json
{
  "pairs_planned": 2,
  "pairs_attempted": 2,
  "equivalent_count": 0,
  "non_equivalent_count": 1,
  "timeout_count": 1,
  "unsupported_count": 0,
  "tool_error_count": 0,
  "not_attempted_count": 0,
  "decidable_count": 1,
  "semantic_equivalence_rate": 0.0,
  "semantic_equivalence_rate_status": "computed",
  "result_checker_exactness_used": false,
  "local_diagnostic_only": true,
  "official_metric_input": false,
  "paper_result_input": false,
  "retained_evidence_promoted": false,
  "leaderboard_input": false
}
```

Interpretation:

- The computed rate is a local synthetic verifier-support summary over two synthetic rows.
- It is not Common-core evidence.
- It is not official Semantic Equivalence Rate.
- It is not paper evidence.
- It is not retained evidence.
- It is not leaderboard input.

The summary confirms that the existing schema can represent a mixed outcome with one decidable verifier row and one timeout row while preserving local-only boundary flags.
