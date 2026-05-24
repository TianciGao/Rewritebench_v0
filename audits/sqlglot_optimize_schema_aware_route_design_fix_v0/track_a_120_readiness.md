# Track A 120 Readiness

Current verdict:
- `sqlglot_optimize_schema_aware` is ready for a larger local diagnostic trial.
- It is not yet ready for an official or paper-facing Track A 120 rerun.

What improved:
- The immediate `CONS_0005` context-free invalid qualification blocker is removed for generation/preflight across PostgreSQL, MySQL, and Spark.
- The old context-free route remains available for historical comparison and fail-visible behavior.

Still needed before full Track A 120 local diagnostic rerun:
- Bounded tri-engine execution/checker pass for `sqlglot_optimize_schema_aware`.
- Exact-gated timing only after checker exactness is established.
- Denominator-aware route card under the D035 local diagnostic output convention.
- Review of any optimizer warnings or dialect-specific unsupported expressions, including the MySQL `ARRAY_ANY is unsupported` warning observed during `CONS_0005` generation.
- PORT source-role policy remains separate and must not be silently mixed with same-engine route readiness.

Paper boundary:
- No official metrics are computed by this task.
- No Semantic Equivalence Rate is computed.
- No paper table or retained evidence is updated.
