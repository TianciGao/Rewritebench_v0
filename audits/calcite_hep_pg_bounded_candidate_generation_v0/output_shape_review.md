# Output Shape Review

Runtime output followed the D035 output layout under the task-local `/tmp` root:

- Results: `/tmp/sqlrb_calcite_hep_pg_bounded_candidate_generation_v0/output/results/calcite_hep_pg_candidate_generation/`
- Logs: `/tmp/sqlrb_calcite_hep_pg_bounded_candidate_generation_v0/output/logs/calcite_hep_pg_candidate_generation/`
- Reports: `/tmp/sqlrb_calcite_hep_pg_bounded_candidate_generation_v0/output/reports/calcite_hep_pg_candidate_generation/`

A transient user workspace was created by the user-entry facade and copied to:

- `/tmp/sqlrb_calcite_hep_pg_bounded_candidate_generation_v0/run_snapshot/`

The transient repository `runs/user/calcite_hep_pg_candidate_generation` directory was removed after the local snapshot was copied to `/tmp`.

The per-row candidate ledger shape records:

- `case_id`, `pool`, `engine`
- `method_id=calcite_hep_fail_closed`
- `route_id=calcite_hep_fail_closed`
- source SQL and schema traces
- `candidate_generated`
- candidate SQL path and SHA-256 when generated
- fail-closed bucket and reason when not generated
- Calcite runtime status and adapter exit code
- stdout/stderr trace paths
- `local_only=true`
- `official_metric_input=false`
- `paper_result=false`

No repository-level `output/`, top-level `reports/`, top-level `results/`, or committed `runs/user/` artifact was produced.
