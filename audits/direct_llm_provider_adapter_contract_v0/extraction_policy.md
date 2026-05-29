# Extraction Policy

Extraction policy id:

```text
single_sql_candidate_v0
```

Accepted candidate forms:
- Exactly one fenced SQL block, with `sql` or empty fence language.
- A full response that looks like one `SELECT` or `WITH` SQL statement.

Rejected forms:
- Empty response.
- Non-SQL prose.
- Multiple SQL code blocks.
- Multiple SQL statements.
- DDL or DML shapes by start-token policy.

Normalization:
- The adapter strips one trailing semicolon and writes a single trailing semicolon plus newline.
- It does not repair SQL.
- It does not rewrite case SQL.
- It does not alter candidate semantics.

Fail-closed behavior:
- Extraction failures return exit code 0 without writing candidate SQL.
- The user runner records the row as denominator-visible no-candidate/fail-closed output rather than a runner crash.
