# timing_schema_open_questions_resolution_v0

Verdict: `completed`

This audit/design packet resolves the open timing schema questions from `timing_artifact_schema_design_v0` and records the approved defaults for a future Phase 2 exact-gated local timing diagnostic implementation.

This task is decision/audit only. It does not implement timing execution, metrics computation, speedup computation, POCR, skill folders, reports/results updates, retained-evidence promotion, paper rendering, Common-core runs, SQLGlot runs, or leaderboard output.

## Preflight Summary

- Branch: `feature/case-package-v2-external-schema`.
- Starting worktree: clean.
- Required timing schema design commit present: `032fc2e docs(audit): design timing artifact schema`.
- D032 present in `project_control/DECISION_LOG.md`.
- Local paper PDF: `Beyond_Faster_SQL (5).pdf` was not found under `/home/tianci_gao`, `/mnt/data`, or `/tmp`; defaults are resolved from D032, the latest-paper alignment audit, and the timing schema design packet.
- `project_control/DECISION_LOG.md` was not updated. D032 already records the durable project-level decision; this packet records Phase 2 implementation defaults and updates the timing schema draft.

## Approved Defaults Summary

- Local timing diagnostics are allowed before official retained-evidence promotion only with local-only claim boundary fields.
- Timing samples are stored inline in timing row JSON for v0.
- Timing artifacts must store `source_sql_hash` and `candidate_sql_hash`; schema/data hash pointers are optional if available.
- Source timing is not reused across routes in v0.
- Default local policy: `warmup_count=1`, `measured_repetitions=5`, `timeout_seconds=30`, `statistic=median`.
- Cache/session/schema policies are recorded as metadata rather than treated as fully controlled.
- Partial timing failures remain visible with `timing_status=partial_failure`; speedup remains null unless timing is complete.
- Label-only mismatches remain strict mismatches and timing-ineligible.
- Cross-engine timing requires target-engine paired source/reference timing and candidate timing in the same target-engine context.
- Promotion to official retained timing evidence requires a separate promotion task.
- Route mixing is disallowed for future summaries unless explicitly marked diagnostic and non-leaderboard.
- POCR remains deferred.

## Files In This Packet

- `resolved_open_questions.md`
- `approved_timing_defaults.md`
- `phase2_implementation_requirements.md`
- `remaining_risks.md`
- `protected_surface_check.md`
- `command_log.md`
- `boundary_checklist.md`

## Next Safe Action

Authorize a narrow exact-gated local timing diagnostic implementation only after reviewing this packet and the updated draft spec. That future implementation must remain local-only unless a separate retained-evidence/official timing promotion task is approved.
