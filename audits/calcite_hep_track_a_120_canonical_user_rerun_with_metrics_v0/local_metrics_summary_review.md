# Local Metrics Summary Review

Source of truth:

```text
runs/user/calcite_hep_track_a_120_canonical_v0/metrics/local_metrics_summary.json
```

Canonical overall counts copied from `overall.counts`:

| Field | Value |
| --- | ---: |
| selected | 120 |
| candidate_generated | 99 |
| preflight_passed | 99 |
| source_executable | 98 |
| candidate_executable | 95 |
| exact | 81 |
| mismatch | 14 |
| label_only_mismatch | 4 |
| unsupported_fail_closed | 1 |
| timing_eligible | 80 |
| timed | 80 |
| timing_partial_failure | 0 |
| speedup_denominator | 80 |

Canonical rates copied from `overall.rates`:

| Field | Value |
| --- | ---: |
| generation_rate | 0.825 |
| execution_coverage_rate | 0.7916666666666666 |
| result_consistency_rate | 0.675 |

Canonical performance copied from `overall.performance`:

| Field | Value |
| --- | ---: |
| gm_speedup_ratio | 0.9852158585899714 |
| speedup_denominator | 80 |
| speedup_p10 | 0.9348057176014165 |
| speedup_p25 | 0.9802357647404241 |
| speedup_p50 | 0.9952238487768534 |
| speedup_p75 | 1.0054822795790077 |
| speedup_p90 | 1.026117745021687 |

The canonical output reports 81 exact rows and 80 timed rows. `local_timing_speedup_rows.csv` marks `PORT_0024 / postgres` as exact but `timing_status=not_eligible` with `exclusion_reason=timing_not_eligible`; this distinction is preserved here.

Deferred or non-applicable canonical diagnostics:
- Semantic Equivalence Rate: `not_applicable`, formal verifier evidence missing.
- Cross-engine GM speedup ratio: `not_applicable`, target-engine paired timing missing.
- POCR: `not_applicable`, external skill adapter pending.
- Formal Regression@20: not emitted as a formal local metric.
