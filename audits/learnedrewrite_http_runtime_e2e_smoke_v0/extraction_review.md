# Extraction Review

Runtime response:

- HTTP status: 200
- runtime status: `true`
- message: `SUCCESS`
- candidate field: `data.rewritten_sql`

Extracted candidate:

```sql
SELECT NAME AS NAME, COUNT(*) AS C FROM DEPT GROUP BY NAME HAVING NAME = 'Charlie';
```

Extraction status:

- `extracted`
- exactly one SQL statement
- source-like status: `source_like`
- fail-closed rows: 0

The runtime returned `is_rewritten=false`, so this smoke demonstrates runtime
and facade compatibility, not rewrite effectiveness.
