# Calcite HEP PostgreSQL Bounded Candidate Generation

Task: `calcite_hep_pg_bounded_candidate_generation_v0`

Branch: `feature/case-package-v2-external-schema`

Verdict: bounded PostgreSQL-only candidate generation completed locally for the Calcite HEP fail-closed route. The pass selected 40 Common-core v0 PostgreSQL rows, invoked the adapter for 40, generated 33 candidate SQL files, and failed closed on 7 rows.

This audit is candidate-generation only. It did not execute database queries, run the result checker, collect timing, run verifiers, compute official metrics, update paper reports/results, or promote retained evidence.

Runtime root: `/tmp/sqlrb_calcite_hep_pg_bounded_candidate_generation_v0`

D035 output root used under `/tmp`:

- `/tmp/sqlrb_calcite_hep_pg_bounded_candidate_generation_v0/output/results/calcite_hep_pg_candidate_generation/`
- `/tmp/sqlrb_calcite_hep_pg_bounded_candidate_generation_v0/output/logs/calcite_hep_pg_candidate_generation/`
- `/tmp/sqlrb_calcite_hep_pg_bounded_candidate_generation_v0/output/reports/calcite_hep_pg_candidate_generation/`

Primary artifacts in this packet:

- `per_row_candidate_status.csv`
- `diagnostic_summary.json`
- `candidate_generation_summary.md`
- `generated_candidate_review.md`
- `fail_closed_review.md`
