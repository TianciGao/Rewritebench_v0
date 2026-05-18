You are working on SQL-RewriteBench clean public release migration / redevelopment.

Task title:
overnight_non_common_core_case_package_standardization_wave_003

This is a bounded non-Common-core case package standardization task. Use `audits/wave002_closeout_and_wave003_selection_v0/wave003_candidate_selection.csv` and migrate only rows where `wave003_bucket=wave_003_policy_approved_candidate`.

Candidate ids:
- PERF_0027
- PERF_0028
- PERF_0030
- PERF_0031
- PERF_0032
- PERF_0037
- PERF_0039
- PERF_0040
- PERF_0041
- PERF_0042
- PERF_0045
- PERF_0049
- PERF_0051
- PERF_0055
- PERF_0057
- PERF_0058
- PERF_0059
- PERF_0060
- PERF_0061
- PERF_0064
- PERF_0067
- PERF_0068
- PERF_0069
- PERF_0070
- PERF_0071
- PERF_0072
- PERF_0073
- PERF_0074
- PERF_0075
- PORT_0006

Hard boundaries:
- Do not migrate auto/manual/backlog/orphan rows.
- Do not modify the legacy repo.
- Do not modify `case_sets/`, denominators, reports/results, paper results, Common-core packages, or raw legacy evidence.
- Do not compute metrics or render paper tables.
- Do not run DB engines, timing workloads, LLM calls, or validation scripts requiring external services.
- Use `repository_spec/case_readme_public_template_v1.md` and `repository_spec/package_validation_summary_schema_v1.md`.
- Fail closed and write a deferred dossier for any case that violates public-hygiene or package-core guardrails.

Required next action:
Create canonical public-safe packages for only the selected wave 003 policy-approved cases and write a wave 003 audit packet with validation results.
