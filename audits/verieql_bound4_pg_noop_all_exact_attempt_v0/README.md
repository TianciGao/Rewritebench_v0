# verieql_bound4_pg_noop_all_exact_attempt_v0

Task mode: local-only verifier-support attempt.

Branch: `feature/case-package-v2-external-schema`

Source run: `runs/user/common_core_pg_noop_db_checker`

Uniform verifier policy:

- `verifier_tool=verieql`
- `verifier_mode=finite_bound`
- `bound_size=4`
- `timeout_seconds=30`
- `cores=1`

Verdict: the all-exact PostgreSQL SQLGlot-noop VeriEQL attempt completed locally and produced a visible outcome ledger for all 40 selected rows. VeriEQL was attempted for the 35 exact/result-consistent rows. The 5 non-exact PORT rows were recorded as `not_attempted_ineligible`.

Summary:

- Selected rows: 40
- Exact/result-consistent rows: 35
- Verifier-attempted rows: 35
- Decidable rows: 5
- Equivalent rows: 4
- Non-equivalent rows: 1
- Timeout rows: 8
- Unsupported rows: 16
- Not-implemented rows: 5
- Tool-error rows: 1
- Not-attempted ineligible rows: 5

Local diagnostic rate:

- `local_bound4_pg_noop_semantic_equivalence_rate=0.8`
- This is over 5 decidable rows only.
- This is not official Semantic Equivalence Rate and is not paper evidence.

Coverage:

- `verifier_decidability_rate=0.14285714285714285`
- `verifier_decidable_coverage_over_exact_rows=0.14285714285714285`

Paper-facing conclusion: coverage is too low and one `non_equivalent` row appears, so paper-facing Semantic Equivalence Rate remains not ready for promotion.
