# POCR Diagnostic Examples

These examples show the optional `sqlrb user pocr-diagnostic` command. They are local diagnostic examples only.

Positive Operation Coverage diagnostic support is default-off and requires `--enable-pocr-diagnostic`.

This is not official POCR.

Stage A annotation alone is not counted.

Stage B transformation-aware validation is diagnostic only.

Semantic guard atoms are not part of operation coverage numerator.

No route-level POCR score is emitted.

No paper-facing metric is promoted.

## Annotation-Missing Mode

```bash
sqlrb user pocr-diagnostic \
  --enable-pocr-diagnostic \
  --candidate-root runs/user/direct_llm_original_track_a_120_canonical_v0__postgres/candidate_sql \
  --method-id direct_llm_original \
  --route-id direct_llm_original_pg40_user_smoke \
  --engine postgres \
  --run-id pocr_user_smoke_annotation_missing_v0 \
  --output-root /tmp/sqlrb_pocr_user_smoke_annotation_missing_v0/output
```

Expected result: rows are emitted with `annotation_status=annotation_missing`, `diagnostic_only=true`, `official_pocr_computed=false`, `route_level_pocr_aggregated=false`, and `paper_metric_promoted=false`.

## Matching-Route Replay Mode

```bash
sqlrb user pocr-diagnostic \
  --enable-pocr-diagnostic \
  --candidate-root runs/user/direct_llm_original_track_a_120_canonical_v0__postgres/candidate_sql \
  --annotation-jsonl audits/pocr_real_route_direct_llm_pg40_diagnostic_v0/safe_annotation_outputs.jsonl \
  --method-id direct_llm_original \
  --route-id direct_llm_original_pg40_pocr_diagnostic \
  --engine postgres \
  --run-id pocr_user_replay_direct_llm_pg40_matching_route_v0 \
  --output-root /tmp/sqlrb_pocr_user_replay_direct_llm_pg40_matching_route_v0/output
```

Expected result: existing annotation JSONL is replayed read-only; schema-valid rows run transformation-aware Stage B; malformed or schema-invalid rows remain fail-closed.

## Route-Mismatch Fail-Closed Mode

If the same annotation JSONL is replayed with `--route-id direct_llm_original_pg40_user_replay` while the artifact route is `direct_llm_original_pg40_pocr_diagnostic`, rows fail closed due to route mismatch.

Annotation artifacts are route-bound evidence, not reusable across arbitrary route labels.

## Output

Use `/tmp/.../output` for examples. Generated output follows:

```text
output/results/<run_id>/pocr/diagnostic_rows.csv
output/results/<run_id>/pocr/diagnostic_summary_by_pool.csv
output/logs/<run_id>/pocr/pocr_diagnostic.log
output/reports/<run_id>/pocr_diagnostic.md
```

Do not commit generated `output/` artifacts.
