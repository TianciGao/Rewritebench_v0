# Non-Exact Frontier

Twenty selected PostgreSQL rows remain outside the exact timed subset.

Frontier counts:

- `no_candidate_sql = 7`
- `mismatch = 3`
- `source_execution_failed = 2`
- `candidate_execution_failed = 8`

Mismatch rows confirmed by the execution/checker audit:

- `PERF_0035`
- `PERF_0062`
- `CONS_0011`

The route card keeps these rows denominator-visible. They are not dropped from local coverage rates, and they are not included in speedup diagnostics.
