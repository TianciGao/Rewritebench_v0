# Root Cause Assessment

Verdict: `provider_config_issue`.

Confidence: high.

Evidence:
- The targeted retry attempted 150 live calls and produced 0 schema-valid rows.
- Retry safe JSONL errors and manifests show `provider_call_failed` / `RuntimeError` for all retry calls.
- Representative safe error excerpts include HTTP 401 with an insufficient-balance message.
- Earlier malformed JSON and timeout rows exist, but the retry phase did not reach JSON parsing or schema validation for any selected row.
- Prompt-size samples are not large enough to explain a uniform 150/150 provider-call failure pattern.

Secondary issues:
- `output_json_contract_issue` / `parser_extraction_issue` may explain older malformed JSON rows and should be tested later, but it is not the retry blocker.
- `schema_validator_issue` is not supported by the retry evidence.
- `model_capability_issue` remains possible for malformed rows after provider health is restored, but current evidence is provider/configuration first.

Blocker before next retry batch: yes.

Blocker before paper-promotion review: yes.

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted. No bulk retry is run. POCR@planned and POCR@candidate remain D039 promotion views. POCR@curated remains deferred until a predeclared curated manifest exists.
