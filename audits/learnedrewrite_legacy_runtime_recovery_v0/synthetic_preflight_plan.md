# Synthetic Preflight Plan

This plan defines one safe non-benchmark request. It was not executed in this task because no external LearnedRewrite runtime was configured and port 6336 was not listening.

## Request

Synthetic SQL:

```sql
SELECT COUNT(*) FROM tiny_orders WHERE amount > 10;
```

Synthetic schema JSON:

```json
[
  {
    "table": "tiny_orders",
    "rows": 3,
    "columns": [
      {"name": "order_id", "type": "integer"},
      {"name": "amount", "type": "numeric"}
    ]
  }
]
```

## Expected Runtime Response

Accepted response shapes:

- `{"data": {"rewritten_sql": "..."}, "status": true}`
- `{"rewritten_sql": "..."}`

The preferred official extraction path is `data.rewritten_sql` if present.

## Extraction Expectations

- exactly one complete SQL statement;
- no prose-only output;
- no empty output;
- no multiple SQL statements;
- safe code fence stripping only if needed;
- no local optimization or transpilation.

## Fail-Closed Conditions

- no configured `SQLRB_LEARNEDREWRITE_URL` or command;
- runtime unreachable;
- HTTP non-2xx response;
- malformed JSON;
- missing rewritten SQL field;
- empty SQL or prose-only response;
- multiple statements;
- unsupported status from runtime;
- response includes only stack trace or error payload.

## Boundary

No Common-core SQL may be used in the synthetic preflight.
