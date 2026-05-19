# V2 Compatibility Reference Cleanup Plan

Task: `case_package_v2_reference_cleanup_plan_v0`

Date: 2026-05-19

Branch: `feature/case-package-v2-external-schema`

## Purpose And Scope

This branch-only planning task identifies the remaining references that block clean-template cleanup for the five v2 pilot cases:

- `PERF_0006`
- `PERF_0007`
- `CONS_0005`
- `PORT_0003`
- `LONGTAIL_0011`

No case package, schema package, evidence directory, runs directory, benchmark surface, metric output, or leaderboard output was modified.

## Why Previous Cleanup Removed No Files

The previous cleanup pilot reviewed 15 candidates marked `ready_for_cleanup=true` but removed no files because live compatibility references still exist. The skipped candidates were:

- Five nested SQL compatibility candidates: `sql/positives/` and `sql/negatives/`.
- Five copied case-local notes candidates: `notes/`.
- Five placeholder-only case-local runs candidates: `runs/`.

Deleting those paths before reference cleanup would leave stale manifest, README, checker, metadata, validation-script, or dev-script references.

## Reference Categories

- `live_manifest_reference`: manifest fields or compatibility blocks that would become stale.
- `live_readme_reference`: public README text that would become inaccurate.
- `live_runtime_reference`: checker or retained config references that might be consumed by a runner/checker.
- `live_script_reference`: validation or dev scripts that still point at compatibility paths.
- `compatibility_block_reference`: legacy compatibility metadata that should be updated or removed when the compatibility path is removed.
- `historical_audit_reference`: prior audit files that record past state and should not block cleanup.
- `documentation_only_reference`: repository specs or historical docs that describe policy, not live case state.

## Live Blockers

Live blockers were found for every skipped candidate.

- Skipped candidates reviewed: 15.
- Live reference blocker rows recorded: 50.
- Historical/documentation exclusions recorded: 30.
- Nested SQL dirs are blocked by manifest `compatibility.sql_legacy`, checker YAML, old validation scripts, selected `metadata/artifact_paths.yaml`, and dev scripts that still inspect `sql/positives/` or `sql/negatives/`.
- Copied notes dirs are blocked by manifest `notes_legacy` and metadata note references, README wording, and selected old validation-script comments.
- Placeholder `runs/` dirs are blocked by manifest `runs_legacy`, README wording, and old validation scripts that still write into case-local `runs/`.

## Historical Or Audit-Only References

Historical references in older audits and repository specs should not block cleanup. They should remain unchanged unless a separate audit-rewrite task is explicitly authorized. Future cleanup should not try to rewrite prior audit logs, prior planning manifests, or historical migration reports.

## Deletion Readiness Summary

- `deletion_ready_after_reference_update`: 10 candidates. This covers nested SQL compatibility dirs and copied case-local notes after live refs are updated to direct SQL paths and external evidence notes.
- `deletion_ready_after_retention_mapping`: 5 candidates. This covers placeholder `runs/` dirs after manifest/README/script references are updated and retained-runs mapping is preserved.
- `manual_review_required`: 0 of the 15 skipped ready candidates. Manual review still applies to non-candidate areas such as schema engine files, metadata source-of-truth files, data fixtures, validation engine-specific scripts, retained evidence, and PORT dialect variants.

## Future Execution Recommendation

Run a writable reference cleanup execution task that first updates live references and then deletes only candidates classified as `deletion_ready_after_reference_update`. The future task should not delete retained evidence, schema engine files, metadata source-of-truth files, data fixtures, validation engine-specific scripts, or any candidate that still has live references after the update.

## Exact Next Safe Action

Authorize `case_package_v2_reference_cleanup_execution_v0` to update live compatibility references and delete only candidates classified as `deletion_ready_after_reference_update`, with static v2 validation after each case and no DB/checker execution, official metrics, reports/results changes, denominator changes, paper-result changes, retained-evidence deletion, or leaderboard output.
