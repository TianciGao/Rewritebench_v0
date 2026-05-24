# Synthetic Preflight Review

Runtime mode: HTTP server from external JAR.

Port used: `6336`.

Temp workdir:

```text
/tmp/sqlrb_learnedrewrite_runtime_staging_v0/
```

Request:

- endpoint: `POST /rewriter`
- request count: exactly 1
- SQL: `SELECT order_id FROM tiny_orders WHERE amount > 10`
- schema: artificial `tiny_orders` schema with `order_id integer` and
  `amount numeric`
- Common-core SQL/schema: no

Result:

- curl exit code: 0
- HTTP status: 200
- elapsed seconds: 0.685
- response parseable JSON: yes
- response status: true
- response message: `SUCCESS`
- candidate field: `data.rewritten_sql`
- single SQL extractable: yes
- extracted SQL: `SELECT order_id FROM tiny_orders WHERE amount > 10`
- `is_rewritten`: false

This is only a runtime availability and response-contract preflight. It is not
benchmark evidence, not a correctness result, not a performance result, and not
a metric.

The runtime was shut down after the request.
