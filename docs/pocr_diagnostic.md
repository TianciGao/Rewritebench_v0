# POCR Diagnostic CLI

`sqlrb user pocr-diagnostic` is an optional, default-off command for Positive Operation Coverage diagnostic support.

It writes local user-output files for inspecting POCR Stage A annotation status and transformation-aware Stage B diagnostics over existing candidate SQL. It does not create an official benchmark result.

Future candidate SQL roots should follow the D035-aligned storage contract in `candidate_sql_outputs.md`. Existing `runs/user` candidate roots may be referenced read-only for diagnostics, but should not be copied, moved, deleted, or normalized without inventory and retention mapping.

Annotation JSONL artifacts should follow the route-bound contract in `pocr_annotation_artifacts.md`. Annotation JSONL is required for replay with non-missing annotation rows. Annotation JSONL is diagnostic evidence, not official POCR.

## What It Is Not

- This is not official POCR.
- This does not compute a paper-facing metric.
- This does not emit a route-level POCR score.
- This is not a leaderboard.
- This does not run DB/checker/timing.
- This does not rerun baselines.
- This does not call live API in replay / annotation-missing mode.

Stage A annotation alone is not counted.

Stage B transformation-aware validation is diagnostic only.

Semantic guard atoms are not part of operation coverage numerator.

No route-level POCR score is emitted.

No paper-facing metric is promoted.

## Required Inputs

The command is disabled unless `--enable-pocr-diagnostic` is supplied.

Required arguments:

- `--enable-pocr-diagnostic`
- `--candidate-root`
- `--method-id`
- `--route-id`
- `--engine`
- `--run-id`
- `--output-root`

Optional argument:

- `--annotation-jsonl`

If `--annotation-jsonl` is absent, the command emits annotation-missing diagnostic rows. If `--annotation-jsonl` is present, the command replays existing annotation rows read-only, validates schema and route binding, and runs transformation-aware Stage B diagnostics for schema-valid rows.

## Annotation-Missing Example

This command reads an existing candidate root and emits annotation-missing rows. It does not call an API, read API keys, run DB/checker/timing, or rerun the baseline.

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

Expected diagnostic behavior:

- rows are emitted for resolved candidate rows;
- `annotation_status=annotation_missing`;
- `diagnostic_only=true`;
- `official_pocr_computed=false`;
- `route_level_pocr_aggregated=false`;
- `paper_metric_promoted=false`.

## Matching-Route Replay Example

This command replays an existing annotation JSONL artifact whose route ID matches the supplied `--route-id`.

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

Expected diagnostic behavior:

- reads the existing annotation JSONL file read-only;
- makes no live API call;
- validates annotation schema and route binding;
- runs transformation-aware Stage B diagnostics for schema-valid rows;
- keeps malformed or schema-invalid rows fail-closed;
- keeps `official_pocr_computed=false`, `route_level_pocr_aggregated=false`, and `paper_metric_promoted=false`.

The current Direct LLM PG40 matching-route replay smoke emitted 40 rows, with 33 schema-valid rows, 7 schema-invalid fail-closed rows, 41 transformation-supported operation atoms, 13 presence-only operation atoms, and 33 insufficient-transformation-evidence operation atoms. These are diagnostic counts only, not official POCR and not a route-level score.

## Route-Mismatch Fail-Closed Example

Annotation artifacts are route-bound evidence. They are not reusable across arbitrary route labels.

If the same annotation JSONL is replayed with:

```text
--route-id direct_llm_original_pg40_user_replay
```

while the annotation artifact contains:

```text
direct_llm_original_pg40_pocr_diagnostic
```

the replay fails closed with schema-invalid route-mismatch diagnostics. Operation atoms are not promoted from route-mismatched annotations.

## Output Tree

The command writes under the caller-provided output root using the D035 user-output shape:

```text
output/results/<run_id>/pocr/diagnostic_rows.csv
output/results/<run_id>/pocr/diagnostic_summary_by_pool.csv
output/logs/<run_id>/pocr/pocr_diagnostic.log
output/reports/<run_id>/pocr_diagnostic.md
```

For local examples, use `/tmp/.../output` as the output root. Do not commit generated `output/` artifacts.

## POCR Evidence Boundaries

Operation atoms come only from case-local root-level `skills.md`.

Do not infer operation atoms from taxonomy, SQL shape, positive SQL, source SQL, candidate SQL, retained evidence, or ad hoc analysis.

`candidate_sql_span`, `source_sql_span`, and `positive_sql_span` alone are not operation coverage evidence. Operation support requires transformation-aware Stage B evidence relative to source.

The generated Markdown report must include:

- Positive Operation Coverage diagnostic support
- This is not official POCR.
- Stage A annotation alone is not counted.
- Stage B transformation-aware validation is diagnostic only.
- Semantic guard atoms are not part of operation coverage numerator.
- No route-level POCR score is emitted.
- No paper-facing metric is promoted.
