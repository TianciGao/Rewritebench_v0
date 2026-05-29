# Exact Row Inventory

The refreshed exact-row inventory is recorded in `exact_row_inventory.csv`.

Row count:

- CSV data rows: 35
- Header rows: 1

Inventory fields include:

- `case_id`
- `pool`
- `engine`
- `route_id`
- `method_id`
- source, candidate, schema, and checker paths
- exact/result-consistency status
- updated bound-4 eligibility label
- proposed subset label
- known bound-4 evidence

Updated exact-row label counts:

- `already_validated_bound4_equivalent`: 2
- `blocked_exists_or_subquery`: 17
- `blocked_function_or_datetime`: 10
- `blocked_like_not_implemented`: 4
- `blocked_dialect_syntax`: 2

`CONS_0036` and `CONS_0037` are the only exact rows currently marked as already validated under the declared bound-4 policy.
