# Retry Batch Gate Review

Batch 1 call count: 100.

Batch 1 schema-valid yield: 87/100 = 0.870.

Provider error recurrence: no for provider_config_issue. Observed provider failures were HTTP 504/520, not 401 / insufficient-balance / unauthorized.

Batch 2 gate: pass.

Batch 2 call count: 100.

Reason: batch 1 yield was >= 50%, no route/candidate identity issue was detected, and the prior provider_config_issue did not recur. No further retry batch was run because the total live-call cap was reached at 203 calls including the probe.

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted. No blind full retry is run. POCR@planned and POCR@candidate remain D039 promotion views. POCR@curated remains deferred until a predeclared curated manifest exists. Track A 120 is not a leaderboard.
