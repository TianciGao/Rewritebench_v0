# Diagnostic Metrics Summary

Local diagnostic formulas used selected PostgreSQL rows as the route-card denominator:

- `local_generation_rate = generated_candidate_rows / selected_rows = 33 / 40 = 0.825000`
- `local_execution_coverage_rate = candidate_executable_rows / selected_rows = 23 / 40 = 0.575000`
- `local_result_consistency_rate = exact_rows / selected_rows = 20 / 40 = 0.500000`

Timing diagnostics use exact timed rows only:

- Exact timed rows: 20
- Timing failures: 0
- Diagnostic GM speedup: 0.995749
- Diagnostic median/P50 speedup: 0.994866
- P10/P25/P75/P90: 0.955860 / 0.977056 / 1.005032 / 1.057408

Not computed:

- Official metrics
- Formal Regression@20
- Semantic Equivalence Rate
- Paper result rows
- Leaderboard outputs

The diagnostic speedup is approximately neutral over the exact timed subset and must not be interpreted without the 20-row non-exact/non-timed frontier.
