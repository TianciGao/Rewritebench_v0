# Dry Run Scope

Included routes:

- Direct LLM Repair-1 PostgreSQL PG40, using the accepted release-v0 diagnostic exemplar after targeted retry.
- SQLGlot no-op PostgreSQL PG40, using the sanity/control diagnostic route.

These routes are used because they are the current complete PG40 exemplar/control pair with route-bound annotation and replay artifacts. Repair-1 exercises a real method route. SQLGlot no-op checks that Stage B remains conservative for source-like or low-transform candidates.

SQLGlot optimize schema-aware PostgreSQL PG40 is excluded from numeric dry-run because it is not ready for full PG40 annotation: only 34/40 actual optimize candidates exist, and no-op candidates must not be substituted.

This task does not change denominator, case membership, paper results, raw legacy evidence, retained evidence, candidate SQL, or top-level reports/results.

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted.
