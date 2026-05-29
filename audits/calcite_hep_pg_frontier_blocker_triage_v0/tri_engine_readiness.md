# Tri-Engine Readiness

PostgreSQL-only route-card comparison against SQLGlot noop is safe as a local diagnostic comparison if it preserves:

- The 40-row selected denominator.
- The non-exact frontier.
- The local-only, non-official boundary.
- The fact that timing applies only to exact rows.

MySQL/Spark/full-120 expansion should remain blocked for now.

Reasons:

- PORT source-role/dialect handling is not settled.
- DATETIME/TIMESTAMP/schema ingestion blockers remain.
- Schema-fallback candidates should be excluded by policy until hardened.
- Identifier quoting affects candidate execution and may behave differently across engines.
- Three PostgreSQL rows are true checker mismatches requiring manual review.
