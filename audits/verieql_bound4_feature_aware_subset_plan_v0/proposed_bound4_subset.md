# Proposed Bound-4 Subset

The proposed next actual verifier pass should remain small and use exactly one declared policy: `finite_bound_bound4_timeout30_cores1`.

Proposed rows:

- `CONS_0036`
- `CONS_0037`

Rationale:

- Both rows are exact/result-consistent in `runs/user/common_core_pg_noop_db_checker`.
- Both rows have already returned clean all-`EQU` under the uniform bound-4 policy.
- `CONS_0036` remains the positive-control row.
- `CONS_0037` verifies that the DDL parser hardening and smaller declared bound policy can support the first expansion row.

Rows not included in the first expansion:

- LIKE rows remain blocked by `blocked_like_not_implemented`.
- EXISTS/subquery rows remain blocked by `blocked_exists_or_subquery`.
- Function/date-time-heavy rows remain blocked by `blocked_function_or_datetime`.
- Dialect syntax rows remain blocked by `blocked_dialect_syntax`.

The proposed subset is recorded in `proposed_bound4_subset.csv`.
