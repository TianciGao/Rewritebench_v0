# Source/Candidate SQL Excerpt Review

This review includes only timing-tail, frontier, and true source-like diagnostic selections from `timing_tail_case_selection.csv`. SQL is excerpted and not reproduced in full.

## learnedrewrite / CONS_0005

- Selection types: `key_frontier_row`
- Failure bucket(s): `mismatch`
- Speedup ratio(s): `N.A.`
- Source-like classification: `nontrivial_or_changed`
- Visible structural note: candidate differs from source after simple whitespace/comment/case normalization; inspect full local files for exact structure.
- Source path: `cases/CONS/CONS_0005/sql/source.sql`
- Candidate path: `runs/user/learnedrewrite_pg40_manual_inspection_rerun_v0/candidate_sql/CONS_0005__postgres.sql`

Source excerpt:

```sql
SELECT i, j FROM table1 WHERE table1.j NOT IN ( SELECT i FROM table2 WHERE table1.i = table2.j );
```

Candidate excerpt:

```sql
SELECT "t7"."i", "t7"."j" FROM (SELECT "i", "j", "j" AS "j0" FROM "table1") AS "t7" LEFT JOIN (SELECT "i", "j", TRUE AS "$f1" FROM "table2") AS "t8" ON "t7"."i" = "t8"."j" AND "t7"."j0" = "t8"."i" WHERE "t8"."$f1" IS NOT TRUE;
```

## learnedrewrite / CONS_0007

- Selection types: `key_frontier_row`
- Failure bucket(s): `mismatch`
- Speedup ratio(s): `N.A.`
- Source-like classification: `nontrivial_or_changed`
- Visible structural note: candidate differs from source after simple whitespace/comment/case normalization; inspect full local files for exact structure.
- Source path: `cases/CONS/CONS_0007/sql/source.sql`
- Candidate path: `runs/user/learnedrewrite_pg40_manual_inspection_rerun_v0/candidate_sql/CONS_0007__postgres.sql`

Source excerpt:

```sql
SELECT * FROM tmp_emps e1 WHERE EXISTS ( SELECT * FROM ( SELECT e2.deptno FROM tmp_emps e2 WHERE e2.commission = e1.commission ) AS table3 WHERE table3.deptno <> e1.deptno );
```

Candidate excerpt:

```sql
SELECT "tmp_emps2"."empid", "tmp_emps2"."deptno", "tmp_emps2"."name", "tmp_emps2"."salary", "tmp_emps2"."commission" FROM "tmp_emps" AS "tmp_emps2" INNER JOIN (SELECT "t6"."deptno" AS "deptno0", "t5"."commission", TRUE AS "$f0" FROM (SELECT "deptno", "commission" FROM "tmp_emp...
```

## learnedrewrite / CONS_0009

- Selection types: `key_frontier_row`
- Failure bucket(s): `no_candidate_sql`
- Speedup ratio(s): `N.A.`
- Source-like classification: `no_candidate`
- Visible structural note: candidate missing; no structural SQL comparison available.
- Source path: `cases/CONS/CONS_0009/sql/source.sql`
- Candidate path: `N.A.`

Source excerpt:

```sql
SELECT * FROM t0 WHERE t0a < ( SELECT SUM(c) FROM ( SELECT t1c AS c FROM t1 WHERE t1a = t0a UNION ALL SELECT t2c AS c FROM t2 WHERE t2b = t0b ) AS tmp );
```

Candidate excerpt:

```sql
N.A.
```

## learnedrewrite / CONS_0010

- Selection types: `key_frontier_row`
- Failure bucket(s): `mismatch`
- Speedup ratio(s): `N.A.`
- Source-like classification: `nontrivial_or_changed`
- Visible structural note: candidate differs from source after simple whitespace/comment/case normalization; inspect full local files for exact structure.
- Source path: `cases/CONS/CONS_0010/sql/source.sql`
- Candidate path: `runs/user/learnedrewrite_pg40_manual_inspection_rerun_v0/candidate_sql/CONS_0010__postgres.sql`

Source excerpt:

```sql
SELECT E1.* FROM emp E1 WHERE NOT EXISTS ( SELECT 1 FROM emp E2 JOIN bonus B ON E2.SAL = E1.SAL AND B.JOB = E1.JOB WHERE E2.EMPNO <> E1.EMPNO );
```

Candidate excerpt:

```sql
SELECT "emp5"."empno", "emp5"."ename", "emp5"."job", "emp5"."mgr", "emp5"."hiredate", "emp5"."sal", "emp5"."comm", "emp5"."deptno" FROM "emp" AS "emp5" LEFT JOIN (SELECT "t8"."empno" AS "empno0", "bonus1"."job" AS "job0", "t8"."sal" AS "sal0", TRUE AS "$f0" FROM "emp" AS "emp6...
```

## learnedrewrite / CONS_0011

- Selection types: `key_frontier_row`
- Failure bucket(s): `mismatch`
- Speedup ratio(s): `N.A.`
- Source-like classification: `nontrivial_or_changed`
- Visible structural note: candidate differs from source after simple whitespace/comment/case normalization; inspect full local files for exact structure.
- Source path: `cases/CONS/CONS_0011/sql/source.sql`
- Candidate path: `runs/user/learnedrewrite_pg40_manual_inspection_rerun_v0/candidate_sql/CONS_0011__postgres.sql`

Source excerpt:

```sql
SELECT E1.ENAME FROM emp E1 WHERE EXISTS ( SELECT 1 FROM dept D LEFT JOIN bonus B ON D.DNAME = B.ENAME AND B.JOB = E1.JOB WHERE B.ENAME IS NULL );
```

