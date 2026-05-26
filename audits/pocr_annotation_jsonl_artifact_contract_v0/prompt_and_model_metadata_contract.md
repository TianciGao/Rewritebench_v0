# Prompt And Model Metadata Contract

Annotation artifacts must record enough safe metadata to make route-bound replay auditable.

Required prompt metadata:

- `prompt_template_id`
- `prompt_template_version`
- `prompt_hash`
- `skills_contract_hash`
- input field names
- `system_message_hash`
- whether boundary instructions were present

Required provider/model metadata:

- `provider_label`
- `model_label`
- `call_timestamp_utc`
- decoding parameters such as temperature, max tokens, and response format
- token counts if available
- call status and safe error type if the call failed

Do not store API keys, bearer tokens, environment variable values, raw `.env` content, or local secrets in annotation JSONL, manifests, logs, or audit packets.

Safe raw prompt/response retention, if later authorized, must remain under explicitly scoped audit or output roots and must be redacted for secrets.
