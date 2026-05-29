# Patch Summary

Files changed:

- `src/sql_rewrite_bench/candidate_preflight.py`
- `src/sql_rewrite_bench/spark_execution.py`
- `tests/user_entry/test_candidate_preflight.py`

## Candidate Preflight

`candidate_preflight.py` now exposes `split_sql_statements_comment_aware(sql)`. It splits SQL only on semicolons that are outside:

- `--` line comments
- `/* ... */` block comments
- single-quoted string literals
- double-quoted identifiers/literals
- backtick identifiers

Candidate preflight multi-statement detection now uses this shared splitter. Genuine multi-statement SQL remains rejected.

## Spark Execution

`spark_execution.py` now delegates `_split_sql_statements` to the shared preflight splitter. It still applies the existing Spark-path full-line `--` comment normalization before splitting because the previous Spark execution path already normalized those comments before sending SQL to Spark.

The patch does not strip block comments from SQL sent to Spark. It only prevents semicolons inside comments or quoted text from being treated as statement separators.

## Non-Changes

- SQLGlot adapter behavior changed: no.
- Checker normalization changed: no.
- Case SQL changed: no.
- Case manifests changed: no.
- Schema/checker/validation files changed: no.
- Reports/results changed: no.
- Official metrics/timing/leaderboard changed: no.
