# Engine Metrics Review

Source: `metrics/local_metrics_by_engine.csv`, copied to `canonical_engine_metrics_snapshot.csv`.

PostgreSQL:

- selected: 40
- candidate_generated: 34
- source_executable: 34
- candidate_executable: 32
- exact: 29
- mismatch: 3
- label_only_mismatch: 2
- timed: 29
- generation_rate: 0.85
- execution_coverage_rate: 0.8
- result_consistency_rate: 0.725
- gm_speedup_ratio: 1.0485753363343828
- speedup p10/p25/p50/p75/p90: 0.9936317917950342 / 0.9984599387585501 / 1.0035449609727676 / 1.0100052234906263 / 1.0376695086997443

MySQL:

- selected: 40
- candidate_generated: 32
- source_executable: 32
- candidate_executable: 29
- exact: 20
- mismatch: 9
- label_only_mismatch: 4
- timed: 20
- generation_rate: 0.8
- execution_coverage_rate: 0.725
- result_consistency_rate: 0.5
- gm_speedup_ratio: 0.9986065408169843
- speedup p10/p25/p50/p75/p90: 0.987303595692022 / 0.9909585944928913 / 1.0011841474307959 / 1.0069395119061264 / 1.0109773417011063

Spark:

- selected: 40
- candidate_generated: 39
- source_executable: 34
- candidate_executable: 30
- exact: 17
- mismatch: 13
- label_only_mismatch: 10
- unsupported_fail_closed: 5
- timed: 17
- generation_rate: 0.975
- execution_coverage_rate: 0.75
- result_consistency_rate: 0.425
- gm_speedup_ratio: 0.9988089830968593
- speedup p10/p25/p50/p75/p90: 0.9154147673506776 / 0.9583198262679561 / 1.026288831812628 / 1.0734287326575565 / 1.0831729605116192
