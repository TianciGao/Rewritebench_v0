# Minimal Reproducer

Environment:

- SQLGlot version: `30.2.1`.
- Case: `CONS_0005`.
- Source file: `cases/CONS/CONS_0005/sql/source.sql`.
- Adapter route under triage: `python baselines/sqlglot/sqlglot_user_adapter.py --route optimize`.

Input SQL:

```sql
SELECT i, j
FROM table1
WHERE table1.j NOT IN (
  SELECT i
  FROM table2
  WHERE table1.i = table2.j
);
```

Reproducer:

```python
from pathlib import Path
import sqlglot
from sqlglot.optimizer import optimize

source_sql = Path("cases/CONS/CONS_0005/sql/source.sql").read_text()

for dialect in ["postgres", "mysql", "spark"]:
    expression = sqlglot.parse_one(source_sql, read=dialect)
    optimized = optimize(expression)
    print(dialect)
    print(optimized.sql(dialect=dialect))
```

Observed behavior:

- `parse_one(..., read=dialect)` succeeds for PostgreSQL, MySQL, and Spark.
- `optimize(expression)` succeeds for all three dialect inputs.
- Emitted candidate SQL contains an invalid subquery projection reference:
  - PostgreSQL: `"table1"."table2"."i"`.
  - MySQL: `` `table1`.`table2`.`i` ``.
  - Spark: `` `table1`.`table2`.`i` ``.
- The invalid reference shape is the same across engines: a table alias from the outer scope is prefixed onto the inner `table2.i` projection.

Control variants:

- Parse/emit without optimize preserves an executable query shape for all three dialects.
- Optimizing with a simple schema mapping for `table1(i,j)` and `table2(i,j)` no longer emits `table1.table2.i`, but it rewrites the query into more complex dialect-specific array/list constructs. That is a different route semantics and was not adopted in this triage.
