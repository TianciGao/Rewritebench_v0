# Local Metrics Summary Review

Source: `metrics/local_metrics_summary.json`, copied to `canonical_metrics_snapshot.json`.

Canonical overall counts:

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

Canonical rates:

- generation_rate: 0.875
- execution_coverage_rate: 0.7583333333333333
- result_consistency_rate: 0.55

Canonical speedup diagnostics over strict exact + timed rows:

- gm_speedup_ratio: 1.020315612310745
- p10: 0.9706250147027313
- p25: 0.9929843677046468
- p50: 1.0030570718919793
- p75: 1.0116739305181726
- p90: 1.0739447492006393

Deferred metrics remain canonical N.A. or deferred:

- Semantic Equivalence Rate: not_applicable
- Cross-Engine GM Speedup Ratio: not_applicable
- POCR: not_applicable / skill adapter pending
- Regression@20: not_implemented
