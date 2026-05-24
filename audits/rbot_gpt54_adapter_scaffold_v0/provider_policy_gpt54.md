# Provider Policy GPT-5.4

Future live R-Bot-adapted calls must use the Direct LLM provider policy:

- provider: `openai_compatible`
- base URL: `SQLRB_LLM_BASE_URL` or GPTSAPI-compatible alias
- model: `gpt-5.4`
- live gate: `SQLRB_LLM_ALLOW_LIVE=1`
- API keys: environment variables only
- no API key values printed, written, staged, or committed

Metadata must record:

- `adapted_gpt54_local_diagnostic=true`
- `original_paper_reproduction=false`
- `original_rbot_official_stack=false`
- `official_rbot_stack=false`

This adapted route is not an exact original-paper reproduction. It must not be mixed with old retained evidence or paper claims without a separate promotion policy.
