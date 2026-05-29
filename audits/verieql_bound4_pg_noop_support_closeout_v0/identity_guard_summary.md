# Identity Guard Summary

Identity-guard source:

- `audits/verieql_pg_noop_identity_guard_reclassification_v0/`

Policy:

- A source-vs-candidate verdict may enter corrected `V_equiv` or corrected `V_non` only if both source-vs-source and candidate-vs-candidate normalize to `equivalent` under the same verifier policy.

Counts:

- Identity-checked rows: 35
- Identity-passed rows: 4
- Identity-failed rows: 31

Identity-passed rows:

- `CONS_0036`
- `CONS_0037`
- `PORT_0003`
- `PORT_0005`

Identity-failed categories:

- `identity_guard_failed_unsupported`: 16
- `identity_guard_failed_timeout`: 8
- `identity_guard_failed_not_implemented`: 5
- `identity_guard_failed_tool_error`: 1
- `identity_guard_failed_non_equivalent`: 1

`LONGTAIL_0023` remains `identity_guard_failed_non_equivalent` and is excluded from corrected `V_non`.
