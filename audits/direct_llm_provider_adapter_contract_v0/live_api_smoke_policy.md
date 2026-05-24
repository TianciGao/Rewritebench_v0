# Live API Smoke Policy

Default behavior:
- The adapter does not call a live provider unless `SQLRB_LLM_ALLOW_LIVE=1`.

Required live environment:
- `SQLRB_LLM_PROVIDER=openai_compatible`
- `SQLRB_LLM_BASE_URL=https://api.gptsapi.net/v1`
- `SQLRB_LLM_API_KEY=<secret>`
- `SQLRB_LLM_MODEL=gpt-5.4`
- `SQLRB_LLM_ALLOW_LIVE=1`

Optional GPTSAPI aliases:
- `GPTSAPI_API_KEY`
- `GPTSAPI_BASE_URL`
- `GPTSAPI_MODEL`

Policy:
- Live smoke should remain tiny and local diagnostic only.
- Runtime output must go under `/tmp/...` unless separately authorized.
- Raw provider response saving is opt-in through `SQLRB_LLM_SAVE_RAW_RESPONSE=1`; fake provider saves raw response for test traceability.
- API keys and other secrets must never be committed or written to status metadata.

This task:
- No live API call was made.
- Fake provider was used for smoke validation.
