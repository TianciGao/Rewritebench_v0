# LONGTAIL Final Readiness And Canonical Migration Planning Wave

Date: 2026-05-16

## Purpose And Scope

This readiness wave reviews the five remaining LONGTAIL Common-core cases together and prepares human-reviewable hard-negative and structure-boundary material for future canonical migration. It is not case migration, not Common-core 40 blind/bulk migration, not DB validation, not evidence regeneration, and not a reports/results/case_sets/denominator update.

Cases reviewed: `LONGTAIL_0012`, `LONGTAIL_0013`, `LONGTAIL_0022`, `LONGTAIL_0023`, and `LONGTAIL_0024`.

Current pool status: LONGTAIL is 1/6 canonical complete (`LONGTAIL_0011`) and 5/6 remaining. Common-core case-package migration remains 35/40 overall.

## Confirmed Boundaries

- PERF, CONS, and PORT are canonical complete at case-package level.
- `LONGTAIL_0011` is the completed LONGTAIL canonical reference pilot.
- This task did not touch `case_sets/`, `reports/`, `results/`, denominator files, paper tables, release case packages, or legacy files.
- Long-tail interpretation must be structural robustness only; no workload-frequency or production-frequency claim should be created.

## Per-Case Readiness Summary

- `LONGTAIL_0012`: ready for future migration after maintainer approval; hard-negative reason `optional_vote_count_left_join_changed_to_inner_join`; Spark plans need sanitization; validation scripts need retained-legacy caveat.
- `LONGTAIL_0013`: ready for future migration after maintainer approval; hard-negative reason `best_question_attachment_left_join_changed_to_inner_join`; Spark plans need sanitization; validation scripts need retained-legacy caveat.
- `LONGTAIL_0022`: ready for future migration after maintainer approval; hard-negative reason `comment_aggregation_grouping_fragmented_by_commenter`; Spark plans need sanitization; validation scripts need retained-legacy caveat.
- `LONGTAIL_0023`: ready for future migration after maintainer approval; hard-negative reason `directed_postlink_inbound_outbound_semantics_collapsed`; Spark plans need sanitization; validation scripts need retained-legacy caveat.
- `LONGTAIL_0024`: ready for future migration after maintainer approval; hard-negative reason `posthistory_revision_aggregation_fragmented_by_editor`; Spark plans need sanitization; validation scripts need retained-legacy caveat.

## Hard-Negative And Structure Boundary Summary

- All five cases have `source.sql`, `rewrite_pos_01.sql`, and `rewrite_neg_01.sql` in legacy.
- Retained result checks show source/positive equality and source/negative difference across PostgreSQL, MySQL, and Spark.
- The hard-negative reasons are clear from static SQL differences and legacy notes, but maintainer approval is still required before canonical migration records them as approved expected rejections.
- The README/metadata wording in future packages must state structural robustness only and explicitly avoid workload-frequency claims.

## Public Hygiene Summary

- All five cases have raw Spark plan text with `file:/tmp/...` traces and require sanitized public Spark plan copies in future migration.
- Validation scripts write into case-local `runs/` and must be retained as legacy validation assets, not final public runners.
- `LONGTAIL_0012` and `LONGTAIL_0013` have WSL-local wording in Spark validation script comments that should be neutralized in public copies.
- No raw stdout/stderr logs should be copied into public evidence.

## Recommended Migration Batch

Primary recommendation: migrate all five remaining LONGTAIL cases in one bounded final LONGTAIL batch after maintainer approval of the expected rejection wording. This is not blind Common-core 40 migration; it is a fixed five-case final LONGTAIL wave with one shared migration pattern.

Fallback recommendation: migrate `LONGTAIL_0012` and `LONGTAIL_0013` first as the SQLStorm pair, then migrate the Stack-substrate trio `LONGTAIL_0022`, `LONGTAIL_0023`, and `LONGTAIL_0024` after the first batch passes.

User approval is needed before migration to approve expected-rejection wording. During execution, the user should be reachable for abort-condition decisions but does not need to supervise every copy operation if the prompt is followed.

## Why Case Sets, Reports, Results, And Denominator Must Not Be Touched Yet

These cases are not canonical packages yet. Updating denominator, paper results, reports/results, or `case_sets/` before the final LONGTAIL migration and validation would mix planning status with benchmark result governance. Those updates remain out of scope until all Common-core case packages are canonical and a separate reports/results evidence-map task is approved.
