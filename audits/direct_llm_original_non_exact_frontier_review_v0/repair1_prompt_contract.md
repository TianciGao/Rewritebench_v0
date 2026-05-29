# Repair-1 Prompt Contract

Prompt template id: `direct_llm_repair_1_feedback_sql_only_v0`

The prompt should provide:

- Target engine
- Schema context used by the original route
- Source SQL
- Original Direct LLM candidate SQL
- Original candidate id
- Feedback type
- Local execution/checker feedback summary
- Constraint that the answer must be one same-engine SQL query only

The model response must be accepted only when extraction finds exactly one SQL candidate and exactly one SQL statement. Markdown prose, multiple alternatives, explanatory text without a single SQL candidate, multiple SQL blocks, and empty responses must fail closed.

The prompt must not include API keys, environment variable values, raw provider headers, or raw provider response bodies.
