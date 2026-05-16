# LONGTAIL Final Bounded Migration Summary

## Purpose And Scope

This audit records the bounded canonical migration of the five remaining LONGTAIL Common-core cases: LONGTAIL_0012, LONGTAIL_0013, LONGTAIL_0022, LONGTAIL_0023, and LONGTAIL_0024.

Actual migration performed: yes. Legacy repo modified: no. The migration was static and copy-first: no database engines were run, no evidence was regenerated, no timing workload was run, and no new benchmark result was created.

Common-core case-package migration moved from 35/40 to 40/40 because all five selected LONGTAIL cases passed validator v0.3 full-case and canonical-case modes, and the full Common-core regression passed 40/40.

## Per-Case Migration Summary

- LONGTAIL_0012: canonical package created; maintainer-approved hard-negative reason `optional_vote_count_left_join_changed_to_inner_join` recorded.
- LONGTAIL_0013: canonical package created; maintainer-approved hard-negative reason `best_question_attachment_left_join_changed_to_inner_join` recorded.
- LONGTAIL_0022: canonical package created; maintainer-approved hard-negative reason `comment_aggregation_grouping_fragmented_by_commenter` recorded.
- LONGTAIL_0023: canonical package created; maintainer-approved hard-negative reason `directed_postlink_inbound_outbound_semantics_collapsed` recorded.
- LONGTAIL_0024: canonical package created; maintainer-approved hard-negative reason `posthistory_revision_aggregation_fragmented_by_editor` recorded.

Each hard negative is documented as a checker control, not a method-generated failure.

## Spark Plan Sanitization

Spark plan text was published only as sanitized retained plan copies under each case's `evidence/retained_plans/spark/` directory. Raw Spark plan originals remain mapped in each `evidence/runs_retention.yaml` and were not modified. No raw Spark plan text was copied into public retained evidence.

## Validation Script Caveat

Copied validation scripts are retained legacy validation assets, not final public user runners. They were not executed during migration. Each package records that future public runner outputs must not write to case-local `runs/` by default.

## Public Hygiene And Boundaries

Public hygiene scan passed across the five new case packages and audit outputs. Denominator, paper results, Common-core membership, case_sets, reports, results, and raw legacy evidence are unchanged. Workload-frequency, production-frequency, speedup, timing, ranking, leaderboard, and new benchmark-result claims were not created.

## Validation Result

- Selected-case full-case validator: PASS 5/5.
- Selected-case canonical-case validator: PASS 5/5.
- Full Common-core full-case regression: PASS 40/40.
- Full Common-core canonical-case regression: PASS 40/40.
- Python compile, YAML parse, JSON parse, CSV row checks, public hygiene scan, and git checks are recorded for this task.

## Next Safe Action

Review the final LONGTAIL migration and then create a separate Common-core 40 case-package completion closeout if desired. Do not touch case_sets, reports, results, denominator files, or paper tables until a separate retained-evidence/reporting task is explicitly approved.
