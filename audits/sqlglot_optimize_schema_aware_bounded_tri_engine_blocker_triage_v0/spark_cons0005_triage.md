# Spark CONS_0005 Triage

Problem row:

- case_id: `CONS_0005`
- engine: `spark`
- route_id: `sqlglot_optimize_schema_aware`
- prior status: `checker_mismatch`

## Source and candidate

Source SQL:

```sql
SELECT i, j
FROM table1
WHERE table1.j NOT IN (
  SELECT i
  FROM table2
  WHERE table1.i = table2.j
);
```

Spark setup from the prior trace:

```sql
CREATE TABLE table1 (i INT, j INT) USING parquet;
CREATE TABLE table2 (i INT, j INT) USING parquet;

INSERT INTO table1 VALUES (1, 2), (1, 3);
INSERT INTO table2 VALUES (NULL, 1), (2, 1);
```

Candidate SQL:

```sql
WITH `_u_0` AS (
  SELECT COLLECT_LIST(`table2`.`i`) AS `i`, `table2`.`j` AS `_u_1`
  FROM `table2` AS `table2`
  GROUP BY `table2`.`j`
)
SELECT `table1`.`i` AS `i`, `table1`.`j` AS `j`
FROM `table1` AS `table1`
LEFT JOIN `_u_0` AS `_u_0`
  ON `_u_0`.`_u_1` = `table1`.`i`
WHERE NOT (
  SIZE(`_u_0`.`i`) = 0
  OR SIZE(FILTER(`_u_0`.`i`, `_x` -> `table1`.`j` = `_x`)) <> 0
);
```

## Checker evidence

The mismatch artifact recorded:

```json
{
  "source_row_count": 0,
  "candidate_row_count": 1,
  "source_preview": [],
  "candidate_preview": [{"i": 1, "j": 3}],
  "cross_dialect_normalization": {
    "value_exact": false,
    "value_mismatch_reason": "row_count_mismatch",
    "label_only_mismatch": false,
    "label_policy": "strict"
  }
}
```

## Classification

Primary classification:

- `spark_semantic_mismatch_candidate`

Secondary classifications:

- `sqlglot_schema_aware_optimizer_limit`
- `true_candidate_semantic_drift`
- `manual_review_required`

## Root cause

The mismatch is a row-count/value mismatch, not a label mismatch. The source result is empty, while the candidate returns one row: `{"i": 1, "j": 3}`.

The source query uses `NOT IN` over a correlated subquery whose matching input includes `NULL`. The optimized Spark candidate rewrites the predicate through `COLLECT_LIST`, `FILTER`, and `SIZE`. The observed result indicates that the rewrite did not preserve the source predicate behavior for the `NULL`-sensitive case.

This should be treated as candidate semantic risk unless a dedicated SQLGlot/Spark semantic analysis proves otherwise.

## Recommendation

Do not normalize this mismatch away. `CONS_0005` should block a larger Spark `sqlglot_optimize_schema_aware` trial until a dedicated fix or route-level exclusion policy is authorized.

