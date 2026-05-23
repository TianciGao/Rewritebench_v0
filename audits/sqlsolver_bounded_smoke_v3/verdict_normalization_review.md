# Verdict Normalization Review

SQLSolver-like output maps to the shared vocabulary:

- `equivalent`: clear equivalent/proved/valid/verified output.
- `non_equivalent`: clear counterexample/refute/not-equivalent/invalid output.
- `unknown`: inconclusive, undecidable, or unknown output.
- `timeout`: timeout or time-limit output, or process timeout.
- `unsupported`: unsupported SQL/syntax output.
- `tool_error`: nonzero or unrecognized error output.
- `not_attempted`: fail-closed unavailable path.

Nonzero process exits that still emit a clear counterexample remain `non_equivalent`, not `tool_error`.

Bare solver terms such as `sat`/`unsat` are not treated as sufficient evidence by this wrapper; output must contain a clearer equivalence or counterexample signal.
