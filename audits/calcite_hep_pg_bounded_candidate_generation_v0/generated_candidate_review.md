# Generated Candidate Review

Generated candidate rows: 33

Candidate review status counts:

| candidate_review_status | count |
| --- | --- |
| fail_closed_no_candidate | 7 |
| generated_calcite_rel_to_sql | 29 |
| generated_parse_only_schema_fallback_review | 4 |

Review observations:

- Empty generated candidate files: 0.
- Normalized source-identical generated candidates: 0.
- Calcite `rel_to_sql` generated candidates: 29.
- Calcite parse-only schema-fallback generated candidates: 4.

Parse-only schema-fallback rows require manual review before any execution/checker pass because the runtime emitted SQL after parse-level handling while reporting a schema-ingestion limitation:

| case_id | blocker_category | emission_mode | candidate_sql_bytes |
| --- | --- | --- | --- |
| PORT_0013 | schema_ingestion_unsupported_column_definition | calcite_parse_only | 200 |
| LONGTAIL_0022 | schema_ingestion_unsupported_sql_type | calcite_parse_only | 559 |
| LONGTAIL_0023 | schema_ingestion_unsupported_sql_type | calcite_parse_only | 762 |
| LONGTAIL_0024 | schema_ingestion_unsupported_sql_type | calcite_parse_only | 637 |

The runner did not check candidate parse status and did not execute candidates in this task. The next execution/checker pass must treat these generated candidates as unexecuted local diagnostic candidates, not as exact or metric-ready evidence.
