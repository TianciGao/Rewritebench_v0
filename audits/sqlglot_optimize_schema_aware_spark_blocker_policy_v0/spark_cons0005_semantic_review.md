# Spark CONS_0005 Semantic Review

Row:

- case_id: `CONS_0005`
- engine: `spark`
- route_id: `sqlglot_optimize_schema_aware`

Post-guard status:

- candidate generated: true
- source executable: true
- candidate executable: true
- checker attempted: true
- exact/result-consistent: false
- failure bucket: `mismatch`

## Observed Difference

Source query:

```sql
SELECT i, j
FROM table1
WHERE table1.j NOT IN (
  SELECT i
  FROM table2
  WHERE table1.i = table2.j
);
```

Candidate query:

```sql
WITH `_u_0` AS (SELECT COLLECT_LIST(`table2`.`i`) AS `i`, `table2`.`j` AS `_u_1` FROM `table2` AS `table2` GROUP BY `table2`.`j`) SELECT `table1`.`i` AS `i`, `table1`.`j` AS `j` FROM `table1` AS `table1` LEFT JOIN `_u_0` AS `_u_0` ON `_u_0`.`_u_1` = `table1`.`i` WHERE NOT (SIZE(`_u_0`.`i`) = 0 OR SIZE(FILTER(`_u_0`.`i`, `_x` -> `table1`.`j` = `_x`)) <> 0);
```

Checker mismatch summary:

- source row count: 0
- candidate row count: 1
- source preview: empty
- candidate preview: `{"i": 1, "j": 3}`
- `value_exact`: false
- `value_mismatch_reason`: `row_count_mismatch`
- `label_only_mismatch`: false

## Verdict

This is a true semantic-risk mismatch, not a checker-normalization issue. The source and candidate both execute, but they return different row counts and different values.

Policy recommendation:

- keep `CONS_0005` / Spark as mismatch for `sqlglot_optimize_schema_aware`;
- do not time this row;
- do not include it in exact-result local metrics;
- require separate SQLGlot Spark rewrite semantic triage before any larger Spark optimize trial.
