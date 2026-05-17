# Future Official Membership Files Plan

Date: 2026-05-17

This plan describes a future task that may create official staged/backlog membership files. It does not create those files now.

## Candidate Future Files

- `case_sets/staged_v0/manifest.yaml`
- `case_sets/staged_v0/cases.csv`
- `case_sets/backlog_v0/manifest.yaml`
- `case_sets/backlog_v0/cases.csv`

## Required Approval Inputs

- Maintainer approval of the staged/backlog criteria.
- Maintainer disposition for the seven unregistered directories.
- Confirmation that staged/backlog membership is non-denominator governance only.
- Confirmation that Common-core v0 remains fixed at 40 cases.
- Confirmation of CSV schemas and whether manual-review/exclude/defer rows should be separate files.

## Validation Gates

- Official staged + backlog + manual-review accounting must cover all 157 non-Common-core cases or explicitly defer/exclude rows.
- No Common-core case may appear in staged/backlog files unless separately mirrored as reference-only metadata.
- `case_sets/common_core_v0/` must not change.
- Denominator scaffolds must not change.
- Reports/results and paper tables must not change.
- The seven unregistered directories must be reconciled before official inclusion.

## Row-count Expectations From This Preview

- Proposed staged rows: 61.
- Proposed backlog rows: 76.
- Manual-review rows: 13.
- Orphan/unregistered review rows: 7.
- Duplicate/alias review rows: 0.
- Exclude/private/scratch rows: 0.
- Defer post-release rows: 0.

## No Denominator-change Rule

Official staged/backlog files, if created later, must include `denominator_changed: false`, `paper_results_changed: false`, and `common_core_membership_changed: false` fields or equivalent notes.

## No Common-core Membership-change Rule

Staged/backlog membership is governance metadata only. It must not alter Common-core 40 membership, Track A 120 planned denominator rows, paper results, or public v0 main-result scope.
