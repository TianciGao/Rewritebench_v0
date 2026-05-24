# R-Bot GPT-5.4 Adapted Wrapper

This baseline directory contains a local diagnostic scaffold for an adapted
R-Bot route:

- `route_id`: `rbot_gpt54_adapted`
- `method_id`: `rbot`
- provider policy for future live calls: OpenAI-compatible / GPTSAPI-compatible
- model policy for future live calls: `gpt-5.4`

This is not an original R-Bot paper reproduction and does not use the official
LLM4Rewrite stack. The current adapter implements fake fixture mode only.

## Fake Mode

Use fake mode with one of:

```bash
SQLRB_RBOT_MODE=fake
SQLRB_RBOT_FAKE_SQL="SELECT ..."
```

or:

```bash
SQLRB_RBOT_MODE=fake
SQLRB_RBOT_FAKE_RESPONSE='{"status":"ok","candidate_sql":"SELECT ..."}'
```

The adapter writes exactly one candidate SQL statement to
`SQLRB_CANDIDATE_SQL_PATH` only when extraction succeeds. It writes
`rbot_status.json` in `SQLRB_WORKSPACE_DIR` for both success and fail-closed
paths.

## Future Live Mode Boundary

Future live R-Bot-adapted work must use the same provider policy as Direct LLM:

- `SQLRB_LLM_PROVIDER=openai_compatible`
- `SQLRB_LLM_BASE_URL` or `GPTSAPI_BASE_URL`
- `SQLRB_LLM_MODEL=gpt-5.4` or `GPTSAPI_MODEL=gpt-5.4`
- `SQLRB_LLM_ALLOW_LIVE=1`
- API keys through environment variables only

Live API calls, RAG retrieval, Chroma index use, CalciteRewrite invocation, DB
execution, checker execution, timing, local metrics, official metrics, paper
rendering, and retained-evidence promotion are not part of this scaffold.

## Metadata Boundary

Every status file records:

- `adapted_gpt54_local_diagnostic=true`
- `original_paper_reproduction=false`
- `original_rbot_official_stack=false`
- `official_rbot_stack=false`
- `local_diagnostic_only=true`
- no secret values

Old R-Bot retained artifacts and legacy logs may guide future wrapper design,
but must not be imported as new canonical metrics.