Candidate excerpt:

```sql
SELECT "emp1"."ename" AS "ENAME" FROM "emp" AS "emp1" INNER JOIN (SELECT "bonus1"."job", TRUE AS "$f0" FROM "dept" AS "dept1" LEFT JOIN "bonus" AS "bonus1" ON "dept1"."dname" = "bonus1"."ename" WHERE "bonus1"."ename" IS NULL) AS "t9" ON "emp1"."job" = "t9"."job";
```

## learnedrewrite / CONS_0012

- Selection types: `key_frontier_row`
- Failure bucket(s): `no_candidate_sql`
- Speedup ratio(s): `N.A.`
- Source-like classification: `no_candidate`
- Visible structural note: candidate missing; no structural SQL comparison available.
- Source path: `cases/CONS/CONS_0012/sql/source.sql`
- Candidate path: `N.A.`

Source excerpt:

```sql
SELECT * FROM dept d WHERE EXISTS ( SELECT * FROM emp e WHERE e.deptno = d.deptno LIMIT 1 OFFSET 2 );
```

Candidate excerpt:

```sql
N.A.
```

## learnedrewrite / CONS_0024

- Selection types: `key_frontier_row`
- Failure bucket(s): `no_candidate_sql`
- Speedup ratio(s): `N.A.`
- Source-like classification: `no_candidate`
- Visible structural note: candidate missing; no structural SQL comparison available.
- Source path: `cases/CONS/CONS_0024/sql/source.sql`
- Candidate path: `N.A.`

Source excerpt:

```sql
SELECT empno FROM emp AS e LEFT JOIN dept AS d ON d.deptno = e.deptno AND EXISTS ( SELECT e2.deptno FROM emp AS e2 WHERE e2.deptno = d.deptno GROUP BY e2.deptno HAVING SUM(e2.sal) > 1000000 );
```

Candidate excerpt:

```sql
N.A.
```

## learnedrewrite / CONS_0036

- Selection types: `p90_near; source_like_row`
- Failure bucket(s): `none`
- Speedup ratio(s): `1.7050299297252396`
- Source-like classification: `source_like`
- Visible structural note: normalized candidate matches the source SQL; diagnostic source-like/no-op behavior.
- Source path: `cases/CONS/CONS_0036/sql/source.sql`
- Candidate path: `runs/user/learnedrewrite_pg40_manual_inspection_rerun_v0/candidate_sql/CONS_0036__postgres.sql`

Source excerpt:

```sql
SELECT NAME AS NAME, COUNT(*) AS C FROM DEPT GROUP BY NAME HAVING NAME = 'Charlie'
```

Candidate excerpt:

```sql
SELECT NAME AS NAME, COUNT(*) AS C FROM DEPT GROUP BY NAME HAVING NAME = 'Charlie';
```

## learnedrewrite / CONS_0037

- Selection types: `source_like_row`
- Failure bucket(s): `none`
- Speedup ratio(s): `0.9420492818192759`
- Source-like classification: `source_like`
- Visible structural note: normalized candidate matches the source SQL; diagnostic source-like/no-op behavior.
- Source path: `cases/CONS/CONS_0037/sql/source.sql`
- Candidate path: `runs/user/learnedrewrite_pg40_manual_inspection_rerun_v0/candidate_sql/CONS_0037__postgres.sql`

Source excerpt:

```sql
SELECT EMP.DEPTNO, COUNT(DISTINCT DEPT.NAME) FROM EMP LEFT JOIN DEPT ON EMP.DEPTNO = DEPT.DEPTNO GROUP BY EMP.DEPTNO
```

Candidate excerpt:

```sql
SELECT EMP.DEPTNO, COUNT(DISTINCT DEPT.NAME) FROM EMP LEFT JOIN DEPT ON EMP.DEPTNO = DEPT.DEPTNO GROUP BY EMP.DEPTNO;
```

## learnedrewrite / LONGTAIL_0011

- Selection types: `key_frontier_row`
- Failure bucket(s): `candidate_execution_failed`
- Speedup ratio(s): `N.A.`
- Source-like classification: `nontrivial_or_changed`
- Visible structural note: candidate differs from source after simple whitespace/comment/case normalization; inspect full local files for exact structure.
- Source path: `cases/LONGTAIL/LONGTAIL_0011/sql/source.sql`
- Candidate path: `runs/user/learnedrewrite_pg40_manual_inspection_rerun_v0/candidate_sql/LONGTAIL_0011__postgres.sql`

Source excerpt:

```sql
WITH RankedPosts AS ( SELECT p.Id, p.Title, p.CreationDate, p.Score, p.ViewCount, u.DisplayName AS OwnerDisplayName, DENSE_RANK() OVER (PARTITION BY p.OwnerUserId ORDER BY p.Score DESC) AS PostRank FROM Posts p JOIN Users u ON p.OwnerUserId = u.Id WHERE p.PostTypeId = 1 AND p....
```

Candidate excerpt:

```sql
SELECT "t84"."Title", "t84"."CreationDate", "t84"."Score", "t84"."ViewCount", "t84"."OwnerDisplayName" FROM (SELECT "t83"."Id", "t83"."Title", "t83"."CreationDate", "t83"."Score", "t83"."ViewCount", "Users19"."DisplayName" AS "OwnerDisplayName", DENSE_RANK() OVER (PARTITION BY...
```

## learnedrewrite / LONGTAIL_0012

