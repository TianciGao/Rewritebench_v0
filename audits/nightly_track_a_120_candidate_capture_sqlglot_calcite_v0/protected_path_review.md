# Protected Path Review

This task wrote local runtime candidate-capture outputs only under repository-local `output/`, and wrote committed audit/project-control documentation only.

## Protected Paths Not Modified

- `cases/`
- case-local root-level `skills.md`
- `skill/` folders
- top-level `reports/`
- top-level `results/`
- case-local `runs/`
- `runs/user/`
- `runs/user/**/candidate_sql`

No existing candidate SQL file was moved, copied, deleted, normalized, regenerated, rewritten, staged, or committed.

## Local Runtime Output

The following local output roots were created and intentionally left untracked:

- `output/results/sqlglot_noop_track_a_120_candidate_capture_v0/`
- `output/results/sqlglot_optimize_schema_aware_track_a_120_candidate_capture_v0/`
- `output/results/calcite_hep_fail_closed_track_a_120_candidate_capture_v0/`
- matching `output/logs/<run_id>/`
- matching `output/reports/<run_id>/`

`output/` is not committed.

## Boundary

No live API call, API key read, annotation JSONL generation, POCR annotation, POCR Stage B validation, DB/checker/timing run, local_metrics computation, official POCR computation, route-level POCR aggregation, paper-facing metric promotion, top-level reports/results update, denominator change, case membership change, paper result change, raw legacy evidence change, retained-evidence promotion, or leaderboard output occurred.
