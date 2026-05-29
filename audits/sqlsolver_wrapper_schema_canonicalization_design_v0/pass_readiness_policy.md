# Pass Readiness Policy

## ready_to_rerun_same_8_pairs

Ready only after all planned canonicalization unit tests pass and the five non-benchmark identity canaries are authorized and produce stable, interpretable identity-guard outcomes. A same-8 rerun must use the same selected pair scope as `sqlsolver_bounded_verifier_pass_sqlglot_noop_pg_v0`.

## ready_for_sqlglot_noop_pg_35

Ready only after the same-8 rerun shows no unexpected identity-guard regressions and all non-decidable rows have explicit, expected buckets. Any remaining `UNKNOWN` identity guard must be tied to a predeclared out-of-scope feature family, not an unexplained wrapper/schema issue.

## ready_for_cross_route_346_manifest

Blocked until SQLGlot no-op PostgreSQL 35 is stable and a separate route/engine applicability matrix is updated. Cross-route coverage must not be inferred from PostgreSQL SQLGlot no-op stability.

## blocked_by_feature_support

Rows with unsupported feature families, including DENSE_RANK/CTE ranking or untested window-function families, remain blocked until feature canaries pass or the family is explicitly excluded from the verifier-support scope.

## blocked_by_schema_canonicalization

Rows with DDL parser diagnostics, unsupported type syntax, inline comments, draft DDL preambles, or schema abstraction uncertainty remain blocked until schema canonicalization is designed and tested.

## blocked_by_wrapper_format

Rows with leading line comments, multi-line SQL, multiple statements, or line-comment collapse risks remain blocked until the wrapper line-shaping policy is implemented and unit tested.