- Selection types: `key_frontier_row`
- Failure bucket(s): `candidate_execution_failed`
- Speedup ratio(s): `N.A.`
- Source-like classification: `nontrivial_or_changed`
- Visible structural note: candidate differs from source after simple whitespace/comment/case normalization; inspect full local files for exact structure.
- Source path: `cases/LONGTAIL/LONGTAIL_0012/sql/source.sql`
- Candidate path: `runs/user/learnedrewrite_pg40_manual_inspection_rerun_v0/candidate_sql/LONGTAIL_0012__postgres.sql`

Source excerpt:

```sql
SELECT u.DisplayName AS UserName, COUNT(DISTINCT p.Id) AS TotalPosts, SUM(CASE WHEN p.PostTypeId = 1 THEN 1 ELSE 0 END) AS TotalQuestions, SUM(CASE WHEN p.PostTypeId = 2 THEN 1 ELSE 0 END) AS TotalAnswers, p.Title AS LastPostTitle, MAX(p.CreationDate) AS LastPostDate, AVG(COAL...
```

Candidate excerpt:

```sql
SELECT "t77"."DisplayName" AS "UserName", COUNT(DISTINCT "Posts8"."Id") AS "TotalPosts", SUM(CASE WHEN "Posts8"."PostTypeId" = 1 THEN 1 ELSE 0 END) AS "TotalQuestions", SUM(CASE WHEN "Posts8"."PostTypeId" = 2 THEN 1 ELSE 0 END) AS "TotalAnswers", "Posts8"."Title" AS "LastPostT...
```

## learnedrewrite / LONGTAIL_0013

- Selection types: `key_frontier_row`
- Failure bucket(s): `candidate_execution_failed`
- Speedup ratio(s): `N.A.`
- Source-like classification: `nontrivial_or_changed`
- Visible structural note: candidate differs from source after simple whitespace/comment/case normalization; inspect full local files for exact structure.
- Source path: `cases/LONGTAIL/LONGTAIL_0013/sql/source.sql`
- Candidate path: `runs/user/learnedrewrite_pg40_manual_inspection_rerun_v0/candidate_sql/LONGTAIL_0013__postgres.sql`

Source excerpt:

```sql
WITH RankedPosts AS ( SELECT p.Id AS PostId, p.Title, p.OwnerUserId, p.CreationDate, p.Score, ROW_NUMBER() OVER (PARTITION BY p.OwnerUserId ORDER BY p.Score DESC) AS rank_value FROM Posts p WHERE p.PostTypeId = 1 ), UserStats AS ( SELECT u.Id AS UserId, u.DisplayName, COALESCE...
```

Candidate excerpt:

```sql
SELECT "t734"."DisplayName", COUNT("t734"."Id0") FILTER (WHERE "t734"."$g_0") AS "AnsweredQuestions", CASE WHEN (MIN("t734"."$f6") FILTER (WHERE "t734"."$g_1")) IS NOT NULL THEN CAST(MIN("t734"."$f6") FILTER (WHERE "t734"."$g_1") AS INTEGER) ELSE 0 END AS "AvgScore", "t734"."T...
```

## learnedrewrite / LONGTAIL_0022

- Selection types: `key_frontier_row`
- Failure bucket(s): `candidate_execution_failed`
- Speedup ratio(s): `N.A.`
- Source-like classification: `nontrivial_or_changed`
- Visible structural note: candidate differs from source after simple whitespace/comment/case normalization; inspect full local files for exact structure.
- Source path: `cases/LONGTAIL/LONGTAIL_0022/sql/source.sql`
- Candidate path: `runs/user/learnedrewrite_pg40_manual_inspection_rerun_v0/candidate_sql/LONGTAIL_0022__postgres.sql`

Source excerpt:

```sql
WITH CommentStats AS ( SELECT c.PostId, COUNT(*) AS comment_count, COUNT(DISTINCT c.UserId) AS distinct_commenters FROM Comments c GROUP BY c.PostId ) SELECT p.Id AS PostId, p.Title, p.Score, cs.comment_count, cs.distinct_commenters, u.DisplayName AS OwnerDisplayName FROM Comm...
```

Candidate excerpt:

```sql
SELECT "Posts4"."Id" AS "PostId", "Posts4"."Title", "Posts4"."Score", "t29"."comment_count", "t29"."distinct_commenters", "Users4"."DisplayName" AS "OwnerDisplayName" FROM (SELECT "PostId", COUNT(*) AS "comment_count", COUNT(DISTINCT "UserId") AS "distinct_commenters" FROM "Co...
```

## learnedrewrite / LONGTAIL_0023

- Selection types: `key_frontier_row`
- Failure bucket(s): `candidate_execution_failed`
- Speedup ratio(s): `N.A.`
- Source-like classification: `nontrivial_or_changed`
- Visible structural note: candidate differs from source after simple whitespace/comment/case normalization; inspect full local files for exact structure.
- Source path: `cases/LONGTAIL/LONGTAIL_0023/sql/source.sql`
- Candidate path: `runs/user/learnedrewrite_pg40_manual_inspection_rerun_v0/candidate_sql/LONGTAIL_0023__postgres.sql`

Source excerpt:

```sql
WITH OutboundLinks AS ( SELECT pl.PostId, COUNT(*) AS outbound_count FROM PostLinks pl GROUP BY pl.PostId ), InboundLinks AS ( SELECT pl.RelatedPostId AS PostId, COUNT(*) AS inbound_count FROM PostLinks pl GROUP BY pl.RelatedPostId ) SELECT p.Id AS PostId, p.Title, COALESCE(o....
```

Candidate excerpt:

