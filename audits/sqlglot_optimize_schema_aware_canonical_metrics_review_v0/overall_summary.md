# Overall Summary

Source: `metrics/local_metrics_summary.json`.

Canonical counts copied from `overall.counts`:

- selected: 120
- candidate_generated: 105
- preflight_passed: 105
- source_executable: 100
- candidate_executable: 91
- exact: 66
- mismatch: 25
- label_only_mismatch: 16
- unsupported_fail_closed: 5
- timing_eligible: 66
- timed: 66
- speedup_denominator: 66

Canonical rates copied from `overall.rates`:

- generation_rate: 0.875
- execution_coverage_rate: 0.7583333333333333
- result_consistency_rate: 0.55

Canonical speedup diagnostics copied from `overall.performance`:

- gm_speedup_ratio: 1.020315612310745
- speedup_p10: 0.9706250147027313
- speedup_p25: 0.9929843677046468
- speedup_p50: 1.0030570718919793
- speedup_p75: 1.0116739305181726
- speedup_p90: 1.0739447492006393

Deferred canonical metric statuses:

- Semantic Equivalence Rate: not applicable without formal verifier evidence.
- Cross-Engine GM Speedup Ratio: not applicable without target-engine paired timing.
- POCR: not applicable; external skill adapter pending.
- Regression@20: not implemented in formal local metrics v0 scope.
