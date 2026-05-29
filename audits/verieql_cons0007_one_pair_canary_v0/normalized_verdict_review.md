# Normalized Verdict Review

Verifier verdict row:

```json
{
  "pair_id": "CONS_0007_source_vs_positive_pos_01",
  "tool": "verieql",
  "invocation_status": "unsupported",
  "verdict": "unsupported",
  "normalized_verdict": "unsupported",
  "verdict_reason": "normalized_from_status:unsupported",
  "timeout_seconds": 30
}
```

Normalization basis:

- Raw VeriEQL state: `NSE`.
- Raw VeriEQL error: `Not supported feature: EXISTS`.
- Existing wrapper normalization maps `NSE` / unsupported-feature output to the shared `unsupported` verdict.

Classification:

```text
unsupported
```

This is not:

- `equivalent`
- `non_equivalent`
- `unknown`
- `timeout`
- `tool_error`
- `not_attempted`

Boundary:

- The output is local verifier-support evidence only.
- It does not establish an official Semantic Equivalence Rate.
- It does not modify benchmark correctness, denominator, paper result, or retained-evidence state.
