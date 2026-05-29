# Fail-Closed Review

Fail-closed rows: 7

All fail-closed rows were PORT cases with `failure_bucket=no_candidate_sql` and `calcite_runtime_status=calcite_no_candidate_sql`. The external command exited `0` but emitted no candidate SQL, so the adapter correctly preserved fail-closed behavior.

Fail-closed rows:

| case_id | blocker_category | blocker_stage | runtime_status |
| --- | --- | --- | --- |
| PORT_0003 | calcite_parse_double_quote_identifier | parse | calcite_no_candidate_sql |
| PORT_0004 | calcite_parse_datetime_keyword_or_ddl_type | parse | calcite_no_candidate_sql |
| PORT_0005 | calcite_parse_double_quote_identifier | parse | calcite_no_candidate_sql |
| PORT_0008 | calcite_parse_double_quote_identifier | parse | calcite_no_candidate_sql |
| PORT_0012 | calcite_parse_double_quote_identifier | parse | calcite_no_candidate_sql |
| PORT_0022 | calcite_parse_datetime_keyword_or_ddl_type | parse | calcite_no_candidate_sql |
| PORT_0025 | calcite_parse_datetime_keyword_or_ddl_type | parse | calcite_no_candidate_sql |

Main buckets:

- `calcite_parse_double_quote_identifier`: PostgreSQL/MySQL-style quoted identifier syntax was not accepted by the external Calcite parse path for four PORT rows.
- `calcite_parse_datetime_keyword_or_ddl_type`: `DATETIME` syntax/type handling blocked three PORT rows.

No failed row was silently dropped. Each row remains visible in `per_row_candidate_status.csv` with the stdout/stderr trace path under `/tmp`.