```sql
SELECT "Posts3"."Id" AS "PostId", "Posts3"."Title", CASE WHEN "t26"."outbound_count" IS NOT NULL THEN CAST("t26"."outbound_count" AS BIGINT) ELSE 0 END AS "outbound_count", CASE WHEN "t28"."inbound_count" IS NOT NULL THEN CAST("t28"."inbound_count" AS BIGINT) ELSE 0 END AS "in...
```

## learnedrewrite / LONGTAIL_0024

- Selection types: `key_frontier_row`
- Failure bucket(s): `candidate_execution_failed`
- Speedup ratio(s): `N.A.`
- Source-like classification: `nontrivial_or_changed`
- Visible structural note: candidate differs from source after simple whitespace/comment/case normalization; inspect full local files for exact structure.
- Source path: `cases/LONGTAIL/LONGTAIL_0024/sql/source.sql`
- Candidate path: `runs/user/learnedrewrite_pg40_manual_inspection_rerun_v0/candidate_sql/LONGTAIL_0024__postgres.sql`

Source excerpt:

```sql
WITH HistoryStats AS ( SELECT ph.PostId, COUNT(*) AS revision_count, COUNT(DISTINCT ph.UserId) AS distinct_editors, MIN(ph.CreationDate) AS first_revision_at, MAX(ph.CreationDate) AS last_revision_at FROM PostHistory ph GROUP BY ph.PostId ) SELECT p.Id AS PostId, p.Title, hs.r...
```

Candidate excerpt:

```sql
SELECT "Posts3"."Id" AS "PostId", "Posts3"."Title", "t23"."revision_count", "t23"."distinct_editors", "t23"."first_revision_at", "t23"."last_revision_at", "Posts3"."Score", "Posts3"."ViewCount" FROM (SELECT "PostId", COUNT(*) AS "revision_count", COUNT(DISTINCT "UserId") AS "d...
```

## learnedrewrite / PERF_0008

- Selection types: `min_speedup`
- Failure bucket(s): `none`
- Speedup ratio(s): `0.5608400092854456`
- Source-like classification: `nontrivial_or_changed`
- Visible structural note: candidate differs from source after simple whitespace/comment/case normalization; inspect full local files for exact structure.
- Source path: `cases/PERF/PERF_0008/sql/source.sql`
- Candidate path: `runs/user/learnedrewrite_pg40_manual_inspection_rerun_v0/candidate_sql/PERF_0008__postgres.sql`

Source excerpt:

```sql
-- PERF_0008 source layer -- Source registry row: SRC_001 (TPC-H) -- Raw source file: datasets/raw/tpch/TPC-H V3.0.1/dbgen/queries/3.sql -- Seed: TPC-H Query 3, Shipping Priority Query -- Freeze method: manual freeze because local qgen executable was not present. -- Reference ...
```

Candidate excerpt:

```sql
SELECT "t789"."l_orderkey", SUM("t789"."l_extendedprice" * (1 - "t789"."l_discount")) AS "revenue", "t788"."o_orderdate", "t788"."o_shippriority" FROM (SELECT * FROM (SELECT * FROM "customer" WHERE "c_mktsegment" = 'MACHINERY') AS "t786", (SELECT * FROM "orders" WHERE "o_order...
```

## learnedrewrite / PERF_0017

- Selection types: `p50_near`
- Failure bucket(s): `none`
- Speedup ratio(s): `0.999038713817663`
- Source-like classification: `nontrivial_or_changed`
- Visible structural note: candidate differs from source after simple whitespace/comment/case normalization; inspect full local files for exact structure.
- Source path: `cases/PERF/PERF_0017/sql/source.sql`
- Candidate path: `runs/user/learnedrewrite_pg40_manual_inspection_rerun_v0/candidate_sql/PERF_0017__postgres.sql`

Source excerpt:

```sql
-- PERF_0017 source layer -- Source registry row: SRC_001 (TPC-H) -- Raw source file: datasets/raw/tpch/TPC-H V3.0.1/dbgen/queries/10.sql -- Seed: TPC-H Query 10, Returned Item Reporting Query -- Freeze method: manual freeze because local qgen executable was not used for this ...
```

Candidate excerpt:

```sql
SELECT "t727"."c_custkey", "t727"."c_name", SUM("t727"."l_extendedprice" * (1 - "t727"."l_discount")) AS "revenue", "t727"."c_acctbal", "nation102"."n_name", "t727"."c_address", "t727"."c_phone", "t727"."c_comment" FROM (SELECT * FROM (SELECT * FROM "customer" AS "customer102"...
```

## learnedrewrite / PERF_0019

- Selection types: `key_frontier_row`
- Failure bucket(s): `mismatch`
- Speedup ratio(s): `N.A.`
- Source-like classification: `nontrivial_or_changed`
- Visible structural note: candidate differs from source after simple whitespace/comment/case normalization; inspect full local files for exact structure.
- Source path: `cases/PERF/PERF_0019/sql/source.sql`
- Candidate path: `runs/user/learnedrewrite_pg40_manual_inspection_rerun_v0/candidate_sql/PERF_0019__postgres.sql`

Source excerpt:

```sql
-- PERF_0019 source layer -- Source registry row: SRC_001 (TPC-H) -- Raw source file: datasets/raw/tpch/TPC-H V3.0.1/dbgen/queries/13.sql -- Seed: TPC-H Query 13, Customer Distribution Query -- Freeze method: manual freeze because local qgen executable was not used for this ba...
```

Candidate excerpt:

