# Metadata Review

The adapter wrote `direct_llm_repair_1_status.json` in each per-row workspace
before the temporary source run was removed.

Observed per-row adapter metadata:

| case_id | route_id | method_id | feedback_type | provider | model_id | live_call | api_key_present |
|---|---|---|---|---|---|---|---|
| `CONS_0005` | `direct_llm_repair_1` | `direct_llm_repair_1` | `checker_mismatch_feedback` | `fake` | `gpt-5.4` | `false` | `false` |
| `LONGTAIL_0012` | `direct_llm_repair_1` | `direct_llm_repair_1` | `candidate_execution_error_feedback` | `fake` | `gpt-5.4` | `false` | `false` |

Required metadata was present in adapter status:

- `route_id=direct_llm_repair_1`
- `method_id=direct_llm_repair_1`
- `original_candidate_id`
- `feedback_type`
- `repair_prompt_template_id=direct_llm_repair_1_feedback_sql_only_v0`
- `repaired_candidate_id`
- `extraction_policy=single_sql_candidate_repair_v0`
- provider/model metadata
- `local_only=true`
- `official_metric_input=false`
- `paper_result=false`
- `retained_evidence_promoted=false`
- `leaderboard_input=false`

The exported user-output `run_manifest.json` also recorded
`local_diagnostic_only=true`, `official_metric_input=false`,
`paper_result_input=false`, `official_SER=false`, and `leaderboard_input=false`.
Because the smoke used a temporary wrapper as the adapter command, the exported
manifest route identity remained the generic wrapper-derived user-adapter route;
the Repair-1 route identity was verified in the adapter status metadata.

No API key values or secrets were present in reviewed metadata.
