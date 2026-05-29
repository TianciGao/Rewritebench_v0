# Route Mismatch Triage

This is not official POCR. No route-level official POCR score is emitted. No paper-facing metric is promoted. POCR@planned and POCR@candidate remain D039 promotion views. POCR@curated remains deferred until a predeclared curated manifest exists. Track A 120 is not a leaderboard.

## Row Identity

- Case: `CONS_0011` / pool `CONS`.
- Expected route/method/engine: `direct_llm_repair_1_tri_engine_pocr_pilot_v0` / `direct_llm_repair_1` / `mysql`.
- Candidate SHA256: `562463408416e4f1188b8b571cb7e1b28150f5796a339531c05a0f3991e55146`.
- Candidate root: `runs/user/direct_llm_repair_1_track_a_120_canonical_v0__mysql/candidate_sql`.
- Annotation JSONL: `output/results/pocr_annotation_track_a120_final_retry_merged_direct_llm_repair1_mysql_v0/pocr/annotations/direct_llm_repair_1/direct_llm_repair_1_tri_engine_pocr_pilot_v0/mysql/merged_safe_annotation_outputs.jsonl`.
- Row metrics source: `output/results/pocr_user_replay_track_a120_final_retry_direct_llm_repair1_mysql_v0/pocr/stage_b/pocr_stage_b_row_metrics.csv`.

## Observed Identity

- Safe annotation row top-level route/method/engine: `direct_llm_repair_1_tri_engine_pocr_pilot_v0` / `direct_llm_repair_1` / `mysql`.
- Nested provider annotation route/method/engine: `direct_llm_repair_1_tri_pocr_pilot_v0` / `direct_llm_repair_1` / `mysql`.
- Replay row metrics route/method/engine: `direct_llm_repair_1_tri_engine_pocr_pilot_v0` / `direct_llm_repair_1` / `mysql`.
- Candidate mismatch: `false`.

## Likely Cause

The mismatch is isolated to the nested provider annotation route id: `direct_llm_repair_1_tri_pocr_pilot_v0` versus expected `direct_llm_repair_1_tri_engine_pocr_pilot_v0`. The safe annotation row envelope, method, engine, candidate SHA, and replay configuration are otherwise aligned. This points to a stale or mistyped annotation identity inside one provider JSON object, not to a candidate-root or replay-route selection issue.

## Isolated Or Systemic

The final row metrics contain one route mismatch row out of 480 diagnostic rows and zero candidate mismatch rows. This appears isolated.

## Recommended Disposition

Keep this row fail-closed for promotion-diagnostic POCR. A tiny route-id repair or targeted retry may be useful before a final paper freeze, but this isolated fail-closed row does not block preparing a paper-facing promotion review packet with an explicit boundary.

## Blocks Promotion Review

No, provided the promotion review packet carries the boundary: one isolated route mismatch was failed closed and no operation support was counted for it.
