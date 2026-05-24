# Schema Context Design

Schema source:
- The adapter uses `SQLRB_CASE_DIR`, `SQLRB_ENGINE`, and case metadata to resolve per-engine DDL.
- Resolution checks case-local compatibility DDL paths and external schema profiles referenced from `schema/schema_profile.yaml` and `manifest.yaml`.
- Supported engine keys are PostgreSQL, MySQL, and Spark.

Schema parser:
- Reads simple `CREATE TABLE ... (...)` statements.
- Extracts table names, column names, and column type text.
- Skips table constraints such as `PRIMARY`, `FOREIGN`, `UNIQUE`, `CHECK`, and `CONSTRAINT`.
- Handles Spark `USING parquet` suffixes in the current schema assets.

SQLGlot optimizer call:

```python
optimize(expression, schema=schema_context, dialect=dialect)
```

Fail-closed buckets:
- `schema_context_unavailable`
- `sqlglot_schema_parse_failed`
- `sqlglot_optimize_failed`
- `candidate_generation_failed`

Traceability:
- The adapter writes `sqlglot_status.json` into the supplied workspace.
- Status metadata includes route id, method id, engine, dialect, source SQL path, case dir, candidate SQL path, schema DDL path, schema context tables, and local-only/paper-boundary flags.
