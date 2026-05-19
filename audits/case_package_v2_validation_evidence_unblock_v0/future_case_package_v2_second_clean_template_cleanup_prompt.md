# Future Prompt: case_package_v2_second_clean_template_cleanup_v0

Work only in `/home/tianci_gao/code/Rewritebench_v0` on branch `feature/case-package-v2-external-schema`.

Use `audits/case_package_v2_validation_evidence_unblock_v0/` as input. This is a cleanup execution task only for the five pilot cases: `PERF_0006`, `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011`.

Allowed deletion candidates after reconfirmation:

- old engine-specific validation scripts listed as `deletion_ready_after_wrapper_update`,
- case-local `schema/<engine>/` directories only after old scripts are deleted or proven absent from live references,
- case-local `evidence/` directories only after external `evidence/cases/<POOL>/<CASE_ID>/` copies and manifest/checker/witness references are revalidated.

Do not delete `PORT_0003/sql/dialect_variants/` unless a separate portability review approves it. Do not modify case_sets, inventory, reports, results, denominator values, paper results, official metrics, DB/checker execution outputs, or leaderboard outputs. Do not run DB/checker execution.
