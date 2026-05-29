# Synthetic Preflight Request Plan

## Purpose

The first real-runtime request must use synthetic, non-benchmark SQL and schema only. It must not use Common-core case SQL, schemas, checker artifacts, retained evidence, or generated benchmark outputs.

## Synthetic SQL

```sql
SELECT a FROM synthetic_table WHERE a > 10;
```

## Synthetic Schema

```json
{
  "tables": [
    {
      "name": "synthetic_table",
      "columns": [
        {"name": "a", "type": "INTEGER"},
        {"name": "b", "type": "INTEGER"}
      ],
      "row_count": 10
    }
  ]
}
```

## Intended HTTP Request Shape

```json
{
  "sql": "SELECT a FROM synthetic_table WHERE a > 10;",
  "schema": {
    "tables": [
      {
        "name": "synthetic_table",
        "columns": [
          {"name": "a", "type": "INTEGER"},
          {"name": "b", "type": "INTEGER"}
        ],
        "row_count": 10
      }
    ]
  }
}
```

## Expected Response Shape

Preferred response:

```json
{
  "rewritten_sql": "SELECT a FROM synthetic_table WHERE a > 10"
}
```

Acceptable equivalents only after explicit wrapper support:

- `candidate_sql`
- `sql`

## Extraction Expectations

The response is acceptable only if one complete SQL statement is extractable and the statement starts with `SELECT` or `WITH`. Empty output, prose-only output, multiple statements, malformed JSON, stack traces, or unsupported status must fail closed.

## Current Status

This plan was not executed because no external LearnedRewrite command or URL is configured in the current shell environment.
