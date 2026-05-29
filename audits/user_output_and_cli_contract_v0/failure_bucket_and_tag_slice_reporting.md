# Failure Bucket And Tag-Slice Reporting

## Placement

Machine-readable:

- `output/results/<run_id>/failure_buckets.csv`
- `output/results/<run_id>/tag_slices.csv`

Human-readable:

- `output/reports/<run_id>/failure_buckets.md`
- `output/reports/<run_id>/tag_slices.md`

## `failure_buckets.csv`

Expected fields:

- `failure_bucket`
- `count`
- `engines`
- `pools`
- `representative_cases`
- `explanation`

Failure buckets should remain diagnostic and fail-visible. They must not hide adapter failures, execution failures, checker mismatches, unsupported/fail-closed rows, or label-only mismatches.

## `tag_slices.csv`

Expected fields:

- `tag_axis`
- `tag`
- `selected`
- `candidate_generated`
- `candidate_executable`
- `exact`
- `mismatch`
- `label_only_mismatch`
- `timed`
- `dominant_failure_bucket`
- `notes`

Tag slices are denominator-aware diagnostics, not scores or rankings.
