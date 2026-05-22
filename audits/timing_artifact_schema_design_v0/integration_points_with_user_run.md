# Integration Points With User Run

This file sketches future integration points only. It does not implement timing in `user_run`.

## Placement In The Pipeline

Future timing collection should occur after:

1. candidate generation;
2. candidate preflight;
3. source/reference execution;
4. candidate execution;
5. local result checker;
6. strict exactness and role/support gating.

Timing should not run before the checker has established strict exactness.

## Runner Inputs

Future CLI flags might include:

- `--enable-timing`
- `--timing-policy <path-or-id>`
- `--timing-out <path>`
- `--timing-run-id <id>`

These are design placeholders only and are not authorized by this task.

## Ledger Integration

Future ledger rows should carry or join to:

- `timing_eligible`
- `timing_status`
- `timing_na_reason`
- `timing_artifact_path`
- `environment_metadata_path`
- `timing_policy_id`

Existing exact/mismatch and failure buckets should remain the source of timing eligibility.

## Quality Summary Integration

Future quality summaries can report local diagnostic counts:

- timing eligible rows;
- timed rows;
- timing N.A. rows by reason;
- timeout rows;
- partial failure rows.

These counts must stay local diagnostic summaries, not official metrics.

## Tag Slice Integration

Tag slices may join timing status fields for local diagnostic inspection. They must preserve route and engine grouping and must not become a global leaderboard or official paper table.

## Role Metadata

PORT and cross-engine timing must use resolved manifest local-diagnostic role metadata. Timing code must not infer target/source roles from filenames, SQL text, or directory names.
