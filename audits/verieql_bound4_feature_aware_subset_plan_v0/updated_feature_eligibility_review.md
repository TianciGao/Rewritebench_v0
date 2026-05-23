# Updated Feature Eligibility Review

The refreshed feature matrix is recorded in `updated_feature_eligibility_matrix.csv`.

The prior DDL parser rough edge for parameterized SQL types has been removed from the active blocker classification. The hardening task preserved parameterized types such as `VARCHAR(32)`, `NUMERIC(15,2)`, and `DECIMAL(9,2)` in VeriEQL schema metadata. `CONS_0037` is therefore no longer blocked by DDL parsing.

Updated exact-row eligibility counts:

- `already_validated_bound4_equivalent`: 2
- `blocked_exists_or_subquery`: 17
- `blocked_function_or_datetime`: 10
- `blocked_like_not_implemented`: 4
- `blocked_dialect_syntax`: 2

Already validated bound-4 rows:

- `CONS_0036`: clean all-`EQU` under `finite_bound_bound4_timeout30_cores1`
- `CONS_0037`: clean all-`EQU` under `finite_bound_bound4_timeout30_cores1`

Blocked categories:

- `blocked_like_not_implemented`: includes rows such as `PERF_0077` and `PERF_0082`; previous real attempts returned `NIE` on `LIKE`.
- `blocked_exists_or_subquery`: includes `CONS_0007`, which previously returned unsupported because of `EXISTS`, plus other nested-subquery, union, or window/subquery-heavy rows.
- `blocked_function_or_datetime`: includes aggregation, date/time, arithmetic, and function-heavy PERF/PORT rows that remain outside the first bound-4 expansion.
- `blocked_dialect_syntax`: includes exact PORT rows with dialect syntax and quoting/order/limit/null-ordering risks.

No additional row beyond `CONS_0036` and `CONS_0037` was identified as low-risk enough for the first actual bound-4 feature-aware verifier pass.
