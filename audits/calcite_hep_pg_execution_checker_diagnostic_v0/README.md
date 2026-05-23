# Calcite HEP PostgreSQL Execution Checker Diagnostic

Task: `calcite_hep_pg_execution_checker_diagnostic_v0`

Branch: `feature/case-package-v2-external-schema`

Verdict: PostgreSQL-only local execution/checker diagnostic completed over the Calcite HEP candidate-generation ledger from `audits/calcite_hep_pg_bounded_candidate_generation_v0/`.

Summary:

| metric | count |
| --- | --- |
| selected_rows | 40 |
| generated_candidate_rows | 33 |
| no_candidate_rows | 7 |
| execution_attempted_rows | 33 |
| source_executable_rows | 31 |
| candidate_executable_rows | 23 |
| checker_attempted_rows | 23 |
| exact_rows | 20 |
| mismatch_rows | 3 |
| source_execution_failed_rows | 2 |
| candidate_execution_failed_rows | 8 |

Local diagnostic result-consistency rate over selected rows: `0.5`. This is not an official metric and is not paper evidence.

Runtime root: `/tmp/sqlrb_calcite_hep_pg_execution_checker_diagnostic_v0`

No timing, verifier pass, official metrics, paper reports/results update, retained-evidence promotion, leaderboard output, denominator change, case membership change, or paper result change occurred.
