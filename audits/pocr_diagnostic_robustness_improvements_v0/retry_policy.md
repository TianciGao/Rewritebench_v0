# Retry Policy

Default retry-eligible statuses are `malformed_json`, `timeout`, and `provider_call_failed`.

Retry is never automatic. A future retry must be explicit, bounded to selected rows, and must preserve the original fail-closed status in manifests. Successful JSONL rows must not be duplicated. Route, method, candidate, skills-contract, duplicate, missing-candidate, and unsupported-engine failures remain fail-closed until their binding or input problem is resolved.

This task only plans retries; it does not call a provider.
