# Missing or Ambiguous Roots

The broad candidate SQL inventory found 1,579 ambiguous roots, mostly unit, smoke, fixture, or partial artifacts. Those roots should not be used for POCR annotation without human selection.

## Table 1 Routes Without Complete Candidate Roots

- SQLGlot no-op Track A 120: canonical PostgreSQL component has 35 Common-core candidate files, so the tri-engine denominator is incomplete.
- SQLGlot optimize schema-aware: MySQL has 32, PostgreSQL has 34, and Spark has 39 Common-core candidate files.
- Calcite HEP fail-closed: each engine has 33 Common-core candidate files.
- LearnedRewrite PG40 prior-method row: only 29 generated PostgreSQL candidate files are present.

## Roots To Ignore For This Reconciliation

Smoke and unit-test candidate roots remain useful for tests, but they do not map cleanly to Table 1 route rows. They should not be used to fill Positive Operation Coverage Rate values.

## Human Selection Required

Any root that lacks a clear method, route, engine, and denominator mapping should remain excluded from POCR annotation. Annotation artifacts are route-bound evidence and must match case ID, engine, method ID, route ID, candidate identity, prompt/schema version, provider/model metadata, and call timestamp.
