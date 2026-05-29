# Provider Policy GPT-5.4

Future live LLM-R2 adapted runs must follow the same Direct LLM provider
policy:

- provider: `openai_compatible`
- endpoint: GPTSAPI-compatible URL from environment variables
- model: `gpt-5.4`
- live gate: `SQLRB_LLM_ALLOW_LIVE=1`
- secrets: environment variables only
- raw API keys: never printed, written, staged, or committed

The route metadata must record:

- `adapted_gpt54_local_diagnostic=true`
- `original_paper_reproduction=false`
- `official_llm_r2_stack=false` unless a separate official-stack policy is
  authorized
- `local_diagnostic_only=true`

This route is adapted local diagnostic evidence, not an original-paper
reproduction and not a paper result.
