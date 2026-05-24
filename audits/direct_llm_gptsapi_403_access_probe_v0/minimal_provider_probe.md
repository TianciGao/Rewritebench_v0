# Minimal Provider Probe

Probe:

- Endpoint: OpenAI-compatible `POST /v1/chat/completions`
- Model: `gpt-5.4`
- Prompt: `Return SELECT 1;`
- `temperature`: `0`
- `max_tokens`: `32`
- User-Agent: `SQL-RewriteBench/0.1`

Results:

```text
authorization_bearer: HTTP 200, choices_present=true, code_1010_detected=false
x-api-key: HTTP 200, choices_present=true, code_1010_detected=false
```

Classification: provider minimal chat-completions access succeeds with the explicit User-Agent.

