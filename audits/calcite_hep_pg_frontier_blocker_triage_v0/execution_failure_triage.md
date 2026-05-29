# Execution Failure Triage

Source execution failures: 2.

- `PORT_0013`: source failed in PostgreSQL; candidate origin was `calcite_parse_only_schema_fallback`.
- `PORT_0024`: source failed in PostgreSQL; candidate origin was `calcite_rel_to_sql`.

The execution/checker audit notes that both failed because PORT source SQL uses syntax that is not PostgreSQL-executable in this PostgreSQL-only pass.

Candidate execution failures: 8.

Identifier quoting failures:

- `CONS_0036`
- `CONS_0037`
- `LONGTAIL_0011`
- `LONGTAIL_0012`
- `LONGTAIL_0013`

The execution/checker audit notes that these failed due quoted mixed-case identifiers such as `DEPT`, `EMP`, `Posts`, or `Comments` not matching PostgreSQL-loaded relation names.

Schema-fallback candidate failures:

- `LONGTAIL_0022`
- `LONGTAIL_0023`
- `LONGTAIL_0024`

These rows reached source execution but candidate execution failed after a parse-only schema fallback caused by unsupported `timestamp` schema ingestion.

Recommended ordering:

1. Address identifier quoting for generated candidates.
2. Define PORT source-role policy for PostgreSQL-only runs.
3. Exclude schema-fallback candidates from execution by default until schema ingestion is hardened.
