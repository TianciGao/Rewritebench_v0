# Source Audit Inputs

This policy packet uses existing committed audit outputs and local runtime traces only.

Committed source audits:

- `audits/sqlglot_optimize_schema_aware_bounded_tri_engine_execution_checker_v0/`
- `audits/sqlglot_optimize_schema_aware_bounded_tri_engine_blocker_triage_v0/`
- `audits/sqlglot_optimize_schema_aware_mysql_array_any_fail_closed_v0/`
- `audits/sqlglot_optimize_schema_aware_post_array_any_tri_engine_rerun_v0/`

Primary committed ledger:

- `audits/sqlglot_optimize_schema_aware_post_array_any_tri_engine_rerun_v0/per_row_execution_checker_status.csv`
- `audits/sqlglot_optimize_schema_aware_post_array_any_tri_engine_rerun_v0/diagnostic_summary.json`

Local runtime traces inspected:

- `/tmp/sqlrb_sqlglot_optimize_schema_aware_post_array_any_tri_engine_rerun_v0/runtime/sqlglot_optimize_schema_aware_post_array_any_tri_engine_rerun_v0/workspaces/CONS_0005/spark/checker/mismatch_summary.json`
- `/tmp/sqlrb_sqlglot_optimize_schema_aware_post_array_any_tri_engine_rerun_v0/runtime/sqlglot_optimize_schema_aware_post_array_any_tri_engine_rerun_v0/workspaces/CONS_0036/spark/checker/mismatch_summary.json`
- corresponding Spark source/candidate query and result artifacts under the same `/tmp` runtime root.

Post-ARRAY_ANY bounded rerun summary:

- planned rows: 9
- generated executable candidates: 8
- explicit fail-closed rows: 1
- source executable rows: 9
- candidate executable rows: 8
- checker attempted rows: 8
- exact/result-consistent rows: 6
- mismatches: 2
- candidate execution failures: 0

No new candidate generation, SQL execution, checker run, timing run, verifier run, or metric computation was performed for this policy packet.
