# Repair-1 Spark Quality Review

After retry, Direct LLM Repair-1 Spark improved from 3 schema-valid rows and 37 fail-closed rows to 37 schema-valid rows and 3 fail-closed rows.

Stage B counts after retry:
- supported atoms: 44
- presence-only atoms: 15
- insufficient-evidence atoms: 39

The previous zero POCR was primarily an annotation/provider failure artifact, not evidence that Spark Repair-1 candidates lacked transformations. Remaining fail-closed rows should be handled by another bounded retry or manual annotation review before paper-facing promotion review. Stage B under-accept is not the dominant explanation after this retry, but a manual review of low-support exact rows remains prudent.

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted. No blind full retry is run. POCR@planned and POCR@candidate remain D039 promotion views. POCR@curated remains deferred until a predeclared curated manifest exists. Track A 120 is not a leaderboard.
