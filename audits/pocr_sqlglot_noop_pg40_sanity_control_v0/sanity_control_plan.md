# Sanity Control Plan

1. Select an existing SQLGlot no-op PostgreSQL PG40 candidate root from prior inventory.
2. Verify it resolves 40/40 Common-core PostgreSQL candidates without generating or modifying candidate SQL.
3. Run checkpointed Stage A annotation with explicit live gate and a 40-call cap.
4. Replay the route-bound annotation JSONL through `sqlrb user pocr-diagnostic`.
5. Inspect Stage B output for no-op over-accept risk.
6. Commit only this audit packet and project-control updates; leave `output/` and `/tmp` uncommitted.

This is not official POCR.
No route-level POCR score is emitted.
No paper-facing metric is promoted.
Stage A annotation alone is not counted.
Stage B transformation-aware validation is diagnostic only.
Semantic guard atoms are not part of operation coverage numerator.
No global leaderboard is produced.
