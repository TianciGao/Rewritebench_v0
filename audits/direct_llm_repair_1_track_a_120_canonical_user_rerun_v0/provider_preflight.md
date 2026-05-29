# Provider Preflight

Live environment review was presence-only and did not print secret values.

- `SQLRB_LLM_ALLOW_LIVE=1`: present.
- `SQLRB_LLM_PROVIDER`: present and matched `openai_compatible`.
- Base URL env: present.
- Model env: present and matched `gpt-5.4`.
- API key env: present.
- Temperature/top_p/timeout: existing environment matched the prior Repair-1 live-smoke defaults (`0`, `1`, `60`) or adapter defaults.
- Safe provider health check: `GET /v1/models` returned HTTP 200 and listed the configured model.
- Secret values printed/written/staged/committed: no.
