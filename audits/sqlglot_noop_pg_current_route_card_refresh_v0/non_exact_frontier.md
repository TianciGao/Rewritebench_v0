# Non-Exact Frontier

The non-exact frontier contains five rows. All five are no-candidate rows from cross-dialect PORT cases whose source SQL is MySQL-like while the SQLGlot noop adapter was invoked with PostgreSQL dialect settings.

| case_id | pool | frontier_bucket | status |
| --- | --- | --- | --- |
| PORT_0004 | PORT | no_candidate_sql / adapter_failed | SQLGlot parse failed |
| PORT_0013 | PORT | no_candidate_sql / adapter_failed | SQLGlot parse failed |
| PORT_0022 | PORT | no_candidate_sql / adapter_failed | SQLGlot parse failed |
| PORT_0024 | PORT | no_candidate_sql / adapter_failed | SQLGlot parse failed |
| PORT_0025 | PORT | no_candidate_sql / adapter_failed | SQLGlot parse failed |

There were no checker mismatches, source execution failures, candidate execution failures, or timing failures among generated rows.

Recommended treatment:

- Keep these five rows denominator-visible.
- Do not reinterpret local exactness from other rows as evidence for these rows.
- Treat the blocker as a cross-dialect PORT source-role / dialect-syntax issue, not as a PostgreSQL execution/checker failure for generated SQLGlot candidates.
