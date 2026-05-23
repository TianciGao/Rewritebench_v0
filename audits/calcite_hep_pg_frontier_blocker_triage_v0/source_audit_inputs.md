# Source Audit Inputs

This triage used committed audit outputs only.

Candidate-generation audit:

- `audits/calcite_hep_pg_bounded_candidate_generation_v0/diagnostic_summary.json`
- `audits/calcite_hep_pg_bounded_candidate_generation_v0/per_row_candidate_status.csv`
- `audits/calcite_hep_pg_bounded_candidate_generation_v0/fail_closed_review.md`

Execution/checker audit:

- `audits/calcite_hep_pg_execution_checker_diagnostic_v0/diagnostic_summary.json`
- `audits/calcite_hep_pg_execution_checker_diagnostic_v0/per_row_execution_checker_status.csv`
- `audits/calcite_hep_pg_execution_checker_diagnostic_v0/failure_bucket_review.md`
- `audits/calcite_hep_pg_execution_checker_diagnostic_v0/schema_fallback_review.md`

Timing audit:

- `audits/calcite_hep_pg_exact_timing_diagnostic_v0/diagnostic_summary.json`
- `audits/calcite_hep_pg_exact_timing_diagnostic_v0/per_row_timing.csv`

Route-card projection audit:

- `audits/calcite_hep_pg_local_metrics_projection_v0/route_card.json`
- `audits/calcite_hep_pg_local_metrics_projection_v0/non_exact_frontier.md`
- `audits/calcite_hep_pg_local_metrics_projection_v0/blocker_summary.md`

Runtime `/tmp` artifacts were not used as metric inputs, and no replay was performed.
