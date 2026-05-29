# Next Step Recommendation

Recommendation: stop R-Bot at PostgreSQL-only bounded evidence for now.

The PG40 result is useful and should be retained as adapted prior-method appendix diagnostic evidence, but it does not justify Track A 120 expansion without a separate support-assessment task.

Next implementation direction:

- Move to LLM-R2 GPT-5.4 adapted fake/no-live adapter scaffold.
- Keep the same Direct LLM provider policy for future LLM-dependent adapted prior-method routes: OpenAI-compatible / GPTSAPI-compatible, model `gpt-5.4`, live gate `SQLRB_LLM_ALLOW_LIVE=1`, env-only secrets, and no raw API keys printed/written/staged/committed.
- Return to R-Bot only if a separate engine-support or Track A support-assessment task is authorized.

If R-Bot is reopened, the task must define MySQL/Spark support, unsupported-row handling, denominator visibility, and whether the adapted GPT-5.4 route remains a local diagnostic appendix route rather than original-paper reproduction.
