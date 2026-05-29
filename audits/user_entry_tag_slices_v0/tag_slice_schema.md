# Tag Slice Schema

`tag_slices.csv` is written under `runs/user/{run_name}/`.

Columns:

- `axis`
- `tag`
- `selected_rows`
- `candidate_generated_rows`
- `candidate_preflight_passed_rows`
- `candidate_preflight_failed_rows`
- `db_execution_attempted_rows`
- `candidate_executed_rows`
- `checker_attempted_rows`
- `exact_rows`
- `mismatch_rows`
- `execution_failed_rows`
- `checker_failed_rows`
- `source_like_rows`
- `timed_rows`
- `local_diagnostic_only`
- `official_metric`
- `leaderboard_input`
- `claim_boundary`
- `notes`

Every row has `local_diagnostic_only=true`, `official_metric=false`, and
`leaderboard_input=false`.

The claim boundary is:

`local diagnostic tag slice only; not a score, not official metrics, not paper evidence, not leaderboard input`

No tag score, ranking field, timing metric, speedup field, official metric name,
paper table, retained evidence promotion, reports/results update, or leaderboard
output is part of this schema.
