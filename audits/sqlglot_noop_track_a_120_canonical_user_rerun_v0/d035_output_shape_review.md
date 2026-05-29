# D035 Output Shape Review

Runtime output was limited to:
- `/tmp/sqlrb_sqlglot_noop_track_a_120_canonical_user_rerun_v0/output/`

D035 directories observed under the temp root:
- `output/results/<run_id>/`
- `output/logs/<run_id>/`
- `output/reports/<run_id>/`

Per-engine exports were present for:
- `sqlglot_noop_track_a_120_canonical_v0__postgres`
- `sqlglot_noop_track_a_120_canonical_v0__mysql`
- `sqlglot_noop_track_a_120_canonical_v0__spark`

Aggregate metrics export was present for:
- `sqlglot_noop_track_a_120_canonical_v0`

No repository-level `output/`, top-level `reports/`, or top-level `results` artifacts were staged or committed.
