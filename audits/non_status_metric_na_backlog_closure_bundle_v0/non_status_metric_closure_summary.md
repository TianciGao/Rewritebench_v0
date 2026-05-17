# Non-status Metric N.A. And Backlog Closure Bundle v0

## Purpose And Scope

This packet closes the A-line v0 treatment for Metrics Contract v1 primary metrics that are not already handled by the limited official status-metrics path.

No new metrics were computed. No official metrics were computed or recomputed. No adapters were implemented. No paper tables were rendered. No `reports/` or `results/` files were created or updated. Denominator values, case membership, paper results, raw legacy evidence, and prior metric outputs were unchanged.

## Metrics Reviewed

- Semantic Equivalence Rate
- GM_Speedup
- Speedup Ratio Percentiles
- Attribution Coverage
- Cross-Engine Execution
- Cross-Engine Consistency
- Speedup Retention

## Recommended v0 Treatment

- Semantic Equivalence Rate: include audit-only support evidence only. Verifier references may remain support artifacts, but no official Semantic Equivalence Rate is available for v0.
- GM_Speedup: report as blocked. Timing adapter, timing eligibility, exact+timed denominator, and speedup interpretation are absent.
- Speedup Ratio Percentiles: report as blocked. The same timing adapter and exact+timed denominator blockers apply, with an additional percentile-output gate.
- Attribution Coverage: defer post-release. The attribution schema, eligibility denominator, and validated annotation pipeline are not approved.
- Cross-Engine Execution: defer post-release. Portability candidate rows and a portability denominator are not implemented or validated.
- Cross-Engine Consistency: defer post-release. Cross-engine checker policy and portability adapter output are not implemented or validated.
- Speedup Retention: report as N.A. for v0. Paired source/target result-consistent timing is unavailable.

## Rationale

Metrics Contract v1 requires non-status metrics to use validated record types and denominators. The retained-evidence maps show support references for verifier, timing, plan/observability, and portability evidence, but those references are not canonical metric rows. They require future adapters, row-grain validation, public hygiene review, and separate metric authorization before computation.

Semantic verifier support is useful as audit-only evidence, but it must not be overclaimed as Semantic Equivalence Rate. Timing artifacts exist as raw or reference material, but they must not be parsed into GM_Speedup or percentiles without a timing adapter and timing eligibility policy. Portability evidence is separate from Track A same-engine and must not be mixed into the 120-row same-engine denominator.

## Impact On A-line Closure

This closes the remaining non-status primary metrics for public v0 without adding metric values. A-line can now move toward a final renderer input package that carries:

- limited official status metrics for Execution Coverage Rate and Result Consistency Rate;
- blocked Generation Rate;
- audit-only Semantic Equivalence support;
- blocked performance metrics;
- N.A. Speedup Retention;
- post-release Attribution and Cross-Engine metrics.

## Next Safe Action

Run `a_line_final_renderer_input_package_v0` to package official limited metrics, blocked metrics, N.A. records, audit-only support, and post-release backlog decisions for a future renderer without rendering paper tables or writing `reports/` or `results/`.
