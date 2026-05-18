# Wave 002 Policy-unlocked Batch Plan

## Candidate Counts

- Auto candidates: 0.
- Policy-approved candidates: 28.
- Manual-review required: 0.
- Backlog defer: 0.

## Recommended Wave 002 Target Size

Attempt up to 28 policy-approved candidates in one batch. Stop or defer any case whose concrete files violate the policy guardrails.

## Recommended Exclusions

Exclude any case that requires raw run copying, raw logs, stdout/stderr/debug payloads, prompt/token/API/model traces, local-path artifact publication, DB execution, timing reruns, metric computation, paper rendering, reports/results updates, denominator changes, paper-result changes, or case-set membership changes.

## Required Wave 002 Templates And Guards

- Use `repository_spec/case_readme_public_template_v1.md` for every package README.
- Use `repository_spec/package_validation_summary_schema_v1.md` for every case-local `evidence/package_validation_summary.json`.
- Keep repository-wide mutation claims in wave audit outputs and project-control files, not in case-local package summaries.

## Boundary Requirements

Wave 002 must not change `case_sets/`, denominators, reports/results, paper results, raw legacy evidence, metrics, paper tables, or case membership.

## Suggested Next Codex Task Title

`overnight_non_common_core_case_package_standardization_wave_002_policy_approved`
