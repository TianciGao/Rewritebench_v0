# Direct LLM Original PG40 Diagnostic POCR Pass v0

This packet runs one diagnostic-only POCR Stage A/Stage B pass over existing Direct LLM original PostgreSQL Common-core 40 candidate SQL. It uses the transformation-aware D037 Stage B policy and writes audit-only outputs.

- selected candidate root: `runs/user/direct_llm_original_track_a_120_canonical_v0__postgres/candidate_sql`
- Common-core PG rows resolved: 40
- live calls attempted: 40
- provider/model: `openai_compatible` / `gpt-5.4`
- schema-valid annotations: 33
- malformed/schema-invalid annotations: 7
- transformation-supported operation atoms: 41
- presence-only operation atoms: 13
- insufficient-transformation-evidence operation atoms: 33
- rejected-noop-equivalent operation atoms: 0

This is not official Positive Operation Coverage Rate, not route-level POCR aggregation, not user-output integration, not a baseline rerun, and not paper-facing metric promotion.
