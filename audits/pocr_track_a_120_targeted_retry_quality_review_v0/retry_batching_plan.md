# Retry Batching Plan

Retry-eligible fail-closed rows: 235. Live retry cap: 150.

The cap is exceeded, so only batch1 is retried in this task. Selection follows the requested priority order: Direct LLM Repair-1 Spark first, SQLGlot optimize MySQL/Spark second, SQLGlot no-op MySQL/Spark control rows third, and remaining retryable rows deferred.

Eligible rows by priority bucket:
- 1_direct_llm_repair1_spark: 37 eligible, 37 selected for batch1.
- 2_sqlglot_optimize_mysql_spark: 71 eligible, 71 selected for batch1.
- 3_sqlglot_noop_mysql_spark_control: 71 eligible, 42 selected for batch1.
- 4_remaining_retryable: 56 eligible, 0 selected for batch1.

Deferred retry-eligible rows: 85.

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted. POCR@planned and POCR@candidate remain D039 promotion views. POCR@curated remains deferred until a predeclared curated manifest exists. Micro-average is diagnostic only and not the paper formula. Track A 120 is not a leaderboard.
