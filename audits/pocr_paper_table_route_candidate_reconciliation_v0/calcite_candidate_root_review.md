# Calcite Candidate Root Review

The Calcite HEP fail-closed candidate roots exist for all three engines, but each is incomplete:

- MySQL: 33 Common-core candidate files
- PostgreSQL: 33 Common-core candidate files
- Spark: 33 Common-core candidate files

These roots represent generated candidate SQL where Calcite produced a candidate. Parse-failed, unsupported, or fail-closed rows appear to have no candidate SQL file. That is expected route behavior, but it makes the roots unsuitable for direct full-denominator POCR annotation without an explicit no-candidate policy.

Calcite HEP fail-closed is therefore not PG40-ready and not Track A 120-ready for POCR annotation. It should remain N.A. in the paper-facing Positive Operation Coverage Rate column unless a separately authorized task defines how no-candidate rows are represented in diagnostic POCR outputs.

No candidate SQL was modified, moved, copied, or deleted during this review.
