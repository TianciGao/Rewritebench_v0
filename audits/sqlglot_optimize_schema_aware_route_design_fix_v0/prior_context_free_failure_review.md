# Prior Context-Free Failure Review

Input audits reviewed:
- `audits/sqlglot_user_adapter_bounded_smoke_v0/`
- `audits/sqlglot_optimize_cons0005_triage_v0/`
- `audits/track_a_120_rerun_readiness_plan_v0/`

Prior verdict:
- `sqlglot_optimize` was classified as a `context_free_optimizer_qualification_gap`.

The context-free route parses source SQL by target dialect and calls `optimize(expression)` without schema or catalog context. On `CONS_0005`, SQLGlot produced an invalid subquery projection reference:
- PostgreSQL: `"table1"."table2"."i"`
- MySQL/Spark: `` `table1`.`table2`.`i` ``

The source SQL for `CONS_0005` is a correlated `NOT IN` over `table1` and `table2`. Source execution succeeded in prior bounded smoke, candidate preflight passed, but candidate execution failed across PostgreSQL, MySQL, and Spark because of the emitted invalid three-part reference.

Standalone reproduction confirmed:
- `parse_one` succeeds.
- No-op parse/emit does not create the invalid reference.
- Context-free optimize creates the invalid reference.
- Supplying a schema map prevents that invalid qualification, but changes route semantics and therefore needs a separate route id.
