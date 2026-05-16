# Risk Notes

- Portability risk: `identifier_quoting`, `order_direction_gap`, `limit_fetch_gap`.
- Likely hard-negative failure mode: the ordering direction changes the selected earliest non-null driver row into the latest non-null driver row.
- Common-core feasibility: plausible, but still candidate-only and not reviewed.
- Construction risk: low.
- Blockers before registry writeback:
  - witness fixture is draft-only and not yet loaded
  - checker remains draft-only until execution evidence exists
  - Spark adaptation still needs execution review
  - no tri-engine validation has been run
