# verieql_cons0036_cons0037_two_row_exact_candidate_pass_v0

Local-only bounded VeriEQL finite-bound exact-candidate pass for two SQLGlot-noop PostgreSQL rows from `runs/user/common_core_pg_noop_db_checker`.

Rows:
- `CONS_0036`
- `CONS_0037`

Verdict:
- Both rows were found in the source run and passed the exact/result-consistency gate.
- Both rows were attempted by VeriEQL finite-bound mode with `bound_size=10`, `timeout_seconds=30`, and `cores=1`.
- `CONS_0036` returned clean all-`EQU` states and normalized to `equivalent`.
- `CONS_0037` reached VeriEQL with corrected schema metadata, including `DEPT.NAME=VARCHAR(32)`, but returned `EQU|EQU|EQU|EQU|TMO` and normalized to `timeout`.
- The DDL parser blocker for `CONS_0037` is resolved, but the row is not decidable at this bound/timeout.

Local diagnostic summary:
- selected rows: 2
- exact candidate rows: 2
- verifier attempted rows: 2
- equivalent count: 1
- non-equivalent count: 0
- timeout count: 1
- decidable count: 1
- `local_two_row_semantic_equivalence_rate`: 1.0 over the one decidable row
- `verifier_decidability_rate`: 0.5
- `verifier_eligibility_rate`: 1.0

This is not official Semantic Equivalence Rate, not paper evidence, not retained evidence, and not leaderboard input.

Packet contents:
- `selection_review.md`
- `exact_gate_review.md`
- `verifier_pair_shape_review.md`
- `verifier_results_summary.md`
- `semantic_equivalence_rate_readiness.md`
- `per_row_verdicts.csv`
- `diagnostic_summary.json`
- `command_log.md`
- `protected_surface_check.md`
- `boundary_checklist.md`

