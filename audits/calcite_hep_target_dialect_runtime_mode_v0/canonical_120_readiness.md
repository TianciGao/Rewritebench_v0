# Canonical Track A 120 Readiness

Verdict: not ready for canonical metrics yet, but the target-dialect runtime
blocker is materially reduced.

Ready after this task:

- Adapter passes target engine to the runtime.
- External runtime can emit MySQL and Spark dialect SQL on the bounded matrix.
- PostgreSQL behavior remained stable.
- MySQL/Spark PostgreSQL-dialect guard remains as a safety net.
- MySQL and Spark are ready for a larger bounded execution/checker diagnostic.

Still blocking canonical Track A 120 metrics:

- This was only an 18-row bounded smoke, not a 120-row diagnostic.
- `PORT_0004` remains no-candidate.
- Spark `PORT_0024` remains blocked by target-reference/source-role policy.
- Spark DDL ingestion still falls back to parse-only for some `STRING` DDL
  shapes; this did not block the bounded exact rows but needs tracking.
- Schema-fallback policy and broader mismatch frontier still need full
  denominator-visible diagnostic review.

Next safe task:

Run a Calcite HEP Track A 120 local execution/checker diagnostic through the
user facade, with no timing and no `compute-local-metrics`, to discover the
full tri-engine denominator frontier after target-dialect mode.
