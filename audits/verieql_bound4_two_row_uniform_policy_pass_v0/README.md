# verieql_bound4_two_row_uniform_policy_pass_v0

Local-only, exact-gated, two-row VeriEQL finite-bound pass under one uniform declared verifier policy:

- `verifier_mode=finite_bound`
- `bound_size=4`
- `timeout_seconds=30`
- `cores=1`

Rows:
- `CONS_0036`
- `CONS_0037`

Source:
- SQLGlot noop
- PostgreSQL
- `runs/user/common_core_pg_noop_db_checker`

Verdict:
- Both rows were found in the source run.
- Both rows passed the exact/result-consistency gate.
- Both rows were attempted under the same declared verifier policy.
- `CONS_0036` returned clean all-`EQU` and normalized to `equivalent`.
- `CONS_0037` returned clean all-`EQU` and normalized to `equivalent`.

Local diagnostic summary:
- selected rows: 2
- exact candidate rows: 2
- verifier attempted rows: 2
- equivalent count: 2
- non-equivalent count: 0
- decidable count: 2
- `local_bound4_two_row_semantic_equivalence_rate`: 1.0
- `verifier_decidability_rate`: 1.0
- `verifier_eligibility_rate`: 1.0

This result is tied only to the declared `bound_size=4` policy. It does not imply equivalence under `bound_size=10`, does not mix with earlier bound-10 results, and is not official Semantic Equivalence Rate.

