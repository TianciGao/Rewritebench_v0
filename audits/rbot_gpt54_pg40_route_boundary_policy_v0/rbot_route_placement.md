# R-Bot Route Placement

Recommended public v0 placement: PostgreSQL-only adapted GPT-5.4 bounded prior-method evidence / appendix diagnostic.

Rationale:

- The route is `rbot_gpt54_adapted`, not original R-Bot / LLM4Rewrite paper reproduction.
- It uses the shared OpenAI-compatible / GPTSAPI-compatible `gpt-5.4` provider policy.
- It does not use the official R-Bot runtime, RAG retrieval, Chroma index, or CalciteRewrite substrate.
- The canonical evidence is PostgreSQL-only PG40 local diagnostic output from `local_metrics.py`.
- MySQL and Spark remain unassessed for this adapted route.
- Track A same-engine canonical local diagnostics require a 120-row tri-engine denominator policy and row visibility across PostgreSQL, MySQL, and Spark.

The R-Bot adapted PG40 result should be reported as bounded prior-method appendix evidence, not mixed into the current tri-engine Track A 120 canonical local metrics table and not used for a global leaderboard comparison.

If R-Bot is revisited later, the next R-Bot-specific step must be a separate engine-support or Track A support-assessment authorization that defines MySQL/Spark handling, unsupported-row policy, route denominator policy, and whether the adapted GPT-5.4 route remains distinct from original R-Bot reproduction.
