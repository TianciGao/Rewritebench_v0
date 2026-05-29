# SQLGlot Candidate Root Review

## SQLGlot No-Op

`runs/user/common_core_pg_noop_db_checker/candidate_sql` appears to be the correct PostgreSQL-only Common-core no-op root for PG40 diagnostics. It contains 40 Common-core PostgreSQL candidates and is suitable as a sanity/control root for diagnostic POCR work.

The canonical Track A 120 SQLGlot no-op roots are not complete as a tri-engine family. The inventory shows:

- MySQL: 40 Common-core candidate files
- PostgreSQL: 35 Common-core candidate files
- Spark: 40 Common-core candidate files

Because the PostgreSQL canonical Track A component is incomplete, SQLGlot no-op is not ready for Track A 120 POCR annotation. The complete PG40 no-op root must not be used to fill a Track A 120 POCR cell.

## SQLGlot Optimize Schema-Aware

The inventory found candidate roots for SQLGlot optimize schema-aware, but they are incomplete:

- MySQL: 32 Common-core candidate files
- PostgreSQL: 34 Common-core candidate files
- Spark: 39 Common-core candidate files

These roots are candidate SQL files, not merely result or metrics artifacts, but they do not cover the PG40 or Track A 120 denominator. Missing or fail-closed rows must remain visible and cannot be silently dropped for POCR annotation.

## Boundary

SQLGlot no-op can support PostgreSQL-only PG40 diagnostic control work. SQLGlot optimize schema-aware remains POCR-deferred until candidate-root completeness and no-candidate handling are explicitly scoped.
