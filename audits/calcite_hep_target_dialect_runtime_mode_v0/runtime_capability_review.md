# Runtime Capability Review

Prior capability:

- The external runtime accepted arbitrary `--key value` pairs but ignored target
  dialect.
- It hardcoded `PostgresqlSqlDialect.DEFAULT` for RelToSql and parse-only SQL
  emission.
- MySQL/Spark therefore received PostgreSQL-style double-quoted identifiers.

Staged capability:

- The external runtime now parses target dialect from `--engine`, with aliases
  also accepted for `--dialect` and `--target`.
- Supported values:
  - `postgres`, `postgresql`, `pg`
  - `mysql`
  - `spark`, `spark_sql`, `sparksql`
- Runtime emission dialects:
  - PostgreSQL: `PostgresqlSqlDialect.DEFAULT`
  - MySQL: `MysqlSqlDialect.DEFAULT`
  - Spark: `SparkSqlDialect.DEFAULT`

Direct runtime probe:

- `CONS_0036 --engine postgres` emitted PostgreSQL double-quoted identifiers.
- `CONS_0036 --engine mysql` emitted MySQL backtick identifiers and completed
  `calcite_rel_to_sql`.
- `CONS_0036 --engine spark` emitted Spark backtick identifiers. The simple DDL
  parser did not ingest Spark `STRING` DDL for this row, so the runtime fell
  back to `calcite_parse_only`, but emitted Spark-dialect SQL.

The runtime change was made outside this release repository under:

`/home/tianci_gao/.local/share/sqlrb/calcite_hep/src/CalciteHepRewriteSmoke.java`

Compiled classes were refreshed under the external runtime's local `classes/`
directory. No external runtime source, class, JAR, build, or cache artifact was
committed to this repository.
