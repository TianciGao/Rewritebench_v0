# Experimental Variants

These checks were performed as scratch SQLGlot-only reproducer snippets. They did not call `user_run`, did not broaden the optimize route trial, and did not modify production code.

## Variant 1: Parse/Emit Only

Call pattern:

```python
expression = sqlglot.parse_one(source_sql, read=dialect)
candidate = expression.sql(dialect=dialect)
```

Result:

- PostgreSQL, MySQL, and Spark parsing succeeded.
- Emitted SQL preserved the original correlated subquery shape.
- No `table1.table2.i` reference was emitted.
- This is consistent with the bounded smoke where the no-op route reached exact `2/2` on each of PostgreSQL, MySQL, and Spark for `PERF_0006` and `CONS_0005`.

## Variant 2: Current Optimize Route

Call pattern:

```python
expression = sqlglot.parse_one(source_sql, read=dialect)
candidate = optimize(expression).sql(dialect=dialect)
```

Result:

- Optimization completed for all three dialect inputs.
- The emitted candidates contained the invalid subquery projection reference:
  - PostgreSQL: `"table1"."table2"."i"`.
  - MySQL/Spark: `` `table1`.`table2`.`i` ``.
- The same structural invalid reference was present across all selected engines.

## Variant 3: Optimize With Dialect Argument

Call pattern:

```python
candidate = optimize(expression, dialect=dialect).sql(dialect=dialect)
```

Result:

- The invalid reference remained.
- Supplying only `dialect` did not resolve the qualification problem.

## Variant 4: Optimize With Schema Mapping

Call pattern:

```python
schema = {
    "table1": {"i": "INT", "j": "INT"},
    "table2": {"i": "INT", "j": "INT"},
}
candidate = optimize(expression, schema=schema).sql(dialect=dialect)
```

Result:

- The invalid `table1.table2.i` reference disappeared.
- SQLGlot rewrote the query into a join plus array/list aggregation expression.
- PostgreSQL output used `ARRAY_AGG`, `ARRAY_LENGTH`, and `UNNEST`.
- MySQL output used `GROUP_CONCAT` and `ARRAY_ANY`; SQLGlot printed an unsupported construct warning during generation.
- Spark output used `COLLECT_LIST`, `SIZE`, and `FILTER`.

Interpretation:

Schema context changes the optimizer behavior, but adopting it would be a new route design. It should not be silently substituted for the current `sqlglot_optimize` route because it changes semantics, dependencies, and comparability boundaries.
