# Route And Denominator Guard Review

## Route Guards

All reviewed summary JSON files report:

- `route_ids=["sqlglot_noop"]`
- `method_ids=["sqlglot"]`
- `grouping_policy.route_aware=true`
- `grouping_policy.method_aware=true`
- `grouping_policy.route_mixing_allowed=false`
- `grouping_policy.method_ordering_output=false`

The by-engine CSV groups by local run, route, method, engine, and timing policy.

The by-pool CSV groups by local run, route, method, pool, and timing policy.

The per-row speedup CSV includes route, method, engine, pool, case, denominator, and timing policy identity.

## Denominator Guards

Each reviewed bounded smoke run has two denominator rows:

- `track_a_same_engine:CONS_0005:<engine>`
- `track_a_same_engine:PERF_0006:<engine>`

The denominator identifiers are preserved in summary, by-engine/by-pool CSVs, and row-level timing diagnostics.

## Performance Gate

Performance fields are populated from strict exact + timed rows only:

- PostgreSQL: 2 exact timed rows, speedup denominator 2.
- MySQL: 2 exact timed rows, speedup denominator 2.
- Spark: 2 exact timed rows, speedup denominator 2.

No reviewed output includes non-exact rows in the performance denominator. The reviewed bounded smoke does not include label-only, unsupported, or partial timing rows, but the fields needed to represent them are present and were covered by the calculator implementation tests.

## Verdict

Route, method, denominator, engine, and timing-policy guards are present and suitable for broader local diagnostic projection. No route mixing or leaderboard-style aggregation was observed.
