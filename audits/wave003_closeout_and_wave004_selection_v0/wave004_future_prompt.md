# Future Prompt: overnight_non_common_core_case_package_standardization_wave_004

Use `audits/wave003_closeout_and_wave004_selection_v0/wave004_candidate_selection.csv` as the only candidate source.

Migrate only rows where `wave004_bucket` is `wave_004_auto_migration_candidate` or `wave_004_policy_approved_candidate`. If the eligible count remains zero, stop and report that wave 004 has no migration candidates under current guardrails.

Skip rows marked `wave_004_manual_review_required`, `wave_004_backlog_defer`, or `orphan_or_unregistered_review`.

Reuse `repository_spec/case_readme_public_template_v1.md` and `repository_spec/package_validation_summary_schema_v1.md`.

Do not change `case_sets/`, denominators, reports/results, paper results, case membership, metrics, paper tables, or raw legacy evidence. Do not run DB engines, timing workloads, LLM calls, or validation scripts requiring external services. Fail closed for unsafe cases.
