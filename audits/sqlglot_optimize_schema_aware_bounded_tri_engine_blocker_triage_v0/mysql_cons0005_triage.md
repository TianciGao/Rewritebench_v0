# MySQL CONS_0005 Triage

Problem row:

- case_id: `CONS_0005`
- engine: `mysql`
- route_id: `sqlglot_optimize_schema_aware`
- prior status: `candidate_execution_failed`

## Candidate SQL

The candidate emitted by the schema-aware SQLGlot optimize route was:

```sql
WITH `_u_0` AS (
  SELECT GROUP_CONCAT(`table2`.`i`) AS `i`, `table2`.`j` AS `_u_1`
  FROM `table2` AS `table2`
  GROUP BY `table2`.`j`
)
SELECT `table1`.`i` AS `i`, `table1`.`j` AS `j`
FROM `table1` AS `table1`
LEFT JOIN `_u_0` AS `_u_0`
  ON `_u_0`.`_u_1` = `table1`.`i`
WHERE NOT ARRAY_ANY(`_u_0`.`i`, `_x` -> `table1`.`j` = `_x`);
```

The `ARRAY_ANY(..., _x -> ...)` expression is the failing construct. The adapter stderr recorded:

```text
ARRAY_ANY is unsupported
```

The MySQL execution error was:

```text
ERROR 1064 (42000) at line 2: You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '`table1`.`j` = `_x`)' at line 1
```

## Classification

Primary classification:

- `mysql_array_any_dialect_emission_blocker`

Secondary classifications:

- `sqlglot_schema_aware_optimizer_limit`
- `adapter_fail_closed_policy_needed`

## Root cause

This is not the original context-free optimizer qualification issue. The prior invalid `table1.table2.i` shape is absent. The schema-aware route generated a MySQL candidate that still contains a SQLGlot optimizer expression shape MySQL cannot execute: `ARRAY_ANY` with lambda syntax.

The failure is best treated as a SQLGlot dialect emission / optimizer-output limitation surfaced by the schema-aware route. The adapter already detects the unsupported construct in stderr, but the route currently lets the candidate advance to local execution and fail there.

## Fixability

Safe immediate policy candidate:

- Add a narrow MySQL fail-closed guard for schema-aware optimize candidates containing `ARRAY_ANY` or lambda-style constructs that SQLGlot reports as unsupported.

Potential future implementation candidate:

- Investigate whether SQLGlot can emit an equivalent MySQL-safe anti-join or null-aware expression for this pattern.

Unsafe in this audit:

- Rewriting `ARRAY_ANY` ad hoc inside the audit task.
- Changing case SQL or core runner behavior.
- Marking the row exact based on source behavior or local checker exactness.

## Recommendation

Until a dedicated SQLGlot dialect fix is authorized, `CONS_0005` / MySQL should fail closed for `sqlglot_optimize_schema_aware` instead of being treated as a generated executable candidate. This row should block a larger MySQL optimize trial and full Track A 120 readiness for this route.

