# Blocker Summary

Frontier bucket counts:

| bucket | count |
| --- | ---: |
| no_candidate_sql | 7 |
| mismatch | 3 |
| source_execution_failed | 2 |
| candidate_execution_failed | 8 |

Primary category counts:

| category | count |
| --- | ---: |
| calcite_identifier_quoting_blocker | 9 |
| datetime_timestamp_syntax_or_type_blocker | 3 |
| port_source_dialect_not_pg_executable | 2 |
| calcite_generated_candidate_semantic_mismatch | 3 |
| schema_fallback_candidate_failed | 3 |

Schema fallback rows are 4 total. `PORT_0013` is counted primarily as a PORT source-dialect failure because source execution failed before candidate execution could be evaluated, but it is still a schema-fallback row for policy purposes.

Main blocker themes:

- Identifier quoting / mixed-case relation names are the largest direct fix candidate.
- DATETIME/TIMESTAMP/schema-ingestion support blocks no-candidate and fallback rows.
- PORT source-role handling needs a policy boundary before broader engine expansion.
- Mismatch rows need manual semantic review before promotion.
