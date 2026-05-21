# Root Cause Analysis

The targeted rerun reproduced four failures at the MySQL source query execution stage. Schema setup and load were not the failing stage: MySQL DDL/load assets are present through the current external schema profiles, and the backend reached `source.sql` execution before failing. Candidate execution and checker handoff did not run because the source side failed first.

The failing `source.sql` files are PostgreSQL-like. `PORT_0003` and `PORT_0005` use double-quoted identifiers plus PostgreSQL `NULLS LAST` or `NULLS FIRST` ordering. `PORT_0008` uses double-quoted identifiers and PostgreSQL expression forms. `PORT_0012` uses double-quoted identifiers and PostgreSQL date/numeric formatting functions. These files are not MySQL-compatible in isolation.

The legacy branch was used as a read-only reference. For all four cases, the legacy branch records `source_dialect: postgres_like_candidate` and retained PostgreSQL source output under `runs/pg/source.tsv`. It also records retained MySQL target-positive output under `runs/mysql/rewrite_pos_01.tsv`. No legacy `runs/mysql/source.tsv` artifact was found for these cases.

Therefore, old retained evidence suggests a legacy role mapping gap rather than a schema/load/backend export gap. The old path appears to have validated cross-dialect equivalence from PostgreSQL source reference to MySQL positive rewrite. The new `--engine mysql` same-engine diagnostic attempts direct MySQL execution of `source.sql`, which is a different route.

This audit does not prove a real semantic failure in the case SQL. It identifies that the current local diagnostic route is asking MySQL to execute a PostgreSQL-like source file for these four PORT cases. A future fix should first clarify role metadata and runner routing for PostgreSQL-source to MySQL-target PORT diagnostics.

This is not official metrics or paper evidence. The rerun is a bounded local diagnostic and does not compute timing, speedup, denominator values, paper tables, reports/results outputs, retained-evidence promotion, or leaderboard data.
