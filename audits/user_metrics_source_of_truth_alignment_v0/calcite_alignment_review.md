# Calcite Alignment Review

Reviewed packets:

- `audits/calcite_hep_pg_local_metrics_projection_v0/`
- `audits/calcite_hep_pg_post_quoting_chain_rerun_v0/`
- `audits/calcite_vs_sqlglot_noop_pg_local_comparison_v0/`

Findings:

- `calcite_hep_pg_local_metrics_projection_v0` is a projection over prior audit outputs. It has `route_card.json` and `route_card.csv`, but no canonical source run and no `local_metrics.py` outputs.
- `calcite_hep_pg_post_quoting_chain_rerun_v0` generated candidate, execution/checker, timing, and route-card outputs using `run_post_quoting_chain.py`. Its `route_card.json` and `route_card.csv` were computed by the audit helper.
- `calcite_vs_sqlglot_noop_pg_local_comparison_v0` consumed helper route cards and generated a comparison table. It is not a canonical metrics comparison.

Correction plan:

1. Treat existing Calcite route-card and comparison outputs as provisional audit summaries.
2. Re-run or reprocess Calcite through the user facade so a standard source run exists.
3. Run `compute-local-metrics` on the standard source run.
4. Rebuild any Calcite comparison only from canonical `local_metrics.py` outputs.

If Calcite still requires route-specific schema-fallback policy or external runtime handling not expressible through the facade, that is a user-facade/runtime gap and should be fixed or documented before a canonical Calcite route-card claim.
