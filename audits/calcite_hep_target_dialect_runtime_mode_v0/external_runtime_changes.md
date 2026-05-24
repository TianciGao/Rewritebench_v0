# External Runtime Changes

External path changed outside the release repo:

`/home/tianci_gao/.local/share/sqlrb/calcite_hep/src/CalciteHepRewriteSmoke.java`

Change summary:

- Imported Calcite `SqlDialect`, `MysqlSqlDialect`, and `SparkSqlDialect`.
- Added a `TargetDialect` enum.
- Parsed target dialect from `--engine`, with fallback aliases `--dialect` and
  `--target`.
- Default target dialect remains PostgreSQL for backward compatibility.
- Passed the selected dialect to `RelToSqlConverter`.
- Used the selected dialect for `SqlNode.toSqlString(...)`.
- Printed `target_dialect=<dialect>` in runtime stdout.

External compile command:

```bash
javac -cp "$(cat /home/tianci_gao/.local/share/sqlrb/calcite_hep/classpath.txt)" \
  -d /home/tianci_gao/.local/share/sqlrb/calcite_hep/classes \
  /home/tianci_gao/.local/share/sqlrb/calcite_hep/src/CalciteHepRewriteSmoke.java
```

No external files were staged or committed. The repository commit only records
the adapter contract, tests, docs, audit packet, and project-control writeback.
