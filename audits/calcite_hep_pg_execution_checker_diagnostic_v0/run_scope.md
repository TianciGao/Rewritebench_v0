# Run Scope

Input scope:

- Source audit: `audits/calcite_hep_pg_bounded_candidate_generation_v0/`
- Source candidate CSV: `audits/calcite_hep_pg_bounded_candidate_generation_v0/per_row_candidate_status.csv`
- Case set: `common_core_v0`
- Engine: `postgres`
- Route/method: `calcite_hep_fail_closed`
- Selected rows: 40
- Generated candidate rows: 33
- No-candidate rows preserved: 7

Execution/checker scope:

- Executed only rows with `candidate_generated=true` in the prior audit.
- Preserved no-candidate rows as `not_attempted_no_candidate` / `no_candidate_sql`.
- Ran PostgreSQL source/candidate execution through the existing PostgreSQL execution helper.
- Ran the local result checker only when both source and candidate execution succeeded.
- Timing and verifier passes were not run.

A preliminary user-entry replay path was discarded because the existing user-entry PORT role mapping can use cross-dialect source-reference execution for generated PORT rows. The committed audit result is produced by the PostgreSQL-only helper in this packet.
