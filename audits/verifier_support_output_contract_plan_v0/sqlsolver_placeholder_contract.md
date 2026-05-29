# SQLSolver Placeholder Contract

Status: planned only; not implemented.

Expected input shape:

- A planned pair from `verifier_pairs.csv`.
- Source SQL path.
- Candidate, positive, or negative SQL path depending on `pair_type`.
- Schema context path when available.
- Optional checker context path for traceability.

Expected bounded support-pair mode:

- Start with small `support_pair_smoke` pairs.
- Restrict to SQL features supported by the tool.
- Fail closed for unsupported SQL or missing schema context.

Verdict normalization:

- Equivalent proof -> `equivalent`.
- Non-equivalence proof or counterexample -> `non_equivalent`.
- Inconclusive solver result -> `unknown`.
- Timeout -> `timeout`.
- Unsupported syntax/dialect -> `unsupported`.
- Tool invocation failure -> `tool_error`.

Timeout/error handling:

- Preserve raw stdout/stderr artifacts.
- Record runtime and timeout policy.
- Do not treat unsupported/tool-error outcomes as formal non-equivalence.
- Do not feed SQLSolver outcomes into leaderboard or speedup reporting.
