# Recommended Fix Plan

Recommended minimal path:

1. Stop blind retry while provider calls return HTTP 401 / insufficient balance.
2. Add or run a provider health preflight before any annotation batch. It should verify only safe metadata and perform at most a tiny authorized probe, not a full annotation retry.
3. Fix provider account/configuration or switch to a known-good provider/model before retrying fail-closed rows.
4. After provider health is fixed, run a capped 3-row probe covering one prior malformed JSON row, one prior provider-call-failed row, and one schema-valid control row.
5. If the probe returns valid content but JSON formatting is still unstable, add narrow tests and a safe extractor improvement for fenced/prose-wrapped single JSON objects. Keep truncated/partial JSON fail-closed.
6. Only then run the next bounded retry batch.

No broad behavior change is implemented in this task because the dominant blocker is provider configuration, not local parser/schema behavior.

Further blind retry is not recommended.

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted. No bulk retry is run. POCR@planned and POCR@candidate remain D039 promotion views. POCR@curated remains deferred until a predeclared curated manifest exists.
