# Schema Payload Review

Schema source: case resolver schema artifacts exposed to the adapter through the D035 user facade. The adapter derived LearnedRewrite HTTP `schema` payloads from PostgreSQL DDL; no schema file was mutated.

Payload shape: JSON-array string passed as the `schema` field to `/rewriter`, with entries shaped as table objects containing `table`, `rows`, and `columns`.

Schema payload statuses:

| status | count |
| --- | ---: |
| ddl_derived_schema_json | 40 |

DDL-derived schema table count distribution:

| table_count | rows |
| ---: | ---: |
| 1 | 9 |
| 2 | 13 |
| 3 | 7 |
| 4 | 5 |
| 5 | 3 |
| 6 | 3 |

Rows with schema serialization issues: none.

Limitations:

- The serialization is conservative PostgreSQL DDL parsing, not a full SQL dialect model.
- Constraint, data distribution, row-count, and advanced type modeling remain approximate for LearnedRewrite runtime compatibility.
- PostgreSQL-only scope was used; MySQL/Spark dialect payloads were not attempted.
