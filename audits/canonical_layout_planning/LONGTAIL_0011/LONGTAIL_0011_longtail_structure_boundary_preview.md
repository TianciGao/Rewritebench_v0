# LONGTAIL_0011 Long-Tail Structure Boundary Preview

This preview is planning-only. It proposes how future canonical metadata and README text should describe `LONGTAIL_0011` without creating workload-frequency claims.

## Structures Present

Static inspection of the legacy SQL shows these long-tail structures:

- CTE pipeline: the source query uses `RankedPosts` and `MaxRank`.
- Window function: the source and positive rewrite use `DENSE_RANK()`.
- Join: query logic joins `Posts` and `Users`.
- Grouping and aggregate: the source computes `MAX(PostRank)` by owner display name.
- Sort/order sensitivity: the final query orders by score and view count.
- Tie-sensitive semantics: the hard negative changes `DENSE_RANK()` to `ROW_NUMBER()`.
- Realistic multi-clause style: the query combines filters, joins, window ranking, CTEs, grouping, and final ordering.

No static evidence indicates set operations or outer joins in this case.

## Why This Is LONGTAIL

The case is LONGTAIL because it packages a realistic SQLStorm-derived StackOverflow query shape with a multi-step CTE/window strategy and tie-handling semantics. It is not primarily a PERF case because this migration plan does not create or evaluate timing, speedup, latency, ranking, or leaderboard evidence. It is not primarily a CONS case because the main stressor is structurally realistic SQL packaging rather than a narrowly isolated semantic guard. It is not primarily a PORT case because the central issue is not cross-dialect syntax adaptation.

## Evidence Supporting The Classification

- `manifest.yaml` records `source_family: SQLStorm`, `source_workload: stackoverflow`, and `source_query_identity: 6625.sql`.
- `source.sql` contains the CTE/window source shape.
- `rewrite_pos_01.sql` preserves the dense-rank tie semantics through a simplified CTE strategy.
- `rewrite_neg_01.sql` intentionally collapses ties using `ROW_NUMBER()`.
- Retained result evidence shows source/positive equality and negative divergence across PostgreSQL, MySQL, and Spark witness outputs.

## Boundary

This migration plan must not imply:

- that this case frequency is representative of the StackOverflow workload;
- that the case proves broad production workload coverage;
- that any denominator, paper table, leaderboard, or Common-core membership changed;
- that long-tail classification by itself admits or promotes the case.

Future `metadata/taxonomy.yaml` should use structural labels such as:

- `source_family: SQLStorm`
- `source_workload: stackoverflow`
- `longtail_structure: true`
- `sql_features: [cte, window_function, join, aggregate, sort]`
- `semantic_risks: [tie_handling, rank_function_substitution]`
- `workload_frequency_claim_created: false`

The public README should describe structural robustness without adding production-frequency claims.
