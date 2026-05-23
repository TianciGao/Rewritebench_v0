# Tool Detection

Detection order:

1. Explicit `command` argument.
2. `SQLRB_SQLSOLVER_CMD`.
3. `SQLSOLVER_COMMAND`.
4. `SQLSOLVER_BIN`.
5. PATH lookup for `sqlsolver`, `SQLSolver`, `sql-solver`, and `sqlsolver-cli`.

Local result:

- `tool_available=false`
- `tool_version=null`
- `detection_reason=sqlsolver_command_not_found`

No external tool was installed. Because SQLSolver was unavailable, no real SQLSolver smoke was run.
