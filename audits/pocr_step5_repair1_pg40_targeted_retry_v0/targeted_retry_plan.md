
# Targeted Retry Plan

Target baseline: Direct LLM Repair-1 PostgreSQL PG40.

- method_id: `direct_llm_repair_1`
- route_id: `direct_llm_repair_1_pg40_pocr_diagnostic`
- engine: `postgres`
- candidate root: `runs/user/direct_llm_repair_1_track_a_120_canonical_v0__postgres/candidate_sql`
- source full annotation artifact: `output/results/pocr_annotation_direct_llm_repair1_pg40_checkpointed_full_v0/pocr/annotations/direct_llm_repair_1/direct_llm_repair_1_pg40_pocr_diagnostic/postgres`
- retry output root: `output/results/pocr_annotation_direct_llm_repair1_pg40_targeted_retry_v0/pocr/annotations/direct_llm_repair_1/direct_llm_repair_1_pg40_pocr_diagnostic/postgres`

The retry planner selected only rows whose original full-run status was `malformed_json` or `timeout`. Schema-valid rows were not retried. Candidate SQL was read-only and was not moved, copied, deleted, regenerated, normalized, or modified.

Live API calls were allowed only for the five selected retry rows with an explicit live gate. API key values came from environment only and were not printed or written.
