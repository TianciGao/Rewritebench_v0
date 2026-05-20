# PERF_0077 / PERF_0082 Source-Path Follow-Up v0

## Purpose

This narrow follow-up reviewed the two remaining Common-core source-path provenance caveats for `PERF_0077` and `PERF_0082`. The task checked whether an exact source path or source-entry pointer could be recovered from current manifests, branch-history manifests, deleted branch-history provenance files, existing audit outputs, registry rows, and current source SQL comments.

## Scope

Reviewed cases:

- `PERF_0077`
- `PERF_0082`

No README, SQL, schema, checker, validation, case-set, inventory, reports/results, denominator, paper-result, or raw retained-evidence files were modified. No DB/checker execution, metrics computation, paper rendering, retained-evidence parsing, or leaderboard generation was performed.

## Evidence Checked

- Current target manifests: `cases/PERF/PERF_0077/manifest.yaml`, `cases/PERF/PERF_0082/manifest.yaml`.
- Current source SQL comments: `cases/PERF/PERF_0077/sql/source.sql`, `cases/PERF/PERF_0082/sql/source.sql`.
- Deleted branch-history provenance files at `42ef246^`: `metadata/provenance.yaml` for both cases.
- Pre-v2 branch-history manifests at `42ef246^`.
- Existing manifest caveat closeout outputs under `audits/case_package_v2_manifest_caveat_closeout_v0/`.
- Wave C and final closeout follow-up records that tracked the unresolved source-path caveat.
- `inventory/case_registry.csv`, `inventory/source_registry.csv`, and `case_sets/common_core_v0/cases.csv`.

## Result

No exact source path or source-entry pointer was recovered for either case. Branch-history provenance explicitly records `source_entry: ''` and `source_materialization: legacy case-local source.sql` for both `PERF_0077` and `PERF_0082`. Current SQL comments identify the JOB query identity or draft marker, but those comments do not provide a safe exact source path and were not used to fabricate one.

The source-path caveats are therefore explicitly closed as retained nonblocking provenance uncertainty for public release closeout. The manifests were not modified because no safe source-path field repair was supported by repository evidence. The existing manifest caveat remains visible and public-safe: `source_path: manual_review_required` plus `source_path_not_recovered`.

## Next Safe Action

Proceed to final public-release closeout planning, carrying the explicit note that `PERF_0077` and `PERF_0082` retain nonblocking source-path provenance uncertainty and no exact JOB source path is claimed.
