# Quality Gate Review

Gate decision: `quality_review_needed`.

Passed gates:
- 120 planned rows per route are accounted in row metrics.
- Live calls attempted: 291, which is <= the 300-call cap.
- Route mismatch rows: 0.
- Candidate mismatch rows: 0.
- SQLGlot no-op possible over-accept cases: 0.
- SQLGlot optimize missing rows remain fail-closed and no no-op substitutes were used.
- POCR@curated remains NA / curated_manifest_missing.
- Official POCR was not computed and no paper metric was promoted.

Boundary gates:
- New MySQL/Spark annotation rows show a high provider_call_failed rate after the provider began failing broadly.
- Direct LLM Repair-1 Spark, SQLGlot no-op MySQL/Spark, and SQLGlot optimize MySQL/Spark should not be used for promotion review before targeted retry or provider quality review.

Recommended next step: targeted retry / Stage B quality review before any paper metric promotion review.

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted. POCR@planned and POCR@candidate remain D039 promotion views. POCR@curated remains deferred until a predeclared curated manifest exists. Micro-average is diagnostic only and not the paper formula. Track A 120 is not a leaderboard.
