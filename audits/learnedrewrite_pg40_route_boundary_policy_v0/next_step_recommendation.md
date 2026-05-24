# Next Step Recommendation

Recommendation: stop LearnedRewrite at PG40 bounded evidence for now.

Do not expand LearnedRewrite beyond PostgreSQL Common-core 40 unless a separate failure-triage or engine-support task is authorized.

Preferred next work:

- Move to R-Bot / LLM-R2 wrapper planning under the GPTSAPI/OpenAI-compatible `gpt-5.4` adapted-local-diagnostic policy already recorded in prior onboarding/design packets.
- Start with planning or fake adapter scaffolds, not live method execution.
- Preserve the same boundaries used for Direct LLM adapted local diagnostics: env-only secrets, no raw API keys, explicit live gate, and adapted-local-diagnostic wording.

If LearnedRewrite is revisited later, the next LearnedRewrite-specific task should be one of:

- runtime/schema failure triage for the 11 fail-closed/no-candidate PG40 rows;
- generated-SQL execution triage for the 6 candidate-execution-failed rows;
- a PostgreSQL-only appendix reporting policy; or
- a separate engine-support design for MySQL/Spark.

Do not run full Track A 120 without a route policy.
