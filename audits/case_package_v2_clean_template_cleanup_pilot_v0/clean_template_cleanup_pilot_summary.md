# Clean Template Cleanup Pilot Summary

Task: `case_package_v2_clean_template_cleanup_pilot_v0`

Date: 2026-05-19

Branch: `feature/case-package-v2-external-schema`

## Purpose And Scope

This branch-only cleanup pilot reviewed the five v2 pilot cases and limited cleanup consideration to paths marked `ready_for_cleanup=true` in:

`audits/case_package_v2_template_parity_gap_review_v0/template_parity_cleanup_readiness.csv`

Pilot cases:

- `PERF_0006`
- `PERF_0007`
- `CONS_0005`
- `PORT_0003`
- `LONGTAIL_0011`

## Cleanup Decision

No files were removed.

The parity audit marked three cleanup areas as ready for each case: nested SQL compatibility directories, copied case-local notes, and placeholder-only `runs/`. During this task, each candidate was rechecked against live references. All candidate areas still have live manifest, README, checker, metadata, validation-script, or dev-script references, so deleting them in this task would create stale compatibility references.

## Candidate Areas Reviewed

- Nested SQL compatibility directories: skipped for all five cases because `compatibility.sql_legacy`, checker configs, metadata path records, old validation scripts, and dev scripts still reference `sql/positives/` or `sql/negatives/`.
- Copied case-local notes: skipped for all five cases because the external evidence notes exist, but manifests and READMEs still reference case-local `notes/`.
- Placeholder-only `runs/`: skipped for all five cases because manifests and READMEs still document `runs/README.md` as legacy retained-evidence compatibility state.

## Files Removed

None.

## Files Skipped

Fifteen cleanup candidates were skipped:

- Five nested SQL compatibility cleanup candidates.
- Five copied case-local notes cleanup candidates.
- Five placeholder-only `runs/` cleanup candidates.

## Protected Boundary Summary

- Retained evidence deleted: no.
- Case-local evidence deleted without mapping: no.
- Schema engine DDL/load files deleted: no.
- Metadata deleted: no.
- Data fixtures deleted: no.
- Engine-specific validation scripts deleted: no.
- `case_sets/` changed: no.
- Inventory changed: no.
- Reports/results changed: no.
- Denominator changed: no.
- Paper results changed: no.
- Official metrics computed: no.
- DB/checker execution run: no.
- Global leaderboard created: no.
- Legacy repo modified: no.

## Validation Summary

Static v2 validation was run for all five pilot cases and passed. Unit tests passed. Summary JSON boundary assertions passed. `git diff --check` passed.

## Exact Next Safe Action

Authorize a narrow compatibility-reference cleanup planning task that updates or removes stale manifest/README/checker/metadata/validation references first, then re-evaluates the same ready candidates for actual deletion without touching retained evidence, schema engine files, metadata source-of-truth files, data fixtures, DB/checker execution, official metrics, or leaderboard output.
