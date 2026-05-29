# Next Comparison Plan

The refreshed SQLGlot noop PostgreSQL route card is locally comparable against `audits/calcite_hep_pg_post_quoting_chain_rerun_v0/` because both packets use:

- Common-core v0 PostgreSQL selected rows as the route-card denominator;
- D035-shaped runtime output under a task-local `/tmp` root;
- local candidate generation, execution/checker, exact-gated timing, and route-card projection;
- local-only boundary flags;
- no official metrics, no Semantic Equivalence Rate, no retained-evidence promotion, and no leaderboard output.

Recommended next task:

Create a bounded local diagnostic comparison packet for SQLGlot noop vs Calcite HEP PostgreSQL route cards. The comparison should remain local-only and should keep the non-exact frontiers visible for both routes.

Still blocked:

- MySQL/Spark expansion.
- Full Track-A 120 expansion.
- Paper-facing metrics or retained-evidence promotion.
- Formal Regression@20 or Semantic Equivalence Rate claims.
