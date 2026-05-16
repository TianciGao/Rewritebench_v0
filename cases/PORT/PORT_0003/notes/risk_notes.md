# Risk Notes

- Portability risk: `identifier_quoting`, `null_semantics_gap`, `limit_fetch_gap`.
- Likely hard-negative failure mode: a naive top-1 ordering rewrite mishandles null placement or flips the absolute-longitude ranking direction.
- Witness rows intended to expose the failure: one `NULL` longitude row plus competing positive and negative longitude magnitudes with distinct `gsoffered` labels.
- Common-core feasibility: plausible, but still candidate-only and not reviewed.
- Construction risk: low.
- Blockers before registry writeback:
  - witness rows are still draft fixtures and have not been loaded
  - checker is draft-only and not executed
  - Spark adaptation still needs review
  - no tri-engine validation has been run
  - common-core vs extended status remains unresolved
