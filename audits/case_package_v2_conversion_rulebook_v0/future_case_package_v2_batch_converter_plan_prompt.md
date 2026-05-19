# Future Prompt: case_package_v2_batch_converter_plan_v0

Task title: `case_package_v2_batch_converter_plan_v0`

Work only on branch `feature/case-package-v2-external-schema`.

Goal: perform a read-only converter dry-run over:

- `PERF_0006`
- `PERF_0007`
- `CONS_0005`
- `PORT_0003`
- `LONGTAIL_0011`

Use:

- `repository_spec/case_package_v2_conversion_rulebook_draft.md`
- `audits/case_package_v2_conversion_rulebook_v0/v2_file_disposition_matrix.csv`
- `audits/case_package_v2_conversion_rulebook_v0/v2_manifest_field_contract.csv`
- `audits/case_package_v2_conversion_rulebook_v0/v2_validation_consolidation_matrix.csv`
- `audits/case_package_v2_conversion_rulebook_v0/v2_evidence_runs_disposition_matrix.csv`
- `audits/case_package_v2_conversion_rulebook_v0/v2_batch_conversion_algorithm.md`

Do not convert files yet.

Required output:

- per-case read-only inventory
- per-case file disposition plan
- schema externalization plan
- evidence externalization plan
- validation wrapper consolidation plan
- retention mapping blockers
- stop-condition report
- recommended first writable batch scope

Hard boundaries:

- do not modify case files
- do not modify schemas
- do not modify evidence
- do not modify case_sets
- do not modify inventory
- do not modify reports or results
- do not change denominators
- do not change paper results
- do not run DB/checker execution
- do not compute metrics
- do not render paper tables
- do not create leaderboard output
- do not merge to main

Validation:

- branch check
- CSV/header checks
- JSON parse
- protected path checks
- `git diff --check`

Next task after the dry-run:

- authorize a bounded writable converter pilot only for cases whose read-only disposition plans have no stop-condition blockers.
