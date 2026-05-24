# Track A 120 Existing Baseline Evidence Inventory

Task: `track_a_120_existing_baseline_evidence_inventory_v0`

Routes inventoried:

- `direct_llm_original` / `direct_llm_original_track_a_120_canonical_v0`
- `sqlglot_noop` / `sqlglot_noop_track_a_120_canonical_v0`
- `sqlglot_optimize_schema_aware` / `sqlglot_optimize_schema_aware_track_a_120_canonical_v0`
- `calcite_hep_fail_closed` / `calcite_hep_track_a_120_canonical_v0`

Inventory result:

- All four routes have canonical aggregate local metrics outputs.
- All four routes have aggregate ledgers and per-engine source-run ledgers.
- All four routes have per-engine `failures.csv`.
- All four routes have per-engine `tag_slices.csv` with axes `portability_risk`, `rewrite_opportunity`, and `sql_feature`.
- All four routes have recoverable candidate SQL for generated candidates under per-engine source runs.
- No formal verifier outputs exist for these four canonical routes.
- Exact-row verifier-pair inventory can proceed without rerunning adapters, DB execution, checker, timing, LLM calls, SQLSolver, or VeriEQL.

Analyses that can proceed without rerun:

- route-level canonical metric summary review from existing `local_metrics.py` outputs
- per-engine canonical metric summary review
- route-level failure-bucket inventory
- tag-aware failure slice analysis using existing source-run ledgers and tag slices
- verifier-pair inventory manifest generation over exact/result-consistent rows

No baseline must be rerun for the requested inventory. Formal verifier execution and POCR remain unavailable and require separate authorization.

Next safe action: proceed to Track A 120 tag-aware failure slice analysis if desired. Do not proceed to Repair-1 until metric, tag, and verifier evidence layers remain inventoried and reviewed.
