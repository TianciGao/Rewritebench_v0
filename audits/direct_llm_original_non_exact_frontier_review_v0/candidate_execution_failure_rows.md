# Candidate Execution Failure Rows

These 3 rows generated candidates and the source SQL executed, but the candidate SQL failed before checker comparison. Repair-1 should attempt these rows with candidate execution feedback.

| case_id | pool | engine | source_executable | candidate_executable | exact | failure bucket | likely feedback type | attempt |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CONS_0009 | CONS | spark | true | false | false | candidate_execution_failed | candidate_execution_error_feedback | yes |
| CONS_0011 | CONS | spark | true | false | false | candidate_execution_failed | candidate_execution_error_feedback | yes |
| LONGTAIL_0012 | LONGTAIL | spark | true | false | false | candidate_execution_failed | candidate_execution_error_feedback | yes |

Required Repair-1 feedback fields for this bucket:

- `source_executable=true`
- `candidate_executable=false`
- `checker_attempted=false`
- `failure_bucket=candidate_execution_failed`
- normalized candidate execution error class/message summary, without credentials or raw provider response bodies
- original candidate SQL and candidate SQL hash from the Direct LLM original run
