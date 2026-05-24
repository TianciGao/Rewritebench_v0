# Blocker Classification

Primary blockers observed in this bounded smoke:

| blocker | affected rows in smoke | classification | current handling |
|---|---:|---|---|
| PostgreSQL-dialect output for MySQL | 5 | adapter/runtime target-dialect gap | fail closed before DB execution |
| PostgreSQL-dialect output for Spark | 5 | adapter/runtime target-dialect gap | fail closed before DB execution |
| DATETIME/TIMESTAMP / PORT dialect row | 3 `PORT_0004` rows | Calcite no-candidate / source dialect frontier | fail closed |
| PostgreSQL `CONS_0036` label-only mismatch | 1 | checker label policy / route output frontier | remain mismatch |
| Spark `PORT_0024` source-role / target-reference policy | 1 | route-scope policy issue | remain blocked/fail-closed |

MySQL blockers:

- The external runtime can be invoked with MySQL DDL, but emitted
  PostgreSQL-style quoted identifiers.
- The adapter now catches this class before DB execution.
- A real MySQL-ready Calcite route still needs target-dialect emission from the
  external runtime or a separately authorized engine mode contract.

Spark blockers:

- The external runtime can be invoked with Spark DDL, but emitted
  PostgreSQL-style quoted identifiers.
- The adapter now catches this class before DB execution.
- Spark source-role and target-reference policy remains separate for PORT rows.

PostgreSQL blockers:

- `PORT_0004` remains no-candidate.
- `CONS_0036` remains a strict checker mismatch after successful source and
  candidate execution.

The fail-closed target-dialect guard is a readiness hardening fix, not evidence
that Calcite is tri-engine capable.
