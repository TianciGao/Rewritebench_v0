# Synthetic Smoke Results

Runtime root:

- `/tmp/sqlrb_sqlsolver_external_setup_wrapper_smoke_v0/`

Environment:

- `SQLRB_SQLSOLVER_JAR=/home/tianci_gao/.local/share/sqlrb/sqlsolver/SQLSolver/build/libs/sqlsolver-v1.1.0.jar`
- `SQLRB_SQLSOLVER_ROOT=/home/tianci_gao/.local/share/sqlrb/sqlsolver/SQLSolver`
- `SQLRB_SQLSOLVER_LD_LIBRARY_PATH=/home/tianci_gao/.local/share/sqlrb/sqlsolver/SQLSolver/lib`
- `SQLRB_SQLSOLVER_JAVA=java`

Pairs:

| Pair ID | SQL 1 | SQL 2 | Raw output | Normalized verdict |
|---|---|---|---|---|
| `synthetic_sqlsolver_equivalent` | `SELECT i, j FROM a` | `SELECT T.COL1, T.COL2 FROM (SELECT i AS COL1, j AS COL2 FROM a) AS T` | `EQ` | `equivalent` |
| `synthetic_sqlsolver_non_equivalent` | `SELECT i FROM a` | `SELECT j FROM a` | `NEQ` | `non_equivalent` |

Schema:

```sql
CREATE TABLE a ( i INT PRIMARY KEY, j INT, k INT );
```

Summary:

- Tool available: true.
- Tool version: `SQLSolver v1.1.0`.
- Pairs planned: 2.
- Pairs attempted: 2.
- Equivalent: 1.
- Non-equivalent: 1.
- Decidable: 2.
- Verifier decidability rate: 1.0 for this synthetic smoke.

This smoke is local verifier-support evidence only. It is not Common-core evidence, not official Semantic Equivalence Rate, not paper evidence, and not retained evidence.
