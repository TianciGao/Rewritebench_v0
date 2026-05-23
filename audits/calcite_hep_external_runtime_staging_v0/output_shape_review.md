# Output Shape Review

The tiny smoke used the D035 user-output facade and wrote only under:

- `/tmp/sqlrb_calcite_hep_external_runtime_staging_v0/smoke_output/results/calcite_hep_external_runtime_smoke/`
- `/tmp/sqlrb_calcite_hep_external_runtime_staging_v0/smoke_output/logs/calcite_hep_external_runtime_smoke/`
- `/tmp/sqlrb_calcite_hep_external_runtime_staging_v0/smoke_output/reports/calcite_hep_external_runtime_smoke/`

The exported manifest recorded:

- `route_id=calcite_hep_fail_closed`
- `method_id=calcite_hep_fail_closed`

The candidate ledger records:

- `candidate_generated=true` for all 3 rows.
- `extraction_status=captured_from_candidate_file`.
- `failure_bucket=none`.
- `official_metric_input=false`.
- `retained_evidence_input=false`.

No top-level `reports/`, top-level `results/`, repository-level `output/`, or committed `runs/user/` artifacts were produced.
