# Spark CONS_0036 Label Review

Row:

- case_id: `CONS_0036`
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
SELECT NAME AS NAME, COUNT(*) AS C FROM DEPT GROUP BY NAME HAVING NAME = 'Charlie'
```

Candidate query:

```sql
SELECT `dept`.`name` AS `name`, COUNT(*) AS `c` FROM `dept` AS `dept` GROUP BY `dept`.`name` HAVING `dept`.`name` = 'Charlie';
```

Source result:

```json
{"NAME": "Charlie", "C": 2}
```

Candidate result:

```json
{"name": "Charlie", "c": 2}
```

Checker mismatch summary:

- source row count: 1
- candidate row count: 1
- `value_exact`: true
- `value_mismatch_reason`: `none`
- `label_exact`: false
- `label_only_mismatch`: true
- label mismatch class: `unclassified_label_difference`
- label policy: `strict`

## Verdict

This is label-only under the current strict label policy. The values match and only result labels differ by identifier case:

- source labels: `NAME`, `C`
- candidate labels: `name`, `c`

This is a reasonable future checker-normalization policy candidate because the row count and values match exactly. A future policy could allow case-insensitive label matching for Spark same-engine outputs when value equality is already established and no positional/value coercion is needed.

Policy boundary:

- do not implement label normalization in this task;
- keep the row classified as mismatch until an explicit checker policy task is authorized;
- require tests proving same-engine default behavior and cross-dialect policies remain protected.
