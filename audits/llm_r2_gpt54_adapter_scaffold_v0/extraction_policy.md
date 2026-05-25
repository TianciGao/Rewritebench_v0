# Extraction Policy

The scaffold uses a single-SQL extraction policy:

- accept exactly one `SELECT` or `WITH` statement;
- accept one safe SQL code fence when it contains exactly one statement;
- accept a labeled `SQL:` / `candidate_sql:` / `rewritten_sql:` section when
  rule-sequence text is present and the SQL is unambiguous;
- preserve SQL content except for normalizing one trailing semicolon.

Rejected forms:

- empty output;
- prose-only output;
- markdown with no SQL block;
- multiple SQL code blocks;
- multiple SQL statements;
- rule-only response with no candidate SQL;
- ambiguous labeled sections.

The adapter does not optimize, transpile, execute, or repair SQL locally.
