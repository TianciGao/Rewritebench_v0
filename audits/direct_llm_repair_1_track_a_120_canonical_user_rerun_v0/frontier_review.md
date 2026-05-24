# Frontier Review

Final non-exact / boundary frontier from the Repair-1 route ledger:

- unsupported_engine: 5
- no_candidate_sql: 0
- candidate_execution_failed: 0
- mismatch: 4
- checker_failed: 0
- fail_closed rows: 0
- timing-ineligible exact rows: 13

| case_id | engine | pool | failure_bucket | exact_status | timing_status | timing_na_reason |
| --- | --- | --- | --- | --- | --- | --- |
| PORT_0004 | mysql | PORT | mismatch | mismatch | not_eligible | checker_not_success |
| PORT_0013 | mysql | PORT | mismatch | mismatch | not_eligible | checker_not_success |
| PORT_0022 | mysql | PORT | mismatch | mismatch | not_eligible | checker_not_success |
| PORT_0024 | mysql | PORT | mismatch | mismatch | not_eligible | checker_not_success |
| PORT_0008 | spark | PORT | unsupported_engine | not_exact_due_to_execution_failure | not_eligible | unsupported_fail_closed |
| PORT_0012 | spark | PORT | unsupported_engine | not_exact_due_to_execution_failure | not_eligible | unsupported_fail_closed |
| PORT_0022 | spark | PORT | unsupported_engine | not_exact_due_to_execution_failure | not_eligible | unsupported_fail_closed |
| PORT_0024 | spark | PORT | unsupported_engine | not_exact_due_to_execution_failure | not_eligible | unsupported_fail_closed |
| PORT_0025 | spark | PORT | unsupported_engine | not_exact_due_to_execution_failure | not_eligible | unsupported_fail_closed |
