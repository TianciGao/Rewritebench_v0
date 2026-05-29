# Implementation Summary

Task: `sqlsolver_wrapper_schema_canonicalization_impl_v0`

## Files changed

- `src/sql_rewrite_bench/verifier_support/sqlsolver.py`
- `tests/verifier_support/test_sqlsolver_canonicalization.py`

## Functions added or changed

- Added `SQLSOLVER_GUARD_CATEGORIES` and `SQLSolverCanonicalizationResult`.
- Added `canonicalize_sqlsolver_query(sql_text)` for SQLSolver query input shaping.
- Added `canonicalize_sqlsolver_schema(schema_text)` for SQLSolver schema DDL shaping.
- Added `classify_sqlsolver_guard(sql_text, schema_text=None)` for explicit support-risk categories.
- Updated the SQLSolver JAR invocation path to write canonicalized temporary verifier inputs and to fail closed before invocation when canonicalization is unsafe.
- Added canonicalization metadata to SQLSolver verdict `artifact_paths` so guard categories are visible and not silently promoted.

## Canonicalization families implemented

- SQL line/comment shaping.
- One-statement-per-line query preparation.
- Terminal semicolon normalization.
- Block and line comment stripping outside string literals and quoted identifiers.
- Schema inline-comment stripping.
- `DROP TABLE` preamble removal for SQLSolver schema input only.
- Conservative PostgreSQL type normalization for `DOUBLE PRECISION`, `TIMESTAMP WITHOUT TIME ZONE`, `TEXT`, and `NUMERIC`.
- Guard classification for unsupported SQL features, PostgreSQL dialect risk, schema canonicalization gaps, wrapper input format gaps, type/function modeling gaps, query normalization gaps, and unknown tool behavior.

## What remains unsupported

- The quoted identifier plus `NULLS FIRST` canary still returned SQLSolver `UNKNOWN` for source and candidate identity checks.
- The `DENSE_RANK` / CTE ranking canary still returned SQLSolver `UNKNOWN` for source and candidate identity checks.
- No benchmark pair is newly eligible for SER promotion from this task.

## Why this implementation is narrow

The layer does not rewrite query semantics, does not run SQLGlot optimization/transpilation, does not mutate benchmark SQL/schema files, and writes only temporary verifier inputs. Unsafe shaping fails closed as verifier-support limitation. It does not compute or promote SER.
