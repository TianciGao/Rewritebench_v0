# Blocker Backlog

Identity guard failures:

- `identity_guard_failed_unsupported`: 16 rows
- `identity_guard_failed_timeout`: 8 rows
- `identity_guard_failed_not_implemented`: 5 rows
- `identity_guard_failed_tool_error`: 1 row
- `identity_guard_failed_non_equivalent`: 1 row

Rows passing identity guard:

- `CONS_0036`
- `CONS_0037`
- `PORT_0003`
- `PORT_0005`

Key blocker:

- `LONGTAIL_0023` remains `identity_guard_failed_non_equivalent`.

Next options:

- Stop VeriEQL expansion for paper-facing SER until identity failures are understood.
- Improve VeriEQL support classes and re-run identity guards only for explicitly targeted rows.
- Run an independent SQLSolver setup/smoke path to compare verifier behavior.
- Keep Semantic Equivalence Rate N.A. or coverage-limited in any public-facing context.
