# Future Prompt: case_package_v2_pilot_acceptance_or_common_core40_plan_v0

Task title:
`case_package_v2_pilot_acceptance_or_common_core40_plan_v0`

Repository:
- Work only in `/home/tianci_gao/code/Rewritebench_v0`.
- Work only on branch `feature/case-package-v2-external-schema`.
- Do not modify `main`.
- Do not inspect or modify the legacy repository.

Purpose:
Review the five-case v2 pilot after the clean-template cleanup readiness pass and decide whether the pilot is accepted for a Common-core 40 conversion plan, or whether an additional compatibility-reference cleanup planning task is required first.

Required inputs:
- `audits/case_package_v2_template_parity_gap_review_v0/`
- `audits/case_package_v2_clean_template_cleanup_pilot_v0/`
- Current v2 pilot case packages for `PERF_0006`, `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011`.

Scope:
- Read-only planning unless separately authorized.
- Do not delete retained evidence.
- Do not delete case-local schema engine files.
- Do not delete metadata, data fixtures, or validation engine-specific scripts.
- Do not run DB/checker execution.
- Do not compute official metrics.
- Do not update denominators, paper results, reports/results, `case_sets/`, or inventory.
- Do not create leaderboard output.

Decision points:
- Whether live compatibility refs should be removed before deleting nested SQL, copied notes, or placeholder runs.
- Whether the five-case pilot is accepted as a v2 branch pilot despite remaining compatibility directories.
- Whether to authorize a Common-core 40 conversion plan using the folder-ordered v2 rulebook.

Expected output:
- Pilot acceptance or blocker review packet.
- Explicit next safe action.
