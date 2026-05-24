# Spark CONS_0036 Triage

Problem row:

- case_id: `CONS_0036`
- engine: `spark`
- route_id: `sqlglot_optimize_schema_aware`
- prior status: `checker_mismatch`

## Source and candidate

Source SQL:

```sql
SELECT NAME AS NAME, COUNT(*) AS C FROM DEPT GROUP BY NAME HAVING NAME = 'Charlie'
```

Candidate SQL:

```sql
SELECT `dept`.`name` AS `name`, COUNT(*) AS `c`
FROM `dept` AS `dept`
GROUP BY `dept`.`name`
HAVING `dept`.`name` = 'Charlie';
```

## Checker evidence

The mismatch artifact recorded:

```json
{
  "source_preview": [{"C": 2, "NAME": "Charlie"}],
  "candidate_preview": [{"c": 2, "name": "Charlie"}],
  "source_row_count": 1,
  "candidate_row_count": 1,
  "cross_dialect_normalization": {
    "value_exact": true,
    "label_exact": false,
    "label_only_mismatch": true,
    "label_policy": "strict",
    "label_mismatch_class": "unclassified_label_difference",
    "value_mismatch_reason": "none"
  }
}
```

## Classification

Primary classification:

- `spark_label_only_mismatch_candidate`

Secondary classification:

- `checker_normalization_policy_candidate`

## Root cause

The result values match positionally and semantically:

- source: `{"NAME": "Charlie", "C": 2}`
- candidate: `{"name": "Charlie", "c": 2}`

The mismatch is caused by strict result-label comparison. SQLGlot emitted lowercase aliases for Spark, while the source query has uppercase explicit aliases.

Under the current documented strict-label policy, this remains a mismatch. It is not currently exact/result-consistent.

## Recommendation

This row is a safe normalization candidate only if a future explicit label policy is authorized. Such a policy should be case/role/config gated and should not be inferred ad hoc in the route adapter. Until then, the row remains fail-visible as `checker_mismatch`.

This row should not block exact-gated timing over other exact rows, but it does block paper-facing promotion and should remain visible in any larger Spark route trial.

