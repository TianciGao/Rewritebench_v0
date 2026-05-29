# Failure Bucket Review

Failure bucket counts:

| failure_bucket | count |
| --- | --- |
| candidate_execution_failed | 8 |
| mismatch | 3 |
| no_candidate_sql | 7 |
| none | 20 |
| source_execution_failed | 2 |


## source_execution_failed

| case_id | candidate_origin | execution_error | source_status | candidate_status | checker_status |
| --- | --- | --- | --- | --- | --- |
| PORT_0013 | calcite_parse_only_schema_fallback | source_execution_failed | source_execution_failed | execution_not_enabled | not_attempted |
| PORT_0024 | calcite_rel_to_sql | source_execution_failed | source_execution_failed | execution_not_enabled | not_attempted |
## candidate_execution_failed

| case_id | candidate_origin | execution_error | source_status | candidate_status | checker_status |
| --- | --- | --- | --- | --- | --- |
| CONS_0036 | calcite_rel_to_sql | candidate_execution_failed | source_execution_success | candidate_execution_failed | not_attempted |
| CONS_0037 | calcite_rel_to_sql | candidate_execution_failed | source_execution_success | candidate_execution_failed | not_attempted |
| LONGTAIL_0011 | calcite_rel_to_sql | candidate_execution_failed | source_execution_success | candidate_execution_failed | not_attempted |
| LONGTAIL_0012 | calcite_rel_to_sql | candidate_execution_failed | source_execution_success | candidate_execution_failed | not_attempted |
| LONGTAIL_0013 | calcite_rel_to_sql | candidate_execution_failed | source_execution_success | candidate_execution_failed | not_attempted |
| LONGTAIL_0022 | calcite_parse_only_schema_fallback | candidate_execution_failed | source_execution_success | candidate_execution_failed | not_attempted |
| LONGTAIL_0023 | calcite_parse_only_schema_fallback | candidate_execution_failed | source_execution_success | candidate_execution_failed | not_attempted |
| LONGTAIL_0024 | calcite_parse_only_schema_fallback | candidate_execution_failed | source_execution_success | candidate_execution_failed | not_attempted |
## mismatch

| case_id | candidate_origin | execution_error | source_status | candidate_status | checker_status |
| --- | --- | --- | --- | --- | --- |
| PERF_0035 | calcite_rel_to_sql |  | source_execution_success | candidate_execution_success | checker_mismatch |
| PERF_0062 | calcite_rel_to_sql |  | source_execution_success | candidate_execution_success | checker_mismatch |
| CONS_0011 | calcite_rel_to_sql |  | source_execution_success | candidate_execution_success | checker_mismatch |
## no_candidate_sql

| case_id | candidate_origin | execution_error | source_status | candidate_status | checker_status |
| --- | --- | --- | --- | --- | --- |
| PORT_0003 | no_candidate |  | not_attempted | not_attempted | not_attempted |
| PORT_0004 | no_candidate |  | not_attempted | not_attempted | not_attempted |
| PORT_0005 | no_candidate |  | not_attempted | not_attempted | not_attempted |
| PORT_0008 | no_candidate |  | not_attempted | not_attempted | not_attempted |
| PORT_0012 | no_candidate |  | not_attempted | not_attempted | not_attempted |
| PORT_0022 | no_candidate |  | not_attempted | not_attempted | not_attempted |
| PORT_0025 | no_candidate |  | not_attempted | not_attempted | not_attempted |

Mismatch notes:

- `CONS_0011` is a label-only mismatch under the strict local checker: values match but labels differ by case.
- `PERF_0035` and `PERF_0062` are column-count/shape mismatches in the local checker output.

Execution failure notes:

- `CONS_0036`, `CONS_0037`, and several LONGTAIL rows failed candidate execution due quoted mixed-case identifiers such as `"DEPT"`, `"EMP"`, `"Posts"`, or `"Comments"` not matching PostgreSQL-loaded relation names.
- `PORT_0013` and `PORT_0024` failed PostgreSQL source execution because their source SQL uses backtick-style syntax in this PostgreSQL-only pass.
