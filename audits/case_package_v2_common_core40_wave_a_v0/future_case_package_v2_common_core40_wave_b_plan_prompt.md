# Future Prompt: case_package_v2_common_core40_wave_b_plan_v0

Repository:
- Work only in `/home/tianci_gao/code/Rewritebench_v0`.
- Work only on branch `feature/case-package-v2-external-schema`.
- Do not modify main or inspect the legacy repo.

Task title: `case_package_v2_common_core40_wave_b_plan_v0`

This is a branch-only read-only planning task for Wave B Common-core v2 conversion.

Scope:
- Use the accepted five-case pilot and converted Wave A cases as templates.
- Plan only the 22 Wave B schema-grouped non-PORT Common-core cases.
- Do not perform writable conversion, cleanup, DB/checker execution, official metric computation, reports/results migration, denominator update, case_sets update, or leaderboard creation.

Required plan:
- Group cases by verified source family and schema compatibility.
- Identify where grouped external schemas are safe and where per-case schemas are required.
- Produce a folder-ordered conversion prompt for the first Wave B batch.
- Preserve regeneration-first `evidence_policy` and clean-template-minimal case-local shape.
- Keep protected benchmark surfaces unchanged.
