# Source Generation Input Review

Input audit:
- `audits/sqlglot_optimize_schema_aware_route_design_fix_v0/`

The input route-design audit established:
- separate route id `sqlglot_optimize_schema_aware`;
- existing context-free `sqlglot_optimize` preserved;
- per-engine DDL resolution from case metadata;
- DDL-derived SQLGlot schema map;
- generation/preflight smoke over the same 9 rows with 9/9 candidates and 9/9 preflight passed.

This execution/checker diagnostic regenerated the same bounded row set through the current adapter rather than reusing committed runtime candidates. Runtime candidates were written under `/tmp` only.

Schema context:
- `CONS_0005`: `schemas/calcite_core_sql_tests_cons0005_v0/<engine>/ddl.sql`
- `PERF_0006`: `schemas/tpch_common_core_v0/<engine>/ddl.sql`
- `CONS_0036`: `schemas/verieql_cons0036_v0/<engine>/ddl.sql`

Local engine environment:
- PostgreSQL probe succeeded through existing libpq configuration.
- MySQL probe succeeded through existing `SQLRB_MYSQL_*` configuration.
- Spark PySpark backend was available through existing Spark local diagnostic configuration.
