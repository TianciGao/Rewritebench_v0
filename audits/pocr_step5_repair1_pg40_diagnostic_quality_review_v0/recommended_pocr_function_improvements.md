# Recommended POCR Function Improvements

- Add provider JSON robustness improvements: stricter response-format enforcement, smaller prompt sections when needed, and explicit one-object output reminders near the end of the prompt.
- Add targeted retry policy for `malformed_json` and `timeout` rows only, gated by an explicit retry flag and preserving original fail-closed rows in the manifest.
- Improve prompt length and prompt format monitoring, especially for PERF and LONGTAIL rows where the 5 invalid/timeout rows concentrated.
- Add stricter evidence_ref validation before provider output is accepted as schema-valid, including unsupported prefix and empty-span checks.
- Surface Stage B strict-span rejection as a first-class review bucket so possible under-accept cases can be manually inspected.
- Add per-pool error monitoring for malformed/timeout concentration.
- Improve candidate_sha and route-binding UX by summarizing mismatches before replay starts.
- Add manual review hooks for all transformation-supported atoms and for implemented atoms rejected by Stage B.
- Keep annotation JSONL diagnostic-only unless a separate promotion task authorizes official POCR handling.
