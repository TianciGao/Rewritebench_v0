# Repair-1 Prompt Contract

Prompt template id:

```text
direct_llm_repair_1_feedback_sql_only_v0
```

Required prompt inputs:

- target engine
- schema context when available
- source SQL
- original Direct LLM candidate SQL
- original candidate id
- original candidate SQL SHA256
- feedback type
- failure bucket
- source/candidate/checker status fields
- local execution/checker feedback summary

The prompt instructs the provider to return exactly one SQL query for the target
same-engine dialect and to return SQL only. It forbids DDL, DML, temp tables,
indexes, stored procedures, UDFs, and multiple statements.

The prompt must not include API keys, environment variable values, raw provider
headers, or secret-bearing metadata.

Accepted responses:

- exactly one `SELECT` or `WITH` statement
- optionally in exactly one SQL fenced code block

Rejected responses:

- empty response
- prose response
- multiple SQL blocks
- multiple SQL statements
- ambiguous extraction
