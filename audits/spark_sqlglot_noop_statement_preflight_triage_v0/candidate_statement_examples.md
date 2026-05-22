# Candidate Statement Examples

The examples below are excerpts from existing local artifacts under `runs/user/common_core_sqlglot_noop_spark_snapshot/`. They are not retained evidence and were not committed.

## Common Shape

Each affected candidate has this shape:

```sql
/* source metadata comment with semicolons */ SELECT ...;
```

The source artifacts have the same metadata content as full-line `--` comments. Spark source execution succeeded because the Spark splitter removes lines that begin with `--` before scanning for semicolons. SQLGlot noop emits those comments as `/* ... */` block comments, and the Spark splitter does not currently skip block comments.

## PERF_0008

Candidate excerpt:

```sql
/* PERF_0008 source layer */ /* Source registry row: SRC_001 (TPC-H) */ /* Raw source file: datasets/raw/tpch/TPC-H V3.0.1/dbgen/queries/3.sql */ /* Seed: TPC-H Query 3, Shipping Priority Query */ /* Freeze method: manual freeze because local qgen executable was not present. */ /* Reference substitution file: datasets/raw/tpch/TPC-H V3.0.1/ref_data/1/subparam_3 */ /* Substitutions: :1 = MACHINERY; :2 = 1995-03-27; :n 10 = LIMIT 10. */ SELECT ...
```

Statement-boundary observation: three raw semicolons, one semicolon outside comments, Spark splitter returned three fragments.

## PERF_0013

Candidate excerpt:

```sql
/* PERF_0013 source layer */ /* Source registry row: SRC_001 (TPC-H) */ /* Raw source file: datasets/raw/tpch/TPC-H V3.0.1/dbgen/queries/5.sql */ /* Seed: TPC-H Query 5, Local Supplier Volume Query */ /* Freeze method: manual freeze because local qgen executable was not present. */ /* Reference substitution file: datasets/raw/tpch/TPC-H V3.0.1/ref_data/1/subparam_5 */ /* Substitutions: :1 = MIDDLE EAST; :2 = 1997-01-01; :n -1 = no row limit. */ SELECT ...
```

Statement-boundary observation: three raw semicolons, one semicolon outside comments, Spark splitter returned three fragments.

## PERF_0017

Candidate excerpt:

```sql
/* PERF_0017 source layer */ /* Source registry row: SRC_001 (TPC-H) */ /* Raw source file: datasets/raw/tpch/TPC-H V3.0.1/dbgen/queries/10.sql */ /* Seed: TPC-H Query 10, Returned Item Reporting Query */ /* Freeze method: manual freeze because local qgen executable was not used for this batch. */ /* Reference substitution file: datasets/raw/tpch/TPC-H V3.0.1/ref_data/1/subparam_10 */ /* Substitutions: :1 = 1993-11-01; :n 20 = LIMIT 20. */ SELECT ...
```

Statement-boundary observation: two raw semicolons, one semicolon outside comments, Spark splitter returned two fragments.

## PERF_0019

Candidate excerpt:

```sql
/* PERF_0019 source layer */ /* Source registry row: SRC_001 (TPC-H) */ /* Raw source file: datasets/raw/tpch/TPC-H V3.0.1/dbgen/queries/13.sql */ /* Seed: TPC-H Query 13, Customer Distribution Query */ /* Freeze method: manual freeze because local qgen executable was not used for this batch. */ /* Reference substitution file: datasets/raw/tpch/TPC-H V3.0.1/ref_data/1/subparam_13 */ /* Substitutions: :1 = express; :2 = deposits; :n -1 = no row limit. */ SELECT ...
```

Statement-boundary observation: three raw semicolons, one semicolon outside comments, Spark splitter returned three fragments.

## PERF_0024

Candidate excerpt:

```sql
/* PERF_0024 source query. */ /* TPC-H Q20 frozen from ref_data/1/subparam_20. */ /* Substitutions: :1 = 'pale'; :2 = DATE '1997-01-01'; :3 = 'BRAZIL'; :n = -1. */ SELECT s_name, s_address FROM supplier ...
```

Statement-boundary observation: four raw semicolons, one semicolon outside comments, Spark splitter returned four fragments.

## PERF_0082

Candidate excerpt:

```sql
/* draft_id: JOB_DRAFT_0005 */ /* original local source path redacted during public migration; see metadata/provenance.yaml for retained legacy mapping. */ /* not official case */ SELECT MIN(t.title) AS typical_european_movie FROM ...
```

Statement-boundary observation: two raw semicolons, one semicolon outside comments, Spark splitter returned two fragments.

## Diagnostic Stripping Result

A comment-aware statement-boundary scan sees one semicolon outside comments for each candidate. After ignoring comments and treating the final trailing semicolon as a terminator, each affected candidate is a single SQL statement for boundary-check purposes. This audit did not execute stripped candidates against Spark.
