# Extraction Results

Rows selected:
- 6.

Provider response:
- No provider response was received because no live provider call was attempted.

Extraction status:
- `not_attempted` for all 6 rows.

Candidate generation:
- 0 candidates generated.

Fail-closed bucket:
- Adapter status bucket: `missing_api_key` for all 6 rows.
- User ledger bucket: `no_candidate_sql` for all 6 rows, because the adapter exited cleanly without writing candidate SQL.

Interpretation:
- This validates the fail-closed live gate for missing credentials.
- It does not validate GPTSAPI response shape, single-SQL extraction from a live response, candidate semantics, or execution/checker behavior.
