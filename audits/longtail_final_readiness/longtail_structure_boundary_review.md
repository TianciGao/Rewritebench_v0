# LONGTAIL Structure Boundary Review

Date: 2026-05-16

This review explains why each remaining case belongs in LONGTAIL as structural robustness evidence. It does not create workload-frequency or production-frequency claims.

## LONGTAIL_0012

- LONGTAIL structure: window_function; subquery_in_from; outer_join; aggregation; sort_limit; complex_expression.
- Evidence basis: legacy manifest tags, source SQL structure, witness notes, and retained tri-engine result checks under `cases/LONGTAIL/LONGTAIL_0012/runs/`.
- What not to claim: do not claim this pattern is frequent in production, representative of workload frequency, or newly validated by this planning task.
- README/metadata phrasing: describe it as a structural robustness case with retained evidence and explicit no-frequency/no-new-result boundaries.
- Workload-frequency claim must be explicitly false: yes.
- Hard-negative boundary: `optional_vote_count_left_join_changed_to_inner_join`; maintainer approval required before migration records it as approved.

## LONGTAIL_0013

- LONGTAIL structure: cte; window_function; outer_join; aggregation; sort; complex_expression.
- Evidence basis: legacy manifest tags, source SQL structure, witness notes, and retained tri-engine result checks under `cases/LONGTAIL/LONGTAIL_0013/runs/`.
- What not to claim: do not claim this pattern is frequent in production, representative of workload frequency, or newly validated by this planning task.
- README/metadata phrasing: describe it as a structural robustness case with retained evidence and explicit no-frequency/no-new-result boundaries.
- Workload-frequency claim must be explicitly false: yes.
- Hard-negative boundary: `best_question_attachment_left_join_changed_to_inner_join`; maintainer approval required before migration records it as approved.

## LONGTAIL_0022

- LONGTAIL structure: cte; join; outer_join; aggregation; order_by.
- Evidence basis: legacy manifest tags, source SQL structure, witness notes, and retained tri-engine result checks under `cases/LONGTAIL/LONGTAIL_0022/runs/`.
- What not to claim: do not claim this pattern is frequent in production, representative of workload frequency, or newly validated by this planning task.
- README/metadata phrasing: describe it as a structural robustness case with retained evidence and explicit no-frequency/no-new-result boundaries.
- Workload-frequency claim must be explicitly false: yes.
- Hard-negative boundary: `comment_aggregation_grouping_fragmented_by_commenter`; maintainer approval required before migration records it as approved.

## LONGTAIL_0023

- LONGTAIL structure: cte; outer_join; aggregation; directed_graph_relation; order_by.
- Evidence basis: legacy manifest tags, source SQL structure, witness notes, and retained tri-engine result checks under `cases/LONGTAIL/LONGTAIL_0023/runs/`.
- What not to claim: do not claim this pattern is frequent in production, representative of workload frequency, or newly validated by this planning task.
- README/metadata phrasing: describe it as a structural robustness case with retained evidence and explicit no-frequency/no-new-result boundaries.
- Workload-frequency claim must be explicitly false: yes.
- Hard-negative boundary: `directed_postlink_inbound_outbound_semantics_collapsed`; maintainer approval required before migration records it as approved.

## LONGTAIL_0024

- LONGTAIL structure: cte; join; aggregation; temporal_min_max; order_by.
- Evidence basis: legacy manifest tags, source SQL structure, witness notes, and retained tri-engine result checks under `cases/LONGTAIL/LONGTAIL_0024/runs/`.
- What not to claim: do not claim this pattern is frequent in production, representative of workload frequency, or newly validated by this planning task.
- README/metadata phrasing: describe it as a structural robustness case with retained evidence and explicit no-frequency/no-new-result boundaries.
- Workload-frequency claim must be explicitly false: yes.
- Hard-negative boundary: `posthistory_revision_aggregation_fragmented_by_editor`; maintainer approval required before migration records it as approved.
