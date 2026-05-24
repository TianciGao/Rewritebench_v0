# Implementation Summary

Task: `sqlsolver_support_scope_guard_impl_v0`

## Files changed

- `src/sql_rewrite_bench/verifier_support/sqlsolver.py`
- `tests/verifier_support/test_sqlsolver_canonicalization.py`

## Guard logic added or tightened

- Added `SQLSolverSupportScopeDecision` and `sqlsolver_support_scope_decision(sql_text)`.
- Added pre-invocation support-scope checks for current known SQLSolver blocker families.
- Added guarded verdict artifact metadata: `support_scope_guarded`, `support_scope_family`, `support_scope_guard_category`, `support_scope_verdict=no_verifier_support`, and `sqlsolver_invocation_allowed=false`.
- The shared normalized verdict remains `unsupported` because the current verifier verdict vocabulary does not include `no_verifier_support` as a normalized verdict.

## Families scoped out

- `quoted_identifier_null_ordering`: quoted identifiers combined with `NULLS FIRST` / `NULLS LAST` ordering.
- `dense_rank_cte_ranking`: `DENSE_RANK()` and CTE/window-over-CTE ranking shapes.

## Existing behavior preserved

- Line/comment shaping.
- One-statement-per-line preparation.
- Terminal semicolon normalization.
- Block and line comment stripping outside string literals / quoted identifiers.
- Schema inline-comment stripping.
- `DROP TABLE` preamble removal for SQLSolver schema input only.
- Conservative PostgreSQL type normalization.
- Unsafe canonicalization fail-closed behavior.

## What remains unsupported

The two scoped-out families remain outside current SQLSolver support. They are reported as verifier-support boundaries and excluded from decidable SER support. No semantic rewriting was added to make them pass.

## Why this is not semantic rewriting

The guard does not change SQL semantics, strip quoted identifiers, remove NULL ordering, or rewrite DENSE_RANK/window/CTE forms. It only prevents known unsupported families from reaching SQLSolver and returning unclassified `UNKNOWN`.
