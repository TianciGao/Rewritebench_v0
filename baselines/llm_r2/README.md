# LLM-R2 GPT-5.4 Adapted Wrapper

This baseline directory contains a local diagnostic scaffold for an adapted
LLM-R2 route:

- `route_id`: `llm_r2_gpt54_adapted`
- `method_id`: `llm_r2`
- future provider policy: OpenAI-compatible / GPTSAPI-compatible
- future model policy: `gpt-5.4`

This is not an original LLM-R2 paper reproduction and does not use the
official LLM-R2 runtime, Java rule system, SimCSE checkpoint, demonstration
selector, or retained legacy outputs. The current scaffold supports fake
fixture mode only.

## Fake Mode

Use fake mode with one of:

```bash
SQLRB_LLM_R2_MODE=fake
SQLRB_LLM_R2_FAKE_SQL="SELECT ..."
```

or:

```bash
SQLRB_LLM_R2_MODE=fake
SQLRB_LLM_R2_FAKE_RESPONSE='{"status":"ok","candidate_sql":"SELECT ...","rule_sequence":["FilterMerge"]}'
```

The adapter writes exactly one candidate SQL statement to
`SQLRB_CANDIDATE_SQL_PATH` only when extraction succeeds. It writes
`llm_r2_status.json` in `SQLRB_WORKSPACE_DIR` for both success and fail-closed
paths.

## Future Live Boundary

Future live LLM-R2-adapted work must use the same provider policy as Direct
LLM:

- `SQLRB_LLM_PROVIDER=openai_compatible`
- `SQLRB_LLM_BASE_URL` or `GPTSAPI_BASE_URL`
- `SQLRB_LLM_MODEL=gpt-5.4` or `GPTSAPI_MODEL=gpt-5.4`
- `SQLRB_LLM_ALLOW_LIVE=1`
- API keys through environment variables only

`SQLRB_LLM_R2_MODE=live` is intentionally fail-closed in this scaffold. It
checks the live gate and provider configuration but does not call a provider.

Future official-stack work would also need separately authorized rule-system,
checkpoint, and demonstration-selector configuration:

- `SQLRB_LLM_R2_RULE_SYSTEM_CMD`
- `SQLRB_LLM_R2_CHECKPOINT_PATH`
- `SQLRB_LLM_R2_DEMO_SELECTOR_PATH`

## Metadata Boundary

Every status file records:

- `adapted_gpt54_local_diagnostic=true`
- `original_paper_reproduction=false`
- `official_llm_r2_stack=false`
- `local_diagnostic_only=true`
- `rule_system_runtime_used=false` in fake mode
- `checkpoint_used=false` in fake mode
- no secret values

Old LLM-R2 retained artifacts and legacy logs may guide future wrapper design,
but must not be imported as new canonical metrics.
