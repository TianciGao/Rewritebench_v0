# Root Cause Analysis

## Current Runner Behavior

The current user-entry selection path builds each selected row with:

```text
source_sql_path = cases/{POOL}/{CASE_ID}/sql/source.sql
```

`resolve_case_package()` then requires manifest `sql.source` to match that selected `source_sql_path`. The PostgreSQL executor reads `row.source_sql_path` directly and builds `source_query.sql` from that file. There is no current engine-aware source SQL or dialect-variant selection for PostgreSQL.

## Case Metadata

For all five target cases, manifest metadata records the retained source dialect as `mysql_like_candidate`. The failing `source.sql` files contain MySQL-like backtick identifiers. Some also contain MySQL-oriented date/time or type syntax, including `DATE_FORMAT`, `CAST(... AS DATETIME)`, and `DOUBLE`.

Each case has a `sql/pos_01.sql` file that appears PostgreSQL-like. However, the manifests declare these files under `sql.positive_rewrites`, not as PostgreSQL source-oracle variants. Only `PORT_0004` and `PORT_0013` have a `sql.dialect_variants` section, and those entries are Spark-only.

## Failure Classification

The failures are reproducible in the targeted five-case run. They occur during source query execution after schema setup. The recorded failure bucket is `source_execution_failed`, and candidate execution/checker comparison are skipped.

This is best classified as:

- expected PORT dialect incompatibility for the retained MySQL-like source SQL under PostgreSQL, and
- a user-entry PostgreSQL diagnostic feature gap: the runner lacks an approved engine-aware source/dialect variant selection policy.

It is not best classified as a schema/setup issue because external PostgreSQL schema assets resolved and execution reached `source_query.sql`. It is not a method or rewriter-quality failure because the source oracle itself fails before candidate/checker evaluation.

## Safest Path

The next safe action is a narrow design task for engine-aware source/dialect variant selection. That design should decide whether PostgreSQL diagnostics can use `pos_01.sql` or another explicitly declared manifest path as a PostgreSQL source oracle for PORT cases. The design should also define fail-closed behavior when no approved engine-compatible source SQL exists.

No case SQL or manifests should be changed until the source-role and engine-variant policy is approved.

## Boundaries

- Local diagnostic triage only.
- No official metrics.
- No timing or speedup.
- No paper tables.
- No reports/results updates.
- No denominator changes.
- No case membership changes.
- No raw legacy evidence changes.
- No leaderboard.
