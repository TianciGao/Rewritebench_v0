# Execution Checker Summary

Execution/checker policy:

- Execute/check `calcite_rel_to_sql` candidates.
- Exclude `calcite_parse_only_schema_fallback` candidates by default as `not_attempted_schema_fallback_policy`.
- Preserve no-candidate rows as `not_attempted_no_candidate`.

Summary:

| field | count |
| --- | ---: |
| generated_candidate_rows | 33 |
| schema_fallback_rows | 4 |
| schema_fallback_excluded_rows | 4 |
| execution_attempted_rows | 29 |
| source_executable_rows | 28 |
| candidate_executable_rows | 28 |
| checker_attempted_rows | 28 |
| exact_rows | 22 |
| mismatch_rows | 6 |
| source_execution_failed_rows | 1 |
| candidate_execution_failed_rows | 0 |

Exact rows newly gained versus pre-fix route card:

- `CONS_0011`
- `CONS_0037`

Rows newly reaching the checker after quote normalization:

- `CONS_0036`: checker mismatch, label-only with value-exact result.
- `CONS_0037`: checker exact.
- `LONGTAIL_0011`: checker mismatch.
- `LONGTAIL_0012`: checker mismatch.
- `LONGTAIL_0013`: checker mismatch.

Remaining source execution failure:

- `PORT_0024`
