# Paper Table Boundary

This audit is local diagnostic verifier-support evidence only.

It is not:

- official Semantic Equivalence Rate
- official metrics
- paper results
- retained evidence promotion
- leaderboard input

Paper-facing feasibility:

- Not ready.
- Decidable coverage is 5 of 35 exact rows.
- One `non_equivalent` row was reported by VeriEQL and must be investigated before any promotion.
- The outcome ledger can inform future feasibility work, but it must not be rendered as a paper table value.

If a future paper-facing Semantic Equivalence Rate row is considered, it must include:

- the exact verifier policy
- verifier-attempt coverage over exact rows
- verifier-decidable coverage over exact rows
- counts for timeout, unsupported, not implemented, syntax error, unknown, OOM, tool error, and not attempted
- investigation results for any `non_equivalent` row
