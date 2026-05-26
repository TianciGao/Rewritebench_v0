# Local Artifact Read-Only Review

Local Step 5 artifacts present: true.

Read-only inputs inspected if present:
- `output/results/pocr_annotation_direct_llm_repair1_pg40_checkpointed_full_v0/pocr/annotations/direct_llm_repair_1/direct_llm_repair_1_pg40_pocr_diagnostic/postgres/annotation_manifest.csv`
- `output/results/pocr_annotation_direct_llm_repair1_pg40_checkpointed_full_v0/pocr/annotations/direct_llm_repair_1/direct_llm_repair_1_pg40_pocr_diagnostic/postgres/safe_annotation_outputs.jsonl`
- `audits/pocr_step5_repair1_pg40_diagnostic_quality_review_v0/`

The extraction produced:
- retry candidate rows: 40 total, 5 retry-eligible;
- evidence-ref linter rows: 83;
- manual review rows: 60.

No local `output/` or `/tmp` files were modified. No annotation JSONL was generated or rewritten.
