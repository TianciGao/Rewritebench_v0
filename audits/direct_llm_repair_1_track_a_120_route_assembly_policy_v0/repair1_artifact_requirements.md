# Repair-1 Artifact Requirements

The future Track A 120 Repair-1 route must retain row-level artifacts sufficient to reconstruct final candidate provenance without secrets.

Required row metadata:

- `case_id`
- `pool`
- `engine`
- `route_id=direct_llm_repair_1`
- `method_id=direct_llm_repair_1`
- `original_route_id=direct_llm_original`
- `original_method_id=direct_llm_original`
- `original_run_id`
- `original_candidate_id`
- `original_candidate_path`
- `original_failure_bucket`
- `feedback_type`
- `repair_attempted`
- `repair_prompt_template_id`
- `repaired_candidate_id`
- `repaired_candidate_path`
- `final_candidate_source`: `original`, `repaired`, or `none`
- `final_status`
- provider and model metadata without secret values
- `base_url_host`
- `temperature`
- `top_p`
- `max_tokens`
- `timeout`
- `extraction_policy`
- `extraction_status`
- `live_call`
- `local_diagnostic_only=true`
- `official_metric_input=false`
- `paper_result=false`
- `retained_evidence_promoted=false`
- verifier status placeholder or coverage-limited status

Required row execution/checker/timing metadata:

- `final_candidate_generated`
- `source_executable`
- `final_candidate_executable`
- `checker_attempted`
- `exact`
- `mismatch`
- `timing_attempted`
- `timing_success`
- `candidate_sql_sha256` for the final candidate when generated
- `fail_closed_bucket` when no final candidate exists or a row is unsupported

Secret boundary:

- Do not write API key values.
- Do not write Authorization header values.
- Do not commit env files.
- Provider metadata must be limited to provider id, base URL host, model id, parameter values, and presence-only checks.
