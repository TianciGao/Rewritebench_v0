# Pilot Leftover Compatibility Directories Cleanup

## Purpose and Scope

This narrow writable cleanup removed only the leftover empty pilot compatibility directories reported by the Common-core 40 v2 final closeout blocker list. Target cases were `PERF_0006`, `PERF_0007`, `CONS_0005`, `PORT_0003`, and `LONGTAIL_0011`.

## Candidate Set

Checked 15 candidate directories: `notes/`, `sql/positives/`, and `sql/negatives/` for each target case.

## Cleanup Result

- Directories deleted: 15.
- Directories skipped: 0.
- Every deleted directory was empty, had no live path references, and had a direct replacement or policy replacement.
- `sql/pos_01.sql` and `sql/neg_01.sql` existed for every target case before deletion.
- `notes/` contained no files; stable public notes remain represented by README/manifest policy.

## Validation

- Target case v2 validators passed: 5/5.
- Full Common-core 40 static validator rerun passed: 40/40.
- Unit tests passed: 19/19.
- No DB/checker execution, official metrics, report rendering, or leaderboard creation was performed.

## Protected Boundary Summary

- Only the five target pilot case directories were affected, and only by empty directory removal.
- No tracked case file content changed.
- Schemas, `case_sets/`, inventory, reports/results, denominator files, paper results, and `evidence/cases/` were unchanged.
- PORT dialect variants were not deleted.

## Exact Next Safe Action

Rerun the read-only Common-core 40 v2 final closeout. If clean-template-minimal passes for all 40 cases, perform the separate `PERF_0077`/`PERF_0082` source-path provenance follow-up before public release closeout.
