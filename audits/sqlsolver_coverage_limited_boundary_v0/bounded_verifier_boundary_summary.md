# Bounded Verifier Boundary Summary

SQLSolver currently supports only bounded diagnostic verifier evidence in this repository.

The same-8 stability gate failed after canonicalization and support-scope guards. The rerun used the same eight SQLGlot no-op PostgreSQL pairs, but only two pairs passed both identity guards. Three pairs were explicitly scoped out as `no_verifier_support`, and three pairs still have unclassified identity blockers.

## Blocked scopes

- SQLGlot no-op PostgreSQL 35-row exact subset: blocked.
- 346-pair manifest: blocked.
- Cross-route verifier coverage: blocked.

## Interpretation

This is not a rewrite-method failure and not a result-consistency failure. The affected rows were exact/result-consistent before verifier support was attempted. The boundary is a SQLSolver verifier-support, schema-modeling, and SQL-feature coverage boundary.

Unsupported, `no_verifier_support`, unknown, timeout, and tool-error verifier outcomes must be reported separately from method failure buckets and excluded from any decidable SER denominator.
