# Live Environment Review

Required live variables:
- `SQLRB_LLM_ALLOW_LIVE=1`
- `SQLRB_LLM_PROVIDER=openai_compatible`
- `SQLRB_LLM_BASE_URL=https://api.gptsapi.net/v1`
- `SQLRB_LLM_MODEL=gpt-5.4`
- `SQLRB_LLM_API_KEY=<secret>`

Preflight environment status in this shell:
- `SQLRB_LLM_ALLOW_LIVE`: missing.
- `SQLRB_LLM_PROVIDER`: missing.
- `SQLRB_LLM_BASE_URL`: missing.
- `SQLRB_LLM_MODEL`: missing.
- `SQLRB_LLM_API_KEY`: missing.
- `GPTSAPI_API_KEY`: missing.
- `GPTSAPI_BASE_URL`: missing.
- `GPTSAPI_MODEL`: missing.

Live provider enabled:
- No.

Live call made:
- No.

Gate-smoke environment:
- The no-secret user-facade gate smoke explicitly set:
  - `SQLRB_LLM_PROVIDER=openai_compatible`
  - `SQLRB_LLM_BASE_URL=https://api.gptsapi.net/v1`
  - `SQLRB_LLM_MODEL=gpt-5.4`
- It explicitly removed API key variables and did not set `SQLRB_LLM_ALLOW_LIVE`.
- The adapter failed closed before any network request with `missing_api_key`.

Secret handling:
- No API key value was printed.
- No API key value was written to adapter metadata.
- No env file was used or committed.