```sql
SELECT "t9"."EXPR$1", COUNT(*) AS "custdist" FROM (SELECT "customer1"."c_custkey", COUNT("orders1"."o_orderkey") AS "EXPR$1" FROM "customer" AS "customer1" LEFT JOIN "orders" AS "orders1" ON "customer1"."c_custkey" = "orders1"."o_custkey" AND "orders1"."o_comment" NOT LIKE '%e...
```

## learnedrewrite / PERF_0033

- Selection types: `key_frontier_row`
- Failure bucket(s): `mismatch`
- Speedup ratio(s): `N.A.`
- Source-like classification: `nontrivial_or_changed`
- Visible structural note: candidate differs from source after simple whitespace/comment/case normalization; inspect full local files for exact structure.
- Source path: `cases/PERF/PERF_0033/sql/source.sql`
- Candidate path: `runs/user/learnedrewrite_pg40_manual_inspection_rerun_v0/candidate_sql/PERF_0033__postgres.sql`

Source excerpt:

```sql
-- PERF_0033 source SQL. -- Frozen from TPC-DS query55.tpl via repaired repo-local dsqgen: -- COUNT=1, QUALIFY=Y, SCALE=1, DIALECT=ansi -- PostgreSQL normalization only replaces TOP 100 with LIMIT 100. select i.i_brand_id as brand_id, i.i_brand as brand, sum(ss.ss_ext_sales_pr...
```

Candidate excerpt:

```sql
SELECT "t151"."i_brand_id", "t151"."i_brand", SUM("t149"."ext_price" * "t151"."$f3") AS "ext_price" FROM (SELECT "t147"."ss_item_sk", SUM("t146"."$f1" * "t147"."ext_price") AS "ext_price" FROM (SELECT "d_date_sk", COUNT(*) AS "$f1" FROM "date_dim" WHERE "d_moy" = 12 AND "d_yea...
```

## learnedrewrite / PERF_0035

- Selection types: `key_frontier_row`
- Failure bucket(s): `no_candidate_sql`
- Speedup ratio(s): `N.A.`
- Source-like classification: `no_candidate`
- Visible structural note: candidate missing; no structural SQL comparison available.
- Source path: `cases/PERF/PERF_0035/sql/source.sql`
- Candidate path: `N.A.`

Source excerpt:

```sql
-- PERF_0035 source SQL. -- Frozen from TPC-DS query57.tpl via repaired repo-local dsqgen: -- COUNT=1, QUALIFY=Y, SCALE=1, DIALECT=ansi -- PostgreSQL normalization only replaces TOP 100 with LIMIT 100. with v1 as ( select i.i_category, i.i_brand, cc.cc_name, d.d_year, d.d_moy,...
```

Candidate excerpt:

```sql
N.A.
```

## learnedrewrite / PERF_0052

- Selection types: `p10_near`
- Failure bucket(s): `none`
- Speedup ratio(s): `0.7070555507115637`
- Source-like classification: `nontrivial_or_changed`
- Visible structural note: candidate differs from source after simple whitespace/comment/case normalization; inspect full local files for exact structure.
- Source path: `cases/PERF/PERF_0052/sql/source.sql`
- Candidate path: `runs/user/learnedrewrite_pg40_manual_inspection_rerun_v0/candidate_sql/PERF_0052__postgres.sql`

Source excerpt:

```sql
-- PERF_0052 source SQL. -- Frozen from TPC-DS query_templates/query1.tpl via repaired repo-local dsqgen: -- COUNT=1, QUALIFY=Y, SCALE=1, DIALECT=ansi -- PostgreSQL normalization replaces TOP 100 with LIMIT 100. with customer_total_return as ( select sr_customer_sk as ctr_cust...
```

Candidate excerpt:

```sql
SELECT "t1387"."c_customer_id" FROM (SELECT * FROM (SELECT * FROM (SELECT "store_returns205"."sr_customer_sk" AS "ctr_customer_sk", "store_returns205"."sr_store_sk" AS "ctr_store_sk", SUM("store_returns205"."sr_fee") AS "ctr_total_return" FROM "store_returns" AS "store_returns...
```

## learnedrewrite / PERF_0054

- Selection types: `max_speedup`
- Failure bucket(s): `none`
- Speedup ratio(s): `1.7586744034651542`
- Source-like classification: `nontrivial_or_changed`
- Visible structural note: candidate differs from source after simple whitespace/comment/case normalization; inspect full local files for exact structure.
- Source path: `cases/PERF/PERF_0054/sql/source.sql`
- Candidate path: `runs/user/learnedrewrite_pg40_manual_inspection_rerun_v0/candidate_sql/PERF_0054__postgres.sql`

Source excerpt:

```sql
-- PERF_0054 source SQL. -- Frozen from TPC-DS query_templates/query3.tpl via repaired repo-local dsqgen: -- COUNT=1, QUALIFY=Y, SCALE=1, DIALECT=ansi -- PostgreSQL normalization replaces TOP 100 with LIMIT 100. select dt.d_year, item.i_brand_id brand_id, item.i_brand brand, s...
```

Candidate excerpt:

```sql
SELECT "t789"."d_year", "t789"."i_brand_id" AS "brand_id", "t789"."i_brand" AS "brand", "t789"."sum_agg" FROM (SELECT "t783"."d_year", "t785"."i_brand", "t785"."i_brand_id", SUM("t783"."sum_agg" * "t785"."$f3") AS "sum_agg" FROM (SELECT "t780"."d_year", "t781"."ss_item_sk", SU...
```

## learnedrewrite / PORT_0004

- Selection types: `key_frontier_row`
- Failure bucket(s): `no_candidate_sql`
- Speedup ratio(s): `N.A.`
- Source-like classification: `no_candidate`
- Visible structural note: candidate missing; no structural SQL comparison available.
- Source path: `cases/PORT/PORT_0004/sql/source.sql`
- Candidate path: `N.A.`

