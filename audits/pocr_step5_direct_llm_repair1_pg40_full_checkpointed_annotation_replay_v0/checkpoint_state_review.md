# Checkpoint State Review

Checkpoint state local path:

`output/results/pocr_annotation_direct_llm_repair1_pg40_checkpointed_full_v0/pocr/annotations/direct_llm_repair_1/direct_llm_repair_1_pg40_pocr_diagnostic/postgres/checkpoint_state.json`

```json
{
  "diagnostic_only": true,
  "jsonl_rows": 40,
  "official_pocr_computed": false,
  "paper_metric_promoted": false,
  "route_level_pocr_aggregated": false,
  "rows": 40,
  "run_id": "pocr_annotation_direct_llm_repair1_pg40_checkpointed_full_v0",
  "status_counts": {
    "malformed_json": 3,
    "schema_valid": 35,
    "timeout": 2
  },
  "updated_at_utc": "2026-05-26T13:05:23.851659+00:00"
}
```

The checkpoint state records 40 manifest rows, 40 safe JSONL rows, diagnostic-only flags, and no official POCR computation.
