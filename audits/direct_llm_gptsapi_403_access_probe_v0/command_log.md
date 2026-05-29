# Command Log

Environment presence check:

```bash
printf '<presence-only checks for SQLRB_LLM_ALLOW_LIVE, API key, base URL, model>'
```

Sanitized result:

```text
SQLRB_LLM_ALLOW_LIVE_present=yes
SQLRB_LLM_ALLOW_LIVE_equals_1=yes
api_key_present=yes
base_url_present=yes
model_present=yes
```

Minimal provider probe:

```bash
python - <<'PY'
# Reads provider env, sends tiny POST /v1/chat/completions with
# User-Agent: SQL-RewriteBench/0.1, prints sanitized JSON only.
PY
```

Sanitized result:

```text
authorization_bearer: status_code=200, classification=success
x-api-key: status_code=200, classification=success
```

User-Agent comparison and model-list probe:

```bash
python - <<'PY'
# Sends one adapter-like POST without a custom User-Agent, then GET /v1/models
# with User-Agent: SQL-RewriteBench/0.1. Prints sanitized JSON only.
PY
```

Sanitized result:

```text
no_custom_user_agent_chat_probe: status_code=403, code_1010_detected=true
models_probe_with_user_agent: status_code=200, model_gpt_5_4_listed=true
```

One-row facade adapter smoke before fix:

```bash
env \
  SQLRB_LLM_ALLOW_LIVE=1 \
  SQLRB_LLM_PROVIDER=openai_compatible \
  SQLRB_LLM_BASE_URL=https://api.gptsapi.net/v1 \
  SQLRB_LLM_MODEL=gpt-5.4 \
  python -m cli.main user evaluate \
    --case-set common_core_v0 \
    --case-list /tmp/sqlrb_direct_llm_gptsapi_403_access_probe_v0_case_list.txt \
    --engines postgres \
    --adapter-command "python baselines/direct_llm_original/adapter.py" \
    --output-root /tmp/sqlrb_direct_llm_gptsapi_403_access_probe_v0/output \
    --run-id direct_llm_gptsapi_403_access_probe_v0_adapter_one_row \
    --enable-db-execution \
    --enable-checker
```

Sanitized result:

```text
selected_rows=1
candidate_generated_rows=0
adapter_call_status=request_failed
adapter_failure_summary=HTTP 403: error code 1010
```

Validation after adapter header fix:

```bash
python -m pytest tests/user_entry/test_direct_llm_adapter.py
```

Result:

```text
9 passed
```

