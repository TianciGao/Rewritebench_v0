# User-Agent Probe

Positive probe:

```text
POST /v1/chat/completions
auth_style=authorization_bearer
user_agent=SQL-RewriteBench/0.1
status_code=200
classification=success
code_1010_detected=false
```

Adapter-like comparison without a custom User-Agent:

```text
POST /v1/chat/completions
auth_style=authorization_bearer
custom_user_agent=false
status_code=403
classification=provider_auth_or_access_denied
code_1010_detected=true
error_summary=HTTP 403: error code 1010
```

Interpretation: the provider-side denial is triggered by the adapter-like request headers. Adding the explicit SQL-RewriteBench User-Agent resolves the minimal provider probe.

