# Timing Summary

Timing policy:

- Exact-gated only.
- Warmup: 1.
- Measured repetitions: 5.
- Timeout: 30 seconds.
- Statistic: median.
- Execution order: source then candidate.

Timing summary:

| field | count |
| --- | ---: |
| exact_rows | 22 |
| timing_attempted_rows | 22 |
| timed_exact_rows | 22 |
| timing_failed_rows | 0 |
| non_timed_rows | 18 |

Diagnostic speedup over the 22 exact timed rows:

| statistic | value |
| --- | ---: |
| GM speedup | 1.009852 |
| P10 | 0.981979 |
| P25 | 0.989623 |
| P50 / median | 0.995700 |
| P75 | 1.005620 |
| P90 | 1.008519 |

These timing values are local diagnostics over exact timed rows only. They are not official paper metrics and are not formal Regression@20.
