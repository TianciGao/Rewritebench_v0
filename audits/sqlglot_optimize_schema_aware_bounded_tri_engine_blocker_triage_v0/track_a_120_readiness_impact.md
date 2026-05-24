# Track A 120 Readiness Impact

Route:

- `sqlglot_optimize_schema_aware`

Prior bounded scope:

- 3 cases: `CONS_0005`, `PERF_0006`, `CONS_0036`
- 3 engines: PostgreSQL, MySQL, Spark
- 9 planned rows

## Current readiness

PostgreSQL:

- Bounded diagnostic status: 3/3 exact.
- Readiness impact: PostgreSQL looks ready for a larger local diagnostic trial, subject to standard fail-visible route-card boundaries.

MySQL:

- Bounded diagnostic status: 2/3 exact.
- Blocker: `CONS_0005` candidate execution failure from unsupported `ARRAY_ANY` / lambda syntax.
- Readiness impact: not ready for larger MySQL optimize trial until the route fails closed earlier or emits MySQL-safe SQL.

Spark:

- Bounded diagnostic status: 1/3 exact.
- Blockers:
  - `CONS_0005` row-count/value mismatch.
  - `CONS_0036` label-only mismatch under strict checker policy.
- Readiness impact: not ready for larger Spark optimize trial until Spark semantic and label-policy questions are handled or explicitly accepted as fail-visible boundaries.

## Timing readiness

Exact-gated timing over the six exact rows is technically safe because the non-exact rows would remain excluded and denominator-visible. However, the higher-value next step is blocker resolution before timing if the goal is Track A 120 readiness.

Recommendation:

- Timing smoke can proceed only as a narrow local diagnostic over the six exact rows.
- Larger route-card timing or Track A 120 timing should wait.

## Full Track A 120 readiness verdict

Not ready.

Reasons:

- MySQL still has an unsupported SQLGlot dialect-emission blocker.
- Spark has one value/row-count semantic-risk mismatch.
- Spark has one strict-label mismatch requiring explicit policy before any exactness change.
- The evidence comes from a 9-row bounded smoke, not a 40 x 3 local diagnostic rerun.

No official metrics, Semantic Equivalence Rate, paper-facing result, retained-evidence promotion, or leaderboard output is authorized from this audit.

