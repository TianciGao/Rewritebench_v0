# Documentation Change Summary

Changed file: `baselines/sqlglot/README.md`

Added section: `Known Context-free Optimize Limitation`

The new section documents:

- `--route noop` and `--route optimize` are separate user-entry adapter routes.
- Current `--route optimize` is context-free: it reads source SQL, parses using the selected dialect, calls SQLGlot `optimize(expression)` without case schema or catalog context, and emits candidate SQL.
- Context-free optimize may emit invalid qualification for some correlated subqueries.
- The observed bounded diagnostic example is `CONS_0005`.
- PostgreSQL emitted invalid reference: `"table1"."table2"."i"`.
- MySQL/Spark emitted invalid reference: `` `table1`.`table2`.`i` ``.
- The failure is fail-visible adapter behavior, not a database backend failure, checker failure, timing issue, official metric, or benchmark code failure.
- Bounded local diagnostic SQLGlot route results are not official retained baseline evidence.
- A future schema-aware SQLGlot route needs a separately named route and separate authorization.

No adapter behavior was changed. No schema-aware route was added. No SQLGlot behavior was patched. No broader SQLGlot diagnostic was run.
