# Output Shape Review

The route fits the existing user candidate ledger shape.

Ledger behavior:

- `candidate_generated=false`
- `candidate_sql_path` empty
- `extraction_status=no_candidate_sql`
- `failure_bucket=no_candidate_sql`
- DB execution and checker evaluation remain skipped unless a future run explicitly enables them and a candidate exists.

D035 export behavior:

- Results: `output/results/<run_id>/` or an explicit local output root with the same `results/<run_id>/` shape.
- Logs: `output/logs/<run_id>/`.
- Reports: `output/reports/<run_id>/`.
- The tiny smoke used `/tmp/.../d035_output/results|logs|reports/calcite_hep_scaffold_smoke/`.

Route identity:

- `run_manifest.json` records `route_id=calcite_hep_fail_closed`.
- `run_manifest.json` records `method_id=calcite_hep_fail_closed`.

Boundary:

- `local_diagnostic_only=true`
- `official_metric_input=false`
- `paper_result_input=false`
- `retained_evidence_promoted=false`
- `leaderboard_input=false`
