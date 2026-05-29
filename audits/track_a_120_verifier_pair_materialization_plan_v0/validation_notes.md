# Validation Notes

Validation status is recorded after checks run.

| check | result |
| --- | --- |
| CSV parse checks | passed; three generated CSV files parsed |
| Markdown non-empty checks | passed; Markdown and text audit files are non-empty |
| source path existence checks | passed for all eligible manifest rows |
| candidate SQL path existence checks | passed for all eligible manifest rows |
| hash generation checks | passed; SHA256 fields are present and match source/candidate file contents |
| pair count sanity against inventory estimates | passed; eligible counts are `direct_llm_original=102`, `sqlglot_noop=97`, `sqlglot_optimize_schema_aware=66`, `calcite_hep_fail_closed=81` |
| no-prohibited-command check | passed |
| no primary metric recomputed or changed | passed; no local metrics command or metric output path was written |
| no official metric computed | passed |
| protected-path review | passed |
| changed-file secret scan | passed |
| `git diff --check` | passed |
| staged-file secret scan | passed |
| staged protected-path review | passed |