Source excerpt:

```sql
-- case_id: PORT_0004 -- draft source id: PORT_PARROT_DRAFT_0004 -- draft-only / not validated -- source dialect: mysql_like_candidate SELECT CAST( SUM( CASE WHEN `sex` = 'F' THEN 1 ELSE 0 END ) AS DOUBLE ) * 100 / COUNT( `id` ) FROM `patient` WHERE `diagnosis` = 'RA' AND DATE...
```

Candidate excerpt:

```sql
N.A.
```

## learnedrewrite / PORT_0008

- Selection types: `key_frontier_row`
- Failure bucket(s): `no_candidate_sql`
- Speedup ratio(s): `N.A.`
- Source-like classification: `no_candidate`
- Visible structural note: candidate missing; no structural SQL comparison available.
- Source path: `cases/PORT/PORT_0008/sql/source.sql`
- Candidate path: `N.A.`

Source excerpt:

```sql
SELECT "t2"."admemail1" , "t2"."admemail2" FROM "frpm" AS "t1" INNER JOIN "schools" AS "t2" ON "t1"."cdscode" = "t2"."cdscode" WHERE "t2"."county" = 'San Bernardino' AND "t2"."city" = 'San Bernardino' AND "t2"."doc" :: integer = 54 AND EXTRACT( YEAR FROM "t2"."opendate" ) BETW...
```

Candidate excerpt:

```sql
N.A.
```

## learnedrewrite / PORT_0012

- Selection types: `key_frontier_row`
- Failure bucket(s): `no_candidate_sql`
- Speedup ratio(s): `N.A.`
- Source-like classification: `no_candidate`
- Visible structural note: candidate missing; no structural SQL comparison available.
- Source path: `cases/PORT/PORT_0012/sql/source.sql`
- Candidate path: `N.A.`

Source excerpt:

```sql
SELECT CAST( SUM( CASE WHEN "sex" = 'F' THEN 1 ELSE 0 END ) AS REAL ) * 100 / NULLIF( COUNT( "id" ) , 0 ) FROM "patient" WHERE "diagnosis" = 'RA' AND TO_CHAR( CAST( "birthday" AS TIMESTAMP ) , 'YYYY' ) = '1980'
```

Candidate excerpt:

```sql
N.A.
```

## learnedrewrite / PORT_0013

- Selection types: `key_frontier_row`
- Failure bucket(s): `no_candidate_sql`
- Speedup ratio(s): `N.A.`
- Source-like classification: `no_candidate`
- Visible structural note: candidate missing; no structural SQL comparison available.
- Source path: `cases/PORT/PORT_0013/sql/source.sql`
- Candidate path: `N.A.`

Source excerpt:

```sql
SELECT CAST( SUM( `t2`.`gender` = 'F' ) AS DOUBLE ) * 100 / COUNT( `t2`.`client_id` ) FROM `district` AS `t1` INNER JOIN `client` AS `t2` ON `t1`.`district_id` = `t2`.`district_id` WHERE `t1`.`a11` > 10000
```

Candidate excerpt:

```sql
N.A.
```

## learnedrewrite / PORT_0022

- Selection types: `key_frontier_row`
- Failure bucket(s): `no_candidate_sql`
- Speedup ratio(s): `N.A.`
- Source-like classification: `no_candidate`
- Visible structural note: candidate missing; no structural SQL comparison available.
- Source path: `cases/PORT/PORT_0022/sql/source.sql`
- Candidate path: `N.A.`

Source excerpt:

```sql
SELECT CAST( COUNT( `t1`.`id` ) AS DOUBLE ) / 12 FROM `postlinks` AS `t1` INNER JOIN `posts` AS `t2` ON `t1`.`postid` = `t2`.`id` WHERE `t2`.`answercount` <= 2 AND DATE_FORMAT( CAST( `t1`.`creationdate` AS DATETIME ) , '%Y' ) = '2010'
```

Candidate excerpt:

```sql
N.A.
```

## learnedrewrite / PORT_0024

- Selection types: `key_frontier_row`
- Failure bucket(s): `no_candidate_sql`
- Speedup ratio(s): `N.A.`
- Source-like classification: `no_candidate`
- Visible structural note: candidate missing; no structural SQL comparison available.
- Source path: `cases/PORT/PORT_0024/sql/source.sql`
- Candidate path: `N.A.`

Source excerpt:

```sql
SELECT CAST( SUM( CASE WHEN `istextless` = 0 AND `isstoryspotlight` = 1 THEN 1 ELSE 0 END ) AS DOUBLE ) * 100 / COUNT( `id` ) FROM `cards`
```

Candidate excerpt:

```sql
N.A.
```

## learnedrewrite / PORT_0025

- Selection types: `key_frontier_row`
- Failure bucket(s): `no_candidate_sql`
- Speedup ratio(s): `N.A.`
- Source-like classification: `no_candidate`
- Visible structural note: candidate missing; no structural SQL comparison available.
- Source path: `cases/PORT/PORT_0025/sql/source.sql`
- Candidate path: `N.A.`

Source excerpt:

```sql
SELECT `t1`.`account_id` FROM `loan` AS `t1` INNER JOIN `account` AS `t2` ON `t1`.`account_id` = `t2`.`account_id` WHERE DATE_FORMAT( CAST( `t2`.`account_date` AS DATETIME ) , '%Y' ) = '1993' AND `t1`.`duration` > 12 ORDER BY `t1`.`amount` DESC LIMIT 1
```

