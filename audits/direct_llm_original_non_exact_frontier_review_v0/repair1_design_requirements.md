# Repair-1 Design Requirements

Repair-1 should be a second-stage local diagnostic route that consumes Direct LLM original output for the non-exact frontier. It must not mutate the original route output or reclassify Direct LLM original rows.

Required input source:

- Canonical Direct LLM original source run: `direct_llm_original_track_a_120_canonical_v0`
- Original candidate SQL and metadata from the Direct LLM original output
- Local checker and execution feedback from the canonical run
- No raw provider response bodies and no API key or environment values

Required row identity:

- `original_run_id`
- `case_id`
- `pool`
- `engine`
- `route_id=direct_llm_original`
- `method_id=direct_llm_original`
- `original_candidate_id={original_run_id}:{case_id}:{engine}:direct_llm_original`
- `original_candidate_sql_sha256`

Required feedback contract:

- `feedback_type`, one of:
  - `checker_mismatch_feedback`
  - `candidate_execution_error_feedback`
  - `unsupported_engine_boundary_feedback`
- `source_executable`
- `candidate_executable`
- `checker_attempted`
- `exact_status`
- `failure_bucket`
- `checker_or_error_summary`
- optional normalized execution error class
- optional checker mismatch artifact reference

Required Repair-1 prompt and output identifiers:

- `repair_prompt_template_id=direct_llm_repair_1_feedback_sql_only_v0`
- `repaired_candidate_id={original_candidate_id}:repair_1`
- `extraction_policy=single_sql_candidate_repair_v0`

Required provider/model metadata:

- `provider=openai_compatible`
- `base_url_host=api.gptsapi.net`
- `model_id=gpt-5.4`
- `temperature`
- `top_p`
- `max_tokens`
- `timeout`
- `user_agent=SQL-RewriteBench/0.1`
- `live_call=true` only when explicitly authorized
- `local_only=true`
- `official_metric_input=false`
- `paper_result=false`

Attempt policy:

- Attempt the 10 `mismatch` rows with checker mismatch feedback.
- Attempt the 3 `candidate_execution_failed` rows with candidate execution error feedback.
- Do not attempt the 5 `unsupported_engine` rows until a separate source-engine support policy changes.

Output policy:

- Repair-1 output should be written under a new local diagnostic run id.
- It should preserve a pointer to `original_candidate_id` for every attempted row.
- It should record repaired candidate SQL hash, extraction status, execution status, checker status, and fail-closed bucket.
- It should never overwrite Direct LLM original candidates or canonical metrics.
