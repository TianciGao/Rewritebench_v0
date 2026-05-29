# Identity Guard Policy

A source-vs-candidate VeriEQL verdict may enter the corrected local decidable denominator only if all conditions hold:

- source-vs-source normalizes to `equivalent`
- candidate-vs-candidate normalizes to `equivalent`
- source-vs-candidate normalizes to `equivalent` or `non_equivalent`

Rows fail the identity guard when either identity pair returns:

- `non_equivalent`
- `timeout`
- `unsupported`
- `not_implemented`
- `tool_error`
- `syntax_error`
- `unknown`
- `out_of_memory`
- any other non-equivalent status

Failure labels:

- `identity_guard_failed_non_equivalent`
- `identity_guard_failed_timeout`
- `identity_guard_failed_unsupported`
- `identity_guard_failed_not_implemented`
- `identity_guard_failed_tool_error`
- `identity_guard_failed_other`

Rows failing the identity guard are excluded from corrected `V_equiv` and corrected `V_non`.

This guard is local diagnostic policy for this audit. It is not a durable project decision and does not update `DECISION_LOG.md`.
