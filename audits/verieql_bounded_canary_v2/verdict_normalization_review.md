# Verdict Normalization Review

The VeriEQL wrapper maps bounded process output to the shared verifier verdict vocabulary.

Examples covered by tests:

- `Result: equivalent` -> `equivalent`
- `VERIFIED: valid` -> `equivalent`
- `Counterexample found` -> `non_equivalent`
- `The claim was refuted` -> `non_equivalent`
- `unknown` -> `unknown`
- `unsupported syntax` -> `unsupported`
- timeout state -> `timeout`
- nonzero return with crash text -> `tool_error`

The wrapper checks non-equivalence/refutation before equivalence so strings like `not equivalent` do not become false positives.

Unrecognized output remains fail-visible as `tool_error`.
