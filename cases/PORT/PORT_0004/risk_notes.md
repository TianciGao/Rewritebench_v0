# Risk Notes

- Portability risk: `identifier_quoting`, `datetime_semantics_gap`, `type_semantics_gap`.
- Likely hard-negative failure mode: the year-filter rewrite shifts from 1980 to 1981 and changes the aggregate percentage.
- Witness rows intended to expose the failure: mixed RA and non-RA patients with 1980 and 1981 birthdays and both female and non-female rows.
- Common-core feasibility: plausible, but still candidate-only and not reviewed.
- Construction risk: low.
- Blockers before registry writeback:
  - witness rows are still draft fixtures and have not been loaded
  - aggregate checker behavior is only drafted
  - Spark rewrite still needs review
  - no validation evidence exists yet
  - common-core vs extended status remains unresolved
