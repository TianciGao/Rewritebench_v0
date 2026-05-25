# Nightly Track A 120 Candidate Capture: SQLGlot and Calcite v0

This packet records a nightly candidate-SQL capture/reproduction attempt for three deterministic routes over Common-core v0 Track A 120:

- SQLGlot no-op
- SQLGlot optimize schema-aware
- Calcite HEP fail-closed

This is not D038 Step 3. It is not POCR annotation generation. It is not official POCR. It computes no metrics and promotes no paper-facing result.

## Local Output Roots

Local user-run outputs were written under:

- `output/results/sqlglot_noop_track_a_120_candidate_capture_v0/`
- `output/results/sqlglot_optimize_schema_aware_track_a_120_candidate_capture_v0/`
- `output/results/calcite_hep_fail_closed_track_a_120_candidate_capture_v0/`
- corresponding logs under `output/logs/<run_id>/`
- corresponding local reports under `output/reports/<run_id>/`

`output/` is local runtime output and is not committed.

## Capture Summary

| Route | Planned rows | Candidate-present rows | Main missing/fail-closed frontier |
| --- | ---: | ---: | --- |
| SQLGlot no-op | 120 | 115 | 5 PostgreSQL PORT parse failures |
| SQLGlot optimize schema-aware | 120 | 105 | 10 generation failures, 5 preflight-blocked rows |
| Calcite HEP fail-closed | 120 | 0 | 120 preflight-blocked rows because Calcite runtime env was not configured |

LearnedRewrite was intentionally skipped.

## Boundary

No live API call, API key read, DB/checker/timing run, POCR annotation JSONL generation, POCR Stage B validation, official metric computation, paper-facing metric promotion, retained-evidence promotion, leaderboard generation, top-level reports/results update, `runs/user` write, case package modification, or candidate SQL movement/copy/deletion occurred.

Next safe action: inspect the captured Track A 120 candidate manifests, then continue D038 Step 3 annotation JSONL artifact contract or authorize route-specific POCR annotation generation only after candidate capture quality is reviewed.
