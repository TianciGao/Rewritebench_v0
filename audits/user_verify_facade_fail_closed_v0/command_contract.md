# Command Contract

Supported commands:

```bash
sqlrb user verify --run-id <run_id> --tool verieql --output-root output
sqlrb user verify --run-id <run_id> --tool sqlsolver --output-root output
```

Optional flags:

- `--tool-cmd <path-or-command>`: explicit local verifier command.
- `--timeout <seconds>`: wrapper timeout, default `30`.
- `--pair-scope synthetic-smoke|run-candidates|controls`: only `synthetic-smoke` is implemented.

Unsupported scopes:

- `run-candidates`
- `controls`

These fail closed with a clear error and do not write verifier artifacts.

`sqlrb user evaluate --verifier verieql` and `sqlrb user evaluate --verifier sqlsolver` remain fail-closed and are not silently broadened by this task.
