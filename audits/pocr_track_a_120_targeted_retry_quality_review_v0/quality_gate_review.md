# Quality Gate Review

Gate decision: `quality_review_needed`.

- All diagnostic rows accounted: 480/480.
- Retry live calls attempted: 150 (cap 150).
- Route mismatch rows: 0.
- Candidate mismatch rows: 0.
- Schema-valid rows after retry batch: 230.
- Fail-closed rows after retry batch: 250.
- SQLGlot no-op possible over-accept cases: 0.
- POCR@curated remains NA / curated_manifest_missing.
- Official POCR was not computed and no paper metric was promoted.

Recommendation: quality_review_needed / retry_needed if fail-closed concentration remains high; otherwise human paper-promotion review may be considered only in a separately authorized task.

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted. POCR@planned and POCR@candidate remain D039 promotion views. POCR@curated remains deferred until a predeclared curated manifest exists. Micro-average is diagnostic only and not the paper formula. Track A 120 is not a leaderboard.
