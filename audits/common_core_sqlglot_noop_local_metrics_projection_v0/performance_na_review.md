# Performance N.A. Review

Performance metrics are not available for this Common-core projection because the selected input runs do not contain timing artifacts.

Reviewed input runs:

- `runs/user/common_core_sqlglot_noop_postgres_snapshot`
- `runs/user/common_core_sqlglot_noop_mysql_snapshot`
- `runs/user/common_core_spark_sqlglot_noop_after_statement_patch`

Observed calculator performance status:

| Engine | timing_policy_id | timing_eligible | timed | speedup_denominator | GM Speedup Ratio | performance_na_reason |
|---|---|---:|---:|---:|---|---|
| PostgreSQL | `not_timed` | 0 | 0 | 0 | `null` | `no_exact_timed_rows` |
| MySQL | `not_timed` | 0 | 0 | 0 | `null` | `no_exact_timed_rows` |
| Spark | `not_timed` | 0 | 0 | 0 | `null` | `no_exact_timed_rows` |

The per-row speedup CSVs contain 40 rows per engine and no rows included in performance. Exact rows are excluded with `timing_not_eligible`; non-exact rows are excluded with `not_exact`.

No new timing was collected. No official speedup, route-level paper metric, paper table, retained evidence, reports/results output, or leaderboard was produced.

Deferred performance/generalization outputs remain:

- Cross-Engine GM Speedup Ratio: `not_applicable`, target-engine paired timing missing.
- Semantic Equivalence Rate: `not_applicable`, formal verifier evidence missing.
- POCR: `not_applicable`, external skill adapter pending.
- Regression@20: not implemented under D033.
