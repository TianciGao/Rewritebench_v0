# Semantic Mismatch Rows

These 10 rows generated candidates and both source and candidate SQL executed, but the local checker found non-exact results. Repair-1 should attempt these rows with checker mismatch feedback.

| case_id | pool | engine | source_executable | candidate_executable | exact | failure bucket | likely feedback type | attempt |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CONS_0005 | CONS | postgres | true | true | false | mismatch | checker_mismatch_feedback | yes |
| PERF_0062 | PERF | mysql | true | true | false | mismatch | checker_mismatch_feedback | yes |
| CONS_0005 | CONS | mysql | true | true | false | mismatch | checker_mismatch_feedback | yes |
| CONS_0037 | CONS | mysql | true | true | false | mismatch | checker_mismatch_feedback | yes |
| PORT_0004 | PORT | mysql | true | true | false | mismatch | checker_mismatch_feedback | yes |
| PORT_0012 | PORT | mysql | true | true | false | mismatch | checker_mismatch_feedback | yes |
| PORT_0013 | PORT | mysql | true | true | false | mismatch | checker_mismatch_feedback | yes |
| PORT_0022 | PORT | mysql | true | true | false | mismatch | checker_mismatch_feedback | yes |
| PORT_0024 | PORT | mysql | true | true | false | mismatch | checker_mismatch_feedback | yes |
| CONS_0005 | CONS | spark | true | true | false | mismatch | checker_mismatch_feedback | yes |

Required Repair-1 feedback fields for this bucket:

- `checker_attempted=true`
- `exact_status=mismatch`
- `failure_bucket=mismatch`
- mismatch summary from the local checker, without raw secrets or provider response bodies
- original candidate SQL and candidate SQL hash from the Direct LLM original run
