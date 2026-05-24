# Env Presence Review

Only presence/equality was checked. Secret values were not printed.

```text
SQLRB_LLM_ALLOW_LIVE_present=yes
SQLRB_LLM_ALLOW_LIVE_equals_1=yes
api_key_present=yes
base_url_present=yes
model_present=yes
```

The API key presence check accepted either `SQLRB_LLM_API_KEY` or `GPTSAPI_API_KEY`.
The base URL presence check accepted either `SQLRB_LLM_BASE_URL` or `GPTSAPI_BASE_URL`.
The model presence check accepted either `SQLRB_LLM_MODEL` or `GPTSAPI_MODEL`.

