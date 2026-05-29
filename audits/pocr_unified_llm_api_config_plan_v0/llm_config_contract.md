# LLM Config Contract

The project should converge on one user-facing LLM configuration model for Direct LLM baseline generation, Direct LLM Repair-1 / feedback routes, POCR Stage A annotation generation, and future LLM-backed diagnostics.

Conceptual future object:

```text
LLMClientConfig:
  provider_label
  base_url
  api_key_env
  model
  temperature
  max_tokens
  timeout_seconds
  response_format
  retry_policy
  prompt_template_id
  prompt_template_version
  live_enabled
  diagnostic_only
```

This contract is intentionally transport/configuration-only. It does not imply shared prompts, shared response schemas, shared route labels, shared denominators, shared evidence status, or metric promotion.

`live annotation must remain explicit and default-off`.

Annotation JSONL is diagnostic evidence only. Stage A annotation alone is not counted. No official POCR is computed. No paper-facing metric is promoted. No global leaderboard is produced.
