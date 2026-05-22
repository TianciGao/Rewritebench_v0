# VeriEQL Placeholder Contract

Status: planned only; not implemented.

Expected input shape:

- A planned pair from `verifier_pairs.csv`.
- Source SQL path.
- Candidate, positive, or negative SQL path depending on `pair_type`.
- Schema context path when available.
- Checker context path for diagnostic traceability only.

Expected bounded/canary mode:

- Start with `support_pair_smoke` pairs before broader source/candidate use.
- Fail closed when schema context or dialect support is missing.

Verdict normalization:

- Tool-native equivalent -> `equivalent`.
- Tool-native counterexample/non-equivalence -> `non_equivalent`.
- Inconclusive -> `unknown`.
- Timeout -> `timeout`.
- Unsupported syntax/dialect -> `unsupported`.
- Invocation or parsing failures -> `tool_error`.

Timeout/error handling:

- Record `timeout_seconds`.
- Preserve raw stdout/stderr paths.
- Do not convert errors or unsupported cases into mismatches.
- Do not compute Semantic Equivalence Rate from non-decidable outcomes.
