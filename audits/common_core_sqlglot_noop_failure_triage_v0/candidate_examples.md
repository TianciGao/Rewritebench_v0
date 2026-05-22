# Candidate Examples

This file records representative evidence from local run artifacts. It is not a rerun and not official evidence.

## PostgreSQL Adapter Parse Failures

The PostgreSQL fail-visible rows failed before candidate generation. Example from `PORT_0004`:

```text
error: SQLGlot parse failed: Expected END after CASE
```

Example from `PORT_0025`:

```text
error: SQLGlot parse failed: Invalid expression / Unexpected token
```

No candidate SQL, DB execution, or checker comparison was produced for these rows.

## MySQL Invalid Target Candidate

`PORT_0008` generated target SQL with single-quoted identifier paths:

```sql
SELECT 't2'.'admemail1', 't2'.'admemail2'
```

MySQL rejected that syntax during candidate execution.

## MySQL Literalized Identifier Mismatches

`PORT_0003` executed but returned a literal:

```sql
SELECT 'gsoffered' FROM `schools`
```

The candidate result was `gsoffered`; the source-reference result was `north-max`.

`PORT_0005` similarly returned `nationality` instead of `japan_earliest`.

## MySQL Label-only Checker Mismatch

`PERF_0062` source and candidate values matched positionally, but labels differed:

```text
source labels: avg(...), sum(...)
candidate labels: AVG(...), SUM(...)
```

The same label-only pattern appeared for `PORT_0004`, `PORT_0013`, `PORT_0022`, and `PORT_0024`, where values matched but generated expression labels differed by formatting.

## Spark Same-engine Candidate Execution Failures

For `PERF_0008`, `PERF_0013`, `PERF_0017`, `PERF_0019`, `PERF_0024`, and `PERF_0082`, candidate preflight passed and source execution succeeded, but Spark candidate execution failed with:

```text
Spark diagnostic query must contain exactly one statement
```

The candidate files preserve SQLGlot-emitted block comments plus the query. This is a candidate execution / Spark statement-handling investigation candidate, not a checker mismatch.

## Spark PORT Candidate Failures and Mismatches

`PORT_0003` emitted:

```sql
ORDER BY ABS('longitude') DESC
```

Spark attempted to cast the literal string `longitude` to `DOUBLE` and failed.

`PORT_0013` emitted a boolean aggregate:

```sql
SUM(`t2`.`gender` = 'F')
```

Spark rejected `SUM(boolean)` as a datatype mismatch.

`PORT_0004` executed but returned `NULL` while the source-reference result was `50`.

`PORT_0005` executed but returned literal `nationality` while the source-reference result was `japan_earliest`.
