# Prompt Template

Prompt template id:

```text
direct_llm_original_sql_only_v0
```

System contract:
- The model acts as a SQL rewrite engine for SQL-RewriteBench.
- It must return exactly one SQL query.
- It must return SQL only, with no markdown, explanation, or commentary.
- It must preserve source query semantics, result columns, result labels, and row multiplicity.
- It must use only tables and columns present in the provided schema.
- It must not emit DDL, DML, temp tables, indexes, stored procedures, UDFs, or multiple statements.
- If no safe rewrite is possible, it must return the original SQL unchanged.

User payload fields:
- `case_id`
- `pool`
- `target dialect`
- `model_id`
- schema / DDL context
- source SQL

Target dialect values:
- `postgres`
- `mysql`
- `spark`

Schema context:
- The adapter first checks case-local DDL paths.
- It also resolves current external schema profiles referenced by case metadata.
- If no schema can be resolved, the prompt marks schema as unavailable and the status metadata records `schema_context_status = unavailable`.

Boundary:
- Direct LLM original does not consume execution feedback.
- Direct LLM original does not repair output.
- Repair-1 requires a separate route and separate authorization.
