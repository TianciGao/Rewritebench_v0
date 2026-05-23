# Blocker Summary

Known blockers carried forward from the source audits:

- Identifier quoting / mixed-case Calcite candidates against PostgreSQL-loaded lower-case relations.
- DATETIME/TIMESTAMP and PORT source-dialect blockers.
- Parse-only schema-fallback candidates all failed during execution.
- Checker mismatches for `PERF_0035`, `PERF_0062`, and `CONS_0011`.
- Seven rows failed closed with `no_candidate_sql`.

These blockers must be addressed before MySQL/Spark expansion or a full 120-row route interpretation.
