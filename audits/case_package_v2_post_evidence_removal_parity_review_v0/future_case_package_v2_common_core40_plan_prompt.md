# Future Prompt: case_package_v2_common_core40_conversion_plan_v0

Repository:
- Work only in `/home/tianci_gao/code/Rewritebench_v0`.
- Work only on branch `feature/case-package-v2-external-schema`.
- Do not modify main.
- Do not inspect or modify the legacy repo.

Task title:
`case_package_v2_common_core40_conversion_plan_v0`

This is a branch-only read-only planning task.

This is NOT conversion execution.
This is NOT DB/checker execution.
This is NOT official metric computation.
This is NOT reports/results migration.
This is NOT denominator update.
This is NOT case_sets update.
This is NOT global leaderboard creation.

Goal:
Use the accepted five-case clean-template-minimal v2 pilot as the template for planning Common-core 40 conversion. The plan should define case ordering, layer ordering, risk classes, required resolver/validator expectations, and protected-boundary checks before any writable Common-core 40 conversion is authorized.

Required inputs:
- `project_control/MIGRATION_MASTER_PLAN.md`
- `project_control/MIGRATION_STATUS.md`
- `project_control/DECISION_LOG.md`
- `project_control/MIGRATION_RUN_LOG.md`
- All five-case v2 pilot audit outputs through `case_package_v2_post_evidence_removal_parity_review_v0`
- `case_sets/common_core_v0/`
- `inventory/`
- v2 repository specs under `repository_spec/`

Required outputs:
- Common-core 40 conversion planning summary
- Case-by-case readiness and risk matrix
- Layer-by-layer conversion plan
- Protected-boundary matrix
- Future writable execution prompt
- Summary JSON
- Command log

Hard boundaries:
- Do not modify cases.
- Do not modify schemas.
- Do not modify evidence.
- Do not modify case_sets or inventory.
- Do not modify reports/results.
- Do not change denominators or paper results.
- Do not compute official metrics.
- Do not run DB/checker execution.
- Do not create leaderboard output.
- Do not use `git add .`.

Exact next action after plan:
Maintainer review decides whether to authorize a bounded writable Common-core 40 conversion execution task.
