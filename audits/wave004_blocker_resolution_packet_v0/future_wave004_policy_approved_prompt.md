# Future Prompt: overnight_non_common_core_case_package_standardization_wave_004_policy_approved

Use this only after a separate blocker-resolution follow-up promotes one or more rows in `audits/wave004_blocker_resolution_packet_v0/wave004_candidate_selection_after_blocker_resolution.csv` to `new_wave004_bucket = wave_004_policy_approved_candidate`.

Task boundaries:

- Migrate only rows with `new_wave004_bucket = wave_004_policy_approved_candidate`.
- Skip manual-review, backlog-defer, and orphan/unregistered rows.
- Reuse `repository_spec/case_readme_public_template_v1.md`.
- Reuse `repository_spec/package_validation_summary_schema_v1.md`.
- Keep `case_sets/` unchanged.
- Keep denominators unchanged.
- Keep reports/results unchanged.
- Keep paper results unchanged.
- Do not compute metrics or render paper tables.
- Do not modify raw legacy evidence or the legacy repository.
- Skip unsafe cases and write deferred dossiers.

If the candidate file still contains zero policy-approved rows, stop and report that wave004 migration remains blocked.
