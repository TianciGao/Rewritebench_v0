# Source Audit Inputs

The triage used committed audit artifacts from:

- `audits/sqlglot_optimize_schema_aware_bounded_tri_engine_execution_checker_v0/per_row_execution_checker_status.csv`
- `audits/sqlglot_optimize_schema_aware_bounded_tri_engine_execution_checker_v0/diagnostic_summary.json`
- `audits/sqlglot_optimize_schema_aware_bounded_tri_engine_execution_checker_v0/execution_checker_summary.md`
- `audits/sqlglot_optimize_schema_aware_bounded_tri_engine_execution_checker_v0/cons0005_execution_review.md`
- `audits/sqlglot_optimize_schema_aware_bounded_tri_engine_execution_checker_v0/failure_bucket_review.md`

The prior runtime traces were still available under:

- `/tmp/sqlrb_sqlglot_optimize_schema_aware_bounded_tri_engine_execution_checker_v0/runtime/sqlglot_optimize_schema_aware_bounded_tri_engine_execution_checker_v0/`

Trace files inspected:

- `candidate_sql/CONS_0005__mysql.sql`
- `candidate_sql/CONS_0005__spark.sql`
- `candidate_sql/CONS_0036__spark.sql`
- `workspaces/CONS_0005/mysql/adapter_stderr.txt`
- `workspaces/CONS_0005/mysql/execution/mysql_same_engine/candidate_error.txt`
- `workspaces/CONS_0005/spark/checker/mismatch_summary.json`
- `workspaces/CONS_0005/spark/execution/source_result.jsonl`
- `workspaces/CONS_0005/spark/execution/candidate_result.jsonl`
- `workspaces/CONS_0005/spark/execution/setup.sql`
- `workspaces/CONS_0036/spark/checker/mismatch_summary.json`
- `workspaces/CONS_0036/spark/execution/source_result.jsonl`
- `workspaces/CONS_0036/spark/execution/candidate_result.jsonl`

No targeted rerun was needed because the existing committed audit outputs and local `/tmp` traces were sufficient to answer the triage questions.

## Prior diagnostic summary

- Planned rows: 9.
- Generated candidates: 9.
- Preflight passed: 9.
- Source executable: 9.
- Candidate executable: 8.
- Checker attempted: 8.
- Exact/result-consistent: 6.
- Mismatches: 2.
- Source execution failures: 0.
- Candidate execution failures: 1.

By engine:

- PostgreSQL: 3/3 exact.
- MySQL: 2/3 exact; `CONS_0005` candidate execution failed.
- Spark: 1/3 exact; `CONS_0005` and `CONS_0036` mismatched.

Boundary:

- `official_metric_input = false`
- `paper_result = false`
- timing was not collected
- verifiers were not run

