# Schema Fallback Review

Handling decision: execute the four schema-fallback candidates because each had a non-empty generated SQL file and the PostgreSQL executor fails closed on execution errors.

Schema-fallback rows:

| case_id | source_execution_status | candidate_execution_status | checker_status | failure_bucket |
| --- | --- | --- | --- | --- |
| PORT_0013 | source_execution_failed | execution_not_enabled | not_attempted | source_execution_failed |
| LONGTAIL_0022 | source_execution_success | candidate_execution_failed | not_attempted | candidate_execution_failed |
| LONGTAIL_0023 | source_execution_success | candidate_execution_failed | not_attempted | candidate_execution_failed |
| LONGTAIL_0024 | source_execution_success | candidate_execution_failed | not_attempted | candidate_execution_failed |

Results:

- Schema-fallback rows attempted: 4.
- Schema-fallback exact rows: 0.
- Schema-fallback failed rows: 4.
- `PORT_0013` failed at PostgreSQL source execution because the source SQL uses backtick syntax that is not PostgreSQL-compatible.
- `LONGTAIL_0022`, `LONGTAIL_0023`, and `LONGTAIL_0024` source SQL executed, but generated candidates failed because Calcite emitted quoted mixed-case table identifiers that do not match the PostgreSQL-loaded lower-case relations.

These rows must remain separate from the 29 `calcite_rel_to_sql` rows in any later interpretation.
