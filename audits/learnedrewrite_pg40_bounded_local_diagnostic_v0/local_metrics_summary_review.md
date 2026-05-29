# Local Metrics Summary Review

Source: `runs/user/learnedrewrite_pg40_bounded_diagnostic_v0/metrics/local_metrics_summary.json`, produced by `python -m cli.main user compute-local-metrics` using `src/sql_rewrite_bench/local_metrics.py`.

These values are copied from local_metrics.py outputs only.

| Field | Value |
| --- | ---: |
| selected | 40 |
| generated | 29 |
| candidate_executable | 23 |
| exact | 17 |
| mismatch | 6 |
| timed exact rows | 17 |
| generation rate | 0.725 |
| execution coverage | 0.575 |
| result consistency | 0.425 |
| GM speedup | 1.0291029729677286 |
| P10 | 0.8134186116858578 |
| P25 | 0.9784093859740545 |
| P50 | 1.0023559404279565 |
| P75 | 1.014471169398659 |
| P90 | 1.704766251233957 |
| SER status | N.A. (`not_applicable` in local_metrics.py JSON) |
| POCR status | deferred / N.A. (`not_applicable` in local_metrics.py JSON) |

Metric output paths created under the runtime run before cleanup:

- `runs/user/learnedrewrite_pg40_bounded_diagnostic_v0/metrics/local_metrics_summary.json`
- `runs/user/learnedrewrite_pg40_bounded_diagnostic_v0/metrics/local_metrics_by_engine.csv`
- `runs/user/learnedrewrite_pg40_bounded_diagnostic_v0/metrics/local_metrics_by_pool.csv`
- `runs/user/learnedrewrite_pg40_bounded_diagnostic_v0/metrics/local_timing_speedup_rows.csv`
- `runs/user/learnedrewrite_pg40_bounded_diagnostic_v0/metrics/local_metrics_boundary.md`

The CLI exported the same metrics under `/tmp/sqlrb_learnedrewrite_pg40_bounded_local_diagnostic_v0/output/results/learnedrewrite_pg40_bounded_diagnostic_v0/metrics/` before runtime-output cleanup.
