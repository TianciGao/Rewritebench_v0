# Timing Policy

Timing policy:

- exact-gated: yes
- warmup executions: 1
- measured repetitions: 5
- timeout: 30 seconds
- statistic: median
- speedup ratio: `source_median_ms / candidate_median_ms`

Rows excluded from timing:

- mismatches
- fail-closed rows
- candidate execution failures
- no-candidate rows
- unsupported rows
- label-only mismatch rows under the current strict-label policy

The timing helper executed only source and candidate SQL for exact rows. It did not run verifiers and did not compute official metrics.
