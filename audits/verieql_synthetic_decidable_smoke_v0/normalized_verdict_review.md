# Normalized Verdict Review

Pair verdicts:

```text
synthetic_select1_equivalent: unsupported
synthetic_select1_nonequivalent: unsupported
```

Normalization basis:

- Raw state for both rows: `NSE`.
- Raw error for both rows: `Not supported feature: Query must have a FROM clause`.
- Existing wrapper normalization maps `NSE` / unsupported-feature output to the shared `unsupported` verdict.

Classification:

```text
unsupported_count=2
decidable_count=0
```

This smoke did not produce:

- `equivalent`
- `non_equivalent`
- `unknown`
- `timeout`
- `tool_error`
- `not_attempted`

Consequence:

- The staged tool can be invoked through the wrapper.
- `SELECT 1` without a `FROM` clause is not a viable decidability smoke for this VeriEQL tree.
- A future synthetic decidability smoke should use a minimal `FROM` clause plus schema context.
