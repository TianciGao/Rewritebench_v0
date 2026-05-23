# Exact Gate Review

Source run row: `runs/user/common_core_pg_noop_db_checker/ledger.csv`

Gate fields for `LONGTAIL_0023`:

- selected: `true`
- source executable: `source_execution_success`
- candidate generated: `true`
- candidate executable: `candidate_execution_success`
- checker status: `checker_success`
- exact status: `exact`
- failure bucket: `none`

Source result path:

- `runs/user/common_core_pg_noop_db_checker/workspaces/LONGTAIL_0023/postgres/execution/source_result.jsonl`

Candidate result path:

- `runs/user/common_core_pg_noop_db_checker/workspaces/LONGTAIL_0023/postgres/execution/candidate_result.jsonl`

Conclusion:

- `LONGTAIL_0023` passed the exact/result-consistency gate again.
- The gate only made the row eligible for verifier triage; it was not used as formal verifier equivalence evidence.
