# Output Shape Review

Runtime output was written only under the task-local `/tmp` root:

- Results: `/tmp/sqlrb_calcite_hep_pg_execution_checker_diagnostic_v0/output/results/calcite_hep_pg_execution_checker/`
- Logs: `/tmp/sqlrb_calcite_hep_pg_execution_checker_diagnostic_v0/output/logs/calcite_hep_pg_execution_checker/`
- Reports: `/tmp/sqlrb_calcite_hep_pg_execution_checker_diagnostic_v0/output/reports/calcite_hep_pg_execution_checker/`

Committed audit copies:

- `per_row_execution_checker_status.csv`
- `diagnostic_summary.json`

No repository-level `output/`, top-level `reports/`, top-level `results/`, or `runs/user/` artifacts are committed.

The per-row CSV includes the required fields for case identity, generation status, candidate origin, execution/checker statuses, exact/mismatch status, failure bucket, SQL traces, checker traces, and local-only boundary flags.
