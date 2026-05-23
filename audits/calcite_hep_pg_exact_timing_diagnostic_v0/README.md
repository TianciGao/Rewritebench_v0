# calcite_hep_pg_exact_timing_diagnostic_v0

Task: local-only PostgreSQL timing diagnostic for the Calcite HEP fail-closed route.

Source execution/checker gate:

- Audit: `audits/calcite_hep_pg_execution_checker_diagnostic_v0/`
- Selected PostgreSQL rows: 40
- Generated candidate rows: 33
- Exact/result-consistent rows: 20
- Non-timed diagnostic rows: 20

Timing was attempted only for the 20 rows marked exact/result-consistent in the source audit. All 20 were timed successfully with the existing local timing defaults: warmup 1, measured repetitions 5, timeout 30 seconds, median statistic, fresh PostgreSQL schema per row, source-then-candidate order.

Diagnostic timing result:

- Timed exact rows: 20
- Timing failures: 0
- Diagnostic GM speedup: 0.995749
- Diagnostic median speedup: 0.994866
- Diagnostic speedup percentiles: P10 0.955860, P25 0.977056, P50 0.994866, P75 1.005032, P90 1.057408

Boundary:

- This is a local diagnostic timing pass only.
- It is not an official metric computation.
- It does not update paper reports/results.
- It does not promote retained evidence.
- It did not time no-candidate, mismatch, source-failed, or candidate-failed rows.
