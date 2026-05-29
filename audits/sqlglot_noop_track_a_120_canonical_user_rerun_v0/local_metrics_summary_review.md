# Local Metrics Summary Review

Source: `runs/user/sqlglot_noop_track_a_120_canonical_v0/metrics/local_metrics_summary.json`

Canonical overall counts copied from `overall.counts`:

| Field | Value |
| --- | ---: |
| selected | 120 |
| candidate_generated | 115 |
| preflight_passed | 115 |
| source_executable | 110 |
| candidate_executable | 107 |
| exact | 97 |
| mismatch | 10 |
| label_only_mismatch | 5 |
| unsupported_fail_closed | 5 |
| timing_eligible | 97 |
| timed | 97 |
| timing_partial_failure | 0 |
| speedup_denominator | 97 |

Canonical rates copied from `overall.rates`:

| Field | Value |
| --- | ---: |
| generation_rate | 0.9583333333333334 |
| execution_coverage_rate | 0.8916666666666667 |
| result_consistency_rate | 0.8083333333333333 |

Canonical performance values copied from `overall.performance`:

| Field | Value |
| --- | ---: |
| gm_speedup_ratio | 0.9798350077258852 |
| speedup_p10 | 0.9402013795777502 |
| speedup_p25 | 0.9830818562518341 |
| speedup_p50 | 0.9973694789124162 |
| speedup_p75 | 1.0082898937485303 |
| speedup_p90 | 1.0268045388090905 |

Deferred canonical diagnostics:
- Semantic Equivalence Rate: `not_applicable`, reason `formal_verifier_evidence_missing`.
- POCR: `not_applicable`, reason `external_skill_adapter_pending`.
- Cross-engine GM speedup: `not_applicable`, reason `target_engine_paired_timing_missing`.