Candidate excerpt:

```sql
N.A.
```

## llm_r2_gpt54_adapted / CONS_0010

- Selection types: `key_frontier_row`
- Failure bucket(s): `mismatch`
- Speedup ratio(s): `N.A.`
- Source-like classification: `nontrivial_or_changed`
- Visible structural note: candidate differs from source after simple whitespace/comment/case normalization; inspect full local files for exact structure.
- Source path: `cases/CONS/CONS_0010/sql/source.sql`
- Candidate path: `runs/user/llm_r2_gpt54_pg40_manual_inspection_rerun_v0/candidate_sql/CONS_0010__postgres.sql`

Source excerpt:

```sql
SELECT E1.* FROM emp E1 WHERE NOT EXISTS ( SELECT 1 FROM emp E2 JOIN bonus B ON E2.SAL = E1.SAL AND B.JOB = E1.JOB WHERE E2.EMPNO <> E1.EMPNO );
```

Candidate excerpt:

```sql
SELECT E1.* FROM emp E1 WHERE NOT EXISTS ( SELECT 1 FROM emp E2 WHERE E2.EMPNO <> E1.EMPNO ) OR NOT EXISTS ( SELECT 1 FROM bonus B WHERE B.JOB = E1.JOB );
```

## llm_r2_gpt54_adapted / CONS_0024

- Selection types: `p50_near`
- Failure bucket(s): `none`
- Speedup ratio(s): `0.9954983650814071`
- Source-like classification: `nontrivial_or_changed`
- Visible structural note: candidate differs from source after simple whitespace/comment/case normalization; inspect full local files for exact structure.
- Source path: `cases/CONS/CONS_0024/sql/source.sql`
- Candidate path: `runs/user/llm_r2_gpt54_pg40_manual_inspection_rerun_v0/candidate_sql/CONS_0024__postgres.sql`

Source excerpt:

```sql
SELECT empno FROM emp AS e LEFT JOIN dept AS d ON d.deptno = e.deptno AND EXISTS ( SELECT e2.deptno FROM emp AS e2 WHERE e2.deptno = d.deptno GROUP BY e2.deptno HAVING SUM(e2.sal) > 1000000 );
```

Candidate excerpt:

```sql
SELECT e.empno FROM emp AS e LEFT JOIN ( SELECT e2.deptno FROM emp AS e2 GROUP BY e2.deptno HAVING SUM(e2.sal) > 1000000 ) AS x ON x.deptno = e.deptno LEFT JOIN dept AS d ON d.deptno = x.deptno;
```

## llm_r2_gpt54_adapted / LONGTAIL_0011

- Selection types: `key_frontier_row`
- Failure bucket(s): `candidate_execution_failed`
- Speedup ratio(s): `N.A.`
- Source-like classification: `nontrivial_or_changed`
- Visible structural note: candidate differs from source after simple whitespace/comment/case normalization; inspect full local files for exact structure.
- Source path: `cases/LONGTAIL/LONGTAIL_0011/sql/source.sql`
- Candidate path: `runs/user/llm_r2_gpt54_pg40_manual_inspection_rerun_v0/candidate_sql/LONGTAIL_0011__postgres.sql`

Source excerpt:

```sql
WITH RankedPosts AS ( SELECT p.Id, p.Title, p.CreationDate, p.Score, p.ViewCount, u.DisplayName AS OwnerDisplayName, DENSE_RANK() OVER (PARTITION BY p.OwnerUserId ORDER BY p.Score DESC) AS PostRank FROM Posts p JOIN Users u ON p.OwnerUserId = u.Id WHERE p.PostTypeId = 1 AND p....
```

Candidate excerpt:

```sql
WITH RankedPosts AS ( SELECT p.Id, p.Title, p.CreationDate, p.Score, p.ViewCount, u.DisplayName AS OwnerDisplayName, DENSE_RANK() OVER (PARTITION BY p.OwnerUserId ORDER BY p.Score DESC) AS PostRank, MAX(DENSE_RANK() OVER (PARTITION BY p.OwnerUserId ORDER BY p.Score DESC)) OVER...
```

## llm_r2_gpt54_adapted / LONGTAIL_0022

- Selection types: `min_speedup`
- Failure bucket(s): `none`
- Speedup ratio(s): `0.4101297905818729`
- Source-like classification: `nontrivial_or_changed`
- Visible structural note: candidate differs from source after simple whitespace/comment/case normalization; inspect full local files for exact structure.
- Source path: `cases/LONGTAIL/LONGTAIL_0022/sql/source.sql`
- Candidate path: `runs/user/llm_r2_gpt54_pg40_manual_inspection_rerun_v0/candidate_sql/LONGTAIL_0022__postgres.sql`

Source excerpt:

```sql
WITH CommentStats AS ( SELECT c.PostId, COUNT(*) AS comment_count, COUNT(DISTINCT c.UserId) AS distinct_commenters FROM Comments c GROUP BY c.PostId ) SELECT p.Id AS PostId, p.Title, p.Score, cs.comment_count, cs.distinct_commenters, u.DisplayName AS OwnerDisplayName FROM Comm...
```

Candidate excerpt:

```sql
SELECT p.Id AS PostId, p.Title, p.Score, cs.comment_count, cs.distinct_commenters, u.DisplayName AS OwnerDisplayName FROM Posts p JOIN ( SELECT c.PostId, COUNT(*) AS comment_count, COUNT(DISTINCT c.UserId) AS distinct_commenters FROM Comments c GROUP BY c.PostId HAVING COUNT(*...
```

