# Root Cause

PostgreSQL folds unquoted identifiers to lowercase. The Common-core PostgreSQL DDL for the affected rows declares identifiers such as `DEPT`, `EMP`, `Users`, `Posts`, and `Votes` without double quotes, so PostgreSQL loads them as lowercase names.

The external Calcite runtime emitted generated candidate SQL with quoted identifiers preserving the source/DDL spelling, for example:

```sql
FROM "DEPT"
```

PostgreSQL treats quoted identifiers as case-sensitive, so `"DEPT"` does not resolve to the loaded relation `dept`.

The safe repair point for generated candidates is after Calcite emits SQL and before candidate execution. The adapter already has the resolved PostgreSQL DDL path, so it can identify which quoted names are actually unquoted DDL identifiers and normalize only those names.

This is distinct from the PORT no-candidate rows, where the external runtime failed while parsing source SQL that contains double-quoted identifiers. Those rows require a separate parser/input-normalization or runtime-side task.
