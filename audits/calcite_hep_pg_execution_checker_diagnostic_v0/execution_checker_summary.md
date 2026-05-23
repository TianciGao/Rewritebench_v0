# Execution Checker Summary

Core counts:

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
| schema_fallback_rows | 4 |
| schema_fallback_exact_rows | 0 |
| schema_fallback_failed_rows | 4 |

Status counts:

| source_execution_status | count |
| --- | --- |
| not_attempted | 7 |
| source_execution_failed | 2 |
| source_execution_success | 31 |

| candidate_execution_status | count |
| --- | --- |
| candidate_execution_failed | 8 |
| candidate_execution_success | 23 |
| execution_not_enabled | 2 |
| not_attempted | 7 |

| checker_status | count |
| --- | --- |
| checker_mismatch | 3 |
| checker_success | 20 |
| not_attempted | 17 |

Exact rows:

PERF_0006, PERF_0007, PERF_0008, PERF_0013, PERF_0017, PERF_0019, PERF_0024, PERF_0033, PERF_0034, PERF_0052, PERF_0054, PERF_0056, PERF_0077, PERF_0082, CONS_0005, CONS_0007, CONS_0009, CONS_0010, CONS_0012, CONS_0024

Local diagnostic result-consistency rate over selected rows: `0.5`. This is diagnostic-only and not an official metric.
