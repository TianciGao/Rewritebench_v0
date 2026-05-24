# Adapter Engine Mode Review

The adapter can be invoked by `python -m cli.main user evaluate` for all three
target engines. It also resolves per-engine DDL paths through the existing
case-package metadata:

- PostgreSQL DDL: `<schema>/postgres/ddl.sql`
- MySQL DDL: `<schema>/mysql/ddl.sql`
- Spark DDL: `<schema>/spark/ddl.sql`

The external runtime command shape remains:

```text
calcite-hep-rewrite-smoke --case-id <case_id> --source-sql <source-sql> --ddl <schema-ddl> --output-sql <candidate-sql> --mode real_route_canary
```

There is no committed adapter contract for `--engine postgres|mysql|spark`.
The bounded pre-guard smoke showed that the runtime emits PostgreSQL-dialect
SQL for MySQL and Spark, including double-quoted identifiers. Those candidates
previously reached DB execution and failed with target parser errors.

Narrow fix applied in the adapter:

- PostgreSQL behavior remains unchanged, including the existing PostgreSQL-only
  unquoted/lowercase DDL identifier postprocess.
- MySQL and Spark now fail closed before DB execution when generated SQL
  contains known PostgreSQL-dialect forms for those targets:
  - double-quoted identifiers
  - `DOUBLE PRECISION`
- Unsupported generated SQL is retained in the local row workspace as
  `unsupported_candidate.sql`.
- `SQLRB_CANDIDATE_SQL_PATH` is left absent so user-run output records no
  executable candidate.
- Status metadata records `preflight_status =
  calcite_target_dialect_unsupported` and an explicit target-dialect guard
  bucket.

This is not a dialect rewrite. It is a fail-closed guard until the external
runtime supports target-dialect emission or a separately authorized adapter
contract is added.
