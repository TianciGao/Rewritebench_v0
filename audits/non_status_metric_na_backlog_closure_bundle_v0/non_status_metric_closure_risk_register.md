# Non-status Metric Closure Risk Register

## Verifier Support Overclaimed As Semantic Equivalence Rate

Verifier references are support evidence only. They must not become Semantic Equivalence Rate until a verifier support adapter, row-grain validation, decidability policy, and metric computation task are separately authorized.

## Timing Evidence Used Without Exact+Timed Denominator

Raw timing references and timing logs are not metric inputs. GM_Speedup requires result-consistent timed rows with timing eligibility and validated `speedup_ratio`.

## Speedup Percentiles Computed From Biased Timed Subset

Percentile tables can be misleading if missing timing, unsupported rows, or non-exact rows are dropped silently. A future percentile task must preserve missingness and denominator partitions.

## Attribution Coverage Overclaimed Without Validated Annotations

Plan availability, PlanFrontier, and LLM-proposed annotations are support material. They do not establish Attribution Coverage without an attribution schema, eligibility denominator, and validation pipeline.

## Cross-engine Evidence Mixed Into Same-engine Track A

Portability rows use separate semantics and must not reuse Track A same-engine denominators or appear in a same-engine leaderboard.

## Speedup Retention Computed Without Paired Timing

Speedup Retention requires source and target timing on paired result-consistent portability rows. Missing target timing is `N.A.`, not zero and not failure.

## N.A. Values Hidden

N.A. records must remain visible in renderer input packages. Hiding N.A. values would imply unsupported metrics were silently excluded.

## Post-release Backlog Hidden

Attribution Coverage and Cross-Engine metrics are post-release backlog for v0. A future renderer must not imply they were omitted accidentally or computed elsewhere.

## Paper Renderer Overstates Metric Coverage

A renderer must distinguish limited official status metrics, blocked metrics, N.A. metrics, audit-only support, and post-release backlog. No main paper table should imply the full Metrics Contract v1 suite is computed for v0.
