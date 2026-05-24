# SQLGlot Optimize Schema-Aware Track A 120 Exact Timing

Task: `sqlglot_optimize_schema_aware_track_a_120_exact_timing_v0`

This packet records a local-only exact-gated timing diagnostic for `route_id=sqlglot_optimize_schema_aware` over the Common-core v0 Track A planned set of 40 cases x 3 same-engine rows.

The exact gate source is `audits/sqlglot_optimize_schema_aware_track_a_120_execution_checker_diagnostic_v0/`. Only the 66 rows marked exact/result-consistent there were timed. The remaining 54 rows remain denominator-visible as non-timed frontier rows.

Summary:

| Field | Value |
| --- | ---: |
| selected rows | 120 |
| generated candidate rows | 105 |
| fail-closed rows | 20 |
| candidate executable rows | 91 |
| checker attempted rows | 91 |
| exact rows | 66 |
| timing attempted rows | 66 |
| timed exact rows | 66 |
| timing failed rows | 0 |
| diagnostic GM speedup | 1.022011 |
| P10/P25/P50/P75/P90 | 0.942395 / 0.986440 / 0.997147 / 1.011439 / 1.097909 |

This is not official metric input, not a paper result, not retained evidence promotion, and not leaderboard output.
