# Exact-Gating Review

## Bounded Smoke Rows

The reviewed timing smoke artifacts contain six exact same-engine rows:

- `PERF_0006` on PostgreSQL, MySQL, and Spark
- `CONS_0005` on PostgreSQL, MySQL, and Spark

All six row artifacts have:

- `exact_status=exact`
- `failure_bucket=none`
- `timing_eligible=true`
- `timing_status=timed`
- five source samples
- five candidate samples
- non-null source/candidate medians
- non-null per-row local diagnostic `speedup_ratio`

This confirms exact rows can be timed under the opt-in local diagnostic path.

## Non-Exact And N.A. Rows

The bounded smoke artifacts contain no non-exact rows. Non-exact behavior was reviewed through the committed implementation tests and the implementation audit:

- mismatch rows become `timing_eligible=false` with `speedup_ratio=null`
- label-only mismatches remain timing-ineligible under the strict label policy
- unsupported/fail-closed rows remain timing-ineligible
- partial timing failures retain available samples and use `timing_status=partial_failure` with `speedup_ratio=null`

No reviewed artifact or committed test indicates a violation of exact-gated timing eligibility.

## Review Boundary

This review did not create new timing artifacts and did not compute official metrics. The observed per-row `speedup_ratio` values are existing local diagnostic fields in row artifacts, not route-level or paper metrics.
