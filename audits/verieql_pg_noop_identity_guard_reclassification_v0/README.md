# verieql_pg_noop_identity_guard_reclassification_v0

Task mode: local diagnostic verifier-support reclassification.

Branch: `feature/case-package-v2-external-schema`

Source run: `runs/user/common_core_pg_noop_db_checker`

Prior ledger: `audits/verieql_bound4_pg_noop_all_exact_attempt_v0/per_row_verdicts.csv`

Uniform verifier policy:

- `verifier_tool=verieql`
- `verifier_mode=finite_bound`
- `bound_size=4`
- `timeout_seconds=30`
- `cores=1`

Verdict: identity guard reclassification completed for all 35 exact SQLGlot-noop PostgreSQL rows. Only 4 rows passed both source-vs-source and candidate-vs-candidate identity sanity. The corrected local diagnostic denominator contains 4 equivalent rows and 0 non-equivalent rows. `LONGTAIL_0023` remains excluded because its source-vs-source and candidate-vs-candidate checks also fail identity sanity.

Counts:

- Selected rows: 40
- Exact candidate rows: 35
- Identity-checked rows: 35
- Identity-passed rows: 4
- Identity-failed rows: 31
- Corrected equivalent rows: 4
- Corrected non-equivalent rows: 0
- Corrected decidable rows: 4
- Corrected local diagnostic SER: 1.0 over 4 identity-passing decidable rows
- Corrected verifier decidability coverage over exact rows: 4/35

Paper boundary: not feasible for paper-facing promotion. The corrected rate is local-only and coverage-limited.
