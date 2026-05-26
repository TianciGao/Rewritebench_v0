# Step 5 Plan

Selected baseline: Direct LLM Repair-1 PostgreSQL PG40.

Planned flow:

1. Select complete Repair-1 PG40 candidate root.
2. Generate route-bound Stage A annotation JSONL with explicit live configuration.
3. Validate schema.
4. Replay through `sqlrb user pocr-diagnostic`.
5. Report diagnostic Stage B counts only.

Actual outcome: step 1 completed; step 2 did not produce an auditable annotation artifact after the first live subprocess attempt was terminated; steps 3-5 were blocked fail-closed.

No baseline rerun, DB/checker/timing run, candidate SQL generation, official POCR computation, route-level POCR aggregation, paper metric promotion, or leaderboard output occurred.
