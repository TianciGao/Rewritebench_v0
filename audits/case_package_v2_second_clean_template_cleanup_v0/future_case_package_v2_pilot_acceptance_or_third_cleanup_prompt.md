# Future Prompt: case_package_v2_pilot_acceptance_or_third_cleanup_v0

Repository:
- Work only in `/home/tianci_gao/code/Rewritebench_v0`.
- Work only on branch `feature/case-package-v2-external-schema`.
- Do not inspect or modify the legacy repo.

Task:
- If the five-case pilot is accepted as clean-template-minimal with `PORT_0003/sql/dialect_variants/` retained as an optional v2 asset, produce a read-only Common-core 40 conversion plan.
- If maintainers do not accept the optional dialect-variant status, perform only a read-only portability review for `PORT_0003/sql/dialect_variants/`.

Hard boundaries:
- Do not run DB/checker execution.
- Do not compute official metrics.
- Do not modify case_sets, inventory, reports, results, denominators, paper results, or leaderboard outputs.
- Do not delete retained evidence or dialect variants without a separate explicit maintainer decision.

Required inputs:
- `audits/case_package_v2_second_clean_template_cleanup_v0/second_clean_template_cleanup_summary.md`
- `audits/case_package_v2_second_clean_template_cleanup_v0/second_cleanup_post_parity_case_summary.csv`
- `audits/case_package_v2_second_clean_template_cleanup_v0/second_cleanup_post_path_gap_matrix.csv`

Expected output:
- A branch-only audit/plan stating whether to proceed to Common-core 40 conversion planning or to run a narrow dialect-variant review first.
