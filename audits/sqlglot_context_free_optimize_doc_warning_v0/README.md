# SQLGlot Context-free Optimize Documentation Warning

Verdict: `completed`

This audit documents the known context-free SQLGlot `--route optimize` limitation found in `sqlglot_optimize_cons0005_triage_v0`. The only repository documentation change is a warning section in `baselines/sqlglot/README.md`.

The warning states that `--route noop` and `--route optimize` are separate user-entry adapter routes, that the current optimize route calls SQLGlot `optimize(expression)` without case schema or catalog context, and that this context-free mode can emit invalid qualification for correlated subqueries. The bounded diagnostic example is `CONS_0005`, where SQLGlot emitted invalid three-part references: PostgreSQL `"table1"."table2"."i"` and MySQL/Spark `` `table1`.`table2`.`i` ``.

This is fail-visible adapter behavior. It is not a database backend failure, checker failure, timing issue, official metric, or benchmark code failure.

No adapter behavior changed. No schema-aware route was added. No broader SQLGlot trial was run.

## Project-control Metadata Note

Preflight found that project control already contained the `sqlglot_optimize_cons0005_triage_v0` status and run-log entries. Those entries did not explicitly record the final triage commit/push metadata. This task records the prior triage final commit `98b4e9e` and push result `pushed to origin/feature/case-package-v2-external-schema` as a non-destructive metadata note in the new project-control writeback.

## Boundary

This packet is documentation/audit only. It does not compute official metrics, timing, speedup, paper results, reports/results tables, retained-evidence promotion, or leaderboard outputs. It does not change denominators, paper results, case membership, raw retained evidence, adapter behavior, or SQLGlot route semantics.

## Next Safe Action

Keep the current context-free optimize route fail-visible. Any schema-aware SQLGlot route should be separately named and separately authorized because it changes route semantics and comparability.
