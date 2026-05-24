# Source Blocker Review

Source audit:

- `audits/sqlglot_optimize_schema_aware_bounded_tri_engine_blocker_triage_v0/`

The blocker triage classified:

- `CONS_0005` / MySQL as `mysql_array_any_dialect_emission_blocker`.
- `CONS_0005` / Spark as `spark_semantic_mismatch_candidate`.
- `CONS_0036` / Spark as `spark_label_only_mismatch_candidate`.

Only the MySQL `ARRAY_ANY` issue was targeted by this task.

## MySQL blocker

The prior MySQL candidate for `CONS_0005` contained:

```sql
WHERE NOT ARRAY_ANY(`_u_0`.`i`, `_x` -> `table1`.`j` = `_x`);
```

The previous execution/checker audit recorded:

- adapter stderr: `ARRAY_ANY is unsupported`
- MySQL execution error: syntax error near the lambda body
- prior stage status: `candidate_execution_failed`

The prior invalid `table1.table2.i` qualification was already gone. This task does not alter that earlier schema-aware route fix.

## Non-target blockers

Spark `CONS_0005` remains a value/row-count semantic mismatch:

- source row count: 0
- candidate row count: 1

Spark `CONS_0036` remains a strict-label mismatch:

- values equal
- labels differ by case

Neither Spark blocker was modified or normalized.
