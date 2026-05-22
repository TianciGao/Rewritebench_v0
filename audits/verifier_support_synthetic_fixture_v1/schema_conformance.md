# Schema Conformance

The implementation validates the required fields from `repository_spec/verifier_support_output_contract_v0_draft.md`.

`verifier_pairs.csv` required fields:

- `pair_id`
- `run_id`
- `tool`
- `case_id`
- `pool`
- `engine`
- `route_id`
- `method_id`
- `pair_type`
- `source_sql_path`
- `candidate_sql_path`
- `positive_sql_path`
- `negative_sql_path`
- `schema_context_path`
- `checker_context_path`
- `denominator_id`
- local-only boundary flags

`verifier_verdicts.jsonl` required fields:

- `pair_id`
- `tool`
- `tool_version`
- `invocation_status`
- `verdict`
- `raw_stdout_path`
- `raw_stderr_path`
- `runtime_ms`
- `timeout_seconds`
- `normalized_verdict`
- `verdict_reason`
- `artifact_paths`
- local-only boundary flags

`semantic_equivalence_summary.json` required fields:

- run and tool identity fields
- planned/attempted pair counts
- verdict bucket counts
- `decidable_count`
- `semantic_equivalence_rate`
- `verifier_decidability_rate`
- `na_reason`
- local-only boundary flags

Implementation adds `not_attempted_count`, `semantic_equivalence_rate_status`, `semantic_equivalence_source`, and `result_checker_exactness_used` for diagnostic clarity.
