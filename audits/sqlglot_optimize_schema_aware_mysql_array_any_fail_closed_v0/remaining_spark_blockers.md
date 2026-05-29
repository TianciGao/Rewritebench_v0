# Remaining Spark Blockers

This task intentionally did not address Spark blockers.

## Spark CONS_0005

Status:

- Still a checker mismatch.
- Source row count remains 0.
- Candidate row count remains 1.

Classification from prior triage:

- `spark_semantic_mismatch_candidate`
- `true_candidate_semantic_drift`
- `manual_review_required`

Recommended next action:

- Dedicated Spark semantic triage for SQLGlot's NULL-sensitive `NOT IN` rewrite behavior.

## Spark CONS_0036

Status from prior triage:

- Strict-label mismatch.
- Values match.
- Labels differ by case.

Classification:

- `spark_label_only_mismatch_candidate`
- `checker_normalization_policy_candidate`

Recommended next action:

- Keep fail-visible unless a separate explicit checker label policy is authorized.

These blockers continue to prevent larger Spark and full Track A 120 readiness for `sqlglot_optimize_schema_aware`.
