# Per-Engine Summary

Source: `metrics/local_metrics_by_engine.csv`.

PostgreSQL row:

- selected: 40
- candidate_generated: 34
- candidate_executable: 32
- exact: 29
- timed: 29
- generation_rate: 0.85
- execution_coverage_rate: 0.8
- result_consistency_rate: 0.725
- gm_speedup_ratio: 1.0485753363343828

MySQL row:

- selected: 40
- candidate_generated: 32
- candidate_executable: 29
- exact: 20
- timed: 20
- generation_rate: 0.8
- execution_coverage_rate: 0.725
- result_consistency_rate: 0.5
- gm_speedup_ratio: 0.9986065408169843

Spark row:

- selected: 40
- candidate_generated: 39
- candidate_executable: 30
- exact: 17
- timed: 17
- generation_rate: 0.975
- execution_coverage_rate: 0.75
- result_consistency_rate: 0.425
- gm_speedup_ratio: 0.9988089830968593

These values are copied from the canonical CSV rows, not recalculated in this audit.
