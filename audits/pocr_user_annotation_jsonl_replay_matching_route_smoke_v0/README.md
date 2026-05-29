# POCR User Annotation JSONL Replay Matching Route Smoke v0

This packet records a default-off user-facing POCR diagnostic replay smoke using the same route ID as the source Direct LLM PG40 annotation artifact. The smoke exercises `sqlrb user pocr-diagnostic --enable-pocr-diagnostic --annotation-jsonl` without live API calls, API-key reads, DB/checker/timing, baseline reruns, official POCR computation, route-level aggregation, paper metric promotion, or leaderboard output.

- Rows emitted: 40
- Schema-valid replay rows: 33
- Schema-invalid fail-closed rows: 7
- Route mismatch rows: 0
- Transformation-supported operation atoms: 41
- Presence-only operation atoms: 13
- Insufficient-transformation-evidence operation atoms: 33

All output rows preserve `diagnostic_only=true`, `official_pocr_computed=false`, `route_level_pocr_aggregated=false`, and `paper_metric_promoted=false`.
