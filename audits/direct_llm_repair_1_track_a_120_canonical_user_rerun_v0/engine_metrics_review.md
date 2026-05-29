# Engine Metrics Review

Copied from `local_metrics_by_engine.csv` only.

| engine | selected | generated | candidate_executable | exact | mismatch | unsupported | timed | generation_rate | execution_coverage_rate | result_consistency_rate | gm_speedup |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| mysql | 40 | 40 | 40 | 36 | 4 | 0 | 32 | 1.0 | 1.0 | 0.9 | 1.0031908116792292 |
| postgres | 40 | 40 | 40 | 40 | 0 | 0 | 35 | 1.0 | 1.0 | 1.0 | 0.9932632014461932 |
| spark | 40 | 40 | 35 | 35 | 0 | 5 | 31 | 1.0 | 0.875 | 0.875 | 0.9975418383548386 |
