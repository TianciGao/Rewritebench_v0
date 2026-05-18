# Future Prompt: overnight_non_common_core_case_package_standardization_wave_002_policy_approved

Use `audits/wave002_policy_readme_schema_guard_v0/wave002_candidate_selection_after_policy.csv` as the candidate queue.

Migrate only cases with `new_wave002_bucket` equal to `wave_002_auto_migration_candidate` or `wave_002_policy_approved_candidate`. Skip manual-review and backlog cases.

For every migrated case:

- Use `repository_spec/case_readme_public_template_v1.md` for README content.
- Use `repository_spec/package_validation_summary_schema_v1.md` for `evidence/package_validation_summary.json`.
- Create `evidence/runs_retention.yaml` with archive-mapped or excluded unsafe evidence; do not copy raw legacy runs wholesale.
- Mark static-inferred hard-negative reason as `needs_review` when applicable and do not create paper-facing approval.
- Retain validation scripts only as assets with output-policy caveats unless separately authorized to execute them.
- Skip any case requiring raw logs, stdout/stderr/debug payloads, prompt/token/API/model traces, local-path artifact publication, DB execution, timing reruns, metrics, paper tables, reports/results updates, denominator changes, paper-result changes, case-set changes, or raw legacy evidence modification.

Keep `case_sets/`, denominators, reports/results, paper results, metrics, paper tables, and raw legacy evidence unchanged.
