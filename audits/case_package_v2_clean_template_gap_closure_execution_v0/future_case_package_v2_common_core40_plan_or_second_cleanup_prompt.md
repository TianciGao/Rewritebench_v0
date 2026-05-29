# Future Prompt: case_package_v2_common_core40_plan_or_second_cleanup_v0

Work only on `feature/case-package-v2-external-schema` in `/home/tianci_gao/code/Rewritebench_v0`.

Use `audits/case_package_v2_clean_template_gap_closure_execution_v0/` as input. If the five pilot cases are accepted with explicit blockers, draft a Common-core 40 conversion plan only; do not convert cases. If clean-template-minimal status is required first, plan a second targeted cleanup that handles only:

- checker/witness evidence reference migration away from case-local `evidence/`,
- replacement or archival decision for old engine-specific validation scripts,
- deletion of case-local schema engine directories only after validation-script references are gone,
- deletion of case-local evidence only after retained evidence mapping and references are verified,
- explicit review of `PORT_0003/sql/dialect_variants/`.

Do not run DB/checker execution. Do not compute official metrics. Do not change case_sets, inventory, reports, results, denominators, paper results, retained evidence, or leaderboard outputs.
