# SQLGlot Optimize CONS_0005 Triage v0

Verdict: `context_free_optimizer_qualification_gap`

This audit triages the SQLGlot optimize route failure on `CONS_0005` from `sqlglot_user_adapter_bounded_smoke_v0`. It is diagnosis-only. No benchmark code, adapter code, SQL files, cases, schemas, checker configs, reports/results, or retained evidence were modified.

## Summary

`CONS_0005` source SQL:

```sql
SELECT i, j
FROM table1
WHERE table1.j NOT IN (
  SELECT i
  FROM table2
  WHERE table1.i = table2.j
);
```

The `sqlglot_optimize` route parses this query successfully for PostgreSQL, MySQL, and Spark dialects. It then calls SQLGlot `optimize(expression)` without schema/catalog context and emits a candidate whose subquery projects an invalid three-part reference:

- PostgreSQL: `"table1"."table2"."i"`
- MySQL: `` `table1`.`table2`.`i` ``
- Spark: `` `table1`.`table2`.`i` ``

All three engines reject that candidate during candidate execution. Source execution succeeds, candidate preflight passes, and checker is not attempted for the failed `CONS_0005` candidate rows.

## Root Cause Category

Likely root cause: SQLGlot optimizer qualification behavior under missing schema/catalog context for a correlated subquery with an unqualified inner projection. This is a context-free optimize-route limitation rather than a DB backend issue, checker issue, timing issue, official-metric issue, or benchmark code failure.

This does not prove the case SQL is invalid: the no-op parse/emit route executed exactly on PostgreSQL, MySQL, and Spark in the bounded smoke. It also does not prove that a schema-aware SQLGlot route would be safe as a drop-in replacement; that would alter route semantics and needs separate authorization.

## Recommendation

Keep the current optimize route as fail-visible local diagnostic behavior. If desired, authorize a separate future task to design and test a schema-aware SQLGlot route, with explicit route naming and comparability boundaries. A documentation warning that the current optimize route is context-free and may emit invalid qualification is also reasonable, but documentation changes were not made in this triage.
