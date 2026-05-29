# verieql_one_baseline_feature_aware_subset_plan_v0

Task mode: planning/audit only.

This packet defines a feature-aware, bounded one-baseline VeriEQL exact-candidate subset plan for SQLGlot noop on PostgreSQL, using the existing local diagnostic run `runs/user/common_core_pg_noop_db_checker`.

Scope:
- Baseline route/method: SQLGlot noop.
- Engine: PostgreSQL.
- Source run: `runs/user/common_core_pg_noop_db_checker`.
- Candidate row population: exact/result-consistent rows only.
- Verifier tool: VeriEQL, finite-bound mode planned.

No VeriEQL pass was run in this task. No official Semantic Equivalence Rate, official metrics, top-level `reports/`/`results`, retained evidence, leaderboard, denominator, case membership, or paper result changed.

Key result:
- Selected rows in source run: 40.
- Exact/result-consistent rows: 35.
- Non-exact rows: 5, all source-execution failures and verifier-ineligible.
- Currently proven verifier-eligible exact rows: 1, `CONS_0036`.
- First expansion candidate after DDL parser hardening: `CONS_0037`.
- Main blockers: subquery/EXISTS/set-operation shapes, date/time/function-heavy SQL, `LIKE`, dialect quoting/LIMIT/NULLS syntax, and parameterized DDL parser rough edges.

Recommended next safe action:
- Harden the DDL parser for parameterized types, then run a bounded two-row VeriEQL exact-candidate pass over `CONS_0036` and `CONS_0037` only.

