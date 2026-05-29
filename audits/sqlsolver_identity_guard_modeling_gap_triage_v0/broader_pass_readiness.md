# Broader Pass Readiness

ready_for_larger_sqlsolver_pass: no

## Recommended Next Scope

Do not authorize a larger SQLSolver pass yet. The recommended next scope is a wrapper/schema canonicalization design task for identity-guard stability, followed by bounded non-benchmark feature canaries for the observed gap families.

## Required Fixes Before Broader Pass

- Strip or preserve line comments safely instead of collapsing leading `--` comments into a single-line SQLSolver input.
- Canonicalize schema DDL for SQLSolver, including inline comments, draft DDL preambles, `DOUBLE PRECISION`, and unsupported PostgreSQL types when necessary.
- Decide date/interval normalization policy for TPC-H-style PostgreSQL syntax.
- Decide PORT scope policy for quoted identifiers, `NULLS FIRST/LAST`, and draft schema evidence.
- Add identity-guard canaries for DENSE_RANK/CTE ranking before including longtail ranking rows in a broader verifier pass.

## Full SQLGlot No-op PostgreSQL 35 Exact Subset

Not safe yet. The bounded 8-row sample already found 5 identity-guard unknown rows, including PERF and PORT cases. A 35-row pass would likely increase unknown coverage before the modeling gaps are understood.

## Broader 346-Pair Manifest Scope

Blocked. The 346-pair cross-route manifest includes more engines, routes, and feature families than this bounded subset. It should not be attempted until PostgreSQL SQLGlot no-op identity guards are stable for an agreed verifier-support subset.

## SER Boundary

No official SER can be promoted from this state. `SER_status` remains `coverage_limited`; `official_SER=false` remains in force.
