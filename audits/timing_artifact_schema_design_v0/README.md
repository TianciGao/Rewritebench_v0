# timing_artifact_schema_design_v0

Verdict: `completed_with_metadata_correction`

This audit/design packet defines the Phase 1 timing artifact schema for future exact-gated local timing diagnostics. It follows D032 and `latest_paper_metrics_timing_protocol_alignment_v0` and does not implement timing execution, timing collection, metrics computation, POCR, retained-evidence promotion, paper rendering, reports/results updates, or leaderboard output.

## Preflight Summary

- Branch: `feature/case-package-v2-external-schema`.
- Required prior commit present: `469b2b2 docs(audit): align latest paper metrics timing protocol`.
- Required prior audit present: `audits/latest_paper_metrics_timing_protocol_alignment_v0/`.
- D032 present in `project_control/DECISION_LOG.md`.
- `project_control/MIGRATION_RUN_LOG.md` contains the latest-paper alignment entry, but that older entry still records commit/push as pending. This task records the non-destructive correction that `latest_paper_metrics_timing_protocol_alignment_v0` finalized at commit `469b2b2` and was pushed to `origin/feature/case-package-v2-external-schema`.

## Design Summary

The proposed timing schema is row-grained, route-aware, denominator-aware, and exact-gated. Future timing artifacts must keep non-exact rows visible as timing-ineligible rather than dropping them from the performance surface.

Timing is paired:

- source and candidate timing samples are retained for the same row;
- both sides are measured in the same engine, environment, and local run context;
- summary joins preserve planned, generated, executed, exact, and timed stages;
- speedup is nullable and only meaningful for exact, fully timed rows.

## Boundary

This packet is local diagnostic design only. It does not authorize or perform official metrics, timing/speedup computation, reports/results updates, paper table rendering, retained-evidence promotion, denominator changes, case membership changes, POCR implementation, skill-folder creation, operation-atom inference, release/export/tag creation, or leaderboard output.

## Files In This Packet

- `timing_row_schema.md`
- `timing_policy_schema.md`
- `timing_environment_metadata_schema.md`
- `timing_status_and_na_policy.md`
- `exact_gating_and_denominator_policy.md`
- `local_vs_official_timing_boundary.md`
- `integration_points_with_user_run.md`
- `future_metrics_join_plan.md`
- `open_questions_for_human.md`
- `protected_surface_check.md`
- `command_log.md`
- `boundary_checklist.md`

The reusable draft spec is also recorded at `repository_spec/timing_artifact_schema_v0_draft.md`.

## Recommended Next Safe Action

Review and approve the timing artifact schema and open questions before authorizing an exact-gated local timing diagnostic implementation task. That future task should still avoid official metrics, reports/results, retained evidence, paper rendering, and leaderboard output unless separately authorized.
