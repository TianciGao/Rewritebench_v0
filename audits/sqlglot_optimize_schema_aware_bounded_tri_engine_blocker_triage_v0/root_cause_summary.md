# Root Cause Summary

Rows triaged: 3.

## Primary classification counts

| Classification | Count | Rows |
| --- | ---: | --- |
| `mysql_array_any_dialect_emission_blocker` | 1 | `CONS_0005` / MySQL |
| `spark_semantic_mismatch_candidate` | 1 | `CONS_0005` / Spark |
| `spark_label_only_mismatch_candidate` | 1 | `CONS_0036` / Spark |

## Findings

The prior invalid qualification issue is resolved:

- No inspected row contains `"table1"."table2"."i"`.
- No inspected row contains `` `table1`.`table2`.`i` ``.

Remaining blockers are independent:

1. MySQL `CONS_0005` is a dialect-emission failure. SQLGlot emitted `ARRAY_ANY` with lambda syntax that MySQL rejected.
2. Spark `CONS_0005` is value/row-count drift. The source result is empty, while the candidate returns one row.
3. Spark `CONS_0036` is label-only drift under strict checker policy. Values match, labels differ by case.

## Safe normalization candidates

Only Spark `CONS_0036` is a safe normalization candidate, and only under a future explicit label policy. No policy change was made in this task.

## True semantic-risk candidates

Spark `CONS_0005` is a true semantic-risk candidate because the source and candidate row sets differ. It should not be normalized away.

MySQL `CONS_0005` is not semantically classified because the candidate did not execute. It is a dialect-emission blocker and should fail closed or be fixed before semantic interpretation.

