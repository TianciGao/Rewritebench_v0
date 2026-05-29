# Next Steps

Recommended next safe action:

- Produce a Track A 120 rerun readiness plan.

That plan should decide whether the current PostgreSQL-only local diagnostics
are enough to authorize a broader local rerun, and it should keep these open
questions explicit:

- SQLGlot noop PORT source-role / dialect handling.
- Calcite no-candidate and schema-fallback policy.
- Calcite source-role execution failure.
- Calcite checker mismatches and semantic review.
- MySQL/Spark readiness and engine-specific blockers.

Do not promote this comparison to paper-facing evidence without a separate
authorization and a rerun through the approved user-facing output path.
