# Timing And Metrics Readiness

Timing readiness:

- Exact-gated timing exists.
- Current default policy is warmup 1, measured repetitions 5, timeout 30 seconds, median statistic.
- Timing must only run for exact/result-consistent rows.
- Non-exact, no-candidate, execution-failed, checker-mismatch, unsupported, or fail-closed rows must stay denominator-visible and non-timed.

Local metrics projection readiness:

- Local-only Generation Rate is available as generated / selected.
- Local-only Execution Coverage Rate is available as candidate executable / selected.
- Local-only Result Consistency Rate is available as exact / selected.
- Local-only GM speedup and percentiles are available over exact timed rows only.

Boundaries:

- Regression@20 must not be computed as a formal local metric in this readiness stage.
- Semantic Equivalence Rate must be N.A. unless corrected verifier evidence exists.
- No official metrics or paper tables are authorized by this plan.

Route notes:

- SQLGlot noop is ready to use this timing/metrics path for a local diagnostic Track A 120 rerun.
- SQLGlot optimize needs bounded D035 refresh first.
- Calcite HEP is PostgreSQL-only ready; MySQL/Spark/full-120 timing should remain blocked.
- LLM routes lack candidate-route readiness and timing metadata contracts.
