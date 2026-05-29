# Execution Checker Summary

Execution/checker stage summary:

| field | value |
| --- | ---: |
| selected_rows | 40 |
| generated_candidate_rows | 35 |
| execution_attempted_rows | 35 |
| source_executable_rows | 35 |
| candidate_executable_rows | 35 |
| checker_attempted_rows | 35 |
| exact_rows | 35 |
| mismatch_rows | 0 |
| source_execution_failed_rows | 0 |
| candidate_execution_failed_rows | 0 |
| no_candidate_rows | 5 |

The execution/checker stage was attempted only for generated candidates. All 35 generated rows executed on PostgreSQL, reached checker comparison, and were exact/result-consistent.

The five cross-dialect PORT no-candidate rows remained visible as non-exact frontier rows and were not executed or checked.
