# Schema JSON Mapping Plan

## Release Inputs

Future LearnedRewrite real-runtime use should derive schema JSON from release case package metadata, not from old upstream examples.

Likely inputs:

- `SQLRB_CASE_DIR` from the D035 row environment.
- Engine-specific DDL paths under each case directory.
- `schema_ref` or equivalent resolver metadata from the user facade.
- Optional future external schema profile metadata if exposed by the facade.

## Target LearnedRewrite Schema Shape

The official source example uses an array of table objects:

```json
[
  {
    "table": "table_name",
    "rows": 1000,
    "columns": [
      {"name": "column_name", "type": "integer"}
    ]
  }
]
```

Future mapping should produce the minimal compatible shape:

- `table`: unquoted logical table name.
- `rows`: conservative placeholder or known row-count metadata if available.
- `columns`: ordered list of column names and normalized types.

## Type Mapping Risks

PostgreSQL DDL needs conservative mapping before runtime use:

- `BIGINT`, `INTEGER`, `SMALLINT`
- `NUMERIC(p,s)` and `DECIMAL(p,s)`
- `DOUBLE PRECISION`
- `TEXT`, `VARCHAR(n)`, `CHAR(n)`
- `DATE`, `TIMESTAMP`
- boolean types and engine-specific aliases

Unsupported or ambiguous types should fail closed as `schema_serialization_failed` or `unsupported_type`, not be silently coerced.

## Dialect Risks

- PostgreSQL is the only safe first smoke target because legacy evidence is PG-only and LearnedRewrite is Calcite-centered.
- MySQL and Spark support are not recovered and should remain unsupported until separate dialect preflights pass.
- Quoted identifiers, case folding, date/interval syntax, window functions, CTEs, and engine-specific functions need explicit guard coverage.

## Initial Smoke Recommendation

Before any Common-core case is sent to the runtime:

1. Implement schema JSON serialization tests using synthetic DDL only.
2. Run one synthetic non-benchmark runtime preflight against a configured external endpoint.
3. Run a 1-2 row PostgreSQL-only D035 user-facade smoke without DB/checker/timing only after synthetic preflight succeeds.

Track A 120 is not ready.
