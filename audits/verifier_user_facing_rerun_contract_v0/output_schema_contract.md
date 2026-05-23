# Output Schema Contract

Future canonical verifier reruns must write under D035 output roots:

```text
output/results/<run_id>/verifier/
  verifier_pairs.csv
  verifier_verdicts.jsonl
  verifier_identity_rows.csv
  semantic_equivalence_summary.json
  tools/
    sqlsolver/
    verieql/

output/logs/<run_id>/verifier.log
output/reports/<run_id>/verifier_summary.md
```

Required per-row identity ledger fields:

- `run_id`
- `case_id`
- `pool`
- `engine`
- `method_id`
- `route_id`
- `candidate_id`
- `pair_type`
- `pair_role`
- `verifier_tool`
- `verifier_mode`
- `verifier_policy`
- `source_sql_trace`
- `candidate_sql_trace`
- `schema_trace`
- `source_vs_source_verdict`
- `candidate_vs_candidate_verdict`
- `source_vs_candidate_verdict`
- `identity_guard_passed`
- `corrected_verdict`
- `raw_output_path`
- `normalized_verdict`
- `result_checker_exactness_used`
- `local_only`
- `official_metric_input`
- `paper_result`

Required summary fields:

- `selected_rows`
- `exact_candidate_rows`
- `verifier_attempted_rows`
- `identity_checked_rows`
- `identity_passed_rows`
- `identity_failed_rows`
- `corrected_equivalent_count`
- `corrected_non_equivalent_count`
- `corrected_decidable_count`
- `corrected_unknown_count`
- `corrected_timeout_count`
- `corrected_tool_error_count`
- `corrected_local_semantic_equivalence_rate`
- `corrected_decidable_coverage_over_exact_rows`
- `identity_pass_rate`
- `official_metric_input`
- `paper_result`

Boundary defaults:

- `result_checker_exactness_used=false`
- `official_metric_input=false`
- `paper_result=false`
- `retained_evidence_promoted=false`
- `leaderboard_input=false`
