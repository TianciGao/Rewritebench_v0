# Command Examples Review

The docs include three command/example classes.

## Annotation-Missing

The annotation-missing example uses:

- `--enable-pocr-diagnostic`
- no `--annotation-jsonl`
- existing candidate root `runs/user/direct_llm_original_track_a_120_canonical_v0__postgres/candidate_sql`
- `/tmp/sqlrb_pocr_user_smoke_annotation_missing_v0/output`

Expected documented behavior:

- rows emitted;
- `annotation_status=annotation_missing`;
- `diagnostic_only=true`;
- `official_pocr_computed=false`;
- `route_level_pocr_aggregated=false`;
- `paper_metric_promoted=false`.

## Matching-Route Replay

The matching-route replay example uses:

- annotation JSONL `audits/pocr_real_route_direct_llm_pg40_diagnostic_v0/safe_annotation_outputs.jsonl`
- route ID `direct_llm_original_pg40_pocr_diagnostic`
- `/tmp/sqlrb_pocr_user_replay_direct_llm_pg40_matching_route_v0/output`

Expected documented behavior:

- reads existing annotation JSONL read-only;
- makes no live API call;
- validates schema;
- runs transformation-aware Stage B for schema-valid rows;
- keeps malformed/schema-invalid rows fail-closed.

## Route-Mismatch Fail-Closed

The route-mismatch example documents that replaying the same annotation JSONL with `--route-id direct_llm_original_pg40_user_replay` must fail closed because the annotation artifact route is `direct_llm_original_pg40_pocr_diagnostic`.

The docs state that annotation artifacts are route-bound evidence and are not reusable across arbitrary route labels.

All example output roots use `/tmp/.../output`, and the docs say not to commit generated `output/` artifacts.
