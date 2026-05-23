# Normalized Verdict Review

Verifier verdict row:

```json
{
  "pair_id": "PERF_0062_source_vs_positive_pos_01",
  "tool": "verieql",
  "invocation_status": "timeout",
  "verdict": "timeout",
  "normalized_verdict": "timeout",
  "verdict_reason": "normalized_from_status:timeout",
  "timeout_seconds": 30
}
```

Normalization basis:

- Raw VeriEQL states: `["EQU", "TMO"]`.
- Raw error: `null`.
- The existing wrapper normalizes any row containing `TMO` to `timeout`.

Classification:

```text
timeout
```

This is not:

- `equivalent`
- `non_equivalent`
- `unknown`
- `unsupported`
- `tool_error`
- `not_attempted`

Consequence:

- The row is attempted but not decidable.
- `decidable_count=0`.
- The local semantic-equivalence summary remains N.A.
- No checker exactness was used as verifier evidence.
