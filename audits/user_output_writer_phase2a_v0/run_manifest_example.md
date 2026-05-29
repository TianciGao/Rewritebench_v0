# Run Manifest Example

Representative fields written by `output/results/<run_id>/run_manifest.json`:

```json
{
  "schema_version": "user_output_run_manifest_v0",
  "run_id": "timing_sqlglot_noop_postgres_smoke",
  "source_run_dir": "runs/user/timing_sqlglot_noop_postgres_smoke",
  "result_root": "/tmp/.../output/results/timing_sqlglot_noop_postgres_smoke",
  "log_root": "/tmp/.../output/logs/timing_sqlglot_noop_postgres_smoke",
  "report_root": "/tmp/.../output/reports/timing_sqlglot_noop_postgres_smoke",
  "case_set": "common_core_v0",
  "selected_case_count": 2,
  "selected_engines": ["postgres"],
  "route_id": "sqlglot_noop",
  "method_id": "sqlglot",
  "timing_enabled": true,
  "timing_policy_id": "local_exact_gated_default_v0",
  "verifier_enabled": false,
  "verifier_tools_requested": [],
  "verifier_tools_completed": [],
  "output_contract_version": "v0",
  "local_diagnostic_only": true,
  "official_metric_input": false,
  "paper_result_input": false,
  "retained_evidence_promoted": false,
  "leaderboard_input": false
}
```

The temporary output root used by the smoke was removed after validation. No repository-level `output/` runtime artifacts were committed.
