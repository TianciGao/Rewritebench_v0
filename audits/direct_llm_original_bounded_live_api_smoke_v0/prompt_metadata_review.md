# Prompt Metadata Review

Prompt rendering:
- The adapter rendered `direct_llm_prompt.json` for all 6 selected rows in ignored `runs/user` staging.
- Prompt bodies were not committed.

Metadata observed in `direct_llm_status.json` for each selected row:
- `provider = openai_compatible`
- `base_url_host = api.gptsapi.net`
- `model_id = gpt-5.4`
- `temperature = 0.0`
- `top_p = 1.0`
- `max_tokens = 2048`
- `timeout_seconds = 60.0`
- `prompt_template_id = direct_llm_original_sql_only_v0`
- `extraction_policy = single_sql_candidate_v0`
- `schema_context_status = available`
- `local_only = true`
- `official_metric_input = false`
- `paper_result = false`

Live-call metadata:
- `call_attempted = false`
- `call_status = not_attempted`
- `request_timestamp` is empty because no provider request was made.
- `raw_response_saved = false`

Requirement gap:
- The task intended to validate live request metadata. That could not be satisfied without the live API key and live-call gate.
