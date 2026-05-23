# Timing Summary

Timing policy:

- exact-gated: yes
- warmup repetitions: 1
- measured repetitions: 5
- timeout: 30 seconds
- statistic: median

Timing summary:

| field | value |
| --- | ---: |
| exact_rows | 35 |
| timing_attempted_rows | 35 |
| timed_exact_rows | 35 |
| timing_failed_rows | 0 |

Exact-timed speedup diagnostics:

| field | value |
| --- | ---: |
| diagnostic_gm_speedup | 0.995912 |
| diagnostic_speedup_p10 | 0.988128 |
| diagnostic_speedup_p25 | 0.995110 |
| diagnostic_speedup_p50 | 1.002522 |
| diagnostic_speedup_p75 | 1.009285 |
| diagnostic_speedup_p90 | 1.016506 |
| diagnostic_median_speedup | 1.002522 |

These timing values are local diagnostics over exact timed rows only. They are not official paper metrics and are not formal Regression@20.
