# Extraction Policy

Policy id:

```text
single_sql_candidate_learnedrewrite_v0
```

## Accepted Forms

The adapter accepts exactly one SQL statement that starts with `SELECT` or `WITH`.

Accepted examples:

- plain SQL text;
- one fenced SQL block with language `sql`;
- one fenced SQL block without a language tag;
- SQL with one optional terminal semicolon.

The adapter normalizes successful output to a single terminal semicolon and newline.

## Rejected Forms

The adapter rejects:

- empty responses;
- prose-only responses;
- prose-prefixed SQL outside a safe code fence;
- multiple fenced SQL blocks;
- multiple SQL statements;
- JSON responses missing a string SQL field;
- unsupported or failed fake runtime statuses.

## No Local SQL Rewriting

The adapter does not optimize, transpile, repair, normalize dialect, rewrite semantics, or alter the candidate beyond safe terminal-semicolon formatting.

## Fail-Closed Boundary

Extraction failures leave `SQLRB_CANDIDATE_SQL_PATH` absent. They are denominator-visible no-candidate outcomes if later run through the user facade.
