# Route Card

Route identity:

- `baseline_family = calcite`
- `method_id = calcite_hep_fail_closed`
- `route_id = calcite_hep_fail_closed`
- `engine = postgres`
- `local_only = true`
- `official_metric_input = false`
- `paper_result = false`
- `leaderboard_output_created = false`

Denominator chain:

| Field | Count |
| --- | ---: |
| selected_rows | 40 |
| generated_candidate_rows | 33 |
| no_candidate_rows | 7 |
| source_executable_rows | 31 |
| candidate_executable_rows | 23 |
| checker_attempted_rows | 23 |
| exact_rows | 20 |
| mismatch_rows | 3 |
| source_execution_failed_rows | 2 |
| candidate_execution_failed_rows | 8 |
| timed_exact_rows | 20 |
| timing_failed_rows | 0 |

Local diagnostic coverage rates over selected rows:

| Field | Formula | Value |
| --- | --- | ---: |
| local_generation_rate | 33 / 40 | 0.825000 |
| local_execution_coverage_rate | 23 / 40 | 0.575000 |
| local_result_consistency_rate | 20 / 40 | 0.500000 |

Exact-timed speedup diagnostics:

| Field | Value |
| --- | ---: |
| diagnostic_gm_speedup | 0.995749 |
| diagnostic_speedup_p10 | 0.955860 |
| diagnostic_speedup_p25 | 0.977056 |
| diagnostic_speedup_p50 | 0.994866 |
| diagnostic_speedup_p75 | 1.005032 |
| diagnostic_speedup_p90 | 1.057408 |
