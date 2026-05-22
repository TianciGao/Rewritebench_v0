# Common-core SQLGlot Noop Failure Triage

Verdict: `completed`

This audit triages the fail-visible rows from `common_core_tri_engine_sqlglot_noop_local_diagnostic_snapshot_v0`. No benchmark code, SQLGlot adapter behavior, checker behavior, case package, schema, SQL, or manifest was changed.

The triage inspected the existing local artifacts under:

- `runs/user/common_core_sqlglot_noop_postgres_snapshot`
- `runs/user/common_core_sqlglot_noop_mysql_snapshot`
- `runs/user/common_core_sqlglot_noop_spark_snapshot`

## Classification Summary

PostgreSQL fail-visible rows are all PORT adapter parse failures before candidate generation:

- `PORT_0004`, `PORT_0013`, `PORT_0022`, `PORT_0024`, `PORT_0025`
- Class: SQLGlot parse/emit failure and PORT real-adapter limitation.
- Execution/checker were not attempted because no candidate SQL was generated.

MySQL fail-visible rows split into three groups:

- `PORT_0008`: candidate execution syntax failure caused by emitted single-quoted identifier paths such as `'t2'.'admemail1'`.
- `PORT_0003`, `PORT_0005`, `PORT_0012`: real PORT adapter semantic limitations; emitted single-quoted identifiers/literals executed but returned literal or null values instead of source-reference values.
- `PERF_0062`, `PORT_0004`, `PORT_0013`, `PORT_0022`, `PORT_0024`: checker/normalization gap candidates where source and candidate row values matched positionally but generated expression column labels differed.

Spark fail-visible rows split into four groups:

- `PERF_0008`, `PERF_0013`, `PERF_0017`, `PERF_0019`, `PERF_0024`, `PERF_0082`: same-engine candidate execution failures with `Spark diagnostic query must contain exactly one statement`; source execution succeeded and candidate preflight passed, so this is a Spark candidate execution / preflight-backend investigation candidate.
- `PORT_0003`, `PORT_0013`: PORT target candidate execution failures caused by emitted SQL that is not Spark-compatible or treats identifiers as string literals.
- `PORT_0004`, `PORT_0005`: PORT real-adapter checker mismatches with value differences, not simple normalization-only differences.
- `PORT_0008`, `PORT_0012`, `PORT_0022`, `PORT_0024`, `PORT_0025`: expected manifest-driven unsupported/fail-closed rows.

## Boundary

This is diagnosis only. It does not run SQLGlot optimize, rerun Common-core, patch SQLGlot, patch the checker, patch engine backends, run timing, compute speedup, compute official metrics, update reports/results, promote retained evidence, or create leaderboard output.

## Recommendation

Keep all rows fail-visible for now. Separately authorize narrow follow-ups only if desired:

- a SQLGlot noop PORT route/documentation triage for parse failures and literal-identifier emissions;
- a same-engine checker column-label policy triage for rows where values are equal but expression labels differ;
- a Spark candidate statement-handling/preflight investigation for same-engine rows rejected as not exactly one statement.
