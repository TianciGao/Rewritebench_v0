# A-line Final Closure Recommendation

## Recommendation

Continue A-line only long enough to close metric treatment decisions. Do not implement new adapters or compute new metrics before moving to B-line work.

## Remaining A-line Tasks

Recommended remaining A-line tasks: 3 core tasks.

1. `generation_rate_blocker_final_decision`
2. `non_status_metric_na_backlog_closure_bundle`
3. `a_line_final_renderer_input_package`

Optional detail tasks may split timing/performance or semantic/cross-engine closure if the maintainer wants narrower review, but they can be combined into the non-status closure bundle.

## Metrics To Freeze As Official v0

- Execution Coverage Rate: include as limited official status metric.
- Result Consistency Rate: include as limited official status metric.

Both require denominator-visible and limited-scope caveats. Neither is a paper result yet.

## Metrics To Block Or Mark N.A.

- Generation Rate: blocked until observed generated evidence and inferred-generated policy are resolved.
- Semantic Equivalence Rate: blocked until verifier support and decidability policy exist.
- GM_Speedup: blocked until timing eligibility and timing adapter exist.
- Speedup Ratio Percentiles: blocked until timing eligibility and percentile implementation exist.
- Speedup Retention: report as N.A. for v0 because paired portability timing is unavailable.

## Metrics To Defer Post-release

- Attribution Coverage: defer to attribution schema and evidence pipeline.
- Cross-Engine Execution: defer unless a portability packet adapter is separately authorized.
- Cross-Engine Consistency: defer with Cross-Engine Execution.

## Switch To B-line?

Switch to B-line after the three core A-line decision tasks above are complete. B-line should not inherit unresolved metric ambiguity; it should receive a renderer input package that explicitly labels official, blocked, N.A., and post-release metrics.

## Next Exact Codex Task

`generation_rate_blocker_final_decision_v0`: decide whether Generation Rate remains blocked for v0, becomes diagnostic-only, or receives a narrowly authorized observed-evidence completion task. No metric computation, no renderer, no reports/results writes.
