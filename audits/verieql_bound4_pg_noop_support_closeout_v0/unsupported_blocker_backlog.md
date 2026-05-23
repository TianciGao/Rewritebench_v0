# Unsupported Blocker Backlog

Current blocker categories after identity guard:

- Unsupported: 16 exact rows
- Timeout: 8 exact rows
- Not implemented: 5 exact rows
- Tool error: 1 exact row
- Identity non-equivalent: 1 exact row

Representative blockers:

- `LONGTAIL_0023`: identity non-equivalent, likely VeriEQL modeling/tool-semantics gap.
- `PORT_0012`: tool error in prior all-exact attempt.
- LIKE-related rows: remain not implemented.
- Subquery/EXISTS/set-operation rows: remain unsupported-heavy.
- Some aggregate/date/function-heavy rows remain timeout-prone under bound 4.

Backlog direction:

- Do not expand paper-facing VeriEQL SER until identity failures and support classes are addressed.
- If VeriEQL work continues, target one blocker class at a time and require identity guard before source-vs-candidate classification.
- Keep all non-decidable categories visible.
