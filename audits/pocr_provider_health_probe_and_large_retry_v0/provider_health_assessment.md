# Provider Health Assessment

Verdict: provider_healthy.

The 401 / insufficient-balance / unauthorized failure class disappeared in the 3-row probe. Probe rows produced 2 schema-valid rows and 1 malformed-json row. That satisfies the task gate because at least one probe row was schema-valid and no provider_config_issue recurred.

Batch 1 was authorized by the probe result. Batch 1 produced 87 schema-valid rows out of 100 live calls. Provider-call failures in batch 1 were HTTP 504/520 transient/provider-edge responses, not HTTP 401/insufficient-balance.

Remaining issue class: prompt/schema/model-output stability for malformed rows plus transient HTTP 504/520 provider errors on some rows. Confidence: high that the previous provider_config_issue is resolved; medium that remaining failures require bounded retry plus optional JSON-output hardening rather than account/config repair.

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted. No blind full retry is run. POCR@planned and POCR@candidate remain D039 promotion views. POCR@curated remains deferred until a predeclared curated manifest exists. Track A 120 is not a leaderboard.
