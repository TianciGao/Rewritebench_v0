# Future Prompt: case_package_v2_post_cleanup_parity_review_v0

Repository:
- Work only in `/home/tianci_gao/code/Rewritebench_v0`.
- Work only on branch `feature/case-package-v2-external-schema`.
- Do not modify `main`.
- Do not inspect or modify the legacy repository.

Task title:
`case_package_v2_post_cleanup_parity_review_v0`

Purpose:
Run a read-only post-cleanup parity review for the five v2 pilot cases after `case_package_v2_reference_cleanup_execution_v0`.

Pilot cases:
- `PERF_0006`
- `PERF_0007`
- `CONS_0005`
- `PORT_0003`
- `LONGTAIL_0011`

Scope:
- Compare current case trees against the clean v2 template after nested SQL compatibility dirs and copied case-local notes have been removed.
- Confirm remaining gaps are limited to approved compatibility assets such as `runs/`, case-local evidence, schema engine copies, metadata source-of-truth files, data fixtures, validation engine-specific scripts, and PORT dialect variants.
- Confirm v2 static validator passes for all five cases.

Hard boundaries:
- Do not modify case packages.
- Do not delete retained evidence.
- Do not delete runs.
- Do not delete schema engine files.
- Do not delete metadata, data fixtures, validation scripts, or PORT dialect variants.
- Do not modify `case_sets/`, inventory, reports, results, denominators, paper results, or raw legacy evidence.
- Do not run DB/checker execution.
- Do not compute official metrics.
- Do not create leaderboard output.

Expected output:
- Post-cleanup parity summary.
- Remaining gap matrix.
- Protected boundary checks.
- Exact next safe action.
