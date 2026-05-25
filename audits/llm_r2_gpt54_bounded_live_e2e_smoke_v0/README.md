# LLM-R2 GPT-5.4 Bounded Live E2E Smoke

This packet records a PostgreSQL-only 6-row live end-to-end user-facade smoke for the adapted LLM-R2 GPT-5.4 route. It is local diagnostic evidence only and is not an original LLM-R2 paper reproduction.

## Result

- Selected rows: 6
- Live calls attempted: 6
- Candidates generated: 6
- Candidate executable rows: 5
- Exact rows: 5
- Timed rows: 5
- Failures: 1

The smoke used `provider=openai_compatible` with model `gpt-5.4`, env-only secrets, and `SQLRB_LLM_ALLOW_LIVE=1`. It did not use the official LLM-R2 runtime, Java/rule-system execution, checkpoint inference, or demonstration selector.

Next safe action: authorize a PostgreSQL-only LLM-R2 adapted PG40 bounded diagnostic with DB/checker/timing and local_metrics. Do not run Track A 120 until PG40 and a route boundary policy are complete.
