# Targeted Validation Summary

Runtime root: `/tmp/sqlrb_calcite_hep_pg_identifier_quoting_fix_v0/`.

Validation command invoked the Calcite adapter for the 9 identifier-quoting rows and ran PostgreSQL execution/checker only for rows with generated candidate SQL.

Summary:

| metric | count |
| --- | ---: |
| target_rows | 9 |
| after_candidate_generated_rows | 5 |
| after_source_executable_rows | 5 |
| after_candidate_executable_rows | 5 |
| after_exact_rows | 1 |
| improved_to_exact_rows | 1 |
| improved_to_candidate_executable_rows | 4 |
| unchanged_no_candidate_rows | 4 |
| regressed_rows | 0 |

Per-row outcome:

| case_id | after status |
| --- | --- |
| PORT_0003 | unchanged `no_candidate_sql` |
| PORT_0005 | unchanged `no_candidate_sql` |
| PORT_0008 | unchanged `no_candidate_sql` |
| PORT_0012 | unchanged `no_candidate_sql` |
| CONS_0036 | candidate now executes; checker mismatch is label-only with value-exact result |
| CONS_0037 | candidate now executes and checker is exact |
| LONGTAIL_0011 | candidate now executes; checker value mismatch remains |
| LONGTAIL_0012 | candidate now executes; checker value mismatch remains |
| LONGTAIL_0013 | candidate now executes; checker value mismatch remains |

No timing was collected. No verifier was run. No official metric was computed.
