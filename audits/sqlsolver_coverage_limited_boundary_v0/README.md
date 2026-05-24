# SQLSolver Coverage-Limited Boundary

This packet records the boundary after the same-8 SQLSolver bounded benchmark rerun failed the stability gate after canonicalization and support-scope guards.

## Same-8 rerun result

- Selected benchmark pairs: `8`
- Identity guard passed: `2/8`
- `no_verifier_support`: `3/8`
- Unclassified identity blockers: `3/8`
- Actual source-candidate checks attempted: `2`
- Actual equivalent: `2/2` attempted
- `ready_for_sqlglot_noop_pg_35=false`
- `official_SER=false`

## Why this exists

The support-scope guard fixed the known canary blockers, but the same-8 benchmark rerun still has residual unclassified identity blockers. That means SQLSolver is coverage-limited verifier support, not a stable verifier line for the SQLGlot no-op PostgreSQL 35-row exact subset.

## Next safe action

Integrate this coverage-limited verifier status into user-facing diagnostic summaries, or return to Repair-1 fake-provider implementation. Do not broaden SQLSolver coverage unless a separate residual schema-modeling fix is authorized.
