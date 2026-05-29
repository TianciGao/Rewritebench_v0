# Route Card

Route card: Calcite HEP fail-closed PostgreSQL local diagnostic after the identifier-quoting fix.

| field | value |
| --- | ---: |
| selected_rows | 40 |
| generated_candidate_rows | 33 |
| no_candidate_rows | 7 |
| schema_fallback_rows | 4 |
| schema_fallback_excluded_rows | 4 |
| execution_attempted_rows | 29 |
| source_executable_rows | 28 |
| candidate_executable_rows | 28 |
| checker_attempted_rows | 28 |
| exact_rows | 22 |
| mismatch_rows | 6 |
| source_execution_failed_rows | 1 |
| candidate_execution_failed_rows | 0 |
| timing_attempted_rows | 22 |
| timed_exact_rows | 22 |
| timing_failed_rows | 0 |

Local diagnostic coverage rates using selected rows as denominator:

| field | value |
| --- | ---: |
| local_generation_rate | 0.825000 |
| local_execution_coverage_rate | 0.700000 |
| local_result_consistency_rate | 0.550000 |

Exact-timed speedup diagnostics:

| field | value |
| --- | ---: |
| diagnostic_gm_speedup | 1.009852 |
| diagnostic_speedup_p10 | 0.981979 |
| diagnostic_speedup_p25 | 0.989623 |
| diagnostic_speedup_p50 | 0.995700 |
| diagnostic_speedup_p75 | 1.005620 |
| diagnostic_speedup_p90 | 1.008519 |

Boundary flags:

- `official_metric_input=false`
- `paper_result=false`
- `leaderboard_output_created=false`
