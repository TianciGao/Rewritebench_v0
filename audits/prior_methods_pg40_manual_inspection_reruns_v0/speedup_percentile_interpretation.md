# Speedup Percentile Interpretation

- P10/P90 are distribution percentiles over exact + timed rows only.
- P90 does not mean route-level speedup.
- Route-level `GM Speedup Ratio` is the aggregate timing statistic from `local_metrics.py`.
- The timing-tail rows in this packet are selected for manual inspection of examples and tails, not for method ranking.
- These rerun metrics are manual-inspection rerun outputs, not automatic replacements for existing paper-facing canonical tables.
- LearnedRewrite is PostgreSQL-only external-runtime bounded evidence.
- LLM-R2 adapted GPT-5.4 is an adapted local diagnostic route, not original LLM-R2 paper reproduction.
- Any LLM rerun may drift; compare with prior audit packets before making paper wording changes.
