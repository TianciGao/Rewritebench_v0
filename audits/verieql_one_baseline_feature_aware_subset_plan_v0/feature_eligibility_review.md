# Feature Eligibility Review

Feature matrix file:
- `feature_eligibility_matrix.csv`

Eligibility labels used:
- `verifier_eligible_candidate`
- `likely_supported`
- `blocked_like_not_implemented`
- `blocked_exists_or_subquery`
- `blocked_function_or_datetime`
- `blocked_dialect_syntax`
- `blocked_ddl_parser`
- `blocked_schema_metadata`
- `manual_review_required`
- `not_exact_ineligible`

Primary observed counts across 35 exact rows:

| category | count | interpretation |
| --- | ---: | --- |
| verifier_eligible_candidate | 1 | `CONS_0036` already produced clean all-`EQU` in the tiny exact-candidate pass. |
| blocked_ddl_parser | 1 | `CONS_0037` is the closest expansion row but should wait for DDL parser hardening. |
| blocked_like_not_implemented | 4 | `LIKE` has already produced VeriEQL `NIE` on real rows. |
| blocked_exists_or_subquery | 17 | Includes `EXISTS`, nested `SELECT`, `IN (SELECT ...)`, and set-operation risk. |
| blocked_function_or_datetime | 10 | Includes date/time, window, and function-heavy shapes that need separate probes. |
| blocked_dialect_syntax | 2 | Includes quoted identifiers, `LIMIT`, `NULLS FIRST/LAST`, or dialect syntax risk. |

Cross-cutting flags:
- Parameterized-DDL parser rough edge: 17 exact rows.
- Manual-review caveat present: 4 exact rows.
- Schema canonicalization gap: none observed after the finite-bound wrapper mode, but DDL parsing still needs hardening.

Known empirical constraints:
- `CONS_0036` succeeded despite a `VARCHAR(32)` DDL parser caveat.
- `PERF_0077` and `PERF_0082` both reached VeriEQL but returned `NIE` on `LIKE`.
- `CONS_0007` previously returned unsupported for `EXISTS`.
- `PERF_0062` previously timed out under timeout-mode canary behavior; finite-bound exact-candidate expansion should still avoid date/list-heavy shapes until feature probes are clearer.

