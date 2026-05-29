# Optional Live Probe Plan

No live probe was required for this root-cause audit because the existing retry artifacts already identify the dominant failure mode: provider-call failure with HTTP 401 / insufficient balance.

If a future live probe is authorized after provider configuration is fixed, cap it at 3 calls:
- one previous provider-call-failed Repair-1 Spark row,
- one previous malformed Direct LLM original PostgreSQL row,
- one previous schema-valid control row.

Expected hypothesis: provider health restored should produce at least one response that reaches JSON/schema validation. If all three still fail provider-call status, stop before any batch retry.

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted. No bulk retry is run. POCR@planned and POCR@candidate remain D039 promotion views. POCR@curated remains deferred until a predeclared curated manifest exists.
