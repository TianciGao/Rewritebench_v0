# Direct Original Vs Repair-1 Review

After retry:
- Direct LLM original overall diagnostic POCR@planned / POCR@candidate: 0.422222222222 / 0.422222222222 with 111 schema-valid rows and 9 fail-closed rows.
- Direct LLM Repair-1 overall diagnostic POCR@planned / POCR@candidate: 0.344444444444 / 0.344444444444 with 95 schema-valid rows and 25 fail-closed rows.

The gap narrowed substantially after provider recovery, especially because Repair-1 Spark recovered from provider-failure concentration. Direct original remains higher in this diagnostic snapshot, but method superiority should not be claimed from this alone: remaining Repair-1 MySQL fail-closed concentration, route-id differences between PG40 and tri-engine Repair-1, candidate behavior, and Stage B evidence quality all need review.

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted. No blind full retry is run. POCR@planned and POCR@candidate remain D039 promotion views. POCR@curated remains deferred until a predeclared curated manifest exists. Track A 120 is not a leaderboard.
