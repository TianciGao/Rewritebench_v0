# Future Prompt: case_package_v2_post_empty_runs_parity_review_v0

Repository:
- Work only in `/home/tianci_gao/code/Rewritebench_v0`.
- Work only on branch `feature/case-package-v2-external-schema`.
- Do not modify `main`.
- Do not inspect or modify the legacy repo.

Task title:
`case_package_v2_post_empty_runs_parity_review_v0`

This is a branch-only read-only parity review after placeholder-only case-local `runs/` cleanup.

This is NOT cleanup execution, case conversion, DB/checker execution, official metric computation, reports/results migration, denominator update, case_sets update, or leaderboard creation.

Read first:
- `audits/case_package_v2_empty_runs_cleanup_v0/empty_runs_cleanup_summary.md`
- `audits/case_package_v2_empty_runs_cleanup_v0/empty_runs_deleted_manifest.csv`
- `audits/case_package_v2_empty_runs_cleanup_v0/empty_runs_cleanup_skipped.csv`
- `audits/case_package_v2_post_cleanup_parity_review_v0/post_cleanup_path_gap_matrix.csv`

Goal:
Recompute clean-template parity after removal of audited placeholder-only case-local `runs/` directories. Confirm remaining gaps are limited to case-local evidence, schema engine compatibility files, metadata/data compatibility, validation legacy scripts, and any explicitly documented manual-review paths.

Hard boundaries:
- Do not modify case files.
- Do not delete evidence, schemas, reports, results, or retained evidence.
- Do not modify case_sets, inventory, denominators, paper results, metrics, DB/checker outputs, or leaderboard outputs.
