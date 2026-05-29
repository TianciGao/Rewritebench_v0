# Normalized Verdict Review

Pair verdicts:

```text
synthetic_from_equivalent: timeout
synthetic_from_nonequivalent: non_equivalent
```

Normalization basis:

- `synthetic_from_equivalent` raw states contained many `EQU` states and a final `TMO`; the wrapper normalizes any row containing `TMO` to `timeout`.
- `synthetic_from_nonequivalent` raw state was `NEQ` with `Symbolic reasoning: NOT EQUIVALENT.`; the wrapper normalized the row to `non_equivalent`.

Classification:

```text
timeout_count=1
non_equivalent_count=1
decidable_count=1
```

This smoke did not produce:

- `equivalent`
- `unknown`
- `unsupported`
- `tool_error`
- `not_attempted`

Consequence:

- The staged tool can produce a decidable refutation for a minimal FROM-clause pair.
- The staged tool did not produce a clean equivalent verdict for the identical projection pair within the 30 second timeout.
- No local result-checker exactness was used as verifier evidence.
