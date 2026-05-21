# Same-Engine Regression Boundary

The opt-in cross-dialect checker normalization must not relax same-engine checks.

The normalization policy is enabled only for manifest-declared cross-dialect local diagnostics with `local_diagnostic.diagnostic_mode == cross_dialect_reference` and `local_diagnostic.checker.comparison == source_reference_result_to_target_candidate_result`. It is intended for comparing MySQL source-reference result artifacts with PostgreSQL target-candidate result artifacts in local diagnostics.

PERF, CONS, and LONGTAIL default behavior remains unchanged. Same-engine comparisons continue to use the existing strict checker behavior unless a future task separately authorizes a different policy.

Same-engine PORT cases are not forced into cross-dialect mode. `PORT_0003`, `PORT_0005`, `PORT_0008`, and `PORT_0012` remain same-engine local diagnostic cases with PostgreSQL source-reference and PostgreSQL target-candidate roles.

This boundary protects current user-entry diagnostics from accidentally turning column-label positional comparison or decimal-string relaxation into a global checker default.
