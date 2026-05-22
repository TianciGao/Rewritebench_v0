# Facade Policy

Users should not need to call internal `src/sql_rewrite_bench/` modules directly.

Per D035:

- public-facing CLI/facade target: `src/cli/`
- internal implementation package: `src/sql_rewrite_bench/`
- development and validation tools: `src/dev/`

The future `src/cli` facade should call existing internal modules and should not duplicate business logic.

Developer-only tools may later live under `src/dev`, but this task does not create `src/cli`, `src/dev`, or any CLI implementation.
