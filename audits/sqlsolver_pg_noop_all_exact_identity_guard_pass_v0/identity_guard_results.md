# Identity Guard Results

Identity sanity policy:

A source-vs-candidate SQLSolver verdict may enter the corrected decidable denominator only when source-vs-source and candidate-vs-candidate both normalize to `equivalent`.

Result:

- Identity checked rows: 35.
- Identity passed rows: 24.
- Identity failed rows: 11.
- Identity pass rate: 24/35.

Failure categories:

- `identity_guard_failed_unknown`: 8 rows.
- `identity_guard_failed_timeout`: 3 rows.
- `identity_guard_failed_tool_error`: 0 rows.

Rows excluded by identity guard:

- Timeout: `PERF_0034`, `PERF_0062`, `LONGTAIL_0024`.
- Unknown: `PERF_0035`, `PERF_0052`, `PORT_0003`, `PORT_0005`, `PORT_0008`, `PORT_0012`, `LONGTAIL_0011`, `LONGTAIL_0013`.

All identity-failed rows were excluded from corrected `V_equiv` and `V_non`.
