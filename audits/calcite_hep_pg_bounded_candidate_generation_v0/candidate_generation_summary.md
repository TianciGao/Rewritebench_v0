# Candidate Generation Summary

Summary counts:

| metric | count |
| --- | --- |
| selected_rows | 40 |
| adapter_invoked_rows | 40 |
| adapter_exit_zero_rows | 40 |
| candidate_generated_rows | 33 |
| fail_closed_rows | 7 |

By pool:

| pool | selected | candidate_generated | fail_closed |
| --- | --- | --- | --- |
| CONS | 9 | 9 | 0 |
| LONGTAIL | 6 | 6 | 0 |
| PERF | 16 | 16 | 0 |
| PORT | 9 | 2 | 7 |

Failure bucket counts:

| failure_bucket | count |
| --- | --- |
| no_candidate_sql | 7 |
| none | 33 |

Calcite runtime status counts:

| runtime_status | count |
| --- | --- |
| calcite_invocation_succeeded | 33 |
| calcite_no_candidate_sql | 7 |

Emission mode counts:

| emission_mode | count |
| --- | --- |
| calcite_parse_only | 4 |
| calcite_rel_to_sql | 29 |
| failed | 7 |

The adapter exited `0` for all rows, including fail-closed no-candidate rows, so the user-entry ledger recorded route-level outcomes rather than adapter crashes.
