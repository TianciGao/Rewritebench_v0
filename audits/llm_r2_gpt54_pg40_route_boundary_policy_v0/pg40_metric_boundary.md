# PG40 Metric Boundary

Metric values in this file are copied only from `local_metrics.py` outputs reviewed in `audits/llm_r2_gpt54_pg40_bounded_local_diagnostic_v0/`.

## Canonical Local Diagnostic Values

- selected: 40
- generated: 40
- candidate_executable: 39
- exact: 39
- timed exact rows: 34
- mismatch: 0
- candidate_execution_failed: 1
- generation rate: 1.0
- execution coverage: 0.975
- result consistency: 0.975
- GM speedup: 1.009691483166132
- P10/P25/P50/P75/P90: 0.5650932995267253 / 0.91306615287767 / 0.9929224218407445 / 1.6245036973766611 / 1.7340646690442811

## Boundary

These values are PostgreSQL-only PG40 local diagnostic metrics. They are not Track A 120 metrics, not official metrics, not paper results, not retained evidence, and not original LLM-R2 paper reproduction. They must not be merged into tri-engine Track A 120 canonical route tables or used for global leaderboard comparison.
