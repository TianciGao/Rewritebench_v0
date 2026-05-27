# POCR Provider Health Probe And Large Retry

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted. No blind full retry is run. POCR@planned and POCR@candidate remain D039 promotion views. POCR@curated remains deferred until a predeclared curated manifest exists. Track A 120 is not a leaderboard.

This task runs a capped provider health probe and gated larger retry batches after the provider balance/configuration fix.

Summary:
- Provider health probe live calls: 3.
- Probe schema-valid rows: 2.
- Retry batch 1 live calls: 100.
- Retry batch 1 schema-valid rows: 87.
- Retry batch 2 live calls: 100.
- Retry batch 2 schema-valid rows: 78.
- Total live calls: 203 / 203.
- Schema-valid retry/probe rows merged: 167.
- Replay rerun completed for 8 affected route-engine combinations.
- Aggregation rerun completed over 12 route-engine row metrics.

No DB/checker/timing or baseline rerun occurred.
