# calcite_hep_pg_local_metrics_projection_v0

Task: local-only PostgreSQL bounded route-card / metrics projection for the Calcite HEP fail-closed route.

Inputs used:

- `audits/calcite_hep_pg_bounded_candidate_generation_v0/`
- `audits/calcite_hep_pg_execution_checker_diagnostic_v0/`
- `audits/calcite_hep_pg_exact_timing_diagnostic_v0/`

No new candidate generation, SQL execution, result checking, timing, verifier pass, MySQL/Spark run, full Track-A run, official metric computation, paper report update, retained-evidence promotion, or leaderboard output was performed.

Route-card headline:

- Selected PostgreSQL rows: 40
- Generated candidate rows: 33
- Candidate-executable rows: 23
- Exact/result-consistent rows: 20
- Exact timed rows: 20
- Local generation rate: 0.825000
- Local execution coverage rate: 0.575000
- Local result consistency rate: 0.500000
- Diagnostic GM speedup over exact timed rows: 0.995749

This is a denominator-aware local diagnostic route card only. It is not official paper evidence.
