# Model Access Review

Probe:

- Endpoint: OpenAI-compatible `GET /v1/models`
- Auth style: `Authorization: Bearer <redacted>`
- User-Agent: `SQL-RewriteBench/0.1`

Result:

```text
status_code=200
classification=success
response_allowed=true
model_count_seen=35
model_gpt_5_4_listed=true
code_1010_detected=false
```

Interpretation: model-list access is allowed for the current provider/account/key path when the explicit User-Agent is present, and `gpt-5.4` appears in the returned model list.

