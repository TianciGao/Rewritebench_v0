# Future Prompt: case_package_v2_reference_cleanup_execution_v0

Repository:
- Work only in `/home/tianci_gao/code/Rewritebench_v0`.
- Work only on branch `feature/case-package-v2-external-schema`.
- Do not modify `main`.
- Do not inspect or modify the legacy repository.

Task title:
`case_package_v2_reference_cleanup_execution_v0`

Purpose:
Update live compatibility references and delete only candidates classified as `deletion_ready_after_reference_update` in:

`audits/case_package_v2_reference_cleanup_plan_v0/deletion_readiness_after_reference_cleanup.csv`

Pilot cases:
- `PERF_0006`
- `PERF_0007`
- `CONS_0005`
- `PORT_0003`
- `LONGTAIL_0011`

Allowed cleanup scope:
- Update manifest/README/checker/metadata/validation references that point at nested SQL compatibility paths or copied case-local notes.
- Delete only nested SQL compatibility dirs and copied case-local notes after all live references are updated and static validation passes.
- Do not delete `runs/` unless a separate retained-runs cleanup authorization covers `deletion_ready_after_retention_mapping` candidates.

Hard boundaries:
- Do not delete retained evidence.
- Do not delete case-local evidence without retention mapping.
- Do not delete schema engine DDL/load files.
- Do not delete metadata source-of-truth files unless a separate metadata merge task authorizes it.
- Do not delete data fixtures.
- Do not delete engine-specific validation scripts unless a shared-logic/caller audit explicitly authorizes it.
- Do not delete PORT dialect variants.
- Do not modify `case_sets/`, inventory, reports, results, denominators, paper results, or raw legacy evidence.
- Do not run DB/checker execution.
- Do not compute official metrics.
- Do not render paper tables.
- Do not create global leaderboard output.
- Do not use `git add .`.

Execution order:
1. Read the reference cleanup plan outputs.
2. For each `deletion_ready_after_reference_update` candidate, update live refs first.
3. Re-run the v2 static validator for the affected case.
4. Delete only paths with no remaining live references.
5. Re-run all five v2 validators and static boundary checks.
6. Record deleted paths, skipped paths, validation results, and protected-surface checks.

Required stop conditions:
- Any remaining live manifest, README, checker, metadata, validation-script, dev-script, or validator reference to a candidate path.
- Any candidate classified as `deletion_ready_after_retention_mapping`.
- Any retained evidence, schema engine file, metadata source-of-truth file, data fixture, validation engine-specific script, or PORT dialect variant proposed for deletion.
- Any `case_sets/`, inventory, reports/results, denominator, paper-result, DB/checker output, metric, or leaderboard change.

Expected commit:
`git commit -m "pilot: execute v2 compatibility reference cleanup"`