## llm_r2_gpt54_adapted / PERF_0007

- Selection types: `p10_near`
- Failure bucket(s): `none`
- Speedup ratio(s): `0.5824609372767673`
- Source-like classification: `nontrivial_or_changed`
- Visible structural note: candidate differs from source after simple whitespace/comment/case normalization; inspect full local files for exact structure.
- Source path: `cases/PERF/PERF_0007/sql/source.sql`
- Candidate path: `runs/user/llm_r2_gpt54_pg40_manual_inspection_rerun_v0/candidate_sql/PERF_0007__postgres.sql`

Source excerpt:

```sql
-- PERF_0007 source layer -- Source registry row: SRC_001 (TPC-H) -- Raw source file: datasets/raw/tpch/TPC-H V3.0.1/dbgen/queries/6.sql -- Seed: TPC-H Query 6, Forecasting Revenue Change Query -- Freeze method: manual freeze because local qgen executable was not present. -- R...
```

Candidate excerpt:

```sql
SELECT SUM(l_extendedprice * l_discount) AS revenue FROM lineitem WHERE l_shipdate >= DATE '1995-01-01' AND l_shipdate < DATE '1995-01-01' + INTERVAL '1 year' AND l_discount >= 0.08 AND l_discount <= 0.10 AND l_quantity < 25;
```

## llm_r2_gpt54_adapted / PERF_0008

- Selection types: `key_frontier_row`
- Failure bucket(s): `candidate_execution_failed`
- Speedup ratio(s): `N.A.`
- Source-like classification: `nontrivial_or_changed`
- Visible structural note: candidate differs from source after simple whitespace/comment/case normalization; inspect full local files for exact structure.
- Source path: `cases/PERF/PERF_0008/sql/source.sql`
- Candidate path: `runs/user/llm_r2_gpt54_pg40_manual_inspection_rerun_v0/candidate_sql/PERF_0008__postgres.sql`

Source excerpt:

```sql
-- PERF_0008 source layer -- Source registry row: SRC_001 (TPC-H) -- Raw source file: datasets/raw/tpch/TPC-H V3.0.1/dbgen/queries/3.sql -- Seed: TPC-H Query 3, Shipping Priority Query -- Freeze method: manual freeze because local qgen executable was not present. -- Reference ...
```

Candidate excerpt:

```sql
WITH filtered_orders AS ( SELECT o_orderkey, o_orderdate, o_shippriority FROM orders WHERE o_orderdate < DATE '1995-03-27' ) SELECT l.l_orderkey, SUM(l.l_extendedprice * (1 - l.l_discount)) AS revenue, o.o_orderdate, o.o_shippriority FROM customer c JOIN filtered_orders o ON c...
```

## llm_r2_gpt54_adapted / PERF_0077

- Selection types: `max_speedup`
- Failure bucket(s): `none`
- Speedup ratio(s): `1.7875654195202175`
- Source-like classification: `nontrivial_or_changed`
- Visible structural note: candidate differs from source after simple whitespace/comment/case normalization; inspect full local files for exact structure.
- Source path: `cases/PERF/PERF_0077/sql/source.sql`
- Candidate path: `runs/user/llm_r2_gpt54_pg40_manual_inspection_rerun_v0/candidate_sql/PERF_0077__postgres.sql`

Source excerpt:

```sql
-- case_id: PERF_0077 -- source_family: JOB/IMDB -- original JOB query: 3a.sql -- draft_origin: JOB_DRAFT_0003 SELECT min(t.title) AS movie_title FROM keyword AS k, movie_info AS mi, movie_keyword AS mk, title AS t WHERE k.keyword like '%sequel%' AND mi.info IN ('Sweden', 'Nor...
```

Candidate excerpt:

```sql
SELECT min(t.title) AS movie_title FROM title AS t JOIN movie_info AS mi ON mi.movie_id = t.id JOIN movie_keyword AS mk ON mk.movie_id = t.id JOIN keyword AS k ON k.id = mk.keyword_id WHERE k.keyword LIKE '%sequel%' AND mi.info IN ('Sweden', 'Norway', 'Germany', 'Denmark', 'Sw...
```

## llm_r2_gpt54_adapted / PORT_0008

- Selection types: `p90_near`
- Failure bucket(s): `none`
- Speedup ratio(s): `1.6669146055230468`
- Source-like classification: `nontrivial_or_changed`
- Visible structural note: candidate differs from source after simple whitespace/comment/case normalization; inspect full local files for exact structure.
- Source path: `cases/PORT/PORT_0008/sql/source.sql`
- Candidate path: `runs/user/llm_r2_gpt54_pg40_manual_inspection_rerun_v0/candidate_sql/PORT_0008__postgres.sql`

Source excerpt:

```sql
SELECT "t2"."admemail1" , "t2"."admemail2" FROM "frpm" AS "t1" INNER JOIN "schools" AS "t2" ON "t1"."cdscode" = "t2"."cdscode" WHERE "t2"."county" = 'San Bernardino' AND "t2"."city" = 'San Bernardino' AND "t2"."doc" :: integer = 54 AND EXTRACT( YEAR FROM "t2"."opendate" ) BETW...
```

Candidate excerpt:

```sql
SELECT "t2"."admemail1", "t2"."admemail2" FROM "schools" AS "t2" WHERE "t2"."county" = 'San Bernardino' AND "t2"."city" = 'San Bernardino' AND "t2"."doc"::integer = 54 AND EXTRACT(YEAR FROM "t2"."opendate") BETWEEN 2009 AND 2010 AND "t2"."soc"::integer = 62 AND EXISTS ( SELECT...
```
