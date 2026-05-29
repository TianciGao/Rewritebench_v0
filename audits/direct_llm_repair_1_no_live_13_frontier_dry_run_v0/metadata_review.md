# Metadata Review

Reviewed adapter status metadata for all 13 attempted rows before removing the temporary source-run directories.

| case_id | engine | feedback_type | repair_prompt_template_id | candidate_generated | extraction_status | preflight_status |
|---|---|---|---|---|---|---|
| `CONS_0005` | `postgres` | `checker_mismatch_feedback` | `direct_llm_repair_1_feedback_sql_only_v0` | `true` | `extracted` | `passed` |
| `PERF_0062` | `mysql` | `checker_mismatch_feedback` | `direct_llm_repair_1_feedback_sql_only_v0` | `true` | `extracted` | `passed` |
| `CONS_0005` | `mysql` | `checker_mismatch_feedback` | `direct_llm_repair_1_feedback_sql_only_v0` | `true` | `extracted` | `passed` |
| `CONS_0037` | `mysql` | `checker_mismatch_feedback` | `direct_llm_repair_1_feedback_sql_only_v0` | `true` | `extracted` | `passed` |
| `PORT_0004` | `mysql` | `checker_mismatch_feedback` | `direct_llm_repair_1_feedback_sql_only_v0` | `true` | `extracted` | `passed` |
| `PORT_0012` | `mysql` | `checker_mismatch_feedback` | `direct_llm_repair_1_feedback_sql_only_v0` | `true` | `extracted` | `passed` |
| `PORT_0013` | `mysql` | `checker_mismatch_feedback` | `direct_llm_repair_1_feedback_sql_only_v0` | `true` | `extracted` | `passed` |
| `PORT_0022` | `mysql` | `checker_mismatch_feedback` | `direct_llm_repair_1_feedback_sql_only_v0` | `true` | `extracted` | `passed` |
| `PORT_0024` | `mysql` | `checker_mismatch_feedback` | `direct_llm_repair_1_feedback_sql_only_v0` | `true` | `extracted` | `passed` |
| `CONS_0005` | `spark` | `checker_mismatch_feedback` | `direct_llm_repair_1_feedback_sql_only_v0` | `true` | `extracted` | `passed` |
| `CONS_0009` | `spark` | `candidate_execution_error_feedback` | `direct_llm_repair_1_feedback_sql_only_v0` | `true` | `extracted` | `passed` |
| `CONS_0011` | `spark` | `candidate_execution_error_feedback` | `direct_llm_repair_1_feedback_sql_only_v0` | `true` | `extracted` | `passed` |
| `LONGTAIL_0012` | `spark` | `candidate_execution_error_feedback` | `direct_llm_repair_1_feedback_sql_only_v0` | `true` | `extracted` | `passed` |

Every attempted row recorded the required Repair-1 adapter metadata:

- `route_id=direct_llm_repair_1`
- `method_id=direct_llm_repair_1`
- `original_candidate_id`
- `feedback_type`
- `repair_prompt_template_id=direct_llm_repair_1_feedback_sql_only_v0`
- `repaired_candidate_id`
- `extraction_policy=single_sql_candidate_repair_v0`
- provider/model metadata with `provider=fake` and `model_id=gpt-5.4`
- `local_only=true`
- `official_metric_input=false`
- `paper_result=false`
- `retained_evidence_promoted=false`
- `leaderboard_input=false`
- `live_call=false`
- `api_key_present=false`

The wrapper used by the facade explicitly removed `SQLRB_LLM_ALLOW_LIVE`, `SQLRB_LLM_API_KEY`, and `GPTSAPI_API_KEY` from the adapter process. No secret values were written to reviewed metadata.
