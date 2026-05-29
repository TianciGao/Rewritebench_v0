# Provider Contract

Route:
- `route_id = direct_llm_original`
- `method_id = direct_llm_original`

Provider mode:
- `SQLRB_LLM_PROVIDER=openai_compatible`
- `SQLRB_LLM_PROVIDER=fake` for offline smoke tests.

Default OpenAI-compatible endpoint:
- `SQLRB_LLM_BASE_URL=https://api.gptsapi.net/v1`
- Default model: `gpt-5.4`

Required live-call gate:
- `SQLRB_LLM_ALLOW_LIVE=1`

Environment variables:
- `SQLRB_LLM_PROVIDER`
- `SQLRB_LLM_BASE_URL`
- `SQLRB_LLM_API_KEY`
- `SQLRB_LLM_MODEL`
- `SQLRB_LLM_TEMPERATURE`
- `SQLRB_LLM_TOP_P`
- `SQLRB_LLM_MAX_TOKENS`
- `SQLRB_LLM_TIMEOUT`
- `SQLRB_LLM_AUTH_HEADER`
- `SQLRB_LLM_SAVE_RAW_RESPONSE`
- `SQLRB_LLM_ALLOW_LIVE`

GPTSAPI aliases:
- `GPTSAPI_API_KEY`
- `GPTSAPI_BASE_URL`
- `GPTSAPI_MODEL`

Authentication:
- Default: `Authorization: Bearer <key>`.
- Optional: `x-api-key` when `SQLRB_LLM_AUTH_HEADER=x-api-key`.

Default generation parameters:
- `temperature = 0`
- `top_p = 1`
- `max_tokens = 2048`
- `timeout = 60`

Fail-closed buckets:
- `missing_api_key`
- `live_api_disabled`
- `unsupported_provider`
- `request_failed`
- `response_empty`
- `response_not_sql`
- `multiple_sql_blocks_ambiguous`
- `multiple_sql_statements_ambiguous`

Secret handling:
- API key values are never written to adapter metadata.
- Status records only `api_key_present` and the environment variable name used.
- Status records `base_url_host`, not the full secret-bearing request.

Status metadata:
- provider
- `base_url_host`
- model id
- temperature
- top_p
- max_tokens
- timeout
- prompt template id
- extraction policy id
- request timestamp
- raw response saved flag/path
- candidate generation status
- failure bucket
- local-only and non-official boundary flags
