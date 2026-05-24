# SQLGlot Optimize Schema-Aware Spark Blocker Policy v0

Task: `sqlglot_optimize_schema_aware_spark_blocker_policy_v0`

Branch: `feature/case-package-v2-external-schema`

This packet records a narrow Spark blocker policy review for `sqlglot_optimize_schema_aware` after the post-ARRAY_ANY bounded tri-engine rerun.

Scope:

- `CONS_0005` / Spark semantic mismatch.
- `CONS_0036` / Spark label-only mismatch.

No new benchmark run, timing collection, verifier pass, checker normalization change, official metric computation, Semantic Equivalence Rate computation, paper report/result update, retained-evidence promotion, leaderboard output, denominator change, or case membership change occurred.

## Verdict

- `CONS_0005` / Spark is a true semantic-risk mismatch: source result has 0 rows, candidate result has 1 row `{"i": 1, "j": 3}`.
- `CONS_0036` / Spark is label-only under strict label policy: values match, but source labels are `NAME` and `C` while candidate labels are `name` and `c`.
- `CONS_0036` is a reasonable future checker-normalization policy candidate, but normalization should not be implemented in this task.
- `sqlglot_optimize_schema_aware` is ready for exact-gated timing only over the current six exact rows.
- Full Track A 120 readiness remains blocked by the Spark `CONS_0005` semantic mismatch and unresolved Spark label policy.
