# Live Env Review

Presence/equality only; API key values were not printed.

```text
SQLRB_LLM_ALLOW_LIVE_present=yes
SQLRB_LLM_ALLOW_LIVE_equals_1=yes
SQLRB_LLM_PROVIDER_present=yes
SQLRB_LLM_PROVIDER_expected=yes
SQLRB_LLM_BASE_URL_present=yes
SQLRB_LLM_BASE_URL_expected=yes
SQLRB_LLM_MODEL_present=yes
SQLRB_LLM_MODEL_expected=yes
api_key_present=yes
SQLRB_LLM_TEMPERATURE_present=yes
SQLRB_LLM_TEMPERATURE_expected=yes
SQLRB_LLM_TOP_P_present=yes
SQLRB_LLM_TOP_P_expected=yes
SQLRB_LLM_TIMEOUT_present=yes
SQLRB_LLM_TIMEOUT_expected=yes
```

Provider health check:

```text
POST /v1/chat/completions
status_code=200
classification=success
code_1010_detected=false
choices_present=true
```

Local engine preflight:

```text
PostgreSQL: available; probe ok.
MySQL: available; probe ok.
Spark: PySpark available; live local diagnostic backend available.
```
