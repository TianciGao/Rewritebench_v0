# Extraction Policy

Policy id: `single_select_or_with_sql_rbot_gpt54_v0`

## Accepted

- Exactly one raw SQL statement beginning with `SELECT` or `WITH`.
- Exactly one safe SQL code fence containing one `SELECT` or `WITH` statement.
- One optional terminal semicolon.

## Rejected

- Empty output.
- Prose-only output.
- Multiple SQL statements.
- Multiple SQL code fences.
- Ambiguous markdown or non-SQL code fences.

## Non-Rewrite Boundary

The adapter preserves SQL content after extraction. It does not optimize, transpile, normalize semantics, or apply local rewrite rules.
