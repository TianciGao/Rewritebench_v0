# Run Manifest Schema

Recommended path:

```text
output/results/<run_id>/run_manifest.json
```

Required fields:

- `run_id`
- `created_at`
- `git_commit`
- `benchmark_version`
- `workbench_version`
- `case_set`
- `selected_cases`
- `selected_engines`
- `adapter_command`
- `route_id`
- `method_id`
- `denominator_id`
- `timing_enabled`
- `timing_policy_id`
- `verifier_enabled`
- `verifier_tools_requested`
- `verifier_tools_completed`
- `output_contract_version`
- `result_root`
- `log_root`
- `report_root`
- `local_diagnostic_only`
- `official_metric_input`
- `paper_result_input`
- `retained_evidence_promoted`
- `leaderboard_input`

Required boundary values for local user runs:

```json
{
  "local_diagnostic_only": true,
  "official_metric_input": false,
  "paper_result_input": false,
  "retained_evidence_promoted": false,
  "leaderboard_input": false
}
```

`timing_policy_id` may be `null` when timing is disabled. `verifier_tools_completed` may be empty when verifier evidence is absent; in that case Semantic Equivalence Rate remains `N.A.`.
