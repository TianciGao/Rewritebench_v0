# Metadata Review

All six selected row workspaces wrote `rbot_status.json` with the adapted-route boundary fields.

Confirmed metadata fields:
- `route_id=rbot_gpt54_adapted`
- `method_id=rbot`
- `provider=openai_compatible`
- `model=gpt-5.4`
- `adapted_gpt54_local_diagnostic=true`
- `original_paper_reproduction=false`
- `original_rbot_official_stack=false`
- `official_rbot_stack=false`
- `live_call=true`
- `fake_runtime=false`
- `retrieval_used=false`
- `rag_index_used=false`
- `calcite_rewrite_used=false`
- `local_diagnostic_only=true`
- `raw_response_saved=false`
- `no_secret_values=true`

Each selected row recorded `runtime_status=live_provider_success`, `provider_status=live_provider_success`, and `extraction_status=extracted`.

No API key value or secret value was present in the status metadata. Provider configuration metadata records only safe facts such as provider name, base URL host, model ID, API-key presence, environment variable name, timeout, temperature, top-p, max token setting, and auth-header mode.
