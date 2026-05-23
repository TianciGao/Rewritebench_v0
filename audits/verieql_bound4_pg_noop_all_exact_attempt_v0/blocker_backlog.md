# Blocker Backlog

Main blocker categories from this pass:

- Unsupported SQL features: 16 rows normalized to `unsupported`, mostly subquery/EXISTS/set-operation or other unsupported shapes.
- Not implemented: 5 rows normalized to `not_implemented`, including known LIKE-related rows and `PORT_0008`.
- Timeout: 8 rows remained timeout-prone under `bound_size=4`, `timeout_seconds=30`.
- Tool error: 1 row, `PORT_0012`, emitted `OTE` with `list index out of range`.
- Non-equivalent investigation: 1 row, `LONGTAIL_0023`, emitted `EQU|NEQ`.

Required follow-up before any promotion:

- Investigate `LONGTAIL_0023` as a possible VeriEQL limitation, schema/constraint issue, or true formal refutation.
- Investigate `PORT_0012` `OTE` as a tool/parser issue.
- Keep rows with `NSE`, `NIE`, `TMO`, or `OTE` visible and outside the decidable denominator.
- Do not use local result checker exactness to override any verifier status.

Full Common-core exact-candidate verifier pass remains blocked for paper-facing use because decidable coverage is low and at least one non-equivalent diagnostic result exists.
