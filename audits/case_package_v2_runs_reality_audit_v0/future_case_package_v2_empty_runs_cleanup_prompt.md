# Future Prompt: case_package_v2_empty_runs_cleanup_v0

Repository:
- Work only in `/home/tianci_gao/code/Rewritebench_v0`.
- Work only on branch `feature/case-package-v2-external-schema`.
- Do not modify `main`.
- Do not inspect or modify the legacy repo.

Task title:
`case_package_v2_empty_runs_cleanup_v0`

This is a branch-only cleanup task limited to audited empty or placeholder-only case-local `runs/` directories.

This is NOT retained-evidence deletion.
This is NOT evidence deletion.
This is NOT case conversion.
This is NOT DB/checker execution.
This is NOT official metric computation.
This is NOT reports/results migration.
This is NOT denominator update.
This is NOT case_sets update.
This is NOT global leaderboard creation.

Read first:
- `audits/case_package_v2_runs_reality_audit_v0/runs_reality_audit_summary.md`
- `audits/case_package_v2_runs_reality_audit_v0/case_local_runs_inventory.csv`
- `audits/case_package_v2_runs_reality_audit_v0/runs_classification_summary.csv`
- `audits/case_package_v2_runs_reality_audit_v0/runs_policy_refinement_matrix.csv`
- `project_control/DECISION_LOG.md`
- `repository_spec/case_package_contract_v2_draft.md`
- `repository_spec/external_evidence_contract_v1_draft.md`

Goal:
Delete only case-local `runs/` directories classified as `empty_directory` or `placeholder_only` in the accepted audit.

Hard boundaries:
- Do not delete any `runs/` directory classified as `retained_evidence_present`, `local_or_private_trace_present`, `raw_log_or_debug_trace_present`, or `manual_review_required`.
- Do not delete case-local `evidence/`.
- Do not modify schemas, case_sets, inventory, reports, results, denominators, paper results, metrics, DB/checker outputs, or leaderboard outputs.
- Use explicit `git add` paths only.

Required validation:
- Recompute runs inventory before deletion and stop if any target classification changed.
- Delete only audited empty/placeholder-only directories.
- Confirm no retained evidence, evidence, schemas, case_sets, inventory, reports/results, denominators, paper results, DB/checker outputs, metrics, or leaderboard outputs changed.
- Record removed paths and skipped paths in a new audit directory.
